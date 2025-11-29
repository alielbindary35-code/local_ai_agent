# Auto-Learning Quick Start Script
# This script runs the auto-learner to populate the knowledge base

# Get script directory and project root
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir = Split-Path -Parent $ScriptPath

# If script is in root, use script dir as project root
# Otherwise, go up one level
if (Test-Path (Join-Path $ScriptDir "src\tools\auto_learner.py")) {
    $ProjectRoot = $ScriptDir
} else {
    $ProjectRoot = Split-Path -Parent $ScriptDir
}

# Verify we found the project root
if (-not (Test-Path (Join-Path $ProjectRoot "src\tools\auto_learner.py"))) {
    Write-Host "ERROR: Could not find project root!" -ForegroundColor Red
    Write-Host "Script location: $ScriptDir" -ForegroundColor Yellow
    Write-Host "Trying to find project root..." -ForegroundColor Yellow
    exit 1
}

Write-Host "Auto-Learning Quick Start" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "OK: Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
$autoLearnerPath = Join-Path $ProjectRoot "src\tools\auto_learner.py"
if (-not (Test-Path $autoLearnerPath)) {
    Write-Host "ERROR: auto_learner.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Check if essential_tools.json exists
$toolsFile = Join-Path $ProjectRoot "data\essential_tools.json"
if (-not (Test-Path $toolsFile)) {
    Write-Host "ERROR: essential_tools.json not found!" -ForegroundColor Red
    Write-Host "Please ensure data/essential_tools.json exists" -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$requiredPackages = @("rich", "duckduckgo_search", "requests", "beautifulsoup4")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $packageName = $package.Replace('-', '_')
    $result = python -c "import $packageName; print('ok')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "WARNING: Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    $install = Read-Host "Install missing packages? (y/n)"
    if ($install -eq "y") {
        Write-Host "Installing packages..." -ForegroundColor Cyan
        pip install $missingPackages
    } else {
        Write-Host "Please install missing packages manually: pip install $($missingPackages -join ' ')" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "OK: All dependencies installed" -ForegroundColor Green
}

# Show what will be learned
Write-Host ""
Write-Host "Tools to learn:" -ForegroundColor Cyan
$toolsJson = Get-Content $toolsFile | ConvertFrom-Json
$totalTools = 0
foreach ($category in $toolsJson.PSObject.Properties.Name) {
    $count = ($toolsJson.$category | Measure-Object).Count
    $totalTools += $count
    Write-Host "  $category`: $count tools" -ForegroundColor Yellow
}
Write-Host "  Total: $totalTools tools" -ForegroundColor Green

# Check progress
$progressFile = Join-Path $ProjectRoot "data\learning_progress.json"
if (Test-Path $progressFile) {
    $progress = Get-Content $progressFile | ConvertFrom-Json
    $learnedCount = ($progress | Measure-Object).Count
    Write-Host ""
    Write-Host "OK: Already learned: $learnedCount tools" -ForegroundColor Green
    Write-Host "Remaining: $($totalTools - $learnedCount) tools" -ForegroundColor Yellow
}

# Estimate time
$estimatedMinutes = [math]::Ceiling($totalTools * 0.15)  # ~9 seconds per tool average
Write-Host ""
Write-Host "Estimated time: ~$estimatedMinutes minutes" -ForegroundColor Cyan
Write-Host ""

# Confirm
$confirm = Read-Host "Start auto-learning? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

# Change to project root
Set-Location $ProjectRoot

# Set UTF-8 encoding for Python output
$env:PYTHONIOENCODING = 'utf-8'

Write-Host ""
Write-Host "Starting auto-learning..." -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Run using Python module syntax (handles paths automatically)
python -m src.tools.auto_learner 

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Auto-learning complete!" -ForegroundColor Green
    $kbPath = Join-Path $ProjectRoot "data\knowledge_base"
    Write-Host "Knowledge base location: $kbPath" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "ERROR: Auto-learning encountered errors" -ForegroundColor Red
    Write-Host "Check the output above for details" -ForegroundColor Yellow
}
