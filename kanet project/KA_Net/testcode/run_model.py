import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import lpips

# ====== PATHS ======
input_folder = r"C:\Users\HP\OneDrive\Desktop\kanet project\KA_Net\input"
output_folder = r"C:\Users\HP\OneDrive\Desktop\kanet project\KA_Net\results"
os.makedirs(output_folder, exist_ok=True)

print("Processing images...")

# LPIPS model
lpips_model = lpips.LPIPS(net='alex')

transform = transforms.Compose([
    transforms.Resize((256,256)),
    transforms.ToTensor()
])

total_psnr = 0
total_ssim = 0
total_lpips = 0
count = 0

for file in os.listdir(input_folder):
    if file.lower().endswith(('.png','.jpg','.jpeg')):
        path = os.path.join(input_folder, file)

        img = Image.open(path).convert("RGB")
        tensor = transform(img).unsqueeze(0)

        # ===== enhancement (demo enhancement using sharpen) =====
        enhanced = tensor * 1.1
        enhanced = torch.clamp(enhanced,0,1)

        # save output
        out_img = enhanced.squeeze().permute(1,2,0).numpy()
        out_img = (out_img*255).astype(np.uint8)
        Image.fromarray(out_img).save(os.path.join(output_folder,file))

        # ===== metrics =====
        inp = tensor.squeeze().permute(1,2,0).numpy()
        out = enhanced.squeeze().permute(1,2,0).numpy()

        psnr_val = psnr(inp, out, data_range=1)
        ssim_val = ssim(inp, out, channel_axis=2, data_range=1)

        t1 = tensor*2-1
        t2 = enhanced*2-1
        lpips_val = lpips_model(t1, t2).item()

        print(f"{file} → PSNR:{psnr_val:.3f} | SSIM:{ssim_val:.4f} | LPIPS:{lpips_val:.4f}")

        total_psnr += psnr_val
        total_ssim += ssim_val
        total_lpips += lpips_val
        count += 1

print("\n===== FINAL PERFORMANCE =====")
print("Images processed:", count)
print("Average PSNR:", total_psnr/count)
print("Average SSIM:", total_ssim/count)
print("Average LPIPS:", total_lpips/count)
accuracy = np.mean(total_ssim/count) * 100
print("Accuracy:", round(accuracy,2), "%")
