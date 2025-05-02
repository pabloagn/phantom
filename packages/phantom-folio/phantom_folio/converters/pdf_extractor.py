"""
Advanced PDF content extraction with layout analysis and hierarchical structure detection.

This module goes beyond basic text extraction by analyzing document structure,
detecting sections, paragraphs, headings, and preserving the reading order.
"""

import os
import re
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Tuple, Optional, Union, Any, Iterator
from pathlib import Path
import logging
from collections import defaultdict

try:
    import fitz  # PyMuPDF
    from fitz import Rect
except ImportError:
    raise ImportError("PyMuPDF (fitz) is required. Install with: pip install PyMuPDF")

try:
    import cv2
    import numpy as np
    from PIL import Image
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    # Import just PIL for basic functionality
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow is required. Install with: pip install pillow")

from .pdf import PDFDocument, PDFPage

logger = logging.getLogger(__name__)

class TextBlockType(Enum):
    """Types of text blocks in a document."""
    TITLE = "title"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    CAPTION = "caption"
    FOOTER = "footer"
    HEADER = "header"
    CODE = "code"
    QUOTE = "quote"
    UNKNOWN = "unknown"

@dataclass(frozen=True, eq=True)
class TextBlock:
    """Represents a block of text with position and formatting information."""
    text: str
    block_type: TextBlockType = TextBlockType.PARAGRAPH
    bbox: Tuple[float, float, float, float] = None  # x0, y0, x1, y1
    font_size: float = None
    font_name: str = None
    is_bold: bool = False
    is_italic: bool = False
    line_spacing: float = None
    char_spacing: float = None
    alignment: str = None  # left, right, center, justify
    indentation: float = 0
    page_number: int = None
    
    def __post_init__(self):
        # Since we're frozen, we need to use object.__setattr__ to set values in __post_init__
        if self.text:
            object.__setattr__(self, "text", self.text.strip())
        # Create the children field as a separate attribute that won't be included in hash
        object.__setattr__(self, "children", [])
    
    def __hash__(self):
        # Create a custom hash based on immutable attributes
        return hash((self.text, self.block_type, self.page_number))
    
    @property
    def word_count(self) -> int:
        """Count the number of words in this text block."""
        return len(re.findall(r'\w+', self.text))
    
    @property
    def is_empty(self) -> bool:
        """Check if the text block is empty."""
        return not self.text.strip()
    
    @property
    def width(self) -> Optional[float]:
        """Get the width of the text block."""
        if self.bbox:
            return self.bbox[2] - self.bbox[0]
        return None
    
    @property
    def height(self) -> Optional[float]:
        """Get the height of the text block."""
        if self.bbox:
            return self.bbox[3] - self.bbox[1]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the text block to a dictionary."""
        return {
            'text': self.text,
            'type': self.block_type.value,
            'bbox': self.bbox,
            'font_size': self.font_size,
            'font_name': self.font_name,
            'is_bold': self.is_bold,
            'is_italic': self.is_italic,
            'alignment': self.alignment,
            'indentation': self.indentation,
            'page_number': self.page_number,
            'children': [child.to_dict() for child in self.children]
        }
    
    def __str__(self) -> str:
        type_name = self.block_type.value if self.block_type else "unknown"
        return f"<TextBlock type={type_name} page={self.page_number} words={self.word_count}>"

@dataclass
class DocumentSection:
    """Represents a section in a document with hierarchical structure."""
    title: str
    level: int
    blocks: List[TextBlock] = field(default_factory=list)
    subsections: List['DocumentSection'] = field(default_factory=list)
    page_span: Tuple[int, int] = None  # start_page, end_page
    
    @property
    def word_count(self) -> int:
        """Count the total number of words in this section including subsections."""
        count = sum(block.word_count for block in self.blocks)
        count += sum(section.word_count for section in self.subsections)
        return count
    
    def add_subsection(self, section: 'DocumentSection') -> None:
        """Add a subsection to this section."""
        self.subsections.append(section)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the section to a dictionary."""
        return {
            'title': self.title,
            'level': self.level,
            'page_span': self.page_span,
            'blocks': [block.to_dict() for block in self.blocks],
            'subsections': [section.to_dict() for section in self.subsections]
        }
    
    def __str__(self) -> str:
        return f"<Section level={self.level} title='{self.title}' subsections={len(self.subsections)}>"

