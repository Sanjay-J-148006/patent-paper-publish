# Running KA_Net (local setup)

Recommended: create a conda env using the provided `environment.yml` (ensures Python 3.7 + matching PyTorch).

Commands (PowerShell):

```powershell
# from src/ka_net
conda env create -f environment.yml -n ka_net
conda activate ka_net

# run test (example)
python testcode/KA_net_test.py --model path\to\trained_model.pk --test_dir path\to\test_images --out_dir results
```

If you don't have conda, create a virtualenv with Python 3.7 and install `requirements.txt` (CPU-only PyTorch installation may need a wheel):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
# For GPUs or specific CUDA you may need to install torch from the official instructions: https://pytorch.org/get-started/previous-versions/
```

Notes:
- The repo expects a pretrained model checkpoint (provide via `--model`).
- Default input/output paths are `../input` and `../results` relative to `testcode` when not provided.
- If you don't have a GPU, pass `--device cpu`.