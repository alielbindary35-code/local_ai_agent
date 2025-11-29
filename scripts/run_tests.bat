@echo off
REM Test Runner Script for Windows

echo.
echo ========================================
echo   Running Tests
echo ========================================
echo.

REM Change to project root
cd /d "%~dp0\.."

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)

REM Check if pytest is installed
python -c "import pytest" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing pytest...
    pip install pytest pytest-cov pytest-mock
)

REM Run tests
echo [INFO] Running tests...
echo.
python run_tests.py

if errorlevel 1 (
    echo.
    echo [ERROR] Some tests failed
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] All tests passed!
)

pause

