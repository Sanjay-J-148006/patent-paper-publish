#!/usr/bin/env python3
"""Debug script - show where all the model directories are located"""

from pathlib import Path

root = Path("C:\\Users\\HP\\OneDrive\\Desktop\\Windshield-Dehazing-AV")

print("🔍 Searching for model directories...\n")

# Find src directory
for src in root.rglob('src'):
    if (src / 'nighttime').exists():
        print(f"✅ Found src directory at:")
        print(f"   {src}\n")
        
        print("📁 Model directories found:")
        print(f"   KA-Net:         {src / 'ka_net' / 'testcode'}")
        print(f"   Nighttime:      {src / 'nighttime'}")
        print(f"   ORAMA:          {src / 'orama'}")
        print(f"   DACLiP:         {src / 'daclip'}\n")
        
        # Show the relative path from root
        rel_path = src.relative_to(root)
        print(f"📍 Relative path from project root:")
        print(f"   {rel_path}\n")
        
        print("🎯 To navigate to Nighttime Dehaze:")
        print(f"   cd \"{src / 'nighttime'}\"\n")
        
        print("🎯 Recommended: Use the smart launcher instead:")
        print(f"   python run_any_model.py nighttime\n")
        break
else:
    print("❌ Could not find src directory")
    print(f"\n📂 Searching in: {root}")
    print("\n🔎 All 'src' directories found:")
    for src in root.rglob('src'):
        print(f"   {src}")
