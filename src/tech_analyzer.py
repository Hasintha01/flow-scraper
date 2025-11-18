"""
Module F: Technology Stack Analyzer
Detects technical technologies used (Wappalyzer-like).
"""

from typing import Dict, List, Set
from bs4 import BeautifulSoup
import re


class TechnologyStackAnalyzer:
    """Detects technologies, frameworks, and libraries used on the website."""
    
    def __init__(self):
        """Initialize the Technology Stack Analyzer."""
        self.technologies = self._initialize_technology_signatures()
    
    def _initialize_technology_signatures(self) -> Dict:
        """Initialize technology detection signatures."""
        return {
            'cms': {
                'Webflow': {
                    'scripts': [r'webflow\.js', r'\.webflow\.com'],
                    'css': [r'webflow\.css', r'\.webflow\.com'],
                    'classes': ['w-container', 'w-nav', 'w-slider'],
                    'meta': [('generator', 'Webflow')]
                },
                'WordPress': {
                    'scripts': [r'wp-content', r'wp-includes'],
                    'css': [r'wp-content'],
                    'meta': [('generator', 'WordPress')]
                },
                'Wix': {
                    'scripts': [r'wix\.com', r'parastorage\.com'],
                    'meta': [('generator', 'Wix')]
                },
                'Squarespace': {
                    'scripts': [r'squarespace\.com'],
                    'meta': [('generator', 'Squarespace')]
                }
            },
            'frameworks': {
                'React': {
                    'scripts': [r'react\.js', r'react-dom'],
                    'attributes': ['data-reactroot', 'data-react-helmet']
                },
                'Vue.js': {
                    'scripts': [r'vue\.js', r'vue\.min\.js'],
                    'attributes': ['v-if', 'v-for', 'v-model']
                },
                'Angular': {
                    'scripts': [r'angular\.js', r'angular\.min\.js'],
                    'attributes': ['ng-app', 'ng-controller']
                },
                'Next.js': {
                    'scripts': [r'_next/static'],
                    'meta': [('generator', 'Next.js')]
                }
            },
            'libraries': {
                'jQuery': {
                    'scripts': [r'jquery(?:-\d+\.\d+\.\d+)?(?:\.min)?\.js']
                },
                'GSAP': {
                    'scripts': [r'gsap\.js', r'TweenMax\.js', r'greensock']
                },
                'Lodash': {
                    'scripts': [r'lodash\.js', r'lodash\.min\.js']
                },
                'Bootstrap': {
                    'css': [r'bootstrap\.css', r'bootstrap\.min\.css'],
                    'scripts': [r'bootstrap\.js', r'bootstrap\.min\.js'],
                    'classes': ['container', 'row', 'col-', 'btn-']
                },
                'Tailwind CSS': {
                    'css': [r'tailwind'],
                    'classes': ['flex', 'grid', 'px-', 'py-', 'text-', 'bg-']
                }
            },
            'analytics': {
                'Google Analytics': {
                    'scripts': [r'google-analytics\.com', r'googletagmanager\.com', r'gtag']
                },
                'Google Tag Manager': {
                    'scripts': [r'googletagmanager\.com']
                },
                'Facebook Pixel': {
                    'scripts': [r'connect\.facebook\.net']
                },
                'Hotjar': {
                    'scripts': [r'hotjar\.com']
                }
            },
            'fonts': {
                'Google Fonts': {
                    'css': [r'fonts\.googleapis\.com'],
                    'scripts': [r'fonts\.googleapis\.com']
                },
                'Adobe Fonts': {
                    'css': [r'use\.typekit\.net', r'typekit\.com']
                },
                'Font Awesome': {
                    'css': [r'font-awesome', r'fontawesome']
                }
            },
            'cdn': {
                'Cloudflare': {
                    'scripts': [r'cloudflare\.com'],
                    'css': [r'cloudflare\.com']
                },
                'jsDelivr': {
                    'scripts': [r'jsdelivr\.net'],
                    'css': [r'jsdelivr\.net']
                },
                'unpkg': {
                    'scripts': [r'unpkg\.com'],
                    'css': [r'unpkg\.com']
                }
            },
            'other': {
                'Stripe': {
                    'scripts': [r'stripe\.com']
                },
                'PayPal': {
                    'scripts': [r'paypal\.com']
                },
                'Disqus': {
                    'scripts': [r'disqus\.com']
                },
                'Calendly': {
                    'scripts': [r'calendly\.com']
                }
            }
        }
    
    def analyze(self, soup: BeautifulSoup, assets: Dict[str, List[str]]) -> Dict:
        """
        Analyze the technology stack.
        
        Args:
            soup: BeautifulSoup object
            assets: Dictionary of linked assets
            
        Returns:
            Dictionary with detected technologies
        """
        detected = {
            'cms': [],
            'frameworks': [],
            'libraries': [],
            'analytics': [],
            'fonts': [],
            'cdn': [],
            'other': [],
            'all': []
        }
        
        for category, techs in self.technologies.items():
            for tech_name, signatures in techs.items():
                if self._detect_technology(tech_name, signatures, soup, assets):
                    detected[category].append(tech_name)
                    detected['all'].append({
                        'name': tech_name,
                        'category': category
                    })
        
        # Additional hosting detection
        detected['hosting'] = self._detect_hosting(soup, assets)
        
        return detected
    
    def _detect_technology(self, name: str, signatures: Dict, soup: BeautifulSoup, 
                          assets: Dict[str, List[str]]) -> bool:
        """
        Detect if a specific technology is present.
        
        Args:
            name: Technology name
            signatures: Detection signatures
            soup: BeautifulSoup object
            assets: Assets dictionary
            
        Returns:
            True if technology is detected
        """
        # Check scripts
        if 'scripts' in signatures:
            for pattern in signatures['scripts']:
                for script_url in assets.get('js', []):
                    if re.search(pattern, script_url, re.IGNORECASE):
                        return True
                
                # Also check inline scripts
                for script in soup.find_all('script'):
                    script_content = script.string or ''
                    if re.search(pattern, script_content, re.IGNORECASE):
                        return True
        
        # Check CSS
        if 'css' in signatures:
            for pattern in signatures['css']:
                for css_url in assets.get('css', []):
                    if re.search(pattern, css_url, re.IGNORECASE):
                        return True
        
        # Check classes
        if 'classes' in signatures:
            for class_pattern in signatures['classes']:
                elements = soup.find_all(class_=lambda x: x and class_pattern in x)
                if elements:
                    return True
        
        # Check attributes
        if 'attributes' in signatures:
            for attr in signatures['attributes']:
                elements = soup.find_all(attrs={attr: True})
                if elements:
                    return True
        
        # Check meta tags
        if 'meta' in signatures:
            for meta_name, meta_pattern in signatures['meta']:
                meta_tag = soup.find('meta', attrs={'name': meta_name})
                if meta_tag:
                    content = meta_tag.get('content', '')
                    if re.search(meta_pattern, content, re.IGNORECASE):
                        return True
        
        return False
    
    def _detect_hosting(self, soup: BeautifulSoup, assets: Dict[str, List[str]]) -> Dict:
        """Detect hosting provider."""
        hosting = {
            'provider': 'Unknown',
            'confidence': 'low',
            'indicators': []
        }
        
        # Check for common hosting patterns in assets
        hosting_patterns = {
            'Webflow': [r'\.webflow\.com', r'webflow\.io'],
            'Netlify': [r'\.netlify\.app', r'netlify\.com'],
            'Vercel': [r'\.vercel\.app', r'vercel\.com'],
            'GitHub Pages': [r'\.github\.io'],
            'AWS': [r'\.amazonaws\.com', r'cloudfront\.net'],
            'Firebase': [r'firebaseapp\.com', r'firebase\.com']
        }
        
        all_urls = assets.get('css', []) + assets.get('js', []) + assets.get('images', [])
        
        for provider, patterns in hosting_patterns.items():
            for pattern in patterns:
                for url in all_urls:
                    if re.search(pattern, url, re.IGNORECASE):
                        hosting['provider'] = provider
                        hosting['confidence'] = 'high'
                        hosting['indicators'].append(url)
                        return hosting
        
        return hosting
    
    def get_technology_summary(self, detected: Dict) -> Dict:
        """
        Get a summary of detected technologies.
        
        Args:
            detected: Detected technologies dictionary
            
        Returns:
            Summary dictionary
        """
        summary = {
            'total_technologies': len(detected['all']),
            'by_category': {
                'cms': len(detected['cms']),
                'frameworks': len(detected['frameworks']),
                'libraries': len(detected['libraries']),
                'analytics': len(detected['analytics']),
                'fonts': len(detected['fonts']),
                'cdn': len(detected['cdn']),
                'other': len(detected['other'])
            },
            'main_stack': []
        }
        
        # Identify main stack
        if detected['cms']:
            summary['main_stack'].append(detected['cms'][0])
        if detected['frameworks']:
            summary['main_stack'].append(detected['frameworks'][0])
        if detected['libraries']:
            summary['main_stack'].extend(detected['libraries'][:2])
        
        return summary
