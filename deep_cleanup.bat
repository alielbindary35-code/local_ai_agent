@echo off
chcp 65001 >nul
color 0C
title Deep Project Cleanup - Remove ALL Non-Essential Files

echo ╔════════════════════════════════════════════════════════════╗
echo ║       DEEP PROJECT CLEANUP - AGGRESSIVE MODE               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  THIS WILL REMOVE A LOT OF FILES! ⚠️
echo.
echo WILL KEEP ONLY:
echo  ✓ src/ (core agent code)
echo  ✓ KnowledgeHarvester/
echo  ✓ data/agent_memory.db (knowledge base)
echo  ✓ data/essential_tools.json
echo  ✓ menu.bat
echo  ✓ requirements.txt
echo  ✓ README.md
echo  ✓ PROJECT_GUIDE.md and PROJECT_GUIDE.html
echo  ✓ .git/ (version control)
echo  ✓ .gitignore
echo.
echo WILL DELETE:
echo  ✗ All test files and folders
echo  ✗ All example files
echo  ✗ All documentation except PROJECT_GUIDE
echo  ✗ All batch files except menu.bat
echo  ✗ All text files in root
echo  ✗ All Python cache files
echo  ✗ All log files
echo  ✗ notebooks/, htmlcov/, .pytest_cache/
echo  ✗ scripts/ folder (all batch files moved to menu.bat)
echo  ✗ linux_server_management/, project_name/
echo  ✗ All markdown files except README and PROJECT_GUIDE
echo.
echo ⚠️  WARNING: THIS CANNOT BE UNDONE! ⚠️
echo.
set /p confirm="Type 'DELETE' to confirm: "

if /i not "%confirm%"=="DELETE" (
    echo Cleanup cancelled.
    pause
    exit /b
)

echo.
echo Starting DEEP cleanup...
echo.

REM Remove all folders that are not essential
echo [1/15] Removing non-essential folders...
if exist tests rd /s /q tests 2>nul
if exist examples rd /s /q examples 2>nul
if exist notebooks rd /s /q notebooks 2>nul
if exist htmlcov rd /s /q htmlcov 2>nul
if exist .pytest_cache rd /s /q .pytest_cache 2>nul
if exist scripts rd /s /q scripts 2>nul
if exist linux_server_management rd /s /q linux_server_management 2>nul
if exist project_name rd /s /q project_name 2>nul
if exist .cursor rd /s /q .cursor 2>nul
echo ✓ Done

REM Remove docs folder (we have PROJECT_GUIDE now)
echo [2/15] Removing old documentation...
if exist docs rd /s /q docs 2>nul
echo ✓ Done

REM Remove all __pycache__ directories
echo [3/15] Removing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo ✓ Done

REM Remove coverage files
echo [4/15] Removing coverage reports...
if exist .coverage del /q .coverage
if exist coverage.xml del /q coverage.xml
echo ✓ Done

REM Remove all text files in root
echo [5/15] Removing text files...
if exist training_report.txt del /q training_report.txt
if exist test_agent.txt del /q test_agent.txt
if exist test_output.txt del /q test_output.txt
if exist pytest.ini del /q pytest.ini
if exist run_tests.py del /q run_tests.py
if exist config.py del /q config.py
echo ✓ Done

REM Remove all markdown files except README and PROJECT_GUIDE
echo [6/15] Removing redundant markdown files...
if exist AGENT_CAPABILITIES_TABLE.md del /q AGENT_CAPABILITIES_TABLE.md
if exist COMPREHENSIVE_TEST_READY.md del /q COMPREHENSIVE_TEST_READY.md
if exist ENHANCEMENTS_SUMMARY.md del /q ENHANCEMENTS_SUMMARY.md
if exist EVALUATION_GUIDE.md del /q EVALUATION_GUIDE.md
echo ✓ Done

REM Clean data folder - keep only essential files
echo [7/15] Cleaning data folder...
if exist data\README.md del /q data\README.md
if exist data\training_report.txt del /q data\training_report.txt
if exist data\logs rd /s /q data\logs 2>nul
if exist data\logs_backup rd /s /q data\logs_backup 2>nul
echo ✓ Done

REM Remove evaluation logs
echo [8/15] Removing evaluation logs...
if exist data\evaluation_logs rd /s /q data\evaluation_logs 2>nul
echo ✓ Done

REM Remove knowledge base files (we have new harvested data)
echo [9/15] Cleaning old knowledge base...
if exist data\knowledge_base rd /s /q data\knowledge_base 2>nul
echo ✓ Done

REM Remove learning progress
echo [10/15] Removing old learning data...
if exist data\learning_progress.json del /q data\learning_progress.json
echo ✓ Done

REM Remove all Python files in root
echo [11/15] Removing root Python files...
if exist verify_learning.py del /q verify_learning.py
echo ✓ Done

REM Remove all markdown files in root except essential
echo [12/15] Final markdown cleanup...
for %%f in (*.md) do (
    if /i not "%%f"=="README.md" if /i not "%%f"=="PROJECT_GUIDE.md" del /q "%%f"
)
echo ✓ Done

REM Remove HTML files except PROJECT_GUIDE
echo [13/15] Cleaning HTML files...
for %%f in (*.html) do (
    if /i not "%%f"=="PROJECT_GUIDE.html" del /q "%%f"
)
echo ✓ Done

REM Remove batch files except menu.bat and cleanup.bat
echo [14/15] Removing redundant batch files...
for %%f in (*.bat) do (
    if /i not "%%f"=="menu.bat" if /i not "%%f"=="cleanup.bat" if /i not "%%f"=="deep_cleanup.bat" del /q "%%f"
)
echo ✓ Done

REM Create essential data folders if they don't exist
echo [15/15] Ensuring essential folders exist...
if not exist data mkdir data
if not exist data\logs mkdir data\logs
echo ✓ Done

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          DEEP CLEANUP COMPLETE!                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Your project now contains ONLY:
echo.
echo 📁 Essential Folders:
echo   ├── src/                    (Core agent code)
echo   ├── KnowledgeHarvester/     (Documentation harvester)
echo   ├── data/                   (Knowledge base + essential data)
echo   ├── venv/                   (Python virtual environment)
echo   └── .git/                   (Version control)
echo.
echo 📄 Essential Files:
echo   ├── menu.bat                (Main interface)
echo   ├── cleanup.bat             (This file)
echo   ├── requirements.txt        (Dependencies)
echo   ├── README.md               (Basic readme)
echo   ├── PROJECT_GUIDE.md        (Complete guide)
echo   ├── PROJECT_GUIDE.html      (HTML guide)
echo   └── .gitignore              (Git config)
echo.
echo ✨ Your project is now clean and minimal!
echo.
pause
