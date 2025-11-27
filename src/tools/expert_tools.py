"""
Expert Tools - أدوات متخصصة للخبراء
Specialized tools for:
- Programming & Development
- Web Design & Frontend
- Server Management
- Docker & Containers
- n8n Workflows
- PostgreSQL & Databases
- DevOps & CI/CD
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime

# Import paths system
from src.core.paths import (
    get_knowledge_base_dir,
    ensure_dir
)


class ExpertTools:
    """
    Expert-level tools for advanced tasks
    أدوات متقدمة للمهام الاحترافية
    """
    
    def __init__(self):
        self.system = os.name
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all expert tools"""
        tools = {
            # Programming Tools
            "create_python_project": "Create a new Python project with structure (args: project_name, include_tests, include_docs)",
            "analyze_code": "Analyze code quality and suggest improvements (args: filepath, language)",
            "generate_code": "Generate code from description (args: description, language, framework)",
            "refactor_code": "Refactor code for better quality (args: filepath, refactor_type)",
            "create_api": "Create REST API boilerplate (args: framework, endpoints)",
            
            # Web Design Tools
            "create_html_template": "Create HTML template (args: template_type, include_css, include_js)",
            "generate_css": "Generate CSS from description (args: description, framework)",
            "create_react_component": "Create React component (args: component_name, props)",
            "optimize_images": "Optimize images for web (args: directory, quality)",
            "generate_responsive_layout": "Generate responsive layout (args: layout_type, breakpoints)",
            
            # Server Management Tools
            "check_server_health": "Check server health and resources (args: server_ip)",
            "manage_nginx": "Manage nginx configuration (args: action, config)",
            "setup_ssl": "Setup SSL certificate (args: domain, email)",
            "monitor_logs": "Monitor and analyze server logs (args: log_file, pattern)",
            "backup_server": "Create server backup (args: backup_path, include_db)",
            
            # Docker Tools
            "create_dockerfile": "Create optimized Dockerfile (args: base_image, app_type)",
            "docker_compose_generate": "Generate docker-compose.yml (args: services, networks)",
            "docker_build": "Build Docker image (args: dockerfile_path, image_name, tag)",
            "docker_deploy": "Deploy Docker container (args: image, ports, volumes)",
            "docker_logs": "Get Docker container logs (args: container_name, lines)",
            "docker_health_check": "Check Docker container health (args: container_name)",
            "docker_cleanup": "Cleanup unused Docker resources (args: remove_images, remove_volumes)",
            
            # n8n Workflow Tools
            "create_n8n_workflow": "Create n8n workflow template (args: workflow_type, nodes)",
            "n8n_api_call": "Make n8n API call (args: endpoint, method, data)",
            "export_n8n_workflow": "Export n8n workflow (args: workflow_id, format)",
            "import_n8n_workflow": "Import n8n workflow (args: workflow_json)",
            "test_n8n_webhook": "Test n8n webhook (args: webhook_url, test_data)",
            
            # PostgreSQL Tools
            "postgres_query": "Execute PostgreSQL query (args: query, database, host, user, password)",
            "postgres_backup": "Backup PostgreSQL database (args: database, output_file)",
            "postgres_restore": "Restore PostgreSQL database (args: database, backup_file)",
            "postgres_create_table": "Create PostgreSQL table (args: table_name, columns, database)",
            "postgres_optimize": "Optimize PostgreSQL database (args: database, vacuum, analyze)",
            "postgres_health": "Check PostgreSQL health (args: host, port, database)",
            
            # DevOps & CI/CD Tools
            "create_github_action": "Create GitHub Actions workflow (args: workflow_name, triggers, jobs)",
            "setup_ci_cd": "Setup CI/CD pipeline (args: platform, project_type)",
            "deploy_to_production": "Deploy to production (args: environment, strategy)",
            "rollback_deployment": "Rollback deployment (args: version, environment)",
            "monitor_deployment": "Monitor deployment status (args: deployment_id)",
            
            # Learning & Documentation Tools
            "search_documentation": "Search official documentation online and get actual content (args: technology, query)",
            "download_tutorial": "Download tutorial/guide for offline use (args: topic, format)",
            "save_code_snippet": "Save code snippet to knowledge base (args: code, language, description, tags)",
            "update_knowledge_base": "Write or append content to knowledge base files (args: technology, content, filename, append)",
            "search_stackoverflow": "Search StackOverflow for solutions (args: query, tags)",
            "learn_new_technology": "Learn new technology online and save knowledge (args: technology, topics)",
            "read_knowledge_base": "Read saved knowledge from local database (args: technology)",
        }
        
        return json.dumps(tools, indent=2)
    
    def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Execute an expert tool"""
        method_name = tool_name
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(**params)
        else:
            return f"Error: Expert tool '{tool_name}' not found"
    
    # ═══════════════════════════════════════════════════════════
    # PROGRAMMING TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def create_python_project(self, project_name: str, include_tests: bool = True, include_docs: bool = True) -> str:
        """Create a new Python project structure"""
        try:
            base_path = Path(project_name)
            base_path.mkdir(exist_ok=True)
            
            # Create structure
            (base_path / "src").mkdir(exist_ok=True)
            (base_path / "src" / "__init__.py").touch()
            
            if include_tests:
                (base_path / "tests").mkdir(exist_ok=True)
                (base_path / "tests" / "__init__.py").touch()
            
            if include_docs:
                (base_path / "docs").mkdir(exist_ok=True)
                (base_path / "docs" / "README.md").write_text(f"# {project_name}\n\nProject documentation")
            
            # Create requirements.txt
            (base_path / "requirements.txt").write_text("# Add your dependencies here\n")
            
            # Create README.md
            (base_path / "README.md").write_text(f"# {project_name}\n\nProject description")
            
            # Create .gitignore
            (base_path / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\nvenv/\n")
            
            return f"✅ Created Python project: {project_name}\nStructure: src/, tests/, docs/, README.md, requirements.txt"
        
        except Exception as e:
            return f"Error creating project: {str(e)}"
    
    def generate_code(self, description: str, language: str = "python", framework: str = None) -> str:
        """Generate code from description"""
        # This would use the AI model to generate code
        # For now, return a template
        templates = {
            "python": f'''# Generated Python code
# Description: {description}

def main():
    """Main function"""
    # TODO: Implement {description}
    pass

if __name__ == "__main__":
    main()
''',
            "javascript": f'''// Generated JavaScript code
// Description: {description}

function main() {{
    // TODO: Implement {description}
}}

main();
''',
        }
        
        return templates.get(language, f"# {description}\n# TODO: Implement")
    
    # ═══════════════════════════════════════════════════════════
    # WEB DESIGN TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def create_html_template(self, template_type: str = "landing", include_css: bool = True, include_js: bool = False) -> str:
        """Create HTML template"""
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template_type.title()} Page</title>
    {f'<link rel="stylesheet" href="style.css">' if include_css else ''}
</head>
<body>
    <header>
        <h1>Welcome</h1>
        <nav>
            <a href="#home">Home</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>
    
    <main>
        <section id="hero">
            <h2>Hero Section</h2>
            <p>Your content here</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2025 Your Company</p>
    </footer>
    
    {f'<script src="script.js"></script>' if include_js else ''}
</body>
</html>'''
        
        return html
    
    # ═══════════════════════════════════════════════════════════
    # DOCKER TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def create_dockerfile(self, base_image: str = "python:3.11-slim", app_type: str = "web") -> str:
        """Create optimized Dockerfile"""
        dockerfile = f'''# Dockerfile for {app_type} application
FROM {base_image}

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
'''
        return dockerfile
    
    def docker_compose_generate(self, services: List[str], networks: List[str] = None) -> str:
        """Generate docker-compose.yml"""
        compose = '''version: '3.8'

services:
'''
        
        for service in services:
            if service == "postgres":
                compose += '''  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: database
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

'''
            elif service == "n8n":
                compose += '''  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
    volumes:
      - n8n_data:/home/node/.n8n

'''
            elif service == "app":
                compose += '''  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/database

'''
        
        compose += '''
volumes:
  postgres_data:
  n8n_data:
'''
        
        return compose
    
    # ═══════════════════════════════════════════════════════════
    # POSTGRESQL TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def postgres_query(self, query: str, database: str = "postgres", host: str = "localhost", 
                      user: str = "postgres", password: str = None) -> str:
        """Execute PostgreSQL query"""
        try:
            import psycopg2
            
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            
            cur = conn.cursor()
            cur.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cur.fetchall()
                conn.close()
                return json.dumps(results, indent=2)
            else:
                conn.commit()
                conn.close()
                return "✅ Query executed successfully"
        
        except ImportError:
            return "Error: psycopg2 not installed. Install with: pip install psycopg2-binary"
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # LEARNING TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def search_documentation(self, technology: str, query: str) -> str:
        """Search official documentation online and fetch actual content"""
        try:
            # Use the search_web tool from Tools class to get real content
            from src.tools.tools import Tools
            tools = Tools()
            
            # Search for documentation
            search_query = f"{technology} {query} documentation"
            results = tools.search_web(search_query, max_results=3)
            
            if results and isinstance(results, list) and len(results) > 0:
                content = f"📚 Documentation Search Results for {technology} ({query}):\n\n"
                for i, result in enumerate(results[:3], 1):
                    title = result.get('title', 'No title')
                    snippet = result.get('body', result.get('snippet', 'No description'))
                    url = result.get('href', result.get('url', 'No URL'))
                    content += f"{i}. **{title}**\n"
                    content += f"   {snippet[:200]}...\n"
                    content += f"   🔗 {url}\n\n"
                
                return content
            else:
                # Fallback to URL if search fails
                doc_urls = {
                    "docker": "https://docs.docker.com",
                    "postgres": "https://www.postgresql.org/docs/",
                    "n8n": "https://docs.n8n.io",
                    "python": "https://docs.python.org/3/",
                    "javascript": "https://developer.mozilla.org",
                }
                base_url = doc_urls.get(technology.lower(), f"https://www.google.com/search?q={technology}+documentation")
                return f"📚 Documentation for {technology}:\n{base_url}\nSearch query: {query}\n\n(Note: Web search unavailable, showing URL only)"
        except Exception as e:
            # Fallback on error
            doc_urls = {
                "docker": "https://docs.docker.com",
                "postgres": "https://www.postgresql.org/docs/",
                "n8n": "https://docs.n8n.io",
                "python": "https://docs.python.org/3/",
                "javascript": "https://developer.mozilla.org",
            }
            base_url = doc_urls.get(technology.lower(), f"https://www.google.com/search?q={technology}+documentation")
            return f"📚 Documentation for {technology}:\n{base_url}\nSearch query: {query}\n\n(Error: {str(e)})"
    
    def learn_new_technology(self, technology: str, topics: List[str]) -> str:
        """Learn new technology online using Fast Learning and save REAL knowledge immediately"""
        try:
            # Use Fast Learning module
            print(f"🚀 Fast Learning initiated for {technology}...")
            results = self.fast_learner.learn_fast(technology, topics)
            
            # Save to knowledge base
            save_msg = self.fast_learner.save_to_knowledge_base(results)
            
            return f"""
