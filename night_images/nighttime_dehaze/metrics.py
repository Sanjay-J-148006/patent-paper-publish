import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import lpips
import torch

output_folder = "results/dehaze/output"
gt_folder = "dataset/REALNH/testB"

loss_fn = lpips.LPIPS(net='alex')
loss_fn.eval()

psnr_list=[]
ssim_list=[]
lpips_list=[]

files = os.listdir(output_folder)
total = len(files)
count = 0

print("\nStarting evaluation...\n")

for idx, img in enumerate(files):

    print(f"Processing {idx+1}/{total} : {img}")

    out_path = os.path.join(output_folder, img)
    gt_path = os.path.join(gt_folder, img)

    if not os.path.exists(gt_path):
        print("  → GT missing, skipped")
        continue

    out = cv2.imread(out_path)
    gt = cv2.imread(gt_path)

    if out is None or gt is None:
        print("  → Read error, skipped")
        continue

    out = cv2.resize(out,(gt.shape[1],gt.shape[0]))

    p = psnr(gt,out)
    s = ssim(gt,out,channel_axis=2)

    out_t = torch.tensor(out).permute(2,0,1).unsqueeze(0).float()/255
    gt_t  = torch.tensor(gt).permute(2,0,1).unsqueeze(0).float()/255

    lp = loss_fn(out_t,gt_t).item()

    psnr_list.append(p)
    ssim_list.append(s)
    lpips_list.append(lp)
    count+=1

print("\n==============================")
print("Total processed:",count)

print("\n===== FINAL PERFORMANCE =====")
print("PSNR:", round(np.mean(psnr_list),3))
print("SSIM:", round(np.mean(ssim_list),4))
print("LPIPS:", round(np.mean(lpips_list),4))
accuracy = np.mean(ssim_list) * 100
print("Accuracy:", round(accuracy,2), "%")

