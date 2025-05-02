"""
PDF document handling functionality.

This module provides the core functionality for parsing and extracting content
from PDF documents, which will be used in the conversion process.
"""

import os
import tempfile
from typing import Dict, List, Any, Optional, Union, BinaryIO, Tuple, Iterator
from pathlib import Path
import logging

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")

try:
    from PIL import Image
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

from .base import Document, DocumentPage

logger = logging.getLogger(__name__)

class PDFPage(DocumentPage):
    """Represents a single page in a PDF document."""
    
    def __init__(self, page: fitz.Page):
        """
        Initialize a PDF page.
        
        Args:
            page: PyMuPDF page object
        """
        self._page = page
        self._text = None
        self._images = None
        self._rect = page.rect
        self._page_number = page.number + 1  # Page numbers are 0-based in PyMuPDF
    
    @property
    def text(self) -> str:
        """Get the text content of the page."""
        if self._text is None:
            self._text = self._page.get_text("text")
        return self._text
    
    @property
    def html(self) -> str:
        """Get the HTML representation of the page."""
        return self._page.get_text("html")
    
    @property
    def images(self) -> List[Dict[str, Any]]:
        """Get the images on the page."""
        if self._images is None:
            self._extract_images()
        return self._images
    
    @property
    def width(self) -> float:
        """Get the page width in points."""
        return self._rect.width
    
    @property
    def height(self) -> float:
        """Get the page height in points."""
        return self._rect.height
    
    @property
    def page_number(self) -> int:
        """Get the 1-based page number."""
        return self._page_number
    
    def _extract_images(self) -> None:
        """Extract images from the page."""
        self._images = []
        
        # Get image list
        img_list = self._page.get_images(full=True)
        
        for img_idx, img_info in enumerate(img_list):
            try:
                xref = img_info[0]
                
                # Extract image
                base_image = self._page.parent.extract_image(xref)
                
                if base_image:
                    image_data = {
                        'index': img_idx,
                        'width': base_image.get('width', 0),
                        'height': base_image.get('height', 0),
                        'ext': base_image.get('ext', ''),
                        'colorspace': base_image.get('colorspace', 0),
                        'xref': xref,
                        'image': base_image.get('image', None)
                    }
                    
                    self._images.append(image_data)
            except Exception as e:
                logger.warning(f"Failed to extract image {img_idx} from page {self._page_number}: {str(e)}")
    
    def get_image_as_pil(self, image_index: int) -> Optional[Image.Image]:
        """
        Get a specific image as a PIL Image object.
        
        Args:
            image_index: Index of the image to get
            
        Returns:
            PIL Image or None if image cannot be loaded
        """
        if self._images is None:
            self._extract_images()
        
        if not 0 <= image_index < len(self._images):
            return None
        
        try:
            image_data = self._images[image_index]['image']
            return Image.open(BytesIO(image_data))
        except Exception as e:
            logger.warning(f"Failed to convert image to PIL: {str(e)}")
            return None
    
    def render_to_pil(self, dpi: int = 300, alpha: bool = False) -> Image.Image:
        """
        Render the page to a PIL Image.
        
        Args:
            dpi: Resolution in dots per inch
            alpha: Whether to include an alpha channel
            
        Returns:
            PIL Image of the rendered page
        """
        # Calculate zoom factor based on DPI (72 is the base DPI for PDF)
        zoom = dpi / 72.0
        
        # Get pixmap
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = self._page.get_pixmap(matrix=matrix, alpha=alpha)
        
        # Convert to PIL Image
        if not alpha:
            return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        return Image.frombytes("RGBA", [pixmap.width, pixmap.height], pixmap.samples)

class PDFDocument(Document):
    """Class for handling PDF documents."""
    
    def __init__(self, source: Union[str, Path, BinaryIO]) -> None:
        """
        Initialize a PDF document.
        
        Args:
            source: Path to the PDF file or file-like object
        """
        super().__init__(source)
        
        # Convert Path to string if needed
        if isinstance(source, Path):
            source = str(source)
        
        # Open the PDF file
        self._pdf = fitz.open(source)
        self._extract_metadata()
        self._pages = None
    
    def _extract_metadata(self) -> None:
        """Extract metadata from the PDF document."""
        self.metadata = {}
        pdf_info = self._pdf.metadata
        
        if pdf_info:
            # Map common metadata fields
            field_map = {
                'title': 'title',
                'author': 'author',
                'subject': 'subject',
                'keywords': 'keywords',
                'creator': 'creator',
                'producer': 'producer',
                'creationDate': 'creation_date',
                'modDate': 'modification_date'
            }
            
            for pdf_field, meta_field in field_map.items():
                if pdf_field in pdf_info and pdf_info[pdf_field]:
                    value = pdf_info[pdf_field]
                    
                    # Clean up dates
                    if pdf_field in ('creationDate', 'modDate') and value.startswith('D:'):
                        # TODO: Parse PDF date format
                        pass
                    
                    self.metadata[meta_field] = value
        
        # Set default title if none exists
        if 'title' not in self.metadata or not self.metadata['title']:
            if hasattr(self._pdf, 'name') and self._pdf.name:
                # Use filename without extension as the title
                filename = os.path.basename(self._pdf.name)
                self.metadata['title'] = os.path.splitext(filename)[0]
            else:
                self.metadata['title'] = 'Untitled Document'
        
        # Set default author if none exists
        if 'author' not in self.metadata or not self.metadata['author']:
            self.metadata['author'] = 'Unknown Author'
    
    @property
    def page_count(self) -> int:
        """Get the number of pages in the document."""
        return len(self._pdf)
    
    @property
    def pages(self) -> List[PDFPage]:
        """Get all pages in the document."""
        if self._pages is None:
            self._pages = [PDFPage(self._pdf[i]) for i in range(len(self._pdf))]
        return self._pages
    
    def get_page(self, page_number: int) -> Optional[PDFPage]:
        """
        Get a specific page by number (1-based).
        
        Args:
            page_number: 1-based page number
            
        Returns:
            PDFPage object or None if page doesn't exist
        """
        # Convert to 0-based index
        idx = page_number - 1
        
        if 0 <= idx < len(self._pdf):
            return PDFPage(self._pdf[idx])
        return None
    
    def get_toc(self) -> List[Tuple[int, str, int]]:
        """
        Get the table of contents (outline) of the document.
        
        Returns:
            List of (level, title, page) tuples
        """
        return self._pdf.get_toc()
    
    def close(self) -> None:
        """Close the document and free resources."""
        if hasattr(self, '_pdf') and self._pdf:
            self._pdf.close()
            self._pdf = None