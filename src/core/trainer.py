import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from src.agents.agent import Agent

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from src.agents.agent import Agent
from datetime import datetime
from pathlib import Path

console = Console()

def log_session(message: str):
    """Log message to file."""
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"training_session_{timestamp}.txt"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
    except Exception as e:
        console.print(f"[red]Logging error: {e}[/red]")

def run_interactive_training():
    console.print(Panel.fit("[bold green]🏋️‍♂️ Interactive Agent Trainer[/bold green]", title="Trainer Module"))
    
    try:
        # Initialize agent
        # We don't use auto_approve here because we want the user to verify the final answer,
        # but we might want the agent to be autonomous during the process. 
        # For now, let's stick to default behavior but maybe we can suppress some internal prompts if needed.
        agent = Agent(auto_approve=False) 
    except Exception as e:
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        return

    while True:
        console.print("\n[bold cyan]════════════════════════════════════════════════════════════[/bold cyan]")
        question = Prompt.ask("[bold yellow]Enter a training question (or 'q' to quit)[/bold yellow]")
        
        if question.lower() in ['q', 'quit', 'exit']:
            break
            
        if not question.strip():
            continue

        console.print(f"\n[dim]Training on: {question}[/dim]\n")
        log_session(f"Question: {question}")
        
        # Run the agent
        
        # Run the agent
        start_time = time.time()
        try:
            # We want to capture the final answer. 
            # The agent.run() method returns the final answer string.
            response = agent.run(question)
            duration = time.time() - start_time
            
            console.print(f"\n[bold blue]Agent Answer ({duration:.2f}s):[/bold blue]")
            console.print(Panel(response, border_style="blue"))
            log_session(f"Answer: {response}")
            
            # Interactive Feedback Loop
            
            # Interactive Feedback Loop
            if Confirm.ask("[bold green]Is this answer correct?[/bold green]"):
                # Save to memory
                try:
                    agent.memory.save_solution(question, response, rating=5)
                    console.print("[bold green]✅ Solution saved to memory![/bold green]")
                    console.print("[dim]The agent will use this knowledge next time.[/dim]")
                    log_session("Feedback: Correct (Saved)")
                except Exception as e:
                    console.print(f"[red]Error saving to memory: {e}[/red]")
            else:
                console.print("[bold red]❌ Answer marked as incorrect.[/bold red]")
                if Confirm.ask("Do you want to provide the correct answer for the agent to learn?"):
                    correct_answer = Prompt.ask("Enter the correct answer")
                    try:
                        agent.memory.save_solution(question, correct_answer, rating=5)
                        console.print("[bold green]✅ Correct solution saved to memory![/bold green]")
                        log_session(f"Feedback: Incorrect. Provided correction: {correct_answer}")
                    except Exception as e:
                        console.print(f"[red]Error saving to memory: {e}[/red]")
                else:
                    console.print("[dim]Skipping save. You can try asking again or rephrasing.[/dim]")

        except Exception as e:
            console.print(f"[red]Error during execution: {e}[/red]")

    console.print("\n[bold green]Training session finished. Goodbye! 👋[/bold green]")

if __name__ == "__main__":
    run_interactive_training()
