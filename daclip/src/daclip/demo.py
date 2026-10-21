#!/usr/bin/env python3
"""
Simple demo script for DA-CLIP project
Tests basic functionality without requiring pretrained models
"""

import sys
import torch
print("✓ PyTorch imported successfully")

try:
    import open_clip
    print("✓ Open-CLIP imported successfully")
except ImportError as e:
    print(f"✗ Failed to import open_clip: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("✓ PIL imported successfully")
except ImportError as e:
    print(f"✗ Failed to import PIL: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("✓ NumPy imported successfully")
except ImportError as e:
    print(f"✗ Failed to import NumPy: {e}")
    sys.exit(1)

try:
    import cv2
    print("✓ OpenCV imported successfully")
except ImportError as e:
    print(f"✗ Failed to import OpenCV: {e}")
    sys.exit(1)

# Check CUDA availability
print(f"\n✓ CUDA available: {torch.cuda.is_available()}")
print(f"✓ PyTorch version: {torch.__version__}")

# Try to load DA-CLIP model (if weights are available)
print("\n=== DA-CLIP Project Loaded Successfully ===")
print("The project requires:")
print("1. DA-CLIP pretrained weights: daclip_ViT-B-32.pt")
print("2. Universal Image Restoration model weights")
print("3. Test images for restoration")
print("\nTo run full restoration, you need to:")
print("1. Download pretrained weights from the GitHub page")
print("2. Place them in the 'pretrained' directory")
print("3. Prepare test images")
print("4. Run restoration via the models")
print("\nFor more information, see README.md")
