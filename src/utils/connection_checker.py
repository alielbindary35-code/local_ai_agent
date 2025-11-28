"""
Connection Checker Utility
Checks internet connectivity for hybrid online/offline mode
"""

import requests
from rich.console import Console

console = Console()


class ConnectionChecker:
    """
    Simple utility to check internet connectivity
    """
    
    @staticmethod
    def check_internet(timeout: int = 3) -> bool:
        """
        Check if internet is available
        
        Args:
            timeout: Timeout in seconds for the check
            
        Returns:
            True if internet is available, False otherwise
        """
        try:
            response = requests.get("https://www.google.com", timeout=timeout)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout, Exception):
            return False
    
    @staticmethod
    def get_status_message(online: bool) -> str:
        """
        Get formatted status message
        
        Args:
            online: Whether internet is available
            
        Returns:
            Formatted status message
        """
        if online:
            return "[green]🌐 Online Mode - Internet available[/green]"
        else:
            return "[yellow]📴 Offline Mode - Using cached knowledge[/yellow]"
    
    @staticmethod
    def check_and_display(timeout: int = 3) -> bool:
        """
        Check internet and display status
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if online, False if offline
        """
        online = ConnectionChecker.check_internet(timeout)
        console.print(ConnectionChecker.get_status_message(online))
        return online
