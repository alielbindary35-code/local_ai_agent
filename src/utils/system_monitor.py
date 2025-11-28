"""
System Monitor - Enhanced system integration and monitoring
===========================================================

Monitors server health, system resources, and provides
robust file/command management for offline operation.
"""

import psutil
import subprocess
import platform
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class SystemMonitor:
    """
    Enhanced system monitoring and integration.
    """
    
    def __init__(self):
        """Initialize system monitor."""
        self.system = platform.system()
        self.health_thresholds = {
            "cpu_warning": 80.0,
            "cpu_critical": 95.0,
            "memory_warning": 85.0,
            "memory_critical": 95.0,
            "disk_warning": 85.0,
            "disk_critical": 95.0
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """
        Get comprehensive system health status.
        
        Returns:
            Dictionary with health metrics and status
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                    "status": self._get_cpu_status(cpu_percent)
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_percent": memory.percent,
                    "status": self._get_memory_status(memory.percent)
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": disk.percent,
                    "status": self._get_disk_status(disk.percent)
                },
                "overall_status": "healthy"
            }
            
            # Determine overall status
            statuses = [
                health["cpu"]["status"],
                health["memory"]["status"],
                health["disk"]["status"]
            ]
            
            if "critical" in statuses:
                health["overall_status"] = "critical"
            elif "warning" in statuses:
                health["overall_status"] = "warning"
            
            return health
        except Exception as e:
            logger.error(f"Error getting system health: {e}")
            return {"error": str(e), "status": "unknown"}
    
    def _get_cpu_status(self, percent: float) -> str:
        """Get CPU status based on usage."""
        if percent >= self.health_thresholds["cpu_critical"]:
            return "critical"
        elif percent >= self.health_thresholds["cpu_warning"]:
            return "warning"
        return "healthy"
    
    def _get_memory_status(self, percent: float) -> str:
        """Get memory status based on usage."""
        if percent >= self.health_thresholds["memory_critical"]:
            return "critical"
        elif percent >= self.health_thresholds["memory_warning"]:
            return "warning"
        return "healthy"
    
    def _get_disk_status(self, percent: float) -> str:
        """Get disk status based on usage."""
        if percent >= self.health_thresholds["disk_critical"]:
            return "critical"
        elif percent >= self.health_thresholds["disk_warning"]:
            return "warning"
        return "healthy"
    
    def monitor_processes(self, process_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Monitor specific processes or all processes.
        
        Args:
            process_names: List of process names to monitor (None for all)
        
        Returns:
            List of process information
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info
                    if process_names is None or proc_info['name'].lower() in [p.lower() for p in process_names]:
                        processes.append({
                            "pid": proc_info['pid'],
                            "name": proc_info['name'],
                            "cpu_percent": proc_info['cpu_percent'],
                            "memory_percent": proc_info['memory_percent'],
                            "status": proc_info['status']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes
        except Exception as e:
            logger.error(f"Error monitoring processes: {e}")
            return []
    
    def check_service_status(self, service_name: str) -> Dict[str, Any]:
        """
        Check if a service is running.
        
        Args:
            service_name: Service name to check
        
        Returns:
            Service status information
        """
        try:
            processes = self.monitor_processes([service_name])
            if processes:
                return {
                    "running": True,
                    "processes": processes,
                    "status": "active"
                }
            else:
                return {
                    "running": False,
                    "status": "stopped"
                }
        except Exception as e:
            logger.error(f"Error checking service {service_name}: {e}")
            return {"error": str(e), "status": "unknown"}
    
    def get_file_system_info(self, path: str = "/") -> Dict[str, Any]:
        """
        Get file system information for a path.
        
        Args:
            path: Path to check
        
        Returns:
            File system information
        """
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return {"error": f"Path does not exist: {path}"}
            
            stat = path_obj.stat()
            return {
                "path": str(path_obj.absolute()),
                "exists": True,
                "is_file": path_obj.is_file(),
                "is_dir": path_obj.is_dir(),
                "size_bytes": stat.st_size if path_obj.is_file() else None,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "permissions": {
                    "readable": path_obj.exists() and path_obj.is_readable(),
                    "writable": path_obj.exists() and path_obj.is_writable(),
                    "executable": path_obj.exists() and path_obj.is_executable() if path_obj.is_file() else False
                }
            }
        except Exception as e:
            logger.error(f"Error getting file system info: {e}")
            return {"error": str(e)}
    
    def safe_command_execution(
        self,
        command: str,
        timeout: int = 30,
        check_health: bool = True
    ) -> Dict[str, Any]:
        """
        Safely execute system command with health checks.
        
        Args:
            command: Command to execute
            timeout: Execution timeout
            check_health: Check system health before execution
        
        Returns:
            Command execution result
        """
        try:
            # Check system health before execution
            if check_health:
                health = self.get_system_health()
                if health.get("overall_status") == "critical":
                    return {
                        "error": "System health is critical. Command execution blocked.",
                        "health": health
                    }
            
            # Execute command
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
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }
        except subprocess.TimeoutExpired:
            return {
                "error": f"Command timed out after {timeout} seconds",
                "command": command
            }
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {
                "error": str(e),
                "command": command
            }
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network interface information."""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
                "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {"error": str(e)}

