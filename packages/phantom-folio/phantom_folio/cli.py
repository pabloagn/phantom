"""
Command-line interface for Phantom Folio.

This module provides the command-line interface for the PDF to EPUB conversion
functionality, allowing users to interact with the application from the terminal.
"""

import os
import sys
import time
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import datetime

from .config import config
from .utils.logging import setup_logging
from .converters.converter import PDFToEPUBConverter, ConversionOptions

# Set up logging
logger = logging.getLogger(__name__)

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

def print_color(text: str, color: str = RESET, end: str = "\n") -> None:
    """Print colored text."""
    print(f"{color}{text}{RESET}", end=end)

def print_header() -> None:
    """Print application header."""
    print_color("\n┌───────────────────────────────────────┐", BLUE)
    print_color("│          PHANTOM FOLIO                │", BLUE)
    print_color("│   Advanced PDF to EPUB Converter      │", BLUE)
    print_color("└───────────────────────────────────────┘\n", BLUE)

def spinner(message: str, seconds: float) -> None:
    """Display a spinner with a message for the specified duration."""
    chars = "|/-\\"
    start_time = time.time()
    i = 0
    
    try:
        print(f"{message} ", end="", flush=True)
        
        while time.time() - start_time < seconds:
            print(f"\r{message} {chars[i % len(chars)]}", end="", flush=True)
            i += 1
            time.sleep(0.1)
        
        print(f"\r{message} ✓", flush=True)
        
    except KeyboardInterrupt:
        print(f"\r{message} ✗", flush=True)
        raise

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Phantom Folio: Advanced PDF to EPUB Converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input and output arguments
    parser.add_argument("input", nargs="?", help="Path to input PDF file or directory")
    parser.add_argument("-o", "--output", help="Path to output EPUB file or directory")
    parser.add_argument("-b", "--batch", action="store_true", help="Process all PDFs in input directory")
    
    # Metadata options
    metadata_group = parser.add_argument_group("Metadata Options")
    metadata_group.add_argument("--title", help="EPUB title (overrides PDF metadata)")
    metadata_group.add_argument("--author", help="EPUB author (overrides PDF metadata)")
    metadata_group.add_argument("--language", default="en", help="EPUB language code")
    metadata_group.add_argument("--publisher", help="Publisher name")
    metadata_group.add_argument("--rights", help="Copyright information")
    
    # Conversion options
    conversion_group = parser.add_argument_group("Conversion Options")
    conversion_group.add_argument("--ocr", action="store_true", help="Use OCR for scanned pages")
    conversion_group.add_argument("--ocr-language", default="eng", help="OCR language code (e.g., eng, deu, fra)")
    conversion_group.add_argument("--no-images", dest="extract_images", action="store_false", help="Skip image extraction")
    conversion_group.add_argument("--image-quality", type=int, default=85, help="JPEG quality for images (0-100)")
    conversion_group.add_argument("--max-image-size", type=int, default=1200, help="Maximum image dimension in pixels")
    conversion_group.add_argument("--no-cover", dest="include_cover", action="store_false", help="Skip cover page generation")
    conversion_group.add_argument("--rtl", dest="page_progression", action="store_const", const="rtl", default="ltr", help="Right-to-left reading direction")
    conversion_group.add_argument("--min-heading-size", type=float, default=12.0, help="Minimum font size to consider as heading")
    conversion_group.add_argument("--css", help="Path to custom CSS file")
    
    # Advanced options
    advanced_group = parser.add_argument_group("Advanced Options")
    advanced_group.add_argument("--no-toc", dest="extract_toc", action="store_false", help="Skip table of contents extraction")
    advanced_group.add_argument("--config", help="Path to configuration file")
    advanced_group.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    advanced_group.add_argument("--quiet", "-q", action="store_true", help="Suppress all output except errors")
    advanced_group.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Actions
    action_group = parser.add_argument_group("Actions")
    action_group.add_argument("--list-options", action="store_true", help="List all available options")
    action_group.add_argument("--version", action="store_true", help="Show version information")
    
    return parser.parse_args()

