"""
Extended Expert Tools - More specialized tools
Additional 30+ tools for advanced operations
"""

import subprocess
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from datetime import datetime


class ExtendedTools:
    """Extended tools for more specialized tasks"""
    
    def __init__(self):
        self.system = os.name
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all extended tools"""
        tools = {
            # Git & Version Control (10 tools)
            "git_init": "Initialize git repository (args: directory)",
            "git_clone": "Clone git repository (args: url, destination)",
            "git_commit": "Create git commit (args: message, files)",
            "git_push": "Push to remote repository (args: remote, branch)",
            "git_pull": "Pull from remote repository (args: remote, branch)",
            "git_branch": "Create or switch branch (args: branch_name, create)",
            "git_merge": "Merge branches (args: source_branch, target_branch)",
            "git_status": "Get git status (args: directory)",
            "git_log": "Get git log (args: directory, limit)",
            "git_diff": "Show git diff (args: file, commit)",
            
            # Testing & Quality (8 tools)
            "run_pytest": "Run pytest tests (args: directory, verbose)",
            "run_unittest": "Run unittest tests (args: module)",
            "run_coverage": "Run code coverage analysis (args: directory)",
            "run_linter": "Run code linter (args: filepath, linter_type)",
            "run_formatter": "Format code (args: filepath, formatter)",
            "run_type_checker": "Run type checker (args: directory)",
            "generate_test": "Generate test cases (args: function_name, test_type)",
            "run_security_scan": "Scan for security vulnerabilities (args: directory)",
            
            # API & HTTP Tools (6 tools)
            "test_api_endpoint": "Test API endpoint (args: url, method, headers, body)",
            "generate_api_docs": "Generate API documentation (args: api_file, format)",
            "create_webhook": "Create webhook handler (args: url, secret)",
            "test_webhook": "Test webhook (args: webhook_url, payload)",
            "monitor_api": "Monitor API health (args: endpoints, interval)",
            "create_graphql_schema": "Create GraphQL schema (args: types, queries)",
            
            # Database Tools (8 tools)
            "mysql_query": "Execute MySQL query (args: query, database, host, user, password)",
            "mongodb_query": "Execute MongoDB query (args: collection, query, database)",
            "redis_get": "Get value from Redis (args: key, host, port)",
            "redis_set": "Set value in Redis (args: key, value, host, port)",
            "sqlite_query": "Execute SQLite query (args: query, database_file)",
            "create_migration": "Create database migration (args: migration_name, database_type)",
            "run_migration": "Run database migration (args: migration_file, database)",
            "seed_database": "Seed database with test data (args: database, seed_file)",
            
            # Cloud & Infrastructure (6 tools)
            "aws_s3_upload": "Upload file to AWS S3 (args: file_path, bucket, key)",
            "aws_s3_download": "Download file from AWS S3 (args: bucket, key, destination)",
            "aws_lambda_deploy": "Deploy AWS Lambda function (args: function_name, code_path)",
            "gcp_storage_upload": "Upload to Google Cloud Storage (args: file_path, bucket)",
            "azure_blob_upload": "Upload to Azure Blob Storage (args: file_path, container)",
            "check_cloud_costs": "Check cloud service costs (args: provider, service)",
            
            # Monitoring & Logging (5 tools)
            "setup_prometheus": "Setup Prometheus monitoring (args: targets, config)",
            "setup_grafana": "Setup Grafana dashboard (args: datasources, dashboards)",
            "create_alert": "Create monitoring alert (args: metric, threshold, action)",
            "analyze_logs": "Analyze log files (args: log_file, pattern, time_range)",
            "export_metrics": "Export system metrics (args: metrics, format, destination)",
            
            # Security & Authentication (5 tools)
            "generate_jwt": "Generate JWT token (args: payload, secret, expiry)",
            "verify_jwt": "Verify JWT token (args: token, secret)",
            "hash_password": "Hash password securely (args: password, algorithm)",
            "generate_api_key": "Generate API key (args: length, prefix)",
            "setup_oauth": "Setup OAuth authentication (args: provider, client_id, client_secret)",
            
            # File Processing (6 tools)
            "convert_image": "Convert image format (args: input_file, output_format)",
            "resize_image": "Resize image (args: input_file, width, height)",
            "compress_file": "Compress file/directory (args: source, output_file, format)",
            "extract_archive": "Extract archive file (args: archive_file, destination)",
            "convert_video": "Convert video format (args: input_file, output_format)",
            "extract_audio": "Extract audio from video (args: video_file, output_file)",
            
            # Data Processing (6 tools)
            "parse_json": "Parse and validate JSON (args: json_string, schema)",
            "parse_xml": "Parse XML file (args: xml_file, xpath)",
            "parse_csv": "Parse CSV file (args: csv_file, delimiter)",
            "convert_json_to_csv": "Convert JSON to CSV (args: json_file, output_file)",
            "convert_csv_to_json": "Convert CSV to JSON (args: csv_file, output_file)",
            "validate_schema": "Validate data against schema (args: data, schema_file)",
            
            # Network & Communication (5 tools)
            "ping_host": "Ping network host (args: host, count)",
            "traceroute": "Trace route to host (args: host)",
            "dns_lookup": "DNS lookup (args: domain, record_type)",
            "check_port": "Check if port is open (args: host, port)",
            "send_email": "Send email (args: to, subject, body, smtp_server)",
            
            # Automation & Scheduling (4 tools)
            "create_cron_job": "Create cron job (args: command, schedule)",
            "create_systemd_service": "Create systemd service (args: service_name, command)",
            "schedule_task": "Schedule task (args: task_name, command, time)",
            "run_background_task": "Run task in background (args: command, log_file)",
        }
        
        return json.dumps(tools, indent=2)
    
    def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Execute an extended tool"""
        method_name = tool_name
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(**params)
        else:
            return f"Error: Extended tool '{tool_name}' not found"
    
    # ═══════════════════════════════════════════════════════════
    # GIT TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def git_init(self, directory: str = ".") -> str:
        """Initialize git repository"""
        try:
            result = subprocess.run(
                ["git", "init"],
                cwd=directory,
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def git_status(self, directory: str = ".") -> str:
        """Get git status"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=directory,
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def git_commit(self, message: str, files: List[str] = None, directory: str = ".") -> str:
        """Create git commit"""
        try:
            # Add files
            if files:
                for file in files:
                    subprocess.run(["git", "add", file], cwd=directory)
            else:
                subprocess.run(["git", "add", "."], cwd=directory)
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=directory,
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # TESTING TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def run_pytest(self, directory: str = ".", verbose: bool = True) -> str:
        """Run pytest tests"""
        try:
            cmd = ["pytest"]
            if verbose:
                cmd.append("-v")
            cmd.append(directory)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            return result.stdout + result.stderr
        except FileNotFoundError:
            return "Error: pytest not installed. Install with: pip install pytest"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run_linter(self, filepath: str, linter_type: str = "pylint") -> str:
        """Run code linter"""
        try:
            linters = {
                "pylint": ["pylint", filepath],
                "flake8": ["flake8", filepath],
                "black": ["black", "--check", filepath],
                "eslint": ["eslint", filepath]
            }
            
            cmd = linters.get(linter_type)
            if not cmd:
                return f"Error: Unknown linter type: {linter_type}"
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            return result.stdout + result.stderr
        except FileNotFoundError:
            return f"Error: {linter_type} not installed"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # DATABASE TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def sqlite_query(self, query: str, database_file: str) -> str:
        """Execute SQLite query"""
        try:
            import sqlite3
            
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                conn.close()
                return json.dumps(results, indent=2)
            else:
                conn.commit()
                conn.close()
                return "✅ Query executed successfully"
        except ImportError:
            return "Error: sqlite3 not available"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # FILE PROCESSING TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def compress_file(self, source: str, output_file: str, format: str = "zip") -> str:
        """Compress file or directory"""
        try:
            if format == "zip":
                shutil.make_archive(output_file.replace('.zip', ''), 'zip', source)
            elif format == "tar":
                shutil.make_archive(output_file.replace('.tar.gz', ''), 'gztar', source)
            else:
                return f"Error: Unsupported format: {format}"
            
            return f"✅ Compressed to {output_file}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def extract_archive(self, archive_file: str, destination: str = ".") -> str:
        """Extract archive file"""
        try:
            shutil.unpack_archive(archive_file, destination)
            return f"✅ Extracted to {destination}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # DATA PROCESSING TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def parse_json(self, json_string: str, schema: Dict = None) -> str:
        """Parse and validate JSON"""
        try:
            data = json.loads(json_string)
            
            if schema:
                # Basic schema validation
                for key in schema.get('required', []):
                    if key not in data:
                        return f"Error: Missing required field: {key}"
            
            return json.dumps(data, indent=2)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def convert_json_to_csv(self, json_file: str, output_file: str) -> str:
        """Convert JSON to CSV"""
        try:
            import csv
            
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                data = [data]
            
            if not data:
                return "Error: Empty JSON data"
            
            keys = data[0].keys()
            
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
            return f"✅ Converted to {output_file}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # NETWORK TOOLS
    # ═══════════════════════════════════════════════════════════
    
    def ping_host(self, host: str, count: int = 4) -> str:
        """Ping network host"""
        try:
            param = "-n" if os.name == "nt" else "-c"
            result = subprocess.run(
                ["ping", param, str(count), host],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_port(self, host: str, port: int) -> str:
        """Check if port is open"""
        try:
            import socket
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return f"✅ Port {port} is OPEN on {host}"
            else:
                return f"❌ Port {port} is CLOSED on {host}"
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    tools = ExtendedTools()
    print(tools.get_tool_descriptions())
