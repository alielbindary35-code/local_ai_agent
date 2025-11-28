# Model Selection Options - Quick Guide

## New Feature: Choose Your Model! 🎯

When you start the agent, you now have **3 options**:

```
🤖 MODEL SELECTION
============================================================

How would you like to select models?

[1] Auto-select (Agent chooses best model for each task) ✨
[2] Manual (You choose the model once for all tasks)
[3] Ask me every time

Your choice (1/2/3) [default: 1]:
```

## Option 1: Auto-Select (Recommended) ✨

**What it does**: Agent automatically picks the best model for each task

**Example**:
- You ask: "Create a Python calculator"
- Agent selects: `deepseek-r1:8b` (best for coding)
- You ask: "Analyze this data"
- Agent selects: `gemma3:27b` (best for analysis)

**Best for**: Most users - let the agent optimize!

## Option 2: Manual (Choose Once)

**What it does**: You pick one model to use for ALL tasks

**Example**:
```
📋 Available Models:
  [1] gemma3:27b (17.4 GB) - general
  [2] qwen2.5:3b (1.9 GB) - file_ops
  [3] deepseek-r1:8b (5.2 GB) - coding
  [4] mistral:latest (4.4 GB) - reasoning
  [5] qwen2.5:0.5b (0.4 GB) - simple
  [6] llama3.2:latest (2.0 GB) - conversation

Select model (1-6): 2

✅ Using qwen2.5:3b for all tasks
```

**Best for**: 
- You want a **fast model** (like `qwen2.5:3b` or `mistral:latest`)
- You know which model works best for your workflow
- You want consistent performance

## Option 3: Ask Every Time

**What it does**: Before each task, you choose the model

**Example**:
```
👉 Your task: Create a calculator

📋 Available Models:
  [1] gemma3:27b (17.4 GB) - general
  [2] qwen2.5:3b (1.9 GB) - file_ops
  [3] deepseek-r1:8b (5.2 GB) - coding
  [4] mistral:latest (4.4 GB) - reasoning
  [5] qwen2.5:0.5b (0.4 GB) - simple
  [6] llama3.2:latest (2.0 GB) - conversation
  [0] Auto-select (let agent choose)

Select model (0-6): 3
```

**Best for**:
- You want **full control** over each task
- You're testing different models
- Different tasks need different models

## Recommended Models by Speed

### Fastest (< 5 seconds response)
- `qwen2.5:0.5b` - Simple tasks only
- `qwen2.5:3b` - Good balance of speed & quality

### Fast (5-15 seconds)
- `mistral:latest` - Great for most tasks
- `llama3.2:latest` - Good for conversation

### Slower but Best Quality (15-60+ seconds)
- `deepseek-r1:8b` - Best for coding (may be slow)
- `gemma3:27b` - Best for complex tasks (may be slow)

## My Recommendation 💡

**For your system** (based on the slow response you're seeing):

1. **Start with Option 2 (Manual)**
2. **Choose `mistral:latest` or `qwen2.5:3b`**
3. These models are **fast** and **good quality**

**Example**:
```
Your choice (1/2/3) [default: 1]: 2
Select model (1-6): 4  ← Choose mistral:latest
✅ Using mistral:latest for all tasks
```

Then all your tasks will use the fast `mistral:latest` model! 🚀

## How to Restart

1. **Stop the current session** (Ctrl+C or type `exit`)
2. **Run again**:
   ```powershell
   python examples/interactive_session.py
   ```
3. **Choose your option** (I recommend Option 2 with `mistral:latest`)

Now you have full control! 🎉
