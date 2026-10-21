import argparse
import logging
import os.path
import sys
import time
from collections import OrderedDict
import torchvision.utils as tvutils

import numpy as np
import torch
from IPython import embed
import lpips

import options as option
from models import create_model

sys.path.insert(0, "../../")
import open_clip
import utils as util
from data import create_dataloader, create_dataset
from data.util import bgr2ycbcr

#### options
parser = argparse.ArgumentParser()
parser.add_argument("-opt", type=str, required=True, help="Path to options YMAL file.")
opt = option.parse(parser.parse_args().opt, is_train=False)

opt = option.dict_to_nonedict(opt)

#### mkdir and logger
util.mkdirs(
    (
        path
        for key, path in opt["path"].items()
        if not key == "experiments_root"
        and "pretrain_model" not in key
        and "resume" not in key
    )
)

util.setup_logger(
    "base",
    opt["path"]["log"],
    "test_" + opt["name"],
    level=logging.INFO,
    screen=True,
    tofile=True,
)
logger = logging.getLogger("base")
logger.info(option.dict2str(opt))

#### Create test dataset and dataloader
test_loaders = []
for phase, dataset_opt in sorted(opt["datasets"].items()):
    test_set = create_dataset(dataset_opt)
    test_loader = create_dataloader(test_set, dataset_opt)
    logger.info(
        "Number of test images in [{:s}]: {:d}".format(
            dataset_opt["name"], len(test_set)
        )
    )
    test_loaders.append(test_loader)

model = create_model(opt)
device = model.device

if opt['path']['daclip'] is not None:
    clip_model, preprocess = open_clip.create_model_from_pretrained(
        'daclip_ViT-B-32',
        pretrained=opt['path']['daclip']
    )
else:
    clip_model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32',
        pretrained='laion2b_s34b_b79k'
    )

tokenizer = open_clip.get_tokenizer('ViT-B-32')
clip_model = clip_model.to(device)

sde = util.IRSDE(
    max_sigma=opt["sde"]["max_sigma"],
    T=opt["sde"]["T"],
    schedule=opt["sde"]["schedule"],
    eps=opt["sde"]["eps"],
    device=device
)
sde.set_model(model.model)
lpips_fn = lpips.LPIPS(net='alex').to(device)

scale = opt['degradation']['scale']
sampling_mode = opt["sde"]["sampling_mode"]

for test_loader in test_loaders:
    test_set_name = test_loader.dataset.opt["name"]
    logger.info("\nTesting [{:s}]...".format(test_set_name))
    test_start_time = time.time()
    dataset_dir = os.path.join(opt["path"]["results_root"], test_set_name)
    util.mkdir(dataset_dir)

    test_results = OrderedDict()
    test_results["psnr"] = []
    test_results["ssim"] = []
    test_results["psnr_y"] = []
    test_results["ssim_y"] = []
    test_results["lpips"] = []
    test_results["accuracy"] = []
    test_times = []

    for i, test_data in enumerate(test_loader):
        need_GT = False if test_loader.dataset.opt["dataroot_GT"] is None else True
        img_path = test_data["GT_path"][0] if need_GT else test_data["LQ_path"][0]
        img_name = os.path.splitext(os.path.basename(img_path))[0]

        LQ, GT = test_data["LQ"], test_data["GT"]
        img4clip = test_data["LQ_clip"].to(device)

        with torch.no_grad(), torch.cuda.amp.autocast():
            image_context, degra_context = clip_model.encode_image(img4clip, control=True)
            image_context = image_context.float()
            degra_context = degra_context.float()

        noisy_state = sde.noise_state(LQ)

        model.feed_data(
            noisy_state, LQ, GT,
            text_context=degra_context,
            image_context=image_context
        )

        tic = time.time()
        model.test(sde, mode=sampling_mode, save_states=False)
        toc = time.time()
        test_times.append(toc - tic)

        visuals = model.get_current_visuals()

        SR_img = visuals["Output"]
        output = util.tensor2img(SR_img.squeeze())
        LQ_ = util.tensor2img(visuals["Input"].squeeze())
        GT_ = util.tensor2img(visuals["GT"].squeeze())

        suffix = opt["suffix"]
        if suffix:
            save_img_path = os.path.join(dataset_dir, img_name + suffix + ".png")
        else:
            save_img_path = os.path.join(dataset_dir, img_name + ".png")
        util.save_img(output, save_img_path)

        if need_GT:
            gt_img = GT_ / 255.0
            sr_img = output / 255.0

            crop_border = opt["crop_border"] if opt["crop_border"] else scale
            if crop_border != 0:
                sr_img = sr_img[crop_border:-crop_border, crop_border:-crop_border]
                gt_img = gt_img[crop_border:-crop_border, crop_border:-crop_border]

            psnr = util.calculate_psnr(sr_img * 255, gt_img * 255)
            ssim = util.calculate_ssim(sr_img * 255, gt_img * 255)
            lp_score = lpips_fn(
                GT.to(device) * 2 - 1,
                SR_img.to(device) * 2 - 1
            ).squeeze().item()

            # ===== ACCURACY ADDED =====
            accuracy = psnr / 100.0
            # ===========================

            test_results["psnr"].append(psnr)
            test_results["ssim"].append(ssim)
            test_results["lpips"].append(lp_score)
            test_results["accuracy"].append(accuracy)

            logger.info(
                f"img{i:3d}:{img_name:15s} - "
                f"PSNR: {psnr:.6f} dB; "
                f"SSIM: {ssim:.6f}; "
                f"LPIPS: {lp_score:.6f}; "
                f"Accuracy: {accuracy:.4f}"
            )

    ave_lpips = sum(test_results["lpips"]) / len(test_results["lpips"])
    ave_psnr = sum(test_results["psnr"]) / len(test_results["psnr"])
    ave_ssim = sum(test_results["ssim"]) / len(test_results["ssim"])
    ave_accuracy = sum(test_results["accuracy"]) / len(test_results["accuracy"])

    logger.info(
        f"----Average Results for {test_set_name}----\n"
        f"\tPSNR: {ave_psnr:.6f} dB;\n"
        f"\tSSIM: {ave_ssim:.6f};\n"
        f"\tLPIPS: {ave_lpips:.6f};\n"
        f"\tAccuracy: {ave_accuracy:.4f}\n"
    )

    print(f"average test time: {np.mean(test_times):.4f}")
