# 🚗 Windshield Dehazing AV - Quick Start Guide

## 🎯 Overview
This project contains **4 AI-powered dehazing models** for windshield visibility enhancement:

| Model | Speed | Best For | Command |
|-------|-------|----------|---------|
| **ORAMA** | 29 FPS | Night fog & rain | `./run.ps1 orama` |
| **KA-Net** | 42 FPS | Road fog | `./run.ps1 kanet` |
| **Nighttime** | Real-time | High beam glare | `./run.ps1 nighttime` |
| **DACLiP** | Variable | Universal scenarios | `./run.ps1 daclip` |

---

## 🚀 Quick Start (Recommended: PowerShell Script)

The easiest way to run models—automatically activates the virtual environment:

```powershell
cd C:\Users\HP\OneDrive\Desktop\Windshield-Dehazing-AV
.\run.ps1 orama           # Single model
.\run.ps1 orama kanet     # Multiple models sequentially
```

No need to manually activate the venv—the script handles it!

---

## 🔄 Alternative Methods

### Python Launcher (with venv activation)
```powershell
python run_model.py orama
python run_model.py orama kanet nighttime
```

### Batch File Launcher (Windows CMD)
```cmd
activate_and_run.bat orama
activate_and_run.bat orama kanet
```

### Direct Terminal Activation
If you prefer manual control, activate the venv first:

```powershell
.\.venv\Scripts\Activate.ps1
python run_model.py orama kanet
```

---

## 📊 Model Details

### 🔥 ORAMA (Night Fog King)
- **Input:** Video files from `input/` (e.g., `video1.mp4`, `video2.mp4`)
- **Output:** `output/output_inference_<timestamp>.mp4`
- **Detects:** Cars, trucks, motorcycles, pedestrians with collision risk assessment
- **Run:** `./run.ps1 orama`

### ⚡ KA-Net (42 FPS Beast)
- **Input:** Images from `input/`
- **Output:** Deblurred images in `input/`
- **Speed:** ~42 FPS for road fog removal
- **Run:** `./run.ps1 kanet`

### 🌙 Nighttime Dehaze (Glare Master)
- **Input:** Images from `paired_data/glow/`
- **Output:** Enhanced images in `results/`
- **Specialization:** Nighttime high-beam glare reduction
- **Run:** `./run.ps1 nighttime`

### 🧠 DACLiP (Universal)
- **Input:** Images with text prompts
- **Output:** Restored images in `output/`
- **Capability:** Works on any visibility degradation scenario
- **Run:** `./run.ps1 daclip`

---

## ⚙️ System Requirements
- **Python 3.8+** (3.14 recommended)
- **GPU optional** (CPU will work, slower)
- **Windows 10/11**
- **Disk space:** 5-10GB for all model weights

---

## 🏗️ Project Structure
```
Windshield-Dehazing-AV/
├── main.py                # Show all models
├── run.ps1               # PowerShell launcher (RECOMMENDED)
├── activate_and_run.bat  # Batch launcher
├── run_model.py          # Python launcher
├── run_model.bat         # Batch launcher (legacy)
├── .venv/                # Virtual environment (auto-created)
└── Windshield-Dehazing-AV/
    └── (nested folders...)
        └── src/
            ├── orama/          # ORAMA model dir
            ├── ka_net/         # KA-Net model dir
            ├── nighttime/      # Nighttime model dir
            └── daclip/         # DACLiP model dir
```

---

## 🔧 Setup (First Run Only)

If the virtual environment doesn't exist, create it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Or let the `run.ps1` script handle it—it will warn if the venv is missing.

---

## 📝 Example Workflows

### Process All Models Sequentially
```powershell
.\run.ps1 orama kanet nighttime daclip
```

### Process Single Model and Check Output
```powershell
.\run.ps1 orama
# Output video saved to:
# src/orama/output/output_inference_<timestamp>.mp4
```

### Run with Python (if PowerShell unavailable)
```powershell
python run_model.py orama
```

---

## 🐛 Troubleshooting

### "Module not found" errors
- The `run.ps1` script should activate the venv automatically
- If not working, manually activate: `.\.venv\Scripts\Activate.ps1`

### Models not found
```powershell
python main.py  # Verify all 4 models are accessible
```

### GPU not detected
- Models will fall back to CPU (slower but functional)
- CUDA is optional; all models run on CPU

### Long paths error
- Use `run.ps1` or `activate_and_run.bat`—they handle deep nesting automatically

---

## 📞 Support

For model-specific issues, check individual READMEs:
- `src/orama/README.md` – ORAMA docs
- `src/ka_net/README.md` – KA-Net docs
- `src/nighttime/README.md` – Nighttime dehaze docs
- `src/daclip/README.md` – DACLiP docs

---

## 🎉 Ready to Go!

You're all set! Pick a model and start dehazing:

```powershell
.\run.ps1 orama
```

Enjoy clear windshield visibility! 🚗💨
