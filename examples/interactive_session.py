import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.expert_agent import ExpertAgent
import sys
import time

def main():
    try:
        print("\n🚀 Initializing Expert Agent...")
        agent = ExpertAgent()
        print("\n✅ Agent Ready! (Type 'exit' or 'quit' to stop)")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n👉 Your task: ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye! 👋")
                    break
                
                agent.run(user_input)
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                continue
            except Exception as e:
                print(f"\n❌ Error during execution: {e}")
                
    except Exception as e:
        print(f"\n❌ Fatal Error initializing agent: {e}")
        print("Please check if all dependencies are installed and Ollama is running.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
