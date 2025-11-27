import os
import json
from pathlib import Path
from datetime import datetime

def force_create():
    print("🚀 Forcing creation of n8n knowledge base...")
    
    try:
        # 1. Create directory
        kb_dir = Path("knowledge_base") / "n8n"
        kb_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory created: {kb_dir.absolute()}")
        
        # 2. Create overview.md
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        intro_content = f"""# n8n Knowledge Base
Created: {timestamp}

## What is n8n?
n8n is an extendable workflow automation tool. With a node-based editor, it lets you connect anything to everything.

## Key Concepts
- Workflows
- Nodes
- Triggers

## Resources
- Official Docs: https://docs.n8n.io
- Tutorials: https://n8n.io/learn
"""
        (kb_dir / "overview.md").write_text(intro_content)
        print("✅ Created overview.md")
        
        # 3. Create basic_example.json
        snippet_content = {
            "technology": "n8n",
            "type": "sample_workflow",
            "code": "// Sample n8n workflow code",
            "description": "Basic example for n8n"
        }
        (kb_dir / "basic_example.json").write_text(json.dumps(snippet_content, indent=2))
        print("✅ Created basic_example.json")
        
        print("\n🎉 SUCCESS! n8n knowledge base is ready.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    force_create()
