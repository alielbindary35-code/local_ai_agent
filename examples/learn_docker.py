import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.expert_agent import ExpertAgent
import sys

def learn_docker():
    print("🚀 Starting Active Learning Session for: Docker...")
    
    agent = ExpertAgent()
    
    # Task: Learn Docker and create knowledge base
    task = "Learn Docker technology including containers, images, and docker-compose, and save the knowledge base."
    
    print(f"\n👉 Task: {task}\n")
    agent.run(task)

if __name__ == "__main__":
    learn_docker()
