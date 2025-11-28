# Source Code (`src/`)

This directory contains the core source code for the AI agent system.

## Structure

```
src/
├── agents/          # Agent implementations (simple, standard, expert)
├── core/            # Core functionality (memory, prompts, training)
├── tools/           # Tool libraries (basic, expert, extended)
└── utils/           # Utility modules (cache, connection checking)
```

## Modules

### `agents/`
Contains different agent implementations:
- **`agent.py`**: Standard agent with ReAct loop
- **`expert_agent.py`**: Expert-level agent with advanced features
- **`simple_agent.py`**: Lightweight agent for simple tasks

### `core/`
Core system components:
- **`memory.py`**: SQLite-based memory and learning system
- **`prompts.py`**: Prompt templates and formatters
- **`paths.py`**: Centralized path management
- **`trainer.py`**: Agent training system
- **`automated_trainer.py`**: Automated training workflows

### `tools/`
Tool libraries for agent capabilities:
- **`tools.py`**: Basic tool set (file ops, commands, web)
- **`expert_tools.py`**: Advanced tools (Docker, n8n, databases)
- **`extended_tools.py`**: Extended tool collection
- **`auto_learner.py`**: Automated learning capabilities

### `utils/`
Utility modules:
- **`cache_manager.py`**: Caching system for API responses
- **`connection_checker.py`**: Network connectivity checking

## Usage

Import agents and tools:

```python
from src.agents.agent import Agent
from src.tools.tools import Tools
from src.core.memory import Memory
```

## Development Guidelines

- Follow consistent naming: `camelCase` for functions, `snake_case` for variables
- Add error handling to all critical operations
- Include docstrings for all public functions
- Write unit tests for new features

