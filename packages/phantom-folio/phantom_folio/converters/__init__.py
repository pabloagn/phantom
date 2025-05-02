"""
Document conversion modules for Phantom Folio.

This package contains converters for transforming documents between different formats,
with a primary focus on PDF to EPUB conversion.
"""

from .pdf import PDFDocument, PDFPage
from .pdf_extractor import PDFContentExtractor, TextBlock, TextBlockType, DocumentSection
from .epub_generator import EPUBCreator, EPUBOptions, EPUBChapter
from .converter import PDFToEPUBConverter, ConversionOptions, convert_pdf_to_epub