"""
Security Module
===============

Security features for the AI agent:
- Permission system
- Data encryption for sensitive data
- Audit logging
- Risk assessment
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from enum import Enum

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("cryptography not available. Encryption features disabled.")

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for actions."""
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"


class PermissionSystem:
    """
    Permission system for action approval with enhanced security.
    """
    
    def __init__(self, audit_log_path: Optional[Path] = None, require_approval: bool = True):
        """
        Initialize permission system.
        
        Args:
            audit_log_path: Path to audit log file
            require_approval: Require explicit approval for actions
        """
        if audit_log_path is None:
            audit_log_path = Path("data") / "audit_log.jsonl"
        self.audit_log_path = audit_log_path
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Permission cache (action -> approved)
        self.permission_cache: Dict[str, bool] = {}
        self.require_approval = require_approval
        
        # Command whitelist/blacklist
        self.command_whitelist: List[str] = []
        self.command_blacklist: List[str] = [
            "rm -rf /", "format", "del /f /s /q", "shutdown", "reboot"
        ]
        
        # File path restrictions
        self.restricted_paths: List[str] = [
            "/etc", "/sys", "/proc", "C:\\Windows\\System32"
        ]
    
    def assess_risk(self, action: str, action_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risk level of an action.
        
        Args:
            action: Action name
            action_input: Action parameters
        
        Returns:
            Risk assessment dictionary
        """
        risk_rules = {
            # File operations
            'delete_file': RiskLevel.DANGEROUS,
            'write_file': RiskLevel.CAUTION,
            'read_file': RiskLevel.SAFE,
            
            # Command execution
            'run_command': self._assess_command_risk(action_input),
            
            # System operations
            'install_package': RiskLevel.CAUTION,
            'docker_command': self._assess_docker_risk(action_input),
            
            # Network operations
            'fetch_api': RiskLevel.CAUTION,
            'download_file': RiskLevel.CAUTION,
            
            # Database operations
            'postgres_query': self._assess_query_risk(action_input),
        }
        
        risk_level = risk_rules.get(action, RiskLevel.SAFE)
        
        if isinstance(risk_level, RiskLevel):
            level = risk_level
        else:
            level = risk_level  # Already a RiskLevel from helper function
        
        return {
            'level': level.value,
            'emoji': self._get_risk_emoji(level),
            'explanation': self._get_risk_explanation(level, action, action_input)
        }
    
    def _assess_command_risk(self, action_input: Dict) -> RiskLevel:
        """Assess risk of command execution."""
        command = action_input.get('command', '').lower()
        
        dangerous_keywords = ['rm ', 'del ', 'format', 'drop', 'delete', 'remove', 'uninstall']
        caution_keywords = ['install', 'update', 'restart', 'stop', 'start', 'modify']
        
        if any(keyword in command for keyword in dangerous_keywords):
            return RiskLevel.DANGEROUS
        elif any(keyword in command for keyword in caution_keywords):
            return RiskLevel.CAUTION
        else:
            return RiskLevel.SAFE
    
    def _assess_docker_risk(self, action_input: Dict) -> RiskLevel:
        """Assess risk of Docker commands."""
        command = action_input.get('command', '').lower()
        
        if any(keyword in command for keyword in ['rm', 'prune', 'kill', 'stop']):
            return RiskLevel.DANGEROUS
        elif any(keyword in command for keyword in ['run', 'start', 'build']):
            return RiskLevel.CAUTION
        else:
            return RiskLevel.SAFE
    
    def _assess_query_risk(self, action_input: Dict) -> RiskLevel:
        """Assess risk of database queries."""
        query = action_input.get('query', '').lower()
        
        if any(keyword in query for keyword in ['drop', 'delete', 'truncate', 'alter']):
            return RiskLevel.DANGEROUS
        elif any(keyword in query for keyword in ['update', 'insert', 'create']):
            return RiskLevel.CAUTION
        else:
            return RiskLevel.SAFE
    
    def _get_risk_emoji(self, level: RiskLevel) -> str:
        """Get emoji for risk level."""
        emoji_map = {
            RiskLevel.SAFE: '🟢',
            RiskLevel.CAUTION: '🟡',
            RiskLevel.DANGEROUS: '🔴',
            RiskLevel.CRITICAL: '⚫'
        }
        return emoji_map.get(level, '⚪')
    
    def _get_risk_explanation(self, level: RiskLevel, action: str, action_input: Dict) -> str:
        """Get explanation for risk level."""
        explanations = {
            RiskLevel.SAFE: "This is a safe, read-only operation.",
            RiskLevel.CAUTION: "This will modify system state or data. Review carefully.",
            RiskLevel.DANGEROUS: "This action may cause data loss or system changes. Cannot be undone.",
            RiskLevel.CRITICAL: "CRITICAL: This action may cause severe system damage. Proceed with extreme caution."
        }
        return explanations.get(level, "Unknown risk level.")
    
    def validate_action(self, action: str, action_input: Dict) -> Dict[str, Any]:
        """
        Validate action before execution.
        
        Args:
            action: Action name
            action_input: Action parameters
        
        Returns:
            Validation result with allowed flag and reason
        """
        validation = {
            "allowed": True,
            "reason": "Action validated",
            "warnings": []
        }
        
        # Check command blacklist
        if action == "run_command":
            command = action_input.get("command", "").lower()
            for blocked in self.command_blacklist:
                if blocked.lower() in command:
                    validation["allowed"] = False
                    validation["reason"] = f"Command contains blacklisted pattern: {blocked}"
                    return validation
        
        # Check file path restrictions
        if action in ["read_file", "write_file", "delete_file"]:
            filepath = action_input.get("filepath", "")
            for restricted in self.restricted_paths:
                if restricted.lower() in filepath.lower():
                    validation["warnings"].append(f"Accessing restricted path: {restricted}")
                    validation["allowed"] = False
                    validation["reason"] = "File path is in restricted area"
                    return validation
        
        # Check whitelist if enabled
        if self.command_whitelist and action == "run_command":
            command = action_input.get("command", "").lower()
            if not any(allowed.lower() in command for allowed in self.command_whitelist):
                validation["warnings"].append("Command not in whitelist")
        
        return validation
    
    def log_action(
        self,
        action: str,
        action_input: Dict,
        risk: Dict,
        approved: bool,
        user: Optional[str] = None,
        validation: Optional[Dict] = None
    ):
        """
        Log action to audit log with enhanced details.
        
        Args:
            action: Action name
            action_input: Action parameters
            risk: Risk assessment
            approved: Whether action was approved
            user: User identifier (optional)
            validation: Validation result (optional)
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'action_input': self._sanitize_for_logging(action_input),
            'risk_level': risk['level'],
            'approved': approved,
            'user': user or 'system',
            'validation': validation or {}
        }
        
        try:
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Error writing to audit log: {e}")
    
    def _sanitize_for_logging(self, data: Dict) -> Dict:
        """Remove sensitive information from logging."""
        sanitized = data.copy()
        sensitive_keys = ['password', 'api_key', 'token', 'secret', 'key']
        
        for key in sanitized:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = '***REDACTED***'
        
        return sanitized


