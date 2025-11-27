"""
Complete Learning Script for Colab
===================================
This script learns ALL tools from essential_tools.json
Use this in Google Colab for comprehensive learning
"""

import json
import time
import sys
from pathlib import Path

# Add project root to path
if Path.cwd() not in [Path(p) for p in sys.path]:
    sys.path.insert(0, str(Path.cwd()))

from src.tools.fast_learning import FastLearning
from src.tools.expert_tools import ExpertTools

def learn_all_tools():
    """Learn ALL tools from essential_tools.json"""
    
    # Initialize
    fast_learner = FastLearning()
    expert_tools = ExpertTools()
    
    # Load tools
    tools_file = Path("data/essential_tools.json")
    if not tools_file.exists():
        print("❌ essential_tools.json not found!")
        return
    
    categories = json.loads(tools_file.read_text())
    
    # Load progress
    progress_file = Path("data/learning_progress.json")
    learned = []
    if progress_file.exists():
        try:
            learned = json.loads(progress_file.read_text())
        except:
            learned = []
    
    # Calculate totals
    total_tools = sum(len(tools) for tools in categories.values())
    learned_count = len(learned)
    to_learn = total_tools - learned_count
    
    print("🚀 Complete Learning Session Started")
    print("=" * 60)
    print(f"📚 Total Tools: {total_tools}")
    print(f"✅ Already Learned: {learned_count}")
    print(f"🎓 To Learn: {to_learn}")
    print("=" * 60)
    print()
    
    if to_learn == 0:
        print("🎉 All tools already learned!")
        return
    
    # Learn each tool
    current = 0
    for category, tools in categories.items():
        print(f"\n📂 Category: {category.upper()}")
        print("-" * 60)
        
        for tool in tools:
            if tool in learned:
                print(f"⏭️  Skipping {tool} (already learned)")
                continue
            
            current += 1
            print(f"\n[{current}/{to_learn}] Learning {tool}...")
            
            try:
                # Define topics based on category
                topics = ["overview", "key-features", "installation", "best-practices"]
                
                if category == "data_analysis":
                    topics.extend(["data-structures", "visualization", "analysis-examples"])
                elif category == "databases":
                    topics.extend(["crud-operations", "connection-setup", "query-examples"])
                elif category == "devops_and_docker":
                    topics.extend(["configuration", "deployment", "cli-commands"])
                elif category == "backend":
                    topics.extend(["routing", "middleware", "api-design"])
                elif category == "frontend":
                    topics.extend(["components", "styling", "state-management"])
                
                # Learn
                results = fast_learner.learn_fast(tool, topics)
                
                # Save to knowledge base
                fast_learner.save_to_knowledge_base(results)
                
                # Update progress
                learned.append(tool)
                progress_file.write_text(json.dumps(learned, indent=2))
                
                print(f"✅ {tool} learned successfully!")
                
                # Rate limiting - be nice to APIs
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Failed to learn {tool}: {e}")
                import traceback
                traceback.print_exc()
                continue
    
    print("\n" + "=" * 60)
    print("✨ Complete Learning Session Finished!")
    print(f"📊 Total Learned: {len(learned)}/{total_tools}")
    print(f"📂 Knowledge Base: data/knowledge_base/")
    print("=" * 60)
    
    # Save final progress
    progress_file.write_text(json.dumps(learned, indent=2))
    print(f"\n💾 Progress saved to: {progress_file}")

if __name__ == "__main__":
    learn_all_tools()

