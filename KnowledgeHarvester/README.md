# Knowledge Harvester

A standalone tool to download, organize, and process technical documentation for AI agent knowledge enhancement.

## Features
- Downloads documentation from configured URLs (Docker, PostgreSQL, n8n, Ollama, etc.)
- Supports HTML, PDF, and Markdown/GitHub sources
- Automatically converts HTML to clean Markdown
- Extracts text from PDFs
- Organizes content into categorized folders
- Generates metadata for each downloaded item

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure sources in `config.yaml`.

## Usage

Run the harvester:
```bash
python knowledge_harvester.py
```

Download a specific category only:
```bash
python knowledge_harvester.py --category docker
```

## Output Structure
- `data/materials/`: Original downloaded files (HTML, PDF)
- `data/extracted/`: Processed Markdown files
- `data/metadata/`: JSON metadata for each file
- `logs/`: Operation logs
