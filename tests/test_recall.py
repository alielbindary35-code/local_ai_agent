from expert_tools import ExpertTools

def test_recall():
    print("🚀 Testing Knowledge Recall...")
    tools = ExpertTools()
    
    # Try to read n8n knowledge (which we created earlier)
    print("\n📖 Reading n8n knowledge...")
    result = tools.read_knowledge_base("n8n")
    print(result)

if __name__ == "__main__":
    test_recall()
