"""
Simple Learning Test - Quick verification
اختبار بسيط للتعلم - تحقق سريع
"""

from src.agents.expert_agent import ExpertAgent
from src.utils.knowledge_viewer import KnowledgeViewer
from src.core.knowledge_base import KnowledgeBase
from rich.console import Console
from rich.panel import Panel
import time

console = Console()


def simple_test():
    """Simple learning test"""
    
    console.print(Panel(
        "[bold cyan]🧪 Simple Learning Test[/bold cyan]",
        title="Quick Test",
        border_style="cyan"
    ))
    
    # Initialize
    console.print("\n[bold]1. Initializing Agent...[/bold]")
    agent = ExpertAgent(enable_online_learning=True)
    
    # Get initial count
    viewer = KnowledgeViewer()
    initial_stats = viewer.get_statistics()
    initial_count = initial_stats['total_entries']
    console.print(f"[green]✓ Initial entries: {initial_count}[/green]")
    
    # Test query - something specific and new
    test_query = "What is GraphQL and how does it differ from REST API?"
    
    console.print(f"\n[bold]2. Testing with query:[/bold]")
    console.print(f"[cyan]{test_query}[/cyan]")
    
    # Run agent
    console.print(f"\n[bold]3. Running agent...[/bold]")
    response = agent.run(test_query)
    
    # Wait for learning to complete
    console.print(f"\n[bold]4. Waiting for learning to complete...[/bold]")
    time.sleep(3)
    
    # Check results
    console.print(f"\n[bold]5. Checking results...[/bold]")
    final_stats = viewer.get_statistics()
    final_count = final_stats['total_entries']
    new_entries = final_count - initial_count
    
    if new_entries > 0:
        console.print(Panel(
            f"[bold green]✅ SUCCESS![/bold green]\n\n"
            f"• {new_entries} new knowledge entry/entries stored\n"
            f"• Learning system is working correctly",
            title="Test Result",
            border_style="green"
        ))
        
        # Show latest entry
        console.print(f"\n[bold]6. Latest stored knowledge:[/bold]")
        kb = KnowledgeBase()
        latest = kb.retrieve_knowledge(test_query, limit=1)
        kb.close()
        
        if latest:
            entry = latest[0]
            console.print(f"[green]✓ Entry ID: {entry['id']}[/green]")
            console.print(f"[green]✓ Topic: {entry['topic'][:60]}...[/green]")
            console.print(f"[green]✓ Confidence: {entry['confidence']:.2f}[/green]")
    else:
        console.print(Panel(
            f"[bold yellow]⚠️ No new entries[/bold yellow]\n\n"
            f"Possible reasons:\n"
            f"• Knowledge already exists\n"
            f"• Response didn't meet learning criteria",
            title="Test Result",
            border_style="yellow"
        ))
    
    console.print(f"\n[dim]💡 Run 'python view_knowledge.py' to see all knowledge[/dim]")


if __name__ == "__main__":
    simple_test()

