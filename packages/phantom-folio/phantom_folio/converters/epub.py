"""
EPUB generation functionality.

This module provides the tools for creating EPUB files from
extracted PDF content, preserving formatting and images.
"""

import os
import tempfile
import uuid
from typing import Dict, List, Any, Optional, Union, BinaryIO, Tuple
from pathlib import Path
import logging
from io import BytesIO

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    raise ImportError("EbookLib is required. Install with: pip install EbookLib")

try:
    from PIL import Image
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

logger = logging.getLogger(__name__)

class EPUBGenerator:
    """Generator for EPUB books from document content."""
    
    def __init__(self, title: str, author: str, language: str = 'en', identifier: Optional[str] = None):
        """
        Initialize an EPUB generator.
        
        Args:
            title: Book title
            author: Book author
            language: Book language code (default: 'en')
            identifier: Book identifier (UUID will be generated if None)
        """
        self.book = epub.EpubBook()
        
        # Set metadata
        self.book.set_title(title)
        self.book.add_author(author)
        self.book.set_language(language)
        
        # Set identifier
        if identifier is None:
            identifier = str(uuid.uuid4())
        self.book.set_identifier(identifier)
        
        # Initialize book structure
        self.chapters = []
        self.toc = []
        self.images = []
        
        # Create basic CSS
        css_content = '''
        body {
            font-family: "Bookerly", "Georgia", serif;
            margin: 5%;
            text-align: justify;
            line-height: 1.5;
        }
        h1 {
            text-align: center;
            margin: 1em 0;
        }
        h2 {
            margin: 0.8em 0;
        }
        p {
            margin: 0.5em 0;
            text-indent: 1.5em;
        }
        .image-container {
            text-align: center;
            margin: 1em auto;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        .cover {
            text-align: center;
            page-break-after: always;
        }
        .toc {
            page-break-after: always;
        }
        '''
        
        # Add CSS to book
        css = epub.EpubItem(
            uid="style",
            file_name="style/style.css",
            media_type="text/css",
            content=css_content
        )
        self.book.add_item(css)
        self.css = css
    
    def set_cover(self, image_data: bytes, title: str = None) -> None:
        """
        Set the book cover.
        
        Args:
            image_data: Cover image data
            title: Cover title (book title is used if None)
        """
        if title is None:
            title = self.book.title
        
        # Add cover image
        cover_image = epub.EpubItem(
            uid="cover-image",
            file_name="images/cover.jpg",
            media_type="image/jpeg",
            content=image_data
        )
        self.book.add_item(cover_image)
        
        # Set cover
        self.book.set_cover("images/cover.jpg", image_data)
        
        # Create cover page
        cover_content = f'''
        <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" href="style/style.css" type="text/css" />
        </head>
        <body>
            <div class="cover">
                <h1>{title}</h1>
                <img src="images/cover.jpg" alt="Cover" />
            </div>
        </body>
        </html>
        '''
        
        cover_page = epub.EpubHtml(
            title="Cover",
            file_name="cover.xhtml",
            content=cover_content
        )
        cover_page.add_item(self.css)
        self.book.add_item(cover_page)
        
        # Add to chapters list
        self.chapters.insert(0, cover_page)
    
    def add_page(self, page_number: int, title: str, content: str, images: List[Dict[str, Any]]) -> None:
        """
        Add a page to the EPUB.
        
        Args:
            page_number: Page number
            title: Page title
            content: Page text content
            images: List of image data dictionaries
        """
        # Create chapter for the page
        file_name = f"page_{page_number}.xhtml"
        chapter = epub.EpubHtml(title=title, file_name=file_name)
        
        # Process content
        html_content = f"<h1>{title}</h1>"
        
        # Add images
        for img_idx, img_data in enumerate(images):
            if 'image' in img_data and img_data['image']:
                # Generate image file name
                img_ext = img_data.get('ext', 'jpg')
                img_file_name = f"images/p{page_number}_img{img_idx}.{img_ext}"
                
                # Add image to book
                image_item = epub.EpubItem(
                    uid=f"img_{page_number}_{img_idx}",
                    file_name=img_file_name,
                    media_type=f"image/{img_ext}",
                    content=img_data['image']
                )
                self.book.add_item(image_item)
                self.images.append(image_item)
                
                # Add image to chapter content
                html_content += f'''
                <div class="image-container">
                    <img src="{img_file_name}" alt="Image {img_idx+1}" />
                </div>
                '''
        
        # Process text content into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if para:
                html_content += f"<p>{para}</p>"
        
        # Set chapter content
        chapter.content = html_content
        chapter.add_item(self.css)
        
        # Add chapter to book
        self.book.add_item(chapter)
        self.chapters.append(chapter)
        
        # Add to table of contents
        self.toc.append((title, file_name))
    
    def add_navigation(self) -> None:
        """Add navigation elements to the EPUB."""
        # Create table of contents
        self.book.toc = [(epub.Section(title), []) for title, _ in self.toc]
        
        # Add to spine
        self.book.spine = self.chapters
        
        # Add NCX and Nav files
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
    
    def write(self, output_path: Union[str, Path]) -> None:
        """
        Write the EPUB to a file.
        
        Args:
            output_path: Path where the EPUB will be saved
        """
        # Add navigation
        self.add_navigation()
        
        # Convert Path to string if needed
        if isinstance(output_path, Path):
            output_path = str(output_path)
        
        # Write EPUB
        epub.write_epub(output_path, self.book, {})
        logger.info(f"EPUB written to {output_path}")