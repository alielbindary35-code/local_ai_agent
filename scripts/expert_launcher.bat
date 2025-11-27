@echo off
setlocal
title Expert AI Agent Launcher

REM Change to script directory to ensure relative paths work
cd /d "%~dp0\.."
set PYTHONPATH=%CD%;%PYTHONPATH%

:MENU
cls
echo ========================================
echo    Expert AI Agent Launcher
echo    Multi-Model System with 137+ Tools
echo ========================================
echo.
echo Available Options:
echo.
echo [1] Run Expert Agent (Interactive Mode)
echo [2] Quick Test (3 sample tasks)
echo [3] Show Available Models
echo [4] Show All Tools (137+)
echo [5] Run Training Session
echo [6] Monitor Training Logs
echo [7] Learn New Technology
echo [8] View Documentation (HTML)
echo [9] Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto RUN_INTERACTIVE
if "%choice%"=="2" goto RUN_TEST
if "%choice%"=="3" goto SHOW_MODELS
if "%choice%"=="4" goto SHOW_TOOLS
if "%choice%"=="5" goto RUN_TRAINING
if "%choice%"=="6" goto MONITOR_LOGS
if "%choice%"=="7" goto LEARN_TECH
if "%choice%"=="8" goto VIEW_DOCS
if "%choice%"=="9" goto EXIT

echo.
echo Invalid choice. Please try again.
pause
goto MENU

:RUN_INTERACTIVE
cls
echo Starting Expert Agent in Interactive Mode...
python examples\interactive_session.py
echo.
echo Session ended.
pause
goto MENU

:RUN_TEST
cls
echo Running Quick Test...
python src\agents\expert_agent.py
if errorlevel 1 (
    echo.
    echo ❌ Error occurred during execution.
)
echo.
pause
goto MENU

:SHOW_MODELS
cls
echo Available Models:
echo.
ollama list
echo.
pause
goto MENU

:SHOW_TOOLS
cls
echo Loading Tools Library...
python -c "import sys; sys.path.insert(0, '.'); from src.tools.tools import Tools; from src.tools.expert_tools import ExpertTools; from src.tools.extended_tools import ExtendedTools; t1 = Tools(); t2 = ExpertTools(); t3 = ExtendedTools(); print('\n=== BASIC TOOLS ==='); print(t1.get_tool_descriptions()); print('\n=== EXPERT TOOLS ==='); print(t2.get_tool_descriptions()); print('\n=== EXTENDED TOOLS ==='); print(t3.get_tool_descriptions())"
echo.
pause
goto MENU

:RUN_TRAINING
cls
echo Starting Automated Training...
python src\core\automated_trainer.py
pause
goto MENU

:MONITOR_LOGS
cls
echo Monitoring Logs (Press Ctrl+C to stop)...
python src\core\monitor_training.py tail 50
pause
goto MENU

:LEARN_TECH
cls
set /p tech="Enter technology to learn (e.g., Docker): "
python -c "import sys; sys.path.insert(0, '.'); from src.agents.expert_agent import ExpertAgent; agent = ExpertAgent(); agent.run('Learn %tech% best practices and save examples for offline use')"
pause
goto MENU

:VIEW_DOCS
cls
echo Opening Documentation...
start docs\documentation.html
goto MENU

:EXIT
exit
