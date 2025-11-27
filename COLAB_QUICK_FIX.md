# 🔧 Quick Fix for Colab JSON Error

## If you get JSON error in Colab:

### Quick Fix (Copy this in Colab):

```python
# Fix JSON files encoding
import json
from pathlib import Path

# Fix essential_tools.json
tools_file = Path('data/essential_tools.json')
if tools_file.exists():
    try:
        content = tools_file.read_text(encoding='utf-8').strip()
        content = content.lstrip('\ufeff')  # Remove BOM
        data = json.loads(content)
        tools_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        print("OK: Fixed essential_tools.json")
    except Exception as e:
        print(f"ERROR: {e}")

# Fix learning_progress.json
progress_file = Path('data/learning_progress.json')
if progress_file.exists():
    try:
        content = progress_file.read_text(encoding='utf-8').strip()
        content = content.lstrip('\ufeff')
        if content:
            data = json.loads(content)
            progress_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
            print("OK: Fixed learning_progress.json")
    except:
        progress_file.write_text('[]', encoding='utf-8')
        print("OK: Created fresh learning_progress.json")
```

### Then run auto-learner:

```python
from src.tools.auto_learner import AutoLearner
learner = AutoLearner()
learner.learn_all()
```

---

**The fixes are already in the latest GitHub version!** Just re-clone to get them.

