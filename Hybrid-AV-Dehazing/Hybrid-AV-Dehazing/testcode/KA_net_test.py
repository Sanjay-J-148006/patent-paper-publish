import cv2
import numpy as np
import os
import glob

def pure_ka_net_dehaze(frame):
    """PURE dehazing - NO resize, original dimensions"""
    h, w = frame.shape[:2]
    
    # Dark Channel (NO resize)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
    dark_channel = cv2.erode(np.min(frame, axis=2), kernel)
    
    # Transmission (same size)
    A = np.percentile(dark_channel, 99.9)
    transmission = 1 - 0.95 * dark_channel / (A + 1e-7)
    
    # CLAHE enhancement (same size)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    dehazed_lab = cv2.merge([l, a, b])
    dehazed = cv2.cvtColor(dehazed_lab, cv2.COLOR_LAB2BGR)
    
    # Apply transmission (same size)
    dehazed = dehazed.astype(np.float32) * transmission[:,:,None]
    return np.clip(dehazed, 0, 255).astype(np.uint8)

# Batch process input/ → results/
input_paths = glob.glob("input/*.png") + glob.glob("input/*.jpg")
os.makedirs("results", exist_ok=True)

for path in input_paths:
    print(f"KA-Net: {os.path.basename(path)}")
    img = cv2.imread(path)
    dehazed = pure_ka_net_dehaze(img)
    cv2.imwrite(f"results/KA-Net_{os.path.basename(path)}", dehazed)
    print(f"✅ results/KA-Net_{os.path.basename(path)}")

print("✅ KA-Net images ready in results/")
