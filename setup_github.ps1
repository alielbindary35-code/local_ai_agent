# GitHub Setup Helper Script
# This script helps you push your local repo to GitHub

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

# Change to project root
Set-Location $ProjectRoot

Write-Host "GitHub Setup Helper" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "OK: Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check current branch
$currentBranch = git branch --show-current
Write-Host "Current branch: $currentBranch" -ForegroundColor Yellow
Write-Host ""

# Check if remote exists
$remoteExists = git remote -v
if ($remoteExists) {
    Write-Host "WARNING: Remote already configured:" -ForegroundColor Yellow
    Write-Host $remoteExists
    Write-Host ""
    $remove = Read-Host "Do you want to remove and reconfigure? (y/n)"
    if ($remove -eq "y") {
        git remote remove origin
        Write-Host "OK: Removed existing remote" -ForegroundColor Green
    } else {
        Write-Host "Skipping remote setup. Use 'git push -u origin $currentBranch' to push." -ForegroundColor Yellow
        exit 0
    }
}

# Get GitHub username
Write-Host ""
Write-Host "Enter your GitHub details:" -ForegroundColor Cyan
$username = Read-Host "GitHub Username"
$repoName = Read-Host "Repository Name (default: local_ai_agent)"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "local_ai_agent"
}

# Ask for protocol preference
Write-Host ""
Write-Host "Choose connection method:" -ForegroundColor Cyan
Write-Host "1. HTTPS (easier, requires token)" -ForegroundColor Yellow
Write-Host "2. SSH (requires SSH key setup)" -ForegroundColor Yellow
$method = Read-Host "Enter choice (1 or 2)"

if ($method -eq "1") {
    $remoteUrl = "https://github.com/$username/$repoName.git"
} else {
    $remoteUrl = "git@github.com:$username/$repoName.git"
}

# Add remote
Write-Host ""
Write-Host "Adding remote..." -ForegroundColor Cyan
git remote add origin $remoteUrl

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK: Remote added successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Create the repository on GitHub (if not already created)" -ForegroundColor Yellow
    Write-Host "   Go to: https://github.com/new" -ForegroundColor Yellow
    Write-Host "   Name: $repoName" -ForegroundColor Yellow
    Write-Host "   DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "2. Push your code:" -ForegroundColor Yellow
    Write-Host "   git push -u origin $currentBranch" -ForegroundColor White
    Write-Host ""
    Write-Host "   If your GitHub default branch is 'main', use:" -ForegroundColor Yellow
    Write-Host "   git push -u origin ${currentBranch}:main" -ForegroundColor White
    Write-Host ""
    
    $pushNow = Read-Host "Do you want to push now? (y/n)"
    if ($pushNow -eq "y") {
        Write-Host ""
        Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
        git push -u origin $currentBranch
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "OK: Successfully pushed to GitHub!" -ForegroundColor Green
            Write-Host "View your repo: https://github.com/$username/$repoName" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "ERROR: Push failed. Common issues:" -ForegroundColor Red
            Write-Host "   - Repository doesn't exist on GitHub yet" -ForegroundColor Yellow
            Write-Host "   - Authentication failed (use Personal Access Token)" -ForegroundColor Yellow
            Write-Host "   - Branch name mismatch (try: git push -u origin ${currentBranch}:main)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "ERROR: Failed to add remote" -ForegroundColor Red
}
