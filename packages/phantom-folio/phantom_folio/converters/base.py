# phantom_folio/converters/base.py
"""
Base classes for PDF to EPUB conversion.

This module provides the base classes for document handling and conversion.
"""

import abc
from typing import Dict, List, Any, Optional, Union, BinaryIO
from pathlib import Path

class Document(metaclass=abc.ABCMeta):
    """Base class for all document types."""
    
    def __init__(self, source: Union[str, Path, BinaryIO]) -> None:
        """
        Initialize a document from a file path or file-like object.
        
        Args:
            source: Path to the document file or file-like object
        """
        # Initialize instance variables that will be defined in subclasses
        self.metadata = {}  # Changed from self.metadata: Dict[str, str] = {}
        self._pages = None   # Changed from self.pages: List[Any] = []
    
    @property
    @abc.abstractmethod
    def page_count(self) -> int:
        """Get the number of pages in the document."""
        pass
    
    @property
    def pages(self):
        """Get all pages in the document."""
        return self._pages
    
    @abc.abstractmethod
    def close(self) -> None:
        """Close the document and free resources."""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class DocumentPage(metaclass=abc.ABCMeta):
    """Base class for document pages."""
    
    @property
    @abc.abstractmethod
    def text(self) -> str:
        """Get the text content of the page."""
        pass
    
    @property
    @abc.abstractmethod
    def images(self) -> List[Dict[str, Any]]:
        """Get the images on the page."""
        pass

class Converter(metaclass=abc.ABCMeta):
    """Base class for document format converters."""
    
    @abc.abstractmethod
    def convert(self, input_path: Union[str, Path], output_path: Union[str, Path], **options) -> bool:
        """
        Convert a document from one format to another.
        
        Args:
            input_path: Path to the input document
            output_path: Path where the output document will be saved
            **options: Additional conversion options
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        pass