@echo off
chcp 65001 >nul
color 0A
title Local AI Agent - Desktop Application

echo ╔════════════════════════════════════════════════════════════╗
echo ║     Local AI Agent - Desktop Application Launcher         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
)

REM Check PyQt6
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyQt6 and dependencies...
    pip install PyQt6 PyQt6-Qt6 PyQt6-sip markdown
)

REM Check Ollama
ollama list >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running or not installed.
    echo [WARNING] Please start Ollama before using the application.
    echo.
    pause
)

echo.
echo [INFO] Starting Desktop Application...
echo.

python desktop_app/main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start.
    pause
)

