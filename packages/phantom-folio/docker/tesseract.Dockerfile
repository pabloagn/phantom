FROM ubuntu:22.04

# Prevent interactive prompts during installation
ARG DEBIAN_FRONTEND=noninteractive

# Install Tesseract OCR with all languages and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-all \
    libleptonica-dev \
    libtesseract-dev \
    poppler-utils \
    ghostscript \
    libxml2-dev \
    libxslt1-dev \
    pkg-config \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directory for custom language data
RUN mkdir -p /usr/share/tessdata

# Set working directory
WORKDIR /app

# Default command - will be overridden in docker-compose
CMD ["tail", "-f", "/dev/null"]