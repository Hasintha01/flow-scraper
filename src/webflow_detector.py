"""
Module B: Webflow Detector
Verifies whether the site is built using Webflow.
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import re


class WebflowDetector:
    """Detects if a website is built with Webflow and extracts Webflow-specific information."""
    
    # Webflow-specific patterns
    WEBFLOW_CLASSES = [
        'w-container', 'w-row', 'w-col', 'w-nav', 'w-nav-menu', 'w-nav-link',
        'w-dropdown', 'w-dropdown-toggle', 'w-dropdown-list', 'w-slider',
        'w-slide', 'w-form', 'w-input', 'w-button', 'w-tab-menu', 'w-tab-link',
        'w-tab-content', 'w-tab-pane', 'w-lightbox', 'w-embed', 'w-video',
        'w-background-video', 'w-richtext', 'w-dyn-list', 'w-dyn-item',
        'w-dyn-items', 'w-condition-invisible'
    ]
    
    WEBFLOW_ATTRIBUTES = [
        'data-wf-page', 'data-wf-site', 'data-animation', 'data-w-id',
        'data-nav-menu-open', 'data-ix'
    ]
    
    WEBFLOW_CSS_PATTERNS = [
        r'webflow\.css',
        r'\.webflow\.com',
        r'normalize\.css',
        r'uploads-ssl\.webflow\.com'
    ]
    
    WEBFLOW_JS_PATTERNS = [
        r'webflow\.js',
        r'\.webflow\.com/js'
    ]
    
    def __init__(self):
        """Initialize the Webflow Detector."""
        pass
    
    def detect(self, html: str, soup: BeautifulSoup, assets: Dict[str, List[str]]) -> Dict:
        """
        Detect if the website is built with Webflow.
        
        Args:
            html: Raw HTML content
            soup: BeautifulSoup object
            assets: Dictionary of linked assets
            
        Returns:
            Dictionary with detection results
        """
        detection_signals = {
            'css_files': self._check_webflow_css(assets.get('css', [])),
            'js_files': self._check_webflow_js(assets.get('js', [])),
            'html_classes': self._check_webflow_classes(soup),
            'html_attributes': self._check_webflow_attributes(soup),
            'comments': self._check_webflow_comments(html),
            'meta_generator': self._check_meta_generator(soup)
        }
        
        # Calculate confidence score
        is_webflow, confidence = self._calculate_confidence(detection_signals)
        
        # Extract Webflow-specific data
        webflow_data = None
        if is_webflow:
            webflow_data = self._extract_webflow_data(soup, assets)
        
        return {
            'is_webflow': is_webflow,
            'confidence': confidence,
            'detection_signals': detection_signals,
            'webflow_data': webflow_data
        }
    
    def _check_webflow_css(self, css_urls: List[str]) -> Dict:
        """Check for Webflow CSS files."""
        webflow_css = []
        for url in css_urls:
            for pattern in self.WEBFLOW_CSS_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    webflow_css.append(url)
                    break
        
        return {
            'found': len(webflow_css) > 0,
            'files': webflow_css,
            'count': len(webflow_css)
        }
    
    def _check_webflow_js(self, js_urls: List[str]) -> Dict:
        """Check for Webflow JavaScript files."""
        webflow_js = []
        for url in js_urls:
            for pattern in self.WEBFLOW_JS_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    webflow_js.append(url)
                    break
        
        return {
            'found': len(webflow_js) > 0,
            'files': webflow_js,
            'count': len(webflow_js)
        }
    
    def _check_webflow_classes(self, soup: BeautifulSoup) -> Dict:
        """Check for Webflow-specific CSS classes."""
        found_classes = set()
        
        for class_name in self.WEBFLOW_CLASSES:
            elements = soup.find_all(class_=lambda x: x and class_name in x.split())
            if elements:
                found_classes.add(class_name)
        
        return {
            'found': len(found_classes) > 0,
            'classes': list(found_classes),
            'count': len(found_classes)
        }
    
    def _check_webflow_attributes(self, soup: BeautifulSoup) -> Dict:
        """Check for Webflow-specific HTML attributes."""
        found_attributes = set()
        
        for attr in self.WEBFLOW_ATTRIBUTES:
            elements = soup.find_all(attrs={attr: True})
            if elements:
                found_attributes.add(attr)
        
        return {
            'found': len(found_attributes) > 0,
            'attributes': list(found_attributes),
            'count': len(found_attributes)
        }
    
    def _check_webflow_comments(self, html: str) -> Dict:
        """Check for Webflow-specific HTML comments."""
        webflow_patterns = [
            r'Built with Webflow',
            r'Webflow',
            r'webflow\.io'
        ]
        
        found_comments = []
        for pattern in webflow_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                found_comments.append(pattern)
        
        return {
            'found': len(found_comments) > 0,
            'patterns': found_comments,
            'count': len(found_comments)
        }
    
    def _check_meta_generator(self, soup: BeautifulSoup) -> Dict:
        """Check meta generator tag for Webflow."""
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        
        is_webflow = False
        content = None
        
        if meta_generator:
            content = meta_generator.get('content', '')
            is_webflow = 'webflow' in content.lower()
        
        return {
            'found': is_webflow,
            'content': content
        }
    
    def _calculate_confidence(self, signals: Dict) -> tuple:
        """
        Calculate confidence score for Webflow detection.
        
        Args:
            signals: Detection signals dictionary
            
        Returns:
            Tuple of (is_webflow, confidence_percentage)
        """
        score = 0
        max_score = 0
        
        # Weight different signals
        weights = {
            'css_files': 30,
            'js_files': 25,
            'html_classes': 20,
            'html_attributes': 15,
            'meta_generator': 5,
            'comments': 5
        }
        
        for signal_name, weight in weights.items():
            max_score += weight
            if signal_name in signals and signals[signal_name].get('found'):
                score += weight
        
        confidence = (score / max_score) * 100 if max_score > 0 else 0
        is_webflow = confidence >= 50  # Threshold for detection
        
        return is_webflow, round(confidence, 2)
    
    def _extract_webflow_data(self, soup: BeautifulSoup, assets: Dict) -> Dict:
        """
        Extract Webflow-specific data.
        
        Args:
            soup: BeautifulSoup object
            assets: Assets dictionary
            
        Returns:
            Dictionary with Webflow-specific information
        """
        data = {
            'site_id': None,
            'page_id': None,
            'version': None,
            'components': []
        }
        
        # Extract site and page IDs
        site_id_elem = soup.find(attrs={'data-wf-site': True})
        if site_id_elem:
            data['site_id'] = site_id_elem.get('data-wf-site')
        
        page_id_elem = soup.find(attrs={'data-wf-page': True})
        if page_id_elem:
            data['page_id'] = page_id_elem.get('data-wf-page')
        
        # Detect Webflow components
        component_map = {
            'navigation': 'w-nav',
            'slider': 'w-slider',
            'tabs': 'w-tab-menu',
            'dropdown': 'w-dropdown',
            'lightbox': 'w-lightbox',
            'form': 'w-form',
            'cms': 'w-dyn-list',
            'video': 'w-video'
        }
        
        for component_name, class_name in component_map.items():
            if soup.find(class_=lambda x: x and class_name in x.split()):
                data['components'].append(component_name)
        
        # Try to extract version from webflow.js
        for js_url in assets.get('js', []):
            version_match = re.search(r'webflow[.-]?(\d+\.?\d*\.?\d*)', js_url, re.IGNORECASE)
            if version_match:
                data['version'] = version_match.group(1)
                break
        
        return data
