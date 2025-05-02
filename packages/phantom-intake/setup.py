#!/usr/bin/env python3
"""
Setup script for the LibGen Downloader package.
"""

from setuptools import setup, find_packages
import os

# Get version from the package's __init__.py file
with open(os.path.join("phantom_intake", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

setup(
    name="phantom-intake",
    version=version,
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility to download files from LibGen via IPFS links",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phantom-intake",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.1",
        "beautifulsoup4>=4.11.1",
        "rich>=12.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "phantom-intake=phantom_intake:main",
        ],
    },
)