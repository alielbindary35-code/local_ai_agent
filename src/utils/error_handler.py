"""
Error Handler and Recovery System
=================================

Comprehensive error detection, handling, and recovery mechanisms.
"""

import logging
import traceback
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from enum import Enum

from src.utils.logger import get_logger

logger = get_logger().logger


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    TOOL_EXECUTION = "tool_execution"
    MODEL_ERROR = "model_error"
    SYSTEM_ERROR = "system_error"
    NETWORK_ERROR = "network_error"
    DATA_ERROR = "data_error"
    PERMISSION_ERROR = "permission_error"
    UNKNOWN = "unknown"


class ErrorHandler:
    """
    Comprehensive error handling and recovery system.
    """
    
    def __init__(self):
        """Initialize error handler."""
        self.error_history: List[Dict[str, Any]] = []
        self.recovery_strategies: Dict[str, Callable] = {}
        self.max_history = 100
    
    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        auto_recover: bool = True
    ) -> Dict[str, Any]:
        """
        Handle an error with context and recovery.
        
        Args:
            error: Exception that occurred
            context: Error context
            category: Error category
            severity: Error severity
            auto_recover: Attempt automatic recovery
        
        Returns:
            Error handling result
        """
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "severity": severity.value,
            "category": category.value,
            "context": context or {}
        }
        
        # Log error
        logger.error(f"[{category.value}] {error_info['error_message']}", exc_info=error)
        
        # Add to history
        self.error_history.append(error_info)
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)
        
        # Attempt recovery
        recovery_result = None
        if auto_recover:
            recovery_result = self.attempt_recovery(error, category, context)
            error_info["recovery_attempted"] = True
            error_info["recovery_result"] = recovery_result
        
        error_info["handled"] = True
        return error_info
    
    def attempt_recovery(
        self,
        error: Exception,
        category: ErrorCategory,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Attempt automatic error recovery.
        
        Args:
            error: Exception that occurred
            category: Error category
            context: Error context
        
        Returns:
            Recovery result
        """
        recovery_strategy = self.recovery_strategies.get(category.value)
        
        if recovery_strategy:
            try:
                result = recovery_strategy(error, context)
                logger.info(f"Recovery attempted for {category.value}: {result.get('success', False)}")
                return result
            except Exception as e:
                logger.error(f"Recovery strategy failed: {e}")
                return {"success": False, "error": str(e)}
        
        # Default recovery strategies
        if category == ErrorCategory.TOOL_EXECUTION:
            return self._recover_tool_error(error, context)
        elif category == ErrorCategory.MODEL_ERROR:
            return self._recover_model_error(error, context)
        elif category == ErrorCategory.NETWORK_ERROR:
            return self._recover_network_error(error, context)
        
        return {"success": False, "message": "No recovery strategy available"}
    
    def _recover_tool_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Recover from tool execution error."""
        tool_name = context.get("tool_name") if context else None
        
        if "not found" in str(error).lower():
            return {
                "success": False,
                "message": f"Tool '{tool_name}' not found. Check available tools.",
                "suggestion": "Verify tool name and parameters"
            }
        elif "permission" in str(error).lower() or "access" in str(error).lower():
            return {
                "success": False,
                "message": "Permission denied",
                "suggestion": "Check file/directory permissions or run with appropriate privileges"
            }
        elif "timeout" in str(error).lower():
            return {
                "success": False,
                "message": "Operation timed out",
                "suggestion": "Retry with longer timeout or check system resources"
            }
        
        return {
            "success": False,
            "message": "Tool error recovery not available",
            "suggestion": "Check error message and retry"
        }
    
    def _recover_model_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Recover from model error."""
        if "connection" in str(error).lower():
            return {
                "success": False,
                "message": "Cannot connect to model",
                "suggestion": "Check if Ollama is running: ollama serve"
            }
        elif "not found" in str(error).lower():
            return {
                "success": False,
                "message": "Model not found",
                "suggestion": "Pull the model: ollama pull <model_name>"
            }
        elif "timeout" in str(error).lower():
            return {
                "success": False,
                "message": "Model request timed out",
                "suggestion": "Try a smaller model or increase timeout"
            }
        
        return {
            "success": False,
            "message": "Model error recovery not available"
        }
    
    def _recover_network_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Recover from network error."""
        return {
            "success": True,
            "message": "Switching to offline mode",
            "action": "use_local_knowledge_base"
        }
    
    def register_recovery_strategy(
        self,
        category: ErrorCategory,
        strategy: Callable[[Exception, Optional[Dict]], Dict[str, Any]]
    ):
        """
        Register custom recovery strategy.
        
        Args:
            category: Error category
            strategy: Recovery function
        """
        self.recovery_strategies[category.value] = strategy
        logger.info(f"Recovery strategy registered for {category.value}")
    
    def get_error_patterns(self) -> Dict[str, int]:
        """
        Analyze error history for patterns.
        
        Returns:
            Dictionary of error patterns and frequencies
        """
        patterns = {}
        for error in self.error_history:
            error_type = error["error_type"]
            patterns[error_type] = patterns.get(error_type, 0) + 1
        
        return patterns
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors."""
        return self.error_history[-limit:]
    
    def clear_history(self):
        """Clear error history."""
        self.error_history.clear()
        logger.info("Error history cleared")


# Global error handler instance
_global_error_handler: Optional[ErrorHandler] = None


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler

