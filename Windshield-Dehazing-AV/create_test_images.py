#!/usr/bin/env python3
"""
Create dummy test images for the dehazing models
"""

import os
import numpy as np
from PIL import Image

def create_test_images():
    """Create simple test images for model testing"""
    
    # Create a simple hazy image (grayscale with some noise)
    hazy_img = np.ones((512, 512, 3), dtype=np.uint8) * 150
    # Add some variation
    for i in range(512):
        for j in range(512):
            hazy_img[i, j] = np.clip(150 + np.sin(i/50) * 30 + np.sin(j/50) * 30, 0, 255)
    
    # Create corresponding clear image
    clear_img = np.ones((512, 512, 3), dtype=np.uint8) * 100
    for i in range(512):
        for j in range(512):
            clear_img[i, j] = np.clip(100 + np.sin(i/50) * 50 + np.sin(j/50) * 50, 0, 255)
    
    # Save test images
    pairs_dir = "paired_data/glow"
    os.makedirs(pairs_dir, exist_ok=True)
    
    Image.fromarray(hazy_img).save(os.path.join(pairs_dir, "input.jpg"))
    Image.fromarray(clear_img).save(os.path.join(pairs_dir, "target.jpg"))
    
    print(f"✅ Created test images in {pairs_dir}")
    print(f"   - input.jpg (hazy image)")
    print(f"   - target.jpg (clear image)")

if __name__ == "__main__":
    create_test_images()
