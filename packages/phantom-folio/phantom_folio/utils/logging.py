"""
Logging configuration for Phantom Folio.

This module sets up logging for the application, with support for
console and file output.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union

def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (if None, logs to console only)
        log_format: Logging format (if None, uses default format)
        date_format: Date format for log messages (if None, uses default)
        
    Returns:
        Logger object
    """
    # Set default formats if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if requested
    if log_file is not None:
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_dir = log_path.parent
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(log_format, date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Get the application logger
    app_logger = logging.getLogger('phantom_folio')
    
    return app_logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name
        
    Returns:
        Logger object
    """
    return logging.getLogger(f'phantom_folio.{name}')