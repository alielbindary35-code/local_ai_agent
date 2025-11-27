# Simple Auto-Learning Script (Fixed)
# This script runs the auto-learner with proper path setup

# Get project root
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir = Split-Path -Parent $ScriptPath

if (Test-Path (Join-Path $ScriptDir "src\tools\auto_learner.py")) {
    $ProjectRoot = $ScriptDir
} else {
    $ProjectRoot = Split-Path -Parent $ScriptDir
}

# Change to project root
Set-Location $ProjectRoot

Write-Host "Auto-Learning Script" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Set PYTHONPATH
$env:PYTHONPATH = $ProjectRoot

# Run using Python module syntax
python -m src.tools.auto_learner

