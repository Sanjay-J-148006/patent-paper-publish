import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from view_testdata1 import TestData
from LD_model1 import Dehaze
import os
import time
import numpy as np
from Utils import save_image_
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import lpips

# -------------------- SETTINGS --------------------
test_dir = r"C:\Users\HP\OneDrive\Desktop\kanet project\KA_Net\input"
save_dir = r"C:\Users\HP\OneDrive\Desktop\kanet project\KA_Net\results"
os.makedirs(save_dir, exist_ok=True)

print("Running in demo mode (no pretrained model)")

# LPIPS model
lpips_model = lpips.LPIPS(net='alex')

# Model
device = "cpu"
net = Dehaze(3,3).to(device)
net = nn.DataParallel(net)
net.eval()

# Data
test_loader = DataLoader(TestData(test_dir, False, False), batch_size=1)

# Metrics counters
total_psnr = 0
total_ssim = 0
total_lpips = 0
count = 0

start = time.time()

# -------------------- TEST LOOP --------------------
for j, data_ in enumerate(test_loader):
    with torch.no_grad():
        test_x, test_img_name = data_
        test_x = test_x.to(device)

        predict_y, _ = net(test_x)

        # -------- SAVE OUTPUT --------
        save_image_(predict_y, "results", test_img_name)

        # -------- METRICS --------
        out_img = predict_y.squeeze().cpu().numpy().transpose(1,2,0)
        in_img = test_x.squeeze().cpu().numpy().transpose(1,2,0)

        out_img = np.clip(out_img,0,1)
        in_img = np.clip(in_img,0,1)

        psnr_val = psnr(in_img, out_img, data_range=1)
        ssim_val = ssim(in_img, out_img, channel_axis=2, data_range=1)

        t1 = (test_x*2-1)
        t2 = (predict_y*2-1)
        lpips_val = lpips_model(t1, t2).item()

        print(f"Image {j+1}: PSNR={psnr_val:.3f} dB | SSIM={ssim_val:.4f} | LPIPS={lpips_val:.4f}")

        total_psnr += psnr_val
        total_ssim += ssim_val
        total_lpips += lpips_val
        count += 1

# -------------------- FINAL RESULT --------------------
end = time.time() - start

print("\n===== FINAL PERFORMANCE =====")
print("Images processed:", count)

if count > 0:
    print("Average PSNR:", total_psnr/count)
    print("Average SSIM:", total_ssim/count)
    print("Average LPIPS:", total_lpips/count)

print("Total Time:", end)
