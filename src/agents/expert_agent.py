"""
Expert AI Agent - وكيل ذكاء اصطناعي خبير
Advanced agent with:
- Multi-model orchestration (auto-selects best model)
- 100+ specialized tools
- Online learning capability
- Offline knowledge storage
"""

import json
import requests
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from src.tools.tools import Tools
from src.tools.expert_tools import ExpertTools
from src.tools.extended_tools import ExtendedTools
from src.core.memory import Memory
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class ExpertAgent:
    """
    Expert-Level AI Agent with advanced capabilities
    وكيل ذكاء اصطناعي خبير مع قدرات متقدمة
    """
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        max_iterations: int = 8,
        auto_approve: bool = False,
        enable_online_learning: bool = True
    ):
        self.ollama_url = ollama_url
        self.max_iterations = max_iterations
        self.auto_approve = auto_approve
        self.enable_online_learning = enable_online_learning
        
        # Initialize components
        self.tools = Tools()
        self.expert_tools = ExpertTools()
        self.extended_tools = ExtendedTools()
        self.memory = Memory()
        self.conversation_history = []
        
        # Get available models
        self.available_models = self._get_available_models()
        self.model_capabilities = self._analyze_model_capabilities()
        
        # Display initialization
        self._display_initialization()
    
    def _get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models with their specs"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [{
                    'name': m['name'],
                    'size': m.get('size', 0),
                    'modified': m.get('modified_at', '')
                } for m in models]
            return []
        except Exception as e:
            console.print(f"[yellow]Warning: Could not fetch models: {e}[/yellow]")
            return []
    
    def _analyze_model_capabilities(self) -> Dict[str, Dict]:
        """
        Analyze capabilities of each model
        تحليل قدرات كل موديل
        """
        capabilities = {}
        
        for model in self.available_models:
            name = model['name']
            size = model.get('size', 0)
            
            # Determine capabilities based on model name and size
            caps = {
                'speed': 'fast',
                'accuracy': 'medium',
                'specialization': 'general',
                'best_for': []
            }
            
            # DeepSeek models - best for coding
            if 'deepseek' in name.lower():
                caps['specialization'] = 'coding'
                caps['accuracy'] = 'high'
                caps['best_for'] = ['programming', 'debugging', 'code_review', 'architecture']
            
            # Qwen models - balanced, good for reasoning
            elif 'qwen' in name.lower():
                if '0.5b' in name:
                    caps['speed'] = 'very_fast'
                    caps['accuracy'] = 'low'
                    caps['best_for'] = ['simple_queries', 'quick_answers']
                elif '3b' in name:
                    caps['speed'] = 'fast'
                    caps['accuracy'] = 'medium'
                    caps['best_for'] = ['general_tasks', 'file_operations', 'system_info']
                else:
                    caps['accuracy'] = 'high'
                    caps['best_for'] = ['complex_reasoning', 'analysis', 'planning']
            
            # Llama models - good for general tasks
            elif 'llama' in name.lower():
                caps['specialization'] = 'general'
                caps['accuracy'] = 'high'
                caps['best_for'] = ['conversation', 'general_tasks', 'reasoning']
            
            # Mistral - balanced performance
            elif 'mistral' in name.lower():
                caps['specialization'] = 'general'
                caps['accuracy'] = 'high'
                caps['best_for'] = ['general_tasks', 'reasoning', 'analysis']
            
            capabilities[name] = caps
        
        return capabilities
    
    def _select_best_model(self, task_description: str, task_type: str = None) -> str:
        """
        Intelligently select the best model for the task
        اختيار أفضل موديل للمهمة بذكاء
        
        Args:
            task_description: Description of the task
            task_type: Type of task (coding, web_design, server, docker, database, etc.)
        
        Returns:
            Best model name
        """
        if not self.available_models:
            return "qwen2.5:3b"  # Fallback
        
        # Auto-detect task type if not provided
        if not task_type:
            task_type = self._detect_task_type(task_description)
        
        console.print(f"[dim]🎯 Detected task type: {task_type}[/dim]")
        
        # Scoring system for model selection
        scores = {}
        
        for model in self.available_models:
            name = model['name']
            caps = self.model_capabilities.get(name, {})
            score = 0
            
            # Task-specific scoring
            if task_type == 'coding' or task_type == 'programming':
                if 'deepseek' in name.lower():
                    score += 100  # DeepSeek is best for coding
                elif 'qwen' in name.lower() and '3b' not in name:
                    score += 50
            
            elif task_type == 'web_design':
                if 'deepseek' in name.lower():
                    score += 80
                elif 'qwen' in name.lower():
                    score += 60
            
            elif task_type in ['server', 'docker', 'database', 'devops']:
                if 'deepseek' in name.lower():
                    score += 90
                elif 'llama' in name.lower():
                    score += 70
                elif 'mistral' in name.lower():
                    score += 75
            
            elif task_type == 'simple':
                if '0.5b' in name or '3b' in name:
                    score += 100  # Small models for simple tasks
            
            else:  # general tasks
                if 'mistral' in name.lower():
                    score += 80
                elif 'llama' in name.lower():
                    score += 75
                elif 'qwen' in name.lower() and '3b' not in name:
                    score += 70
            
            # Size bonus (prefer larger models for complex tasks)
            size = model.get('size', 0)
            if task_type in ['coding', 'web_design', 'server', 'docker', 'database']:
                if size > 4_000_000_000:  # > 4GB
                    score += 30
                elif size > 2_000_000_000:  # > 2GB
                    score += 15
            
            scores[name] = score
        
        # Select model with highest score
        best_model = max(scores, key=scores.get)
        best_score = scores[best_model]
        
        console.print(f"[cyan]🤖 Selected model:[/cyan] [bold]{best_model}[/bold] (score: {best_score})")
        console.print(f"[dim]Reason: {self.model_capabilities.get(best_model, {}).get('specialization', 'general')} specialist[/dim]")
        
        return best_model
    
    def _detect_task_type(self, task_description: str) -> str:
        """
        Detect task type from description
        كشف نوع المهمة من الوصف
        """
        task_lower = task_description.lower()
        
        # Coding keywords
        if any(word in task_lower for word in ['code', 'program', 'function', 'class', 'debug', 'python', 'javascript', 'java', 'c++', 'algorithm']):
            return 'coding'
        
        # Web design keywords
        if any(word in task_lower for word in ['website', 'web', 'html', 'css', 'frontend', 'backend', 'ui', 'ux', 'design']):
            return 'web_design'
        
        # Server/DevOps keywords
        if any(word in task_lower for word in ['server', 'deploy', 'nginx', 'apache', 'linux', 'ubuntu', 'centos']):
            return 'server'
        
        # Docker keywords
        if any(word in task_lower for word in ['docker', 'container', 'dockerfile', 'compose', 'kubernetes', 'k8s']):
            return 'docker'
        
        # Database keywords
        if any(word in task_lower for word in ['database', 'sql', 'postgres', 'postgresql', 'mysql', 'mongodb', 'query']):
            return 'database'
        
        # n8n keywords
        if any(word in task_lower for word in ['n8n', 'workflow', 'automation', 'integration']):
            return 'automation'
        
        # Simple tasks
        if any(word in task_lower for word in ['what is', 'show', 'list', 'get', 'check', 'find']):
            return 'simple'
        
        return 'general'
    
    def _display_initialization(self):
        """Display initialization info"""
        # Create models table
        table = Table(title="🤖 Available Models", show_header=True)
        table.add_column("Model", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Specialization", style="yellow")
        table.add_column("Best For", style="blue")
        
        for model in self.available_models:
            name = model['name']
            size_gb = model.get('size', 0) / 1_000_000_000
            caps = self.model_capabilities.get(name, {})
            
            table.add_row(
                name,
                f"{size_gb:.1f} GB",
                caps.get('specialization', 'general'),
                ', '.join(caps.get('best_for', ['general'])[:2])
            )
        
        console.print(table)
        
        # Tools count
        basic_tools = len(self.tools.get_tool_descriptions().split('\n'))
        expert_tools = len(self.expert_tools.get_tool_descriptions().split('\n'))
        extended_tools = len(self.extended_tools.get_tool_descriptions().split('\n'))
        total_tools = basic_tools + expert_tools + extended_tools
        
        console.print(Panel.fit(
            f"[bold green]🎓 Expert AI Agent Initialized[/bold green]\n"
            f"[cyan]Total Models:[/cyan] {len(self.available_models)}\n"
            f"[cyan]Total Tools:[/cyan] {total_tools} (Basic: {basic_tools}, Expert: {expert_tools}, Extended: {extended_tools})\n"
            f"[cyan]Online Learning:[/cyan] {'✅ Enabled' if self.enable_online_learning else '❌ Disabled'}\n"
            f"[cyan]Max Iterations:[/cyan] {self.max_iterations}",
            title="Expert Agent Status"
        ))
    
    def _diagnose_ollama_issue(self) -> Dict[str, Any]:
        """
        Diagnose Ollama service health and system resources.
        Returns diagnostic information about potential issues.
        """
        diagnostics = {
            'ollama_health': 'unknown',
            'system_resources': {},
            'ollama_process': 'unknown',
            'issues': []
        }
        
        # Check Ollama health
        try:
            health_response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if health_response.status_code == 200:
                diagnostics['ollama_health'] = 'healthy'
            else:
                diagnostics['ollama_health'] = 'unhealthy'
                diagnostics['issues'].append(f"Ollama returned status {health_response.status_code}")
        except requests.exceptions.ConnectionError:
            diagnostics['ollama_health'] = 'not_connected'
            diagnostics['issues'].append("Cannot connect to Ollama service")
        except requests.exceptions.Timeout:
            diagnostics['ollama_health'] = 'slow'
            diagnostics['issues'].append("Ollama is responding slowly")
        except Exception as e:
            diagnostics['ollama_health'] = 'error'
            diagnostics['issues'].append(f"Error checking Ollama: {str(e)}")
        
        # Check system resources
        try:
            resources = self.tools.monitor_resources()
            diagnostics['system_resources'] = resources
            
            # Check for resource issues
            if isinstance(resources, dict):
                cpu_percent = resources.get('cpu_percent', 0)
                memory_percent = resources.get('memory_percent', 0)
                
                if cpu_percent > 90:
                    diagnostics['issues'].append(f"High CPU usage: {cpu_percent:.1f}%")
                if memory_percent > 90:
                    diagnostics['issues'].append(f"High memory usage: {memory_percent:.1f}%")
        except Exception as e:
            diagnostics['issues'].append(f"Error checking resources: {str(e)}")
        
        # Check Ollama process
        try:
            import psutil
            ollama_found = False
            for proc in psutil.process_iter(['name', 'pid', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    proc_name = proc.info['name'].lower()
                    if 'ollama' in proc_name:
                        ollama_found = True
                        diagnostics['ollama_process'] = {
                            'pid': proc.info['pid'],
                            'status': proc.info['status'],
                            'cpu_percent': proc.info.get('cpu_percent', 0),
                            'memory_percent': proc.info.get('memory_percent', 0)
                        }
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not ollama_found:
                diagnostics['issues'].append("Ollama process not found")
        except Exception as e:
            diagnostics['issues'].append(f"Error checking Ollama process: {str(e)}")
        
        return diagnostics
    
    def _try_fallback_model(self, failed_model: str, prompt: str, temperature: float = 0.1) -> Optional[str]:
        """
        Try a fallback model when the primary model fails.
        Selects a faster/smaller model based on model_capabilities.
        """
        console.print(f"[yellow]⚠ Attempting fallback model (previous: {failed_model})...[/yellow]")
        
        # Find faster/smaller models
        fallback_candidates = []
        
        for model in self.available_models:
            name = model['name']
            if name == failed_model:
                continue
            
            caps = self.model_capabilities.get(name, {})
            size = model.get('size', 0)
            
            # Prefer smaller, faster models
            if caps.get('speed') in ['very_fast', 'fast']:
                fallback_candidates.append((name, size, caps))
        
        # Sort by size (smaller first) and speed
        fallback_candidates.sort(key=lambda x: (x[1], 0 if x[2].get('speed') == 'very_fast' else 1))
        
        # Try fallback models
        for model_name, _, _ in fallback_candidates[:3]:  # Try up to 3 fallback models
            console.print(f"[cyan]🔄 Trying fallback model: {model_name}[/cyan]")
            try:
                # Disable fallback to prevent infinite recursion
                result = self._call_ollama(prompt, model_name, temperature, use_fallback=False)
                if not result.startswith("Error:"):
                    console.print(f"[green]✅ Fallback model {model_name} succeeded![/green]")
                    return result
            except Exception as e:
                console.print(f"[red]❌ Fallback model {model_name} failed: {str(e)}[/red]")
                continue
        
        return None
    
    def _call_ollama(self, prompt: str, model: str, temperature: float = 0.1, use_fallback: bool = True) -> str:
        """
        Call Ollama API with specified model using streaming and adaptive timeout.
        
        Features:
        - Real-time streaming to monitor progress
        - Adaptive timeout that extends when progress is detected (up to 600 seconds)
        - Automatic diagnostics when no progress detected
        - Fallback model switching on failure
        """
        base_timeout = 120  # Initial timeout: 2 minutes
        max_timeout = 600   # Maximum timeout: 10 minutes
        no_progress_threshold = 30  # Consider stalled if no data for 30 seconds
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Calling {model}...", total=None)
                
                # Start streaming request
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "stream": True
                    },
                    stream=True,
                    timeout=base_timeout
                )
                
                if response.status_code != 200:
                    error_msg = f"Error: Status {response.status_code}"
                    if use_fallback:
                        fallback_result = self._try_fallback_model(model, prompt, temperature)
                        if fallback_result:
                            return fallback_result
                    return error_msg
                
                # Process streaming response
                full_response = ""
                tokens_received = 0
                last_data_time = time.time()
                current_timeout = base_timeout
                start_time = time.time()
                stalled = False
                last_status_update = 0
                status_update_interval = 10  # Update status every 10 seconds
                
                # Initial status
                console.print(f"[cyan]📡 Status:[/cyan] [green]Connecting to {model}...[/green]")
                
                try:
                    for line in response.iter_lines():
                        current_time = time.time()
                        elapsed = current_time - start_time
                        time_since_last_data = current_time - last_data_time
                        
                        # Periodic status updates
                        if current_time - last_status_update >= status_update_interval:
                            last_status_update = current_time
                            if tokens_received > 0:
                                tokens_per_sec = tokens_received / elapsed if elapsed > 0 else 0
                                status = f"[green]✅ Active[/green] - Processing ({tokens_received} tokens @ {tokens_per_sec:.1f}/s, {elapsed:.0f}s elapsed)"
                            elif elapsed < 30:
                                status = f"[yellow]⏳ Waiting[/yellow] - Model is thinking ({elapsed:.0f}s elapsed)"
                            elif elapsed < 60:
                                status = f"[yellow]⚠️ Slow Start[/yellow] - Model taking longer than usual ({elapsed:.0f}s, no tokens yet)"
                            else:
                                status = f"[red]⚠️ Very Slow[/red] - No tokens received for {elapsed:.0f}s - Model may be stuck or overloaded"
                            console.print(f"[cyan]📊 Status:[/cyan] {status}")
                            
                            # Early warning if taking too long (only show once)
                            if elapsed > 60 and tokens_received == 0 and elapsed < 70:
                                console.print(f"[yellow]💡 Tip:[/yellow] Model is taking longer than expected. This might indicate:")
                                console.print(f"  • Model is processing a complex request")
                                console.print(f"  • System resources are limited (check CPU/RAM)")
                                console.print(f"  • Consider using a smaller/faster model")
                        
                        # Warning before timeout (at 80% of timeout)
                        if elapsed > current_timeout * 0.8 and elapsed < current_timeout:
                            remaining = current_timeout - elapsed
                            console.print(f"[yellow]⏰ Warning:[/yellow] Timeout approaching in {remaining:.0f}s...")
                        
                        # Check overall timeout first
                        if elapsed > current_timeout:
                            error_msg = f"Error: Request timed out after {elapsed:.1f}s"
                            console.print(f"[red]❌ {error_msg}[/red]")
                            console.print(f"[yellow]🔍 Attempting diagnostics...[/yellow]")
                            
                            diagnostics = self._diagnose_ollama_issue()
                            if diagnostics['issues']:
                                console.print("[red]📋 Diagnostics:[/red]")
                                for issue in diagnostics['issues']:
                                    console.print(f"  • {issue}")
                            
                            if use_fallback:
                                fallback_result = self._try_fallback_model(model, prompt, temperature)
                                if fallback_result:
                                    return fallback_result
                            
                            return error_msg
                        
                        if line:
                            last_data_time = current_time
                            
                            # Reset stalled flag when we receive data
                            if stalled:
                                stalled = False
                                console.print(f"[green]✅ Resumed[/green] - Receiving data again")
                            
                            try:
                                chunk = json.loads(line)
                                
                                # Check if response is complete
                                if chunk.get('done', False):
                                    console.print(f"[green]✅ Complete[/green] - Received {tokens_received} tokens in {elapsed:.1f}s")
                                    break
                                
                                # Extract response text
                                chunk_text = chunk.get('response', '')
                                if chunk_text:
                                    full_response += chunk_text
                                    tokens_received += 1
                                    
                                    # Update progress bar with detailed status
                                    if tokens_received % 10 == 0 or tokens_received == 1:  # Update every 10 tokens or first token
                                        status_emoji = "🧠" if "learn" in prompt.lower() else "💭"
                                        status_text = "Learning" if "learn" in prompt.lower() else "Processing"
                                        tokens_per_sec = tokens_received / elapsed if elapsed > 0 else 0
                                        progress.update(
                                            task,
                                            description=f"{status_emoji} {status_text} with {model}... ({tokens_received} tokens @ {tokens_per_sec:.1f}/s, {elapsed:.0f}s)"
                                        )
                                        
                                        # Show first token received message
                                        if tokens_received == 1:
                                            console.print(f"[green]✅ First token received[/green] after {elapsed:.1f}s - Model is responding")
                                
                                # Adaptive timeout: extend if we're making progress
                                if elapsed < max_timeout:
                                    # Extend timeout if we're receiving data
                                    if time_since_last_data < 5:  # Received data in last 5 seconds
                                        current_timeout = min(max_timeout, elapsed + 60)  # Add 1 minute buffer
                            
                            except json.JSONDecodeError:
                                continue
                        else:
                            # Empty line - check for stall condition
                            if time_since_last_data > no_progress_threshold and not stalled:
                                stalled = True
                                console.print(f"[yellow]⚠️ Stalled[/yellow] - No progress for {no_progress_threshold}s (elapsed: {elapsed:.0f}s)")
                                console.print(f"[cyan]🔍 Diagnosing issue...[/cyan]")
                                
                                # Run diagnostics
                                diagnostics = self._diagnose_ollama_issue()
                                
                                # Display diagnostics
                                if diagnostics['issues']:
                                    console.print("[red]📋 Diagnostics:[/red]")
                                    for issue in diagnostics['issues']:
                                        console.print(f"  • {issue}")
                                
                                # If Ollama is healthy, continue waiting (might be a large response)
                                if diagnostics['ollama_health'] == 'healthy':
                                    console.print(f"[green]✅ Ollama is healthy[/green] - Continuing to wait (might be processing large response)")
                                    console.print(f"[dim]⏳ Will wait up to {current_timeout - elapsed:.0f}s more...[/dim]")
                                    last_data_time = current_time  # Reset timer
                                    stalled = False
                                else:
                                    # Ollama has issues, abort and try fallback
                                    error_msg = f"Error: Ollama issue detected - {', '.join(diagnostics['issues'])}"
                                    console.print(f"[red]❌ {error_msg}[/red]")
                                    if use_fallback:
                                        fallback_result = self._try_fallback_model(model, prompt, temperature)
                                        if fallback_result:
                                            return fallback_result
                                    return error_msg
                            elif stalled and time_since_last_data > no_progress_threshold:
                                # Still stalled, show periodic updates
                                if int(time_since_last_data) % 15 == 0:  # Every 15 seconds
                                    console.print(f"[yellow]⏳ Still waiting...[/yellow] No data for {time_since_last_data:.0f}s (total: {elapsed:.0f}s)")
                    
                    # Successfully received full response
                    if full_response:
                        return full_response
                    else:
                        return "Error: Empty response from Ollama"
                
                except requests.exceptions.Timeout:
                    error_msg = f"Error: Request timed out after {current_timeout}s"
                    console.print(f"[yellow]⚠ {error_msg}, attempting diagnostics...[/yellow]")
                    
                    diagnostics = self._diagnose_ollama_issue()
                    if diagnostics['issues']:
                        console.print("[red]Diagnostics:[/red]")
                        for issue in diagnostics['issues']:
                            console.print(f"  - {issue}")
                    
                    if use_fallback:
                        fallback_result = self._try_fallback_model(model, prompt, temperature)
                        if fallback_result:
                            return fallback_result
                    
                    return error_msg
        
        except requests.exceptions.ConnectionError:
            error_msg = "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
            console.print(f"[red]{error_msg}[/red]")
            
            if use_fallback:
                # Still try fallback in case it's a model-specific issue
                fallback_result = self._try_fallback_model(model, prompt, temperature)
                if fallback_result:
                    return fallback_result
            
            return error_msg
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            console.print(f"[red]{error_msg}[/red]")
            
            if use_fallback:
                fallback_result = self._try_fallback_model(model, prompt, temperature)
                if fallback_result:
                    return fallback_result
            
            return error_msg
    
    def run(self, user_input: str, task_type: str = None) -> str:
        """
        Run the expert agent with tool execution loop
        """
        console.print(Panel(
            f"[bold cyan]{user_input}[/bold cyan]",
            title="🎯 Expert Task",
            border_style="cyan"
        ))
        
        # Select best model
        selected_model = self._select_best_model(user_input, task_type)
        
        # Build prompt
        prompt = self._build_expert_prompt(user_input, selected_model)
        
        console.print(f"\n[yellow]🚀 Executing with {selected_model}...[/yellow]\n")
        console.print(f"[cyan]📊 Status:[/cyan] [green]Starting AI processing...[/green]\n")
        
        # Initial response
        response = self._call_ollama(prompt, selected_model)
        
        # Status update after getting response
        if response and not response.startswith("Error:"):
            console.print(f"[cyan]📊 Status:[/cyan] [green]AI response received, analyzing for tool calls...[/green]")
        elif response.startswith("Error:"):
            console.print(f"[cyan]📊 Status:[/cyan] [red]Error occurred during AI processing[/red]")
        
        # Check for tool calls (Simple heuristic for now)
        # We look for patterns like: tool_name(arg1="val", arg2="val") or JSON format
        
        tool_executed = False
        tools_executed_count = 0
        # Start with empty response, we'll build it from tool results and cleaned explanation
        final_response = ""
        original_response = response
        
        # Try to find tool calls in the response
        # This is a simplified parser. In production, we'd use structured output or regex
        import re
        
        # === STEP 1: Try to parse JSON-style tool calls first ===
        json_tool_calls = []
        try:
            # Look for JSON objects with "tool" and "args" fields
            # Use a more robust approach: find complete JSON objects
            json_pattern = r'\{[^{}]*"tool"\s*:\s*"([^"]+)"[^{}]*"args"\s*:\s*(\[.*?\])\s*[^{}]*\}'
            
            # For nested structures, we need to handle it differently
            # Let's try to find all potential JSON blocks first
            potential_jsons = []
            brace_count = 0
            start_idx = -1
            
            for i, char in enumerate(response):
                if char == '{':
                    if brace_count == 0:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        json_str = response[start_idx:i+1]
                        potential_jsons.append(json_str)
                        start_idx = -1
            
            # Now try to parse each potential JSON
            for json_str in potential_jsons:
                try:
                    data = json.loads(json_str)
                    if isinstance(data, dict) and "tool" in data and "args" in data:
                        tool_name = data["tool"]
                        args_list = data["args"]
                        if not isinstance(args_list, list):
                            args_list = [args_list]
                        json_tool_calls.append((tool_name, args_list))
                        console.print(f"[cyan]📊 Status:[/cyan] [yellow]Found JSON tool call: {tool_name}[/yellow]")
                except (json.JSONDecodeError, KeyError):
                    continue
                    
        except Exception as e:
            console.print(f"[dim]Note: JSON tool parsing failed: {e}[/dim]")
        
        # === STEP 2: Execute JSON-style tool calls ===
        for tool_name, args_list in json_tool_calls:
            # Check if it's a valid tool
            if hasattr(self.tools, tool_name) or hasattr(self.expert_tools, tool_name) or hasattr(self.extended_tools, tool_name):
                console.print(f"[bold green]🔧 Executing Tool:[/bold green] {tool_name}")
                
                # Show what the tool is doing
                if "learn" in tool_name.lower():
                    console.print(f"[dim]💡 Action: Learning and saving knowledge...[/dim]")
                elif "search" in tool_name.lower():
                    console.print(f"[dim]🔍 Action: Searching for information...[/dim]")
                elif "read" in tool_name.lower():
                    console.print(f"[dim]📖 Action: Reading from knowledge base...[/dim]")
                elif "save" in tool_name.lower() or "update" in tool_name.lower():
                    console.print(f"[dim]💾 Action: Saving/updating knowledge...[/dim]")
                
                # Convert args list to params dict based on tool signature
                params = {}
                try:
                    if tool_name == "learn_new_technology":
                        # args: [technology, topics_list]
                        if len(args_list) >= 1:
                            params["technology"] = args_list[0]
                            params["topics"] = args_list[1] if len(args_list) > 1 else []
                    
                    elif tool_name == "search_documentation":
                        # args: [query] or [technology, query]
                        if len(args_list) == 1:
                            params["query"] = args_list[0]
                        elif len(args_list) >= 2:
                            params["technology"] = args_list[0]
                            params["query"] = args_list[1]
                    
                    elif tool_name == "read_knowledge_base":
                        # args: [technology]
                        if args_list:
                            params["technology"] = args_list[0]
                    
                    elif tool_name == "update_knowledge_base":
                        # args: [technology, content, filename, append]
                        if len(args_list) >= 2:
                            params["technology"] = args_list[0]
                            params["content"] = args_list[1]
                            params["filename"] = args_list[2] if len(args_list) > 2 else "overview.md"
                            params["append"] = args_list[3] if len(args_list) > 3 else False
                    
                    elif tool_name == "save_code_snippet":
                        # args: [code, language, description, tags]
                        if len(args_list) >= 3:
                            params["code"] = args_list[0]
                            params["language"] = args_list[1]
                            params["description"] = args_list[2]
                            params["tags"] = args_list[3] if len(args_list) > 3 else []
                    
                    elif tool_name == "search_web":
                        # args: [query, max_results]
                        if args_list:
                            params["query"] = args_list[0]
                            params["max_results"] = int(args_list[1]) if len(args_list) > 1 else 5
                    
                    # Generic fallback: use first arg as "query" or "technology"
                    if not params and args_list:
                        if "search" in tool_name.lower():
                            params["query"] = args_list[0]
                        elif "learn" in tool_name.lower() or "read" in tool_name.lower():
                            params["technology"] = args_list[0]
                
                except Exception as e:
                    console.print(f"[red]Error parsing JSON args: {e}[/red]")
                
                # Execute tool
                result = "Error: Tool execution failed"
                try:
                    if hasattr(self.tools, tool_name):
                        method = getattr(self.tools, tool_name)
                        result = method(**params)
                    elif hasattr(self.expert_tools, tool_name):
                        result = self.expert_tools.execute(tool_name, params)
                    elif hasattr(self.extended_tools, tool_name):
                        result = self.extended_tools.execute(tool_name, params)
                    
                    console.print(Panel(str(result), title=f"✅ Tool Result: {tool_name}", border_style="green"))
                    
                    # Status update
                    if "Successfully" in str(result) or "✅" in str(result):
                        console.print(f"[cyan]📊 Status:[/cyan] [green]Tool completed successfully[/green]")
                    elif "Error" in str(result) or "❌" in str(result):
                        console.print(f"[cyan]📊 Status:[/cyan] [red]Tool encountered an error[/red]")
                    else:
                        console.print(f"[cyan]📊 Status:[/cyan] [yellow]Tool execution completed[/yellow]")
                    
                    # Add to final response
                    if result not in final_response:
                        if final_response:
                            final_response += f"\n\n{result}"
                        else:
                            final_response = result
                    tool_executed = True
                    tools_executed_count += 1
                
                except Exception as e:
                    console.print(f"[red]❌ Error executing {tool_name}: {str(e)}[/red]")
                    console.print(Panel(str(e), title=f"❌ Execution Error: {tool_name}", border_style="red"))
        
        # === STEP 3: Fallback to function-style parsing ===
        # Regex to find tool calls: tool_name(arg="val")
        tool_pattern = r'(\w+)\((.*?)\)'
        matches = re.findall(tool_pattern, response)
        
        for tool_name, args_str in matches:
            # Check if it's a valid tool
            if hasattr(self.tools, tool_name) or hasattr(self.expert_tools, tool_name) or hasattr(self.extended_tools, tool_name):
                console.print(f"[cyan]📊 Status:[/cyan] [yellow]Found tool call: {tool_name}[/yellow]")
                console.print(f"[bold green]🔧 Executing Tool:[/bold green] {tool_name}")
                
                # Show what the tool is doing
                if "learn" in tool_name.lower():
                    console.print(f"[dim]💡 Action: Learning and saving knowledge...[/dim]")
                elif "search" in tool_name.lower():
                    console.print(f"[dim]🔍 Action: Searching for information...[/dim]")
                elif "read" in tool_name.lower():
                    console.print(f"[dim]📖 Action: Reading from knowledge base...[/dim]")
                elif "save" in tool_name.lower() or "update" in tool_name.lower():
                    console.print(f"[dim]💾 Action: Saving/updating knowledge...[/dim]")
                
                # Parse arguments (Improved Parser)
                params = {}
                try:
                    # 1. Try to parse key="value" pattern
                    kwargs_pattern = r'(\w+)=["\'](.*?)["\']'
                    kwargs_matches = re.findall(kwargs_pattern, args_str)
                    
                    if kwargs_matches:
                        for key, val in kwargs_matches:
                            params[key] = val
                    
                    # 2. If no kwargs found, try positional args (strings between quotes)
                    elif '"' in args_str or "'" in args_str:
                        args_matches = re.findall(r'["\'](.*?)["\']', args_str)
                        
                        # Map positional args to parameters based on tool name
                        if tool_name == "search_documentation":
                            if len(args_matches) >= 2:
                                params = {"technology": args_matches[0], "query": args_matches[1]}
                            elif len(args_matches) == 1:
                                params = {"technology": args_matches[0], "query": "general"}
                                
                        elif tool_name == "search_web":
                            if args_matches:
                                params = {"query": args_matches[0]}
                                if len(args_matches) > 1:
                                    try:
                                        params["max_results"] = int(args_matches[1])
                                    except:
                                        pass
                                
                        elif tool_name == "read_knowledge_base":
                            if args_matches:
                                params = {"technology": args_matches[0]}
                                
                        elif tool_name == "learn_new_technology":
                            if args_matches:
                                params = {"technology": args_matches[0], "topics": args_matches[1:] if len(args_matches) > 1 else ["General"]}
                                
                        elif tool_name == "update_knowledge_base":
                            if len(args_matches) >= 2:
                                params = {
                                    "technology": args_matches[0],
                                    "content": args_matches[1],
                                    "filename": args_matches[2] if len(args_matches) > 2 else "overview.md",
                                    "append": args_matches[3].lower() == "true" if len(args_matches) > 3 else False
                                }
                                
                        elif tool_name == "save_code_snippet":
                            if len(args_matches) >= 3:
                                params = {
                                    "code": args_matches[0],
                                    "language": args_matches[1],
                                    "description": args_matches[2],
                                    "tags": args_matches[3:] if len(args_matches) > 3 else []
                                }
                        
                        # Fallback for single argument tools
                        elif args_matches and not params:
                            # Try to guess the first argument name based on common patterns
                            params = {"technology": args_matches[0]} # Default guess
                            
                except Exception as e:
                    console.print(f"[red]Error parsing args: {e}[/red]")
                
                # Execute tool
                result = "Error: Tool execution failed"
                
                # Ensure required params exist (Simple validation)
                if tool_name == "search_documentation" and "query" not in params:
                     params["query"] = "general"
                if tool_name == "search_web" and "query" not in params and args_matches:
                    params["query"] = args_matches[0]
                
                # Execute tool from the appropriate class
                if hasattr(self.tools, tool_name):
                    # Execute tool from basic tools
                    method = getattr(self.tools, tool_name)
                    result = method(**params)
                elif hasattr(self.expert_tools, tool_name):
                    result = self.expert_tools.execute(tool_name, params)
                elif hasattr(self.extended_tools, tool_name):
                    result = self.extended_tools.execute(tool_name, params)
                
                console.print(Panel(str(result), title=f"✅ Tool Result: {tool_name}", border_style="green"))
                
                # Status update based on tool result
                if "Successfully" in str(result) or "✅" in str(result):
                    console.print(f"[cyan]📊 Status:[/cyan] [green]Tool completed successfully[/green]")
                elif "Error" in str(result) or "❌" in str(result):
                    console.print(f"[cyan]📊 Status:[/cyan] [red]Tool encountered an error[/red]")
                else:
                    console.print(f"[cyan]📊 Status:[/cyan] [yellow]Tool execution completed[/yellow]")
                
                # Add tool output with separator (only if not already added)
                if result not in final_response:
                    if final_response:
                        final_response += f"\n\n{result}"
                    else:
                        final_response = result
                tool_executed = True
                tools_executed_count += 1
        
        if not tool_executed:
            # If no tool was detected by regex, check for specific keywords
            if "read_knowledge_base" in response and "n8n" in user_input.lower():
                console.print("[bold green]🔧 Auto-executing read_knowledge_base for n8n...[/bold green]")
                result = self.expert_tools.read_knowledge_base("n8n")
                console.print(Panel(str(result), title="✅ Tool Result", border_style="green"))
                final_response += f"\n\n{result}"
        
        # Clean up original response: Remove tool call patterns and extract only meaningful explanation
        import re
        
        # If tools were executed, clean the original response to get only the explanation part
        if tool_executed:
            # Remove tool calls from original response
            tool_call_pattern = r'\w+\([^)]*\)\s*\n?'
            cleaned_explanation = re.sub(tool_call_pattern, '', original_response)
            
            # Remove lines that are just tool calls or empty
            lines = cleaned_explanation.split('\n')
            meaningful_lines = []
            for line in lines:
                line = line.strip()
                # Skip empty lines, tool calls, and tool execution messages
                is_tool_call = re.match(r'^\w+\(.*\)$', line)
                is_tool_message = ('tool' in line.lower() and ('executed' in line.lower() or 'called' in line.lower() or 'will' in line.lower()))
                
                if line and not is_tool_call and not is_tool_message:
                    meaningful_lines.append(line)
            
            cleaned_explanation = '\n'.join(meaningful_lines).strip()
            
            # Remove any tool results that might be in the explanation (prevent duplication)
            # Tool results typically contain emojis like 🎉, ✅, 📂, etc.
            if final_response:
                # Remove lines from explanation that match tool result patterns
                explanation_lines = cleaned_explanation.split('\n')
                filtered_lines = []
                for line in explanation_lines:
                    line_stripped = line.strip()
                    # Skip lines that look like tool results (contain result indicators)
                    is_tool_result = (
                        '🎉' in line_stripped or 
                        '✅' in line_stripped or 
                        '📂' in line_stripped or
                        'Successfully' in line_stripped or
                        'Local Knowledge' in line_stripped or
                        line_stripped in final_response[:100]  # Check if line appears in tool result
                    )
                    if not is_tool_result:
                        filtered_lines.append(line)
                cleaned_explanation = '\n'.join(filtered_lines).strip()
            
            # Combine: explanation (if meaningful) + tool results
            cleaned_explanation = cleaned_explanation.strip()
            
            # Check if explanation already contains tool results (prevent duplication)
            if final_response:
                # Remove tool result content from explanation if it's already in final_response
                explanation_words = set(cleaned_explanation.split()[:50])  # First 50 words
                result_words = set(final_response.split()[:50])
                overlap = len(explanation_words & result_words)
                
                # If more than 30% overlap, explanation likely contains tool results
                if overlap > len(explanation_words) * 0.3:
                    cleaned_explanation = ""  # Skip explanation, it's duplicate
            
            if cleaned_explanation and len(cleaned_explanation) > 20:  # Only if there's meaningful content
                final_response = cleaned_explanation + "\n\n" + final_response
            else:
                # If no meaningful explanation, just show tool results
                final_response = final_response.strip()
        else:
            # No tools executed, use original response
            final_response = original_response.strip()

        # Remove duplicate sections
        final_response = re.sub(r'--- Tool Output ---\s*', '', final_response)
        final_response = re.sub(r'\n{3,}', '\n\n', final_response)  # Remove excessive newlines
        final_response = final_response.strip()

        # Final status update
        if tool_executed:
            console.print(f"\n[cyan]📊 Final Status:[/cyan] [green]✅ Task completed successfully[/green]")
            console.print(f"[dim]💡 Tools executed: {tools_executed_count} tool(s)[/dim]\n")
        else:
            console.print(f"\n[cyan]📊 Final Status:[/cyan] [yellow]⚠️ No tools executed, showing AI response only[/yellow]\n")

        # Display final response
        if final_response:
            console.print(Panel(
                Markdown(final_response),
                title="✅ Expert Response",
                border_style="green"
            ))
        
        return final_response
    
    def _build_expert_prompt(self, user_input: str, model: str) -> str:
        """Build optimized prompt for the selected model"""
        
        # Get all available tools from all three libraries
        all_tools = (
            self.tools.get_tool_descriptions() + "\n\n" + 
            self.expert_tools.get_tool_descriptions() + "\n\n" +
            self.extended_tools.get_tool_descriptions()
        )
        
        prompt = f"""You are an expert AI agent with access to 100+ specialized tools.

AVAILABLE TOOLS:
{all_tools}

USER REQUEST: {user_input}

CRITICAL INSTRUCTIONS:
1. **MUST EXECUTE TOOLS**: If the user asks you to learn, save, search, create files, or perform any action, you MUST actually call the tool by writing it in this exact format:
   write_file("filename.bat", "@echo off\ndate /T\ntime /T")
   write_file("script.py", "print('Hello')")
   learn_new_technology("TechnologyName", ["topic1", "topic2"])
   read_knowledge_base("TechnologyName")
   search_documentation("TechnologyName", "query")
   update_knowledge_base("TechnologyName", "content to save", "filename.md", append=False)

2. **FOR FILE CREATION**: When user asks to create ANY file (batch, Python, text, etc.), you MUST use write_file tool:
   - write_file("filename.ext", "full file content here")
   - DO NOT just show code - ACTUALLY CREATE THE FILE using write_file!
   - Example: User asks "create a batch file to show date and time"
     → You MUST call: write_file("show_date_time.bat", "@echo off\ndate /T\ntime /T\npause")

3. **DO NOT JUST EXPLAIN**: Do not just explain what you would do - ACTUALLY DO IT by writing the tool call.

4. **TOOL CALL FORMAT**: Write tool calls exactly like this:
   - write_file("script.bat", "@echo off\necho Hello\npause")
   - write_file("app.py", "print('Hello World')")
   - learn_new_technology("Docker", ["containers", "images", "docker-compose"])
   - read_knowledge_base("Docker")
   - search_documentation("Docker", "networking")
   - update_knowledge_base("Docker", "# Docker Containers\n\nContainers are...", "overview.md", append=True)

5. **SAVE SEARCH RESULTS**: After searching, use update_knowledge_base to save the actual content, not just show URLs.

6. **FOR LEARNING TASKS**: When user asks to "learn" something:
   - First: learn_new_technology("Technology", ["topic1", "topic2"])
   - Then: search_documentation("Technology", "topic1") to get real content
   - Then: update_knowledge_base("Technology", "FULL CONTENT FROM SEARCH RESULTS HERE", "topic1.md", append=False)
   - IMPORTANT: Copy the ENTIRE search result content (titles, snippets, URLs) into update_knowledge_base, not just placeholder text!
   - Repeat for each topic

7. **DO NOT REPEAT TOOL CALLS**: After executing a tool, do NOT repeat the tool call in your response. Only show the results and your explanation.

8. **ACTUALLY SEARCH AND SAVE**: Don't just create empty structure - search for real content and save it!

9. **SAVE FULL CONTENT**: When using update_knowledge_base, you MUST pass the FULL content from search results, not placeholder text like "Content from search will be inserted here". Copy the entire search result including titles, descriptions, and URLs.

10. **FILE CREATION EXAMPLES**:
    - User: "create a batch file to show date and time"
      → You MUST call: write_file("show_date_time.bat", "@echo off\ndate /T\ntime /T\npause")
    
    - User: "create a Python script to calculate fibonacci"
      → You MUST call: write_file("fibonacci.py", "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))")
    
    - NEVER just show code without calling write_file!

11. **PROJECT CREATION**: When user asks to create a project, use create_project tool:
    - User: "create a Python project called myapp"
      → You MUST call: create_project("myapp", "python", {"include_tests": True, "include_docs": True})
    
    - User: "create a web project"
      → You MUST call: create_project("web_project", "web", {})
    
    - User: "create a React app called todo-app"
      → You MUST call: create_project("todo-app", "react", {})
    
    - For complex projects, you can combine:
      1. create_project("project_name", "project_type", options) - creates structure
      2. create_directory("project_name/subfolder") - add extra folders
      3. write_file("project_name/file.py", "content") - add specific files

12. **DIRECTORY CREATION**: When user asks to create folders/directories:
    - User: "create a folder called data"
      → You MUST call: create_directory("data")
    
    - User: "create folders for src, tests, docs"
      → You MUST call: create_directory("src"), create_directory("tests"), create_directory("docs")

13. **COMPLETE PROJECT WORKFLOW**: For complex requests like "create a full-stack app":
    - Step 1: create_project("app_name", "project_type", options) - creates base structure
    - Step 2: create_directory("app_name/backend") - add backend folder
    - Step 3: create_directory("app_name/frontend") - add frontend folder
    - Step 4: write_file("app_name/backend/main.py", "code") - add backend files
    - Step 5: write_file("app_name/frontend/index.html", "code") - add frontend files
    - Continue until all requested files are created!

IMPORTANT: For learning tasks, you MUST:
1. Create structure with learn_new_technology
2. Search for real content with search_documentation (which returns full search results)
3. Save the ENTIRE search result content with update_knowledge_base - copy everything from the search result, not just a placeholder!

EXAMPLE:
   search_documentation("Docker", "containers") returns:
   "1. **Title**\n   Description...\n   🔗 URL"
   
   Then you MUST do:
   update_knowledge_base("Docker", "1. **Title**\n   Description...\n   🔗 URL", "containers.md", append=False)
   
   NOT:
   update_knowledge_base("Docker", "Content from search will be inserted here", "containers.md", append=False)

Response:"""
        
        return prompt


def main():
    """Test the expert agent"""
    console.print("""
[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🎓 Expert AI Agent - وكيل خبير                  ║
║                                                           ║
║     Multi-Model • 100+ Tools • Online Learning           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]
    """)
    
    agent = ExpertAgent()
    
    # Test with different task types
    test_tasks = [
        ("Create a Python function to calculate fibonacci", "coding"),
        ("How do I deploy a Docker container?", "docker"),
        ("Design a landing page with HTML/CSS", "web_design"),
    ]
    
    for task, task_type in test_tasks:
        console.print(f"\n[bold]{'='*70}[/bold]")
        agent.run(task, task_type)
        console.print(f"[bold]{'='*70}[/bold]\n")


if __name__ == "__main__":
    main()
