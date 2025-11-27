@echo off
echo Organizing project structure...
echo.

REM Create directories
if not exist "src\agents" mkdir "src\agents"
if not exist "src\tools" mkdir "src\tools"
if not exist "src\core" mkdir "src\core"
if not exist "scripts" mkdir "scripts"
if not exist "docs" mkdir "docs"
if not exist "tests" mkdir "tests"
if not exist "data" mkdir "data"
if not exist "examples" mkdir "examples"

echo Directories created.

REM Move agent files
if exist "agent.py" move "agent.py" "src\agents\"
if exist "expert_agent.py" move "expert_agent.py" "src\agents\"
if exist "simple_agent.py" move "simple_agent.py" "src\agents\"
echo Agents moved.

REM Move tool files
if exist "tools.py" move "tools.py" "src\tools\"
if exist "expert_tools.py" move "expert_tools.py" "src\tools\"
if exist "extended_tools.py" move "extended_tools.py" "src\tools\"
echo Tools moved.

REM Move core files
if exist "memory.py" move "memory.py" "src\core\"
if exist "prompts.py" move "prompts.py" "src\core\"
if exist "simple_prompts.py" move "simple_prompts.py" "src\core\"
if exist "trainer.py" move "trainer.py" "src\core\"
if exist "automated_trainer.py" move "automated_trainer.py" "src\core\"
if exist "monitor_training.py" move "monitor_training.py" "src\core\"
if exist "train_agent.py" move "train_agent.py" "src\core\"
if exist "clean_memory.py" move "clean_memory.py" "src\core\"
echo Core files moved.

REM Move scripts
move "*.bat" "scripts\" 2>nul
move "*.sh" "scripts\" 2>nul
echo Scripts moved.

REM Move documentation (keep README.md in root)
for %%f in (*.md) do (
    if not "%%f"=="README.md" move "%%f" "docs\"
)
if exist "documentation.html" move "documentation.html" "docs\"
echo Documentation moved.

REM Move test files
move "test_*.py" "tests\" 2>nul
move "test_*.txt" "tests\" 2>nul
if exist "verify_agent.py" move "verify_agent.py" "tests\"
if exist "test_output.txt" move "test_output.txt" "tests\"
echo Tests moved.

REM Move data files
if exist "agent_log.txt" move "agent_log.txt" "data\"
if exist "agent_memory.db" move "agent_memory.db" "data\"
if exist "training_report.txt" move "training_report.txt" "data\"
if exist "logs" move "logs" "data\logs_backup"
if exist "knowledge_base" move "knowledge_base" "data\knowledge_base"
echo Data files moved.

REM Move examples
if exist "learn_docker.py" move "learn_docker.py" "examples\"
if exist "force_create_n8n.py" move "force_create_n8n.py" "examples\"
if exist "interactive_session.py" move "interactive_session.py" "examples\"
echo Examples moved.

echo.
echo Project organization complete!
echo.
echo Next steps:
echo 1. Update import statements in Python files
echo 2. Update script paths in batch files
echo 3. Test that everything works
pause

