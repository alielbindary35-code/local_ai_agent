"""
Expert-Level Local AI Agent
وكيل الذكاء الاصطناعي المحلي المتقدم

Main agent file implementing the ReAct (Reasoning + Acting) loop
with multi-model orchestration, risk assessment, and continuous learning.
"""

import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.tools.tools import Tools
from src.core.memory import Memory
from src.core.prompts import get_system_prompt, format_tool_response
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm, Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class Agent:
    """
    Expert-Level AI Agent with ReAct loop, multi-model support, and learning capabilities.
    
    وكيل ذكاء اصطناعي متقدم مع حلقة ReAct ودعم متعدد النماذج وقدرات التعلم.
    """
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        default_model: str = "qwen2.5:3b",  # Changed to match installed model
        max_iterations: int = 10,
        auto_approve: bool = False
    ):
        """
        Initialize the agent.
        
        Args:
            ollama_url: URL of local Ollama instance
            default_model: Default model to use
            max_iterations: Maximum ReAct loop iterations
            auto_approve: If True, automatically approve all actions (for testing)
        """
        self.ollama_url = ollama_url
        self.default_model = default_model
        self.max_iterations = max_iterations
        self.auto_approve = auto_approve
        
        # Initialize components
        self.tools = Tools()
        self.memory = Memory()
        self.conversation_history = []
        self.current_task = None
        
        # Available models (will be populated from Ollama)
        self.available_models = self._get_available_models()
        
        console.print(Panel.fit(
            "[bold green]🤖 Expert AI Agent Initialized[/bold green]\n"
            f"[cyan]Ollama URL:[/cyan] {ollama_url}\n"
            f"[cyan]Default Model:[/cyan] {default_model}\n"
            f"[cyan]Available Models:[/cyan] {len(self.available_models)}",
            title="Agent Status"
        ))
    
    def _get_available_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = [model['name'] for model in response.json().get('models', [])]
                return models
            return [self.default_model]
        except Exception as e:
            # console.print(f"[yellow]Warning: Could not fetch models: {e}[/yellow]")
            return [self.default_model]
    
    def _select_model(self, task_complexity: str) -> str:
        """
        Select the best model based on task complexity.
        
        Args:
            task_complexity: 'simple', 'medium', or 'complex'
        
        Returns:
            Model name to use
        """
        # Model preferences by complexity (checking for actual model names)
        preferences = {
            'simple': ['llama3.1:8b', 'llama3.1', 'llama3:8b', 'llama3', 'qwen2.5:7b', 'qwen2.5', 'mistral:7b', 'mistral'],
            'medium': ['qwen2.5:14b', 'qwen2.5', 'llama3.1:8b', 'llama3.1', 'deepseek-coder:6.7b', 'deepseek-coder'],
            'complex': ['llama3.1:70b', 'qwen2.5:32b', 'qwen2.5:14b', 'deepseek-coder:33b', 'llama3.1', 'qwen2.5']
        }
        
        # Find first available model from preferences
        for preferred_model in preferences.get(task_complexity, preferences['simple']):
            # Check if this model exists in available models
            for available in self.available_models:
                if preferred_model in available or available in preferred_model:
                    console.print(f"[dim]Using available model: {available}[/dim]")
                    return available
        
        # If no preferred model found, use the first available model
        if self.available_models:
            console.print(f"[yellow]No preferred model found, using: {self.available_models[0]}[/yellow]")
            return self.available_models[0]
        
        # Fallback to default (will likely fail, but at least we tried)
        console.print(f"[red]Warning: No models found! Using default: {self.default_model}[/red]")
        return self.default_model
    
    def _analyze_task_complexity(self, user_input: str) -> str:
        """
        Analyze task complexity to select appropriate model.
        
        Args:
            user_input: User's request
        
        Returns:
            'simple', 'medium', or 'complex'
        """
        # Simple heuristics (can be improved with ML)
        user_lower = user_input.lower()
        
        # Complex indicators
        complex_keywords = [
            'design', 'architecture', 'analyze', 'optimize', 'security audit',
            'performance', 'scale', 'microservices', 'complex', 'advanced'
        ]
        
        # Simple indicators
        simple_keywords = [
            'what is', 'how do i', 'check', 'list', 'show', 'get', 'find'
        ]
        
        if any(keyword in user_lower for keyword in complex_keywords):
            return 'complex'
        elif any(keyword in user_lower for keyword in simple_keywords):
            return 'simple'
        else:
            return 'medium'
    
    def _assess_risk(self, action: str, action_input: Dict) -> Dict[str, Any]:
        """
        Assess risk level of an action.
        
        Args:
            action: Tool name
            action_input: Tool parameters
        
        Returns:
            Risk assessment dict with level and explanation
        """
        risk_levels = {
            'safe': '🟢',
            'caution': '🟡',
            'dangerous': '🔴'
        }
        
        # Define risk rules
        if action == 'delete_file':
            return {
                'level': 'dangerous',
                'emoji': risk_levels['dangerous'],
                'explanation': 'This will permanently delete files. Cannot be undone.'
            }
        
        elif action == 'run_command':
            cmd = action_input.get('command', '').lower()
            if any(word in cmd for word in ['rm ', 'del ', 'format', 'drop']):
                return {
                    'level': 'dangerous',
                    'emoji': risk_levels['dangerous'],
                    'explanation': 'This command may delete or modify system files.'
                }
            elif any(word in cmd for word in ['install', 'update', 'restart', 'stop']):
                return {
                    'level': 'caution',
                    'emoji': risk_levels['caution'],
                    'explanation': 'This command will modify system state.'
                }
            else:
                return {
                    'level': 'safe',
                    'emoji': risk_levels['safe'],
                    'explanation': 'This is a read-only or low-risk command.'
                }
        
        elif action in ['write_file', 'install_package']:
            return {
                'level': 'caution',
                'emoji': risk_levels['caution'],
                'explanation': 'This will modify files or install software.'
            }
        
        else:
            return {
                'level': 'safe',
                'emoji': risk_levels['safe'],
                'explanation': 'This is a safe, read-only operation.'
            }
    
    def _ask_permission(self, action: str, action_input: Dict, risk: Dict) -> bool:
        """
        Ask user for permission to execute an action.
        
        Args:
            action: Tool name
            action_input: Tool parameters
            risk: Risk assessment
        
        Returns:
            True if user approves, False otherwise
        """
        console.print(Panel(
            f"[bold]{risk['emoji']} {risk['level'].upper()}[/bold]\n\n"
            f"[cyan]Action:[/cyan] {action}\n"
            f"[cyan]Parameters:[/cyan] {json.dumps(action_input, indent=2)}\n\n"
            f"[yellow]Risk:[/yellow] {risk['explanation']}",
            title="Permission Required",
            border_style="yellow"
        ))
        
        if self.auto_approve:
            console.print("[bold green]Auto-approved (Training Mode)[/bold green]")
            return True
            
        return Confirm.ask("Do you approve this action?", default=False)
    
    def _call_ollama(self, prompt: str, model: str) -> str:
        """
        Call Ollama API to get AI response.
        
        Args:
            prompt: Prompt to send
            model: Model to use
        
        Returns:
            AI response text
        """
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task(f"Thinking with {model}...", total=None)
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    return response.json().get('response', '')
                elif response.status_code == 404:
                    error_msg = f"Model '{model}' not found. Please pull it first with: ollama pull {model}"
                    console.print(f"[red]{error_msg}[/red]")
                    console.print(f"[yellow]Available models: {', '.join(self.available_models)}[/yellow]")
                    return f"Error: {error_msg}"
                else:
                    return f"Error: Ollama returned status {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (ollama serve)"
        except requests.exceptions.Timeout:
            return "Error: Request timed out. The model might be too large or busy."
        except Exception as e:
            return f"Error calling Ollama: {str(e)}"
    
    def run(self, user_input: str) -> str:
        """
        Main ReAct loop - processes user request and executes plan.
        
        Args:
            user_input: User's request in natural language
        
        Returns:
            Final response to user
        """
        self.current_task = user_input
        
        # Display user request
        console.print(Panel(
            f"[bold cyan]{user_input}[/bold cyan]",
            title="User Request",
            border_style="cyan"
        ))
        
        # 1. Check memory for similar past solutions
        console.print("\n[yellow]🧠 Checking memory for similar solutions...[/yellow]")
        past_solutions = self.memory.search_similar(user_input)
        
        if past_solutions:
            console.print(f"[green]✓ Found {len(past_solutions)} similar past solution(s)[/green]")
            # Show past solution and ask if user wants to use it
            for solution, rating in past_solutions[:1]:  # Show top solution
                if self.auto_approve:
                    console.print("[yellow]Training Mode: Skipping past solution to verify reasoning...[/yellow]")
                    break
                
                if Confirm.ask(f"Use this past solution? (Rating: {rating}⭐)"):
                    console.print(Panel(solution, title="Past Solution", border_style="green"))
                    return solution
        
        # 2. Analyze task complexity and select model
        complexity = self._analyze_task_complexity(user_input)
        model = self._select_model(complexity)
        console.print(f"[cyan]📊 Task Complexity:[/cyan] {complexity}")
        console.print(f"[cyan]🤖 Selected Model:[/cyan] {model}\n")
        
        # 3. ReAct Loop
        iteration = 0
        final_answer = None
        last_action_signature = None
        
        while iteration < self.max_iterations and not final_answer:
            iteration += 1
            console.print(f"\n[bold magenta]═══ Iteration {iteration}/{self.max_iterations} ═══[/bold magenta]\n")
            
            # Build prompt with history
            prompt = get_system_prompt(
                user_input=user_input,
                tools_list=self.tools.get_tool_descriptions(),
                history=self.conversation_history,
                os_info=self.tools.get_os_identifier()
            )
            
            # Get AI response
            ai_response = self._call_ollama(prompt, model)
            
            # Parse AI response (expecting JSON with thought, action, etc.)
            try:
                # Try to extract JSON from response
                if '{' in ai_response and '}' in ai_response:
                    json_start = ai_response.index('{')
                    json_end = ai_response.rindex('}') + 1
                    response_data = json.loads(ai_response[json_start:json_end])
                else:
                    # If no JSON, treat as final answer
                    final_answer = ai_response
                    break
                
                # Display thought process
                thought = response_data.get('thought', 'No thought provided')
                console.print(Panel(
                    Markdown(f"**Thought:** {thought}"),
                    title="AI Reasoning",
                    border_style="blue"
                ))
                
                # Check if this is a final answer
                if response_data.get('final_answer'):
                    final_answer = response_data['final_answer']
                    break
                
                # Execute action
                action = response_data.get('action')
                action_input = response_data.get('action_input', {})
                
                if not action:
                    console.print("[red]Error: No action specified[/red]")
                    break
                
                # Clean up action_input - remove any extra fields that aren't parameters
                # The AI sometimes adds fields like "tool" which should be removed
                if isinstance(action_input, dict):
                    # Remove 'tool', 'action', or any other meta fields
                    cleaned_input = {k: v for k, v in action_input.items() 
                                   if k not in ['tool', 'action', 'thought', 'risk_level', 'risk_explanation']}
                    action_input = cleaned_input
                
                # Assess risk
                risk = self._assess_risk(action, action_input)
                
                # Ask for permission
                if self._ask_permission(action, action_input, risk):
                    # Execute tool
                    console.print(f"[dim]Executing {action}...[/dim]")
                    result = self.tools.execute(action, action_input)
                    
                    # Truncate long output
                    if len(str(result)) > 2000:
                        result = str(result)[:2000] + "... (truncated)"
                    
                    console.print(Panel(
                        str(result),
                        title=f"Tool Output: {action}",
                        border_style="white"
                    ))
                    
                    # Handle "Tool not found" specifically
                    if isinstance(result, str) and "Tool" in result and "not found" in result:
                        self.conversation_history.append({
                            "role": "system",
                            "content": f"SYSTEM ERROR: {result}. Please check the AVAILABLE TOOLS list and use a valid tool."
                        })
                        continue # Skip adding user message, let the agent retry immediately
                    
                    # Add to history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    self.conversation_history.append({
                        "role": "user", 
                        "content": f"Tool '{action}' output: {result}"
                    })

                    # Loop Detection
                    if last_action_signature == (action, str(action_input)):
                        console.print("[yellow]⚠️ Loop detected! The agent is repeating the same action.[/yellow]")
                        self.conversation_history.append({
                            "role": "system",
                            "content": "You are repeating the same action. Try a different approach or use your internal knowledge if the tool is not working."
                        })
                    last_action_signature = (action, str(action_input))
                    
                else:
                    console.print("[red]Action denied by user.[/red]")
                    self.conversation_history.append({
                        "role": "user",
                        "content": f"Action '{action}' was denied by the user. Please try a different approach."
                    })
            
            except Exception as e:
                console.print(f"[red]Error in iteration: {str(e)}[/red]")
                # Fallback Logic
                self.conversation_history.append({
                    "role": "system",
                    "content": f"Error executing previous action: {str(e)}. If you cannot use tools, try to answer using your internal knowledge."
                })
                console.print(f"[yellow]The AI may need clearer instructions. Trying next iteration...[/yellow]")
                # Don't break - let it try again
                continue
        
        # Display final answer first
        if final_answer:
            console.print(Panel(
                Markdown(final_answer),
                title="Final Answer",
                border_style="green"
            ))
            
            # 4. Save successful solution to memory (AFTER showing answer)
            if iteration < self.max_iterations:
                # Don't save if it looks like an error
                if "Error:" in final_answer or "returned status" in final_answer:
                    return final_answer

                # Simplified feedback loop
                console.print("\n[dim]──────────────────────────────────────────────────────────────────────[/dim]")
                
                should_save = False
                if self.auto_approve:
                    should_save = True # Auto-save in training mode
                else:
                    should_save = Confirm.ask("Did this solve your problem?", default=True)
                
                if should_save:
                    try:
                        # Auto-save with high rating if user says yes
                        self.memory.save_solution(
                            problem=user_input,
                            solution=final_answer,
                            rating=5  # Assume 5 stars if it solved the problem
                        )
                        console.print("[green]✓ Solution saved to memory[/green]")
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not save to memory: {e}[/yellow]")
                else:
                    console.print("[yellow]Okay, I won't save this solution.[/yellow]")
        else:
            final_answer = "Maximum iterations reached without finding a solution."
            console.print(Panel(
                final_answer,
                title="Final Answer",
                border_style="red"
            ))
        
        return final_answer


def main():
    """Main entry point for the agent."""
    console.print("""
[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🤖 Expert-Level Local AI Agent                  ║
║                                                           ║
║     Powered by Ollama • Secure • Local • Self-Learning   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]
    """)
    
    # Initialize agent
    try:
        agent = Agent()
    except Exception as e:
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        console.print("[yellow]Make sure Ollama is running at http://localhost:11434[/yellow]")
        return
    
    # Main loop
    console.print("\n[green]Agent ready! Type your request or 'quit' to exit.[/green]\n")
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            
            if not user_input.strip():
                continue
            
            # Run agent
            agent.run(user_input)
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
