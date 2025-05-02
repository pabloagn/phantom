# Phantom Folio

**Phantom Folio** is a powerful document processing system designed to convert various document formats (especially PDFs) into structured, searchable EPUBs with complete metadata preservation. It excels at handling even the most challenging document types, from scanned images to complex layouts with figures, diagrams, and code.

## Features

- Universal PDF Processing: Convert any PDF (scanned or digital) to high-quality EPUB.
- Full Metadata Preservation: Extract and preserve all document metadata.
- Advanced OCR: Process scanned documents with multi-language support.
- Image & Figure Extraction: Preserve images, diagrams, and figures.
- Structure Detection: Identify chapters, sections, tables of contents.
- Code Block Recognition: Preserve code formatting in technical documents.
- Batch Processing: Process documents in bulk with parallel execution.
- Web Interface: Easy-to-use interface for uploading and managing documents.
- REST API: Programmatic access to all functions.

## Architecture

Phantom Folio consists of several components:

- Web Interface: For document management and administration.
- API Server: For programmatic access and integration.
- OCR Worker: Processes documents asynchronously.
- Database: Stores document metadata and processing status.
- Redis: Task queue and caching.

## Getting Started

### Prerequisites

- Docker and Docker Compose.
- For NixOS users: Nix package manager.

### Quick Start

1. Clone the repository:

  ```shell
  git clone https://github.com/Phantomklange/phantom-folio
  cd phantom-folio
  ```

2. Run the setup script:

```shell
# For NixOS users:
nix-shell

# For everyone:
chmod +x setup.sh
chmod +x cleanup.sh
./setup.sh
```

3. Access the web interface at <http://localhost:8080>.

### Running with Docker

```shell
docker compose up -d
```

### Running with NixOS

```shell
nix-shell
./setup.sh
```

## Project Structure

```text
phantom-folio/
├── docker/                          # Docker configuration
│   ├── ocr-worker.Dockerfile        # OCR Worker container definition
│   └── web.Dockerfile               # Web interface container definition
├── phantom_folio/                   # Main application package
│   ├── __init__.py                  # Package initialization
│   ├── __main__.py                  # Command-line entry point
│   ├── api.py                       # FastAPI application
│   ├── config.py                    # Configuration management
│   ├── worker.py                    # Celery worker configuration
│   ├── cli.py                       # Command-line interface
│   ├── converters/                  # PDF to EPUB conversion logic
│   │   ├── __init__.py
│   │   ├── base.py                  # Base converter interfaces
│   │   ├── pdf.py                   # PDF handling functionality
│   │   ├── epub.py                  # EPUB generation
│   │   └── ocr.py                   # OCR processing
│   ├── models/                      # Database models
│   │   ├── __init__.py
│   │   ├── base.py                  # Base model classes
│   │   └── document.py              # Document-related models
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   └── document.py              # Document schema definitions
│   ├── services/                    # Business logic services
│   │   ├── __init__.py
│   │   └── conversion.py            # Conversion service
│   ├── tasks/                       # Background tasks
│   │   ├── __init__.py
│   │   └── conversion.py            # Conversion tasks
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── files.py                 # File handling utilities
│   │   ├── health.py                # Health check utilities
│   │   ├── logging.py               # Logging configuration
│   │   └── text.py                  # Text processing utilities
│   └── web/                         # Web interface
│       ├── __init__.py
│       ├── app.py                   # Web app definition
│       └── templates/               # HTML templates
├── scripts/                         # Utility scripts
│   ├── download_models.py           # Script to download OCR models
│   └── benchmark.py                 # Performance benchmarking
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Test configuration
│   ├── test_api.py                  # API tests
│   ├── test_converters/             # Converter tests
│   │   ├── __init__.py
│   │   ├── test_pdf.py
│   │   └── test_epub.py
│   └── test_utils/                  # Utility tests
│       ├── __init__.py
│       └── test_files.py
├── .gitignore                       # Git ignore file
├── docker-compose.yml               # Docker Compose configuration
├── requirements.txt                 # Python dependencies
├── setup.py                         # Package installation
├── setup.sh                         # Setup script
├── cleanup.sh                       # Cleanup script
└── shell.nix                        # NixOS development environment
```
