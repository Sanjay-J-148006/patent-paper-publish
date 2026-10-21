#!/usr/bin/env python3
"""
Windshield Dehazing - Complete Setup and Test Runner
Fixes paths, creates necessary files, and validates setup
"""

import os
import sys
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

def setup_directories():
    """Create all required directories"""
    dirs = [
        "results/dehaze/model",
        "results/ka_net/model",
        "results/ka_net/output",
        "paired_data/glow"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("✅ Directory structure created")

def create_test_images():
    """Create minimal test images"""
    try:
        # Create hazy image (lighter/washed out)
        hazy = np.ones((256, 256, 3), dtype=np.uint8) * 200
        hazy[50:200, 50:200] = 150  # Add some pattern
        
        # Create clear image (darker/more contrast)
        clear = np.ones((256, 256, 3), dtype=np.uint8) * 100
        clear[50:200, 50:200] = 50
        
        os.makedirs("paired_data/glow", exist_ok=True)
        Image.fromarray(hazy).save("paired_data/glow/input.jpg")
        Image.fromarray(clear).save("paired_data/glow/target.jpg")
        print("✅ Test images created: paired_data/glow/{input,target}.jpg")
    except Exception as e:
        print(f"⚠️  Could not create test images: {e}")

def create_dummy_models():
    """Create minimal PyTorch models for testing"""
    try:
        import torch
        import torch.nn as nn
        
        # Create minimal dehaze models as dummies
        models_info = [
            ("results/dehaze/model/best.pt", "Nighttime Dehaze"),
            ("results/ka_net/model/best.pt", "KA-Net"),
        ]
        
        for model_path, name in models_info:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Create minimal model state dict
            state = {
                'model': {
                    'features.0.weight': torch.randn(64, 3, 3, 3),
                    'features.0.bias': torch.randn(64),
                }
            }
            
            try:
                torch.save(state, model_path)
                print(f"✅ Created dummy model: {model_path}")
            except Exception as e:
                print(f"⚠️  Could not create {name} model: {e}")
                
    except ImportError:
        print("⚠️  PyTorch not available, skipping model creation")

def verify_paths():
    """Verify critical paths exist"""
    script_dir = Path(__file__).parent
    checks = {
        "Windshield-Dehazing-AV root": script_dir,
        "paired_data/glow": script_dir / "paired_data" / "glow",
        "results/dehaze/model": script_dir / "results" / "dehaze" / "model",
        "results/ka_net/model": script_dir / "results" / "ka_net" / "model",
    }
    
    print("\n📁 Path Verification:")
    for name, path in checks.items():
        exists = "✅" if path.exists() else "❌"
        print(f"  {exists} {name}: {path}")
    
    # Find src directory
    for src_candidate in script_dir.rglob('src'):
        if (src_candidate / 'ka_net').exists():
            print(f"  ✅ Found source code: {src_candidate}")
            return True
    
    print(f"  ❌ Source code not found")
    return False

def main():
    print("\n" + "="*60)
    print("  WINDSHIELD DEHAZING - Setup & Verification")
    print("="*60 + "\n")
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    print("1️⃣  Creating directory structure...")
    setup_directories()
    
    print("\n2️⃣  Creating test images...")
    create_test_images()
    
    print("\n3️⃣  Creating dummy models for testing...")
    create_dummy_models()
    
    print("\n4️⃣  Verifying paths...")
    verify_paths()
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("  python run_model.py kanet      # Test KA-Net")
    print("  python run_model.py nighttime  # Test Nighttime Dehaze")
    print("  python run_model.py orama      # Test ORAMA")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
