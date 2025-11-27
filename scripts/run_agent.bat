@echo off
REM Expert-Level Local AI Agent - Windows Launcher

echo.
echo ========================================
echo   Expert-Level Local AI Agent
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if Ollama is running
echo.
echo Checking Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Cannot connect to Ollama at http://localhost:11434
    echo Please make sure Ollama is running.
    echo.
    echo To start Ollama:
    echo   1. Open a new terminal
    echo   2. Run: ollama serve
    echo.
    pause
)

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [WARNING] Some dependencies failed to install
    echo The agent may still work with core dependencies
    echo.
)

REM Run the agent
echo.
echo ========================================
echo   Starting Agent...
echo ========================================
echo.

REM Change to script directory to ensure relative paths work
cd /d "%~dp0\.."

REM Add src to PYTHONPATH and run agent
set PYTHONPATH=%CD%;%PYTHONPATH%
python src\agents\agent.py

REM Deactivate virtual environment on exit
deactivate

echo.
echo Agent stopped.
pause
