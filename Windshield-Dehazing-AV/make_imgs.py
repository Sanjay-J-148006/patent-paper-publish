#!/usr/bin/env python3
import os, sys
import numpy as np
from PIL import Image

# Create images with simple gradients
hazy = np.ones((256, 256, 3), dtype=np.uint8) * 180
clear = np.ones((256, 256, 3), dtype=np.uint8) * 80

os.makedirs("paired_data/glow", exist_ok=True)
Image.fromarray(hazy).save("paired_data/glow/input.jpg")
Image.fromarray(clear).save("paired_data/glow/target.jpg")
print("OK:Images created in paired_data/glow")
