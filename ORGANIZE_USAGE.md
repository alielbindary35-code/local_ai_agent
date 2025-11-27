# 📁 Project Organization Script - دليل الاستخدام

## Overview

The `organize_project.py` script organizes your project files into proper directory structure using the centralized paths system.

## Usage

### Dry Run (Preview - Recommended First)

```powershell
python organize_project.py --dry-run
```

This shows what **would be moved** without actually moving anything.

### Actual Organization

```powershell
python organize_project.py
```

This actually moves files to their proper locations.

## What Gets Organized

### Files Moved to `tests/`
- `test_*.py` - All test Python files

### Files Moved to `examples/`
- `learn_*.py` - Learning scripts
- `fast_learn_*.py` - Fast learning scripts
- `colab_complete_learning.py` - Colab learning script

### Files Moved to `docs/`
- `*_GUIDE.md` - Guide files
- `*_PLAN.md` - Plan files
- `*_STEPS.md` - Steps files
- `*_FIX.md` - Fix documentation
- `HOW_TO_*.md` - How-to guides
- `PATH_*.md` - Path system docs
- `TOOLS_*.md` - Tools documentation
- `COLAB_*.md` - Colab documentation
- `DEPLOYMENT_*.md` - Deployment guides
- `QUICK_*.md` - Quick start guides
- `NEXT_*.md` - Next steps
- `MIGRATION_*.md` - Migration docs

### Files Moved to `data/`
- `agent_memory.db` - Database files
- `*.db` - Other database files
- `1.txt` - Temporary text files

### Files That Stay in Root
- `README.md` - Main readme
- `requirements.txt` - Dependencies
- `.gitignore` - Git ignore
- `config.py` - Configuration
- `organize_project.py` - This script
- `reorganize.py` - Reorganize script
- `generate_colab_notebook.py` - Notebook generator
- `GUIDE_ARABIC.md` - Main Arabic guide
- `*.ps1` - PowerShell scripts

### Cleaned Up
- `-p/` - Empty folder
- `__pycache__/` - Python cache (in root)

## Features

1. **Uses Centralized Paths**: Uses `src/core/paths.py` for consistent paths
2. **Dry Run Mode**: Preview changes before applying
3. **Safe**: Won't overwrite existing files (adds suffix if needed)
4. **Smart**: Skips files already in correct location
5. **Comprehensive**: Handles multiple file patterns

## Example Output

```
============================================================
Project Organization Script
============================================================
Working directory: C:\Users\...\local_ai_agent
Dry run: False

✓ Directory ready: ...\scripts
✓ Directory ready: ...\examples
✓ Directory ready: ...\docs
✓ Directory ready: ...\tests
✓ Directory ready: ...\data

📁 Processing Test Python files -> tests/
------------------------------------------------------------
  ✓ Moved: test_docker_learning.py -> test_docker_learning.py
  ✓ Moved: test_json_parsing.py -> test_json_parsing.py
  ✓ Moved: test_read_docker.py -> test_read_docker.py

...

============================================================
Organization Summary
============================================================
✓ Moved: 20 files
⊘ Skipped: 0 files
✗ Errors: 0 files

✅ Project organization complete!
```

## After Organization

After running the script, your project will be:
- ✅ Cleaner root directory
- ✅ Better organized structure
- ✅ Easier to navigate
- ✅ Professional layout

## Notes

- The script is **safe** - it won't delete files, only move them
- If a file already exists in destination, it adds a number suffix
- Always run `--dry-run` first to see what will happen
- The script uses the centralized paths system for consistency

