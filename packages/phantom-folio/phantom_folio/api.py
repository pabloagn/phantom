"""
FastAPI application for Phantom Folio.

This module defines a RESTful API that allows external services to access
the PDF to EPUB conversion functionality.
"""

import os
import sys
import tempfile
import json
import logging
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Query, Depends, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import config
from .utils.health import check_api_health
from .utils.logging import setup_logging
from .converters.converter import PDFToEPUBConverter, ConversionOptions

# Set up logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Phantom Folio API",
    description="PDF to EPUB conversion API with advanced features",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for file operations
TEMP_DIR = Path(tempfile.gettempdir()) / "phantom-folio"
TEMP_DIR.mkdir(exist_ok=True)

# Pydantic models for API
class ConversionOptions(BaseModel):
    """Options for PDF to EPUB conversion."""
    title: Optional[str] = None
    author: Optional[str] = None
    language: str = "en"
    use_ocr: bool = False
    ocr_language: str = "eng"
    extract_images: bool = True
    image_quality: int = Field(85, ge=1, le=100)
    max_image_size: Optional[int] = 1200
    include_cover: bool = True
    page_progression: str = "ltr"
    min_heading_size: float = 12.0
    extract_toc: bool = True

class ConversionResponse(BaseModel):
    """Response for conversion request."""
    success: bool
    message: str
    filename: Optional[str] = None
    file_size: Optional[int] = None
    download_url: Optional[str] = None
    conversion_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    """Response for health check."""
    status: str
    version: str
    dependencies: Dict[str, Dict[str, str]]
    services: Dict[str, Dict[str, str]]

