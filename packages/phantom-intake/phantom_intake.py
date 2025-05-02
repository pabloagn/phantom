#!/usr/bin/env python3
"""
Phantom-Intake
----------------
A utility script to download files from LibGen via IPFS links with proper
error handling, logging, and terminal progress indication.
"""

from pathlib import Path

from phantom_intake.config import load_config
from phantom_intake.downloader import DownloadManager


def main() -> None:
    """Main entry point for the application."""
    # Load configuration
    config = load_config()
    
    # Initialize and run download manager
    manager = DownloadManager(config)
    manager.run()


if __name__ == "__main__":
    main()