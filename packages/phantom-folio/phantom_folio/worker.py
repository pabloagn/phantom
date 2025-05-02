"""
Worker module for Phantom Folio background tasks.

This module provides the Celery worker configuration for processing
asynchronous background tasks like OCR and PDF conversion.
"""

import os
import logging
import time
from typing import Dict, Any, Optional, Union
from pathlib import Path

# Conditional imports for Celery
try:
    from celery import Celery
    from celery.signals import worker_ready, worker_shutdown
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

# Set up logging
logging.basicConfig(
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('phantom_folio.worker')

# Get Redis URL from environment or use default
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Celery if available
if CELERY_AVAILABLE:
    app = Celery('phantom_folio', broker=REDIS_URL, backend=REDIS_URL)
    
    # Configure Celery
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        worker_concurrency=int(os.environ.get('WORKER_CONCURRENCY', '2')),
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        task_time_limit=3600,  # 1 hour timeout for tasks
        task_soft_time_limit=3300,  # 55 minutes soft timeout
    )
    
    @worker_ready.connect
    def on_worker_ready(**kwargs):
        """Log when the worker is ready."""
        logger.info("Phantom Folio OCR Worker is ready and waiting for tasks")
    
    @worker_shutdown.connect
    def on_worker_shutdown(**kwargs):
        """Log when the worker is shutting down."""
        logger.info("Phantom Folio OCR Worker is shutting down")
    
    @app.task(bind=True, name='phantom_folio.tasks.convert_pdf_to_epub')
    def convert_pdf_to_epub(
        self,
        pdf_path: str,
        output_path: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Convert a PDF file to EPUB format.
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Path where the EPUB will be saved (if None, uses the same name with .epub extension)
            options: Dictionary of conversion options
            
        Returns:
            Dictionary with conversion results
        """
        logger.info(f"Starting conversion of {pdf_path} to EPUB")
        
        # This is a placeholder for the actual implementation
        # We'll implement the real conversion logic soon
        
        if output_path is None:
            output_path = str(Path(pdf_path).with_suffix('.epub'))
        
        if options is None:
            options = {}
        
        # Simulate processing time (remove in the real implementation)
        time.sleep(2)
        
        result = {
            'success': True,
            'input_path': pdf_path,
            'output_path': output_path,
            'options': options,
            'message': 'Conversion completed successfully'
        }
        
        logger.info(f"Completed conversion: {pdf_path} -> {output_path}")
        return result
    
    @app.task(bind=True, name='phantom_folio.tasks.ocr_pdf')
    def ocr_pdf(
        self,
        pdf_path: str,
        output_path: Optional[str] = None,
        languages: str = 'eng',
        dpi: int = 300
    ) -> Dict[str, Any]:
        """
        Perform OCR on a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Path where the OCR'd PDF will be saved (if None, uses the original path)
            languages: Comma-separated list of language codes for OCR
            dpi: DPI for image extraction
            
        Returns:
            Dictionary with OCR results
        """
        logger.info(f"Starting OCR of {pdf_path} with languages: {languages}")
        
        # This is a placeholder for the actual implementation
        # We'll implement the real OCR logic soon
        
        if output_path is None:
            output_path = pdf_path.replace('.pdf', '_ocr.pdf')
        
        # Simulate processing time (remove in the real implementation)
        time.sleep(5)
        
        result = {
            'success': True,
            'input_path': pdf_path,
            'output_path': output_path,
            'languages': languages,
            'dpi': dpi,
            'message': 'OCR completed successfully'
        }
        
        logger.info(f"Completed OCR: {pdf_path} -> {output_path}")
        return result

else:
    # Fallback for when Celery is not available
    logger.warning("Celery is not available. Running in standalone mode without task queue.")
    
    # Define dummy task functions for API compatibility
    def convert_pdf_to_epub(
        pdf_path: str,
        output_path: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Dummy implementation when Celery is not available."""
        logger.warning("Called convert_pdf_to_epub without Celery support")
        return {
            'success': False,
            'error': 'Celery is not available'
        }
    
    def ocr_pdf(
        pdf_path: str,
        output_path: Optional[str] = None,
        languages: str = 'eng',
        dpi: int = 300
    ) -> Dict[str, Any]:
        """Dummy implementation when Celery is not available."""
        logger.warning("Called ocr_pdf without Celery support")
        return {
            'success': False,
            'error': 'Celery is not available'
        }

if __name__ == "__main__":
    if CELERY_AVAILABLE:
        logger.info("Starting Celery worker...")
        app.worker_main(['worker', '--loglevel=info'])
    else:
        logger.info("Phantom Folio worker starting in standalone mode...")
        
        # Keep the worker running in standalone mode
        try:
            while True:
                logger.info("Worker heartbeat")
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Worker shutting down")