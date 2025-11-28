"""
Comprehensive Logging System
=============================

Logs events, errors, and actions for troubleshooting and maintenance.
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler

from src.core.paths import get_data_dir


class AgentLogger:
    """
    Comprehensive logging system for the AI agent.
    """
    
    def __init__(
        self,
        log_dir: Optional[Path] = None,
        log_level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """
        Initialize logger.
        
        Args:
            log_dir: Log directory (defaults to data/logs)
            log_level: Logging level
            max_bytes: Max log file size before rotation
            backup_count: Number of backup files to keep
        """
        if log_dir is None:
            log_dir = get_data_dir() / "logs"
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger("ai_agent")
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler with rotation
        log_file = self.log_dir / "agent.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Separate error log
        error_log_file = self.log_dir / "errors.log"
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def log_event(
        self,
        event_type: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        level: str = "INFO"
    ):
        """
        Log an event with structured data.
        
        Args:
            event_type: Type of event (e.g., "tool_execution", "task_started")
            message: Event message
            data: Optional event data
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        log_data = {
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        log_message = f"[{event_type}] {message}"
        if data:
            log_message += f" | Data: {json.dumps(data, default=str)}"
        
        if level.upper() == "DEBUG":
            self.logger.debug(log_message)
        elif level.upper() == "WARNING":
            self.logger.warning(log_message)
        elif level.upper() == "ERROR":
            self.logger.error(log_message)
        else:
            self.logger.info(log_message)
    
    def log_tool_execution(
        self,
        tool_name: str,
        params: Dict[str, Any],
        result: Any,
        execution_time: float,
        success: bool = True
    ):
        """Log tool execution."""
        self.log_event(
            "tool_execution",
            f"Tool: {tool_name} | Success: {success} | Time: {execution_time:.2f}s",
            {
                "tool_name": tool_name,
                "params": params,
                "result_preview": str(result)[:200] if result else None,
                "execution_time": execution_time,
                "success": success
            },
            "INFO" if success else "ERROR"
        )
    
    def log_task_start(self, task_id: str, user_input: str):
        """Log task start."""
        self.log_event(
            "task_started",
            f"Task {task_id} started",
            {"task_id": task_id, "user_input": user_input}
        )
    
    def log_task_complete(self, task_id: str, success: bool, result: Optional[str] = None):
        """Log task completion."""
        self.log_event(
            "task_completed",
            f"Task {task_id} completed | Success: {success}",
            {"task_id": task_id, "success": success, "result_preview": result[:200] if result else None},
            "INFO" if success else "ERROR"
        )
    
    def log_error(
        self,
        error_type: str,
        message: str,
        exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log an error with context."""
        error_data = {
            "error_type": error_type,
            "message": message,
            "context": context or {}
        }
        
        if exception:
            error_data["exception_type"] = type(exception).__name__
            error_data["exception_message"] = str(exception)
            import traceback
            error_data["traceback"] = traceback.format_exc()
        
        self.log_event(
            "error",
            f"{error_type}: {message}",
            error_data,
            "ERROR"
        )
    
    def log_system_event(self, event: str, data: Optional[Dict[str, Any]] = None):
        """Log system-level event."""
        self.log_event("system", event, data)
    
    def get_log_file_path(self) -> Path:
        """Get path to main log file."""
        return self.log_dir / "agent.log"
    
    def get_error_log_path(self) -> Path:
        """Get path to error log file."""
        return self.log_dir / "errors.log"


# Global logger instance
_global_logger: Optional[AgentLogger] = None


def get_logger() -> AgentLogger:
    """Get global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = AgentLogger()
    return _global_logger

