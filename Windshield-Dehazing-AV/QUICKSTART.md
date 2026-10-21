# 🚗 Windshield Dehazing AV - Quick Start Guide

## 🎯 Overview
This project contains **4 AI-powered dehazing models** for windshield visibility enhancement:

| Model | Speed | Best For | Command |
|-------|-------|----------|---------|
| **ORAMA** | 29 FPS | Night fog & rain | `python run_model.py orama` |
| **KA-Net** | 42 FPS | Road fog | `python run_model.py kanet` |
| **Nighttime** | Real-time | High beam glare | `python run_model.py nighttime` |
| **DACLiP** | Variable | Universal scenarios | `python run_model.py daclip` |

---

## 🚀 Quick Start

### Option 1: Python Launcher (Recommended)
```powershell
cd C:\Users\HP\OneDrive\Desktop\Windshield-Dehazing-AV
python run_model.py orama
```

Available commands:
```powershell
python run_model.py orama      # ORAMA - Night Fog King
python run_model.py kanet      # KA-Net - 42 FPS Beast
python run_model.py nighttime  # Nighttime Dehaze - Glare Master
python run_model.py daclip     # DACLiP - Universal Handler
```

### Option 2: Batch File Launcher
```powershell
cd C:\Users\HP\OneDrive\Desktop\Windshield-Dehazing-AV
.\run_model.bat orama
```

### Option 3: Display All Models
```powershell
python main.py
```
Shows all 4 models and their status.

---

## 📊 Model Details

### 🔥 ORAMA (Night Fog King)
**Path:** `src/orama/`
**Input:** Video files
**Output:** Video with detected objects and collision risk
**Usage:**
```powershell
python run_model.py orama
```

### ⚡ KA-Net (42 FPS Beast)
**Path:** `src/ka_net/testcode/`
**Input:** Images
**Output:** Deblurred images
**Usage:**
```powershell
python run_model.py kanet
```

### 🌙 Nighttime Dehaze (Glare Master)
**Path:** `src/nighttime/`
**Input:** Images
**Output:** Enhanced nighttime images
**Usage:**
```powershell
python run_model.py nighttime
```

### 🧠 DACLiP (Universal)
**Path:** `src/daclip/`
**Input:** Images/videos with text prompts
**Output:** Restored images
**Usage:**
```powershell
python run_model.py daclip
```

---

## 📁 Directory Structure
```
Windshield-Dehazing-AV/
├── main.py                 # Show all models
├── run_model.py           # Python launcher (Recommended)
├── run_model.bat          # Batch launcher (Windows CMD)
└── Windshield-Dehazing-AV/
    └── (nested folders...)
        └── src/
            ├── orama/
            ├── ka_net/
            ├── nighttime/
            └── daclip/
```

---

## ⚙️ System Requirements
- **Python 3.8+**
- **GPU recommended** (NVIDIA with CUDA)
- **Windows 10/11** (tested)
- **Disk space:** 5-10GB for models

---

## 📝 Example Workflows

### Process a foggy video with ORAMA:
```powershell
cd C:\Users\HP\OneDrive\Desktop\Windshield-Dehazing-AV
python run_model.py orama
# Check output in: src/orama/output/
```

### Enhance a nighttime image:
```powershell
python run_model.py nighttime
# Check output in: src/nighttime/results/
```

### Run multiple models:
```powershell
python run_model.py orama
# Then...
python run_model.py nighttime
# Then...
python run_model.py kanet
```

---

## 🐛 Troubleshooting

### Model not found error
```powershell
python main.py  # Verify all models are accessible
```

### Path too long error (Windows)
Use the `run_model.py` launcher which handles paths automatically.

### GPU not detected
Models will fall back to CPU (slower but works).

---

## 📞 Support
For issues with specific models, check their README files:
- `src/orama/README.md`
- `src/ka_net/README.md`
- `src/nighttime/README.md`
- `src/daclip/README.md`

---

## 🎉 You're ready!
Pick a model and start dehazing your windshield footage!
