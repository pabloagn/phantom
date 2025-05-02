"""
Advanced EPUB generation with customizable styling and structure preservation.

This module creates high-quality EPUB files from structured document content,
with support for complex layouts, custom styling, and metadata.
"""

import os
import uuid
import tempfile
import re
import shutil
import io
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Union, Any, BinaryIO
from pathlib import Path
import logging
from datetime import datetime

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    raise ImportError("EbookLib is required. Install with: pip install EbookLib")

try:
    from PIL import Image
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

try:
    from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape, Template
except ImportError:
    raise ImportError("Jinja2 is required. Install with: pip install Jinja2")

from .pdf_extractor import TextBlock, TextBlockType, DocumentSection, PDFContentExtractor

logger = logging.getLogger(__name__)

# Default CSS for styling EPUB content
DEFAULT_CSS = """
@charset "utf-8";

/* Global styles */
body {
    font-family: "Bookerly", "Palatino", "Georgia", serif;
    margin: 5% 5% 5% 5%;
    text-align: justify;
    line-height: 1.5;
    hyphens: auto;
    -webkit-hyphens: auto;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Bookerly", "Palatino", "Georgia", serif;
    line-height: 1.2;
    margin-top: 1em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
    page-break-inside: avoid;
}

h1 {
    font-size: 1.5em;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
}

h2 {
    font-size: 1.3em;
    margin-top: 1.5em;
}

h3 {
    font-size: 1.1em;
}

p {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    text-indent: 1.5em;
    widows: 2;
    orphans: 2;
}

/* First paragraph after heading shouldn't be indented */
h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p {
    text-indent: 0;
}

/* Lists */
ul, ol {
    margin-left: 1em;
    margin-right: 0;
    padding-left: 0.5em;
}

li {
    margin-top: 0.2em;
    margin-bottom: 0.2em;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}

.image-container {
    text-align: center;
    margin: 1em auto;
    page-break-inside: avoid;
}

/* Figure and captions */
figure {
    margin: 1em 0;
    page-break-inside: avoid;
    text-align: center;
}

figcaption {
    font-size: 0.9em;
    font-style: italic;
    text-align: center;
    margin-top: 0.5em;
}

/* Tables */
table {
    border-collapse: collapse;
    margin: 1em auto;
    max-width: 100%;
}

th, td {
    border: 1px solid #ccc;
    padding: 0.5em;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
}

/* Code blocks */
pre {
    font-family: "Courier New", Courier, monospace;
    background-color: #f5f5f5;
    padding: 1em;
    white-space: pre-wrap;
    margin: 1em 0;
    font-size: 0.9em;
    border-radius: 0.3em;
}

code {
    font-family: "Courier New", Courier, monospace;
    font-size: 0.9em;
}

/* Quotes */
blockquote {
    margin: 1em 2em;
    padding-left: 1em;
    border-left: 0.25em solid #ccc;
    font-style: italic;
}

/* Cover */
.cover {
    text-align: center;
    max-height: 100%;
    page-break-after: always;
}

.cover img {
    max-height: 100%;
    max-width: 100%;
}

/* Table of contents */
.toc {
    page-break-before: always;
    page-break-after: always;
}

.toc h1 {
    text-align: center;
    margin-bottom: 2em;
}

.toc ul {
    list-style-type: none;
    padding-left: 0;
}

.toc li {
    margin-bottom: 0.5em;
}

.toc a {
    text-decoration: none;
    color: black;
}

/* Footnotes */
.footnote {
    font-size: 0.9em;
    vertical-align: super;
}

.footnotes {
    margin-top: 2em;
    border-top: 1px solid #ccc;
    padding-top: 1em;
    font-size: 0.9em;
}

/* Header and footer */
.header, .footer {
    font-size: 0.8em;
    color: #666;
    text-align: center;
    margin: 1em 0;
}
"""

# Default EPUB templates using Jinja2
COVER_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="style/stylesheet.css" />
</head>
<body>
    <div class="cover">
        <h1>{{ title }}</h1>
        {% if author %}
        <h2>{{ author }}</h2>
        {% endif %}
        {% if cover_image %}
        <div class="cover-image">
            <img src="{{ cover_image }}" alt="Cover" />
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

TOC_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Table of Contents</title>
    <link rel="stylesheet" type="text/css" href="style/stylesheet.css" />
