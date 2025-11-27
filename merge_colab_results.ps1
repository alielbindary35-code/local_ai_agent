# Merge Colab Knowledge Base with Local
# This script merges the downloaded knowledge_base.zip with your local knowledge base

Write-Host "🔄 Merging Colab Knowledge Base with Local" -ForegroundColor Cyan
Write-Host ""

# Check if zip exists in Downloads (try both names)
$zipPath = $null
$possibleNames = @(
    "$HOME\Downloads\knowledge_base_complete.zip",
    "$HOME\Downloads\knowledge_base.zip"
)

foreach ($name in $possibleNames) {
    if (Test-Path $name) {
        $zipPath = $name
        break
    }
}

if (-not $zipPath) {
    Write-Host "❌ Knowledge base zip not found in Downloads folder" -ForegroundColor Red
    Write-Host "Looking for:" -ForegroundColor Yellow
    foreach ($name in $possibleNames) {
        Write-Host "  - $name" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please download the zip file from Colab first, or specify the path:" -ForegroundColor Yellow
    $customPath = Read-Host "Enter path to knowledge_base zip (or press Enter to exit)"
    if ($customPath -and (Test-Path $customPath)) {
        $zipPath = $customPath
    } else {
        exit 1
    }
}

Write-Host "✅ Found zip file: $zipPath" -ForegroundColor Green

# Create temp extraction directory
$tempDir = "$HOME\Downloads\knowledge_base_temp"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host ""
Write-Host "📦 Extracting zip file..." -ForegroundColor Cyan
try {
    Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
    Write-Host "✅ Extraction complete" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to extract: $_" -ForegroundColor Red
    exit 1
}

# Find the knowledge_base folder inside
$extractedKb = Get-ChildItem -Path $tempDir -Recurse -Directory -Filter "knowledge_base" | Select-Object -First 1
if (-not $extractedKb) {
    # Maybe it's directly in tempDir
    $extractedKb = Get-Item $tempDir
}

Write-Host ""
Write-Host "📂 Found knowledge base at: $($extractedKb.FullName)" -ForegroundColor Cyan

# Count folders
$folders = Get-ChildItem -Path $extractedKb.FullName -Directory
Write-Host "📚 Found $($folders.Count) technology folders" -ForegroundColor Yellow

# Ensure local knowledge base exists
$localKb = "data\knowledge_base"
if (-not (Test-Path $localKb)) {
    New-Item -ItemType Directory -Path $localKb | Out-Null
    Write-Host "✅ Created local knowledge base directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔄 Copying folders to local knowledge base..." -ForegroundColor Cyan

$copied = 0
$skipped = 0
foreach ($folder in $folders) {
    $dest = Join-Path $localKb $folder.Name
    if (Test-Path $dest) {
        Write-Host "  ⚠️  $($folder.Name) already exists - merging..." -ForegroundColor Yellow
        # Merge contents
        Copy-Item -Path "$($folder.FullName)\*" -Destination $dest -Recurse -Force
        $merged = $true
    } else {
        Copy-Item -Path $folder.FullName -Destination $dest -Recurse
        Write-Host "  ✅ Copied $($folder.Name)" -ForegroundColor Green
        $copied++
    }
}

Write-Host ""
Write-Host "✨ Merge Complete!" -ForegroundColor Green
Write-Host "   Copied: $copied new folders" -ForegroundColor Cyan
Write-Host "   Merged: $($folders.Count - $copied) existing folders" -ForegroundColor Cyan

# Cleanup
Write-Host ""
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Cyan
Remove-Item -Path $tempDir -Recurse -Force
Write-Host "✅ Cleanup complete" -ForegroundColor Green

# Merge progress file if exists
$progressFile = "$HOME\Downloads\learning_progress.json"
if (Test-Path $progressFile) {
    Write-Host ""
    Write-Host "📊 Merging progress file..." -ForegroundColor Cyan
    
    $localProgress = @()
    $localProgressFile = "data\learning_progress.json"
    if (Test-Path $localProgressFile) {
        $localProgress = Get-Content $localProgressFile | ConvertFrom-Json
    }
    
    $colabProgress = Get-Content $progressFile | ConvertFrom-Json
    
    # Merge (Colab takes priority, but keep unique local items)
    $mergedProgress = ($localProgress + $colabProgress) | Select-Object -Unique | Sort-Object
    
    $mergedProgress | ConvertTo-Json | Set-Content $localProgressFile
    Write-Host "✅ Progress merged: $($mergedProgress.Count) tools learned" -ForegroundColor Green
}

Write-Host ""
Write-Host "📂 Your local knowledge base is now at: $(Resolve-Path $localKb)" -ForegroundColor Cyan

# Final summary
$finalFolders = (Get-ChildItem -Path $localKb -Directory).Count
$finalProgress = @()
if (Test-Path "data\learning_progress.json") {
    $finalProgress = Get-Content "data\learning_progress.json" | ConvertFrom-Json
}

Write-Host ""
Write-Host "📊 Final Summary:" -ForegroundColor Cyan
Write-Host "   Knowledge Base Folders: $finalFolders" -ForegroundColor Yellow
Write-Host "   Learned Tools: $($finalProgress.Count)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 Done! Your agent now has all the knowledge from Colab!" -ForegroundColor Green

