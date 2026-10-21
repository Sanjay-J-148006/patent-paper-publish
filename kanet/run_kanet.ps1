#!/usr/bin/env powershell
<#
.SYNOPSIS
Setup and run KA_Net dehazing test with automatic environment creation.

.DESCRIPTION
This script will:
1. Check for conda
2. Create/activate ka_net conda environment
3. Run the KA_Net test on input images

.PARAMETER ModelPath
Path to the pretrained model (.pk file). Required.

.PARAMETER TestDir
Path to test images directory. Default: src/KA_Net_repo/input

.PARAMETER OutputDir  
Path to output results directory. Default: src/KA_Net_repo/results

.PARAMETER Device
Device to run on: 'cpu' or 'cuda'. Default: 'cuda'

.EXAMPLE
.\run_kanet.ps1 -ModelPath src\KA_Net_repo\testcode\model.pk
.\run_kanet.ps1 -ModelPath model.pk -Device cpu
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ModelPath,
    
    [Parameter(Mandatory=$false)]
    [string]$TestDir = "src\KA_Net_repo\input",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "src\KA_Net_repo\results",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('cpu', 'cuda')]
    [string]$Device = 'cuda'
)

# Check if model path provided
if (-not $ModelPath) {
    Write-Host "ERROR: Model path required!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\run_kanet.ps1 -ModelPath <path_to_model.pk>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\run_kanet.ps1 -ModelPath src\KA_Net_repo\testcode\model.pk" -ForegroundColor Yellow
    Write-Host "  .\run_kanet.ps1 -ModelPath model.pk -Device cpu" -ForegroundColor Yellow
    exit 1
}

# Check if model file exists
if (-not (Test-Path $ModelPath)) {
    Write-Host "ERROR: Model file not found: $ModelPath" -ForegroundColor Red
    exit 1
}

$ModelPath = (Resolve-Path $ModelPath).Path
Write-Host "[*] Using model: $ModelPath" -ForegroundColor Cyan

# Check for conda
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Conda not found! Please install Anaconda/Miniconda." -ForegroundColor Red
    exit 1
}

# Create conda environment from environment.yml
$CondaEnvName = "ka_net"
$EnvironmentFile = "src\KA_Net_repo\environment.yml"

if (-not (Test-Path $EnvironmentFile)) {
    Write-Host "ERROR: environment.yml not found at: $EnvironmentFile" -ForegroundColor Red
    exit 1
}

Write-Host "[*] Checking conda environment..." -ForegroundColor Cyan
$EnvExists = (conda env list | Select-String $CondaEnvName) -ne $null

if (-not $EnvExists) {
    Write-Host "[*] Creating conda environment from $EnvironmentFile" -ForegroundColor Cyan
    conda env create -f $EnvironmentFile -n $CondaEnvName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create conda environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[+] Conda environment '$CondaEnvName' already exists" -ForegroundColor Green
}

# Activate conda environment and run test
Write-Host "[*] Activating conda environment: $CondaEnvName" -ForegroundColor Cyan
$ActivateScript = "$((conda info --base).Trim())\Scripts\activate.bat"

# Run test in conda environment
Write-Host "[*] Running KA_Net test..." -ForegroundColor Cyan
Write-Host "    Model:      $ModelPath" -ForegroundColor Gray
Write-Host "    Test dir:   $TestDir" -ForegroundColor Gray
Write-Host "    Output dir: $OutputDir" -ForegroundColor Gray
Write-Host "    Device:     $Device" -ForegroundColor Gray
Write-Host ""

$TestScript = "src\KA_Net_repo\testcode\KA_net_test.py"
$cmd = "& cmd /c `"$ActivateScript $CondaEnvName && python $TestScript --model $ModelPath --test_dir $TestDir --out_dir $OutputDir --device $Device`""

Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[+] Test completed successfully!" -ForegroundColor Green
    Write-Host "[+] Results saved to: $OutputDir" -ForegroundColor Green
    if ((Get-ChildItem $OutputDir -Filter *.png 2>/dev/null | Measure-Object).Count -gt 0) {
        Write-Host "[+] Output images found in: $OutputDir" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "[-] Test failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
