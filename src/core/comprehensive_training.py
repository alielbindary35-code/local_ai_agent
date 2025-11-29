"""
Comprehensive Training System
Learn Servers, Docker, PostgreSQL, n8n, Python, and Data Science
Downloads official documentation and stores for offline use
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path - find project root by looking for config.py or README.md
def find_project_root():
    """Find the project root directory"""
    current = Path(__file__).resolve()
    # Go up from src/core/comprehensive_training.py to project root
    # Should be: project_root/src/core/comprehensive_training.py
    while current != current.parent:
        # Check for project markers
        if (current / "config.py").exists() and (current / "src").exists():
            return current
        if (current / "README.md").exists() and (current / "src").exists():
            return current
        current = current.parent
    # Fallback: go up 2 levels from src/core/ to get project root
    return Path(__file__).parent.parent.parent

# Add project root to Python path BEFORE importing other modules
project_root = find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table

from src.agents.expert_agent import ExpertAgent
from src.core.knowledge_base import KnowledgeBase
from src.utils.connection_checker import ConnectionChecker

console = Console()

# Comprehensive Training Topics
TRAINING_TOPICS = {
    "Docker": {
        "description": "Containerization and Docker ecosystem",
        "official_docs": [
            "https://docs.docker.com/get-started/",
            "https://docs.docker.com/engine/",
            "https://docs.docker.com/compose/",
            "https://docs.docker.com/network/",
            "https://docs.docker.com/storage/",
            "https://docs.docker.com/security/",
        ],
        "learning_tasks": [
            "What is Docker and how does containerization work?",
            "How to create and run a Docker container?",
            "How to build a Docker image from a Dockerfile?",
            "How to use Docker Compose for multi-container applications?",
            "How to manage Docker volumes and networks?",
            "How to optimize Docker images for production?",
            "How to deploy Docker containers to production?",
            "What are Docker best practices for security?",
        ],
        "keywords": ["docker", "container", "dockerfile", "compose", "image", "volume", "network"]
    },
    "PostgreSQL": {
        "description": "PostgreSQL database administration and development",
        "official_docs": [
            "https://www.postgresql.org/docs/current/",
            "https://www.postgresql.org/docs/current/tutorial.html",
            "https://www.postgresql.org/docs/current/admin.html",
            "https://www.postgresql.org/docs/current/sql.html",
            "https://www.postgresql.org/docs/current/performance-tips.html",
            "https://www.postgresql.org/docs/current/backup.html",
        ],
        "learning_tasks": [
            "What is PostgreSQL and how does it work?",
            "How to install and configure PostgreSQL?",
            "How to create databases and tables in PostgreSQL?",
            "How to write efficient SQL queries in PostgreSQL?",
            "How to manage PostgreSQL users and permissions?",
            "How to backup and restore PostgreSQL databases?",
            "How to optimize PostgreSQL performance?",
            "How to use PostgreSQL with Python applications?",
        ],
        "keywords": ["postgresql", "postgres", "database", "sql", "query", "index", "transaction"]
    },
    "n8n": {
        "description": "n8n workflow automation platform",
        "official_docs": [
            "https://docs.n8n.io/",
            "https://docs.n8n.io/getting-started/",
            "https://docs.n8n.io/workflows/",
            "https://docs.n8n.io/integrations/",
            "https://docs.n8n.io/execution/",
            "https://docs.n8n.io/security/",
        ],
        "learning_tasks": [
            "What is n8n and how does workflow automation work?",
            "How to install and set up n8n?",
            "How to create workflows in n8n?",
            "How to use n8n integrations and nodes?",
            "How to schedule and trigger n8n workflows?",
            "How to handle errors and debugging in n8n?",
            "How to deploy n8n workflows to production?",
            "What are n8n best practices for automation?",
        ],
        "keywords": ["n8n", "workflow", "automation", "integration", "node", "trigger", "webhook"]
    },
    "Python": {
        "description": "Python programming language and ecosystem",
        "official_docs": [
            "https://docs.python.org/3/",
            "https://docs.python.org/3/tutorial/",
            "https://docs.python.org/3/library/",
            "https://docs.python.org/3/howto/",
            "https://peps.python.org/",
        ],
        "learning_tasks": [
            "What are the latest Python features and best practices?",
            "How to use Python for web development?",
            "How to use Python for API development?",
            "How to handle errors and exceptions in Python?",
            "How to optimize Python code performance?",
            "How to use Python with databases?",
            "How to test Python applications?",
            "What are Python design patterns?",
        ],
        "keywords": ["python", "programming", "web", "api", "framework", "library", "package"]
    },
    "Data Science": {
        "description": "Data science with Python (pandas, numpy, matplotlib, scikit-learn)",
        "official_docs": [
            "https://pandas.pydata.org/docs/",
            "https://numpy.org/doc/stable/",
            "https://matplotlib.org/stable/contents.html",
            "https://scikit-learn.org/stable/",
            "https://seaborn.pydata.org/",
        ],
        "learning_tasks": [
            "How to use pandas for data analysis?",
            "How to clean and preprocess data with pandas?",
            "How to perform statistical analysis with numpy?",
            "How to create visualizations with matplotlib and seaborn?",
            "How to use scikit-learn for machine learning?",
            "How to handle missing data in datasets?",
            "How to perform time series analysis?",
            "How to export and import data in various formats?",
        ],
        "keywords": ["pandas", "numpy", "matplotlib", "data", "analysis", "visualization", "machine learning"]
    },
    "Server Management": {
        "description": "Linux server administration and DevOps",
        "official_docs": [
            "https://www.nginx.com/resources/wiki/",
            "https://httpd.apache.org/docs/",
            "https://docs.ansible.com/",
            "https://kubernetes.io/docs/",
        ],
        "learning_tasks": [
            "How to manage Linux servers?",
            "How to configure web servers (Nginx, Apache)?",
            "How to set up SSL certificates?",
            "How to manage server security?",
            "How to monitor server performance?",
            "How to automate server tasks?",
            "How to deploy applications to servers?",
            "What are server best practices?",
        ],
        "keywords": ["server", "linux", "nginx", "apache", "ssl", "security", "deployment", "devops"]
    }
}


class ComprehensiveTrainer:
    """Comprehensive training system for multiple technologies"""
    
    def __init__(self, auto_approve=True):
        self.agent = ExpertAgent(auto_approve=auto_approve)
        self.knowledge_base = KnowledgeBase()
        self.connection_checker = ConnectionChecker()
        self.is_online = self.connection_checker.check_and_display()
        self.results = {}
        self.start_time = None
        self.log_file = None
        
    def setup_logging(self):
        """Setup logging for training session"""
        from src.core.paths import get_logs_dir
        log_dir = get_logs_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = log_dir / f"comprehensive_training_{timestamp}.txt"
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("🎓 COMPREHENSIVE TRAINING SESSION\n")
            f.write("=" * 80 + "\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Online: {self.is_online}\n")
            f.write("=" * 80 + "\n\n")
    
    def log(self, message):
        """Log message to file and console"""
        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
    
    def learn_topic(self, topic_name: str, topic_data: dict):
        """Learn a specific topic comprehensively"""
        console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
        console.print(f"[bold yellow]📚 Learning: {topic_name}[/bold yellow]")
        console.print(f"[dim]{topic_data['description']}[/dim]")
        console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")
        
        self.log(f"\n{'='*80}")
        self.log(f"Learning: {topic_name}")
        self.log(f"Description: {topic_data['description']}")
        self.log(f"{'='*80}\n")
        
        topic_results = {
            "topic": topic_name,
            "tasks_completed": 0,
            "tasks_total": len(topic_data['learning_tasks']),
            "knowledge_saved": 0,
            "errors": []
        }
        
        # Learn each task
        for i, task in enumerate(topic_data['learning_tasks'], 1):
            console.print(f"[cyan]Task {i}/{len(topic_data['learning_tasks'])}:[/cyan] {task}")
            self.log(f"\nTask {i}: {task}")
            
            try:
                # Use learn_new_technology tool if available
                if hasattr(self.agent.expert_tools, 'learn_new_technology'):
                    result = self.agent.expert_tools.learn_new_technology(
                        technology=topic_name,
                        topics=[task]
                    )
                    console.print(f"[green]✓ Learned:[/green] {result[:200]}...")
                    topic_results["knowledge_saved"] += 1
                else:
                    # Fallback: Use regular agent run
                    response = self.agent.run(task)
                    if response and "Error" not in response:
                        # Save to knowledge base
                        self.knowledge_base.store_knowledge(
                            topic=topic_name,
                            content=response,
                            source="comprehensive_training",
                            tags=topic_data['keywords']
                        )
                        topic_results["knowledge_saved"] += 1
                        console.print(f"[green]✓ Saved knowledge[/green]")
                    else:
                        console.print(f"[yellow]⚠ Partial success[/yellow]")
                
                topic_results["tasks_completed"] += 1
                time.sleep(2)  # Small delay between tasks
                
            except Exception as e:
                error_msg = f"Error in task {i}: {str(e)}"
                console.print(f"[red]❌ {error_msg}[/red]")
                self.log(f"ERROR: {error_msg}")
                topic_results["errors"].append(error_msg)
        
        self.results[topic_name] = topic_results
        return topic_results
    
    def download_documentation(self, topic_name: str, topic_data: dict):
        """Download official documentation for offline use"""
        if not self.is_online:
            console.print(f"[yellow]⚠ Offline mode - skipping documentation download for {topic_name}[/yellow]")
            return
        
        console.print(f"\n[cyan]📥 Downloading documentation for {topic_name}...[/cyan]")
        self.log(f"\nDownloading documentation for {topic_name}")
        
        docs_saved = 0
        for doc_url in topic_data['official_docs']:
            try:
                # Use search_documentation tool to get content
                if hasattr(self.agent.expert_tools, 'search_documentation'):
                    result = self.agent.expert_tools.search_documentation(
                        technology=topic_name,
                        query="official documentation"
                    )
                    
                    if result and "Error" not in str(result):
                        # Save to knowledge base
                        self.knowledge_base.store_knowledge(
                            topic=f"{topic_name}_docs",
                            content=str(result),
                            source=doc_url,
                            tags=["official_docs", topic_name]
                        )
                        docs_saved += 1
                        console.print(f"[green]✓ Downloaded:[/green] {doc_url}")
                        self.log(f"Downloaded: {doc_url}")
                else:
                    # Fallback: Use web scraping
                    from src.tools.tools import Tools
                    tools = Tools()
                    content = tools.scrape_webpage(doc_url)
                    if content and "Error" not in content:
                        self.knowledge_base.store_knowledge(
                            topic=f"{topic_name}_docs",
                            content=content,
                            source=doc_url,
                            tags=["official_docs", topic_name]
                        )
                        docs_saved += 1
                        console.print(f"[green]✓ Downloaded:[/green] {doc_url}")
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                console.print(f"[yellow]⚠ Could not download {doc_url}: {str(e)}[/yellow]")
                self.log(f"Could not download {doc_url}: {str(e)}")
        
        return docs_saved
    
    def run_comprehensive_training(self, topics: list = None):
        """Run comprehensive training for specified topics"""
        self.setup_logging()
        self.start_time = time.time()
        
        if topics is None:
            topics = list(TRAINING_TOPICS.keys())
        
        console.print(Panel.fit(
            f"[bold green]🎓 Starting Comprehensive Training[/bold green]\n"
            f"[cyan]Topics:[/cyan] {', '.join(topics)}\n"
            f"[cyan]Total Topics:[/cyan] {len(topics)}\n"
            f"[cyan]Online:[/cyan] {'✅ Yes' if self.is_online else '❌ No'}\n"
            f"[cyan]Log File:[/cyan] {self.log_file}",
            title="Comprehensive Trainer"
        ))
        
        total_tasks = sum(len(TRAINING_TOPICS[topic]['learning_tasks']) for topic in topics)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            main_task = progress.add_task("[cyan]Training Progress", total=total_tasks)
            
            for topic_name in topics:
                if topic_name not in TRAINING_TOPICS:
                    console.print(f"[red]⚠ Unknown topic: {topic_name}[/red]")
                    continue
                
                topic_data = TRAINING_TOPICS[topic_name]
                
                # Download documentation first (if online)
                if self.is_online:
                    self.download_documentation(topic_name, topic_data)
                
                # Learn the topic
                topic_results = self.learn_topic(topic_name, topic_data)
                progress.update(main_task, advance=topic_results["tasks_completed"])
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive training report"""
        total_time = time.time() - self.start_time
        
        console.print(f"\n\n[bold green]{'='*80}[/bold green]")
        console.print(f"[bold green]📊 COMPREHENSIVE TRAINING REPORT[/bold green]")
        console.print(f"[bold green]{'='*80}[/bold green]\n")
        
        # Summary table
        table = Table(title="Training Summary")
        table.add_column("Topic", style="cyan")
        table.add_column("Tasks", style="green")
        table.add_column("Knowledge Saved", style="yellow")
        table.add_column("Errors", style="red")
        
        total_tasks = 0
        total_knowledge = 0
        total_errors = 0
        
        for topic_name, results in self.results.items():
            table.add_row(
                topic_name,
                f"{results['tasks_completed']}/{results['tasks_total']}",
                str(results['knowledge_saved']),
                str(len(results['errors']))
            )
            total_tasks += results['tasks_completed']
            total_knowledge += results['knowledge_saved']
            total_errors += len(results['errors'])
        
        console.print(table)
        
        # Overall stats
        console.print(f"\n[bold cyan]Overall Statistics:[/bold cyan]")
        console.print(f"  Total Topics: {len(self.results)}")
        console.print(f"  Total Tasks Completed: {total_tasks}")
        console.print(f"  Total Knowledge Saved: {total_knowledge}")
        console.print(f"  Total Errors: {total_errors}")
        console.print(f"  Total Time: {total_time:.2f}s ({total_time/60:.1f} minutes)")
        console.print(f"  Average Time per Task: {total_time/total_tasks:.2f}s" if total_tasks > 0 else "")
        
        # Write to log
        self.log("\n" + "="*80)
        self.log("📊 COMPREHENSIVE TRAINING REPORT")
        self.log("="*80)
        for topic_name, results in self.results.items():
            self.log(f"{topic_name}: {results['tasks_completed']}/{results['tasks_total']} tasks, "
                    f"{results['knowledge_saved']} knowledge saved, {len(results['errors'])} errors")
        self.log(f"\nTotal Time: {total_time:.2f}s")
        
        console.print(f"\n[cyan]Full log saved to:[/cyan] {self.log_file}")
        console.print(f"[bold green]{'='*80}[/bold green]\n")


