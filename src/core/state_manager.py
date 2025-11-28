"""
State Manager - Robust task and session state management
========================================================

Manages agent state persistence, task recovery, and session management
for offline operation without internet dependency.
"""

import sqlite3
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from enum import Enum

from src.core.paths import get_data_dir

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class StateManager:
    """
    Manages agent state, tasks, and sessions with SQLite persistence.
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize state manager.
        
        Args:
            db_path: Path to state database (defaults to data/agent_state.db)
        """
        if db_path is None:
            db_path = get_data_dir() / "agent_state.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create database tables for state management."""
        cursor = self.conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                user_input TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                result TEXT,
                error_message TEXT,
                iteration_count INTEGER DEFAULT 0,
                max_iterations INTEGER DEFAULT 10,
                context_data TEXT,
                metadata TEXT
            )
        """)
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                last_activity TEXT NOT NULL,
                task_count INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        # Task history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            )
        """)
        
        # Checkpoints table for task recovery
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                checkpoint_name TEXT NOT NULL,
                state_data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_checkpoints_task ON checkpoints(task_id)")
        
        self.conn.commit()
    
    def create_task(
        self,
        task_id: str,
        user_input: str,
        max_iterations: int = 10,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Create a new task.
        
        Args:
            task_id: Unique task identifier
            user_input: User's request
            max_iterations: Maximum iterations
            metadata: Optional metadata
        
        Returns:
            True if created successfully
        """
        try:
            cursor = self.conn.cursor()
            now = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO tasks (
                    task_id, user_input, status, created_at, updated_at,
                    max_iterations, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task_id,
                user_input,
                TaskStatus.PENDING.value,
                now,
                now,
                max_iterations,
                json.dumps(metadata or {})
            ))
            
            self.conn.commit()
            logger.info(f"Task {task_id} created")
            return True
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return False
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
        context_data: Optional[Dict] = None
    ) -> bool:
        """
        Update task status.
        
        Args:
            task_id: Task identifier
            status: New status
            result: Task result (if completed)
            error_message: Error message (if failed)
            context_data: Context data for recovery
        
        Returns:
            True if updated successfully
        """
        try:
            cursor = self.conn.cursor()
            now = datetime.now().isoformat()
            
            updates = {
                "status": status.value,
                "updated_at": now
            }
            
            if status == TaskStatus.RUNNING and not self.get_task(task_id).get("started_at"):
                updates["started_at"] = now
            
            if status == TaskStatus.COMPLETED:
                updates["completed_at"] = now
                if result:
                    updates["result"] = result
            
            if status == TaskStatus.FAILED and error_message:
                updates["error_message"] = error_message
            
            if context_data:
                updates["context_data"] = json.dumps(context_data)
            
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [task_id]
            
            cursor.execute(f"""
                UPDATE tasks
                SET {set_clause}
                WHERE task_id = ?
            """, values)
            
            self.conn.commit()
            logger.info(f"Task {task_id} status updated to {status.value}")
            return True
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return False
    
    def increment_task_iteration(self, task_id: str) -> bool:
        """Increment task iteration count."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE tasks
                SET iteration_count = iteration_count + 1,
                    updated_at = ?
                WHERE task_id = ?
            """, (datetime.now().isoformat(), task_id))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error incrementing iteration: {e}")
            return False
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task by ID.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Task data or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                task = dict(row)
                # Parse JSON fields
                if task.get("metadata"):
                    task["metadata"] = json.loads(task["metadata"])
                if task.get("context_data"):
                    task["context_data"] = json.loads(task["context_data"])
                return task
            return None
        except Exception as e:
            logger.error(f"Error getting task: {e}")
            return None
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks."""
        return self.get_tasks_by_status(TaskStatus.PENDING)
    
    def get_running_tasks(self) -> List[Dict[str, Any]]:
        """Get all running tasks."""
        return self.get_tasks_by_status(TaskStatus.RUNNING)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Dict[str, Any]]:
        """Get tasks by status."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC", (status.value,))
            rows = cursor.fetchall()
            
            tasks = []
            for row in rows:
                task = dict(row)
                if task.get("metadata"):
                    task["metadata"] = json.loads(task["metadata"])
                if task.get("context_data"):
                    task["context_data"] = json.loads(task["context_data"])
                tasks.append(task)
            
            return tasks
        except Exception as e:
            logger.error(f"Error getting tasks by status: {e}")
            return []
    
    def save_checkpoint(
        self,
        task_id: str,
        checkpoint_name: str,
        state_data: Dict[str, Any]
    ) -> bool:
        """
        Save task checkpoint for recovery.
        
        Args:
            task_id: Task identifier
            checkpoint_name: Checkpoint name
            state_data: State data to save
        
        Returns:
            True if saved successfully
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO checkpoints (task_id, checkpoint_name, state_data, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                task_id,
                checkpoint_name,
                json.dumps(state_data),
                datetime.now().isoformat()
            ))
            self.conn.commit()
            logger.info(f"Checkpoint {checkpoint_name} saved for task {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
            return False
    
    def get_latest_checkpoint(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get latest checkpoint for a task."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM checkpoints
                WHERE task_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (task_id,))
            row = cursor.fetchone()
            
            if row:
                checkpoint = dict(row)
                checkpoint["state_data"] = json.loads(checkpoint["state_data"])
                return checkpoint
            return None
        except Exception as e:
            logger.error(f"Error getting checkpoint: {e}")
            return None
    
    def recover_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Recover task from checkpoint.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Recovered state data or None
        """
        checkpoint = self.get_latest_checkpoint(task_id)
        if checkpoint:
            # Update task status to running
            self.update_task_status(task_id, TaskStatus.RUNNING)
            return checkpoint["state_data"]
        return None
    
    def log_task_action(
        self,
        task_id: str,
        action: str,
        data: Optional[Dict] = None
    ) -> bool:
        """
        Log task action to history.
        
        Args:
            task_id: Task identifier
            action: Action name
            data: Optional action data
        
        Returns:
            True if logged successfully
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO task_history (task_id, action, timestamp, data)
                VALUES (?, ?, ?, ?)
            """, (
                task_id,
                action,
                datetime.now().isoformat(),
                json.dumps(data or {})
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error logging action: {e}")
            return False
    
    def create_session(self, session_id: str, metadata: Optional[Dict] = None) -> bool:
        """Create a new session."""
        try:
            cursor = self.conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO sessions (session_id, started_at, last_activity, status, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session_id,
                now,
                now,
                "active",
                json.dumps(metadata or {})
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return False
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update session last activity timestamp."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE sessions
                SET last_activity = ?, task_count = task_count + 1
                WHERE session_id = ?
            """, (datetime.now().isoformat(), session_id))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.conn.close()
        except:
            pass

