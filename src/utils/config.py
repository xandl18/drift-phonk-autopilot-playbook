"""
Configuration management utilities for the Drift Phonk Autopilot Playbook.
"""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config_path: str = "config/default.yaml"):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'autopilot.provider')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def get_autopilot_config(self) -> Dict[str, Any]:
        """Get autopilot configuration section."""
        return self.get('autopilot', {})
    
    def get_audio_config(self) -> Dict[str, Any]:
        """Get audio configuration section."""
        return self.get('audio', {})
    
    def get_sync_config(self) -> Dict[str, Any]:
        """Get synchronization configuration section."""
        return self.get('sync', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration section."""
        return self.get('logging', {})
    
    def get_safety_config(self) -> Dict[str, Any]:
        """Get safety configuration section."""
        return self.get('safety', {})