"""Learning Verification Script - Check if agent saved information to knowledge base"""
from pathlib import Path

def verify_learning(technology: str):
    """Verify if information for a technology was saved"""
    kb_path = Path("data/knowledge_base") / technology.lower().replace(" ", "_")
    
    if not kb_path.exists():
        print(f"❌ {technology}: Not found - Information was not saved")
        return False
    
    files = list(kb_path.glob("*.md"))
    if not files:
        print(f"⚠️ {technology}: Directory exists but is empty")
        return False
    
    print(f"✅ {technology}: Found!")
    for file in files:
        size = file.stat().st_size
        print(f"   📄 {file.name} ({size} bytes)")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Knowledge Base Verification")
    print("=" * 60)
    
    # Check system_info
    print("\n📊 Checking System Info:")
    verify_learning("system_info")
    
    # General statistics
    kb = Path("data/knowledge_base")
    if kb.exists():
        technologies = [d.name for d in kb.iterdir() if d.is_dir()]
        print(f"\n📈 Total technologies saved: {len(technologies)}")
        print(f"📍 Path: {kb.absolute()}")
    else:
        print("\n❌ Knowledge base directory not found!")

