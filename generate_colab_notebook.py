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
            "1. Upload your project files to Colab (or clone from GitHub)\n",
            "2. Run the setup cell below\n",
            "3. Start learning!"
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
            "!pip install -q rich duckduckgo-search requests\n",
            "\n",
            "# 2. Clone Repository (If using GitHub)\n",
            "# !git clone https://github.com/YOUR_USERNAME/local_ai_agent.git\n",
            "# %cd local_ai_agent\n",
            "\n",
            "# 3. Verify Setup\n",
            "import sys\n",
            "import os\n",
            "print(f\"Python {sys.version}\")\n",
            "print(\"✅ Environment Ready!\")"
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
            "# @title 🎓 Run Auto-Learner\n",
            "\n",
            "# This will learn all tools in data/essential_tools.json\n",
            "from src.tools.auto_learner import AutoLearner\n",
            "\n",
            "learner = AutoLearner()\n",
            "learner.learn_all()"
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
            "# @title 💾 Download Knowledge Base\n",
            "\n",
            "import shutil\n",
            "from google.colab import files\n",
            "\n",
            "# Zip the knowledge base\n",
            "shutil.make_archive('knowledge_base', 'zip', 'data/knowledge_base')\n",
            "\n",
            "# Download\n",
            "files.download('knowledge_base.zip')"
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
