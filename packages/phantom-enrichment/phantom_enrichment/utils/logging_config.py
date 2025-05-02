# phantom_enrichment/utils/logging_config.py

import sys
from loguru import logger
from phantom_enrichment.config.settings import settings

# Flag to prevent duplicate setup if this module is imported multiple times
_logging_configured = False

def setup_logging():
    """Configures the Loguru logger with console and file sinks."""
    global _logging_configured
    if _logging_configured:
        # logger.trace("Logging already configured.") # Optional: trace log for debugging
        return

    # Ensure settings are loaded (should happen on import of config.settings)
    try:
        log_level = settings.log_level.upper()
        log_file = settings.log_file_path # Access the property
    except Exception as e:
        # Fallback if settings somehow failed before logging setup
        print(f"ERROR accessing settings during logging setup: {e}. Using fallback defaults.")
        log_level = "INFO"
        log_file = Path("./logs/phantom_enrichment_fallback.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)


    logger.remove() # Remove default handler to avoid duplicates

    # Console Sink
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        ),
        colorize=True,
    )

    # File Sink - ADDED
    logger.add(
        log_file, # Use path from settings
        level=log_level, # Log level for the file
        rotation="10 MB", # Rotate log file when it reaches 10 MB
        retention="7 days", # Keep logs for 7 days
        compression="zip", # Compress rotated files
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}", # Detailed format
        encoding="utf-8", # Explicitly set encoding
        enqueue=True, # Make logging asynchronous for better performance
        backtrace=True, # Log full tracebacks on exceptions
        diagnose=True, # Add extended diagnostic info on exceptions
    )

    _logging_configured = True
    logger.info(f"Logging configured. Level: {log_level}. Outputting to console and file: {log_file}")

# --- Configure logging when the module is first imported ---
# This ensures it runs once when the application starts or settings are imported.
try:
   setup_logging()
except Exception as e:
    # Catch errors during setup itself
    print(f"CRITICAL ERROR during logging setup: {e}")
    # Optionally, try a basic print logger as a last resort
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.critical(f"Logging setup failed: {e}")