class PDFContentExtractor:
    """Advanced content extraction from PDF documents with structure analysis."""
    
    def __init__(self, pdf_doc: PDFDocument, min_heading_size: float = 12.0):
        """
        Initialize the content extractor.
        
        Args:
            pdf_doc: PDFDocument to extract content from
            min_heading_size: Minimum font size to consider as a heading
        """
        self.pdf = pdf_doc
        self.min_heading_size = min_heading_size
        self.text_blocks: List[TextBlock] = []
        self.document_sections: List[DocumentSection] = []
        self._extracted = False
    
    def extract_content(self) -> None:
        """Extract all content from the PDF document with structure analysis."""
        if self._extracted:
            return
        
        logger.info(f"Extracting content from PDF with {self.pdf.page_count} pages")
        
        # First pass: Extract raw text blocks from each page
        self._extract_text_blocks()
        
        # Second pass: Classify text blocks by type
        self._classify_blocks()
        
        # Third pass: Build document structure
        self._build_document_structure()
        
        self._extracted = True
        logger.info(f"Extracted {len(self.text_blocks)} text blocks and {len(self.document_sections)} top-level sections")
    
    def _extract_text_blocks(self) -> None:
        """Extract text blocks from all pages with position and formatting info."""
        for page_idx, page in enumerate(self.pdf.pages):
            page_num = page_idx + 1
            logger.debug(f"Extracting text blocks from page {page_num}")
            
            # Get page dimensions
            page_width = page.width
            page_height = page.height
            
            # Extract blocks with PyMuPDF's advanced text extraction
            try:
                # Get all blocks with detailed information
                blocks = page._page.get_text("dict", flags=fitz.TEXT_PRESERVE_LIGATURES | fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
                
                for block_idx, block in enumerate(blocks):
                    # Process text blocks only (skip image blocks)
                    if "lines" in block:
                        # Process all lines in the block
                        for line in block["lines"]:
                            # Get line position and formatting info
                            if not line["spans"]:
                                continue
                                
                            spans = line["spans"]
                            spans_text = [span["text"] for span in spans]
                            line_text = "".join(spans_text)
                            
                            # Skip empty lines
                            if not line_text.strip():
                                continue
                            
                            # Extract bounding box
                            bbox = (line["bbox"][0], line["bbox"][1], line["bbox"][2], line["bbox"][3])
                            
                            # Extract font properties from the first span (may need refinement)
                            span = spans[0]
                            font_name = span["font"]
                            font_size = span["size"]
                            is_bold = "bold" in font_name.lower() or span.get("flags", 0) & 2 > 0
                            is_italic = "italic" in font_name.lower() or span.get("flags", 0) & 4 > 0
                            
                            # Create text block
                            text_block = TextBlock(
                                text=line_text,
                                bbox=bbox,
                                font_size=font_size,
                                font_name=font_name,
                                is_bold=is_bold,
                                is_italic=is_italic,
                                page_number=page_num
                            )
                            
                            self.text_blocks.append(text_block)
            
            except Exception as e:
                logger.error(f"Error extracting text blocks from page {page_num}: {str(e)}")
    
    def _classify_blocks(self) -> None:
        """Classify text blocks by type based on formatting and position."""
        if not self.text_blocks:
            return
        
        # Group blocks by page
        pages_blocks = defaultdict(list)
        for block in self.text_blocks:
            pages_blocks[block.page_number].append(block)
        
        # Calculate average font size across the document
        font_sizes = [block.font_size for block in self.text_blocks if block.font_size]
        avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12.0
        
        # Process each page separately
        for page_num, blocks in pages_blocks.items():
            # Sort blocks by vertical position
            blocks.sort(key=lambda b: b.bbox[1] if b.bbox else float('inf'))
            
            # Get page dimensions
            page = self.pdf.get_page(page_num)
            page_height = page.height if page else 792  # Default to US Letter height
            
            # Classify each block
            for i, block in enumerate(blocks):
                # Skip blocks without font information
                if not block.font_size:
                    continue
                
                # Determine if the block is in the header/footer area
                y_pos = block.bbox[1] if block.bbox else 0
                y_bottom = block.bbox[3] if block.bbox else 0
                is_header = y_pos < page_height * 0.1  # Top 10%
                is_footer = y_bottom > page_height * 0.9  # Bottom 10%
                
                # Classifier logic
                if is_header and block.word_count < 10:
                    block.block_type = TextBlockType.HEADER
                elif is_footer and block.word_count < 10:
                    block.block_type = TextBlockType.FOOTER
                elif block.font_size >= self.min_heading_size and block.font_size > avg_font_size * 1.2:
                    if i == 0 and block.font_size > avg_font_size * 1.5:
                        block.block_type = TextBlockType.TITLE
                    else:
                        block.block_type = TextBlockType.HEADING
                elif block.is_bold and block.word_count < 20:
                    block.block_type = TextBlockType.HEADING
                elif block.text.strip().startswith(('•', '-', '*', '◦', '▪', '○', '►', '→')) or re.match(r'^\d+\.', block.text.strip()):
                    block.block_type = TextBlockType.LIST_ITEM
                elif block.width and block.width < page.width * 0.7 and i > 0 and i < len(blocks) - 1:
                    # Blocks significantly narrower than the page width might be captions
                    block.block_type = TextBlockType.CAPTION
                else:
                    block.block_type = TextBlockType.PARAGRAPH
    
    def _build_document_structure(self) -> None:
        """Build document structure by organizing text blocks into hierarchical sections."""
        if not self.text_blocks:
            return
        
        # Find all heading blocks
        heading_blocks = [b for b in self.text_blocks if b.block_type in (TextBlockType.TITLE, TextBlockType.HEADING)]
        
        # If no headings are detected, create a single section
        if not heading_blocks:
            section = DocumentSection(
                title=self.pdf.metadata.get('title', 'Untitled Document'),
                level=0,
                page_span=(1, self.pdf.page_count)
            )
            section.blocks = self.text_blocks
            self.document_sections = [section]
            return
        
        # Sort headings by page number and position
        heading_blocks.sort(key=lambda b: (b.page_number, b.bbox[1] if b.bbox else 0))
        
        # Determine heading levels based on font size
        heading_sizes = [(b, b.font_size) for b in heading_blocks if b.font_size]
        if heading_sizes:
            # Sort by font size descending
            heading_sizes.sort(key=lambda x: x[1], reverse=True)
            
            # Group similar font sizes
            size_groups = []
            current_group = [heading_sizes[0]]
            
            for i in range(1, len(heading_sizes)):
                current, current_size = heading_sizes[i]
                previous, previous_size = heading_sizes[i-1]
                
                # If sizes are close, group them
                if abs(current_size - previous_size) < 0.5:
                    current_group.append(heading_sizes[i])
                else:
                    size_groups.append(current_group)
                    current_group = [heading_sizes[i]]
            
            size_groups.append(current_group)
            
            # Assign levels to heading blocks based on font size groups
            level_map = {}
            for level, group in enumerate(size_groups):
                for block, _ in group:
                    level_map[block] = level
            
            # Assign levels to all heading blocks
            for block in heading_blocks:
                if block in level_map:
                    block.block_type = TextBlockType.TITLE if level_map[block] == 0 else TextBlockType.HEADING
                else:
                    # Fallback for headings without font size
                    block.block_type = TextBlockType.HEADING
        
        # Create sections from headings
        current_sections = []
        current_blocks = []
        
        # Process all blocks in order
        for block in sorted(self.text_blocks, key=lambda b: (b.page_number, b.bbox[1] if b.bbox else 0)):
            if block.block_type in (TextBlockType.TITLE, TextBlockType.HEADING):
                # Start a new section
                level = level_map.get(block, 0) if heading_sizes else 0
                
                # Create section for accumulated blocks if any
                if current_blocks and not current_sections:
                    # Create an untitled section for content before the first heading
                    untitled = DocumentSection(
                        title="",
                        level=0,
                        blocks=current_blocks.copy()
                    )
                    self.document_sections.append(untitled)
                    current_blocks = []
                
                # Create the new section
                section = DocumentSection(
                    title=block.text,
                    level=level,
                    blocks=[block]  # Include the heading block itself
                )
                
                # Find the parent section for this heading
                parent = None
                for s in reversed(current_sections):
                    if s.level < level:
                        parent = s
                        break
                
                if parent:
                    parent.add_subsection(section)
                else:
                    self.document_sections.append(section)
                
                # Update current sections stack
                while current_sections and current_sections[-1].level >= level:
                    current_sections.pop()
                current_sections.append(section)
                
            else:
                # Add block to the current section
                if current_sections:
                    current_sections[-1].blocks.append(block)
                else:
                    current_blocks.append(block)
        
        # Handle any remaining blocks
        if current_blocks:
            untitled = DocumentSection(
                title="",
                level=0,
                blocks=current_blocks
            )
            self.document_sections.append(untitled)
    
    def get_text_blocks(self, block_type: Optional[TextBlockType] = None) -> List[TextBlock]:
        """
        Get all text blocks, optionally filtered by type.
        
        Args:
            block_type: Optional filter for block type
            
        Returns:
            List of text blocks
        """
        if not self._extracted:
            self.extract_content()
        
        if block_type:
            return [b for b in self.text_blocks if b.block_type == block_type]
        return self.text_blocks
    
    def get_document_structure(self) -> List[DocumentSection]:
        """
        Get the hierarchical document structure.
        
        Returns:
            List of top-level document sections
        """
        if not self._extracted:
            self.extract_content()
        
        return self.document_sections
    
    def get_document_toc(self) -> List[Tuple[int, str, int]]:
        """
        Get table of contents from document structure.
        
        Returns:
            List of (level, title, page_number) tuples
        """
        if not self._extracted:
            self.extract_content()
        
        toc = []
        
        def process_section(section, depth=0):
            if section.title:
                # Find the first page containing this section
                page = None
                for block in section.blocks:
                    if block.page_number:
                        page = block.page_number
                        break
                
                if page:
                    toc.append((depth, section.title, page))
            
            for subsection in section.subsections:
                process_section(subsection, depth + 1)
        
        for section in self.document_sections:
            process_section(section)
        
        return toc
    
    def get_plain_text(self) -> str:
        """
        Get the entire document as plain text.
        
        Returns:
            Document text as a single string
        """
        if not self._extracted:
            self.extract_content()
        
        text = []
        
        # Sort blocks by page and position
        sorted_blocks = sorted(
            self.text_blocks,
            key=lambda b: (b.page_number or 0, b.bbox[1] if b.bbox else float('inf'))
        )
        
        current_page = None
        for block in sorted_blocks:
            if block.page_number != current_page:
                if current_page is not None:
                    text.append("\n\n--- Page {} ---\n\n".format(block.page_number))
                current_page = block.page_number
            
            text.append(block.text)
            text.append("\n")
        
        return "".join(text)
    
    def get_document_metadata(self) -> Dict[str, Any]:
        """
        Get comprehensive document metadata and statistics.
        
        Returns:
            Dictionary of metadata and document statistics
        """
        if not self._extracted:
            self.extract_content()
            
        # Basic metadata from PDF
        metadata = dict(self.pdf.metadata)
        
        # Add structural statistics
        metadata['page_count'] = self.pdf.page_count
        metadata['text_block_count'] = len(self.text_blocks)
        metadata['section_count'] = len(self.document_sections)
        
        # Count block types
        block_type_counts = defaultdict(int)
        for block in self.text_blocks:
            block_type_counts[block.block_type.value] += 1
        
        metadata['block_types'] = dict(block_type_counts)
        
        # Count total words
        metadata['word_count'] = sum(block.word_count for block in self.text_blocks)
        
        # Extract table of contents
        metadata['toc'] = self.get_document_toc()
        
        return metadata