def list_options() -> None:
    """List all available conversion options."""
    options = ConversionOptions()
    options_dict = vars(options)
    
    print_header()
    print_color("Available conversion options:", BOLD)
    print()
    
    for name, value in options_dict.items():
        print_color(f"  {name}:", BOLD)
        print(f"    Default value: {value}")
        print(f"    Type: {type(value).__name__}")
        print()
    
    print_color("Use --help for more information on how to use these options.", YELLOW)

def show_version() -> None:
    """Show version information."""
    from . import __version__, __author__
    
    print_header()
    print_color(f"Version: {__version__}", BOLD)
    print(f"Author: {__author__}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    
    # Check core dependencies
    dependencies = [
        ("PyMuPDF", "fitz"),
        ("EbookLib", "ebooklib"),
        ("Pillow", "PIL"),
        ("Tesseract", "pytesseract")
    ]
    
    print()
    print_color("Dependencies:", BOLD)
    
    for name, module_name in dependencies:
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "unknown")
            print_color(f"  {name}: ", BOLD, end="")
            print(f"{version}")
        except ImportError:
            print_color(f"  {name}: ", BOLD, end="")
            print_color("Not installed", RED)

def convert_file(input_path: Path, output_path: Path, options: ConversionOptions) -> bool:
    """
    Convert a single PDF file to EPUB.
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to output EPUB file
        options: Conversion options
        
    Returns:
        True if conversion was successful, False otherwise
    """
    try:
        # Create converter
        converter = PDFToEPUBConverter(options)
        
        # Show progress
        print_color(f"Converting: ", BOLD, end="")
        print(f"{input_path}")
        print_color(f"Output: ", BOLD, end="")
        print(f"{output_path}")
        print()
        
        # Start conversion
        start_time = time.time()
        success = converter.convert(input_path, output_path)
        elapsed_time = time.time() - start_time
        
        if success:
            print_color(f"✓ Conversion successful ", GREEN, end="")
            print(f"({elapsed_time:.2f} seconds)")
            
            # Show file size
            if output_path.exists():
                size_kb = output_path.stat().st_size / 1024
                size_mb = size_kb / 1024
                if size_mb >= 1:
                    print(f"  Output file size: {size_mb:.2f} MB")
                else:
                    print(f"  Output file size: {size_kb:.2f} KB")
            
            return True
        else:
            print_color(f"✗ Conversion failed ", RED, end="")
            print(f"({elapsed_time:.2f} seconds)")
            return False
    except Exception as e:
        logger.error(f"Error converting {input_path}: {str(e)}")
        print_color(f"✗ Error: ", RED, end="")
        print(f"{str(e)}")
        return False

