from agent import Agent
from rich.console import Console

console = Console()

def test_agent():
    console.print("[bold]Running Verification Test...[/bold]")
    
    # Initialize agent
    agent = Agent(auto_approve=True) # Auto-approve for testing
    
    # Test Question
    question = "What is the OS version?"
    console.print(f"\n[cyan]Question:[/cyan] {question}")
    
    # Run
    response = agent.run(question)
    
    console.print(f"\n[green]Final Answer:[/green] {response}")

if __name__ == "__main__":
    test_agent()
