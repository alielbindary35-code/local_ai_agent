# Project Organization Guide

## Current Status
The project files are currently in the root directory and need to be organized into a proper structure.

## Proposed Structure

```
local_ai_agent/
├── src/                    # Source code
│   ├── agents/            # Agent implementations
│   │   ├── agent.py
│   │   ├── expert_agent.py
│   │   └── simple_agent.py
│   ├── tools/             # Tool libraries
│   │   ├── tools.py
│   │   ├── expert_tools.py
│   │   └── extended_tools.py
│   └── core/              # Core functionality
│       ├── memory.py
│       ├── prompts.py
│       ├── simple_prompts.py
│       ├── trainer.py
│       ├── automated_trainer.py
│       ├── monitor_training.py
│       ├── train_agent.py
│       └── clean_memory.py
├── scripts/               # Batch and shell scripts
│   ├── run_agent.bat
│   ├── run_agent.sh
│   ├── expert_launcher.bat
│   ├── quick_train.bat
│   └── run_training.bat
├── docs/                  # Documentation
│   ├── EXPERT_AGENT_GUIDE.md
│   ├── QUICK_TRAINING_GUIDE.md
│   ├── TRAINING_PLAN.md
│   ├── TRAINING_REPORT.md
│   ├── SYSTEM_SUMMARY.md
│   ├── TASK_LIST.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── documentation.html
├── tests/                 # Test files
│   ├── test_learning.py
│   ├── test_recall.py
│   ├── verify_agent.py
│   ├── test_agent.txt
│   └── test_output.txt
├── examples/              # Example scripts
│   ├── learn_docker.py
│   ├── force_create_n8n.py
│   └── interactive_session.py
├── data/                  # Data and logs
│   ├── agent_log.txt
│   ├── agent_memory.db
│   ├── training_report.txt
│   ├── logs_backup/
│   └── knowledge_base/
│       └── n8n/
├── requirements.txt
├── README.md
└── venv/
```

## Manual Organization Steps

Since automated scripts may not work in all environments, here are manual steps:

### 1. Create Directories
```bash
mkdir src\agents src\tools src\core scripts docs tests data examples
```

### 2. Move Agent Files
```bash
move agent.py src\agents\
move expert_agent.py src\agents\
move simple_agent.py src\agents\
```

### 3. Move Tool Files
```bash
move tools.py src\tools\
move expert_tools.py src\tools\
move extended_tools.py src\tools\
```

### 4. Move Core Files
```bash
move memory.py src\core\
move prompts.py src\core\
move simple_prompts.py src\core\
move trainer.py src\core\
move automated_trainer.py src\core\
move monitor_training.py src\core\
move train_agent.py src\core\
move clean_memory.py src\core\
```

### 5. Move Scripts
```bash
move *.bat scripts\
move *.sh scripts\
```

### 6. Move Documentation
```bash
move EXPERT_AGENT_GUIDE.md docs\
move QUICK_TRAINING_GUIDE.md docs\
move TRAINING_PLAN.md docs\
move TRAINING_REPORT.md docs\
move SYSTEM_SUMMARY.md docs\
move TASK_LIST.md docs\
move IMPLEMENTATION_PLAN.md docs\
move documentation.html docs\
# Keep README.md in root
```

### 7. Move Tests
```bash
move test_*.py tests\
move test_*.txt tests\
move verify_agent.py tests\
move test_output.txt tests\
```

### 8. Move Data Files
```bash
move agent_log.txt data\
move agent_memory.db data\
move training_report.txt data\
move logs data\logs_backup
move knowledge_base data\knowledge_base
```

### 9. Move Examples
```bash
move learn_docker.py examples\
move force_create_n8n.py examples\
move interactive_session.py examples\
```

## After Organization

### Update Imports
All Python files will need their imports updated. For example:

**Before:**
```python
from tools import Tools
from memory import Memory
```

**After:**
```python
from src.tools.tools import Tools
from src.core.memory import Memory
```

Or add the project root to PYTHONPATH and use:
```python
from src.tools import Tools
from src.core import Memory
```

### Update Scripts
Batch and shell scripts will need path updates to point to the new locations.

### Test Everything
Run tests to ensure everything still works after reorganization.

## Benefits

1. **Professional Structure** - Follows Python project best practices
2. **Easy Navigation** - Files organized by purpose
3. **Scalable** - Easy to add new files
4. **Maintainable** - Clear organization
5. **Standard** - Matches common Python project layouts

