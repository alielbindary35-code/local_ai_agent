"""
Knowledge Base Viewer
View and manage stored knowledge
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from src.core.paths import get_memory_db_file

console = Console()


class KnowledgeViewer:
    """View and analyze stored knowledge"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = get_memory_db_file()
        self.db_path = str(db_path)
    
    def view_all_knowledge(self, limit: int = 20, category: Optional[str] = None) -> None:
        """View all stored knowledge entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT id, topic, content, category, tags, source, confidence, usage_count, created_at
                FROM knowledge_entries
                WHERE category = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (category, limit))
        else:
            cursor.execute("""
                SELECT id, topic, content, category, tags, source, confidence, usage_count, created_at
                FROM knowledge_entries
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            console.print("[yellow]No knowledge entries found.[/yellow]")
            return
        
        # Create table
        table = Table(title=f"📚 Knowledge Base Entries ({len(rows)} shown)")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Topic", style="green", width=40)
        table.add_column("Category", style="yellow", width=15)
        table.add_column("Source", style="blue", width=15)
        table.add_column("Confidence", style="magenta", width=10)
        table.add_column("Used", style="white", width=6)
        table.add_column("Created", style="dim", width=12)
        
        for row in rows:
            entry_id, topic, content, cat, tags, source, conf, usage, created = row
            topic_short = topic[:37] + "..." if len(topic) > 40 else topic
            created_short = created[:10] if created else "N/A"
            conf_str = f"{conf:.2f}" if conf else "N/A"
            
            table.add_row(
                str(entry_id),
                topic_short,
                cat or "general",
                source or "unknown",
                conf_str,
                str(usage),
                created_short
            )
        
        console.print(table)
    
    def view_entry(self, entry_id: int) -> None:
        """View detailed information about a specific entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, content, category, tags, source, confidence, usage_count, created_at, updated_at
            FROM knowledge_entries
            WHERE id = ?
        """, (entry_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            console.print(f"[red]Entry {entry_id} not found.[/red]")
            return
        
        entry_id, topic, content, cat, tags, source, conf, usage, created, updated = row
        
        # Display entry
        console.print(Panel(
            f"[bold cyan]Entry ID:[/bold cyan] {entry_id}\n"
            f"[bold green]Topic:[/bold green] {topic}\n"
            f"[bold yellow]Category:[/bold yellow] {cat or 'general'}\n"
            f"[bold blue]Source:[/bold blue] {source or 'unknown'}\n"
            f"[bold magenta]Confidence:[/bold magenta] {conf:.2f}\n"
            f"[bold white]Usage Count:[/bold white] {usage}\n"
            f"[bold dim]Created:[/bold dim] {created}\n"
            f"[bold dim]Updated:[/bold dim] {updated or 'N/A'}\n"
            f"[bold dim]Tags:[/bold dim] {tags or 'None'}",
            title="📖 Knowledge Entry Details",
            border_style="cyan"
        ))
        
        # Display content
        console.print("\n[bold]Content:[/bold]")
        console.print(Panel(
            Markdown(content[:2000] + ("..." if len(content) > 2000 else "")),
            border_style="green"
        ))
    
    def find_duplicates(self, similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """Find duplicate or similar knowledge entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all entries
        cursor.execute("""
            SELECT id, topic, content, category
            FROM knowledge_entries
            ORDER BY created_at DESC
        """)
        
        all_entries = cursor.fetchall()
        conn.close()
        
        duplicates = []
        checked_pairs = set()
        
        from difflib import SequenceMatcher
        
        for i, entry1 in enumerate(all_entries):
            id1, topic1, content1, cat1 = entry1
            
            for j, entry2 in enumerate(all_entries[i+1:], start=i+1):
                id2, topic2, content2, cat2 = entry2
                
                # Skip if already checked
                pair = tuple(sorted([id1, id2]))
                if pair in checked_pairs:
                    continue
                checked_pairs.add(pair)
                
                # Calculate similarity
                topic_sim = SequenceMatcher(None, topic1.lower(), topic2.lower()).ratio()
                content_sim = SequenceMatcher(None, content1[:500].lower(), content2[:500].lower()).ratio()
                
                # Combined similarity
                similarity = (topic_sim * 0.6 + content_sim * 0.4)
                
                if similarity >= similarity_threshold:
                    duplicates.append({
                        "entry1_id": id1,
                        "entry1_topic": topic1,
                        "entry2_id": id2,
                        "entry2_topic": topic2,
                        "similarity": similarity,
                        "category1": cat1,
                        "category2": cat2
                    })
        
        return duplicates
    
    def show_duplicates(self, similarity_threshold: float = 0.8) -> None:
        """Display duplicate entries"""
        duplicates = self.find_duplicates(similarity_threshold)
        
        if not duplicates:
            console.print("[green]✅ No duplicate entries found![/green]")
            return
        
        console.print(f"[yellow]⚠️ Found {len(duplicates)} potential duplicate(s):[/yellow]\n")
        
        table = Table(title="🔄 Duplicate Entries")
        table.add_column("Entry 1", style="cyan", width=30)
        table.add_column("Entry 2", style="green", width=30)
        table.add_column("Similarity", style="yellow", width=12)
        table.add_column("Category", style="blue", width=15)
        
        for dup in duplicates:
            sim_percent = f"{dup['similarity']*100:.1f}%"
            cat = dup['category1'] or dup['category2'] or "general"
            
            table.add_row(
                f"ID {dup['entry1_id']}: {dup['entry1_topic'][:27]}...",
                f"ID {dup['entry2_id']}: {dup['entry2_topic'][:27]}...",
                sim_percent,
                cat
            )
        
        console.print(table)
        console.print(f"\n[dim]💡 Tip: You can delete duplicate entries using option 6 in the menu[/dim]")
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete a knowledge entry"""
        from src.core.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        success = kb.delete_entry(entry_id)
        kb.close()
        
        if success:
            console.print(f"[green]✅ Entry {entry_id} deleted successfully[/green]")
        else:
            console.print(f"[red]❌ Failed to delete entry {entry_id}[/red]")
        
        return success
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total entries
        cursor.execute("SELECT COUNT(*) FROM knowledge_entries")
        stats['total_entries'] = cursor.fetchone()[0]
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM knowledge_entries 
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """)
        stats['by_category'] = dict(cursor.fetchall())
        
        # By source
        cursor.execute("""
            SELECT source, COUNT(*) 
            FROM knowledge_entries 
            GROUP BY source
            ORDER BY COUNT(*) DESC
        """)
        stats['by_source'] = dict(cursor.fetchall())
        
        # Most used
        cursor.execute("""
            SELECT id, topic, usage_count 
            FROM knowledge_entries 
            ORDER BY usage_count DESC 
            LIMIT 5
        """)
        stats['most_used'] = cursor.fetchall()
        
        # Average confidence
        cursor.execute("SELECT AVG(confidence) FROM knowledge_entries")
        avg_conf = cursor.fetchone()[0]
        stats['average_confidence'] = round(avg_conf, 2) if avg_conf else 0
        
        # Learning history count
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        stats['total_learned'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def show_statistics(self) -> None:
        """Display knowledge base statistics"""
        stats = self.get_statistics()
        
        console.print(Panel(
            f"[bold cyan]Total Entries:[/bold cyan] {stats['total_entries']}\n"
            f"[bold cyan]Total Learning Events:[/bold cyan] {stats['total_learned']}\n"
            f"[bold cyan]Average Confidence:[/bold cyan] {stats['average_confidence']}",
            title="📊 Knowledge Base Statistics",
            border_style="cyan"
        ))
        
        # By category
        if stats['by_category']:
            console.print("\n[bold]By Category:[/bold]")
            cat_table = Table(show_header=True, header_style="bold magenta")
            cat_table.add_column("Category", style="cyan")
            cat_table.add_column("Count", style="green")
            
            for cat, count in stats['by_category'].items():
                cat_table.add_row(cat or "general", str(count))
            
            console.print(cat_table)
        
        # By source
        if stats['by_source']:
            console.print("\n[bold]By Source:[/bold]")
            source_table = Table(show_header=True, header_style="bold magenta")
            source_table.add_column("Source", style="cyan")
            source_table.add_column("Count", style="green")
            
            for source, count in stats['by_source'].items():
                source_table.add_row(source or "unknown", str(count))
            
            console.print(source_table)
        
        # Most used
        if stats['most_used']:
            console.print("\n[bold]Most Used Entries:[/bold]")
            used_table = Table(show_header=True, header_style="bold magenta")
            used_table.add_column("ID", style="cyan")
            used_table.add_column("Topic", style="green", width=50)
            used_table.add_column("Usage Count", style="yellow")
            
            for entry_id, topic, usage in stats['most_used']:
                topic_short = topic[:47] + "..." if len(topic) > 50 else topic
                used_table.add_row(str(entry_id), topic_short, str(usage))
            
            console.print(used_table)


def main():
    """Interactive knowledge viewer"""
    viewer = KnowledgeViewer()
    
    console.print("[bold cyan]📚 Knowledge Base Viewer[/bold cyan]\n")
    
    while True:
        console.print("\n[bold]Options:[/bold]")
        console.print("1. View all entries")
        console.print("2. View entry by ID")
        console.print("3. Show statistics")
        console.print("4. Find duplicates")
        console.print("5. Delete entry")
        console.print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            limit = input("How many entries to show? (default: 20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            viewer.view_all_knowledge(limit=limit)
        
        elif choice == "2":
            entry_id = input("Enter entry ID: ").strip()
            if entry_id.isdigit():
                viewer.view_entry(int(entry_id))
            else:
                console.print("[red]Invalid entry ID[/red]")
        
        elif choice == "3":
            viewer.show_statistics()
        
        elif choice == "4":
            threshold = input("Similarity threshold (0.0-1.0, default: 0.8): ").strip()
            threshold = float(threshold) if threshold.replace('.', '').isdigit() else 0.8
            viewer.show_duplicates(threshold)
        
        elif choice == "5":
            entry_id = input("Enter entry ID to delete: ").strip()
            if entry_id.isdigit():
                confirm = input(f"Are you sure you want to delete entry {entry_id}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    viewer.delete_entry(int(entry_id))
                else:
                    console.print("[yellow]Deletion cancelled[/yellow]")
            else:
                console.print("[red]Invalid entry ID[/red]")
        
        elif choice == "6":
            console.print("[green]Goodbye![/green]")
            break
        
        else:
            console.print("[red]Invalid choice[/red]")


if __name__ == "__main__":
    main()

