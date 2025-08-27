"""
Logging utilities for the Drift Phonk Autopilot Playbook.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any


def setup_logging(config: Dict[str, Any], debug: bool = False) -> None:
    """Setup logging configuration.
    
    Args:
        config: Logging configuration dictionary
        debug: Enable debug mode
    """
    # Create logs directory if it doesn't exist
    log_file = config.get('file', 'logs/drift_phonk.log')
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Set logging level
    level = logging.DEBUG if debug else getattr(logging, config.get('level', 'INFO'))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    max_bytes = _parse_size(config.get('max_file_size', '10MB'))
    backup_count = config.get('backup_count', 5)
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def _parse_size(size_str: str) -> int:
    """Parse size string like '10MB' to bytes.
    
    Args:
        size_str: Size string (e.g., '10MB', '1GB')
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper()
    
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        # Assume bytes
        return int(size_str)