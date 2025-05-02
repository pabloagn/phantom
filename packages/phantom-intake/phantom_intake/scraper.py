"""
Web scraping functionality for the LibGen Downloader.
"""

import time
import logging
import random
from typing import List, Tuple, Optional

import requests
from bs4 import BeautifulSoup

from phantom_intake.utils import FileHelpers
from phantom_intake.config import AppConfig


class LibgenScraper:
    """Component for scraping LibGen pages."""
    
    def __init__(
        self, 
        session: requests.Session, 
        config: AppConfig,
        logger: logging.Logger
    ):
        """
        Initialize LibGen scraper.
        
        Args:
            session: Requests session for making HTTP requests
            config: Application configuration
            logger: Logger instance
        """
        self.session = session
        self.config = config
        self.logger = logger
        
        # Configure the session with user agent
        self.session.headers.update({"User-Agent": config.user_agent})
    
    def extract_ipfs_links_and_title(self, page_url: str) -> Tuple[List[str], str]:
        """
        Extract IPFS links and book title with format from a LibGen page.
        
        Args:
            page_url: The LibGen URL to extract information from
            
        Returns:
            A tuple containing a list of IPFS links and the title with format
        """
        # Try each configured domain if the URL doesn't contain a domain
        urls_to_try = [page_url]
        if not any(domain in page_url for domain in self.config.libgen_domains):
            # This means we have a relative URL or a URL that doesn't contain the domain
            # Extract the path part
            path = page_url
            if "://" in page_url:
                path = page_url.split("://", 1)[1]
                if "/" in path:
                    path = "/" + path.split("/", 1)[1]
            
            # Add all configured domains
            urls_to_try = [f"https://{domain}{path}" for domain in self.config.libgen_domains]
            self.logger.info(f"Will try multiple domains: {urls_to_try}")
        
        # Try each URL
        for url in urls_to_try:
            result = self._try_extract_from_url(url)
            if result[0]:  # If we found IPFS links
                return result
                
        # If all fails, return empty results
        self.logger.error(f"Failed to extract IPFS links from any URL variant of {page_url}")
        return [], "Unknown_Title.pdf"
    
    def _try_extract_from_url(self, url: str) -> Tuple[List[str], str]:
        """
        Try to extract IPFS links and title from a specific URL.
        
        Args:
            url: The URL to extract from
            
        Returns:
            A tuple containing a list of IPFS links and the title with format
        """
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.get(url, timeout=self.config.timeout_seconds)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract IPFS links
                ipfs_links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if 'ipfs' in href:
                        ipfs_links.append(href)
                    elif self.config.use_ipfs_gateway and '/ipfs/' in href:
                        # Extract IPFS hash if it's a relative path
                        ipfs_hash = href.split('/ipfs/', 1)[1].split('/', 1)[0]
                        if ipfs_hash:
                            for gateway_url in self.config.ipfs_gateway_urls:
                                ipfs_links.append(f"{gateway_url}{ipfs_hash}")
                
                # Extract title
                title_tag = soup.find('h1')
                if not title_tag:
                    title_tag = soup.find('title')
                title = title_tag.text.strip() if title_tag else 'Unknown_Title'
                
                # Extract format
                format_tag = soup.find(lambda tag: tag.name == "p" and "Format:" in tag.text)
                if not format_tag:
                    # Try alternative format detection methods
                    format_tag = soup.find(lambda tag: tag.name == "td" and "Format" in tag.text)
                
                book_format = 'pdf'  # Default format
                if format_tag:
                    format_text = format_tag.text
                    if "Format:" in format_text:
                        book_format = format_text.split("Format:")[-1].strip()
                    elif ":" in format_text:
                        book_format = format_text.split(":", 1)[1].strip()
                
                # Sanitize filename
                title = FileHelpers.sanitize_filename(title)
                title_with_format = f"{title}.{book_format}"
                
                return ipfs_links, title_with_format
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt+1}/{self.config.max_retries} failed for {url}: {e}")
                if attempt < self.config.max_retries - 1:
                    # Wait with exponential backoff
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    self.logger.info(f"Waiting {wait_time:.2f} seconds before retry")
                    time.sleep(wait_time)
                
        self.logger.error(f"Failed to access {url} after {self.config.max_retries} attempts")
        return [], 'Unknown_Title.pdf'