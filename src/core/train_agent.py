import sys
import time
from rich.console import Console
from rich.panel import Panel
from src.agents.agent import Agent

console = Console()

SCENARIOS = [
    {
        "name": "System Discovery",
        "prompt": "What OS and version is this server running?"
    },
    {
        "name": "Service Intelligence",
        "prompt": "Check if nginx is installed and running. If not installed, tell me."
    },
    {
        "name": "File Operations",
        "prompt": "Create a file named 'test_agent.txt' in the current directory with the text 'Training in progress'."
    },
    {
        "name": "Web Research",
        "prompt": "Search for the release date of Python 3.12."
    },
    {
        "name": "Data Analysis",
        "prompt": "Calculate the average of these numbers: 10, 20, 30, 40, 50."
    },
    {
        "name": "Security Audit",
        "prompt": "Scan open ports on localhost."
    },
    {
        "name": "Complex Logic (File Search)",
        "prompt": "Find all Python files in the current directory."
    },
    {
        "name": "Error Handling",
        "prompt": "Read the file 'non_existent_ghost_file.txt'."
    },
    {
        "name": "Package Management",
        "prompt": "Check if 'git' is installed."
    },
    {
        "name": "Multi-Step Reasoning",
        "prompt": "Create a folder 'logs', write a file 'error.log' inside it, and then read it back."
    }
]

def run_training():
    console.print(Panel.fit("[bold green]🚀 Starting Agent Training Run[/bold green]", title="Training Harness"))
    
    try:
        # Initialize agent in auto-approve mode
        agent = Agent(auto_approve=True)
    except Exception as e:
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        return

    results = []

    for i, scenario in enumerate(SCENARIOS, 1):
        console.print(f"\n[bold magenta]════════════════════════════════════════════════════════════[/bold magenta]")
        console.print(f"[bold magenta]🧪 Scenario {i}/{len(SCENARIOS)}: {scenario['name']}[/bold magenta]")
        console.print(f"[dim]Prompt: {scenario['prompt']}[/dim]")
        console.print(f"[bold magenta]════════════════════════════════════════════════════════════[/bold magenta]\n")
        
        start_time = time.time()
        try:
            response = agent.run(scenario['prompt'])
            duration = time.time() - start_time
            
            if "Error" in str(response) or "Maximum iterations" in str(response):
                status = "❌ FAILED"
                style = "red"
            else:
                status = "✅ PASSED"
                style = "green"
                
            results.append({
                "scenario": scenario['name'],
                "status": status,
                "duration": f"{duration:.2f}s",
                "response": str(response)[:100] + "..."
            })
            
            console.print(f"\n[{style}]Result: {status} ({duration:.2f}s)[/{style}]")
            
        except Exception as e:
            console.print(f"[red]CRITICAL ERROR: {e}[/red]")
            results.append({
                "scenario": scenario['name'],
                "status": "💥 CRASHED",
                "duration": "0s",
                "response": str(e)
            })
            
        # Small pause between scenarios
        time.sleep(2)

    # Print Summary
    console.print("\n[bold]📊 Training Summary[/bold]")
    console.print("────────────────────────────────────────")
    
    # Save results to log file
    with open("training_report.txt", "w", encoding="utf-8") as f:
        f.write("AGENT TRAINING REPORT\n")
        f.write("=====================\n\n")
        for res in results:
            style = "green" if "PASSED" in res['status'] else "red"
            console.print(f"[{style}]{res['status']} - {res['scenario']} ({res['duration']})[/{style}]")
            f.write(f"{res['status']} - {res['scenario']} ({res['duration']})\n")
            f.write(f"Response: {res['response']}\n\n")
            
    console.print("────────────────────────────────────────")
    console.print("\n[blue]Full report saved to training_report.txt[/blue]")
    console.print("[yellow]Press Enter to close this window...[/yellow]")
    input()

if __name__ == "__main__":
    run_training()
