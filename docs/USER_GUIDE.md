# User Guide - AI Agent System

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

## Introduction

The AI Agent is a powerful, self-improving AI assistant that runs locally on your machine using Ollama. It can help with:

- File operations and project management
- Data analysis (Excel, CSV)
- System administration
- Code generation and analysis
- n8n workflow creation
- Docker operations
- Database management
- And much more!

## Getting Started

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running ([Download](https://ollama.ai/))
3. At least one Ollama model (e.g., `ollama pull qwen2.5:3b`)

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the agent:
   ```bash
   python -m src.agents.agent
   ```

## Basic Usage

### Simple Tasks

The agent can handle simple queries directly:

```
You: Check my disk space

Agent: [Checks disk usage and reports]
```

### File Operations

```
You: Create a file called hello.py with a function that prints "Hello, World!"

Agent: [Creates the file with the requested code]
```

### Data Analysis

```
You: Analyze sales.xlsx and show me the top 5 products by revenue

Agent: [Reads Excel file, analyzes data, and presents results]
```

## Advanced Features

### Excel Handling

The agent can:
- Read and write Excel files (.xlsx, .xls)
- Clean data (remove empty rows, normalize dates, strip strings)
- Perform statistical analysis
- Generate reports

**Example:**
```
You: Read data.xlsx, clean it, and show me summary statistics
```

### n8n Workflow Management

Create and manage n8n workflows:

```
You: Create an n8n workflow that processes webhook data
```

The agent can:
- Create workflow templates
- Export/import workflows
- Test webhooks
- Manage workflow status

### API Integration

The agent includes a modular API handler with:
- Multiple authentication methods (API key, OAuth, Basic Auth)
- Automatic retry with exponential backoff
- Response caching
- Data formatting (pandas DataFrame)

### Security Features

- **Permission System**: Every action requires approval based on risk level
- **Risk Assessment**: Actions are categorized as Safe 🟢, Caution 🟡, or Dangerous 🔴
- **Audit Logging**: All actions are logged for review
- **Data Encryption**: Sensitive data can be encrypted

### Performance Optimization

- **Task Prioritization**: Tasks are prioritized based on urgency
- **Resource Monitoring**: System resources are monitored to prevent overload
- **Dynamic Module Loading**: Modules are loaded only when needed

## Configuration

### Environment Variables

You can configure the agent using environment variables:

```bash
export OLLAMA_URL=http://localhost:11434
export DEFAULT_MODEL=qwen2.5:3b
export MAX_ITERATIONS=10
export AUTO_APPROVE=false
```

### Configuration File

Create a `config.py` file in the project root:

```python
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"
MAX_ITERATIONS = 10
AUTO_APPROVE = False
```

## Troubleshooting

### Agent Not Starting

**Problem**: Agent fails to start

**Solutions**:
1. Check if Ollama is running: `ollama serve`
2. Verify Ollama URL is correct
3. Check if model is installed: `ollama list`
4. Review error messages in console

### Model Not Found

**Problem**: "Model not found" error

**Solutions**:
1. Pull the model: `ollama pull qwen2.5:3b`
2. Check available models: `ollama list`
3. Update DEFAULT_MODEL in config

### Permission Denied

**Problem**: Actions are being denied

**Solutions**:
1. Review risk assessment for the action
2. Approve the action when prompted
3. For testing, set AUTO_APPROVE=True (use with caution)

### Memory Issues

**Problem**: Agent running slowly or out of memory

**Solutions**:
1. Use a smaller model for simple tasks
2. Clear memory: `python -m src.core.clean_memory`
3. Monitor resources: Check system resources in agent output

### Excel File Errors

**Problem**: Cannot read Excel file

**Solutions**:
1. Verify file exists and is accessible
2. Check file format (supports .xlsx, .xls, .xlsm)
3. Ensure openpyxl is installed: `pip install openpyxl`

## Best Practices

1. **Start Simple**: Begin with simple tasks to understand the agent's capabilities
2. **Review Actions**: Always review actions before approval, especially for dangerous operations
3. **Use Categories**: Tag solutions in memory for easier retrieval
4. **Monitor Resources**: Keep an eye on system resources for complex tasks
5. **Regular Backups**: Backup your memory database regularly

## Getting Help

- Check the documentation in the `docs/` folder
- Review example scripts in the `examples/` folder
- Check the knowledge base in `data/knowledge_base/`

## Advanced Topics

### Custom Tools

You can register custom tools:

```python
agent.tools.register_custom_tool(
    name="my_tool",
    command="python my_script.py {param}",
    description="My custom tool"
)
```

### Memory Management

View memory statistics:

```python
stats = agent.memory.get_statistics()
print(stats)
```

### Workflow Templates

Create custom n8n workflow templates and save them in `data/knowledge_base/n8n/`.

## Security Considerations

1. **Never approve dangerous actions without review**
2. **Review audit logs regularly** (`data/audit_log.jsonl`)
3. **Encrypt sensitive data** when storing API keys or passwords
4. **Keep Ollama local** - don't expose it to the internet
5. **Review permissions** before granting access to system resources

---

For more information, see the [README.md](../README.md) and other documentation files.

