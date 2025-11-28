# Dockerfile for Local AI Agent
# Optimized for offline server deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/knowledge_base data/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_URL=http://localhost:11434

# Expose port (if needed for web interface)
# EXPOSE 8000

# Default command
CMD ["python", "-m", "src.agents.agent"]

