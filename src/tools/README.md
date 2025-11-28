# Tools Library

This directory contains all tool implementations for the AI agent.

## Tool Categories

### Basic Tools (`tools.py`)
Core functionality available to all agents:
- File system operations (read, write, list, search)
- Command execution
- Web access (search, scrape, API calls)
- Package management
- Python REPL execution
- System information

### Expert Tools (`expert_tools.py`)
Advanced tools for expert-level agents:
- Docker operations
- n8n workflow management
- PostgreSQL database operations
- Server management
- Code generation and analysis
- Web design tools

### Extended Tools (`extended_tools.py`)
Additional specialized tools:
- Extended database support
- Advanced monitoring
- Additional integrations

### Learning Tools (`auto_learner.py`)
Automated learning capabilities:
- Knowledge base management
- Documentation searching
- Code snippet storage
- Technology learning workflows

## Adding New Tools

1. Add the tool method to the appropriate class
2. Update `get_tool_descriptions()` method
3. Add error handling
4. Write unit tests
5. Update documentation

## Tool Execution

Tools are executed through the `execute()` method:

```python
tools = Tools()
result = tools.execute("read_file", {"filepath": "example.txt"})
```

## Error Handling

All tools should:
- Return error messages as strings (not raise exceptions)
- Handle missing dependencies gracefully
- Provide helpful error messages
- Log errors for debugging

