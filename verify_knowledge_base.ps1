# Verify Knowledge Base Completeness
# تحقق من اكتمال قاعدة المعرفة

Write-Host "🔍 Verifying Knowledge Base" -ForegroundColor Cyan
Write-Host ""

# Load essential tools
$toolsFile = "data\essential_tools.json"
if (-not (Test-Path $toolsFile)) {
    Write-Host "❌ essential_tools.json not found!" -ForegroundColor Red
    exit 1
}

$essentialTools = Get-Content $toolsFile | ConvertFrom-Json

# Count total tools
$totalTools = 0
$toolsByCategory = @{}
foreach ($category in $essentialTools.PSObject.Properties.Name) {
    $count = ($essentialTools.$category | Measure-Object).Count
    $totalTools += $count
    $toolsByCategory[$category] = $count
}

Write-Host "📚 Essential Tools Summary:" -ForegroundColor Yellow
foreach ($category in $toolsByCategory.Keys) {
    Write-Host "   $category`: $($toolsByCategory[$category]) tools" -ForegroundColor White
}
Write-Host "   Total: $totalTools tools" -ForegroundColor Green
Write-Host ""

# Check progress
$progressFile = "data\learning_progress.json"
$learnedTools = @()
if (Test-Path $progressFile) {
    $learnedTools = Get-Content $progressFile | ConvertFrom-Json
    Write-Host "✅ Progress file found: $($learnedTools.Count) tools learned" -ForegroundColor Green
} else {
    Write-Host "⚠️  Progress file not found" -ForegroundColor Yellow
}

# Check knowledge base folders
$kbPath = "data\knowledge_base"
$kbFolders = @()
if (Test-Path $kbPath) {
    $kbFolders = Get-ChildItem -Path $kbPath -Directory | ForEach-Object { $_.Name }
    Write-Host "✅ Knowledge base found: $($kbFolders.Count) folders" -ForegroundColor Green
} else {
    Write-Host "❌ Knowledge base not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📊 Comparison:" -ForegroundColor Cyan
Write-Host "   Essential Tools: $totalTools" -ForegroundColor Yellow
Write-Host "   Learned (Progress): $($learnedTools.Count)" -ForegroundColor Yellow
Write-Host "   Knowledge Base Folders: $($kbFolders.Count)" -ForegroundColor Yellow
Write-Host ""

# Find missing tools
$allEssentialTools = @()
foreach ($category in $essentialTools.PSObject.Properties.Name) {
    $allEssentialTools += $essentialTools.$category
}

$missingFromProgress = $allEssentialTools | Where-Object { $_ -notin $learnedTools }
$missingFromKB = $allEssentialTools | Where-Object { 
    $toolName = $_ -replace '[^a-zA-Z0-9]', '_'
    $toolName = $toolName.ToLower()
    $found = $false
    foreach ($folder in $kbFolders) {
        if ($folder -replace '[^a-zA-Z0-9]', '_' -eq $toolName) {
            $found = $true
            break
        }
    }
    -not $found
}

if ($missingFromProgress.Count -eq 0 -and $missingFromKB.Count -eq 0) {
    Write-Host "🎉 Perfect! All tools are learned and in knowledge base!" -ForegroundColor Green
} else {
    if ($missingFromProgress.Count -gt 0) {
        Write-Host "⚠️  Missing from progress ($($missingFromProgress.Count)):" -ForegroundColor Yellow
        $missingFromProgress | ForEach-Object { Write-Host "   - $_" -ForegroundColor White }
    }
    
    if ($missingFromKB.Count -gt 0) {
        Write-Host "⚠️  Missing from knowledge base ($($missingFromKB.Count)):" -ForegroundColor Yellow
        $missingFromKB | ForEach-Object { Write-Host "   - $_" -ForegroundColor White }
    }
}

Write-Host ""
Write-Host "💡 Recommendation:" -ForegroundColor Cyan
if ($missingFromProgress.Count -gt 0 -or $missingFromKB.Count -gt 0) {
    Write-Host "   Run the auto-learner to complete missing tools:" -ForegroundColor Yellow
    Write-Host "   python src/tools/auto_learner.py" -ForegroundColor White
    Write-Host "   OR use Colab for faster learning!" -ForegroundColor White
} else {
    Write-Host "   ✅ Your agent is ready with all tools!" -ForegroundColor Green
}

