@echo off
chcp 65001 >nul
color 0C
title Project Cleanup - Remove Unnecessary Files

echo ╔════════════════════════════════════════════════════════════╗
echo ║          PROJECT CLEANUP UTILITY                           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo This will remove:
echo  - All __pycache__ folders and .pyc files
echo  - Test output files (test_agent.txt, test_output.txt)
echo  - Old log files
echo  - Duplicate/redundant batch files
echo  - Coverage reports
echo  - Temporary files
echo.
echo ⚠️  WARNING: This action cannot be undone!
echo.
set /p confirm="Are you sure you want to continue? (yes/no): "

if /i not "%confirm%"=="yes" (
    echo Cleanup cancelled.
    pause
    exit /b
)

echo.
echo Starting cleanup...
echo.

REM Remove all __pycache__ directories
echo [1/8] Removing __pycache__ directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
echo ✓ Done

REM Remove .pyc files
echo [2/8] Removing .pyc files...
del /s /q *.pyc 2>nul
echo ✓ Done

REM Remove test output files
echo [3/8] Removing test output files...
if exist test_agent.txt del /q test_agent.txt
if exist test_output.txt del /q test_output.txt
echo ✓ Done

REM Remove coverage files
echo [4/8] Removing coverage reports...
if exist .coverage del /q .coverage
if exist coverage.xml del /q coverage.xml
if exist htmlcov rd /s /q htmlcov 2>nul
echo ✓ Done

REM Remove old log files
echo [5/8] Cleaning old log files...
if exist data\logs\errors.log del /q data\logs\errors.log
if exist data\logs_backup\error.log del /q data\logs_backup\error.log
echo ✓ Done

REM Remove duplicate batch files (keep only menu.bat)
echo [6/8] Removing redundant batch files...
if exist scripts\test_enhancements.bat del /q scripts\test_enhancements.bat
if exist scripts\test_comprehensive_training.bat del /q scripts\test_comprehensive_training.bat
if exist scripts\run_training.bat del /q scripts\run_training.bat
if exist scripts\run_comprehensive_training_simple.bat del /q scripts\run_comprehensive_training_simple.bat
if exist scripts\run_comprehensive_training.bat del /q scripts\run_comprehensive_training.bat
if exist scripts\run_comprehensive_evaluation.bat del /q scripts\run_comprehensive_evaluation.bat
if exist scripts\run_agent.bat del /q scripts\run_agent.bat
if exist scripts\quick_train.bat del /q scripts\quick_train.bat
if exist scripts\expert_launcher.bat del /q scripts\expert_launcher.bat
echo ✓ Done

REM Remove empty training report
echo [7/8] Removing empty files...
if exist data\training_report.txt del /q data\training_report.txt
echo ✓ Done

REM Remove pytest cache
echo [8/8] Removing pytest cache...
if exist .pytest_cache rd /s /q .pytest_cache 2>nul
echo ✓ Done

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          CLEANUP COMPLETE!                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Summary:
echo  ✓ Removed all Python cache files
echo  ✓ Removed test output files
echo  ✓ Removed coverage reports
echo  ✓ Cleaned old log files
echo  ✓ Removed redundant batch files
echo  ✓ Removed temporary files
echo.
echo Your project is now clean and organized!
echo Use menu.bat for all operations.
echo.
pause
