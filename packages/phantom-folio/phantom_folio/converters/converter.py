"""
Main PDF to EPUB conversion module.

This module provides the high-level interface for converting PDF documents
to EPUB format, orchestrating the extraction, processing, and generation steps.
"""

import os
import sys
import tempfile
import shutil
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, BinaryIO

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from .base import Converter
from .pdf import PDFDocument
from .pdf_extractor import PDFContentExtractor
from .epub_generator import EPUBCreator, EPUBOptions

logger = logging.getLogger(__name__)

class ConversionOptions:
    """Options for PDF to EPUB conversion."""
    
    def __init__(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        language: str = "en",
        extract_toc: bool = True,
        use_ocr: bool = False,
        ocr_language: str = "eng",
        extract_images: bool = True,
        image_quality: int = 85,
        max_image_size: Optional[int] = 1200,
        min_image_size: int = 100,
        include_cover: bool = True,
        page_progression: str = "ltr",
        css: Optional[str] = None,
        publisher: Optional[str] = None,
        rights: Optional[str] = None,
        min_heading_size: float = 12.0,
        extract_colors: bool = True,
        detect_columns: bool = True,
        metadata: Optional[Dict[str, str]] = None
    ):
        """
        Initialize conversion options.
        
        Args:
            title: Document title (if None, extracted from PDF)
            author: Document author (if None, extracted from PDF)
            language: Document language code
            extract_toc: Whether to extract table of contents
            use_ocr: Whether to use OCR for scanned pages
            ocr_language: Language code for OCR (tesseract format)
            extract_images: Whether to extract images
            image_quality: JPEG quality for images (0-100)
            max_image_size: Maximum dimension for images (px)
            min_image_size: Minimum dimension to keep an image (px)
            include_cover: Whether to include cover page
            page_progression: Reading direction ('ltr' or 'rtl')
            css: Custom CSS for styling
            publisher: Publisher name
            rights: Rights/copyright information
            min_heading_size: Minimum font size to consider as heading
            extract_colors: Whether to extract and preserve colors
            detect_columns: Whether to detect and preserve column layout
            metadata: Additional metadata key-value pairs
        """
        self.title = title
        self.author = author
        self.language = language
        self.extract_toc = extract_toc
        self.use_ocr = use_ocr
        self.ocr_language = ocr_language
        self.extract_images = extract_images
        self.image_quality = image_quality
        self.max_image_size = max_image_size
        self.min_image_size = min_image_size
        self.include_cover = include_cover
        self.page_progression = page_progression
        self.css = css
        self.publisher = publisher
        self.rights = rights
        self.min_heading_size = min_heading_size
        self.extract_colors = extract_colors
        self.detect_columns = detect_columns
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary."""
        return {
            'title': self.title,
            'author': self.author,
            'language': self.language,
            'extract_toc': self.extract_toc,
            'use_ocr': self.use_ocr,
            'ocr_language': self.ocr_language,
            'extract_images': self.extract_images,
            'image_quality': self.image_quality,
            'max_image_size': self.max_image_size,
            'min_image_size': self.min_image_size,
            'include_cover': self.include_cover,
            'page_progression': self.page_progression,
            'css': self.css,
            'publisher': self.publisher,
            'rights': self.rights,
            'min_heading_size': self.min_heading_size,
            'extract_colors': self.extract_colors,
            'detect_columns': self.detect_columns,
            'metadata': self.metadata
        }

class PDFToEPUBConverter(Converter):
    """
    Converter for PDF to EPUB format with advanced options.
    
    This converter extracts content from PDF documents and generates
    high-quality EPUB files with preserved structure, formatting, and images.
    """
    
    def __init__(self, options: Optional[ConversionOptions] = None):
        """
        Initialize the converter.
        
        Args:
            options: Conversion options
        """
        self.options = options or ConversionOptions()
        
        # Check if OCR is available if requested
        if self.options.use_ocr and not TESSERACT_AVAILABLE:
            logger.warning("OCR requested but pytesseract is not available. Install with: pip install pytesseract")
            self.options.use_ocr = False
    
    def convert(self, input_path: Union[str, Path], output_path: Union[str, Path], **kwargs) -> bool:
        """
        Convert a PDF to EPUB.
        
        Args:
            input_path: Path to input PDF file
            output_path: Path to output EPUB file
            **kwargs: Additional options that override the instance options
            
        Returns:
            True if conversion was successful, False otherwise
        """
        start_time = time.time()
        logger.info(f"Starting conversion of {input_path} to {output_path}")
        
        # Update options with kwargs
        options = self.options
        for key, value in kwargs.items():
            if hasattr(options, key):
                setattr(options, key, value)
        
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp(prefix="phantom_folio_")
        logger.debug(f"Created temporary directory: {temp_dir}")
        
        try:
            # Load PDF document
            pdf_doc = PDFDocument(input_path)
            
            # Extract metadata for EPUB
            if not options.title:
                options.title = pdf_doc.metadata.get('title', 'Untitled Document')
            if not options.author:
                options.author = pdf_doc.metadata.get('author', 'Unknown Author')
            
            # Create content extractor
            extractor = PDFContentExtractor(
                pdf_doc=pdf_doc,
                min_heading_size=options.min_heading_size
            )
            
            # Extract content with structure analysis
            extractor.extract_content()
            
            # Create EPUB options
            epub_options = EPUBOptions(
                title=options.title,
                author=options.author,
                language=options.language,
                publisher=options.publisher,
                description=pdf_doc.metadata.get('subject', ''),
                subject=pdf_doc.metadata.get('keywords', ''),
                rights=options.rights,
                css=options.css,
                page_progression_direction=options.page_progression
            )
            
            # Extract cover image if requested
            if options.include_cover:
                # Try to extract first page as cover
                try:
                    first_page = pdf_doc.get_page(1)
                    if first_page:
                        cover_path = os.path.join(temp_dir, "cover.jpg")
                        img = first_page.render_to_pil(dpi=300)
                        img.save(cover_path, "JPEG", quality=options.image_quality)
                        epub_options.cover_image = cover_path
                except Exception as e:
                    logger.warning(f"Failed to extract cover image: {str(e)}")
            
            # Create EPUB generator
            epub_creator = EPUBCreator(options=epub_options)
            
            # Add content from extractor
            epub_creator.add_content_from_extractor(extractor)
            
            # Write EPUB
            epub_creator.write_epub(output_path)
            
            elapsed_time = time.time() - start_time
            logger.info(f"Conversion completed in {elapsed_time:.2f} seconds")
            
            return True
        
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}", exc_info=True)
            return False
        
        finally:
            # Clean up temporary directory
            try:
                shutil.rmtree(temp_dir)
                logger.debug(f"Removed temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary directory: {str(e)}")
    
    def convert_bytes(self, pdf_data: bytes, **kwargs) -> Optional[bytes]:
        """
        Convert PDF bytes to EPUB bytes.
        
        Args:
            pdf_data: PDF file content as bytes
            **kwargs: Conversion options
            
        Returns:
            EPUB file content as bytes, or None if conversion failed
        """
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file, \
             tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as epub_file:
            
            # Write PDF data to temporary file
            pdf_file.write(pdf_data)
            pdf_file.flush()
            
            # Close files to ensure they're written
            pdf_path = pdf_file.name
            epub_path = epub_file.name
        
        try:
            # Convert PDF to EPUB
            success = self.convert(pdf_path, epub_path, **kwargs)
            
            if success:
                # Read EPUB data
                with open(epub_path, "rb") as f:
                    epub_data = f.read()
                return epub_data
            
            return None
        
        finally:
            # Clean up temporary files
            try:
                os.unlink(pdf_path)
                os.unlink(epub_path)
            except Exception:
                pass

# Convenience function for simple conversion
def convert_pdf_to_epub(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    **options
) -> bool:
    """
    Convert a PDF file to EPUB format with the specified options.
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path to save the output EPUB file
        **options: Conversion options
        
    Returns:
        True if the conversion was successful, False otherwise
    """
    converter = PDFToEPUBConverter()
    return converter.convert(input_path, output_path, **options)