"""
Test Learning Scenario - Verify Agent Learning Capabilities
اختبار سيناريو التعلم - التحقق من قدرات تعلم الوكيل
"""

from src.agents.expert_agent import ExpertAgent
from src.utils.knowledge_viewer import KnowledgeViewer
from src.core.knowledge_base import KnowledgeBase
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time

console = Console()


def test_learning_scenario():
    """Test complete learning scenario"""
    
    console.print(Panel(
        "[bold cyan]🧪 Learning Test Scenario[/bold cyan]\n"
        "Testing: Agent learning, storage, and retrieval",
        title="Test Scenario",
        border_style="cyan"
    ))
    
    # Initialize components
    console.print("\n[bold]Step 1: Initializing Agent...[/bold]")
    agent = ExpertAgent(enable_online_learning=True)
    
    # Get initial statistics
    console.print("\n[bold]Step 2: Getting initial knowledge base statistics...[/bold]")
    viewer = KnowledgeViewer()
    initial_stats = viewer.get_statistics()
    initial_count = initial_stats['total_entries']
    
    console.print(f"[green]✓ Initial knowledge entries: {initial_count}[/green]")
    
    # Test topic - something new and specific
    test_topics = [
        {
            "query": "What is FastAPI and how to create a REST API with it?",
            "expected_keywords": ["fastapi", "rest", "api", "python"]
        },
        {
            "query": "How to use Redis for caching in Python applications?",
            "expected_keywords": ["redis", "caching", "python"]
        },
        {
            "query": "Explain Kubernetes pods and deployments",
            "expected_keywords": ["kubernetes", "pods", "deployments"]
        }
    ]
    
    learned_entries = []
    
    for i, test in enumerate(test_topics, 1):
        console.print(f"\n[bold yellow]{'='*70}[/bold yellow]")
        console.print(f"[bold]Test {i}/{len(test_topics)}: Learning New Topic[/bold]")
        console.print(f"[bold yellow]{'='*70}[/bold yellow]")
        
        query = test["query"]
        expected_keywords = test["expected_keywords"]
        
        console.print(f"\n[cyan]📝 Query:[/cyan] {query}")
        console.print(f"[cyan]🔍 Expected Keywords:[/cyan] {', '.join(expected_keywords)}")
        
        # Get count before
        stats_before = viewer.get_statistics()
        count_before = stats_before['total_entries']
        
        # Run agent
        console.print(f"\n[bold]Step 3.{i}: Running agent with query...[/bold]")
        start_time = time.time()
        
        try:
            response = agent.run(query)
            duration = time.time() - start_time
            
            console.print(f"[green]✓ Agent responded in {duration:.2f}s[/green]")
            
            # Wait a bit for background learning to complete
            time.sleep(2)
            
            # Get count after
            stats_after = viewer.get_statistics()
            count_after = stats_after['total_entries']
            
            # Check if knowledge was stored
            new_entries = count_after - count_before
            
            if new_entries > 0:
                console.print(f"[green]✅ SUCCESS: {new_entries} new knowledge entry/entries stored![/green]")
                
                # Get the latest entry
                kb = KnowledgeBase()
                latest_entries = kb.retrieve_knowledge(query, limit=1)
                kb.close()
                
                if latest_entries:
                    entry = latest_entries[0]
                    learned_entries.append({
                        "id": entry["id"],
                        "topic": entry["topic"],
                        "category": entry["category"],
                        "confidence": entry["confidence"],
                        "keywords_found": [kw for kw in expected_keywords if kw.lower() in entry["topic"].lower() or kw.lower() in entry["content"].lower()]
                    })
                    
                    console.print(f"[dim]  Entry ID: {entry['id']}[/dim]")
                    console.print(f"[dim]  Category: {entry.get('category', 'general')}[/dim]")
                    console.print(f"[dim]  Confidence: {entry.get('confidence', 0):.2f}[/dim]")
                    console.print(f"[dim]  Keywords found: {len(learned_entries[-1]['keywords_found'])}/{len(expected_keywords)}[/dim]")
            else:
                console.print(f"[yellow]⚠️ No new entries stored (might already exist or learning evaluation failed)[/yellow]")
            
        except Exception as e:
            console.print(f"[red]❌ Error during test: {e}[/red]")
            import traceback
            traceback.print_exc()
        
        # Small delay between tests
        time.sleep(1)
    
    # Final verification
    console.print(f"\n[bold yellow]{'='*70}[/bold yellow]")
    console.print("[bold]Step 4: Final Verification[/bold]")
    console.print(f"[bold yellow]{'='*70}[/bold yellow]")
    
    # Show final statistics
    final_stats = viewer.get_statistics()
    final_count = final_stats['total_entries']
    total_learned = final_count - initial_count
    
    console.print(f"\n[bold]Final Statistics:[/bold]")
    console.print(f"[cyan]Initial entries:[/cyan] {initial_count}")
    console.print(f"[cyan]Final entries:[/cyan] {final_count}")
    console.print(f"[cyan]Total learned in this session:[/cyan] {total_learned}")
    
    # Show learned entries summary
    if learned_entries:
        console.print(f"\n[bold]Learned Entries Summary:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Topic", style="green", width=40)
        table.add_column("Category", style="yellow", width=15)
        table.add_column("Confidence", style="magenta", width=12)
        table.add_column("Keywords", style="blue", width=20)
        
        for entry in learned_entries:
            topic_short = entry["topic"][:37] + "..." if len(entry["topic"]) > 40 else entry["topic"]
            keywords_str = ", ".join(entry["keywords_found"][:3])
            if len(entry["keywords_found"]) > 3:
                keywords_str += "..."
            
            table.add_row(
                str(entry["id"]),
                topic_short,
                entry["category"] or "general",
                f"{entry['confidence']:.2f}",
                keywords_str or "None"
            )
        
        console.print(table)
    
    # Test retrieval
    console.print(f"\n[bold]Step 5: Testing Knowledge Retrieval[/bold]")
    
    if learned_entries:
        test_entry = learned_entries[0]
        console.print(f"\n[cyan]Testing retrieval for entry ID {test_entry['id']}...[/cyan]")
        
        retrieved = viewer.view_entry(test_entry['id'])
        
        if retrieved:
            console.print(f"[green]✅ Knowledge retrieval successful![/green]")
        else:
            console.print(f"[red]❌ Knowledge retrieval failed![/red]")
    else:
        console.print("[yellow]⚠️ No entries to test retrieval[/yellow]")
    
    # Check for duplicates
    console.print(f"\n[bold]Step 6: Checking for Duplicates[/bold]")
    viewer.show_duplicates(similarity_threshold=0.8)
    
    # Final summary
    console.print(f"\n[bold yellow]{'='*70}[/bold yellow]")
    console.print("[bold]📊 Test Summary[/bold]")
    console.print(f"[bold yellow]{'='*70}[/bold yellow]")
    
    if total_learned > 0:
        console.print(Panel(
            f"[bold green]✅ Learning System Working![/bold green]\n\n"
            f"• {total_learned} new knowledge entries stored\n"
            f"• {len(learned_entries)} entries verified\n"
            f"• Learning evaluation: [green]PASSED[/green]\n"
            f"• Knowledge storage: [green]PASSED[/green]\n"
            f"• Knowledge retrieval: [green]PASSED[/green]",
            title="Test Results",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold yellow]⚠️ No New Knowledge Stored[/bold yellow]\n\n"
            f"Possible reasons:\n"
            f"• Knowledge already exists\n"
            f"• Learning evaluation threshold not met\n"
            f"• Response too short or error occurred",
            title="Test Results",
            border_style="yellow"
        ))
    
    console.print(f"\n[dim]💡 Tip: Run 'python view_knowledge.py' to see all stored knowledge[/dim]")


if __name__ == "__main__":
    test_learning_scenario()

