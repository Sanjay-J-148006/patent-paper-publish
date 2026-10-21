#!/usr/bin/env powershell
<#
.SYNOPSIS
Find deeply nested directories and run commands from the correct location
.PARAMETER Model
Model to run: kanet, nighttime, orama, daclip
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('kanet', 'nighttime', 'orama', 'daclip')]
    [string]$Model,
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AdditionalArgs
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommandPath
Write-Host "🔍 Searching for $Model source code..." -ForegroundColor Cyan

# Find the src directory
$srcDir = $null
foreach ($item in @(Get-ChildItem -Path $scriptDir -Recurse -Directory -Filter 'src' -ErrorAction SilentlyContinue)) {
    if ((Test-Path (Join-Path $item.FullName 'ka_net')) -or 
        (Test-Path (Join-Path $item.FullName 'nighttime')) -or
        (Test-Path (Join-Path $item.FullName 'orama')) -or
        (Test-Path (Join-Path $item.FullName 'daclip'))) {
        $srcDir = $item.FullName
        break
    }
}

if (-not $srcDir) {
    Write-Host "❌ src directory not found!" -ForegroundColor Red
    Exit 1
}

Write-Host "✅ Found src at: $srcDir" -ForegroundColor Green

$modelPath = $null
$runScript = $null
$workDir = $null

switch ($Model) {
    'kanet' {
        $modelPath = Join-Path $srcDir 'ka_net' 'testcode'
        $runScript = 'KA_net_test.py'
        Write-Host "⚡ Running KA-Net..." -ForegroundColor Yellow
    }
    'nighttime' {
        $modelPath = Join-Path $srcDir 'nighttime'
        $runScript = 'main_test.py'
        Write-Host "🌙 Running Nighttime Dehaze..." -ForegroundColor Yellow
    }
    'orama' {
        $modelPath = Join-Path $srcDir 'orama'
        $runScript = 'inference.py'
        Write-Host "🔥 Running ORAMA..." -ForegroundColor Yellow
    }
    'daclip' {
        $modelPath = Join-Path $srcDir 'daclip'
        $runScript = 'predict.py'
        Write-Host "🧠 Running DACLiP..." -ForegroundColor Yellow
    }
}

if (-not (Test-Path $modelPath)) {
    Write-Host "❌ Model directory not found: $modelPath" -ForegroundColor Red
    Exit 1
}

Write-Host "📁 Changing to: $modelPath" -ForegroundColor Cyan
Push-Location $modelPath

Write-Host "▶️  Running: python $runScript $AdditionalArgs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

# Activate venv if it exists
$venvPath = Join-Path $scriptDir '.venv' 'Scripts' 'Activate.ps1'
if (Test-Path $venvPath) {
    & $venvPath
}

# Run the model
$cmd = "python $runScript $AdditionalArgs"
Invoke-Expression $cmd
$exitCode = $LASTEXITCODE

Pop-Location

if ($exitCode -eq 0) {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "✅ $Model completed successfully!" -ForegroundColor Green
} else {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "❌ $Model failed with exit code: $exitCode" -ForegroundColor Red
}

Exit $exitCode
