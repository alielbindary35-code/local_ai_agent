# 🎓 Expert AI Agent - وكيل ذكاء اصطناعي خبير

## 🌟 نظام متكامل مع 3 مستويات + 5 موديلات + 120+ أداة متخصصة

**A powerful, self-improving AI agent that runs locally on your server using Ollama.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-orange)](https://ollama.ai/)

## ✨ Features

- **🧠 Advanced ReAct Loop**: Multi-step reasoning with self-reflection
- **🤖 Multi-Model Intelligence**: Auto-selects best model based on task complexity
- **🛠️ 120+ Tools**: Data analysis, databases, cloud platforms, mobile dev, testing, security, and more
- **💾 Continuous Learning**: SQLite-based memory system that improves over time
- **🔒 Security First**: Risk assessment and explicit permission for every action
- **🌐 Web Integration**: DuckDuckGo search and web scraping (no API keys needed)
- **📦 Smart Package Management**: Auto-installs missing tools (pip, npm, apt, choco, brew)
- **🐳 Container Support**: Docker and Docker Compose integration
- **📊 Data Analysis**: Python REPL with pandas for Excel/CSV analysis
- **🖥️ Cross-Platform**: Works on Windows, Linux, and macOS

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running ([Download](https://ollama.ai/))
3. At least one Ollama model (e.g., `ollama pull llama3.1:8b`)

### Installation

#### Windows

```cmd
cd local_ai_agent
run_agent.bat
```

#### Linux/macOS

```bash
cd local_ai_agent
chmod +x run_agent.sh
./run_agent.sh
```

The launcher will:
- ✅ Check Python and Ollama
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Start the agent

## 📖 Usage Examples

### Example 1: System Administration

```
You: Check my disk space and warn me if it's low

Agent: 
  🧠 Thinking: I'll check disk usage with df command
  🟢 Safe action: run_command("df -h")
  ✓ Disk usage: 45% used (120GB free)
  
  Your disk space is healthy. No action needed.
```

### Example 2: Data Analysis

```
You: Analyze sales.xlsx and show me the top 5 products

Agent:
  🧠 Thinking: I'll use pandas to read and analyze the Excel file
  🟡 Caution: Reading file sales.xlsx
  [You approve]
  
  📊 Analysis Results:
  Top 5 Products by Revenue:
  1. Product A - $45,230
  2. Product B - $38,910
  3. Product C - $32,450
  ...
```

### Example 3: SSL Certificate Check

```
You: Check my SSL certificate for example.com

Agent:
  🧠 Thinking: I'll check the SSL certificate status
  🟢 Safe action: check_ssl("example.com")
  
  ✓ Certificate Status:
  - Domain: example.com
  - Issuer: Let's Encrypt
  - Expires: 2025-03-15
  - Days until expiry: 45
  - Status: Valid ✓
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│           USER INPUT                │
│     (Natural Language)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│         AGENT.PY                    │
│  ┌──────────┐  ┌──────────────┐    │
│  │  ReAct   │  │ Multi-Model  │    │
│  │   Loop   │  │ Orchestrator │    │
│  └──────────┘  └──────────────┘    │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────┐ ┌────────┐
│ TOOLS  │ │MEM │ │PROMPTS │
│  .py   │ │.py │ │  .py   │
└────────┘ └────┘ └────────┘
    │        │        │
    └────────┼────────┘
             │
             ▼
      ┌─────────────┐
      │   OLLAMA    │
      │ (Local AI)  │
      └─────────────┘
```

## 📁 Project Structure

```
local_ai_agent/
├── agent.py              # Main agent with ReAct loop
├── tools.py              # 20+ tool implementations
├── memory.py             # SQLite learning system
├── prompts.py            # Advanced prompting templates
├── requirements.txt      # Python dependencies
├── run_agent.bat         # Windows launcher
├── run_agent.sh          # Linux/macOS launcher
├── agent_memory.db       # SQLite database (created on first run)
└── README.md             # This file
```

## 🛠️ Available Tools

### File System
- `read_file` - Read file content
- `write_file` - Write to file
- `list_dir` - List directory contents
- `search_files` - Search for files by pattern
- `delete_file` - Delete files (with confirmation)
- `check_permissions` - Check file permissions

### Command Execution
- `run_command` - Execute system commands (cross-platform)

### Web Access
- `search_web` - DuckDuckGo search
- `scrape_webpage` - Extract webpage content
- `fetch_api` - HTTP API requests
- `download_file` - Download files from URLs

### Package Management
- `install_package` - Install packages (pip, npm, apt, choco, brew)

### Code Execution
- `python_repl` - Execute Python code (with pandas support)

### System Info
- `get_system_info` - OS, CPU, RAM, disk info
- `check_service_status` - Check if service is running
- `monitor_resources` - Monitor CPU/RAM usage

### Docker
- `docker_command` - Execute Docker commands

### Security
- `scan_ports` - Network port scanning
- `check_ssl` - SSL certificate validation

### Custom Tools
- `register_custom_tool` - Add your own tools

## 🧠 Learning System

The agent learns from every interaction:

- **Solutions**: Stores successful problem-solution pairs
- **Custom Tools**: Remembers commands you teach it
- **Packages**: Tracks installed packages and reasons
- **Preferences**: Learns your workflow preferences
- **Error Patterns**: Remembers errors and their solutions

### Memory Statistics

```python
# View memory stats
agent.memory.get_statistics()

# Output:
{
  'total_solutions': 45,
  'total_custom_tools': 8,
  'total_packages': 12,
  'average_rating': 4.7,
  'most_successful_solution': {
    'problem': 'restart nginx',
    'success_count': 23
  }
}
```

## 🔒 Security & Privacy

- ✅ **100% Local**: All processing happens on your server
- ✅ **No Cloud**: Your data never leaves your machine
- ✅ **Explicit Permission**: Every action requires your approval
- ✅ **Risk Assessment**: Color-coded risk levels (🟢🟡🔴)
- ✅ **Audit Log**: Complete history of all actions
- ✅ **Dry-Run Mode**: Preview actions before execution

## 🎯 Model Recommendations

| Model | RAM | Speed | Best For |
|-------|-----|-------|----------|
| Llama 3.1 8B | 8GB | ⚡⚡⚡ Fast | Simple tasks, quick commands |
| Qwen 2.5 7B | 8GB | ⚡⚡⚡ Fast | General purpose |
| DeepSeek Coder 6.7B | 8GB | ⚡⚡⚡ Fast | Code generation |
| Qwen 2.5 14B | 16GB | ⚡⚡ Medium | Balanced performance |
| Llama 3.1 70B | 64GB | ⚡ Slow | Complex reasoning |

The agent automatically selects the best available model based on task complexity.

## 📚 Documentation

- [Implementation Plan (HTML)](../expert_ai_agent_plan.html)
- [Learning Guide (Arabic-English)](../ai_agent_learning_guide_ar_en.html)

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- **Ollama** - For making local AI accessible
- **DuckDuckGo** - For privacy-respecting search
- **Rich** - For beautiful terminal UI

---

**Built with ❤️ for secure, local AI assistance**

🔒 Secure • 🏠 Local • 🧠 Smart • 📈 Self-Improving
