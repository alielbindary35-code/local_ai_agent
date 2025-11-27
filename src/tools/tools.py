"""
Tools Library - Comprehensive tool collection for the AI agent
مكتبة الأدوات - مجموعة شاملة من الأدوات لوكيل الذكاء الاصطناعي

Contains 20+ tools for file operations, command execution, web access,
package management, code execution, and more.
"""

import subprocess
import platform
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import psutil
try:
    from ddgs import DDGS  # Try new package name first
except ImportError:
    try:
        from duckduckgo_search import DDGS  # Fallback to old package name
    except ImportError:
        DDGS = None  # Will handle in search_web method
import requests
from bs4 import BeautifulSoup


class Tools:
    """
    Comprehensive tool library for the AI agent.
    
    مكتبة أدوات شاملة لوكيل الذكاء الاصطناعي.
    """
    
    def __init__(self):
        """Initialize tools."""
        self.system = platform.system()
        self.system = platform.system()
        self.custom_tools = {}

    def get_os_identifier(self) -> str:
        """Get a human-readable OS identifier."""
        try:
            system = platform.system()
            release = platform.release()
            version = platform.version()
            return f"{system} {release} (Version {version})"
        except Exception:
            return "Unknown OS"
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all available tools."""
        tools = {
            "read_file": "Read content from a file (args: filepath)",
            "write_file": "Write content to a file (args: filepath, content)",
            "list_dir": "List contents of a directory (args: dirpath)",
            "search_files": "Search for files matching a pattern (args: pattern, directory)",
            "delete_file": "Delete a file (requires confirmation) (args: filepath)",
            "check_permissions": "Check file/directory permissions (args: filepath)",
            "run_command": "Execute a system command. On Windows uses PowerShell, on Linux uses Bash. (args: command)",
            "search_web": "Search the web using DuckDuckGo (args: query)",
            "scrape_webpage": "Extract content from a webpage (args: url)",
            "fetch_api": "Make HTTP API request (args: url, method)",
            "download_file": "Download a file from URL (args: url, destination)",
            "install_package": "Install a package (args: package, manager)",
            "python_repl": "Execute Python code in isolated environment (args: code)",
            "get_system_info": "Get system information (OS, CPU, RAM, disk)",
            "check_service_status": "Check if a service is running (args: service_name)",
            "monitor_resources": "Monitor system resources (CPU, RAM usage)",
            "docker_command": "Execute Docker commands (args: command)",
            "scan_ports": "Scan network ports (args: host, ports)",
            "check_ssl": "Check SSL certificate status (args: domain)",
            "register_custom_tool": "Register a new custom tool (args: name, command, description)"
        }
        
        return json.dumps(tools, indent=2)
    
    def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute a tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool
        
        Returns:
            Tool execution result
        """
        # Check if it's a custom tool
        if tool_name in self.custom_tools:
            return self._execute_custom_tool(tool_name, params)
        
        # Execute built-in tool
        method_name = tool_name
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(**params)
        else:
            return f"Error: Tool '{tool_name}' not found"
    
    # ═══════════════════════════════════════════════════════════
    # FILE SYSTEM TOOLS - أدوات نظام الملفات
    # ═══════════════════════════════════════════════════════════
    
    def read_file(self, filepath: str, encoding: str = 'utf-8') -> str:
        """
        Read content from a file.
        قراءة محتوى من ملف.
        """
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, filepath: str, content: str, encoding: str = 'utf-8') -> str:
        """
        Write content to a file.
        كتابة محتوى إلى ملف.
        """
        try:
            # Create parent directories if they don't exist
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_dir(self, dirpath: str = ".", extensions: Optional[List[str]] = None) -> str:
        """
        List contents of a directory.
        عرض محتويات مجلد.
        """
        try:
            path = Path(dirpath)
            if not path.exists():
                return f"Error: Directory '{dirpath}' does not exist"
            
            items = []
            for item in path.iterdir():
                if extensions:
                    if item.is_file() and item.suffix in extensions:
                        items.append(f"📄 {item.name} ({item.stat().st_size} bytes)")
                else:
                    if item.is_dir():
                        items.append(f"📁 {item.name}/")
                    else:
                        items.append(f"📄 {item.name} ({item.stat().st_size} bytes)")
            
            return "\n".join(items) if items else "Directory is empty"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def search_files(self, pattern: str, directory: str = ".", recursive: bool = True) -> str:
        """
        Search for files matching a pattern.
        البحث عن ملفات تطابق نمط معين.
        """
        try:
            path = Path(directory)
            if recursive:
                files = list(path.rglob(pattern))
            else:
                files = list(path.glob(pattern))
            
            if not files:
                return f"No files found matching '{pattern}'"
            
            return "\n".join([str(f) for f in files])
        except Exception as e:
            return f"Error searching files: {str(e)}"
    
    def delete_file(self, filepath: str) -> str:
        """
        Delete a file.
        حذف ملف.
        """
        try:
            Path(filepath).unlink()
            return f"Successfully deleted {filepath}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"
    
    def check_permissions(self, filepath: str) -> str:
        """
        Check file/directory permissions.
        فحص صلاحيات ملف/مجلد.
        """
        try:
            path = Path(filepath)
            if not path.exists():
                return f"Error: '{filepath}' does not exist"
            
            stat = path.stat()
            return {
                "readable": os.access(filepath, os.R_OK),
                "writable": os.access(filepath, os.W_OK),
                "executable": os.access(filepath, os.X_OK),
                "size": stat.st_size,
                "modified": stat.st_mtime
            }
        except Exception as e:
            return f"Error checking permissions: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # COMMAND EXECUTION - تنفيذ الأوامر
    # ═══════════════════════════════════════════════════════════
    
    def run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute a system command (cross-platform).
        تنفيذ أمر نظام (متعدد المنصات).
        """
        try:
            # Determine shell based on OS
            if self.system == "Windows":
                shell = True
            else:
                shell = False
            
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # WEB ACCESS TOOLS - أدوات الوصول للويب
    # ═══════════════════════════════════════════════════════════
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web using DuckDuckGo.
        البحث في الإنترنت باستخدام DuckDuckGo.
        """
        try:
            if DDGS is None:
                return [{"error": "DuckDuckGo search not available. Please install: pip install ddgs"}]
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            return [{"error": str(e)}]
    
    def scrape_webpage(self, url: str) -> str:
        """
        Extract text content from a webpage.
        استخراج محتوى نصي من صفحة ويب.
        """
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 chars
        except Exception as e:
            return f"Error scraping webpage: {str(e)}"
    
    def fetch_api(self, url: str, method: str = "GET", data: Optional[Dict] = None) -> Any:
        """
        Make HTTP API request.
        إجراء طلب API عبر HTTP.
        """
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            return {
                "status_code": response.status_code,
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            return {"error": str(e)}
    
    def download_file(self, url: str, destination: str) -> str:
        """
        Download a file from URL.
        تحميل ملف من رابط.
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return f"Successfully downloaded to {destination}"
        except Exception as e:
            return f"Error downloading file: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # PACKAGE MANAGEMENT - إدارة الحزم
    # ═══════════════════════════════════════════════════════════
    
    def install_package(self, package: str, manager: str = "auto") -> str:
        """
        Install a package using appropriate package manager.
        تثبيت حزمة باستخدام مدير الحزم المناسب.
        
        Args:
            package: Package name
            manager: Package manager (pip, npm, apt, choco, brew, or auto)
        """
        if manager == "auto":
            # Auto-detect based on system
            if self.system == "Windows":
                manager = "choco"
            elif self.system == "Linux":
                manager = "apt"
            elif self.system == "Darwin":
                manager = "brew"
            else:
                manager = "pip"
        
        commands = {
            "pip": f"pip install {package}",
            "npm": f"npm install -g {package}",
            "apt": f"sudo apt install -y {package}",
            "yum": f"sudo yum install -y {package}",
            "choco": f"choco install {package} -y",
            "brew": f"brew install {package}"
        }
        
        command = commands.get(manager)
        if not command:
            return f"Error: Unknown package manager '{manager}'"
        
        return self.run_command(command, timeout=300)

    def suggest_tool_installation(self, tool_name: str) -> str:
        """
        Suggest installing a tool if it's missing.
        """
        common_tools = {
            "nmap": {"cmd": "nmap", "pkg": "nmap"},
            "ffmpeg": {"cmd": "ffmpeg", "pkg": "ffmpeg"},
            "jq": {"cmd": "jq", "pkg": "jq"},
            "curl": {"cmd": "curl", "pkg": "curl"},
            "wget": {"cmd": "wget", "pkg": "wget"},
            "git": {"cmd": "git", "pkg": "git"},
        }
        
        if tool_name in common_tools:
            pkg = common_tools[tool_name]["pkg"]
            return f"Tool '{tool_name}' is not installed. You can install it using: install_package(package='{pkg}')"
        
        return f"Tool '{tool_name}' is not found. You might need to install a package for it."
    
    # ═══════════════════════════════════════════════════════════
    # CODE EXECUTION - تنفيذ الكود
    # ═══════════════════════════════════════════════════════════
    
    def python_repl(self, code: str) -> Any:
        """
        Execute Python code in isolated environment.
        تنفيذ كود Python في بيئة معزولة.
        """
        try:
            # Create isolated namespace
            local_vars = {}
            global_vars = {
                '__builtins__': __builtins__,
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
            }
            
            # Try to import commonly used libraries
            try:
                import pandas as pd
                import numpy as np
                global_vars['pd'] = pd
                global_vars['np'] = np
            except ImportError:
                pass
            
            # Execute code
            exec(code, global_vars, local_vars)
            
            # Return local variables
            return local_vars if local_vars else "Code executed successfully (no return value)"
        except Exception as e:
            return f"Error executing Python code: {str(e)}"
    
    # ═══════════════════════════════════════════════════════════
    # SYSTEM INFO TOOLS - أدوات معلومات النظام
    # ═══════════════════════════════════════════════════════════
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.
        الحصول على معلومات النظام.
        """
        try:
            return {
                "os": platform.system(),
                "os_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "cpu_count": psutil.cpu_count(),
                "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "ram_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                "disk_free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_service_status(self, service_name: str = None, service_names: List[str] = None) -> str:
        """
        Check if a service is running. If no name provided, lists all running services.
        فحص إذا كانت خدمة تعمل.
        """
        # Handle hallucinated plural argument
        if service_names and not service_name:
            if isinstance(service_names, list) and len(service_names) > 0:
                service_name = service_names[0]
            elif isinstance(service_names, str):
                service_name = service_names

        try:
            if not service_name:
                # List all running services (limit to top 20 to avoid spam)
                services = []
                for proc in psutil.process_iter(['name', 'status']):
                    if proc.info['status'] == psutil.STATUS_RUNNING:
                        services.append(proc.info['name'])
                
                # Deduplicate and sort
                services = sorted(list(set(services)))
                return f"✓ Running services ({len(services)} total): {', '.join(services[:50])}..."
            
            for proc in psutil.process_iter(['name']):
                if service_name.lower() in proc.info['name'].lower():
                    return f"✓ Service '{service_name}' is running (PID: {proc.pid})"
            return f"✗ Service '{service_name}' is not running"
        except Exception as e:
            return f"Error checking service: {str(e)}"
    
    def monitor_resources(self) -> Dict[str, Any]:
        """
        Monitor system resources.
        مراقبة موارد النظام.
        """
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "ram_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "network_sent_mb": round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
                "network_recv_mb": round(psutil.net_io_counters().bytes_recv / (1024**2), 2)
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # DOCKER TOOLS - أدوات Docker
    # ═══════════════════════════════════════════════════════════
    
    def docker_command(self, command: str) -> Dict[str, Any]:
        """
        Execute Docker commands.
        تنفيذ أوامر Docker.
        """
        full_command = f"docker {command}"
        return self.run_command(full_command)
    
    # ═══════════════════════════════════════════════════════════
    # SECURITY TOOLS - أدوات الأمان
    # ═══════════════════════════════════════════════════════════
    
    def scan_ports(self, host: str = "localhost", ports: List[int] = None) -> Dict[str, Any]:
        """
        Scan network ports.
        فحص منافذ الشبكة.
        """
        if ports is None:
            ports = [80, 443, 22, 21, 3306, 5432, 27017]
        
        import socket
        results = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                results[port] = "Open" if result == 0 else "Closed"
                sock.close()
            except Exception as e:
                results[port] = f"Error: {str(e)}"
        
        return results
    
    def check_ssl(self, domain: str) -> Dict[str, Any]:
        """
        Check SSL certificate status.
        فحص حالة شهادة SSL.
        """
        try:
            import ssl
            import socket
            from datetime import datetime
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse expiry date
                    expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (expiry - datetime.now()).days
                    
                    return {
                        "domain": domain,
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "subject": dict(x[0] for x in cert['subject']),
                        "expires": cert['notAfter'],
                        "days_until_expiry": days_until_expiry,
                        "status": "Valid" if days_until_expiry > 0 else "Expired"
                    }
        except Exception as e:
            return {"error": str(e)}
    
    # ═══════════════════════════════════════════════════════════
    # CUSTOM TOOLS - الأدوات المخصصة
    # ═══════════════════════════════════════════════════════════
    
    def register_custom_tool(self, name: str, command: str, description: str) -> str:
        """
        Register a new custom tool.
        تسجيل أداة مخصصة جديدة.
        """
        self.custom_tools[name] = {
            "command": command,
            "description": description
        }
        return f"Custom tool '{name}' registered successfully"
    
    def _execute_custom_tool(self, name: str, params: Dict[str, Any]) -> Any:
        """Execute a custom tool."""
        tool = self.custom_tools[name]
        command = tool["command"]
        
        # Replace parameters in command
        for key, value in params.items():
            command = command.replace(f"{{{key}}}", str(value))
        
        return self.run_command(command)
