# Agent Learning Examples

This directory contains scripts to teach your AI agent new technologies.

## 🚀 Quick Start

### 1. Interactive Learning (Recommended)
Run this script to teach the agent *any* technology by answering a few questions:
```bash
python examples/learn_any.py
```

### 2. Specific Examples
- **Docker**: `python examples/fast_learn_docker.py`
- **Flutter**: `python examples/learn_flutter.py`

## 📝 How It Works

These scripts use the **Fast Learning Module** (`src/tools/fast_learning.py`) which:
1. Searches the web (DuckDuckGo)
2. Finds official documentation
3. Looks for GitHub examples
4. Saves everything to `data/knowledge_base/[technology]/`

## 🗣️ Prompt Template

When asking the agent directly, use this format for best results:

> "Learn **[Technology]** and focus on **[Topic 1, Topic 2]**."

Example:
> "Learn **Flutter** and focus on **widgets, state management**."
