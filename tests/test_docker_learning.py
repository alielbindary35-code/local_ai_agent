"""
Test script to verify Docker learning tool works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.expert_tools import ExpertTools

def test_docker_learning():
    print("🧪 Testing Docker Learning Tool...")
    
    tools = ExpertTools()
    
    # Execute the tool
    result = tools.learn_new_technology(
        "Docker",
        ["containers", "images", "docker-compose", "architecture", "networking", "volumes", "best practices"]
    )
    
    print("\n" + "="*60)
    print("TOOL RESULT:")
    print("="*60)
    print(result)
    print("="*60)
    
    # Verify folder was created
    kb_path = Path("data/knowledge_base/docker")
    if kb_path.exists():
        print(f"\n✅ SUCCESS: Docker knowledge base created at: {kb_path.absolute()}")
        print("\nFiles created:")
        for f in kb_path.iterdir():
            print(f"  - {f.name}")
    else:
        print(f"\n❌ FAILURE: Folder not found at {kb_path}")

if __name__ == "__main__":
    test_docker_learning()

