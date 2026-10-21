<#
PowerShell helper to create the conda environment described in environment.yml
Usage (PowerShell):
  ./run_with_conda.ps1
#>
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Error "Conda not found. Install Anaconda/Miniconda and rerun this script."
    exit 1
}

Write-Host "Creating conda environment 'ka_net' from environment.yml..."
conda env create -f environment.yml -p ./ka_net_env
Write-Host "To activate: conda activate ./ka_net_env"
Write-Host "If you prefer a named env: conda env create -f environment.yml -n ka_net"