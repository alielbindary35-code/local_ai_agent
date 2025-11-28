"""
Unit tests for State Manager
"""

import pytest
import tempfile
from pathlib import Path
from src.core.state_manager import StateManager, TaskStatus


class TestStateManager:
    """Test cases for StateManager class."""
    
    def test_init(self, tmp_path):
        """Test state manager initialization."""
        db_path = tmp_path / "test_state.db"
        manager = StateManager(db_path=db_path)
        assert manager.db_path == db_path
        assert manager.conn is not None
    
    def test_create_task(self, tmp_path):
        """Test task creation."""
        manager = StateManager(db_path=tmp_path / "test.db")
        task_id = "test_task_1"
        
        result = manager.create_task(task_id, "Test task", max_iterations=5)
        assert result is True
        
        task = manager.get_task(task_id)
        assert task is not None
        assert task["user_input"] == "Test task"
        assert task["status"] == TaskStatus.PENDING.value
    
    def test_update_task_status(self, tmp_path):
        """Test task status update."""
        manager = StateManager(db_path=tmp_path / "test.db")
        task_id = "test_task_2"
        
        manager.create_task(task_id, "Test")
        manager.update_task_status(task_id, TaskStatus.RUNNING)
        
        task = manager.get_task(task_id)
        assert task["status"] == TaskStatus.RUNNING.value
    
    def test_save_checkpoint(self, tmp_path):
        """Test checkpoint saving."""
        manager = StateManager(db_path=tmp_path / "test.db")
        task_id = "test_task_3"
        
        manager.create_task(task_id, "Test")
        result = manager.save_checkpoint(task_id, "checkpoint_1", {"data": "test"})
        
        assert result is True
        checkpoint = manager.get_latest_checkpoint(task_id)
        assert checkpoint is not None
        assert checkpoint["checkpoint_name"] == "checkpoint_1"
    
    def test_get_pending_tasks(self, tmp_path):
        """Test getting pending tasks."""
        manager = StateManager(db_path=tmp_path / "test.db")
        
        manager.create_task("task1", "Task 1")
        manager.create_task("task2", "Task 2")
        manager.update_task_status("task1", TaskStatus.RUNNING)
        
        pending = manager.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0]["task_id"] == "task2"

