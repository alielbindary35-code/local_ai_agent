#!/bin/bash
# Expert-Level Local AI Agent - Linux/macOS Launcher

echo ""
echo "========================================"
echo "  Expert-Level Local AI Agent"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "[OK] Python found"
python3 --version

# Check if Ollama is running
echo ""
echo "Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "[WARNING] Cannot connect to Ollama at http://localhost:11434"
    echo "Please make sure Ollama is running."
    echo ""
    echo "To start Ollama:"
    echo "  1. Open a new terminal"
    echo "  2. Run: ollama serve"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[WARNING] Some dependencies failed to install"
    echo "The agent may still work with core dependencies"
    echo ""
fi

# Run the agent
echo ""
echo "========================================"
echo "  Starting Agent..."
echo "========================================"
echo ""

# Change to script directory to ensure relative paths work
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD:$PYTHONPATH"

python src/agents/agent.py

# Deactivate virtual environment on exit
deactivate

echo ""
echo "Agent stopped."
