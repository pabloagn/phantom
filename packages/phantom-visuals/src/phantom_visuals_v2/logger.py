# packages/phantom-visuals/src/phantom_visuals_v2/logger.py

"""Logging configuration for phantom_visuals_v2.

This module sets up logging for the phantom_visuals_v2 package,
with both file and console output.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

# Default log directory (can be overridden)
DEFAULT_LOG_DIR = os.path.join(os.path.expanduser("~"), ".phantom_visuals", "logs")

# Global console for rich output
console = Console()

# Global logger instance
logger = logging.getLogger("phantom_visuals")


def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    log_to_console: bool = True,
    log_to_file: bool = True,
) -> None:
    """Setup logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        log_to_console: Whether to log to console
        log_to_file: Whether to log to file
    """
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Set the log level
    logger.setLevel(numeric_level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s"
    )
    
    # Set up console logging if requested
    if log_to_console:
        console_handler = RichHandler(
            rich_tracebacks=True,
            console=console, 
            tracebacks_show_locals=True,
            markup=True
        )
        console_handler.setLevel(numeric_level)
        logger.addHandler(console_handler)
    
    # Set up file logging if requested
    if log_to_file:
        if log_dir is None:
            log_dir = DEFAULT_LOG_DIR
            
        # Create log directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"phantom_visuals_{timestamp}.log")
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(numeric_level)
        logger.addHandler(file_handler)
        
        # Log the location of the log file
        logger.info(f"Log file created at: {log_file}")
    
    # Log startup information
    logger.info("Phantom Visuals V2 logging initialized")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Log level: {log_level}")


def get_logger() -> logging.Logger:
    """Get the configured logger instance.

    Returns:
        Configured logger
    """
    return logger
