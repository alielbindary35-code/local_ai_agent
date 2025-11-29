@echo off
chcp 65001 >nul
color 0A
title Local AI Agent - Main Menu

:MENU
cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║          LOCAL AI AGENT - CONTROL PANEL                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo  [1] Run Agent (Interactive Mode)
echo  [2] Run Expert Agent
echo  [3] Import Knowledge from Harvester
echo.
echo  ─────────────────────────────────────────────────────────────
echo  TRAINING
echo  ─────────────────────────────────────────────────────────────
echo  [4] Quick Training
echo  [5] Comprehensive Training
echo  [6] Run Comprehensive Evaluation
echo.
echo  ─────────────────────────────────────────────────────────────
echo  TESTING
echo  ─────────────────────────────────────────────────────────────
echo  [7] Run All Tests
echo  [8] Test Enhancements
echo.
echo  ─────────────────────────────────────────────────────────────
echo  KNOWLEDGE HARVESTER
echo  ─────────────────────────────────────────────────────────────
echo  [9] Run Knowledge Harvester (All Topics)
echo  [10] Run Knowledge Harvester (Specific Category)
echo.
echo  ─────────────────────────────────────────────────────────────
echo  [0] Exit
echo  ─────────────────────────────────────────────────────────────
echo.
set /p choice="Enter your choice: "

if "%choice%"=="1" goto RUN_AGENT
if "%choice%"=="2" goto RUN_EXPERT
if "%choice%"=="3" goto IMPORT_KNOWLEDGE
if "%choice%"=="4" goto QUICK_TRAIN
if "%choice%"=="5" goto COMPREHENSIVE_TRAIN
if "%choice%"=="6" goto COMPREHENSIVE_EVAL
if "%choice%"=="7" goto RUN_TESTS
if "%choice%"=="8" goto TEST_ENHANCEMENTS
if "%choice%"=="9" goto HARVEST_ALL
if "%choice%"=="10" goto HARVEST_CATEGORY
if "%choice%"=="0" goto EXIT
goto MENU

:RUN_AGENT
cls
echo Running Agent...
python -m src.agents.simple_agent
pause
goto MENU

:RUN_EXPERT
cls
echo Running Expert Agent...
python -m src.agents.expert_agent
pause
goto MENU

:IMPORT_KNOWLEDGE
cls
echo Importing Knowledge from Harvester...
python scripts/import_knowledge.py
pause
goto MENU

:QUICK_TRAIN
cls
echo Running Quick Training...
python -m src.core.train_agent
pause
goto MENU

:COMPREHENSIVE_TRAIN
cls
echo Running Comprehensive Training...
python -m src.core.comprehensive_training
pause
goto MENU

:COMPREHENSIVE_EVAL
cls
echo Running Comprehensive Evaluation...
python -m src.core.comprehensive_evaluation
pause
goto MENU

:RUN_TESTS
cls
echo Running All Tests...
python run_tests.py
pause
goto MENU

:TEST_ENHANCEMENTS
cls
echo Testing Enhancements...
pytest tests/ -v --tb=short
pause
goto MENU

:HARVEST_ALL
cls
echo Running Knowledge Harvester (All Topics)...
cd KnowledgeHarvester
python knowledge_harvester.py
cd ..
pause
goto MENU

:HARVEST_CATEGORY
cls
echo Available Categories:
echo  - python_data
echo  - javascript_nodejs
echo  - docker
echo  - postgresql
echo  - n8n
echo  - ollama
echo  - general_ai
echo.
set /p category="Enter category name: "
cd KnowledgeHarvester
python knowledge_harvester.py --category %category%
cd ..
pause
goto MENU

:EXIT
cls
echo Exiting...
exit
