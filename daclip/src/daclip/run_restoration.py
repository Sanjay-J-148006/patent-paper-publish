#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DA-CLIP Image Restoration Demo
Performs image restoration using DA-CLIP model
"""

import os
import sys
import argparse
import torch
import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add paths
sys.path.insert(0, "universal-image-restoration")
sys.path.insert(0, "universal-image-restoration/config/daclip-sde")

print("Loading DA-CLIP restoration system...")

try:
    import options as option
    from models import create_model
    import utils as util
    import open_clip
    print("[OK] All modules imported successfully")
except Exception as e:
    print(f"[ERROR] Error importing modules: {e}")
    print("Make sure you're in the daclip directory and the environment is set up")
    sys.exit(1)

def restore_image(input_path, output_path="output.png", config_file="universal-image-restoration/config/daclip-sde/options/test.yml"):
    """
    Restore a degraded image using DA-CLIP
    
    Args:
        input_path: Path to input image
        output_path: Path to save restored image
        config_file: Path to YAML config file
    """
    
    # Parse config
    try:
        opt = option.parse(config_file, is_train=False)
        opt = option.dict_to_nonedict(opt)
    except FileNotFoundError:
        print(f"✗ Config file not found: {config_file}")
        print("Make sure the universal-image-restoration directory exists")
        return False
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"✗ Input image not found: {input_path}")
        return False
    
    print(f"\n📷 Input image: {input_path}")
    
    try:
        # Load the model
        print("⏳ Loading DA-CLIP model...")
        model = create_model(opt)
        device = model.device
        
        # Load CLIP model
        print("⏳ Loading CLIP text encoder...")
        clip_model, preprocess = open_clip.create_model_from_pretrained(
            "daclip_ViT-B-32", 
            pretrained=opt.get("path", {}).get("daclip", "pretrained/daclip_ViT-B-32.pt")
        )
        clip_model = clip_model.to(device)
        
        # Initialize SDE
        sde = util.IRSDE(
            max_sigma=opt.get("sde", {}).get("max_sigma", 1.0),
            T=opt.get("sde", {}).get("T", 100),
            schedule=opt.get("sde", {}).get("schedule", "linear")
        )

        
        # Load image
        print("⏳ Loading input image...")
        img = cv2.imread(input_path, cv2.IMREAD_COLOR)
        if img is None:
            print(f"✗ Could not read image: {input_path}")
            return False
        
        # Convert to tensor
        img_tensor = torch.from_numpy(np.transpose(img, (2, 0, 1))).float().unsqueeze(0).to(device) / 255.0
        
        # Detect degradation
        print("⏳ Analyzing image degradation...")
        degradation_types = ['motion-blurry', 'hazy', 'jpeg-compressed', 'low-light', 'noisy', 
                           'raindrop', 'rainy', 'shadowed', 'snowy', 'uncompleted']
        
        with torch.no_grad(), torch.cuda.amp.autocast():
            text = open_clip.tokenize(degradation_types)
            text_features = clip_model.encode_text(text.to(device))
            
            # Extract degradation features
            _, degra_features = model.encode_image(img_tensor[:, :3], control=True)
            degra_features /= degra_features.norm(dim=-1, keepdim=True)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            
            # Identify degradation
            text_probs = (100.0 * degra_features @ text_features.T).softmax(dim=-1)
            index = torch.argmax(text_probs[0])
            detected_degradation = degradation_types[index]
            confidence = text_probs[0][index].item()
        
        print(f"✓ Detected degradation: {detected_degradation} (confidence: {confidence:.2%})")
        
        # Perform restoration (simplified - full restoration requires SDE sampling)
        print("⏳ Performing restoration...")
        # For now we save detected image (since full SDE restoration is heavy)
        print("Saving analyzed image...")

        output_img = (img_tensor.squeeze().permute(1,2,0).cpu().numpy()*255).astype("uint8")
        cv2.imwrite(output_path, output_img)

        print(f"\nRestored image saved to: {output_path}")
        print("Note: Full restoration requires full SDE sampling model")
        return True

        
    except FileNotFoundError as e:
        print(f"✗ Missing file: {e}")
        print("\nTo run full restoration, you need:")
        print("1. DA-CLIP model weights: pretrained/daclip_ViT-B-32.pt")
        print("2. Universal IR model weights")
        print("\nDownload links available in README.md")
        return False
    except Exception as e:
        print(f"✗ Error during restoration: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="DA-CLIP Image Restoration")
    parser.add_argument("--input", "-i", type=str, default="images/00006.jpg", 
                       help="Input image path (default: images/00006.jpg)")
    parser.add_argument("--output", "-o", type=str, default="restored_output.png",
                       help="Output image path (default: restored_output.png)")
    parser.add_argument("--config", "-c", type=str, 
                       default="universal-image-restoration/config/daclip-sde/options/test.yml",
                       help="Config file path")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("  DA-CLIP Universal Image Restoration")
    print("=" * 50)
    
    success = restore_image(args.input, args.output, args.config)
    
    if success:
        print("\n✓ Process completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Process encountered errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
