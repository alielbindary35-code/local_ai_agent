# Core System Components

This directory contains the core functionality of the AI agent system.

## Components

### Memory System (`memory.py`)
SQLite-based persistent memory for:
- Storing solutions and problem-solving history
- Custom tool registry
- Package installation tracking
- User preferences
- Error pattern tracking

**Usage:**
```python
from src.core.memory import Memory

memory = Memory()
memory.save_solution(problem="...", solution="...", rating=5)
similar = memory.search_similar("check disk space")
```

### Prompt System (`prompts.py`)
Advanced prompt templates and formatters:
- System prompts for different task types
- Security-aware prompts
- Data analysis prompts
- Deployment prompts
- Response formatting

### Path Management (`paths.py`)
Centralized path management system:
- Automatic project root detection
- Consistent paths across environments
- Directory creation utilities

**Usage:**
```python
from src.core.paths import get_project_root, get_data_dir

root = get_project_root()
data_dir = get_data_dir()
```

### Training System
- **`trainer.py`**: Manual training workflows
- **`automated_trainer.py`**: Automated training scenarios
- **`monitor_training.py`**: Training progress monitoring
- **`train_agent.py`**: Agent training scripts

### Memory Management
- **`clean_memory.py`**: Memory cleanup utilities

## Best Practices

- Always use `paths.py` for file paths (don't hardcode)
- Use memory system for persistent storage
- Follow prompt templates for consistency
- Log training progress for monitoring

