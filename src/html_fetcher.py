"""
Module A: HTML Fetcher
Fetches the page source code from the target URL.
"""

import requests
from typing import Dict, List, Tuple, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class HTMLFetcher:
    """Fetches and parses HTML from a given URL."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the HTML Fetcher.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch(self, url: str) -> Tuple[str, BeautifulSoup, Dict[str, List[str]]]:
        """
        Fetch HTML content from URL and parse it.
        
        Args:
            url: The target URL
            
        Returns:
            Tuple of (raw_html, soup_object, linked_assets)
            
        Raises:
            requests.RequestException: If fetching fails
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Extract linked assets
            assets = self._extract_assets(soup, url)
            
            return html_content, soup, assets
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")
    
    def _extract_assets(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[str]]:
        """
        Extract all linked assets from the page.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            Dictionary with asset types and their URLs
        """
        assets = {
            'css': [],
            'js': [],
            'images': [],
            'fonts': []
        }
        
        # Extract CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                assets['css'].append(full_url)
        
        # Extract JavaScript files
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                full_url = urljoin(base_url, src)
                assets['js'].append(full_url)
        
        # Extract images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                full_url = urljoin(base_url, src)
                assets['images'].append(full_url)
        
        # Extract font files from CSS @font-face (will be done in CSS collector)
        # This is a placeholder for now
        
        return assets
    
    def fetch_asset(self, url: str) -> Optional[str]:
        """
        Fetch a specific asset (CSS, JS, etc.) from URL.
        
        Args:
            url: Asset URL
            
        Returns:
            Asset content as string, or None if fetch fails
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None
    
    def get_final_url(self, url: str) -> str:
        """
        Get the final URL after redirects.
        
        Args:
            url: Initial URL
            
        Returns:
            Final URL after following redirects
        """
        try:
            response = self.session.head(url, allow_redirects=True, timeout=self.timeout)
            return response.url
        except requests.RequestException:
            return url