</head>
<body>
    <div class="toc">
        <h1>Table of Contents</h1>
        <nav epub:type="toc" id="toc">
            <ol>
                {% for item in toc_items %}
                <li><a href="{{ item.href }}">{{ item.title }}</a>
                    {% if item.children %}
                    <ol>
                        {% for child in item.children %}
                        <li><a href="{{ child.href }}">{{ child.title }}</a></li>
                        {% endfor %}
                    </ol>
                    {% endif %}
                </li>
                {% endfor %}
            </ol>
        </nav>
    </div>
</body>
</html>
"""

CHAPTER_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="style/stylesheet.css" />
</head>
<body>
    <h1>{{ title }}</h1>
    {% for content_block in content_blocks %}
        {{ content_block|safe }}
    {% endfor %}
</body>
</html>
"""

@dataclass
class EPUBOptions:
    """Options for EPUB generation."""
    title: str = "Untitled Document"
    author: str = "Unknown Author"
    language: str = "en"
    publisher: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    rights: Optional[str] = None
    identifier: Optional[str] = None
    publication_date: Optional[str] = None
    modified_date: Optional[str] = None
    css: Optional[str] = None
    cover_image: Optional[Union[str, bytes, Path]] = None
    toc_title: str = "Table of Contents"
    include_toc: bool = True
    chapter_template: Optional[str] = None
    cover_template: Optional[str] = None
    toc_template: Optional[str] = None
    page_progression_direction: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        # Set default dates if not provided
        if not self.publication_date:
            self.publication_date = datetime.now().strftime("%Y-%m-%d")
        if not self.modified_date:
            self.modified_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Generate a UUID identifier if none provided
        if not self.identifier:
            self.identifier = str(uuid.uuid4())
        
        # Use default CSS if none provided
        if not self.css:
            self.css = DEFAULT_CSS
        
        # Use default templates if none provided
        if not self.chapter_template:
            self.chapter_template = CHAPTER_TEMPLATE
        if not self.cover_template:
            self.cover_template = COVER_TEMPLATE
        if not self.toc_template:
            self.toc_template = TOC_TEMPLATE