def batch_convert(input_dir: Path, output_dir: Path, options: ConversionOptions) -> Tuple[int, int]:
    """
    Convert all PDF files in a directory.
    
    Args:
        input_dir: Path to input directory
        output_dir: Path to output directory
        options: Conversion options
        
    Returns:
        Tuple of (successful conversions, total files)
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all PDF files
    pdf_files = sorted(input_dir.glob("**/*.pdf"))
    total_files = len(pdf_files)
    
    if total_files == 0:
        print_color("No PDF files found in the input directory.", YELLOW)
        return 0, 0
    
    print_color(f"Found {total_files} PDF files in {input_dir}", BOLD)
    print()
    
    # Convert each file
    successful = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        # Determine relative path from input_dir
        rel_path = pdf_path.relative_to(input_dir)
        
        # Create output path with the same structure
        epub_path = output_dir / rel_path.with_suffix(".epub")
        
        # Create parent directories if needed
        epub_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Show progress
        print_color(f"[{i}/{total_files}] ", CYAN, end="")
        
        # Convert file
        if convert_file(pdf_path, epub_path, options):
            successful += 1
        
        # Separator between files
        if i < total_files:
            print()
            print_color("─" * 40, BLUE)
            print()
    
    return successful, total_files

def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    args = parse_arguments()
    
    # Set up logging
    log_level = logging.DEBUG if args.debug else (
        logging.INFO if args.verbose else (
            logging.ERROR if args.quiet else logging.WARNING
        )
    )
    setup_logging(level=log_level)
    
    # Special actions
    if args.list_options:
        list_options()
        return 0
    
    if args.version:
        show_version()
        return 0
    
    # Load configuration if specified
    if args.config:
        from .config import configure_from_file
        configure_from_file(args.config)
    
    # Check if input is provided
    if not args.input:
        print_color("Error: No input file or directory specified.", RED)
        print("Use --help for usage information.")
        return 1
    
    # Print header
    if not args.quiet:
        print_header()
    
    # Create input and output paths
    input_path = Path(args.input).expanduser().absolute()
    
    # Check if input exists
    if not input_path.exists():
        print_color(f"Error: Input path '{input_path}' does not exist.", RED)
        return 1
    
    # Create conversion options from arguments
    options_dict = {
        "title": args.title,
        "author": args.author,
        "language": args.language,
        "extract_toc": args.extract_toc,
        "use_ocr": args.ocr,
        "ocr_language": args.ocr_language,
        "extract_images": args.extract_images,
        "image_quality": args.image_quality,
        "max_image_size": args.max_image_size,
        "include_cover": args.include_cover,
        "page_progression": args.page_progression,
        "publisher": args.publisher,
        "rights": args.rights,
        "min_heading_size": args.min_heading_size,
    }
    
    # Load custom CSS if specified
    if args.css:
        css_path = Path(args.css).expanduser().absolute()
        if css_path.exists() and css_path.is_file():
            try:
                with open(css_path, "r", encoding="utf-8") as f:
                    options_dict["css"] = f.read()
            except Exception as e:
                print_color(f"Warning: Failed to load CSS file: {str(e)}", YELLOW)
        else:
            print_color(f"Warning: CSS file '{css_path}' not found.", YELLOW)
    
    # Remove None values
    options_dict = {k: v for k, v in options_dict.items() if v is not None}
    
    # Create options
    options = ConversionOptions(**options_dict)
    
    # Check if batch mode
    if input_path.is_dir() and (args.batch or not args.output):
        # Batch conversion mode
        if args.output:
            output_path = Path(args.output).expanduser().absolute()
            if output_path.exists() and not output_path.is_dir():
                print_color(f"Error: Output path '{output_path}' exists and is not a directory.", RED)
                return 1
        else:
            # Use input directory with "_epub" suffix
            output_path = input_path.with_name(f"{input_path.name}_epub")
        
        # Perform batch conversion
        successful, total = batch_convert(input_path, output_path, options)
        
        # Show summary
        if not args.quiet:
            print()
            print_color("Batch Conversion Summary:", BOLD)
            print(f"  Input directory: {input_path}")
            print(f"  Output directory: {output_path}")
            print(f"  Total files: {total}")
            print_color(f"  Successful: {successful}", GREEN if successful == total else YELLOW)
            
            if successful < total:
                print_color(f"  Failed: {total - successful}", RED)
            
            if successful > 0:
                print()
                print_color(f"EPUB files have been saved to:", BOLD)
                print(f"  {output_path}")
        
        return 0 if successful == total else 1
    
    elif input_path.is_file():
        # Single file conversion mode
        if args.output:
            output_path = Path(args.output).expanduser().absolute()
            if output_path.is_dir():
                output_path = output_path / input_path.with_suffix(".epub").name
        else:
            output_path = input_path.with_suffix(".epub")
        
        # Perform conversion
        success = convert_file(input_path, output_path, options)
        
        return 0 if success else 1
    
    else:
        print_color(f"Error: Input path '{input_path}' is a directory. Use --batch for batch conversion.", RED)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print_color("Operation cancelled by user.", YELLOW)
        sys.exit(130)
    except Exception as e:
        print()
        print_color(f"Unexpected error: {str(e)}", RED)
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)