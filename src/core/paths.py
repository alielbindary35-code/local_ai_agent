"""
Centralized Path Management System
نظام إدارة المسارات المركزي
==================================

This module provides a centralized way to manage all project paths.
It automatically detects the project root and provides consistent paths
regardless of where the code is executed from (terminal, Colab, Jupyter, etc.)
"""

import os
import sys
from pathlib import Path
from typing import Optional


def _find_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the project root directory by looking for specific markers.
    
    Looks for:
    - .git directory
    - requirements.txt
    - src/ directory
    - config.py
    
    Args:
        start_path: Starting directory to search from (defaults to current file)
    
    Returns:
        Path to project root
    """
    if start_path is None:
        # Start from the directory containing this file
        start_path = Path(__file__).resolve().parent.parent.parent
    
    current = Path(start_path).resolve()
    
    # Markers that indicate project root
    markers = [
        '.git',
        'requirements.txt',
        'config.py',
        'src',
        'data/essential_tools.json'
    ]
    
    # Check current directory and parents
    for path in [current] + list(current.parents):
        # Check if any marker exists
        for marker in markers:
            marker_path = path / marker
            if marker_path.exists():
                return path
    
    # Fallback: assume current directory is project root
    return current


# Cache project root to avoid repeated searches
_project_root: Optional[Path] = None


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root (cached after first call)
    """
    global _project_root
    if _project_root is None:
        _project_root = _find_project_root()
    return _project_root


def get_data_dir() -> Path:
    """Get the data directory path."""
    return get_project_root() / "data"


def get_knowledge_base_dir() -> Path:
    """Get the knowledge base directory path."""
    return get_data_dir() / "knowledge_base"


def get_scripts_dir() -> Path:
    """Get the scripts directory path."""
    return get_project_root() / "scripts"


def get_examples_dir() -> Path:
    """Get the examples directory path."""
    return get_project_root() / "examples"


def get_docs_dir() -> Path:
    """Get the docs directory path."""
    return get_project_root() / "docs"


def get_logs_dir() -> Path:
    """Get the logs directory path."""
    return get_data_dir() / "logs_backup"


def get_notebooks_dir() -> Path:
    """Get the notebooks directory path."""
    return get_project_root() / "notebooks"


def get_tests_dir() -> Path:
    """Get the tests directory path."""
    return get_project_root() / "tests"


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Path to directory
    
    Returns:
        Path object (guaranteed to exist)
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_essential_tools_file() -> Path:
    """Get the essential tools JSON file path."""
    return get_data_dir() / "essential_tools.json"


def get_learning_progress_file() -> Path:
    """Get the learning progress JSON file path."""
    return get_data_dir() / "learning_progress.json"


def get_memory_db_file() -> Path:
    """Get the agent memory database file path."""
    return get_data_dir() / "agent_memory.db"


def add_project_to_path():
    """
    Add project root to sys.path if not already present.
    Useful for imports when running from different directories.
    """
    project_root = get_project_root()
    project_root_str = str(project_root)
    
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)


# Auto-add project root to path when module is imported
add_project_to_path()

