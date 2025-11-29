# Desktop Application - Local AI Agent

Desktop application for the Local AI Agent built with PyQt6.

## Features

- 💬 **Chat Interface**: Interactive chat with message bubbles and history
- 📁 **File Manager**: Browse files with tree view and preview
- 📝 **Code Editor**: Syntax highlighting and multi-tab editing
- 📊 **Dashboard**: Real-time statistics and metrics
- ⚙️ **Settings**: Comprehensive configuration panel

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python desktop_app/main.py
```

## Requirements

- Python 3.8+
- PyQt6
- Ollama running locally
- At least one Ollama model installed

## Usage

### Starting the Application

```bash
cd local_ai_agent
python desktop_app/main.py
```

### Keyboard Shortcuts

- `Ctrl+N`: New chat
- `Ctrl+Q`: Quit
- `Ctrl+1`: Switch to Chat tab
- `Ctrl+2`: Switch to File Manager tab
- `Ctrl+3`: Switch to Code Editor tab
- `Ctrl+4`: Switch to Dashboard tab
- `Ctrl+,`: Open Settings
- `Ctrl+Enter`: Send message in chat

## Architecture

```
desktop_app/
├── main.py              # Entry point
├── ui/                  # UI components
│   ├── main_window.py   # Main window
│   ├── chat_widget.py   # Chat interface
│   ├── file_manager.py  # File browser
│   ├── code_editor.py   # Code editor
│   ├── dashboard.py     # Dashboard
│   └── settings.py      # Settings panel
├── core/                # Core functionality
│   └── agent_bridge.py  # Bridge to agents
├── widgets/             # Custom widgets
│   └── message_bubble.py # Chat message widget
└── styles.py            # Application styles
```

## Features Details

### Chat Interface
- Real-time streaming responses
- Markdown rendering
- Message history
- Agent mode switching (Simple/Expert)

### File Manager
- File tree navigation
- File preview
- Quick actions (open, delete)
- Path navigation

### Code Editor
- Syntax highlighting (Python)
- Multi-tab support
- Save/Load files
- Run code directly

### Dashboard
- System resources monitoring
- Memory statistics
- Knowledge base statistics
- Recent activity

### Settings
- Agent configuration
- UI preferences
- Path settings
- Advanced options

## Troubleshooting

### Application won't start
- Check if PyQt6 is installed: `pip install PyQt6`
- Verify Ollama is running: `ollama list`
- Check Python version: `python --version` (should be 3.8+)

### Chat not working
- Ensure Ollama is running on `http://localhost:11434`
- Check if at least one model is installed
- Verify agent initialization in logs

### File Manager not showing files
- Check file permissions
- Verify path is accessible
- Try refreshing the view

## Development

### Adding New Features

1. Create new widget in `ui/` directory
2. Add to main window in `main.py`
3. Connect signals/slots as needed
4. Update styles if needed

### Customization

- Themes: Edit `styles.py` for light/dark themes
- Settings: Add new settings in `ui/settings.py`
- Widgets: Create custom widgets in `widgets/` directory

## License

MIT License - Same as main project

