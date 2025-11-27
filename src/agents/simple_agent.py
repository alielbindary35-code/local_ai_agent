"""
Simple Agent - نسخة مبسطة من الـ Agent للتدريب السريع
Uses simplified prompts and faster iterations
"""

import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from src.tools.tools import Tools
from src.core.memory import Memory
from src.core.simple_prompts import get_simple_prompt
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class SimpleAgent:
    """Simplified AI Agent for training"""
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "qwen2.5:3b",
        max_iterations: int = 5,  # Reduced from 10
        auto_approve: bool = True
    ):
        self.ollama_url = ollama_url
        self.model = model
        self.max_iterations = max_iterations
        self.auto_approve = auto_approve
        
        self.tools = Tools()
        self.memory = Memory()
        self.conversation_history = []
        
        console.print(Panel.fit(
            f"[bold green]🤖 Simple Agent Ready[/bold green]\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Max Iterations:[/cyan] {max_iterations}",
            title="Simple Agent"
        ))
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                progress.add_task(f"Thinking...", total=None)
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,  # Lower temperature for more focused responses
                            "num_predict": 512   # Limit response length
                        }
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json().get('response', '')
                else:
                    return f"Error: Status {response.status_code}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run(self, user_input: str) -> str:
        """Run the agent on a user request"""
        console.print(Panel(
            f"[bold cyan]{user_input}[/bold cyan]",
            title="Question",
            border_style="cyan"
        ))
        
        iteration = 0
        final_answer = None
        
        while iteration < self.max_iterations and not final_answer:
            iteration += 1
            console.print(f"\n[bold magenta]Iteration {iteration}/{self.max_iterations}[/bold magenta]")
            
            # Build simple prompt
            prompt = get_simple_prompt(
                user_input=user_input,
                tools_list=self.tools.get_tool_descriptions()
            )
            
            # Get AI response
            ai_response = self._call_ollama(prompt)
            
            # Parse response
            try:
                # Extract JSON
                if '{' in ai_response and '}' in ai_response:
                    json_start = ai_response.index('{')
                    json_end = ai_response.rindex('}') + 1
                    response_data = json.loads(ai_response[json_start:json_end])
                else:
                    console.print("[yellow]No JSON found, treating as final answer[/yellow]")
                    final_answer = ai_response
                    break
                
                # Show thought
                thought = response_data.get('thought', 'No thought')
                console.print(f"[dim]💭 {thought}[/dim]")
                
                # Check for final answer
                if 'final_answer' in response_data:
                    final_answer = response_data['final_answer']
                    break
                
                # Execute action
                action = response_data.get('action')
                action_input = response_data.get('action_input', {})
                
                if not action:
                    console.print("[red]No action specified[/red]")
                    break
                
                # Auto-approve in training mode
                console.print(f"[cyan]🔧 Executing:[/cyan] {action}")
                console.print(f"[dim]Parameters: {action_input}[/dim]")
                
                # Execute
                result = self.tools.execute(action, action_input)
                
                # Show result
                result_str = str(result)[:500]  # Truncate
                console.print(f"[green]✓ Result:[/green] {result_str}")
                
                # Check for errors
                if "Error:" in result_str or "not found" in result_str:
                    console.print("[yellow]Tool error detected, stopping[/yellow]")
                    final_answer = f"Error: {result_str}"
                    break
                
                # If we got a good result, that's probably the answer
                if iteration >= 2:  # After 2 iterations, try to conclude
                    final_answer = f"Based on the tool execution:\n\n{result_str}"
                    break
            
            except json.JSONDecodeError as e:
                console.print(f"[red]JSON parse error: {e}[/red]")
                console.print(f"[dim]Response was: {ai_response[:200]}...[/dim]")
                final_answer = "Error: Could not parse AI response"
                break
            
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                final_answer = f"Error: {str(e)}"
                break
        
        # Display final answer
        if final_answer:
            console.print(Panel(
                Markdown(final_answer),
                title="Answer",
                border_style="green"
            ))
        else:
            final_answer = "Maximum iterations reached"
            console.print(Panel(
                final_answer,
                title="Answer",
                border_style="red"
            ))
        
        return final_answer


def main():
    """Test the simple agent"""
    console.print("[bold cyan]Simple Agent Test[/bold cyan]\n")
    
    agent = SimpleAgent()
    
    test_questions = [
        "ما هو نظام التشغيل؟",
        "اعرض محتويات المجلد الحالي",
        "احسب متوسط: 10, 20, 30"
    ]
    
    for q in test_questions:
        console.print(f"\n[bold]{'='*70}[/bold]")
        agent.run(q)
        console.print(f"[bold]{'='*70}[/bold]\n")


if __name__ == "__main__":
    main()
