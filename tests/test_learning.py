from expert_tools import ExpertTools
import os

def test_learning():
    print("🚀 Testing Active Learning Tool...")
    
    tools = ExpertTools()
    
    # Force learn n8n
    print("\n1️⃣  Learning n8n...")
    result = tools.learn_new_technology("n8n", ["Workflows", "Nodes", "Triggers"])
    print(result)
    
    # Verify folder creation
    expected_path = os.path.join("knowledge_base", "n8n")
    if os.path.exists(expected_path):
        print(f"\n✅ SUCCESS: Folder created at: {os.path.abspath(expected_path)}")
        print("Files found:")
        for f in os.listdir(expected_path):
            print(f" - {f}")
    else:
        print(f"\n❌ FAILURE: Folder not found at {expected_path}")

if __name__ == "__main__":
    test_learning()
