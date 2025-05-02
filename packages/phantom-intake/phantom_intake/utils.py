"""
Utility functions for Phantom Intake LibGen Downloader.
"""

import re
import os
from typing import Optional
from urllib.parse import unquote
from pathlib import Path


class FileHelpers:
    """Utility functions for file operations."""
    
    @staticmethod
    def get_filename_from_content_disposition(content_disposition: Optional[str]) -> Optional[str]:
        """
        Extract filename from Content-Disposition header.
        
        Args:
            content_disposition: The Content-Disposition header value
            
        Returns:
            The extracted filename or None if not found
        """
        if not content_disposition:
            return None
            
        fname = re.findall(
            r'filename\*?=["\']?(?:UTF-8\'\')?([^"\';]+)["\']?;?',
            content_disposition, 
            flags=re.IGNORECASE
        )
        
        if len(fname) == 1:
            return unquote(fname[0].strip())
            
        return None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing invalid characters.
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
        
        # Replace multiple spaces with single space
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Limit filename length to avoid file system issues
        if len(sanitized) > 200:
            name_part, ext_part = os.path.splitext(sanitized)
            sanitized = name_part[:195] + ext_part
            
        return sanitized
    
    @staticmethod
    def ensure_directory_exists(directory: Path) -> None:
        """
        Ensure that a directory exists, creating it if necessary.
        
        Args:
            directory: The directory path to check/create
        """
        directory.mkdir(parents=True, exist_ok=True)


class TextFormatters:
    """Utility functions for text formatting."""
    
    @staticmethod
    def format_bytes(size: int) -> str:
        """
        Format byte size to human-readable format.
        
        Args:
            size: Size in bytes
            
        Returns:
            Human-readable size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0 or unit == 'TB':
                break
            size /= 1024.0
        return f"{size:.2f} {unit}"