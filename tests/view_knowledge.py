"""
Quick script to view knowledge base
سكريبت سريع لعرض قاعدة المعرفة
"""

from src.utils.knowledge_viewer import KnowledgeViewer
from rich.console import Console

console = Console()

def main():
    viewer = KnowledgeViewer()
    
    console.print("[bold cyan]📚 Knowledge Base Viewer[/bold cyan]\n")
    
    # Show statistics first
    viewer.show_statistics()
    
    # Show recent entries
    console.print("\n[bold]Recent Entries:[/bold]")
    viewer.view_all_knowledge(limit=10)
    
    # Check for duplicates
    console.print("\n[bold]Checking for duplicates...[/bold]")
    viewer.show_duplicates()

if __name__ == "__main__":
    main()

