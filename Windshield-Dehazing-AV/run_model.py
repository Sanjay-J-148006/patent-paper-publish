#!/usr/bin/env python3
"""
Windshield Dehazing Model Launcher
Quick access to run any of the 4 dehazing models
"""

import os
import sys
import subprocess
from pathlib import Path

def get_src_dir():
    """Find the src directory by searching for it"""
    script_dir = Path(__file__).parent
    
    # Search for 'src' directory that contains our known subdirectories
    for potential_src in script_dir.rglob('src'):
        if (potential_src / 'ka_net').exists() or (potential_src / 'nighttime').exists():
            return potential_src
    
    # Fallback: use the known nested path
    src_dir = script_dir / "Windshield-Dehazing-AV" / "Windshield-Dehazing-AV" / "Windshield-Dehazing-AV" / "Windshield-Dehazing-AV" / "Windshield-Dehazing-AV" / "src"
    return src_dir

def show_help():
    """Display usage information"""
    print("\n" + "="*60)
    print("  WINDSHIELD DEHAZING - Model Launcher")
    print("="*60)
    print("\nUsage: python run_model.py [model_name] [args...]")
    print("\nAvailable models:")
    print("  python run_model.py orama        - ORAMA (Night Fog King)")
    print("  python run_model.py kanet        - KA-Net (42 FPS Beast)")
    print("  python run_model.py nighttime    - Nighttime Dehaze (Glare Master)")
    print("  python run_model.py daclip       - DACLiP (Universal)")
    print("\nExamples:")
    print("  python run_model.py orama")
    print("  python run_model.py nighttime")
    print("  python run_model.py kanet")
    print("="*60 + "\n")

def run_orama(src_dir, args):
    """Run ORAMA inference"""
    model_path = src_dir / "orama"
    os.chdir(model_path)
    print(f"\n🔥 Running ORAMA from: {model_path}")
    cmd = ["python", "inference.py"] + args
    return subprocess.run(cmd).returncode

def run_kanet(src_dir, args):
    """Run KA-Net test"""
    model_path = src_dir / "ka_net" / "testcode"
    os.chdir(model_path)
    print(f"\n⚡ Running KA-Net from: {model_path}")
    cmd = ["python", "KA_net_test.py"] + args
    return subprocess.run(cmd).returncode

def run_nighttime(src_dir, args):
    """Run Nighttime Dehaze"""
    model_path = src_dir / "nighttime"
    os.chdir(model_path)
    print(f"\n🌙 Running Nighttime Dehaze from: {model_path}")
    cmd = ["python", "main_test.py"] + args
    return subprocess.run(cmd).returncode

def run_daclip(src_dir, args):
    """Run DACLiP"""
    model_path = src_dir / "daclip"
    os.chdir(model_path)
    print(f"\n🧠 Running DACLiP from: {model_path}")
    cmd = ["python", "predict.py"] + args
    return subprocess.run(cmd).returncode

def main():
    # Check if src directory exists
    src_dir = get_src_dir()
    if not src_dir.exists():
        print(f"❌ Error: src directory not found at {src_dir}")
        sys.exit(1)
    
    # Show help if no arguments
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    models = [m.lower() for m in sys.argv[1:]]
    extra_args = []
    overall_exit = 0
    for m in models:
        try:
            if m == "orama":
                rc = run_orama(src_dir, extra_args)
            elif m == "kanet":
                rc = run_kanet(src_dir, extra_args)
            elif m == "nighttime":
                rc = run_nighttime(src_dir, extra_args)
            elif m == "daclip":
                rc = run_daclip(src_dir, extra_args)
            else:
                print(f"❌ Error: Unknown model '{m}'")
                show_help()
                rc = 1
        except Exception as e:
            print(f"❌ Error running model '{m}': {e}")
            rc = 1
        if rc != 0:
            overall_exit = rc
    sys.exit(overall_exit)

if __name__ == "__main__":
    main()
