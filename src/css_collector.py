"""
Module C: CSS Collector
Gathers all CSS used on the site.
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re


class CSSCollector:
    """Collects and consolidates all CSS from a webpage."""
    
    def __init__(self, fetcher):
        """
        Initialize the CSS Collector.
        
        Args:
            fetcher: HTMLFetcher instance for downloading CSS files
        """
        self.fetcher = fetcher
    
    def collect(self, soup: BeautifulSoup, assets: Dict[str, List[str]]) -> Dict:
        """
        Collect all CSS from the page.
        
        Args:
            soup: BeautifulSoup object
            assets: Dictionary of linked assets
            
        Returns:
            Dictionary with CSS sources and combined content
        """
        css_data = {
            'external_files': [],
            'inline_styles': [],
            'style_attributes': [],
            'combined_css': '',
            'sources': []
        }
        
        # Collect external CSS files
        for css_url in assets.get('css', []):
            css_content = self.fetcher.fetch_asset(css_url)
            if css_content:
                css_data['external_files'].append({
                    'url': css_url,
                    'content': css_content,
                    'size': len(css_content)
                })
                css_data['combined_css'] += f"\n/* Source: {css_url} */\n{css_content}\n"
                css_data['sources'].append({
                    'type': 'external',
                    'source': css_url
                })
        
        # Collect inline <style> blocks
        for idx, style_tag in enumerate(soup.find_all('style')):
            style_content = style_tag.string
            if style_content:
                css_data['inline_styles'].append({
                    'index': idx,
                    'content': style_content,
                    'size': len(style_content)
                })
                css_data['combined_css'] += f"\n/* Inline Style Block {idx} */\n{style_content}\n"
                css_data['sources'].append({
                    'type': 'inline',
                    'source': f'style_block_{idx}'
                })
        
        # Collect inline style attributes
        elements_with_style = soup.find_all(style=True)
        for idx, elem in enumerate(elements_with_style):
            style_attr = elem.get('style', '')
            if style_attr:
                css_data['style_attributes'].append({
                    'index': idx,
                    'tag': elem.name,
                    'style': style_attr
                })
        
        # Extract font URLs from CSS
        css_data['font_urls'] = self._extract_font_urls(css_data['combined_css'])
        
        return css_data
    
    def _extract_font_urls(self, css_content: str) -> List[str]:
        """
        Extract font URLs from @font-face declarations.
        
        Args:
            css_content: Combined CSS content
            
        Returns:
            List of font URLs
        """
        font_urls = []
        
        # Pattern to match @font-face rules
        font_face_pattern = r'@font-face\s*\{([^}]+)\}'
        font_faces = re.findall(font_face_pattern, css_content, re.DOTALL)
        
        for font_face in font_faces:
            # Extract URLs from src property
            url_pattern = r'url\([\'"]?([^\'")\s]+)[\'"]?\)'
            urls = re.findall(url_pattern, font_face)
            font_urls.extend(urls)
        
        return list(set(font_urls))  # Remove duplicates
    
    def get_css_statistics(self, css_data: Dict) -> Dict:
        """
        Get statistics about the collected CSS.
        
        Args:
            css_data: CSS data dictionary
            
        Returns:
            Dictionary with CSS statistics
        """
        total_size = len(css_data['combined_css'])
        
        stats = {
            'total_size': total_size,
            'total_size_kb': round(total_size / 1024, 2),
            'external_files_count': len(css_data['external_files']),
            'inline_blocks_count': len(css_data['inline_styles']),
            'inline_attributes_count': len(css_data['style_attributes']),
            'font_urls_count': len(css_data.get('font_urls', [])),
            'sources_breakdown': {}
        }
        
        # Calculate size breakdown by source
        for source_file in css_data['external_files']:
            stats['sources_breakdown'][source_file['url']] = {
                'size': source_file['size'],
                'size_kb': round(source_file['size'] / 1024, 2)
            }
        
        return stats