@app.get("/", tags=["General"])
async def root():
    """API root endpoint."""
    return {
        "name": "Phantom Folio API",
        "version": "1.0.0",
        "description": "PDF to EPUB conversion API with advanced features",
        "docs_url": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Check the health of the API and its dependencies."""
    return check_api_health()

@app.post("/convert", response_model=ConversionResponse, tags=["Conversion"])
async def convert_pdf_to_epub(
    background_tasks: BackgroundTasks,
    options: Optional[ConversionOptions] = None,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    author: Optional[str] = Form(None),
    language: str = Form("en"),
    use_ocr: bool = Form(False),
    extract_images: bool = Form(True),
    include_cover: bool = Form(True),
    return_file: bool = Form(True),
):
    """
    Convert a PDF file to EPUB format.
    
    The conversion options can be provided either as form fields or as a JSON object.
    The JSON object takes precedence over the form fields.
    
    Args:
        file: PDF file to convert
        options: Conversion options as JSON
        title: Document title (overrides PDF metadata)
        author: Document author (overrides PDF metadata)
        language: Document language code
        use_ocr: Whether to use OCR for scanned pages
        extract_images: Whether to extract images from the PDF
        include_cover: Whether to include a cover page
        return_file: Whether to return the EPUB file in the response
        
    Returns:
        JSON response with conversion results
    """
    import time
    start_time = time.time()
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")
    
    # Create a temporary file to store the uploaded PDF
    pdf_path = TEMP_DIR / f"upload_{file.filename}"
    epub_path = TEMP_DIR / f"{pdf_path.stem}.epub"
    
    try:
        # Save the uploaded file
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        with open(pdf_path, "wb") as f:
            f.write(content)
        
        # Merge options
        conversion_options = options.dict() if options else {}
        
        # Override with form values if provided and not in options
        if title is not None and 'title' not in conversion_options:
            conversion_options['title'] = title
        if author is not None and 'author' not in conversion_options:
            conversion_options['author'] = author
        if 'language' not in conversion_options:
            conversion_options['language'] = language
        if 'use_ocr' not in conversion_options:
            conversion_options['use_ocr'] = use_ocr
        if 'extract_images' not in conversion_options:
            conversion_options['extract_images'] = extract_images
        if 'include_cover' not in conversion_options:
            conversion_options['include_cover'] = include_cover
        
        # Create converter with options
        converter = PDFToEPUBConverter(ConversionOptions(**conversion_options))
        
        # Convert PDF to EPUB
        logger.info(f"Converting {pdf_path} to {epub_path}")
        success = converter.convert(pdf_path, epub_path)
        
        if not success:
            raise HTTPException(status_code=500, detail="Conversion failed")
        
        # Calculate conversion time
        conversion_time = time.time() - start_time
        
        # Get file size
        file_size = epub_path.stat().st_size if epub_path.exists() else None
        
        # Create response
        response_data = {
            "success": True,
            "message": "Conversion successful",
            "filename": file.filename.replace('.pdf', '.epub'),
            "file_size": file_size,
            "conversion_time": conversion_time
        }
        
        # Set up cleanup task
        def cleanup_temp_files():
            try:
                pdf_path.unlink(missing_ok=True)
                # Only clean up EPUB if we're returning it directly
                if return_file:
                    epub_path.unlink(missing_ok=True)
            except Exception as e:
                logger.error(f"Error cleaning up temporary files: {str(e)}")
        
        # If not returning file, provide download URL and keep the file
        if not return_file:
            # Generate unique download ID
            download_id = os.path.basename(epub_path)
            download_url = f"/download/{download_id}"
            response_data["download_url"] = download_url
            
            # Schedule cleanup for later
            background_tasks.add_task(lambda: cleanup_temp_files_after_delay(epub_path, 3600))  # Clean up after 1 hour
            
            return ConversionResponse(**response_data)
        else:
            # Schedule cleanup for after response is sent
            background_tasks.add_task(cleanup_temp_files)
            
            # Return file directly
            return FileResponse(
                path=epub_path,
                filename=response_data["filename"],
                media_type="application/epub+zip",
                background=background_tasks
            )
    
    except Exception as e:
        # Clean up temp files on error
        try:
            pdf_path.unlink(missing_ok=True)
            epub_path.unlink(missing_ok=True)
        except:
            pass
        
        logger.error(f"Error during conversion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

@app.get("/download/{file_id}", tags=["Conversion"])
async def download_file(file_id: str, background_tasks: BackgroundTasks):
    """
    Download a converted EPUB file.
    
    Args:
        file_id: Unique identifier for the file
        
    Returns:
        EPUB file as a downloadable response
    """
    # Security check: ensure file_id doesn't contain path traversal
    if '..' in file_id or '/' in file_id:
        raise HTTPException(status_code=400, detail="Invalid file ID")
    
    # Check if file exists
    file_path = TEMP_DIR / file_id
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Schedule cleanup for after response is sent
    def cleanup_after_download():
        try:
            file_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Error cleaning up file after download: {str(e)}")
    
    background_tasks.add_task(cleanup_after_download)
    
    # Return file
    return FileResponse(
        path=file_path,
        filename=file_id.replace('upload_', ''),
        media_type="application/epub+zip",
        background=background_tasks
    )

def cleanup_temp_files_after_delay(file_path: Path, delay_seconds: int):
    """
    Clean up temporary files after a delay.
    
    Args:
        file_path: Path to the file to clean up
        delay_seconds: Delay in seconds
    """
    import time
    try:
        time.sleep(delay_seconds)
        file_path.unlink(missing_ok=True)
        logger.debug(f"Cleaned up temporary file {file_path} after {delay_seconds} seconds")
    except Exception as e:
        logger.error(f"Error cleaning up temporary file {file_path}: {str(e)}")

def start_api(host: str = None, port: int = None):
    """
    Start the FastAPI application.
    
    Args:
        host: Hostname to bind to
        port: Port to bind to
    """
    import uvicorn
    
    # Get host and port from config if not provided
    if host is None:
        host = config.get('API_HOST', '0.0.0.0')
    if port is None:
        port = config.get('API_PORT', 8000)
    
    # Start server
    uvicorn.run(
        "phantom_folio.api:app",
        host=host,
        port=port,
        log_level=config.get('LOG_LEVEL', 'info').lower(),
        workers=config.get('API_WORKERS', 1),
        reload=config.get('DEBUG', False)
    )

if __name__ == "__main__":
    start_api()