def main():
    """Main entry point"""
    try:
        banner = """[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🎓 Comprehensive Technology Trainer              ║
║                                                           ║
║     Learn: Docker, PostgreSQL, n8n, Python, Data Science ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]"""
        console.print(banner)
    except Exception:
        # Fallback for Windows console issues
        print("\n" + "="*60)
        print("Comprehensive Technology Trainer")
        print("="*60 + "\n")
    
    try:
        trainer = ComprehensiveTrainer(auto_approve=True)
        
        # Ask which topics to train
        console.print("\n[bold]Available Topics:[/bold]")
        for i, topic in enumerate(TRAINING_TOPICS.keys(), 1):
            console.print(f"  {i}. {topic} - {TRAINING_TOPICS[topic]['description']}")
        
        console.print("\n[cyan]Enter topics to train (comma-separated, or 'all' for all topics):[/cyan]")
        choice = input("> ").strip().lower()
        
        if choice == "all":
            topics = None  # Train all
        else:
            topic_list = [t.strip() for t in choice.split(",")]
            topics = [list(TRAINING_TOPICS.keys())[int(t)-1] for t in topic_list if t.isdigit() and 1 <= int(t) <= len(TRAINING_TOPICS)]
            if not topics:
                console.print("[yellow]Invalid selection, training all topics[/yellow]")
                topics = None
        
        trainer.run_comprehensive_training(topics)
        
        console.print("\n[bold green]✅ Comprehensive training completed![/bold green]")
        console.print("[dim]Check the logs directory for detailed results.[/dim]\n")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Training interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Training failed: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Ensure we're in the project root
    import os
    try:
        project_root = find_project_root()
        os.chdir(project_root)
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

