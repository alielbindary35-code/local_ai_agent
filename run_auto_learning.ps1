# Auto-Learning Quick Start Script
# This script runs the auto-learner to populate the knowledge base

Write-Host "🎓 Auto-Learning Quick Start" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "src/tools/auto_learner.py")) {
    Write-Host "❌ auto_learner.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Check if essential_tools.json exists
if (-not (Test-Path "data/essential_tools.json")) {
    Write-Host "❌ essential_tools.json not found!" -ForegroundColor Red
    Write-Host "Please ensure data/essential_tools.json exists" -ForegroundColor Yellow
    exit 1
}

# Check dependencies
Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
$requiredPackages = @("rich", "duckduckgo-search", "requests", "beautifulsoup4")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $result = python -c "import $($package.Replace('-', '_')); print('ok')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "⚠️  Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    $install = Read-Host "Install missing packages? (y/n)"
    if ($install -eq "y") {
        Write-Host "Installing packages..." -ForegroundColor Cyan
        pip install $missingPackages
    } else {
        Write-Host "Please install missing packages manually: pip install $($missingPackages -join ' ')" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ All dependencies installed" -ForegroundColor Green
}

# Show what will be learned
Write-Host ""
Write-Host "📚 Tools to learn:" -ForegroundColor Cyan
$toolsJson = Get-Content "data/essential_tools.json" | ConvertFrom-Json
$totalTools = 0
foreach ($category in $toolsJson.PSObject.Properties.Name) {
    $count = ($toolsJson.$category | Measure-Object).Count
    $totalTools += $count
    Write-Host "  $category`: $count tools" -ForegroundColor Yellow
}
Write-Host "  Total: $totalTools tools" -ForegroundColor Green

# Check progress
if (Test-Path "data/learning_progress.json") {
    $progress = Get-Content "data/learning_progress.json" | ConvertFrom-Json
    $learnedCount = ($progress | Measure-Object).Count
    Write-Host ""
    Write-Host "✅ Already learned: $learnedCount tools" -ForegroundColor Green
    Write-Host "🎓 Remaining: $($totalTools - $learnedCount) tools" -ForegroundColor Yellow
}

# Estimate time
$estimatedMinutes = [math]::Ceiling($totalTools * 0.15)  # ~9 seconds per tool average
Write-Host ""
Write-Host "⏱️  Estimated time: ~$estimatedMinutes minutes" -ForegroundColor Cyan
Write-Host ""

# Confirm
$confirm = Read-Host "Start auto-learning? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

# Run the auto-learner
Write-Host ""
Write-Host "🚀 Starting auto-learning..." -ForegroundColor Cyan
Write-Host ""

python src/tools/auto_learner.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✨ Auto-learning complete!" -ForegroundColor Green
    Write-Host "📂 Knowledge base location: data/knowledge_base" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Auto-learning encountered errors" -ForegroundColor Red
    Write-Host "Check the output above for details" -ForegroundColor Yellow
}

