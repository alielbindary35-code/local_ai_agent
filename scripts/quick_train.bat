@echo off
REM Quick Training Script - سكريبت تدريب سريع
REM يشغل Simple Agent مع أسئلة تدريبية

REM Change to script directory to ensure relative paths work
cd /d "%~dp0\.."
set PYTHONPATH=%CD%;%PYTHONPATH%

echo ========================================
echo    AI Agent Quick Training
echo    تدريب سريع للوكيل الذكي
echo ========================================
echo.

echo [1] Test Simple Agent (3 questions)
echo [2] Run Automated Training (11 questions)
echo [3] Monitor Training (real-time)
echo [4] View Training Logs
echo [5] Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Running Simple Agent Test...
    python src\agents\simple_agent.py
    pause
)

if "%choice%"=="2" (
    echo.
    echo Starting Automated Training...
    echo This will take several minutes...
    python src\core\automated_trainer.py
    pause
)

if "%choice%"=="3" (
    echo.
    echo Starting Real-time Monitor...
    echo Press Ctrl+C to stop
    python src\core\monitor_training.py monitor 300
    pause
)

if "%choice%"=="4" (
    echo.
    echo Showing last 50 lines of training log...
    python src\core\monitor_training.py tail 50
    pause
)

if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit
)

echo.
echo Invalid choice. Please run again.
pause
