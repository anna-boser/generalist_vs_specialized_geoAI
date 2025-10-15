"""
Utility functions for logging and other helpers.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


def setup_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: str = '%(asctime)s - %(levelname)s - %(message)s'
) -> logging.Logger:
    """
    Setup logging configuration.
    
    Automatically creates log file in the same directory as the calling script
    with the same name (but .log extension), unless overridden.
    
    Args:
        log_file: Custom log file path (optional). If None, auto-generates from calling script.
        level: Logging level (default: INFO)
        format_string: Log message format
        
    Returns:
        Configured logger
    """
    # Get the calling script's info
    calling_frame = sys._getframe(1)  # Go up one level to get the caller
    calling_file = calling_frame.f_globals['__file__']
    calling_path = Path(calling_file)
    
    # Generate log file name if not provided
    if log_file is None:
        log_file = calling_path.with_suffix('.log')
    
    # Ensure log file directory exists
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True  # Override any existing logging config
    )
    
    logger = logging.getLogger(calling_path.stem)  # Use script name as logger name
    
    # Log the setup info
    logger.info(f"Logging initialized for {calling_path.name}")
    logger.info(f"Log file: {log_file}")
    
    return logger


def load_data_config() -> Dict[str, Any]:
    """Load all parameters from config file."""
    config_path = Path("configs/data.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


