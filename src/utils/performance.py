"""
Performance Optimization Module
================================

Performance optimizations for the AI agent:
- Task prioritization
- Dynamic module loading
- Resource monitoring
- Task queue management
"""

import psutil
import logging
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import threading
from queue import Queue, PriorityQueue

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class Task:
    """Task representation for queue."""
    task_id: str
    user_input: str
    priority: TaskPriority
    created_at: datetime
    estimated_duration: Optional[float] = None
    required_resources: Optional[Dict[str, Any]] = None
    
    def __lt__(self, other):
        """Compare tasks by priority (for PriorityQueue)."""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        return self.created_at < other.created_at


class ResourceMonitor:
    """
    Monitor system resources (CPU, memory, disk).
    """
    
    def __init__(self, check_interval: float = 1.0):
        """
        Initialize resource monitor.
        
        Args:
            check_interval: Interval between checks (seconds)
        """
        self.check_interval = check_interval
        self.monitoring = False
        self.monitor_thread = None
    
    def get_current_resources(self) -> Dict[str, Any]:
        """
        Get current system resource usage.
        
        Returns:
            Dictionary with CPU, memory, and disk usage
        """
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'cpu_count': psutil.cpu_count(),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'disk_percent': psutil.disk_usage('/').percent,
                'disk_free_gb': round(psutil.disk_usage('/').free / (1024**3), 2)
            }
        except Exception as e:
            logger.error(f"Error getting resources: {e}")
            return {}
    
    def is_resource_available(self, required: Dict[str, Any]) -> bool:
        """
        Check if required resources are available.
        
        Args:
            required: Required resources (e.g., {'memory_gb': 2, 'cpu_percent': 50})
        
        Returns:
            True if resources are available
        """
        current = self.get_current_resources()
        
        if 'memory_gb' in required:
            if current.get('memory_available_gb', 0) < required['memory_gb']:
                return False
        
        if 'cpu_percent' in required:
            if current.get('cpu_percent', 100) > (100 - required['cpu_percent']):
                return False
        
        return True
    
    def start_monitoring(self, callback: Optional[Callable[[Dict], None]] = None):
        """
        Start continuous resource monitoring.
        
        Args:
            callback: Optional callback function for resource updates
        """
        if self.monitoring:
            return
        
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                resources = self.get_current_resources()
                if callback:
                    callback(resources)
                threading.Event().wait(self.check_interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)


class TaskQueue:
    """
    Priority-based task queue with resource awareness.
    """
    
    def __init__(self, resource_monitor: Optional[ResourceMonitor] = None):
        """
        Initialize task queue.
        
        Args:
            resource_monitor: Resource monitor instance
        """
        self.queue = PriorityQueue()
        self.resource_monitor = resource_monitor or ResourceMonitor()
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
    
    def add_task(
        self,
        task_id: str,
        user_input: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        estimated_duration: Optional[float] = None,
        required_resources: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add task to queue.
        
        Args:
            task_id: Unique task identifier
            user_input: User's request
            priority: Task priority
            estimated_duration: Estimated duration in seconds
            required_resources: Required resources
        
        Returns:
            True if task added successfully
        """
        # Check if resources are available
        if required_resources:
            if not self.resource_monitor.is_resource_available(required_resources):
                logger.warning(f"Resources not available for task {task_id}")
                return False
        
        task = Task(
            task_id=task_id,
            user_input=user_input,
            priority=priority,
            created_at=datetime.now(),
            estimated_duration=estimated_duration,
            required_resources=required_resources
        )
        
        self.queue.put(task)
        logger.info(f"Task {task_id} added to queue with priority {priority.name}")
        return True
    
    def get_next_task(self, wait: bool = True) -> Optional[Task]:
        """
        Get next task from queue.
        
        Args:
            wait: Whether to wait if queue is empty
        
        Returns:
            Next task or None
        """
        try:
            if wait:
                task = self.queue.get(timeout=1.0)
            else:
                task = self.queue.get_nowait()
            
            self.active_tasks[task.task_id] = task
            return task
        except:
            return None
    
    def complete_task(self, task_id: str):
        """
        Mark task as completed.
        
        Args:
            task_id: Task identifier
        """
        if task_id in self.active_tasks:
            task = self.active_tasks.pop(task_id)
            self.completed_tasks.append(task)
            logger.info(f"Task {task_id} completed")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """
        Get queue status.
        
        Returns:
            Dictionary with queue statistics
        """
        return {
            'queue_size': self.queue.qsize(),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'resources': self.resource_monitor.get_current_resources()
        }


class ModuleLoader:
    """
    Dynamic module loading for performance optimization.
    """
    
    def __init__(self):
        """Initialize module loader."""
        self.loaded_modules: Dict[str, Any] = {}
        self.module_dependencies: Dict[str, List[str]] = {}
    
    def load_module(self, module_name: str, force_reload: bool = False) -> bool:
        """
        Dynamically load a module.
        
        Args:
            module_name: Name of module to load
            force_reload: Force reload even if already loaded
        
        Returns:
            True if module loaded successfully
        """
        if module_name in self.loaded_modules and not force_reload:
            return True
        
        try:
            # Import module dynamically
            module = __import__(module_name, fromlist=[''])
            self.loaded_modules[module_name] = module
            logger.info(f"Module {module_name} loaded")
            return True
        except ImportError as e:
            logger.error(f"Error loading module {module_name}: {e}")
            return False
    
    def unload_module(self, module_name: str):
        """
        Unload a module to free memory.
        
        Args:
            module_name: Name of module to unload
        """
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]
            logger.info(f"Module {module_name} unloaded")
    
    def get_loaded_modules(self) -> List[str]:
        """Get list of loaded modules."""
        return list(self.loaded_modules.keys())


def estimate_task_complexity(user_input: str) -> Dict[str, Any]:
    """
    Estimate task complexity and required resources.
    
    Args:
        user_input: User's request
    
    Returns:
        Dictionary with complexity estimate and resource requirements
    """
    complexity_keywords = {
        'simple': ['check', 'list', 'show', 'get', 'read', 'find'],
        'medium': ['analyze', 'process', 'create', 'generate', 'update'],
        'complex': ['design', 'optimize', 'architect', 'refactor', 'migrate']
    }
    
    user_lower = user_input.lower()
    complexity = 'medium'  # Default
    
    for level, keywords in complexity_keywords.items():
        if any(keyword in user_lower for keyword in keywords):
            complexity = level
            break
    
    # Estimate resources based on complexity
    resource_estimates = {
        'simple': {'memory_gb': 0.5, 'cpu_percent': 10},
        'medium': {'memory_gb': 1.0, 'cpu_percent': 25},
        'complex': {'memory_gb': 2.0, 'cpu_percent': 50}
    }
    
    return {
        'complexity': complexity,
        'estimated_duration': {'simple': 5, 'medium': 30, 'complex': 120}[complexity],
        'required_resources': resource_estimates.get(complexity, {})
    }

