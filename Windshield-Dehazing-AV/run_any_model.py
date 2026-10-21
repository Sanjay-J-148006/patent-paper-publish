#!/usr/bin/env python3
"""
Find and run Windshield Dehazing models from any location
This handles the deeply nested directory structure automatically
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

def find_src_dir(start_path: Path) -> Optional[Path]:
    """Find the src directory containing model subdirectories"""
    for item in start_path.rglob('src'):
        # Check if this is the right src directory
        has_models = any([
            (item / 'ka_net').exists(),
            (item / 'nighttime').exists(),
            (item / 'orama').exists(),
            (item / 'daclip').exists(),
        ])
        if has_models:
            return item
    return None

def find_project_root() -> Path:
    """Find the project root (where run_model.py is)"""
    current = Path(__file__).parent.resolve()
    while current != current.parent:
        if (current / 'run_model.py').exists():
            return current
        current = current.parent
    return Path.cwd()

def run_kanet(src_dir: Path, argv: list) -> int:
    """Run KA-Net"""
    model_path = src_dir / 'ka_net' / 'testcode'
    script = 'KA_net_test.py'
    print(f"⚡ Running KA-Net from: {model_path}")
    return run_script(model_path, script, argv)

def run_nighttime(src_dir: Path, argv: list) -> int:
    """Run Nighttime Dehaze"""
    model_path = src_dir / 'nighttime'
    script = 'main_test.py'
    print(f"🌙 Running Nighttime Dehaze from: {model_path}")
    return run_script(model_path, script, argv)

def run_orama(src_dir: Path, argv: list) -> int:
    """Run ORAMA"""
    model_path = src_dir / 'orama'
    script = 'inference.py'
    print(f"🔥 Running ORAMA from: {model_path}")
    return run_script(model_path, script, argv)

def run_daclip(src_dir: Path, argv: list) -> int:
    """Run DACLiP"""
    model_path = src_dir / 'daclip'
    script = 'predict.py'
    print(f"🧠 Running DACLiP from: {model_path}")
    return run_script(model_path, script, argv)

def run_script(model_path: Path, script: str, argv: list) -> int:
    """Run a Python script in a specific directory"""
    if not model_path.exists():
        print(f"❌ Model directory not found: {model_path}")
        return 1
    
    script_file = model_path / script
    if not script_file.exists():
        print(f"❌ Script not found: {script_file}")
        return 1
    
    # Change to model directory
    original_cwd = os.getcwd()
    os.chdir(model_path)
    
    try:
        cmd = [sys.executable, script] + argv
        print(f"▶️  {'=' * 50}")
        result = subprocess.run(cmd)
        print(f"{'=' * 50}")
        return result.returncode
    finally:
        os.chdir(original_cwd)

def main():
    project_root = find_project_root()
    print(f"📁 Project root: {project_root}")
    
    src_dir = find_src_dir(project_root)
    if not src_dir:
        print("❌ Could not find src directory!")
        return 1
    
    print(f"✅ Found src at: {src_dir}")
    
    if len(sys.argv) < 2:
        print("\nUsage: python run_any_model.py [model] [args...]")
        print("\nAvailable models:")
        print("  kanet      - KA-Net (42 FPS Beast)")
        print("  nighttime  - Nighttime Dehaze (Glare Master)")
        print("  orama      - ORAMA (Night Fog King)")
        print("  daclip     - DACLiP (Universal)")
        print("\nExamples:")
        print("  python run_any_model.py kanet")
        print("  python run_any_model.py nighttime")
        print("  python run_any_model.py orama")
        return 0
    
    model = sys.argv[1].lower()
    extra_args = sys.argv[2:]
    
    handlers = {
        'kanet': run_kanet,
        'nighttime': run_nighttime,
        'orama': run_orama,
        'daclip': run_daclip,
    }
    
    if model not in handlers:
        print(f"❌ Unknown model: {model}")
        return 1
    
    print(f"\n{'=' * 50}")
    exit_code = handlers[model](src_dir, extra_args)
    print(f"\n{'✅' if exit_code == 0 else '❌'} Exit code: {exit_code}")
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
