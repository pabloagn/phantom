#!/usr/bin/env python
"""
Phantom Folio - Main entry point

This is the main entry point for the Phantom Folio application.
It provides a command-line interface for the PDF to EPUB conversion functionality.
"""

import os
import sys
import time
import argparse
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add the parent directory to the path so we can import the phantom_folio package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phantom_folio.converters.pdf import PDFDocument
from phantom_folio.converters.epub import EPUBGenerator
from phantom_folio.utils.logging import setup_logging

# Set up logging
logger = logging.getLogger('phantom_folio')

# ANSI color codes for terminal output
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
RED = '\033[0;31m'
BOLD = '\033[1m'
NC = '\033[0m'  # No Color

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Phantom Folio - Convert PDF to EPUB with advanced features',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main arguments
    parser.add_argument('input', nargs='?', help='Input PDF file or directory')
    parser.add_argument('-o', '--output', help='Output EPUB file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    # Conversion options
    conversion_group = parser.add_argument_group('Conversion Options')
    conversion_group.add_argument('--ocr', action='store_true', help='Force OCR even if text is present')
    conversion_group.add_argument('--language', default='eng', help='OCR language (e.g., eng, deu, fra)')
    conversion_group.add_argument('--dpi', type=int, default=300, help='DPI for image extraction')
    conversion_group.add_argument('--no-images', action='store_true', help='Skip image extraction')
    conversion_group.add_argument('--no-toc', action='store_true', help='Skip table of contents generation')
    
    # Metadata options
    metadata_group = parser.add_argument_group('Metadata Options')
    metadata_group.add_argument('--title', help='EPUB title (overrides PDF metadata)')
    metadata_group.add_argument('--author', help='EPUB author (overrides PDF metadata)')
    metadata_group.add_argument('--language-code', default='en', help='EPUB language code')
    
    # Debugging options
    debug_group = parser.add_argument_group('Debugging Options')
    debug_group.add_argument('--keep-temp', action='store_true', help='Keep temporary files')
    debug_group.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Special commands
    cmd_group = parser.add_argument_group('Commands')
    cmd_group.add_argument('--version', action='store_true', help='Show version information')
    cmd_group.add_argument('--self-test', action='store_true', help='Run self-test')
    
    return parser.parse_args()

def print_header() -> None:
    """Print application header."""
    print(f"{BOLD}{BLUE}==================================={NC}")
    print(f"{BOLD}{BLUE}  Phantom Folio - PDF to EPUB     {NC}")
    print(f"{BOLD}{BLUE}  Version 1.0.0                   {NC}")
    print(f"{BOLD}{BLUE}==================================={NC}")
    print()

def show_version() -> None:
    """Display version information."""
    print_header()
    print(f"{BOLD}System Information:{NC}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  Platform: {sys.platform}")
    print()
    
    try:
        import pdf2image
        print(f"  pdf2image: {pdf2image.__version__}")
    except ImportError:
        print(f"  pdf2image: {RED}Not installed{NC}")
    
    try:
        import fitz
        print(f"  PyMuPDF: {fitz.version[0]}")
    except ImportError:
        print(f"  PyMuPDF: {RED}Not installed{NC}")
    
    try:
        import ebooklib
        print(f"  ebooklib: {ebooklib.__version__}")
    except ImportError:
        print(f"  ebooklib: {RED}Not installed{NC}")
    
    try:
        import pytesseract
        print(f"  pytesseract: {pytesseract.__version__}")
        try:
            tesseract_version = pytesseract.get_tesseract_version()
            print(f"  Tesseract: {tesseract_version}")
        except Exception:
            print(f"  Tesseract: {RED}Not available{NC}")
    except ImportError:
        print(f"  pytesseract: {RED}Not installed{NC}")
    
    print()

def run_self_test() -> bool:
    """Run basic self-tests to verify the environment."""
    print_header()
    print(f"{BOLD}Running Self-Test...{NC}")
    
    tests_passed = True
    
    # Test 1: Check required packages
    print(f"\n{BOLD}Testing required packages:{NC}")
    required_packages = [
        'fitz',          # PyMuPDF
        'pdf2image',     # PDF to Image conversion
        'PIL',           # Pillow for image processing
        'ebooklib',      # EPUB creation
        'pytesseract',   # OCR
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  {GREEN}✓{NC} {package} is available")
        except ImportError:
            print(f"  {RED}✗{NC} {package} is missing")
            tests_passed = False
    
    # Test 2: Check if Tesseract is installed
    print(f"\n{BOLD}Testing external dependencies:{NC}")
    try:
        import pytesseract
        tesseract_version = pytesseract.get_tesseract_version()
        print(f"  {GREEN}✓{NC} Tesseract OCR is available (version {tesseract_version})")
    except Exception:
        print(f"  {RED}✗{NC} Tesseract OCR is not available")
        tests_passed = False
    
    # Test 3: Check if we can create a simple EPUB
    print(f"\n{BOLD}Testing EPUB generation:{NC}")
    try:
        import ebooklib
        from ebooklib import epub
        
        # Create test EPUB
        book = epub.EpubBook()
        book.set_identifier('test123456')
        book.set_title('Test Book')
        book.set_language('en')
        book.add_author('Phantom Folio')
        
        chapter = epub.EpubHtml(title='Test Chapter', file_name='test_chapter.xhtml')
        chapter.content = '<h1>Test Chapter</h1><p>This is a test.</p>'
        book.add_item(chapter)
        
        # Add navigation
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        book.spine = ['nav', chapter]
        
        temp_file = Path('test_output.epub')
        epub.write_epub(temp_file, book)
        
        if temp_file.exists():
            print(f"  {GREEN}✓{NC} EPUB generation works correctly")
            temp_file.unlink()  # Remove test file
        else:
            print(f"  {RED}✗{NC} Failed to generate EPUB file")
            tests_passed = False
            
    except Exception as e:
        print(f"  {RED}✗{NC} EPUB generation failed: {str(e)}")
        tests_passed = False
    
    # Test 4: Check Docker environment
    print(f"\n{BOLD}Testing Docker environment:{NC}")
    try:
        import subprocess
        result = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"  {GREEN}✓{NC} Docker is running")
            
            # Check for Phantom Folio containers
            if b'phantom-folio' in result.stdout:
                print(f"  {GREEN}✓{NC} Phantom Folio containers are running")
            else:
                print(f"  {YELLOW}⚠{NC} No Phantom Folio containers found. Run setup.sh first.")
        else:
            print(f"  {YELLOW}⚠{NC} Docker is not running or not accessible")
    except Exception:
        print(f"  {YELLOW}⚠{NC} Could not check Docker environment")
    
    # Final results
    print(f"\n{BOLD}Self-Test Results:{NC}")
    if tests_passed:
        print(f"  {GREEN}✓ All critical tests passed!{NC}")
        print(f"  Your environment is ready to use Phantom Folio.")
    else:
        print(f"  {RED}✗ Some tests failed.{NC}")
        print(f"  Please resolve the issues above before using Phantom Folio.")
    
    return tests_passed

def convert_pdf_to_epub(args: argparse.Namespace) -> int:
    """
    Convert PDF to EPUB using the provided arguments.
    
    Returns:
        int: 0 for success, non-zero for failure
    """
    input_path = Path(args.input)
    
    # Check if input file exists
    if not input_path.exists():
        print(f"{RED}Error: Input file '{input_path}' not found{NC}")
        return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.epub')
    
    print(f"{BOLD}Converting:{NC} {input_path}")
    print(f"{BOLD}Output:{NC} {output_path}")
    print()
    
    # Process start time
    start_time = time.time()
    
    # Load PDF
    print(f"{YELLOW}Loading PDF...{NC}")
    try:
        pdf_doc = PDFDocument(input_path)
        page_count = pdf_doc.page_count
        print(f"  {GREEN}✓{NC} Loaded PDF with {page_count} pages")
        print(f"  Title: {pdf_doc.metadata.get('title', 'Unknown')}")
        print(f"  Author: {pdf_doc.metadata.get('author', 'Unknown')}")
    except Exception as e:
        print(f"{RED}Error loading PDF: {str(e)}{NC}")
        return 1
    
    # Extract text and images
    print(f"\n{YELLOW}Processing content...{NC}")
    try:
        # Override metadata if specified
        if args.title:
            pdf_doc.metadata['title'] = args.title
        if args.author:
            pdf_doc.metadata['author'] = args.author
        
        # Process all pages
        for i, page in enumerate(pdf_doc.pages):
            page_num = i + 1
            # Print progress every 5 pages or for first and last page
            if page_num % 5 == 0 or page_num == 1 or page_num == page_count:
                print(f"  Processing page {page_num}/{page_count}...")
        
        print(f"  {GREEN}✓{NC} Content processed successfully")
    except Exception as e:
        print(f"{RED}Error processing content: {str(e)}{NC}")
        return 1
    
    # Generate EPUB
    print(f"\n{YELLOW}Generating EPUB...{NC}")
    try:
        epub_generator = EPUBGenerator(
            title=pdf_doc.metadata.get('title', 'Untitled'),
            author=pdf_doc.metadata.get('author', 'Unknown'),
            language=args.language_code
        )
        
        # Add content from PDF
        for i, page in enumerate(pdf_doc.pages):
            epub_generator.add_page(
                page_number=i + 1,
                title=f"Page {i + 1}",
                content=page.text if hasattr(page, 'text') else "",
                images=page.images if hasattr(page, 'images') and not args.no_images else []
            )
        
        # Write EPUB file
        epub_generator.write(output_path)
        print(f"  {GREEN}✓{NC} EPUB generated successfully")
    except Exception as e:
        print(f"{RED}Error generating EPUB: {str(e)}{NC}")
        return 1
    
    # Process end time
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n{GREEN}Conversion completed successfully in {elapsed_time:.2f} seconds!{NC}")
    print(f"EPUB file saved to: {output_path}")
    
    return 0

def main() -> int:
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Set up logging based on verbosity
    log_level = logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING)
    setup_logging(level=log_level)
    
    # Handle special commands
    if args.version:
        show_version()
        return 0
    
    if args.self_test:
        success = run_self_test()
        return 0 if success else 1
    
    # Check if input is provided for conversion
    if not args.input:
        print(f"{RED}Error: No input file specified{NC}")
        print(f"Run with --help for usage information.")
        return 1
    
    # Run conversion
    return convert_pdf_to_epub(args)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation cancelled by user.{NC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {str(e)}{NC}")
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)