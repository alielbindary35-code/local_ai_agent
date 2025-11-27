"""
Generate Colab Notebook
=======================

Generates a Google Colab notebook for running the agent in the cloud.
"""

import json
from pathlib import Path

def generate_notebook():
    notebook = {
      "nbformat": 4,
      "nbformat_minor": 0,
      "metadata": {
        "colab": {
          "provenance": [],
          "gpuType": "T4"
        },
        "kernelspec": {
          "name": "python3",
          "display_name": "Python 3"
        },
        "language_info": {
          "name": "python"
        }
      },
      "cells": [
        {
          "cell_type": "markdown",
          "metadata": {
            "id": "view-in-github",
            "colab_type": "text"
          },
          "source": [
            "# 🤖 Local AI Agent - Cloud Edition\n",
            "\n",
            "Run your AI agent on Google Colab's powerful hardware.\n",
            "\n",
            "### 🚀 Setup Instructions\n",
            "\n",
            "**Before running this notebook:**\n",
            "1. Push your project to GitHub (see DEPLOYMENT_GUIDE.md)\n",
            "2. Update the GitHub URL in Cell 1 (replace YOUR_USERNAME)\n",
            "3. Run all cells in order\n",
            "\n",
            "**Benefits of Colab:**\n",
            "- ⚡ Faster learning with cloud resources\n",
            "- 💾 Free storage for knowledge base\n",
            "- 🔄 Easy sharing and collaboration\n",
            "- 📊 Built-in visualization tools"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {
            "id": "setup-cell"
          },
          "outputs": [],
          "source": [
            "# @title 🛠️ Setup Environment\n",
            "\n",
            "# 1. Install Dependencies\n",
            "!pip install -q rich duckduckgo-search requests beautifulsoup4 lxml\n",
            "\n",
            "# 2. Clone Repository from GitHub\n",
            "# Replace YOUR_USERNAME with your GitHub username\n",
            "# If repository is private, use: !git clone https://YOUR_TOKEN@github.com/YOUR_USERNAME/local_ai_agent.git\n",
            "!git clone https://github.com/YOUR_USERNAME/local_ai_agent.git\n",
            "%cd local_ai_agent\n",
            "\n",
            "# 3. Add project root to Python path (IMPORTANT for imports)\n",
            "import sys\n",
            "import os\n",
            "from pathlib import Path\n",
            "\n",
            "# Add current directory to Python path\n",
            "project_root = os.getcwd()\n",
            "if project_root not in sys.path:\n",
            "    sys.path.insert(0, project_root)\n",
            "\n",
            "# 4. Verify Setup and JSON files\n",
            "import json\n",
            "print(f\"Python {sys.version}\")\n",
            "print(f\"Current directory: {project_root}\")\n",
            "print(f\"Python path includes project: {project_root in sys.path}\")\n",
            "print(f\"Project exists: {Path('src/tools/auto_learner.py').exists()}\")\n",
            "\n",
            "# Verify JSON files are valid\n",
            "tools_file = Path('data/essential_tools.json')\n",
            "if tools_file.exists():\n",
            "    try:\n",
            "        content = tools_file.read_text(encoding='utf-8').strip()\n",
            "        json.loads(content)\n",
            "        print(\"OK: essential_tools.json is valid\")\n",
            "    except Exception as e:\n",
            "        print(f\"ERROR: essential_tools.json is invalid: {e}\")\n",
            "else:\n",
            "    print(\"WARNING: essential_tools.json not found\")\n",
            "\n",
            "print(\"Environment Ready!\")"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {
            "id": "run-learning"
          },
          "outputs": [],
          "source": [
            "# @title 🎓 Run Auto-Learner (Learn ALL Tools)\n",
            "\n",
            "# Ensure project root is in Python path\n",
            "import sys\n",
            "import os\n",
            "if os.getcwd() not in sys.path:\n",
            "    sys.path.insert(0, os.getcwd())\n",
            "\n",
            "# This will learn ALL tools in data/essential_tools.json\n",
            "# Time: ~15-20 minutes for all 122 tools\n",
            "from src.tools.auto_learner import AutoLearner\n",
            "\n",
            "learner = AutoLearner()\n",
            "learner.learn_all()  # Learns ALL 122+ tools!"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {
            "id": "download-kb"
          },
          "outputs": [],
          "source": [
            "# @title 💾 Download Complete Knowledge Base\n",
            "\n",
            "import shutil\n",
            "import json\n",
            "from pathlib import Path\n",
            "from google.colab import files\n",
            "\n",
            "# Zip the knowledge base\n",
            "shutil.make_archive('knowledge_base_complete', 'zip', 'data/knowledge_base')\n",
            "\n",
            "# Also save progress file\n",
            "if Path('data/learning_progress.json').exists():\n",
            "    shutil.copy('data/learning_progress.json', 'learning_progress.json')\n",
            "    files.download('learning_progress.json')\n",
            "\n",
            "# Download knowledge base\n",
            "files.download('knowledge_base_complete.zip')\n",
            "\n",
            "# Show summary\n",
            "if Path('data/learning_progress.json').exists():\n",
            "    try:\n",
            "        content = Path('data/learning_progress.json').read_text(encoding='utf-8').strip()\n",
            "        if content:\n",
            "            progress = json.loads(content)\n",
            "            print(f\"OK: Downloaded {len(progress)} learned tools!\")\n",
            "            print(f\"Knowledge base ready for merge!\")\n",
            "        else:\n",
            "            print(\"Progress file is empty\")\n",
            "    except json.JSONDecodeError as e:\n",
            "        print(f\"WARNING: Invalid JSON in progress file: {e}\")\n",
            "    except Exception as e:\n",
            "        print(f\"WARNING: Error reading progress: {e}\")"
          ]
        }
      ]
    }
    
    # Create notebooks directory
    Path("notebooks").mkdir(exist_ok=True)
    
    # Save file
    output_file = Path("notebooks/Agent_On_Colab.ipynb")
    output_file.write_text(json.dumps(notebook, indent=2))
    print(f"✅ Generated notebook: {output_file}")

if __name__ == "__main__":
    generate_notebook()
