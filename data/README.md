# Data Directory

This directory contains all data files, databases, and knowledge base content.

## Structure

```
data/
├── agent_memory.db          # SQLite database for agent memory
├── essential_tools.json     # Essential tools configuration
├── learning_progress.json   # Learning progress tracking
├── knowledge_base/          # Knowledge base files (markdown)
└── logs_backup/            # Backup log files
```

## Files

### `agent_memory.db`
SQLite database storing:
- Solutions and problem-solving history
- Custom tools
- Package registry
- User preferences
- Error patterns

### `essential_tools.json`
Configuration file defining essential tools for the agent.

### `learning_progress.json`
Tracks learning progress for different technologies and topics.

### `knowledge_base/`
Markdown files containing knowledge about various technologies:
- Programming languages
- Frameworks
- Tools and utilities
- Best practices

Each technology has its own directory with documentation files.

## Backup

Important: This directory contains persistent data. Regular backups are recommended.

## Access

Use the path management system to access these files:

```python
from src.core.paths import get_data_dir, get_memory_db_file

data_dir = get_data_dir()
memory_db = get_memory_db_file()
```

