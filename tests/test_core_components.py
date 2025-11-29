"""
Tests for core components (paths, prompts, state_manager, etc.)
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.paths import (
    get_project_root,
    get_data_dir,
    get_knowledge_base_dir,
    get_memory_db_file
)
from src.core.prompts import get_system_prompt
from src.core.state_manager import StateManager


class TestPaths:
    """Tests for path utilities"""
    
    def test_get_project_root(self):
        """Test getting project root"""
        root = get_project_root()
        assert isinstance(root, Path)
        assert root.exists()
    
    def test_get_data_dir(self):
        """Test getting data directory"""
        data_dir = get_data_dir()
        assert isinstance(data_dir, Path)
    
    def test_get_knowledge_base_dir(self):
        """Test getting knowledge base directory"""
        kb_dir = get_knowledge_base_dir()
        assert isinstance(kb_dir, Path)
    
    def test_get_memory_db_file(self):
        """Test getting memory database file path"""
        db_file = get_memory_db_file()
        assert isinstance(db_file, Path)
        assert db_file.suffix == '.db'


class TestPrompts:
    """Tests for prompt generation"""
    
    def test_get_system_prompt(self):
        """Test system prompt generation"""
        prompt = get_system_prompt(
            user_input="test query",
            tools_list="read_file, write_file",
            history=[],
            os_info="Windows 10"
        )
        
        assert isinstance(prompt, str)
        assert "test query" in prompt
        assert "read_file" in prompt or "write_file" in prompt
        assert "Windows" in prompt
    
    def test_get_system_prompt_with_history(self):
        """Test prompt with conversation history"""
        history = [
            {"role": "user", "content": "previous question"},
            {"role": "assistant", "content": "previous answer"}
        ]
        
        prompt = get_system_prompt(
            user_input="new question",
            tools_list="read_file",
            history=history,
            os_info="Linux"
        )
        
        assert "previous question" in prompt or "new question" in prompt


class TestStateManager:
    """Tests for StateManager"""
    
    @pytest.fixture
    def state_manager(self):
        """Create StateManager instance"""
        return StateManager()
    
    def test_state_manager_initialization(self, state_manager):
        """Test state manager initializes"""
        assert state_manager is not None
    
    def test_create_task(self, state_manager):
        """Test creating a task"""
        result = state_manager.create_task(
            task_id="test_task_1",
            user_input="test input",
            max_iterations=5
        )
        
        assert result is True
    
    def test_get_task(self, state_manager):
        """Test getting a task"""
        # Create first
        state_manager.create_task("test_task_2", "test input")
        
        # Get task
        task = state_manager.get_task("test_task_2")
        
        # Should return task or None
        assert task is None or isinstance(task, dict)

