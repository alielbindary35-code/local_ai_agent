"""
Real-time Training Monitor - مراقب التدريب المباشر
يعرض تقدم التدريب في الوقت الفعلي ويكتشف الأخطاء
"""

import time
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime

console = Console()


def get_latest_log_file():
    """Get the most recent training log file"""
    log_dir = Path("logs")
    if not log_dir.exists():
        return None
    
    log_files = list(log_dir.glob("automated_training_*.txt"))
    if not log_files:
        return None
    
    # Get the most recent file
    latest = max(log_files, key=lambda p: p.stat().st_mtime)
    return latest


def parse_log_file(log_file):
    """Parse log file and extract statistics"""
    if not log_file or not log_file.exists():
        return None
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Count questions
        questions = content.count("Question ")
        
        # Count phases
        phases_found = set()
        for line in content.split("\n"):
            if "Phase:" in line:
                phase = line.split("Phase:")[1].strip()
                phases_found.add(phase)
        
        # Get last few lines
        lines = content.split("\n")
        recent_lines = [l for l in lines[-30:] if l.strip()]
        
        # Detect errors
        errors = []
        for line in lines:
            if "ERROR" in line or "Error:" in line or "Exception:" in line:
                errors.append(line.strip())
        
        return {
            "questions_processed": questions,
            "phases_found": len(phases_found),
            "recent_lines": recent_lines,
            "errors": errors,
            "total_lines": len(lines)
        }
    except Exception as e:
        return {"error": str(e)}


def create_monitor_display(stats, log_file):
    """Create rich display for monitoring"""
    layout = Layout()
    
    # Header
    header = Panel(
        "[bold cyan]🔍 Real-time Training Monitor[/bold cyan]\n"
        f"[dim]Monitoring: {log_file.name if log_file else 'No log file'}[/dim]",
        style="cyan"
    )
    
    if not stats:
        return Panel("[yellow]Waiting for training to start...[/yellow]", title="Monitor")
    
    if "error" in stats:
        return Panel(f"[red]Error reading log: {stats['error']}[/red]", title="Monitor")
    
    # Statistics table
    table = Table(title="Training Progress", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Questions Processed", str(stats["questions_processed"]))
    table.add_row("Phases Completed", str(stats["phases_found"]))
    table.add_row("Total Log Lines", str(stats["total_lines"]))
    table.add_row("Errors Detected", f"[red]{len(stats['errors'])}[/red]" if stats['errors'] else "[green]0[/green]")
    
    # Recent activity
    recent_text = "\n".join(stats["recent_lines"][-10:])
    recent_panel = Panel(
        recent_text if recent_text else "[dim]No recent activity[/dim]",
        title="Recent Activity",
        border_style="blue"
    )
    
    # Errors panel
    if stats["errors"]:
        errors_text = "\n".join(stats["errors"][-5:])
        errors_panel = Panel(
            errors_text,
            title="⚠️ Recent Errors",
            border_style="red"
        )
    else:
        errors_panel = Panel(
            "[green]✅ No errors detected![/green]",
            title="Errors",
            border_style="green"
        )
    
    # Combine panels
    from rich.columns import Columns
    
    display = Layout()
    display.split_column(
        Layout(header, size=3),
        Layout(table, size=8),
        Layout(recent_panel, size=15),
        Layout(errors_panel, size=8)
    )
    
    return display


def monitor_training(duration_seconds=120):
    """Monitor training for specified duration"""
    console.print(Panel.fit(
        "[bold green]🔍 Starting Real-time Monitor[/bold green]\n"
        f"[cyan]Duration:[/cyan] {duration_seconds} seconds\n"
        "[dim]Press Ctrl+C to stop[/dim]",
        title="Monitor"
    ))
    
    start_time = time.time()
    
    try:
        with Live(console=console, refresh_per_second=2) as live:
            while time.time() - start_time < duration_seconds:
                log_file = get_latest_log_file()
                stats = parse_log_file(log_file)
                display = create_monitor_display(stats, log_file)
                
                live.update(display)
                time.sleep(1)
        
        console.print("\n[green]✅ Monitoring completed[/green]")
        
        # Final summary
        if stats and "errors" in stats:
            console.print(f"\n[bold]Final Summary:[/bold]")
            console.print(f"  Questions: {stats['questions_processed']}")
            console.print(f"  Errors: {len(stats['errors'])}")
            
            if stats["errors"]:
                console.print("\n[bold red]Errors found:[/bold red]")
                for error in stats["errors"][-10:]:
                    console.print(f"  • {error}")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped by user[/yellow]")


def tail_log(lines=50):
    """Show last N lines of the latest log"""
    log_file = get_latest_log_file()
    
    if not log_file:
        console.print("[yellow]No log files found[/yellow]")
        return
    
    console.print(f"[cyan]Reading:[/cyan] {log_file}\n")
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.readlines()
        
        recent = content[-lines:]
        for line in recent:
            console.print(line.rstrip())
    
    except Exception as e:
        console.print(f"[red]Error reading log: {e}[/red]")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "tail":
            lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            tail_log(lines)
        elif sys.argv[1] == "monitor":
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 120
            monitor_training(duration)
        else:
            console.print("[yellow]Usage: python monitor_training.py [monitor|tail] [duration/lines][/yellow]")
    else:
        # Default: monitor for 2 minutes
        monitor_training(120)


if __name__ == "__main__":
    main()