🎉 Successfully learned {technology} using Fast Learning!

{save_msg}

� Summary:
{results['summary'][:500]}...

💡 You can now ask questions about {technology}!
"""
        except Exception as e:
            return f"Error learning technology: {str(e)}"
    
    def read_knowledge_base(self, technology: str) -> str:
        """Read saved knowledge about a technology"""
        try:
            # Use centralized knowledge base path
            kb_dir = get_knowledge_base_dir() / technology.lower().replace(" ", "_")
            
            if not kb_dir.exists():
                return f"❌ No knowledge found for {technology}. Try learning it first using: learn_new_technology('{technology}', ...)"
            
            files = list(kb_dir.glob("*"))
            if not files:
                return f"⚠️ Knowledge directory for {technology} is empty."
            
            content = f"📂 Knowledge for {technology}:\n"
            
            for file in files:
                content += f"\n--- {file.name} ---\n"
                try:
                    content += file.read_text(encoding='utf-8')[:1000]  # Read first 1000 chars
                    if len(file.read_text(encoding='utf-8')) > 1000:
                        content += "\n... (truncated)"
                except Exception:
                    content += "(Binary or unreadable file)"
                content += "\n"
            
            return content
        except Exception as e:
            return f"Error reading knowledge base: {str(e)}"

    def save_code_snippet(self, code: str, language: str, description: str, tags: List[str] = None) -> str:
        """Save code snippet to knowledge base"""
        try:
            # Use centralized knowledge base path
            snippets_dir = get_knowledge_base_dir() / "snippets"
            ensure_dir(snippets_dir)
            
            # Create snippet file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{language}_{timestamp}.json"
            
            snippet_data = {
                "code": code,
                "language": language,
                "description": description,
                "tags": tags or [],
                "created_at": datetime.now().isoformat()
            }
            
            snippet_file = snippets_dir / filename
            snippet_file.write_text(json.dumps(snippet_data, indent=2))
            
            return f"✅ Code snippet saved: {filename}\nLocation: {snippet_file}"
        
        except Exception as e:
            return f"Error saving snippet: {str(e)}"
    
    def update_knowledge_base(self, technology: str, content: str, filename: str = "overview.md", append: bool = False) -> str:
        """
        Update or append content to knowledge base files.
        
        Args:
            technology: Technology name (e.g., "Docker")
            content: Content to write/append
            filename: File name (default: overview.md)
            append: If True, append to file; if False, overwrite
        
        Returns:
            Success message
        """
        try:
            # Use centralized knowledge base path
            kb_dir = get_knowledge_base_dir() / technology.lower().replace(" ", "_")
            ensure_dir(kb_dir)
            
            file_path = kb_dir / filename
            
            if append and file_path.exists():
                # Append with separator
                existing_content = file_path.read_text(encoding='utf-8')
                new_content = f"{existing_content}\n\n--- Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n\n{content}"
            else:
                # Overwrite or create new
                new_content = content
            
            file_path.write_text(new_content, encoding='utf-8')
            
            action = "appended to" if append else "written to"
            return f"✅ Content {action} {file_path}\nSize: {len(new_content)} characters"
        
        except Exception as e:
            return f"Error updating knowledge base: {str(e)}"
    
    def search_stackoverflow(self, query: str, tags: List[str] = None) -> str:
        """Search StackOverflow for solutions"""
        try:
            # Use StackExchange API
            base_url = "https://api.stackexchange.com/2.3/search/advanced"
            params = {
                "order": "desc",
                "sort": "relevance",
                "q": query,
                "site": "stackoverflow"
            }
            
            if tags:
                params["tagged"] = ";".join(tags)
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])[:5]  # Top 5 results
                
                results = "🔍 StackOverflow Results:\n\n"
                for i, item in enumerate(items, 1):
                    results += f"{i}. {item['title']}\n"
                    results += f"   Link: {item['link']}\n"
                    results += f"   Score: {item['score']} | Answers: {item['answer_count']}\n\n"
                
                return results
            else:
                return f"Error: Could not search StackOverflow (Status: {response.status_code})"
        
        except Exception as e:
            return f"Error searching StackOverflow: {str(e)}"


# Test
if __name__ == "__main__":
    from datetime import datetime
    tools = ExpertTools()
    print(tools.get_tool_descriptions())
