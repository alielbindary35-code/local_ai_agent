@echo off
title Agent Training Run
echo Starting Agent Training...

REM Change to script directory to ensure relative paths work
cd /d "%~dp0\.."
set PYTHONPATH=%CD%;%PYTHONPATH%

python src\core\train_agent.py
echo.
echo Training complete. You can close this window.
pause
