@echo off
REM Test script to verify all paths are correct
echo Testing project paths...
echo.

REM Change to script directory
cd /d "%~dp0\.."
set PYTHONPATH=%CD%;%PYTHONPATH%

echo Current directory: %CD%
echo PYTHONPATH: %PYTHONPATH%
echo.

echo Checking if files exist:
echo.

if exist "src\agents\agent.py" (
    echo [OK] src\agents\agent.py
) else (
    echo [ERROR] src\agents\agent.py NOT FOUND
)

if exist "src\agents\expert_agent.py" (
    echo [OK] src\agents\expert_agent.py
) else (
    echo [ERROR] src\agents\expert_agent.py NOT FOUND
)

if exist "src\tools\tools.py" (
    echo [OK] src\tools\tools.py
) else (
    echo [ERROR] src\tools\tools.py NOT FOUND
)

if exist "src\core\memory.py" (
    echo [OK] src\core\memory.py
) else (
    echo [ERROR] src\core\memory.py NOT FOUND
)

if exist "requirements.txt" (
    echo [OK] requirements.txt
) else (
    echo [ERROR] requirements.txt NOT FOUND
)

echo.
echo Testing Python import...
python -c "import sys; sys.path.insert(0, '.'); from src.agents.agent import Agent; print('[OK] Agent import successful')" 2>&1

echo.
echo Path test complete!
pause

