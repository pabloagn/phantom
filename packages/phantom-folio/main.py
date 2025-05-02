#!/usr/bin/env python3
"""
Phantom Folio: Advanced PDF to EPUB Converter

This is the main entry point for the Phantom Folio application.
It detects whether to run the CLI, API server, or worker based on command-line arguments.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

def setup_parser() -> argparse.ArgumentParser:
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Phantom Folio: Advanced PDF to EPUB Converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Global arguments
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # CLI command
    cli_parser = subparsers.add_parser("cli", help="Run command-line interface")
    cli_parser.add_argument("input", help="Path to input PDF file or directory", nargs='?')
    cli_parser.add_argument("-o", "--output", help="Path to output EPUB file or directory")
    cli_parser.add_argument("-b", "--batch", action="store_true", help="Process all PDFs in input directory")
    cli_parser.add_argument("--title", help="EPUB title (overrides PDF metadata)")
    cli_parser.add_argument("--author", help="EPUB author (overrides PDF metadata)")
    cli_parser.add_argument("--language", default="en", help="EPUB language code")
    cli_parser.add_argument("--publisher", help="Publisher name")
    cli_parser.add_argument("--rights", help="Copyright information")
    cli_parser.add_argument("--ocr", action="store_true", help="Use OCR for scanned pages")
    cli_parser.add_argument("--ocr-language", default="eng", help="OCR language code (e.g., eng, deu, fra)")
    cli_parser.add_argument("--no-images", dest="extract_images", action="store_false", help="Skip image extraction")
    cli_parser.add_argument("--image-quality", type=int, default=85, help="JPEG quality for images (0-100)")
    cli_parser.add_argument("--max-image-size", type=int, default=1200, help="Maximum image dimension in pixels")
    cli_parser.add_argument("--no-cover", dest="include_cover", action="store_false", help="Skip cover page generation")
    cli_parser.add_argument("--rtl", dest="page_progression", action="store_const", const="rtl", default="ltr", help="Right-to-left reading direction")
    cli_parser.add_argument("--min-heading-size", type=float, default=12.0, help="Minimum font size to consider as heading")
    cli_parser.add_argument("--css", help="Path to custom CSS file")
    cli_parser.add_argument("--no-toc", dest="extract_toc", action="store_false", help="Skip table of contents extraction")
    cli_parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    cli_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress all output except errors")
    cli_parser.add_argument("--list-options", action="store_true", help="List all available options")
    cli_parser.add_argument("--version", action="store_true", help="Show version information")
    
    # API command
    api_parser = subparsers.add_parser("api", help="Run API server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    api_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    # Worker command
    worker_parser = subparsers.add_parser("worker", help="Run worker for background tasks")
    
    return parser

def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Configure debugging before imports to ensure proper logger configuration
    if args.debug:
        os.environ["DEBUG"] = "true"
        os.environ["LOG_LEVEL"] = "DEBUG"
        
    # Import modules here to avoid circular imports
    from phantom_folio.config import configure_from_file
    
    # Configure from file if specified
    if args.config:
        configure_from_file(args.config)
    
    # Determine which command to run, with a default to CLI if input is provided
    if args.command == "cli" or (args.command is None and args.input):
        from phantom_folio.cli import main as cli_main
        if args.command is None and args.input:
            # If no command is specified but input is provided, use CLI mode
            sys.argv.insert(1, "cli")  # Insert 'cli' as the first argument
        return cli_main()
    
    elif args.command == "api":
        from phantom_folio.api import start_api
        return start_api(host=args.host, port=args.port)
    
    elif args.command == "worker":
        from phantom_folio.worker import main as worker_main
        return worker_main()
    
    else:
        # No command specified and no input provided, show help
        parser.print_help()
        return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        if os.environ.get("DEBUG") == "true":
            import traceback
            traceback.print_exc()
        sys.exit(1)