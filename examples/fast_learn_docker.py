"""
Fast Learning Example - Learn Docker in Minutes
===============================================

This example shows how to use the fast learning module to quickly
acquire knowledge from multiple online sources.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.fast_learning import FastLearning
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def fast_learn_docker():
    """Fast learn Docker using multiple online sources"""
    
    console.print(Panel(
        "[bold cyan]🚀 Fast Learning: Docker[/bold cyan]\n"
        "[dim]Using multiple online sources for accelerated learning[/dim]",
        title="Fast Learning Module",
        border_style="cyan"
    ))
    
    # Initialize fast learner
    fast_learner = FastLearning()
    
    # Topics to learn
    topics = [
        "containers",
        "images", 
        "docker-compose",
        "volumes",
        "networking"
    ]
    
    console.print(f"\n[yellow]📚 Topics:[/yellow] {', '.join(topics)}\n")
    
    # Fast learn!
    results = fast_learner.learn_fast("Docker", topics)
    
    # Display results
    console.print("\n[green]✅ Learning Complete![/green]\n")
    
    # Create summary table
    table = Table(title="📊 Knowledge Sources Found", show_header=True)
    table.add_column("Source Type", style="cyan")
    table.add_column("Count", style="green", justify="right")
    table.add_column("Examples", style="yellow")
    
    for source_type, items in results["sources"].items():
        if items:
            examples = ", ".join([
                item.get("title", item.get("name", ""))[:30] + "..."
                for item in items[:2]
            ])
            table.add_row(source_type.upper(), str(len(items)), examples)
    
    console.print(table)
    
    # Show summary
    console.print("\n[bold]📝 Summary:[/bold]\n")
    console.print(Panel(results["summary"], border_style="green"))
    
    # Save to knowledge base
    console.print("\n[yellow]💾 Saving to knowledge base...[/yellow]")
    save_result = fast_learner.save_to_knowledge_base(results)
    console.print(f"[green]{save_result}[/green]\n")
    
    # Show comparison
    console.print(Panel(
        "[bold green]⚡ Speed Comparison:[/bold green]\n\n"
        "[dim]Traditional Learning:[/dim]\n"
        "• One model response at a time\n"
        "• Limited to model's knowledge cutoff\n"
        "• ~2-5 minutes per topic\n\n"
        "[bold cyan]Fast Learning:[/bold cyan]\n"
        "• Multiple sources simultaneously\n"
        "• Real-time web data\n"
        "• GitHub examples + official docs\n"
        "• ~30 seconds total for all topics ⚡",
        title="🚀 Performance",
        border_style="cyan"
    ))


if __name__ == "__main__":
    fast_learn_docker()
