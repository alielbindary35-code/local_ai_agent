"""
Learn Any Technology
====================

Interactive script to teach your agent any new technology using Fast Learning.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.expert_agent import ExpertAgent
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def main():
    agent = ExpertAgent()
    
    console.print(Panel(
        "[bold cyan]🎓 Teach Your Agent New Skills[/bold cyan]\n"
        "[dim]This script uses the Fast Learning module to quickly acquire knowledge.[/dim]",
        title="Agent Learning Studio",
        border_style="cyan"
    ))
    
    # Get user input
    technology = Prompt.ask("\n[yellow]What technology do you want the agent to learn?[/yellow]", default="Flutter")
    
    console.print(f"\n[dim]Enter specific topics to focus on (comma separated)[/dim]")
    console.print(f"[dim]Example: widgets, state management, api calls[/dim]")
    topics_str = Prompt.ask("[yellow]Topics[/yellow]", default="overview, best practices")
    
    # Construct the "Perfect Template" prompt
    prompt = f"""
    I want you to learn a new technology: {technology}.
    
    Please use the 'learn_new_technology' tool to learn about these specific topics:
    {topics_str}
    
    After learning, please provide a brief summary of what you found.
    """
    
    console.print(f"\n[bold green]🚀 Starting learning process for {technology}...[/bold green]")
    agent.run(prompt)

if __name__ == "__main__":
    from rich.panel import Panel
    main()
