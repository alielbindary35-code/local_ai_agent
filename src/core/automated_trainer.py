"""
Automated Training Script
Runs a series of training questions and monitors performance
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from src.agents.agent import Agent

console = Console()

# Training Questions Database
TRAINING_QUESTIONS = {
    "Phase 1: Basics": [
        {
            "question": "What operating system am I working on?",
            "expected_tool": "get_system_info",
            "description": "Basic system info query"
        },
        {
            "question": "Show me the contents of the current directory",
            "expected_tool": "list_dir",
            "description": "List directory contents"
        },
        {
            "question": "Read the contents of README.md file",
            "expected_tool": "read_file",
            "description": "Read file contents"
        },
        {
            "question": "What is the current CPU and RAM usage?",
            "expected_tool": "monitor_resources",
            "description": "Monitor system resources"
        }
    ],
    "Phase 2: Error Handling": [
        {
            "question": "Search for files with .xyz extension in the current directory",
            "expected_tool": "search_files",
            "description": "Search for non-existent file type"
        },
        {
            "question": "Is the Ollama service currently running?",
            "expected_tool": "check_service_status",
            "description": "Check if service is running"
        }
    ],
    "Phase 3: Complex Tasks": [
        {
            "question": "Search the internet for latest Python version 2024",
            "expected_tool": "search_web",
            "description": "Web search task"
        },
        {
            "question": "Calculate the average of numbers: 10, 20, 30, 40, 50",
            "expected_tool": "python_repl",
            "description": "Calculate average using Python"
        },
        {
            "question": "Create a new text file named test_output.txt and write 'Hello from AI Agent' in it",
            "expected_tool": "write_file",
            "description": "Create and write to file"
        }
    ],
    "Phase 4: Intelligence": [
        {
            "question": "What are the Python files in this directory?",
            "expected_tool": "search_files",
            "description": "Search for Python files"
        },
        {
            "question": "Calculate the remaining disk space in gigabytes",
            "expected_tool": "get_system_info",
            "description": "Get disk space"
        }
    ]
}


class TrainingSession:
    """Manages automated training session"""
    
    def __init__(self, auto_approve=True):
        self.agent = Agent(auto_approve=auto_approve)
        self.results = []
        self.start_time = None
        self.log_file = None
        
    def setup_logging(self):
        """Setup logging for this session"""
        from src.core.paths import get_logs_dir
        log_dir = get_logs_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = log_dir / f"automated_training_{timestamp}.txt"
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("🤖 AUTOMATED TRAINING SESSION\n")
            f.write("=" * 70 + "\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
    
    def log(self, message):
        """Log message to file and console"""
        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
    
    def run_question(self, phase, question_data, question_num, total_questions):
        """Run a single training question"""
        question = question_data["question"]
        expected_tool = question_data.get("expected_tool", "unknown")
        description = question_data.get("description", "")
        
        console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
        console.print(f"[bold yellow]Question {question_num}/{total_questions}[/bold yellow]")
        console.print(f"[cyan]Phase:[/cyan] {phase}")
        console.print(f"[cyan]Question:[/cyan] {question}")
        console.print(f"[dim]Expected Tool: {expected_tool}[/dim]")
        console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")
        
        self.log(f"\n{'='*70}")
        self.log(f"Question {question_num}/{total_questions}: {question}")
        self.log(f"Phase: {phase}")
        self.log(f"Expected Tool: {expected_tool}")
        self.log(f"{'='*70}\n")
        
        # Run the agent
        start_time = time.time()
        try:
            response = self.agent.run(question)
            duration = time.time() - start_time
            
            # Log response
            self.log(f"Response ({duration:.2f}s):")
            self.log(response)
            self.log("")
            
            # Record result
            result = {
                "phase": phase,
                "question": question,
                "expected_tool": expected_tool,
                "description": description,
                "response": response,
                "duration": duration,
                "success": "Error:" not in response and "returned status" not in response
            }
            self.results.append(result)
            
            # Display result
            if result["success"]:
                console.print(f"[bold green]✅ Success ({duration:.2f}s)[/bold green]\n")
            else:
                console.print(f"[bold red]❌ Failed ({duration:.2f}s)[/bold red]\n")
            
            # Small delay between questions
            time.sleep(2)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Exception: {str(e)}"
            
            self.log(f"ERROR ({duration:.2f}s): {error_msg}\n")
            console.print(f"[bold red]❌ Error: {error_msg}[/bold red]\n")
            
            result = {
                "phase": phase,
                "question": question,
                "expected_tool": expected_tool,
                "description": description,
                "response": error_msg,
                "duration": duration,
                "success": False
            }
            self.results.append(result)
            return result
    
    def run_all(self):
        """Run all training questions"""
        self.setup_logging()
        self.start_time = time.time()
        
        console.print(Panel.fit(
            "[bold green]🏋️‍♂️ Starting Automated Training Session[/bold green]\n"
            f"[cyan]Total Phases:[/cyan] {len(TRAINING_QUESTIONS)}\n"
            f"[cyan]Total Questions:[/cyan] {sum(len(q) for q in TRAINING_QUESTIONS.values())}\n"
            f"[cyan]Log File:[/cyan] {self.log_file}",
            title="Automated Trainer"
        ))
        
        question_num = 0
        total_questions = sum(len(questions) for questions in TRAINING_QUESTIONS.values())
        
        # Run each phase
        for phase, questions in TRAINING_QUESTIONS.items():
            console.print(f"\n[bold magenta]{'='*70}[/bold magenta]")
            console.print(f"[bold magenta]🎯 {phase}[/bold magenta]")
            console.print(f"[bold magenta]{'='*70}[/bold magenta]")
            
            for question_data in questions:
                question_num += 1
                self.run_question(phase, question_data, question_num, total_questions)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate training report"""
        total_time = time.time() - self.start_time
        total_questions = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        failed = total_questions - successful
        success_rate = (successful / total_questions * 100) if total_questions > 0 else 0
        
        # Console report
        console.print(f"\n\n[bold green]{'='*70}[/bold green]")
        console.print(f"[bold green]📊 TRAINING REPORT[/bold green]")
        console.print(f"[bold green]{'='*70}[/bold green]\n")
        
        # Summary table
        table = Table(title="Training Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Questions", str(total_questions))
        table.add_row("Successful", f"[green]{successful}[/green]")
        table.add_row("Failed", f"[red]{failed}[/red]")
        table.add_row("Success Rate", f"{success_rate:.1f}%")
        table.add_row("Total Time", f"{total_time:.2f}s")
        table.add_row("Avg Time/Question", f"{total_time/total_questions:.2f}s")
        
        console.print(table)
        
        # Phase breakdown
        console.print("\n[bold cyan]Phase Breakdown:[/bold cyan]")
        for phase in TRAINING_QUESTIONS.keys():
            phase_results = [r for r in self.results if r["phase"] == phase]
            phase_success = sum(1 for r in phase_results if r["success"])
            phase_total = len(phase_results)
            phase_rate = (phase_success / phase_total * 100) if phase_total > 0 else 0
            
            status = "✅" if phase_rate >= 80 else "⚠️" if phase_rate >= 50 else "❌"
            console.print(f"  {status} {phase}: {phase_success}/{phase_total} ({phase_rate:.1f}%)")
        
        # Failed questions
        if failed > 0:
            console.print("\n[bold red]Failed Questions:[/bold red]")
            for i, result in enumerate(self.results):
                if not result["success"]:
                    console.print(f"  {i+1}. {result['question']}")
                    console.print(f"     [dim]Expected: {result['expected_tool']}[/dim]")
        
        # Write to log
        self.log("\n" + "="*70)
        self.log("📊 TRAINING REPORT")
        self.log("="*70)
        self.log(f"Total Questions: {total_questions}")
        self.log(f"Successful: {successful}")
        self.log(f"Failed: {failed}")
        self.log(f"Success Rate: {success_rate:.1f}%")
        self.log(f"Total Time: {total_time:.2f}s")
        self.log(f"Average Time per Question: {total_time/total_questions:.2f}s")
        self.log("\nPhase Breakdown:")
        for phase in TRAINING_QUESTIONS.keys():
            phase_results = [r for r in self.results if r["phase"] == phase]
            phase_success = sum(1 for r in phase_results if r["success"])
            phase_total = len(phase_results)
            phase_rate = (phase_success / phase_total * 100) if phase_total > 0 else 0
            self.log(f"  {phase}: {phase_success}/{phase_total} ({phase_rate:.1f}%)")
        
        console.print(f"\n[cyan]Full log saved to:[/cyan] {self.log_file}")
        console.print(f"[bold green]{'='*70}[/bold green]\n")


def main():
    """Main entry point"""
    console.print("""
[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🤖 Automated AI Agent Trainer                   ║
║                                                           ║
║     Train your agent with predefined questions           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]
    """)
    
    try:
        session = TrainingSession(auto_approve=True)
        session.run_all()
        
        console.print("\n[bold green]✅ Training session completed successfully![/bold green]")
        console.print("[dim]Check the logs directory for detailed results.[/dim]\n")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Training interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Training failed: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
