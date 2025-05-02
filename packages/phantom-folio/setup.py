"""
Setup script for the Phantom Folio package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version from package __init__.py
about = {}
with open(os.path.join(this_directory, 'phantom_folio', '__init__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name="phantom-folio",
    version=about['__version__'],
    author=about['__author__'],
    author_email="support@phantomfolio.com",
    description="Convert PDF documents to EPUB with advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phantom-folio",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics :: Conversion",
    ],
    python_requires=">=3.9",
    install_requires=[
        'fastapi>=0.95.0',
        'uvicorn>=0.22.0',
        'celery>=5.3.0',
        'pydantic>=2.0.0',
        'sqlalchemy>=2.0.0',
        'pypdf>=3.15.0',
        'pdfminer.six>=20221105',
        'pdf2image>=1.16.3',
        'PyMuPDF>=1.22.5',
        'pytesseract>=0.3.10',
        'ebooklib>=0.18.0',
        'pillow>=9.5.0',
        'python-multipart>=0.0.6',
    ],
    entry_points={
        'console_scripts': [
            'phantom-folio=phantom_folio.__main__:main',
        ],
    },
)