class DataEncryption:
    """
    Data encryption for sensitive information.
    """
    
    def __init__(self, key: Optional[bytes] = None, key_file: Optional[Path] = None):
        """
        Initialize encryption system.
        
        Args:
            key: Encryption key (bytes)
            key_file: Path to key file
        """
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required for encryption")
        
        if key:
            self.key = key
        elif key_file and key_file.exists():
            with open(key_file, 'rb') as f:
                self.key = f.read()
        else:
            # Generate new key
            self.key = Fernet.generate_key()
            if key_file:
                key_file.parent.mkdir(parents=True, exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(self.key)
        
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Data to encrypt
        
        Returns:
            Encrypted data (base64 encoded)
        """
        try:
            encrypted = self.cipher.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data (base64 encoded)
        
        Returns:
            Decrypted data
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def encrypt_dict(self, data: Dict[str, Any], sensitive_keys: List[str]) -> Dict[str, Any]:
        """
        Encrypt sensitive values in a dictionary.
        
        Args:
            data: Dictionary to encrypt
            sensitive_keys: Keys containing sensitive data
        
        Returns:
            Dictionary with encrypted values
        """
        encrypted = data.copy()
        for key in sensitive_keys:
            if key in encrypted and isinstance(encrypted[key], str):
                encrypted[key] = self.encrypt(encrypted[key])
        return encrypted
    
    def decrypt_dict(self, data: Dict[str, Any], sensitive_keys: List[str]) -> Dict[str, Any]:
        """
        Decrypt sensitive values in a dictionary.
        
        Args:
            data: Dictionary to decrypt
            sensitive_keys: Keys containing sensitive data
        
        Returns:
            Dictionary with decrypted values
        """
        decrypted = data.copy()
        for key in sensitive_keys:
            if key in decrypted and isinstance(decrypted[key], str):
                try:
                    decrypted[key] = self.decrypt(decrypted[key])
                except:
                    pass  # If decryption fails, keep original
        return decrypted


def hash_sensitive_data(data: str) -> str:
    """
    Hash sensitive data (one-way, for storage).
    
    Args:
        data: Data to hash
    
    Returns:
        SHA256 hash of data
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

