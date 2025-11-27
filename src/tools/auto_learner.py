"""
Auto Learner - The "Brain" Expander
===================================

This module automates the mass-learning of technologies.
It reads a list of tools and systematically learns them using the FastLearning module.
"""

import json
import time
import sys
from typing import List, Dict

# Import paths system
from src.core.paths import (
    get_data_dir,
    get_essential_tools_file,
    get_learning_progress_file,
    get_knowledge_base_dir,
    ensure_dir
)

# Check if we're in a Jupyter/Colab environment
IN_JUPYTER = hasattr(sys, 'ps1') or 'ipykernel' in str(type(sys.modules.get('IPython', None)))

# Import Rich only if not in Jupyter (to avoid recursion issues)
if not IN_JUPYTER:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    console = Console()
else:
    # Simple console for Jupyter/Colab
    class SimpleConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = SimpleConsole()

# Import our tools
from src.tools.fast_learning import FastLearning

class AutoLearner:
    def __init__(self):
        self.fast_learner = FastLearning()
        self.data_dir = get_data_dir()
        self.tools_file = get_essential_tools_file()
        self.progress_file = get_learning_progress_file()
        
        # Ensure directories exist
        ensure_dir(self.data_dir)
        ensure_dir(get_knowledge_base_dir())
        
    def load_tools_list(self) -> Dict[str, List[str]]:
        """Load the master list of tools to learn"""
        if not self.tools_file.exists():
            if IN_JUPYTER:
                print(f"Error: Tools list not found at {self.tools_file}")
            else:
                console.print(f"[red]Error: Tools list not found at {self.tools_file}[/red]")
            return {}
        
        return json.loads(self.tools_file.read_text())
    
    def load_progress(self) -> List[str]:
        """Load list of already learned tools"""
        if not self.progress_file.exists():
            return []
        try:
            return json.loads(self.progress_file.read_text())
        except:
            return []
            
    def save_progress(self, learned_tool: str):
        """Mark a tool as learned"""
        progress = self.load_progress()
        if learned_tool not in progress:
            progress.append(learned_tool)
            self.progress_file.write_text(json.dumps(progress, indent=2))

    def learn_all(self):
        """Learn EVERYTHING in the list automatically"""
        categories = self.load_tools_list()
        learned = self.load_progress()
        
        # Calculate total
        total_tools = sum(len(tools) for tools in categories.values())
        learned_count = len([t for cat in categories.values() for t in cat if t in learned])
        to_learn_count = total_tools - learned_count
        
        if IN_JUPYTER:
            print("🚀 Auto-Learner Initialized")
            print(f"📚 Total Tools: {total_tools}")
            print(f"✅ Already Learned: {learned_count}")
            print(f"🎓 To Learn: {to_learn_count}\n")
            
            if to_learn_count == 0:
                print("🎉 All tools have been learned! You have a genius agent now.")
                return
        else:
            console.print(f"[bold cyan]🚀 Auto-Learner Initialized[/bold cyan]")
            console.print(f"📚 Total Tools: {total_tools}")
            console.print(f"✅ Already Learned: {learned_count}")
            console.print(f"🎓 To Learn: {to_learn_count}\n")
            
            if to_learn_count == 0:
                console.print("[green]🎉 All tools have been learned! You have a genius agent now.[/green]")
                return

        # Start learning loop
        if IN_JUPYTER:
            # Simple progress for Jupyter/Colab
            learned_count = 0
            for category, tools in categories.items():
                for tool in tools:
                    if tool in learned:
                        continue
                    
                    learned_count += 1
                    print(f"[{learned_count}/{to_learn_count}] Learning {tool} ({category})...")
                    
                    # 1. Fast Learn
                    try:
                        # Default topics for general tools
                        topics = ["overview", "key-features", "installation", "best-practices"]
                        
                        # Custom topics based on category
                        if category == "data_analysis":
                            topics.extend(["data-structures", "visualization", "analysis-examples"])
                        elif category == "databases":
                            topics.extend(["crud-operations", "connection-setup", "query-examples"])
                        elif category == "devops_and_docker":
                            topics.extend(["configuration", "deployment", "cli-commands"])
                        elif category == "backend":
                            topics.extend(["routing", "middleware", "api-design", "authentication"])
                        elif category == "frontend":
                            topics.extend(["components", "styling", "state-management", "routing"])
                        elif category == "cloud_platforms":
                            topics.extend(["services", "pricing", "deployment", "scaling"])
                        elif category == "mobile_development":
                            topics.extend(["ui-components", "navigation", "platform-specific", "performance"])
                        elif category == "testing_frameworks":
                            topics.extend(["unit-testing", "integration-testing", "e2e-testing", "mocking"])
                        elif category == "security_tools":
                            topics.extend(["vulnerability-scanning", "penetration-testing", "security-best-practices"])
                        elif category == "api_tools":
                            topics.extend(["api-design", "documentation", "testing", "mock-servers"])
                        elif category == "version_control":
                            topics.extend(["workflows", "branching-strategies", "ci-cd-integration"])
                        elif category == "monitoring_logging":
                            topics.extend(["log-aggregation", "metrics", "alerting", "dashboards"])
                        elif category == "message_queues":
                            topics.extend(["pub-sub", "message-patterns", "scaling", "reliability"])
                        elif category == "caching":
                            topics.extend(["cache-strategies", "invalidation", "performance-optimization"])
                        elif category == "build_tools":
                            topics.extend(["bundling", "optimization", "code-splitting", "plugins"])
                            
                        # Execute learning
                        results = self.fast_learner.learn_fast(tool, topics)
                        
                        # 2. Save to Knowledge Base
                        self.fast_learner.save_to_knowledge_base(results)
                        
                        # 3. Mark as done
                        self.save_progress(tool)
                        print(f"✅ Learned {tool}")
                        
                        # Small pause to be nice to APIs
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"❌ Failed to learn {tool}: {e}")
                        import traceback
                        traceback.print_exc()
                        continue
        else:
            # Rich progress for terminal
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                
                overall_task = progress.add_task("[green]Overall Progress", total=to_learn_count)
                
                for category, tools in categories.items():
                    for tool in tools:
                        if tool in learned:
                            continue
                        
                        # Learn this tool
                        progress.update(overall_task, description=f"[cyan]Learning {tool} ({category})...")
                        
                        # 1. Fast Learn
                        try:
                            # Default topics for general tools
                            topics = ["overview", "key-features", "installation", "best-practices"]
                            
                            # Custom topics based on category
                            if category == "data_analysis":
                                topics.extend(["data-structures", "visualization", "analysis-examples"])
                            elif category == "databases":
                                topics.extend(["crud-operations", "connection-setup", "query-examples"])
                            elif category == "devops_and_docker":
                                topics.extend(["configuration", "deployment", "cli-commands"])
                            elif category == "backend":
                                topics.extend(["routing", "middleware", "api-design", "authentication"])
                            elif category == "frontend":
                                topics.extend(["components", "styling", "state-management", "routing"])
                            elif category == "cloud_platforms":
                                topics.extend(["services", "pricing", "deployment", "scaling"])
                            elif category == "mobile_development":
                                topics.extend(["ui-components", "navigation", "platform-specific", "performance"])
                            elif category == "testing_frameworks":
                                topics.extend(["unit-testing", "integration-testing", "e2e-testing", "mocking"])
                            elif category == "security_tools":
                                topics.extend(["vulnerability-scanning", "penetration-testing", "security-best-practices"])
                            elif category == "api_tools":
                                topics.extend(["api-design", "documentation", "testing", "mock-servers"])
                            elif category == "version_control":
                                topics.extend(["workflows", "branching-strategies", "ci-cd-integration"])
                            elif category == "monitoring_logging":
                                topics.extend(["log-aggregation", "metrics", "alerting", "dashboards"])
                            elif category == "message_queues":
                                topics.extend(["pub-sub", "message-patterns", "scaling", "reliability"])
                            elif category == "caching":
                                topics.extend(["cache-strategies", "invalidation", "performance-optimization"])
                            elif category == "build_tools":
                                topics.extend(["bundling", "optimization", "code-splitting", "plugins"])
                                
                            # Execute learning
                            results = self.fast_learner.learn_fast(tool, topics)
                            
                            # 2. Save to Knowledge Base
                            self.fast_learner.save_to_knowledge_base(results)
                            
                            # 3. Mark as done
                            self.save_progress(tool)
                            progress.advance(overall_task)
                            
                            # Small pause to be nice to APIs
                            time.sleep(1)
                            
                        except Exception as e:
                            console.print(f"[red]❌ Failed to learn {tool}: {e}[/red]")
                            continue
        
        kb_path = get_knowledge_base_dir()
        
        if IN_JUPYTER:
            print("\n✨ Auto-Learning Session Complete! ✨")
            print(f"📂 Knowledge stored in: {kb_path.absolute()}")
        else:
            console.print("\n[bold green]✨ Auto-Learning Session Complete! ✨[/bold green]")
            console.print(f"📂 Knowledge stored in: {kb_path.absolute()}")

if __name__ == "__main__":
    learner = AutoLearner()
    learner.learn_all()
