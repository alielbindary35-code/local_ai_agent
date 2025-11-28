"""
Unit tests for ReAct Loop
"""

import pytest
from src.core.react_loop import ReActLoop, TaskState, TaskContext


class TestReActLoop:
    """Test cases for ReActLoop class."""
    
    def test_init(self):
        """Test ReAct loop initialization."""
        loop = ReActLoop(max_iterations=10, max_retries=3)
        assert loop.max_iterations == 10
        assert loop.max_retries == 3
        assert loop.enable_loop_detection is True
    
    def test_parse_reasoning_with_json(self):
        """Test parsing reasoning with JSON."""
        loop = ReActLoop()
        thought = '{"thought": "I need to read a file", "action": "read_file", "action_input": {"filepath": "test.txt"}}'
        
        result = loop._parse_reasoning(thought)
        
        assert result['action'] == 'read_file'
        assert result['action_input']['filepath'] == 'test.txt'
    
    def test_parse_reasoning_without_json(self):
        """Test parsing reasoning without JSON."""
        loop = ReActLoop()
        thought = "I should read the file"
        
        result = loop._parse_reasoning(thought)
        
        assert result['thought'] == thought
        assert result['action'] is None
    
    def test_detect_loop(self):
        """Test loop detection."""
        loop = ReActLoop()
        
        context = TaskContext(
            task_id="test",
            user_input="test",
            state=TaskState.REASONING,
            iteration=1,
            max_iterations=10,
            conversation_history=[],
            last_action="read_file",
            last_action_input={"filepath": "test.txt"}
        )
        
        # Simulate repeated actions
        loop.action_history = [
            ("read_file", "{'filepath': 'test.txt'}"),
            ("read_file", "{'filepath': 'test.txt'}"),
            ("read_file", "{'filepath': 'test.txt'}")
        ]
        
        is_loop = loop._detect_loop(context)
        assert is_loop is True
    
    def test_execute_simple_task(self):
        """Test executing a simple task."""
        loop = ReActLoop(max_iterations=5)
        
        def reasoning_fn(user_input, history):
            return '{"thought": "Task complete", "final_answer": "Done"}'
        
        def action_fn(action, action_input):
            return "result"
        
        def observation_fn(result):
            return str(result)
        
        result = loop.execute(
            user_input="test",
            task_id="test-1",
            reasoning_fn=reasoning_fn,
            action_fn=action_fn,
            observation_fn=observation_fn
        )
        
        assert result['success'] is True
        assert result['final_answer'] == "Done"
    
    def test_reset(self):
        """Test resetting loop state."""
        loop = ReActLoop()
        loop.action_history = [("action1", "input1"), ("action2", "input2")]
        
        loop.reset()
        
        assert len(loop.action_history) == 0
