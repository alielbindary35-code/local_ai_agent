"""
Agent Bridge - Connects GUI with existing agents
جسر الوكيل - يربط واجهة المستخدم مع الوكلاء الموجودة
"""

from PyQt6.QtCore import QObject, pyqtSignal, QThread
from typing import Optional
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.simple_agent import SimpleAgent
from src.agents.expert_agent import ExpertAgent


class AgentWorker(QThread):
    """Worker thread for agent execution"""
    
    response_ready = pyqtSignal(str)
    response_chunk = pyqtSignal(str)  # For streaming
    error_occurred = pyqtSignal(str)
    thinking = pyqtSignal(str)
    
    def __init__(self, agent_mode: str, user_input: str, enable_streaming: bool = False):
        super().__init__()
        self.agent_mode = agent_mode  # Store mode instead of agent
        self.user_input = user_input
        self.enable_streaming = enable_streaming
        self.agent = None  # Will be created in run() method
    
    def run(self):
        """Run agent in background thread"""
        from io import StringIO
        from rich.console import Console
        
        try:
            # Create agent in this thread to avoid SQLite threading issues
            self.thinking.emit("Initializing agent...")
            
            # Redirect rich console output to StringIO to prevent terminal printing
            # We need to patch the console in the agent modules
            silent_console = Console(file=StringIO(), force_terminal=False)
            
            # Temporarily replace console in agent modules
            import src.agents.simple_agent as simple_agent_module
            import src.agents.expert_agent as expert_agent_module
            
            old_simple_console = getattr(simple_agent_module, 'console', None)
            old_expert_console = getattr(expert_agent_module, 'console', None)
            
            # Set silent console
            if self.agent_mode == "simple":
                simple_agent_module.console = silent_console
                self.agent = SimpleAgent()
            else:
                expert_agent_module.console = silent_console
                self.agent = ExpertAgent()
            
            self.thinking.emit("Processing your request...")
            
            try:
                if self.enable_streaming:
                    # For streaming, we'll collect chunks
                    response = self.agent.run(self.user_input)
                    # Simulate streaming by sending chunks
                    words = response.split()
                    for i, word in enumerate(words):
                        chunk = word + " "
                        self.response_chunk.emit(chunk)
                        self.msleep(50)  # Small delay for streaming effect
                    self.response_ready.emit(response)
                else:
                    response = self.agent.run(self.user_input)
                    self.response_ready.emit(response)
            finally:
                # Restore original console
                if old_simple_console:
                    simple_agent_module.console = old_simple_console
                if old_expert_console:
                    expert_agent_module.console = old_expert_console
                
        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n\n{traceback.format_exc()}"
            self.error_occurred.emit(error_msg)
        finally:
            # Clean up agent
            self.agent = None


class AgentBridge(QObject):
    """Bridge between GUI and agent system"""
    
    response_received = pyqtSignal(str)
    response_chunk = pyqtSignal(str)  # For streaming
    error_occurred = pyqtSignal(str)
    thinking = pyqtSignal(str)
    
    def __init__(self, parent=None, enable_streaming: bool = True):
        super().__init__(parent)
        self.agent_mode = "simple"  # 'simple' or 'expert'
        self.worker = None
        self.enable_streaming = enable_streaming
        # Don't create agent here - will be created in worker thread
    
    def set_agent_mode(self, mode: str):
        """Set agent mode (simple or expert)"""
        self.agent_mode = mode
    
    def send_message(self, user_input: str):
        """Send message to agent"""
        if not user_input.strip():
            return
        
        # Stop any existing worker
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        # Create and start new worker (agent will be created in worker thread)
        self.worker = AgentWorker(self.agent_mode, user_input, self.enable_streaming)
        self.worker.response_ready.connect(self.response_received.emit)
        self.worker.response_chunk.connect(self.response_chunk.emit)
        self.worker.error_occurred.connect(self.error_occurred.emit)
        self.worker.thinking.connect(self.thinking.emit)
        self.worker.start()
    
    def stop_current_request(self):
        """Stop current agent request"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self.error_occurred.emit("Request cancelled by user")

