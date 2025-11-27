# How to Use Docker Knowledge Base - دليل الاستخدام

## ✅ Current Status
The Docker knowledge base has been **successfully created** at:
```
data/knowledge_base/docker/
├── overview.md          (Study guide template)
└── basic_example.json   (Code template)
```

## 📝 Next Steps to Fill with Real Content

### Step 1: Search Web for Docker Tutorial and Save It

**Option A: Using Expert Agent (Recommended)**
```bash
python examples\learn_docker.py
# Then ask: "Search web for Docker tutorial and save the content to knowledge base"
```

**Option B: Direct Command**
```python
from src.agents.expert_agent import ExpertAgent

agent = ExpertAgent()
agent.run("Search web for Docker tutorial about containers and images, then save the content to the Docker knowledge base")
```

### Step 2: Generate Docker Code Examples and Save Them

**Using Expert Agent:**
```python
from src.agents.expert_agent import ExpertAgent

agent = ExpertAgent()

# Example 1: Dockerfile example
agent.run("Generate a Dockerfile example for a Python web application and save it to Docker knowledge base")

# Example 2: docker-compose.yml example
agent.run("Create a docker-compose.yml example with web server and database, then save it to Docker knowledge base")

# Example 3: Docker commands
agent.run("Generate common Docker commands examples (run, build, push) and save them to Docker knowledge base")
```

### Step 3: Read the Saved Knowledge

**Using Python:**
```python
from src.tools.expert_tools import ExpertTools

tools = ExpertTools()
knowledge = tools.read_knowledge_base("Docker")
print(knowledge)
```

**Using Expert Agent:**
```python
from src.agents.expert_agent import ExpertAgent

agent = ExpertAgent()
agent.run("Read the Docker knowledge base and show me what we learned")
```

## 🛠️ Available Tools for Knowledge Base

### 1. `learn_new_technology(technology, topics)`
- ✅ Already executed for Docker
- Creates the structure

### 2. `search_web(query, max_results)`
- Search online for information
- Example: `search_web("Docker containers tutorial", 5)`

### 3. `save_code_snippet(code, language, description, tags)`
- Save code examples
- Example: `save_code_snippet("FROM python:3.9", "dockerfile", "Python Dockerfile", ["docker", "python"])`

### 4. `read_knowledge_base(technology)`
- Read saved knowledge
- Example: `read_knowledge_base("Docker")`

## 📋 Complete Workflow Example

```python
from src.agents.expert_agent import ExpertAgent

agent = ExpertAgent()

# Step 1: Learn (already done ✅)
# agent.run("Learn Docker technology including containers, images, and docker-compose")

# Step 2: Search and learn more
agent.run("Search web for Docker best practices and containerization patterns, then save the key points to Docker knowledge base")

# Step 3: Generate examples
agent.run("Create a complete Docker example with Dockerfile and docker-compose.yml for a Node.js application, then save it to Docker knowledge base")

# Step 4: Read everything
agent.run("Read the complete Docker knowledge base and summarize what we learned")
```

## 🎯 Quick Commands

### Search and Save Docker Content
```bash
python -c "from src.agents.expert_agent import ExpertAgent; agent = ExpertAgent(); agent.run('Search web for Docker networking tutorial and save to knowledge base')"
```

### Generate and Save Code
```bash
python -c "from src.agents.expert_agent import ExpertAgent; agent = ExpertAgent(); agent.run('Generate Dockerfile example for Python Flask app and save to Docker knowledge base')"
```

### Read Knowledge
```bash
python -c "from src.tools.expert_tools import ExpertTools; tools = ExpertTools(); print(tools.read_knowledge_base('Docker'))"
```

## 📂 File Structure

After completing the steps, your knowledge base will look like:
```
data/knowledge_base/docker/
├── overview.md              (Main guide - will be updated)
├── basic_example.json        (Code template - will be updated)
├── dockerfile_example.txt    (Generated examples)
├── docker_compose_example.yml
└── commands_guide.md         (Common commands)
```

## 💡 Tips

1. **Be Specific**: When asking to save content, specify what to save:
   - ✅ "Save the Docker networking tutorial to knowledge base"
   - ❌ "Search Docker" (too vague)

2. **Use Multiple Queries**: Break down learning into topics:
   - "Search Docker containers tutorial"
   - "Search Docker images best practices"
   - "Search docker-compose examples"

3. **Verify**: Always read the knowledge base after saving to verify content

4. **Update**: You can ask to update existing files:
   - "Update the Docker overview.md with new information about volumes"

## 🔍 Verify Your Knowledge Base

```python
from pathlib import Path

kb_path = Path("data/knowledge_base/docker")
if kb_path.exists():
    print("✅ Docker knowledge base exists!")
    print("\nFiles:")
    for f in kb_path.iterdir():
        print(f"  - {f.name} ({f.stat().st_size} bytes)")
else:
    print("❌ Knowledge base not found")
```

---

**Ready to start?** Run:
```bash
python examples\learn_docker.py
```
Then ask: "Search web for Docker containers tutorial and save it to knowledge base"

