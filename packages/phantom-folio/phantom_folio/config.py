"""
Configuration module for Phantom Folio.

This module handles application configuration from environment variables
and configuration files.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Default configuration
DEFAULT_CONFIG = {
    # API settings
    'API_HOST': '0.0.0.0',
    'API_PORT': 8000,
    'API_WORKERS': 2,
    'API_TIMEOUT': 300,
    'API_MAX_UPLOAD_SIZE': 100 * 1024 * 1024,  # 100 MB
    
    # Database settings
    'DATABASE_URL': 'postgresql://postgres:postgres@db:5432/phantom_folio',
    
    # Redis settings
    'REDIS_URL': 'redis://redis:6379/0',
    
    # Storage settings
    'STORAGE_DIR': '/app/library',
    'TEMP_DIR': '/app/temp',
    'MODELS_DIR': '/app/models',
    'LOG_DIR': '/app/logs',
    
    # OCR settings
    'TESSERACT_DATA_DIR': '/app/models/tessdata',
    'DEFAULT_OCR_LANGUAGE': 'eng',
    
    # Conversion settings
    'DEFAULT_IMAGE_QUALITY': 85,
    'MAX_IMAGE_SIZE': 1200,
    
    # Worker settings
    'WORKER_CONCURRENCY': 2,
    'WORKER_MAX_TASKS_PER_CHILD': 100,
    
    # Logging settings
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': None,
    
    # Debug settings
    'DEBUG': False,
    'TESTING': False,
}

class Config:
    """Configuration management for Phantom Folio."""
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file (JSON or .env)
        """
        # Start with default config
        self._config = DEFAULT_CONFIG.copy()
        
        # Load from config file if provided
        if config_file:
            self._load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_env()
        
        # Normalize paths
        self._normalize_paths()
        
        # Set up logging
        self._setup_logging()
    
    def _load_from_file(self, config_file: Union[str, Path]) -> None:
        """Load configuration from file."""
        try:
            path = Path(config_file)
            
            if not path.exists():
                logging.warning(f"Config file not found: {path}")
                return
            
            # Load based on file extension
            if path.suffix.lower() == '.json':
                with open(path, 'r') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
            elif path.suffix.lower() == '.env':
                # Parse .env file
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                
                # Reload from environment
                self._load_from_env()
            else:
                logging.warning(f"Unsupported config file format: {path.suffix}")
        
        except Exception as e:
            logging.error(f"Error loading config file: {str(e)}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        for key in self._config.keys():
            env_value = os.environ.get(key)
            if env_value is not None:
                # Convert values to appropriate types
                if isinstance(self._config[key], bool):
                    self._config[key] = env_value.lower() in ('true', 'yes', '1', 'y')
                elif isinstance(self._config[key], int):
                    try:
                        self._config[key] = int(env_value)
                    except ValueError:
                        logging.warning(f"Invalid integer value for {key}: {env_value}")
                elif isinstance(self._config[key], float):
                    try:
                        self._config[key] = float(env_value)
                    except ValueError:
                        logging.warning(f"Invalid float value for {key}: {env_value}")
                else:
                    self._config[key] = env_value
    
    def _normalize_paths(self) -> None:
        """Normalize directory paths."""
        path_keys = ['STORAGE_DIR', 'TEMP_DIR', 'MODELS_DIR', 'LOG_DIR', 'TESSERACT_DATA_DIR']
        
        for key in path_keys:
            if self._config[key]:
                self._config[key] = os.path.normpath(self._config[key])
    
    def _setup_logging(self) -> None:
        """Configure logging based on settings."""
        log_level = getattr(logging, self._config['LOG_LEVEL'].upper(), logging.INFO)
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[logging.StreamHandler()]
        )
        
        # Add file handler if log file is specified
        if self._config['LOG_FILE']:
            try:
                # Create log directory if it doesn't exist
                log_file = Path(self._config['LOG_FILE'])
                log_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Add file handler
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(log_format))
                logging.getLogger().addHandler(file_handler)
            except Exception as e:
                logging.error(f"Error setting up log file: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key is not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary syntax."""
        return self._config[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if configuration contains a key."""
        return key in self._config
    
    def as_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self._config.copy()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            updates: Dictionary of configuration updates
        """
        self._config.update(updates)
        
        # Re-normalize paths if updated
        self._normalize_paths()

# Global configuration instance
config = Config()

def configure_from_file(config_file: Union[str, Path]) -> None:
    """
    Configure application from file.
    
    Args:
        config_file: Path to configuration file
    """
    global config
    config = Config(config_file)

def get_config() -> Config:
    """
    Get the current configuration.
    
    Returns:
        Config instance
    """
    return config