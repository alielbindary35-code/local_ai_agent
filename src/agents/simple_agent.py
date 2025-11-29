"""
Simple Agent
Uses simplified prompts and faster iterations
"""

import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from src.tools.tools import Tools
from src.core.memory import Memory
from src.core.knowledge_base import KnowledgeBase
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
        max_iterations: int = 5,
        auto_approve: bool = True
    ):
        self.ollama_url = ollama_url
        self.model = model
        self.max_iterations = max_iterations
        self.auto_approve = auto_approve
        
        self.tools = Tools()
        self.memory = Memory()
        self.knowledge_base = KnowledgeBase()
        self.conversation_history = []
        
        # Initialize basic knowledge if needed
        self._ensure_basic_knowledge()
        
        console.print(Panel.fit(
            f"[bold green]🤖 Simple Agent Ready[/bold green]\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Max Iterations:[/cyan] {max_iterations}",
            title="Simple Agent"
        ))
    
    def _ensure_basic_knowledge(self):
        """Ensure basic knowledge entries exist in the knowledge base"""
        try:
            # Check if Python knowledge exists
            python_knowledge = self.knowledge_base.retrieve_knowledge(
                query="Python programming language",
                limit=1
            )
            
            if not python_knowledge or python_knowledge[0]["relevance_score"] < 0.7:
                # Add basic Python knowledge
                basic_python_info = """
# Python Programming Language

Python is a high-level, interpreted programming language known for its simplicity and readability.

## Key Features:
- **Easy to Learn**: Python has a simple syntax that is easy to read and write
- **Versatile**: Used for web development, data science, AI, automation, and more
- **Large Community**: Extensive libraries and frameworks available
- **Cross-platform**: Runs on Windows, macOS, Linux, and more

## Common Use Cases:
- Web development (Django, Flask, FastAPI)
- Data science and analysis (Pandas, NumPy, Matplotlib)
- Machine Learning and AI (TensorFlow, PyTorch, Scikit-learn)
- Automation and scripting
- Game development

## Popular Libraries:
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Django/Flask**: Web frameworks
- **Requests**: HTTP library

Python is widely used in industry and academia for its versatility and ease of use.
"""
                self.knowledge_base.store_knowledge(
                    topic="Python Programming Language Overview",
                    content=basic_python_info,
                    category="programming",
                    tags=["python", "programming", "language"],
                    source="system",
                    confidence=0.9
                )
                console.print("[dim]💡 Basic Python knowledge initialized[/dim]")
        except Exception as e:
            console.print(f"[dim]Note: Could not initialize basic knowledge: {e}[/dim]")
    
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
                            "temperature": 0.1,
                            "num_predict": 512
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
        
        # First, check knowledge base for relevant information
        console.print("\n[yellow]🧠 Checking knowledge base...[/yellow]")
        knowledge_results = self.knowledge_base.retrieve_knowledge(
            query=user_input,
            limit=3
        )
        
        knowledge_context = ""
        if knowledge_results:
            console.print(f"[green]✓ Found {len(knowledge_results)} relevant knowledge entry(ies)[/green]")
            best_match = knowledge_results[0]
            if best_match["relevance_score"] > 0.5:
                knowledge_context = f"\n\nRELEVANT KNOWLEDGE FROM DATABASE:\n{best_match['content'][:1000]}...\n\nUse this knowledge to answer the question. Only search the web if this knowledge is insufficient."
                console.print(f"[dim]💡 Using stored knowledge: {best_match['topic'][:50]}...[/dim]")
        else:
            console.print("[dim]No relevant knowledge found in database[/dim]")
        
        iteration = 0
        final_answer = None
        
        while iteration < self.max_iterations and not final_answer:
            iteration += 1
            console.print(f"\n[bold magenta]Iteration {iteration}/{self.max_iterations}[/bold magenta]")
            
            # Build simple prompt with knowledge context
            user_query = user_input
            if knowledge_context:
                user_query = f"{user_input}\n\n{knowledge_context}"
            
            prompt = get_simple_prompt(
                user_input=user_query,
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
                result_str = str(result)[:500]
                console.print(f"[green]✓ Result:[/green] {result_str}")
                
                # Check for errors
                if "Error:" in result_str or "not found" in result_str:
                    console.print("[yellow]Tool error detected, stopping[/yellow]")
                    final_answer = f"Error: {result_str}"
                    break
                
                # If we got a good result, that's probably the answer
                if iteration >= 2:
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
    """Interactive chat with the agent"""
    console.print(Panel.fit(
        "[bold cyan]🤖 Simple Agent - Interactive Mode[/bold cyan]\n"
        "[yellow]Type your questions and press Enter[/yellow]\n"
        "[dim]Type 'exit' or 'quit' to stop[/dim]",
        border_style="cyan"
    ))
    
    agent = SimpleAgent()
    
    while True:
        try:
            # Get user input
            console.print("\n[bold green]You:[/bold green]", end=" ")
            user_input = input().strip()
            
            # Check for exit
            if user_input.lower() in ['exit', 'quit', 'bye', 'stop']:
                console.print("\n[bold cyan]👋 Goodbye![/bold cyan]")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Run agent
            console.print()
            agent.run(user_input)
            
        except KeyboardInterrupt:
            console.print("\n\n[bold cyan]👋 Goodbye![/bold cyan]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
