"""
Unit tests for Error Handler
"""

import pytest
from src.utils.error_handler import (
    ErrorHandler,
    ErrorCategory,
    ErrorSeverity
)


class TestErrorHandler:
    """Test cases for ErrorHandler class."""
    
    def test_init(self):
        """Test error handler initialization."""
        handler = ErrorHandler()
        assert handler.error_history == []
        assert handler.recovery_strategies == {}
    
    def test_handle_error(self):
        """Test error handling."""
        handler = ErrorHandler()
        error = ValueError("Test error")
        
        result = handler.handle_error(
            error,
            context={"test": "data"},
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.TOOL_EXECUTION
        )
        
        assert result["handled"] is True
        assert result["error_type"] == "ValueError"
        assert result["category"] == ErrorCategory.TOOL_EXECUTION.value
        assert len(handler.error_history) == 1
    
    def test_get_error_patterns(self):
        """Test error pattern analysis."""
        handler = ErrorHandler()
        
        handler.handle_error(ValueError("Error 1"), category=ErrorCategory.TOOL_EXECUTION)
        handler.handle_error(ValueError("Error 2"), category=ErrorCategory.TOOL_EXECUTION)
        handler.handle_error(KeyError("Error 3"), category=ErrorCategory.DATA_ERROR)
        
        patterns = handler.get_error_patterns()
        assert patterns["ValueError"] == 2
        assert patterns["KeyError"] == 1
    
    def test_recovery_strategy(self):
        """Test recovery strategy registration."""
        handler = ErrorHandler()
        
        def custom_strategy(error, context):
            return {"success": True, "message": "Recovered"}
        
        handler.register_recovery_strategy(ErrorCategory.TOOL_EXECUTION, custom_strategy)
        assert ErrorCategory.TOOL_EXECUTION.value in handler.recovery_strategies

