"""
Troubleshooting Tools
Systematic error analysis, log parsing, system diagnostics, and debugging workflows
"""

import re
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import psutil
import socket

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class TroubleshootingTools:
    """
    Tools for systematic troubleshooting and debugging
    """
    
    def __init__(self):
        self.system = platform.system()
        self.error_patterns = self._load_error_patterns()
    
    def _load_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load common error patterns and their solutions"""
        return {
            "python": {
                "SyntaxError": {
                    "pattern": r"SyntaxError: (.+)",
                    "common_causes": [
                        "Missing parentheses, brackets, or quotes",
                        "Incorrect indentation",
                        "Invalid syntax in function/class definition"
                    ],
                    "suggestions": [
                        "Check for balanced parentheses, brackets, and quotes",
                        "Verify indentation (use 4 spaces or tabs consistently)",
                        "Review the line mentioned in the error message"
                    ]
                },
                "ModuleNotFoundError": {
                    "pattern": r"ModuleNotFoundError: No module named '(.+)'",
                    "common_causes": [
                        "Module not installed",
                        "Virtual environment not activated",
                        "Python path issues"
                    ],
                    "suggestions": [
                        "Install the module: pip install <module_name>",
                        "Activate your virtual environment",
                        "Check PYTHONPATH environment variable"
                    ]
                },
                "ImportError": {
                    "pattern": r"ImportError: (.+)",
                    "common_causes": [
                        "Circular imports",
                        "Module path issues",
                        "Missing dependencies"
                    ],
                    "suggestions": [
                        "Check for circular import dependencies",
                        "Verify module paths and __init__.py files",
                        "Install missing dependencies"
                    ]
                },
                "AttributeError": {
                    "pattern": r"AttributeError: (.+)",
                    "common_causes": [
                        "Object doesn't have the attribute",
                        "Typo in attribute name",
                        "Object is None or wrong type"
                    ],
                    "suggestions": [
                        "Check if the object has the attribute using dir() or hasattr()",
                        "Verify spelling of attribute name",
                        "Check if object is None before accessing attributes"
                    ]
                },
                "TypeError": {
                    "pattern": r"TypeError: (.+)",
                    "common_causes": [
                        "Wrong argument type",
                        "Missing required arguments",
                        "Incorrect function call"
                    ],
                    "suggestions": [
                        "Check argument types match function signature",
                        "Verify all required arguments are provided",
                        "Review function documentation"
                    ]
                },
                "FileNotFoundError": {
                    "pattern": r"FileNotFoundError: (.+)",
                    "common_causes": [
                        "File path is incorrect",
                        "File doesn't exist",
                        "Working directory is wrong"
                    ],
                    "suggestions": [
                        "Verify the file path is correct (use absolute path if needed)",
                        "Check if file exists using os.path.exists()",
                        "Verify current working directory"
                    ]
                }
            },
            "docker": {
                "Cannot connect": {
                    "pattern": r"Cannot connect to the Docker daemon",
                    "common_causes": [
                        "Docker daemon not running",
                        "Permission issues",
                        "Docker service not started"
                    ],
                    "suggestions": [
                        "Start Docker daemon: sudo systemctl start docker (Linux) or start Docker Desktop (Windows/Mac)",
                        "Check permissions: sudo usermod -aG docker $USER (Linux)",
                        "Verify Docker is installed and running"
                    ]
                },
                "Port already in use": {
                    "pattern": r"port is already allocated|address already in use",
                    "common_causes": [
                        "Another container using the port",
                        "Application already running on port",
                        "Port conflict"
                    ],
                    "suggestions": [
                        "Find process using port: lsof -i :PORT or netstat -ano | findstr :PORT",
                        "Stop the conflicting container/process",
                        "Use a different port"
                    ]
                },
                "Image not found": {
                    "pattern": r"pull access denied|repository does not exist|image not found",
                    "common_causes": [
                        "Image name is incorrect",
                        "Image doesn't exist in registry",
                        "Authentication required"
                    ],
                    "suggestions": [
                        "Verify image name and tag are correct",
                        "Check if image exists: docker images",
                        "Login to registry if private: docker login"
                    ]
                }
            },
            "database": {
                "Connection refused": {
                    "pattern": r"connection refused|could not connect",
                    "common_causes": [
                        "Database server not running",
                        "Wrong host/port",
                        "Firewall blocking connection"
                    ],
                    "suggestions": [
                        "Check if database service is running",
                        "Verify connection string (host, port, credentials)",
                        "Check firewall rules"
                    ]
                },
                "Authentication failed": {
                    "pattern": r"authentication failed|password authentication failed",
                    "common_causes": [
                        "Wrong username/password",
                        "User doesn't exist",
                        "Password expired"
                    ],
                    "suggestions": [
                        "Verify credentials are correct",
                        "Reset password if needed",
                        "Check user permissions"
                    ]
                },
                "Table doesn't exist": {
                    "pattern": r"relation.*does not exist|table.*doesn't exist",
                    "common_causes": [
                        "Table name is misspelled",
                        "Table not created",
                        "Wrong database/schema"
                    ],
                    "suggestions": [
                        "Verify table name spelling",
                        "Check if table exists: SELECT * FROM information_schema.tables",
                        "Verify you're connected to the correct database"
                    ]
                }
            },
            "network": {
                "Connection timeout": {
                    "pattern": r"connection timeout|timed out",
                    "common_causes": [
                        "Server is down",
                        "Network issues",
                        "Firewall blocking"
                    ],
                    "suggestions": [
                        "Check if server is running and accessible",
                        "Test network connectivity: ping or curl",
                        "Check firewall and proxy settings"
                    ]
                },
                "DNS resolution failed": {
                    "pattern": r"could not resolve host|name resolution failed",
                    "common_causes": [
                        "DNS server issues",
                        "Hostname is incorrect",
                        "Network configuration problems"
                    ],
                    "suggestions": [
                        "Verify hostname is correct",
                        "Check DNS settings: nslookup or dig",
                        "Try using IP address instead of hostname"
                    ]
                }
            }
        }
    
    def get_tool_descriptions(self) -> str:
        """Get descriptions of all troubleshooting tools"""
        tools = {
            "analyze_error": "Analyze error message and suggest fixes (args: error_message, context)",
            "analyze_logs": "Analyze log files to find issues (args: log_file, pattern)",
            "diagnose_system": "Run system diagnostics for a component (args: component)",
            "create_debug_plan": "Create step-by-step debugging plan (args: issue_description)",
            "check_dependencies": "Check if required dependencies are installed (args: dependencies)",
            "test_connectivity": "Test network connectivity to a host (args: host, port)",
            "find_process": "Find process by name or port (args: name, port)",
            "check_service_health": "Check health of a service (args: service_name)"
        }
        return json.dumps(tools, indent=2)
    
    def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Execute a troubleshooting tool"""
        method_name = tool_name
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(**params)
        else:
            return f"Error: Troubleshooting tool '{tool_name}' not found"
    
    def analyze_error(self, error_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Analyze error message and provide suggestions.
        
        Args:
            error_message: The error message to analyze
            context: Additional context (language, framework, etc.)
        
        Returns:
            Formatted analysis with suggestions
        """
        if not error_message:
            return "⚠️ No error message provided"
        
        context = context or {}
        language = context.get("language", "python").lower()
        framework = context.get("framework", "")
        
        # Try to match error patterns
        matched_pattern = None
        error_type = None
        
        # Check language-specific patterns
        if language in self.error_patterns:
            for error_name, error_info in self.error_patterns[language].items():
                pattern = error_info["pattern"]
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    matched_pattern = error_info
                    error_type = error_name
                    break
        
        # Check Docker patterns
        if "docker" in error_message.lower() or context.get("component") == "docker":
            for error_name, error_info in self.error_patterns.get("docker", {}).items():
                pattern = error_info["pattern"]
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    matched_pattern = error_info
                    error_type = error_name
                    break
        
        # Check database patterns
        if any(db in error_message.lower() for db in ["postgres", "mysql", "database", "sql"]):
            for error_name, error_info in self.error_patterns.get("database", {}).items():
                pattern = error_info["pattern"]
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    matched_pattern = error_info
                    error_type = error_name
                    break
        
        # Check network patterns
        if any(net in error_message.lower() for net in ["connection", "timeout", "network", "dns"]):
            for error_name, error_info in self.error_patterns.get("network", {}).items():
                pattern = error_info["pattern"]
                match = re.search(pattern, error_message, re.IGNORECASE)
                if match:
                    matched_pattern = error_info
                    error_type = error_name
                    break
        
        # Build analysis result
        result = []
        result.append("🔍 **Error Analysis**\n")
        result.append(f"**Error Message:**\n```\n{error_message}\n```\n\n")
        
        if matched_pattern:
            result.append(f"**Error Type:** {error_type}\n\n")
            result.append("**Common Causes:**\n")
            for cause in matched_pattern["common_causes"]:
                result.append(f"- {cause}\n")
            result.append("\n**Suggested Solutions:**\n")
            for i, suggestion in enumerate(matched_pattern["suggestions"], 1):
                result.append(f"{i}. {suggestion}\n")
        else:
            result.append("⚠️ **No specific pattern matched**\n\n")
            result.append("**General Troubleshooting Steps:**\n")
            result.append("1. Read the error message carefully - it usually indicates the problem\n")
            result.append("2. Check the line number mentioned in the error\n")
            result.append("3. Verify all dependencies are installed\n")
            result.append("4. Check if recent changes might have caused the issue\n")
            result.append("5. Search online for the exact error message\n")
            result.append("6. Check logs for additional context\n")
        
        # Add context-specific suggestions
        if framework:
            result.append(f"\n**Framework-Specific:** Since you're using {framework}, also check:\n")
            result.append(f"- {framework} documentation\n")
            result.append(f"- {framework} common issues and solutions\n")
        
        return "".join(result)
    
    def analyze_logs(self, log_file: str, pattern: Optional[str] = None) -> str:
        """
        Analyze log files to find issues.
        
        Args:
            log_file: Path to log file
            pattern: Optional pattern to search for (e.g., "ERROR", "WARN")
        
        Returns:
            Analysis of log file
        """
        try:
            log_path = Path(log_file)
            if not log_path.exists():
                return f"❌ Log file not found: {log_file}"
            
            # Read log file
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            except Exception as e:
                return f"❌ Error reading log file: {str(e)}"
            
            if not lines:
                return f"⚠️ Log file is empty: {log_file}"
            
            # Analyze logs
            result = []
            result.append(f"📋 **Log Analysis: {log_file}**\n\n")
            result.append(f"**Total Lines:** {len(lines)}\n\n")
            
            # Count error levels
            error_count = sum(1 for line in lines if re.search(r'\b(ERROR|error|Error|FATAL|fatal|Fatal)\b', line))
            warn_count = sum(1 for line in lines if re.search(r'\b(WARN|warn|Warn|WARNING|warning|Warning)\b', line))
            info_count = sum(1 for line in lines if re.search(r'\b(INFO|info|Info)\b', line))
            
            result.append("**Error Level Summary:**\n")
            result.append(f"- ❌ Errors: {error_count}\n")
            result.append(f"- ⚠️ Warnings: {warn_count}\n")
            result.append(f"- ℹ️ Info: {info_count}\n\n")
            
            # Find errors
            if error_count > 0:
                result.append("**Error Lines:**\n")
                error_lines = [line.strip() for line in lines if re.search(r'\b(ERROR|error|Error|FATAL|fatal|Fatal)\b', line)]
                for i, error_line in enumerate(error_lines[:10], 1):  # Show first 10 errors
                    result.append(f"{i}. {error_line[:200]}\n")
                if len(error_lines) > 10:
                    result.append(f"\n... and {len(error_lines) - 10} more errors\n")
                result.append("\n")
            
            # Pattern search
            if pattern:
                result.append(f"**Pattern Search: '{pattern}'**\n")
                matches = [line.strip() for line in lines if re.search(pattern, line, re.IGNORECASE)]
                if matches:
                    result.append(f"Found {len(matches)} matching lines:\n")
                    for i, match in enumerate(matches[:10], 1):
                        result.append(f"{i}. {match[:200]}\n")
                    if len(matches) > 10:
                        result.append(f"\n... and {len(matches) - 10} more matches\n")
                else:
                    result.append("No matches found.\n")
                result.append("\n")
            
            # Recent errors (last 50 lines)
            result.append("**Recent Activity (Last 50 lines):**\n")
            recent_lines = lines[-50:]
            for line in recent_lines[-10:]:  # Show last 10 lines
                result.append(f"{line.strip()}\n")
            
            return "".join(result)
        
        except Exception as e:
            return f"❌ Error analyzing logs: {str(e)}"
    
    def diagnose_system(self, component: str) -> str:
        """
        Run system diagnostics for a component.
        
        Args:
            component: Component to diagnose (e.g., "docker", "postgres", "python", "network")
        
        Returns:
            Diagnostic report
        """
        component_lower = component.lower()
        result = []
        result.append(f"🔧 **System Diagnostics: {component}**\n\n")
        
        try:
            if component_lower in ["docker", "container"]:
                # Check Docker
                try:
                    docker_version = subprocess.run(
                        ["docker", "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if docker_version.returncode == 0:
                        result.append(f"✅ Docker installed: {docker_version.stdout.strip()}\n")
                    else:
                        result.append("❌ Docker not found or not accessible\n")
                except FileNotFoundError:
                    result.append("❌ Docker not installed\n")
                except Exception as e:
                    result.append(f"⚠️ Error checking Docker: {str(e)}\n")
                
                # Check Docker daemon
                try:
                    docker_info = subprocess.run(
                        ["docker", "info"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if docker_info.returncode == 0:
                        result.append("✅ Docker daemon is running\n")
                    else:
                        result.append("❌ Docker daemon is not running\n")
                        result.append("   Try: sudo systemctl start docker (Linux) or start Docker Desktop\n")
                except Exception as e:
                    result.append(f"⚠️ Error checking Docker daemon: {str(e)}\n")
            
            elif component_lower in ["postgres", "postgresql", "database"]:
                # Check PostgreSQL
                try:
                    psql_version = subprocess.run(
                        ["psql", "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if psql_version.returncode == 0:
                        result.append(f"✅ PostgreSQL client installed: {psql_version.stdout.strip()}\n")
                    else:
                        result.append("⚠️ PostgreSQL client not found in PATH\n")
                except FileNotFoundError:
                    result.append("⚠️ PostgreSQL client not installed\n")
                
                # Check if PostgreSQL service is running
                if self.system == "Windows":
                    try:
                        service_check = subprocess.run(
                            ["sc", "query", "postgresql"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if "RUNNING" in service_check.stdout:
                            result.append("✅ PostgreSQL service is running\n")
                        else:
                            result.append("⚠️ PostgreSQL service status unknown\n")
                    except Exception:
                        pass
                else:
                    try:
                        service_check = subprocess.run(
                            ["systemctl", "is-active", "postgresql"],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if service_check.returncode == 0:
                            result.append("✅ PostgreSQL service is running\n")
                        else:
                            result.append("⚠️ PostgreSQL service may not be running\n")
                    except Exception:
                        pass
            
            elif component_lower in ["python", "py"]:
                # Check Python
                import sys
                result.append(f"✅ Python version: {sys.version}\n")
                result.append(f"✅ Python path: {sys.executable}\n")
                
                # Check pip
                try:
                    pip_version = subprocess.run(
                        [sys.executable, "-m", "pip", "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if pip_version.returncode == 0:
                        result.append(f"✅ pip installed: {pip_version.stdout.strip()}\n")
                except Exception as e:
                    result.append(f"⚠️ Error checking pip: {str(e)}\n")
            
            elif component_lower in ["network", "net"]:
                # Check network connectivity
                result.append("**Network Diagnostics:**\n")
                
                # Check DNS
                try:
                    import socket
                    socket.gethostbyname("google.com")
                    result.append("✅ DNS resolution working\n")
                except Exception as e:
                    result.append(f"❌ DNS resolution failed: {str(e)}\n")
                
                # Check internet connectivity
                try:
                    import requests
                    response = requests.get("https://www.google.com", timeout=5)
                    if response.status_code == 200:
                        result.append("✅ Internet connectivity working\n")
                    else:
                        result.append(f"⚠️ Internet connectivity issue (Status: {response.status_code})\n")
                except Exception as e:
                    result.append(f"❌ Internet connectivity failed: {str(e)}\n")
            
            else:
                result.append(f"⚠️ Unknown component: {component}\n")
                result.append("Supported components: docker, postgres, python, network\n")
        
        except Exception as e:
            result.append(f"❌ Error during diagnostics: {str(e)}\n")
        
        return "".join(result)
    
    def create_debug_plan(self, issue_description: str) -> str:
        """
        Create a step-by-step debugging plan.
        
        Args:
            issue_description: Description of the issue
        
        Returns:
            Step-by-step debugging plan
        """
        result = []
        result.append("📋 **Debugging Plan**\n\n")
        result.append(f"**Issue:** {issue_description}\n\n")
        result.append("**Step-by-Step Debugging Process:**\n\n")
        
        # Analyze issue description to suggest relevant steps
        issue_lower = issue_description.lower()
        
        steps = []
        
        # General steps
        steps.append("1. **Reproduce the Issue**\n   - Try to reproduce the error consistently\n   - Note the exact steps that cause the issue\n")
        
        # Check for specific keywords
        if any(word in issue_lower for word in ["error", "exception", "fail"]):
            steps.append("2. **Analyze Error Message**\n   - Copy the full error message\n   - Use analyze_error() to get suggestions\n   - Check line numbers mentioned in error\n")
        
        if any(word in issue_lower for word in ["log", "logging"]):
            steps.append("3. **Check Logs**\n   - Review application logs\n   - Use analyze_logs() to find patterns\n   - Look for errors, warnings, or anomalies\n")
        
        if any(word in issue_lower for word in ["docker", "container"]):
            steps.append("4. **Docker Diagnostics**\n   - Run diagnose_system('docker')\n   - Check container logs: docker logs <container>\n   - Verify Docker daemon is running\n")
        
        if any(word in issue_lower for word in ["database", "db", "postgres", "mysql"]):
            steps.append("5. **Database Diagnostics**\n   - Run diagnose_system('postgres')\n   - Test database connection\n   - Check database logs\n")
        
        if any(word in issue_lower for word in ["network", "connection", "timeout"]):
            steps.append("6. **Network Diagnostics**\n   - Run diagnose_system('network')\n   - Test connectivity: ping or curl\n   - Check firewall rules\n")
        
        if any(word in issue_lower for word in ["import", "module", "package"]):
            steps.append("7. **Dependency Check**\n   - Verify all required packages are installed\n   - Check Python/environment paths\n   - Reinstall problematic packages\n")
        
        # Common debugging steps
        steps.append("8. **Isolate the Problem**\n   - Comment out recent changes\n   - Test with minimal code\n   - Check if issue exists in clean environment\n")
        
        steps.append("9. **Search for Solutions**\n   - Search online for the specific error\n   - Check official documentation\n   - Review similar issues on StackOverflow\n")
        
        steps.append("10. **Verify Fix**\n    - Test the solution thoroughly\n    - Check if issue is completely resolved\n    - Document the solution for future reference\n")
        
        result.extend(steps)
        
        result.append("\n**Tools Available:**\n")
        result.append("- `analyze_error()` - Analyze error messages\n")
        result.append("- `analyze_logs()` - Parse log files\n")
        result.append("- `diagnose_system()` - System diagnostics\n")
        result.append("- `check_dependencies()` - Verify dependencies\n")
        result.append("- `test_connectivity()` - Test network connections\n")
        
        return "".join(result)
    
    def check_dependencies(self, dependencies: List[str]) -> str:
        """
        Check if required dependencies are installed.
        
        Args:
            dependencies: List of dependency names to check
        
        Returns:
            Status report for each dependency
        """
        result = []
        result.append("📦 **Dependency Check**\n\n")
        
        import sys
        
        for dep in dependencies:
            try:
                # Try importing the module
                __import__(dep)
                result.append(f"✅ {dep} - Installed\n")
            except ImportError:
                result.append(f"❌ {dep} - Not installed\n")
                result.append(f"   Install: pip install {dep}\n")
            except Exception as e:
                result.append(f"⚠️ {dep} - Error checking: {str(e)}\n")
        
        return "".join(result)
    
    def test_connectivity(self, host: str, port: Optional[int] = None) -> str:
        """
        Test network connectivity to a host.
        
        Args:
            host: Hostname or IP address
            port: Optional port number
        
        Returns:
            Connectivity test results
        """
        result = []
        result.append(f"🌐 **Connectivity Test: {host}**\n\n")
        
        try:
            # Test DNS resolution
            try:
                ip = socket.gethostbyname(host)
                result.append(f"✅ DNS Resolution: {host} -> {ip}\n")
            except socket.gaierror:
                result.append(f"❌ DNS Resolution Failed: Cannot resolve {host}\n")
                return "".join(result)
            
            # Test port connectivity if port specified
            if port:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    connection_result = sock.connect_ex((host, port))
                    sock.close()
                    
                    if connection_result == 0:
                        result.append(f"✅ Port {port} is open and accessible\n")
                    else:
                        result.append(f"❌ Port {port} is closed or not accessible\n")
                except Exception as e:
                    result.append(f"⚠️ Error testing port {port}: {str(e)}\n")
            else:
                # Test HTTP connectivity
                try:
                    import requests
                    response = requests.get(f"http://{host}", timeout=5)
                    result.append(f"✅ HTTP connectivity: Status {response.status_code}\n")
                except requests.exceptions.ConnectionError:
                    result.append(f"❌ HTTP connectivity failed: Cannot connect to {host}\n")
                except Exception as e:
                    result.append(f"⚠️ HTTP connectivity error: {str(e)}\n")
        
        except Exception as e:
            result.append(f"❌ Connectivity test failed: {str(e)}\n")
        
        return "".join(result)
    
    def find_process(self, name: Optional[str] = None, port: Optional[int] = None) -> str:
        """
        Find process by name or port.
        
        Args:
            name: Process name to search for
            port: Port number to find process using it
        
        Returns:
            Process information
        """
        result = []
        
        if port:
            result.append(f"🔍 **Finding Process on Port {port}**\n\n")
            try:
                if self.system == "Windows":
                    # Windows: netstat -ano | findstr :PORT
                    cmd = ["netstat", "-ano"]
                    output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    lines = [line for line in output.stdout.split('\n') if f':{port}' in line]
                    
                    if lines:
                        result.append("**Processes using this port:**\n")
                        for line in lines[:5]:
                            result.append(f"{line}\n")
                    else:
                        result.append(f"⚠️ No process found using port {port}\n")
                else:
                    # Linux/Mac: lsof -i :PORT
                    cmd = ["lsof", "-i", f":{port}"]
                    output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if output.returncode == 0 and output.stdout:
                        result.append("**Processes using this port:**\n")
                        result.append(output.stdout)
                    else:
                        result.append(f"⚠️ No process found using port {port}\n")
            except Exception as e:
                result.append(f"❌ Error finding process: {str(e)}\n")
        
        elif name:
            result.append(f"🔍 **Finding Process: {name}**\n\n")
            try:
                found_processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        proc_info = proc.info
                        proc_name = proc_info.get('name', '').lower()
                        cmdline = ' '.join(proc_info.get('cmdline', [])).lower()
                        
                        if name.lower() in proc_name or name.lower() in cmdline:
                            found_processes.append(proc_info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                if found_processes:
                    result.append(f"**Found {len(found_processes)} process(es):**\n")
                    for proc in found_processes[:10]:
                        pid = proc.get('pid', 'N/A')
                        proc_name = proc.get('name', 'N/A')
                        result.append(f"- PID {pid}: {proc_name}\n")
                else:
                    result.append(f"⚠️ No process found matching '{name}'\n")
            except Exception as e:
                result.append(f"❌ Error finding process: {str(e)}\n")
        else:
            result.append("⚠️ Please provide either 'name' or 'port' parameter\n")
        
        return "".join(result)
    
    def check_service_health(self, service_name: str) -> str:
        """
        Check health of a service.
        
        Args:
            service_name: Name of the service to check
        
        Returns:
            Service health report
        """
        result = []
        result.append(f"🏥 **Service Health Check: {service_name}**\n\n")
        
        try:
            if self.system == "Windows":
                # Windows: sc query SERVICE_NAME
                cmd = ["sc", "query", service_name]
                output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                if "RUNNING" in output.stdout:
                    result.append(f"✅ Service '{service_name}' is RUNNING\n")
                elif "STOPPED" in output.stdout:
                    result.append(f"❌ Service '{service_name}' is STOPPED\n")
                    result.append(f"   Start: sc start {service_name}\n")
                else:
                    result.append(f"⚠️ Service '{service_name}' status unknown\n")
                    result.append(f"   Output: {output.stdout[:200]}\n")
            else:
                # Linux: systemctl status SERVICE_NAME
                cmd = ["systemctl", "is-active", service_name]
                output = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                if output.returncode == 0:
                    status = output.stdout.strip()
                    if status == "active":
                        result.append(f"✅ Service '{service_name}' is ACTIVE\n")
                    else:
                        result.append(f"⚠️ Service '{service_name}' status: {status}\n")
                else:
                    result.append(f"❌ Service '{service_name}' is not active\n")
                    result.append(f"   Start: sudo systemctl start {service_name}\n")
        
        except FileNotFoundError:
            result.append(f"⚠️ Cannot check service (systemctl/sc not found)\n")
        except Exception as e:
            result.append(f"❌ Error checking service: {str(e)}\n")
        
        return "".join(result)


# Test
if __name__ == "__main__":
    tools = TroubleshootingTools()
    print(tools.get_tool_descriptions())
    
    # Test error analysis
    print("\n" + "="*60)
    print("Testing error analysis:")
    print(tools.analyze_error("ModuleNotFoundError: No module named 'requests'", {"language": "python"}))

