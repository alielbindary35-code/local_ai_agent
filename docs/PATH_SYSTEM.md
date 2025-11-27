# Path System Documentation - نظام المسارات

## Overview

The project uses a centralized path management system that automatically detects the project root and provides consistent paths regardless of execution context (terminal, Colab, Jupyter, etc.).

## Core Module: `src/core/paths.py`

### Key Functions

#### `get_project_root() -> Path`
Automatically finds the project root by looking for markers:
- `.git` directory
- `requirements.txt`
- `src/` directory
- `config.py`
- `data/essential_tools.json`

#### Directory Functions
- `get_data_dir()` - `data/`
- `get_knowledge_base_dir()` - `data/knowledge_base/`
- `get_scripts_dir()` - `scripts/`
- `get_examples_dir()` - `examples/`
- `get_docs_dir()` - `docs/`
- `get_logs_dir()` - `data/logs_backup/`
- `get_notebooks_dir()` - `notebooks/`

#### File Functions
- `get_essential_tools_file()` - `data/essential_tools.json`
- `get_learning_progress_file()` - `data/learning_progress.json`
- `get_memory_db_file()` - `data/agent_memory.db`

#### Utility Functions
- `ensure_dir(path)` - Creates directory if it doesn't exist
- `add_project_to_path()` - Adds project root to `sys.path`

## Configuration: `config.py`

Centralized configuration file that imports all paths from `paths.py`:

```python
from config import (
    PROJECT_ROOT,
    DATA_DIR,
    KNOWLEDGE_BASE_DIR,
    # ... etc
)
```

## Usage Examples

### In Python Files

```python
from src.core.paths import get_knowledge_base_dir, ensure_dir

# Get knowledge base directory
kb_dir = get_knowledge_base_dir()

# Ensure directory exists
ensure_dir(kb_dir)
```

### In PowerShell Scripts

```powershell
# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Use project root for paths
$toolsFile = Join-Path $ProjectRoot "data\essential_tools.json"
```

## Benefits

1. **Works from anywhere**: Automatically detects project root
2. **Cross-platform**: Works on Windows, Linux, macOS
3. **Colab/Jupyter compatible**: Works in cloud environments
4. **Consistent**: All code uses the same path system
5. **Maintainable**: Change paths in one place

## Migration

All existing code has been updated to use the new path system:
- ✅ `src/tools/auto_learner.py`
- ✅ `src/tools/fast_learning.py`
- ✅ `src/tools/expert_tools.py`
- ✅ `src/core/memory.py`
- ✅ All PowerShell scripts
- ✅ All batch scripts

## Troubleshooting

If paths don't work:
1. Ensure you're in the project directory
2. Check that markers exist (`.git`, `requirements.txt`, etc.)
3. Verify `src/core/paths.py` is accessible
4. Check file permissions

