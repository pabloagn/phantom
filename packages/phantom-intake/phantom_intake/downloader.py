"""
File downloading functionality for the LibGen Downloader.
"""

import time
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
from rich.theme import Theme

from phantom_intake.config import AppConfig, setup_logging
from phantom_intake.utils import FileHelpers


class BookDownloader:
    """Component for downloading books from LibGen."""
    
    def __init__(self, config: AppConfig, logger: logging.Logger):
        """
        Initialize book downloader.
        
        Args:
            config: Application configuration
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        
        # Create a session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": config.user_agent})
        
        # Set up console for rich output
        custom_theme = Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "bold red",
            "success": "bold green"
        })
        self.console = Console(theme=custom_theme)
    
    def extract_download_links(self, page_url: str) -> Tuple[List[str], str, str]:
        """
        Extract download links, title and author from a book page.
        
        Args:
            page_url: URL of the book page
            
        Returns:
            Tuple of (download_links, title, author)
        """
        try:
            self.logger.info(f"Accessing page: {page_url}")
            response = self.session.get(page_url, timeout=self.config.timeout_seconds)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('h1')
            title = title_tag.text.strip() if title_tag else "Unknown_Title"
            self.logger.info(f"Found book: {title}")
            
            # Extract author
            author = "Unknown_Author"
            author_tag = soup.find('p', text=lambda t: t and t.startswith('Author'))
            if author_tag:
                author_text = author_tag.text
                if ':' in author_text:
                    author = author_text.split(':', 1)[1].strip()
                else:
                    author = author_text.replace('Author(s)', '').strip()
            
            # Extract download links - first the direct download
            download_links = []
            
            # Look for the main GET link first (primary method)
            get_links = soup.find_all('h2')
            for h2 in get_links:
                if h2.find('a'):
                    href = h2.find('a')['href']
                    if href:
                        self.logger.info(f"Found primary download link: {href}")
                        download_links.append(href)
            
            # Then look for IPFS links (Cloudflare, IPFS.io, etc.)
            ipfs_section = None
            for div in soup.find_all('div'):
                if div.text and 'IPFS' in div.text:
                    ipfs_section = div.find_next('ul')
                    break
            
            if ipfs_section:
                for li in ipfs_section.find_all('li'):
                    if li.find('a') and li.find('a')['href']:
                        href = li.find('a')['href']
                        self.logger.info(f"Found IPFS link: {href}")
                        download_links.append(href)
            
            return download_links, title, author
            
        except Exception as e:
            self.logger.error(f"Error extracting download links: {e}")
            return [], "Unknown_Title", "Unknown_Author"
    
    def download_book(self, url: str, output_dir: Path) -> bool:
        """
        Download a book from LibGen.
        
        Args:
            url: URL of the book page
            output_dir: Directory to save the downloaded file
            
        Returns:
            True if download was successful, False otherwise
        """
        # Extract download links
        download_links, title, author = self.extract_download_links(url)
        
        if not download_links:
            self.logger.error(f"No download links found for {url}")
            return False
        
        # Try each download link
        for download_url in download_links:
            try:
                # Determine file extension from URL
                extension = "pdf"  # Default
                if "." in os.path.basename(download_url.split('?')[0]):
                    extension = os.path.basename(download_url.split('?')[0]).split('.')[-1]
                
                # Create a clean filename from title and author
                clean_filename = f"{author} - {title}.{extension}"
                clean_filename = FileHelpers.sanitize_filename(clean_filename)
                
                # Full path to save the file
                file_path = output_dir / clean_filename
                
                self.logger.info(f"Downloading from {download_url}")
                self.logger.info(f"Saving to {file_path}")
                
                # Download with progress bar
                with self.console.status(f"[info]Connecting to download server..."):
                    response = self.session.get(
                        download_url, 
                        stream=True, 
                        timeout=self.config.timeout_seconds
                    )
                    response.raise_for_status()
                
                # Get total file size
                total_size = int(response.headers.get('content-length', 0))
                
                # Create a new console for this specific progress bar
                download_console = Console()
                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=download_console
                ) as progress:
                    download_task = progress.add_task(
                        f"[cyan]Downloading {clean_filename}", 
                        total=total_size
                    )
                    
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            progress.update(download_task, advance=len(chunk))
                
                self.logger.info(f"Download completed: {clean_filename}")
                return True
                
            except Exception as e:
                self.logger.warning(f"Download failed from {download_url}: {e}")
                
        # If all download attempts failed
        self.logger.error(f"All download attempts failed for {url}")
        return False


class DownloadManager:
    """Main application class to manage the download process."""
    
    def __init__(self, config: AppConfig):
        """
        Initialize download manager.
        
        Args:
            config: Application configuration
        """
        self.config = config
        
        # Ensure directories exist
        self.config.input_dir.mkdir(parents=True, exist_ok=True)
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self.logger = setup_logging(self.config.log_dir)
        
        # Set up book downloader
        self.downloader = BookDownloader(config, self.logger)
        
        # Set up console
        self.console = self.downloader.console
    
    def run(self) -> None:
        """Run the download process for all URLs in the input file."""
        urls_file_path = self.config.input_dir / self.config.urls_file
        error_log_path = self.config.input_dir / "download_errors.txt"
        success_log_path = self.config.input_dir / "download_success.txt"
        
        # Print startup banner (simple and clean)
        self.console.print("[bold green]" + ("=" * 60))
        self.console.print("[bold green]PHANTOM INTAKE - LibGen Downloader")
        self.console.print("[bold green]" + ("=" * 60))
        
        try:
            with open(urls_file_path, 'r') as file:
                urls = file.read().splitlines()
                urls = [url.strip() for url in urls if url.strip()]
        except FileNotFoundError:
            self.logger.error(f"Input file not found: {urls_file_path}")
            self.console.print(f"[error]Error: Input file not found: {urls_file_path}")
            return
            
        if not urls:
            self.logger.warning("No URLs found in the input file")
            self.console.print("[warning]Warning: No URLs found in the input file")
            return
            
        self.console.print(f"[success]Starting download of {len(urls)} items")
        self.console.print(f"[info]Output directory: {self.config.output_dir}")
        self.console.print("")
        
        # Keep track of successes and failures
        success_count = 0
        failure_count = 0
        
        with open(error_log_path, 'a') as error_log, open(success_log_path, 'a') as success_log:
            # Process each URL
            for i, url in enumerate(urls, 1):
                self.console.print(f"[bold]Processing {i}/{len(urls)}: {url}")
                
                # Download the book
                result = self.downloader.download_book(url, self.config.output_dir)
                
                # Record result
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                if result:
                    success_count += 1
                    success_log.write(f"{timestamp} | {url}\n")
                    success_log.flush()
                    self.console.print(f"[success]Successfully downloaded book from {url}")
                else:
                    failure_count += 1
                    error_log.write(f"{timestamp} | {url}\n")
                    error_log.flush()
                    self.console.print(f"[error]Failed to download book from {url}")
                
                # Add a separator between books for clarity
                self.console.print("-" * 40)
                
                # Wait before next request to avoid rate limiting
                if i < len(urls):
                    time.sleep(self.config.delay_seconds)
        
        # Print completion banner
        self.console.print("[bold green]" + ("=" * 60))
        self.console.print(f"[success]Download process completed!")
        self.console.print(f"[info]Results: {success_count} successful, {failure_count} failed")
        self.console.print(f"[info]Files saved to: {self.config.output_dir}")
        self.console.print("[bold green]" + ("=" * 60))