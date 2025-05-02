FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    TESSDATA_PREFIX=/app/models/tessdata

# Create non-root user
RUN groupadd -r phantom && useradd -r -g phantom phantom

# Install system dependencies - adding ALL required OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libmagickwand-dev \
    ghostscript \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libpq-dev \
    build-essential \
    wget \
    curl \
    # OpenCV dependencies
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    # Add ImageMagick explicitly
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up ImageMagick policy to allow PDF processing
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-6/policy.xml

# Set up working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Second stage - for application code
FROM base AS app

# Create application directories
RUN mkdir -p /app/library /app/temp /app/models/tessdata /app/logs && \
    chown -R phantom:phantom /app

# Copy application code
COPY --chown=phantom:phantom ./phantom_folio /app/phantom_folio

# Switch to non-root user
USER phantom

# Set Python path
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "phantom_folio.api:app", "--host", "0.0.0.0", "--port", "8000"]