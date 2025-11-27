"""
Project Configuration
إعدادات المشروع
==================

Centralized configuration file for project paths and settings.
"""

from pathlib import Path
from src.core.paths import (
    get_project_root,
    get_data_dir,
    get_knowledge_base_dir,
    get_scripts_dir,
    get_examples_dir,
    get_docs_dir,
    get_logs_dir,
    get_notebooks_dir,
    get_essential_tools_file,
    get_learning_progress_file,
    get_memory_db_file
)

# Project root directory
PROJECT_ROOT = get_project_root()

# Directory paths
DATA_DIR = get_data_dir()
KNOWLEDGE_BASE_DIR = get_knowledge_base_dir()
SCRIPTS_DIR = get_scripts_dir()
EXAMPLES_DIR = get_examples_dir()
DOCS_DIR = get_docs_dir()
LOGS_DIR = get_logs_dir()
NOTEBOOKS_DIR = get_notebooks_dir()

# File paths
ESSENTIAL_TOOLS_FILE = get_essential_tools_file()
LEARNING_PROGRESS_FILE = get_learning_progress_file()
MEMORY_DB_FILE = get_memory_db_file()

# Project metadata
PROJECT_NAME = "local_ai_agent"
VERSION = "1.0.0"

