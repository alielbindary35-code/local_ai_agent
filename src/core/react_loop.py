"""
ReAct Loop Module
=================

Modular ReAct (Reasoning + Acting) loop implementation with:
- State machine for task management
- Error recovery and fallback mechanisms
- Task prioritization
- Loop detection and prevention
"""

import json
import logging
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskState(Enum):
    """Task execution states."""
    INITIALIZING = "initializing"
    REASONING = "reasoning"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class TaskContext:
    """Context for a single task execution."""
    task_id: str
    user_input: str
    state: TaskState
    iteration: int
    max_iterations: int
    conversation_history: List[Dict[str, Any]]
    last_action: Optional[str] = None
    last_action_input: Optional[Dict] = None
    error_count: int = 0
    retry_count: int = 0
    start_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()


class ReActLoop:
    """
    Modular ReAct loop with state management and error recovery.
    """
    
    def __init__(
        self,
        max_iterations: int = 10,
        max_retries: int = 3,
        enable_loop_detection: bool = True,
        enable_fallbacks: bool = True
    ):
        """
        Initialize ReAct loop.
        
        Args:
            max_iterations: Maximum iterations per task
            max_retries: Maximum retry attempts for failed actions
            enable_loop_detection: Enable loop detection
            enable_fallbacks: Enable fallback mechanisms
        """
        self.max_iterations = max_iterations
        self.max_retries = max_retries
        self.enable_loop_detection = enable_loop_detection
        self.enable_fallbacks = enable_fallbacks
        self.action_history: List[tuple] = []
    
    def execute(
        self,
        user_input: str,
        task_id: str,
        reasoning_fn: Callable[[str, List[Dict]], str],
        action_fn: Callable[[str, Dict], Any],
        observation_fn: Callable[[Any], str],
        final_answer_fn: Optional[Callable[[str], bool]] = None
    ) -> Dict[str, Any]:
        """
        Execute ReAct loop for a task.
        
        Args:
            user_input: User's request
            task_id: Unique task identifier
            reasoning_fn: Function to generate reasoning/thought
            action_fn: Function to execute actions
            observation_fn: Function to process observations
            final_answer_fn: Function to check if answer is final
        
        Returns:
            Result dictionary with state, answer, and metadata
        """
        context = TaskContext(
            task_id=task_id,
            user_input=user_input,
            state=TaskState.INITIALIZING,
            iteration=0,
            max_iterations=self.max_iterations,
            conversation_history=[]
        )
        
        context.state = TaskState.REASONING
        
        while context.iteration < context.max_iterations:
            context.iteration += 1
            
            try:
                # REASONING phase
                if context.state == TaskState.REASONING:
                    thought = reasoning_fn(user_input, context.conversation_history)
                    
                    # Parse thought to extract action
                    action_data = self._parse_reasoning(thought)
                    
                    if action_data.get('final_answer'):
                        context.state = TaskState.COMPLETED
                        return {
                            'success': True,
                            'state': context.state.value,
                            'final_answer': action_data['final_answer'],
                            'iterations': context.iteration,
                            'context': context
                        }
                    
                    if action_data.get('action'):
                        context.state = TaskState.ACTING
                        context.last_action = action_data['action']
                        context.last_action_input = action_data.get('action_input', {})
                
                # ACTING phase
                elif context.state == TaskState.ACTING:
                    # Check for loops
                    if self.enable_loop_detection:
                        if self._detect_loop(context):
                            logger.warning(f"Loop detected in task {task_id}")
                            context.conversation_history.append({
                                'role': 'system',
                                'content': 'Loop detected. Try a different approach or provide final answer.'
                            })
                            context.state = TaskState.REASONING
                            continue
                    
                    # Execute action
                    try:
                        result = action_fn(context.last_action, context.last_action_input)
                        context.state = TaskState.OBSERVING
                    except Exception as e:
                        logger.error(f"Action execution error: {e}")
                        context.error_count += 1
                        
                        if context.error_count > self.max_retries:
                            context.state = TaskState.FAILED
                            return {
                                'success': False,
                                'state': context.state.value,
                                'error': f'Max errors exceeded: {str(e)}',
                                'iterations': context.iteration,
                                'context': context
                            }
                        
                        # Retry with fallback
                        if self.enable_fallbacks:
                            context.state = TaskState.RETRYING
                            context.retry_count += 1
                            context.conversation_history.append({
                                'role': 'system',
                                'content': f'Action failed: {str(e)}. Try alternative approach.'
                            })
                            context.state = TaskState.REASONING
                            continue
                        else:
                            context.state = TaskState.FAILED
                            return {
                                'success': False,
                                'state': context.state.value,
                                'error': str(e),
                                'iterations': context.iteration,
                                'context': context
                            }
                
                # OBSERVING phase
                elif context.state == TaskState.OBSERVING:
                    observation = observation_fn(result)
                    
                    # Add to conversation history
                    context.conversation_history.append({
                        'role': 'assistant',
                        'content': thought if 'thought' in locals() else ''
                    })
                    context.conversation_history.append({
                        'role': 'user',
                        'content': f"Action '{context.last_action}' result: {observation}"
                    })
                    
                    # Check if we have a final answer
                    if final_answer_fn and final_answer_fn(observation):
                        context.state = TaskState.COMPLETED
                        return {
                            'success': True,
                            'state': context.state.value,
                            'final_answer': observation,
                            'iterations': context.iteration,
                            'context': context
                        }
                    
                    # Continue reasoning
                    context.state = TaskState.REASONING
                
                # RETRYING phase
                elif context.state == TaskState.RETRYING:
                    if context.retry_count > self.max_retries:
                        context.state = TaskState.FAILED
                        return {
                            'success': False,
                            'state': context.state.value,
                            'error': 'Max retries exceeded',
                            'iterations': context.iteration,
                            'context': context
                        }
                    context.state = TaskState.REASONING
            
            except Exception as e:
                logger.error(f"Error in ReAct loop iteration {context.iteration}: {e}")
                context.error_count += 1
                
                if context.error_count > self.max_retries:
                    context.state = TaskState.FAILED
                    return {
                        'success': False,
                        'state': context.state.value,
                        'error': f'Critical error: {str(e)}',
                        'iterations': context.iteration,
                        'context': context
                    }
                
                # Retry
                context.state = TaskState.REASONING
                context.conversation_history.append({
                    'role': 'system',
                    'content': f'Error occurred: {str(e)}. Retrying...'
                })
        
        # Max iterations reached
        context.state = TaskState.FAILED
        return {
            'success': False,
            'state': context.state.value,
            'error': 'Maximum iterations reached',
            'iterations': context.iteration,
            'context': context
        }
    
    def _parse_reasoning(self, thought: str) -> Dict[str, Any]:
        """
        Parse reasoning output to extract action information.
        
        Args:
            thought: Reasoning/thought text (may contain JSON)
        
        Returns:
            Dictionary with action, action_input, and final_answer
        """
        try:
            # Try to extract JSON
            if '{' in thought and '}' in thought:
                json_start = thought.index('{')
                json_end = thought.rindex('}') + 1
                json_str = thought[json_start:json_end]
                data = json.loads(json_str)
                
                return {
                    'thought': data.get('thought', thought),
                    'action': data.get('action'),
                    'action_input': data.get('action_input', {}),
                    'final_answer': data.get('final_answer')
                }
        except Exception:
            pass
        
        # No JSON found, return thought only
        return {
            'thought': thought,
            'action': None,
            'action_input': {},
            'final_answer': None
        }
    
    def _detect_loop(self, context: TaskContext) -> bool:
        """
        Detect if agent is stuck in a loop.
        
        Args:
            context: Current task context
        
        Returns:
            True if loop detected
        """
        if not context.last_action or not context.last_action_input:
            return False
        
        # Check last 3 actions
        recent_actions = [
            (context.last_action, str(context.last_action_input))
        ]
        
        # Add to history
        self.action_history.append((context.last_action, str(context.last_action_input)))
        
        # Keep only last 5 actions
        if len(self.action_history) > 5:
            self.action_history = self.action_history[-5:]
        
        # Check for repetition
        if len(self.action_history) >= 3:
            last_three = self.action_history[-3:]
            if len(set(last_three)) == 1:
                return True
        
        return False
    
    def reset(self):
        """Reset loop state."""
        self.action_history = []

