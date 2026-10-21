#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Windshield Dehazing Model Launcher - PowerShell wrapper
  Activates venv and runs models with proper environment.

.EXAMPLE
  .\run.ps1 orama
  .\run.ps1 orama kanet nighttime
#>

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$models
)

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Activate venv
$venvPath = Join-Path $scriptDir ".venv"
$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "[*] Activating virtual environment..." -ForegroundColor Green
    & $activateScript
} else {
    Write-Host "[!] Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "[!] Please create it with: python -m venv .venv" -ForegroundColor Red
    exit 1
}

# Run models
if ($models.Count -eq 0) {
    Write-Host "[*] No models specified. Running: python run_model.py" -ForegroundColor Yellow
    python run_model.py
} else {
    Write-Host "[*] Running models: $($models -join ', ')" -ForegroundColor Green
    & python run_model.py @models
}

exit $LASTEXITCODE
