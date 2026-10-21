import time, itertools
import torch
import os
import numpy as np
from dataset import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader
from networks import *
from utils import *
from glob import glob
from PIL import Image
from cv2 import resize
import cv2

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

class GAPSF(object):
    def __init__(self, args):
        self.result_dir = args.result_dir
        self.dataset = args.dataset
        self.datasetpath = args.datasetpath
        self.n_res = args.n_res
        self.ch = args.ch
        self.img_size = args.img_size
        self.have_gt = args.have_gt

        # Device auto-detection
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.device)

        print("# dataset :", self.dataset)
        print("# datasetpath :", self.datasetpath)

    def build_model(self):
        self.test_transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5),
                                 std=(0.5, 0.5, 0.5))
        ])

        self.testA = ImageFolder(os.path.join('dataset', self.datasetpath),
                                 self.test_transform)

        self.testA_loader = DataLoader(self.testA,
                                       batch_size=1,
                                       shuffle=False)

        self.genA2B = ResnetGenerator(
            input_nc=3,
            output_nc=3,
            ngf=self.ch,
            n_blocks=self.n_res,
            img_size=self.img_size
        ).to(self.device)

    def load(self, dir, name):
        model_path = os.path.join(dir, name)

        # IMPORTANT FIX: map_location for CPU safety
        params = torch.load(model_path, map_location=self.device)

        self.genA2B.load_state_dict(params['genA2B'])
        print("Model loaded successfully.")

    def test(self):
        model_list = glob(os.path.join(self.result_dir,
                                       self.dataset,
                                       'model',
                                       '*.pt'))

        if len(model_list) == 0:
            raise RuntimeError("No model .pt file found!")

        model_filename = os.path.basename(model_list[-1])
        print("Loading model:", model_filename)

        self.load(os.path.join(self.result_dir,
                               self.dataset,
                               'model'),
                  model_filename)

        self.genA2B.eval()

        path_realA = os.path.join(self.result_dir, self.dataset, 'input')
        path_fakeB = os.path.join(self.result_dir, self.dataset, 'output')
        path_AB = os.path.join(self.result_dir, self.dataset, 'input_output')

        os.makedirs(path_realA, exist_ok=True)
        os.makedirs(path_fakeB, exist_ok=True)
        os.makedirs(path_AB, exist_ok=True)

        input_folder = os.path.join('dataset', self.datasetpath)

        self.input_list = [
            os.path.splitext(f)
            for f in os.listdir(input_folder)
            if any(f.endswith(suffix) for suffix in IMG_EXTENSIONS)
        ]

        for n, in_name in enumerate(self.input_list):
            img_name = in_name[0]
            im_suf = in_name[-1]

            print(f'Predicting {n+1}/{len(self.input_list)}')

            img_path = os.path.join(input_folder,
                                    img_name + im_suf)

            img = Image.open(img_path).convert('RGB')
            img_width, img_height = img.size

            real_A = self.test_transform(img).unsqueeze(0).to(self.device)

            with torch.no_grad():
                fake_A2B, _, _ = self.genA2B(real_A)

            A_real = RGB2BGR(tensor2numpy(denorm(real_A[0])))
            B_fake = RGB2BGR(tensor2numpy(denorm(fake_A2B[0])))

            A_real = resize(A_real, (img_width, img_height))
            B_fake = resize(B_fake, (img_width, img_height))

            A2B = np.concatenate((A_real, B_fake), 1)

            cv2.imwrite(os.path.join(path_realA,
                        f'{img_name}{im_suf}'),
                        A_real * 255.0)

            cv2.imwrite(os.path.join(path_fakeB,
                        f'{img_name}{im_suf}'),
                        B_fake * 255.0)

            cv2.imwrite(os.path.join(path_AB,
                        f'{img_name}{im_suf}'),
                        A2B * 255.0)

        print("Test completed successfully.")