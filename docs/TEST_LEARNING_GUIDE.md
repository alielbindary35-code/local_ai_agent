# 🧪 Learning Test Scenarios Guide

## Quick Test (Recommended for First Time)

Test if the learning system is working:

```bash
python test_simple_learning.py
```

**What it does:**
- Tests with one query about GraphQL
- Checks if knowledge is stored
- Shows the result

**Expected output:**
- ✅ SUCCESS: 1 new knowledge entry stored
- Shows entry ID, topic, and confidence

---

## Comprehensive Test

Full test scenario with multiple topics:

```bash
python test_learning_scenario.py
```

**What it tests:**
1. **FastAPI** - REST API framework
2. **Redis** - Caching system
3. **Kubernetes** - Container orchestration

**What it verifies:**
- ✅ Knowledge storage
- ✅ Knowledge retrieval
- ✅ Duplicate detection
- ✅ Statistics tracking

**Expected output:**
- Shows before/after statistics
- Lists all learned entries
- Verifies retrieval works
- Checks for duplicates

---

## Manual Test

You can also test manually:

```python
from src.agents.expert_agent import ExpertAgent
from src.utils.knowledge_viewer import KnowledgeViewer

# Initialize
agent = ExpertAgent(enable_online_learning=True)
viewer = KnowledgeViewer()

# Get initial count
initial = viewer.get_statistics()['total_entries']
print(f"Initial: {initial} entries")

# Ask agent something new
response = agent.run("What is MongoDB and how to use it?")

# Wait a bit for learning
import time
time.sleep(2)

# Check if learned
final = viewer.get_statistics()['total_entries']
new_entries = final - initial

if new_entries > 0:
    print(f"✅ Learned! {new_entries} new entries")
    viewer.view_all_knowledge(limit=5)
else:
    print("⚠️ No new entries (might already exist)")
```

---

## What to Look For

### ✅ Success Indicators:
- `Knowledge stored (ID: X)` message appears
- Entry count increases
- Entry appears in `view_knowledge.py`
- Retrieval works correctly

### ⚠️ If No Learning Occurs:
1. **Check learning is enabled:**
   ```python
   agent = ExpertAgent(enable_online_learning=True)  # Must be True
   ```

2. **Check response quality:**
   - Response must be > 100 characters
   - Must not contain "Error:"
   - Must have substantial content

3. **Check if already exists:**
   ```python
   viewer = KnowledgeViewer()
   viewer.view_all_knowledge(limit=50)  # Check existing entries
   ```

4. **Check confidence threshold:**
   - Learning requires confidence >= 0.5
   - Some responses might be below threshold

---

## Test Results Interpretation

### Scenario 1: Learning Works ✅
```
Initial entries: 10
Final entries: 13
Total learned: 3
✅ SUCCESS
```

### Scenario 2: No Learning (Already Exists) ⚠️
```
Initial entries: 10
Final entries: 10
Total learned: 0
⚠️ Knowledge might already exist
```

### Scenario 3: No Learning (Low Quality) ⚠️
```
Initial entries: 10
Final entries: 10
Total learned: 0
⚠️ Response didn't meet learning criteria
```

---

## Troubleshooting

### Problem: No entries stored
**Solution:**
1. Check `enable_online_learning=True`
2. Try a completely new topic
3. Check response length (> 100 chars)
4. Verify no errors in response

### Problem: Duplicate entries
**Solution:**
```python
viewer = KnowledgeViewer()
viewer.show_duplicates()
# Then delete duplicates using option 5 in interactive menu
```

### Problem: Can't retrieve knowledge
**Solution:**
```python
viewer = KnowledgeViewer()
viewer.view_entry(entry_id=12)  # Check if entry exists
```

---

## Expected Test Duration

- **Simple test:** ~30-60 seconds
- **Comprehensive test:** ~3-5 minutes (depends on model speed)

---

## Next Steps After Testing

1. **View stored knowledge:**
   ```bash
   python view_knowledge.py
   ```

2. **Check for duplicates:**
   ```python
   from src.utils.knowledge_viewer import KnowledgeViewer
   viewer = KnowledgeViewer()
   viewer.show_duplicates()
   ```

3. **View statistics:**
   ```python
   viewer.show_statistics()
   ```

---

## Example Test Output

```
🧪 Learning Test Scenario
═══════════════════════════════════════════════════════════

Step 1: Initializing Agent...
✓ Agent initialized

Step 2: Getting initial knowledge base statistics...
✓ Initial knowledge entries: 12

Test 1/3: Learning New Topic
═══════════════════════════════════════════════════════════
📝 Query: What is FastAPI and how to create a REST API with it?
🔍 Expected Keywords: fastapi, rest, api, python

Step 3.1: Running agent with query...
✓ Agent responded in 15.23s
✅ SUCCESS: 1 new knowledge entry/entries stored!
  Entry ID: 13
  Category: programming
  Confidence: 0.75
  Keywords found: 3/4

...

Step 4: Final Verification
═══════════════════════════════════════════════════════════
Final Statistics:
Initial entries: 12
Final entries: 15
Total learned in this session: 3

✅ Learning System Working!
```

---

## Tips

1. **Use unique topics** for testing (not already learned)
2. **Wait 2-3 seconds** after agent response for learning to complete
3. **Check statistics** before and after to see changes
4. **Use simple test first** to verify basic functionality
5. **Check logs** if something doesn't work

