"""
Health check utilities for Phantom Folio.

This module provides functions to check the health of the application and its dependencies.
"""

import os
import sys
import subprocess
import importlib
from typing import Dict, List, Tuple, Optional, Union, Any
import logging

logger = logging.getLogger(__name__)

def check_system_dependency(command: str, args: List[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Check if a system dependency is available.
    
    Args:
        command: Command to check
        args: Arguments to pass to the command (default: ["--version"])
        
    Returns:
        Tuple of (success, version)
    """
    if args is None:
        args = ["--version"]
    
    try:
        result = subprocess.run(
            [command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Try to extract version from stdout or stderr
            output = result.stdout or result.stderr
            return True, output.strip()
        else:
            logger.warning(f"Command {command} returned non-zero exit code: {result.returncode}")
            return False, "not available"  # Return string instead of None
    except FileNotFoundError:
        logger.warning(f"Command {command} not found")
        return False, "not found"  # Return string instead of None
    except subprocess.TimeoutExpired:
        logger.warning(f"Command {command} timed out")
        return False, "timed out"  # Return string instead of None
    except Exception as e:
        logger.error(f"Error checking {command}: {str(e)}")
        return False, f"error: {str(e)}"  # Return string instead of None

def check_python_dependency(module_name: str, package_name: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Check if a Python dependency is available.
    
    Args:
        module_name: Name of the module to import
        package_name: Name of the package (if different from module_name)
        
    Returns:
        Tuple of (success, version)
    """
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', None)
        
        if version is None and hasattr(module, 'version'):
            version = module.version
        
        if version is None:
            version = "unknown version"
        
        return True, version
    except ImportError as e:
        logger.warning(f"Module {module_name} not found: {str(e)}")
        return False, None
    except Exception as e:
        logger.error(f"Error importing {module_name}: {str(e)}")
        return False, None

def check_tesseract() -> Tuple[bool, Optional[str]]:
    """
    Check if Tesseract OCR is available.
    
    Returns:
        Tuple of (success, version)
    """
    # First check if the Python binding is available
    py_success, _ = check_python_dependency('pytesseract')
    if not py_success:
        return False, None
    
    # Then check if the Tesseract executable is available
    import pytesseract
    try:
        version = pytesseract.get_tesseract_version()
        return True, str(version)
    except Exception as e:
        logger.error(f"Error getting Tesseract version: {str(e)}")
        return False, None

def check_docker() -> Tuple[bool, Optional[str]]:
    """
    Check if Docker is available.
    
    Returns:
        Tuple of (success, version)
    """
    return check_system_dependency('docker')

def check_database() -> bool:
    """
    Check if the database is available.
    
    Returns:
        True if the database is available, False otherwise
    """
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.sql import text
        
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            logger.warning("DATABASE_URL environment variable not set")
            return False
        
        # Create engine and try to connect
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        return False

def check_redis() -> bool:
    """
    Check if Redis is available.
    
    Returns:
        True if Redis is available, False otherwise
    """
    try:
        import redis
        
        # Get Redis URL from environment
        redis_url = os.environ.get('REDIS_URL')
        if not redis_url:
            logger.warning("REDIS_URL environment variable not set")
            return False
        
        # Try to connect to Redis
        client = redis.from_url(redis_url)
        return client.ping()
    except Exception as e:
        logger.error(f"Error connecting to Redis: {str(e)}")
        return False

def check_worker_health() -> bool:
    """
    Check if the worker is healthy.
    
    Returns:
        True if the worker is healthy, False otherwise
    """
    # Check core dependencies
    dependencies = [
        ('fitz', None),
        ('pdf2image', None),
        ('PIL', None),
        ('ebooklib', None),
        ('pytesseract', None)
    ]
    
    for module_name, package_name in dependencies:
        success, _ = check_python_dependency(module_name, package_name)
        if not success:
            return False
    
    # Check Tesseract
    tesseract_ok, _ = check_tesseract()
    if not tesseract_ok:
        return False
    
    return True

def check_api_health() -> Dict[str, Any]:
    """
    Comprehensive health check for the API.
    
    Returns:
        Dictionary with health check results
    """
    health_info = {
        'status': 'healthy',
        'version': os.environ.get('APP_VERSION', 'unknown'),
        'dependencies': {},
        'services': {}
    }
    
    # Check Python dependencies
    python_deps = [
        ('fitz', 'PyMuPDF'),
        ('pdf2image', None),
        ('PIL', 'Pillow'),
        ('ebooklib', None),
        ('pytesseract', None),
        ('fastapi', None)
    ]
    
    for module_name, package_name in python_deps:
        success, version = check_python_dependency(module_name, package_name)
        dep_name = package_name or module_name
        health_info['dependencies'][dep_name] = {
            'status': 'available' if success else 'missing',
            'version': version or 'not available'  # Ensure version is never None
        }
        
        if not success and dep_name in ['PyMuPDF', 'Pillow', 'ebooklib']:
            health_info['status'] = 'degraded'
    
    # Check system dependencies
    system_deps = [
        ('tesseract', ['--version']),
        ('convert', ['-version']),  # ImageMagick
        ('gs', ['--version'])  # Ghostscript
    ]
    
    for command, args in system_deps:
        success, version = check_system_dependency(command, args)
        health_info['dependencies'][command] = {
            'status': 'available' if success else 'missing',
            'version': version  # This is now always a string
        }
        
        if not success and command == 'tesseract':
            health_info['status'] = 'degraded'
    
    # Check services
    # Database
    db_ok = check_database()
    health_info['services']['database'] = {
        'status': 'available' if db_ok else 'unavailable'
    }
    
    if not db_ok:
        health_info['status'] = 'degraded'
    
    # Redis
    redis_ok = check_redis()
    health_info['services']['redis'] = {
        'status': 'available' if redis_ok else 'unavailable'
    }
    
    if not redis_ok:
        health_info['status'] = 'degraded'
    
    return health_info