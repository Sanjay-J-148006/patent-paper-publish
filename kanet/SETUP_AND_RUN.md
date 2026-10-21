# KA_Net Dehazing Project - Setup & Run Guide

## Status
✅ Repository cloned: `src\KA_Net_repo`
✅ Environment configuration ready: `src\KA_Net_repo\environment.yml`
⏳ **Waiting for:** Pretrained model download (automatic download failed due to Baidu Pan restrictions)

---

## Step 1: Download the Pretrained Model

The pretrained model **must be downloaded manually** from Baidu Pan.

### How to Download

1. Open this link in your browser:  
   **https://pan.baidu.com/s/1HETnxLCTxjHRsBg2STwsHQ**

2. Enter the extraction code: **n2k4**

3. Download the file (typically named something like `model.pk` or `Dehaze_weights.pk`)

4. Save it to the `src\KA_Net_repo\testcode\` folder:
   ```
   C:\Users\HP\OneDrive\Desktop\kanet\src\KA_Net_repo\testcode\<downloaded_file.pk>
   ```

---

## Step 2: Run the Test

### Option A: Using the Helper Script (Recommended - Automatic)

The easiest way — just run this PowerShell command with the path to your downloaded model:

```powershell
# From the project root directory
.\run_kanet.ps1 -ModelPath "src\KA_Net_repo\testcode\<your_model_filename.pk>"

# Example (if the file is named "model.pk")
.\run_kanet.ps1 -ModelPath "src\KA_Net_repo\testcode\model.pk"

# Run on CPU instead of GPU
.\run_kanet.ps1 -ModelPath "src\KA_Net_repo\testcode\model.pk" -Device cpu
```

The script will:
- ✅ Check for conda
- ✅ Create `ka_net` conda environment from `environment.yml`
- ✅ Run the test on all images in `src\KA_Net_repo\input\`
- ✅ Save results to `src\KA_Net_repo\results\`

---

### Option B: Manual Setup and Run

If you prefer to set up conda yourself:

```powershell
# Create the conda environment
conda env create -f src\KA_Net_repo\environment.yml -n ka_net

# Activate the environment
conda activate ka_net

# Run the test
python src\KA_Net_repo\testcode\KA_net_test.py `
  --model src\KA_Net_repo\testcode\<your_model_filename.pk> `
  --test_dir src\KA_Net_repo\input `
  --out_dir src\KA_Net_repo\results `
  --device cuda
```

**Notes:**
- Change `--device cuda` to `--device cpu` if you don't have a GPU
- Default paths are already set to the cloned repository directories

---

## Input & Output

### Input Images
Location: `src\KA_Net_repo\input\`

Currently contains 10 test images:
- aerial.png
- AM_Google_754.png
- bench.png
- building1.png
- canon.png
- canyon.png
- cliff.png
- cones.png
- oxford.png
- pumpkins.png

### Output Results
Results will be saved to: `src\KA_Net_repo\results\`

Dehazing results (dehazed versions of input images) will appear here after the test completes.

---

## Troubleshooting

### Model not found error
```
ERROR: model file not found: ...
```
Make sure you:
1. Downloaded the file from Baidu Pan
2. Placed it in `src\KA_Net_repo\testcode\`
3. Use the correct filename in the `--model` parameter

### Conda not found error
```
ERROR: Conda not found! Please install Anaconda/Miniconda.
```
Install Anaconda or Miniconda from: https://www.anaconda.com/download

### GPU / CUDA issues
If you get CUDA errors:
- Add `--device cpu` to run on CPU (slower but always works)
- Or ensure CUDA 11.0 is installed (matching environment.yml)

### Out of memory error
Reduce batch size or image resolution, or use CPU mode

---

## Project Structure

```
kanet/
├── src/
│   ├── ka_net/              (original folder with input/results)
│   │   ├── environment.yml
│   │   ├── input/
│   │   ├── results/
│   │   └── testcode/
│   │
│   └── KA_Net_repo/         (cloned from https://github.com/fyxnl/KA_Net)
│       ├── environment.yml  (copied from ka_net)
│       ├── README.md        (official project README)
│       ├── input/           (test images)
│       ├── results/         (output location)
│       └── testcode/
│           ├── KA_net_test.py
│           ├── LD_model1.py
│           ├── base_networks.py
│           ├── deconv.py
│           ├── transweather_model.py
│           ├── Utils.py
│           └── view_testdata1.py
│
├── run_kanet.ps1            (helper script to run the test)
├── baidu_download.py        (attempted automated download)
└── baidu_download_v2.py     (attempted automated download v2)
```

---

## Next Steps

1. ✅ **Clone repo** — Done
2. ✅ **Set up environment** — Done  
3. ⏳ **Download model** — **YOU ARE HERE** (manual Baidu Pan download needed)
4. 🚀 **Run test** — After model is downloaded, use the helper script or manual commands above

---

## References

- **Official KA_Net GitHub**: https://github.com/fyxnl/KA_Net
- **Paper**: https://ieeexplore.ieee.org/document/10564179
- **Pretrained Model**: https://pan.baidu.com/s/1HETnxLCTxjHRsBg2STwsHQ (extraction code: `n2k4`)

---

**Need help?** Check the official README in `src\KA_Net_repo\README.md` or the paper for more details.