@dataclass
class EPUBChapter:
    """Represents a chapter in an EPUB book."""
    title: str
    content: Union[str, List[str]]
    filename: str
    level: int = 1
    images: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Process content after initialization."""
        if isinstance(self.content, list):
            self.content = "\n".join(self.content)

class EPUBCreator:
    """Advanced EPUB file creation with structured content and custom styling."""
    
    def __init__(self, options: Optional[EPUBOptions] = None):
        """
        Initialize the EPUB creator.
        
        Args:
            options: EPUB generation options
        """
        self.options = options or EPUBOptions()
        self.chapters: List[EPUBChapter] = []
        self.images: Dict[str, Dict[str, Any]] = {}
        self.book = None
        self.toc_items = []
        
        # Initialize Jinja2 templates
        self.env = Environment(autoescape=select_autoescape(['html', 'xml']))
        self.chapter_template = self.env.from_string(self.options.chapter_template)
        self.cover_template = self.env.from_string(self.options.cover_template)
        self.toc_template = self.env.from_string(self.options.toc_template)
    
    def add_chapter(self, title: str, content: Union[str, List[str]], 
                   level: int = 1, images: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Add a chapter to the EPUB.
        
        Args:
            title: Chapter title
            content: Chapter content as HTML string or list of HTML blocks
            level: Heading level for TOC
            images: List of image data dictionaries
            
        Returns:
            Filename of the added chapter
        """
        # Generate a unique filename
        sanitized_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        sanitized_title = re.sub(r'[-\s]+', '-', sanitized_title)
        filename = f"chapter_{len(self.chapters) + 1}_{sanitized_title}.xhtml"
        
        # Create chapter
        chapter = EPUBChapter(
            title=title,
            content=content,
            filename=filename,
            level=level,
            images=images or []
        )
        
        self.chapters.append(chapter)
        
        # Add to TOC
        self.toc_items.append({
            'title': title,
            'href': filename,
            'level': level,
            'children': []
        })
        
        # Process images
        if images:
            for img_data in images:
                if 'filename' in img_data and 'data' in img_data:
                    self.images[img_data['filename']] = img_data
        
        return filename
    
    def add_section_from_document_section(self, section: DocumentSection, parent_items: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Add a document section and its subsections recursively.
        
        Args:
            section: DocumentSection to add
            parent_items: Parent TOC items for nesting (internal use)
        """
        if not section.title and not section.blocks:
            return
        
        # Convert blocks to HTML content
        content_blocks = []
        for block in section.blocks:
            if block.block_type == TextBlockType.TITLE:
                # Skip as we'll use the section title
                continue
            elif block.block_type == TextBlockType.HEADING:
                level = 'h2' if section.level <= 1 else f'h{min(section.level + 1, 6)}'
                content_blocks.append(f'<{level}>{block.text}</{level}>')
            elif block.block_type == TextBlockType.PARAGRAPH:
                content_blocks.append(f'<p>{block.text}</p>')
            elif block.block_type == TextBlockType.LIST_ITEM:
                # Check if this is the first list item
                if not content_blocks or not content_blocks[-1].startswith('<ul>') and not content_blocks[-1].startswith('<ol>'):
                    # Determine list type
                    if re.match(r'^\d+\.', block.text.strip()):
                        content_blocks.append('<ol>')
                    else:
                        content_blocks.append('<ul>')
                
                item_text = re.sub(r'^[\d\.\s•\-*◦▪○►→]+', '', block.text.strip())
                content_blocks.append(f'<li>{item_text}</li>')
                
                # Check if this is the last list item (peek ahead)
                next_is_list = False
                for i, next_block in enumerate(section.blocks[section.blocks.index(block) + 1:]):
                    if next_block.block_type == TextBlockType.LIST_ITEM:
                        next_is_list = True
                        break
                    elif next_block.block_type != TextBlockType.UNKNOWN:
                        break
                
                if not next_is_list:
                    # Close the list
                    if content_blocks[-2].startswith('<ol>'):
                        content_blocks.append('</ol>')
                    else:
                        content_blocks.append('</ul>')
            elif block.block_type == TextBlockType.CAPTION:
                content_blocks.append(f'<figcaption>{block.text}</figcaption>')
            elif block.block_type == TextBlockType.HEADER or block.block_type == TextBlockType.FOOTER:
                content_blocks.append(f'<div class="{block.block_type.value}">{block.text}</div>')
            else:
                content_blocks.append(f'<p>{block.text}</p>')
        
        # Add chapter
        if section.title or content_blocks:
            title = section.title or f"Section {len(self.chapters) + 1}"
            chapter_filename = self.add_chapter(title, content_blocks, section.level)
            
            # Keep track of TOC structure
            toc_item = {
                'title': title,
                'href': chapter_filename,
                'level': section.level,
                'children': []
            }
            
            if parent_items is not None:
                parent_items.append(toc_item)
            else:
                self.toc_items.append(toc_item)
            
            # Add subsections recursively
            for subsection in section.subsections:
                self.add_section_from_document_section(subsection, toc_item['children'])
    
    def add_content_from_extractor(self, extractor: PDFContentExtractor) -> None:
        """
        Add all content from a PDFContentExtractor.
        
        Args:
            extractor: PDFContentExtractor instance with extracted content
        """
        # Make sure content is extracted
        if not hasattr(extractor, 'document_sections') or not extractor.document_sections:
            extractor.extract_content()
        
        # Extract metadata if not already set
        metadata = extractor.get_document_metadata()
        if 'title' in metadata and not self.options.title:
            self.options.title = metadata['title']
        if 'author' in metadata and not self.options.author:
            self.options.author = metadata['author']
        if 'subject' in metadata and not self.options.subject:
            self.options.subject = metadata['subject']
        
        # Add sections
        for section in extractor.document_sections:
            self.add_section_from_document_section(section)
    
    def create_epub(self) -> epub.EpubBook:
        """
        Create an EPUB book from the added content.
        
        Returns:
            EbookLib EpubBook instance
        """
        # Create book
        book = epub.EpubBook()
        
        # Set metadata
        book.set_title(self.options.title)
        book.set_language(self.options.language)
        book.set_identifier(self.options.identifier)
        book.add_author(self.options.author)
        
        if self.options.publisher:
            book.add_metadata('DC', 'publisher', self.options.publisher)
        if self.options.description:
            book.add_metadata('DC', 'description', self.options.description)
        if self.options.subject:
            book.add_metadata('DC', 'subject', self.options.subject)
        if self.options.rights:
            book.add_metadata('DC', 'rights', self.options.rights)
        if self.options.publication_date:
            book.add_metadata('DC', 'date', self.options.publication_date)
        
        # Add direction if specified
        if self.options.page_progression_direction:
            book.add_metadata('OPF', 'spine', None, {'page-progression-direction': self.options.page_progression_direction})
        
        # Add CSS
        css = epub.EpubItem(
            uid="style_stylesheet",
            file_name="style/stylesheet.css",
            media_type="text/css",
            content=self.options.css
        )
        book.add_item(css)
        
        # Add cover if provided
        cover_html = None
        if self.options.cover_image:
            # Process cover image
            cover_image_data = None
            cover_filename = "images/cover.jpg"
            
            if isinstance(self.options.cover_image, str) and os.path.isfile(self.options.cover_image):
                with open(self.options.cover_image, 'rb') as f:
                    cover_image_data = f.read()
            elif isinstance(self.options.cover_image, bytes):
                cover_image_data = self.options.cover_image
            elif isinstance(self.options.cover_image, Path):
                with open(self.options.cover_image, 'rb') as f:
                    cover_image_data = f.read()
            
            if cover_image_data:
                # Add cover image
                cover_item = epub.EpubItem(
                    uid="cover-image",
                    file_name=cover_filename,
                    media_type="image/jpeg",
                    content=cover_image_data
                )
                book.add_item(cover_item)
                
                # Set cover in metadata
                book.set_cover(cover_filename, cover_image_data)
                
                # Create cover HTML
                cover_html = epub.EpubHtml(
                    title="Cover",
                    file_name="cover.xhtml",
                    lang=self.options.language
                )
                cover_html.content = self.cover_template.render(
                    title=self.options.title,
                    author=self.options.author,
                    cover_image=cover_filename
                )
                book.add_item(cover_html)
        
        # Add images
        for filename, image_data in self.images.items():
            if 'data' in image_data:
                item = epub.EpubItem(
                    uid=f"image_{hash(filename)}",
                    file_name=f"images/{filename}",
                    media_type=f"image/{image_data.get('ext', 'jpeg')}",
                    content=image_data['data']
                )
                book.add_item(item)
        
        # Add chapters
        epub_chapters = []
        for chapter in self.chapters:
            # Create chapter
            epub_chapter = epub.EpubHtml(
                title=chapter.title,
                file_name=chapter.filename,
                lang=self.options.language
            )
            
            # Render chapter content
            content_blocks = chapter.content if isinstance(chapter.content, list) else [chapter.content]
            epub_chapter.content = self.chapter_template.render(
                title=chapter.title,
                content_blocks=content_blocks
            )
            
            # Add chapter to book
            book.add_item(epub_chapter)
            epub_chapters.append(epub_chapter)
        
        # Create TOC page if requested
        toc_html = None
        if self.options.include_toc and self.chapters:
            toc_html = epub.EpubHtml(
                title=self.options.toc_title,
                file_name="toc.xhtml",
                lang=self.options.language
            )
            toc_html.content = self.toc_template.render(
                title=self.options.toc_title,
                toc_items=self.toc_items
            )
            book.add_item(toc_html)
        
        # Add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Build spine
        spine = []
        if cover_html:
            spine.append(cover_html)
        if toc_html:
            spine.append(toc_html)
        spine.append('nav')
        spine.extend(epub_chapters)
        book.spine = spine
        
        # Create nested TOC
        def build_toc(items):
            result = []
            for item in items:
                # Find the corresponding chapter
                chapter = next((ch for ch in epub_chapters if ch.file_name == item['href']), None)
                if chapter:
                    if item['children']:
                        # Create section with children
                        section = (
                            epub.Section(item['title']),
                            [chapter] + build_toc(item['children'])
                        )
                        result.append(section)
                    else:
                        # Add chapter directly
                        result.append(chapter)
            return result
        
        book.toc = build_toc(self.toc_items)
        
        # Store book
        self.book = book
        return book
    
    def write_epub(self, output_path: Union[str, Path]) -> None:
        """
        Write the EPUB to a file.
        
        Args:
            output_path: Path to save the EPUB file
        """
        # Create book if not already created
        if not self.book:
            self.create_epub()
        
        # Convert Path to string if needed
        if isinstance(output_path, Path):
            output_path = str(output_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Write the EPUB
        epub.write_epub(output_path, self.book, {})
        logger.info(f"EPUB written to {output_path}")
    
    def get_epub_bytes(self) -> bytes:
        """
        Get the EPUB as bytes.
        
        Returns:
            EPUB file content as bytes
        """
        # Create book if not already created
        if not self.book:
            self.create_epub()
        
        # Write to in-memory file
        buffer = io.BytesIO()
        epub.write_epub(buffer, self.book, {})
        return buffer.getvalue()