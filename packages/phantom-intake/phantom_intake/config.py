"""
Configuration handling for LibGen Downloader.
"""

import os
import logging
import yaml
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional, Dict, Any


# Constants
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3
DEFAULT_REQUEST_DELAY = 2
DEFAULT_CONFIG_FILE = "config.yaml"


@dataclass
class AppConfig:
    """Application configuration settings."""
    input_dir: Path
    output_dir: Path
    urls_file: str
    log_dir: Path
    max_retries: int
    timeout_seconds: int
    delay_seconds: int
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"


def setup_logging(log_dir: Path, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up application logging with standard formatting.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level
        
    Returns:
        Configured logger instance
    """
    import time
    
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"phantom_intake_{time.strftime('%Y%m%d')}.log"
    
    # Configure logging with a clean format
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Create and return application logger
    logger = logging.getLogger("phantom_intake")
    
    # Disable propagation to avoid duplicate log messages
    logger.propagate = False
    
    return logger


def create_default_config() -> AppConfig:
    """
    Create default application configuration.
    
    Returns:
        Default AppConfig instance
    """
    # Get the base directory (where phantom-intake.py is located)
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    return AppConfig(
        input_dir=base_dir / "input",
        output_dir=base_dir / "outputs",
        urls_file="download.txt",
        log_dir=base_dir / "logs",
        max_retries=DEFAULT_MAX_RETRIES,
        timeout_seconds=DEFAULT_TIMEOUT,
        delay_seconds=DEFAULT_REQUEST_DELAY
    )


def config_to_dict(config: AppConfig) -> Dict[str, Any]:
    """
    Convert AppConfig to a dictionary suitable for YAML serialization.
    
    Args:
        config: AppConfig instance
        
    Returns:
        Dictionary representation of config
    """
    # Convert to dict
    config_dict = asdict(config)
    
    # Convert Path objects to strings
    for key, value in config_dict.items():
        if isinstance(value, Path):
            config_dict[key] = str(value)
            
    return config_dict


def dict_to_config(config_dict: Dict[str, Any]) -> AppConfig:
    """
    Convert dictionary to AppConfig, ensuring Paths are properly converted.
    
    Args:
        config_dict: Dictionary with configuration
        
    Returns:
        AppConfig instance
    """
    # Convert string paths to Path objects
    for key in ['input_dir', 'output_dir', 'log_dir']:
        if key in config_dict and isinstance(config_dict[key], str):
            config_dict[key] = Path(config_dict[key])
    
    # Filter out any keys not in the AppConfig class
    valid_keys = {field.name for field in AppConfig.__dataclass_fields__.values()}
    filtered_dict = {key: value for key, value in config_dict.items() if key in valid_keys}
    
    # Create AppConfig instance
    return AppConfig(**filtered_dict)


def save_config(config: AppConfig, config_path: Optional[Path] = None) -> None:
    """
    Save configuration to YAML file.
    
    Args:
        config: AppConfig instance
        config_path: Path to save configuration to, defaults to base_dir/config.yaml
    """
    if config_path is None:
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = base_dir / DEFAULT_CONFIG_FILE
        
    with open(config_path, 'w') as f:
        yaml.dump(config_to_dict(config), f, default_flow_style=False)


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """
    Load configuration from YAML file or create default if file doesn't exist.
    
    Args:
        config_path: Path to load configuration from, defaults to base_dir/config.yaml
        
    Returns:
        AppConfig instance
    """
    if config_path is None:
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = base_dir / DEFAULT_CONFIG_FILE
    
    # If config file exists, load it
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config_dict = yaml.safe_load(f)
                return dict_to_config(config_dict)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            print("Using default configuration instead.")
            config = create_default_config()
            return config
    
    # Otherwise create default config and save it
    config = create_default_config()
    try:
        save_config(config, config_path)
        print(f"Created new configuration file at {config_path}")
    except Exception as e:
        print(f"Warning: Could not save default configuration to {config_path}: {e}")
        
    return config