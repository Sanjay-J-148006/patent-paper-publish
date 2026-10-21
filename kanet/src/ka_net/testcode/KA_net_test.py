import argparse
import sys
import os
import time
import math
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np

# Ensure local testcode modules import correctly when running from repo root
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from view_testdata1 import TestData  # from test_data_real import TestData
from transweather_model import Transweather
from LD_model1 import Dehaze
from Utils import save_image_, PSNR_cal, SSIM_cal, psnr_, ssim_
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.metrics.pairwise import cosine_similarity
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def PSNR(img1, img2):
    b,_,_,_=img1.shape
    img1=np.clip(img1,0,255)
    img2=np.clip(img2,0,255)
    mse = np.mean((img1/ 255. - img2/ 255.) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 1
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
def ensure_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
def main():
    parser = argparse.ArgumentParser(description='Run KA_Net test')
    parser.add_argument('--test_dir', default=os.path.join(script_dir, '..', 'input'), help='Path to test images')
    parser.add_argument('--out_dir', default=os.path.join(script_dir, '..', 'results'), help='Output directory')
    parser.add_argument('--model',type=str,default=None)
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cuda', help='Device to run on')
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--synTest', action='store_true')
    parser.add_argument('--indoor', action='store_true')
    args = parser.parse_args()

    test_dir = args.test_dir
    test_store = args.out_dir
    ensure_dir(test_store)

    # validate test directory contains image files
    valid_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    imgs = [f for f in os.listdir(test_dir) if f.lower().endswith(valid_exts)]
    if len(imgs) == 0:
        print(f'ERROR: no images found in test_dir: {test_dir}')
        return

    device = 'cuda' if (args.device == 'cuda' and torch.cuda.is_available()) else 'cpu'

    if not args.model:
        print("Running in demo mode (no pretrained weights)")
        return

    if not os.path.isfile(args.model):
        print(f'ERROR: model file not found: {args.model}')
        return

    # load checkpoint
    ckp = torch.load(args.model, map_location=device)

    net = Dehaze(3, 3).to(device)
    if device == 'cuda' and torch.cuda.device_count() > 1:
        net = nn.DataParallel(net)

    # expecting checkpoint with 'model' key
    if isinstance(ckp, dict) and 'model' in ckp:
        net.load_state_dict(ckp['model'])
    else:
        try:
            net.load_state_dict(ckp)
        except Exception:
            print('Failed to load model state. Please check the checkpoint format.')
            return

    net.eval()

    batch_size = args.batch_size
    nyuhaze = False
    synTest = args.synTest
    indoor = args.indoor

    test_loader = DataLoader(TestData(test_dir, synTest, indoor), batch_size=batch_size)
    psnr = []
    ssim = []
    start = time.time()

    for j, data_ in enumerate(test_loader):
        with torch.no_grad():
            test_x, test_img_name = data_
            test_x = test_x.to(device)
            b, c, h, w = test_x.size()
            # adjust to multiple of 16 if needed
            if h % 16 != 0:
                h0 = h % 16
                if h0 % 2 == 0:
                    h1 = int(h0 / 2)
                    test_x = test_x[:, :, h1:(h - h1), :]
                else:
                    h1 = h0 % 2
                    test_x = test_x[:, :, h1:(h + h1 - h0), :]
            if w % 16 != 0:
                w0 = w % 16
                if w0 % 2 == 0:
                    w1 = int(w0 / 2)
                    test_x = test_x[:, :, :, w1:(w - w1)]
                else:
                    w1 = w0 % 2
                    test_x = test_x[:, :, :, w1:(w - w0 + w1)]

            try:
                predict_y, _ = net(test_x)
            except Exception as e:
                print(f'Error processing {test_img_name}: {e}')
                continue

        save_image_(predict_y, test_store, test_img_name)

    end = time.time() - start
    print(f'Elapsed: {end:.2f}s')


if __name__ == '__main__':
    main()

