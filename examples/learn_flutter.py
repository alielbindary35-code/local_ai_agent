"""
Learn Flutter Fast
==================

This script demonstrates how to teach your agent Flutter using the new Fast Learning capabilities.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.expert_agent import ExpertAgent
from rich.console import Console

console = Console()

def main():
    agent = ExpertAgent()
    
    # The "Template" for asking:
    # "Learn [Technology] and focus on [Topics]"
    
    prompt = """
    Can you learn Flutter? 
    Please focus on:
    1. Widgets
    2. State Management (Provider/Riverpod)
    3. Navigation
    4. API Integration
    """
    
    console.print("[bold cyan]🚀 Asking Agent to Learn Flutter...[/bold cyan]")
    agent.run(prompt)

if __name__ == "__main__":
    main()
