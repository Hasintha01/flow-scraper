"""
Module E: Page Structure Analyzer
Analyzes DOM structure to understand UI layout.
"""

from typing import Dict, List, Set
from bs4 import BeautifulSoup, Tag
from collections import Counter


class PageStructureAnalyzer:
    """Analyzes the HTML structure to extract page layout information."""
    
    def __init__(self):
        """Initialize the Page Structure Analyzer."""
        pass
    
    def analyze(self, soup: BeautifulSoup) -> Dict:
        """
        Analyze page structure.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary with structure information
        """
        analysis = {
            'page_info': self._extract_page_info(soup),
            'sections': self._extract_sections(soup),
            'navigation': self._extract_navigation(soup),
            'semantic_structure': self._extract_semantic_structure(soup),
            'classes': self._extract_classes(soup),
            'ids': self._extract_ids(soup),
            'component_hierarchy': self._extract_component_hierarchy(soup),
            'layout_patterns': self._detect_layout_patterns(soup)
        }
        
        return analysis
    
    def _extract_page_info(self, soup: BeautifulSoup) -> Dict:
        """Extract basic page information."""
        info = {
            'title': '',
            'meta_description': '',
            'meta_keywords': '',
            'favicon': '',
            'lang': '',
            'charset': ''
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            info['title'] = title_tag.string or ''
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            info['meta_description'] = meta_desc.get('content', '')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            info['meta_keywords'] = meta_keywords.get('content', '')
        
        # Favicon
        favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon:
            info['favicon'] = favicon.get('href', '')
        
        # Language
        html_tag = soup.find('html')
        if html_tag:
            info['lang'] = html_tag.get('lang', '')
        
        # Charset
        meta_charset = soup.find('meta', charset=True)
        if meta_charset:
            info['charset'] = meta_charset.get('charset', '')
        else:
            meta_charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
            if meta_charset:
                content = meta_charset.get('content', '')
                if 'charset=' in content:
                    info['charset'] = content.split('charset=')[-1].strip()
        
        return info
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract main page sections."""
        sections = []
        
        # Common section elements
        section_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        
        for tag_name in section_tags:
            for idx, element in enumerate(soup.find_all(tag_name)):
                section_info = {
                    'type': tag_name,
                    'index': idx,
                    'id': element.get('id', ''),
                    'classes': element.get('class', []),
                    'children_count': len(list(element.children)),
                    'text_length': len(element.get_text(strip=True))
                }
                sections.append(section_info)
        
        return sections
    
    def _extract_navigation(self, soup: BeautifulSoup) -> Dict:
        """Extract navigation structure."""
        navigation = {
            'nav_elements': [],
            'menu_items': [],
            'links': []
        }
        
        # Find navigation elements
        nav_elements = soup.find_all('nav')
        for idx, nav in enumerate(nav_elements):
            nav_info = {
                'index': idx,
                'id': nav.get('id', ''),
                'classes': nav.get('class', []),
                'links_count': len(nav.find_all('a'))
            }
            navigation['nav_elements'].append(nav_info)
            
            # Extract menu items
            links = nav.find_all('a')
            for link in links:
                navigation['menu_items'].append({
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'classes': link.get('class', [])
                })
        
        # Get all links on the page
        all_links = soup.find_all('a', href=True)
        navigation['total_links'] = len(all_links)
        
        # Categorize links
        internal_links = []
        external_links = []
        anchor_links = []
        
        for link in all_links:
            href = link.get('href', '')
            if href.startswith('#'):
                anchor_links.append(href)
            elif href.startswith('http'):
                external_links.append(href)
            else:
                internal_links.append(href)
        
        navigation['links'] = {
            'internal': len(set(internal_links)),
            'external': len(set(external_links)),
            'anchors': len(set(anchor_links))
        }
        
        return navigation
    
    def _extract_semantic_structure(self, soup: BeautifulSoup) -> Dict:
        """Extract semantic HTML5 elements."""
        semantic_tags = [
            'header', 'nav', 'main', 'section', 'article', 'aside', 'footer',
            'figure', 'figcaption', 'time', 'mark', 'summary', 'details'
        ]
        
        structure = {}
        for tag in semantic_tags:
            elements = soup.find_all(tag)
            structure[tag] = {
                'count': len(elements),
                'ids': [el.get('id', '') for el in elements if el.get('id')],
                'classes': [el.get('class', []) for el in elements if el.get('class')]
            }
        
        return structure
    
    def _extract_classes(self, soup: BeautifulSoup) -> Dict:
        """Extract all CSS classes used in the page."""
        all_classes = []
        
        for element in soup.find_all(class_=True):
            classes = element.get('class', [])
            all_classes.extend(classes)
        
        class_counter = Counter(all_classes)
        
        return {
            'total_unique': len(set(all_classes)),
            'total_usage': len(all_classes),
            'most_common': [cls for cls, _ in class_counter.most_common(20)],
            'frequency': dict(class_counter.most_common(50))
        }
    
    def _extract_ids(self, soup: BeautifulSoup) -> Dict:
        """Extract all IDs used in the page."""
        all_ids = []
        
        for element in soup.find_all(id=True):
            element_id = element.get('id', '')
            if element_id:
                all_ids.append(element_id)
        
        return {
            'total': len(all_ids),
            'ids': all_ids
        }
    
    def _extract_component_hierarchy(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract component hierarchy (common UI patterns)."""
        components = []
        
        # Look for common component patterns
        component_patterns = {
            'hero': ['hero', 'banner', 'jumbotron'],
            'card': ['card'],
            'button': ['btn', 'button'],
            'form': ['form'],
            'modal': ['modal', 'dialog'],
            'carousel': ['carousel', 'slider', 'slideshow'],
            'accordion': ['accordion', 'collapse'],
            'tabs': ['tab', 'tabs'],
            'dropdown': ['dropdown', 'select']
        }
        
        for component_type, class_patterns in component_patterns.items():
            for pattern in class_patterns:
                elements = soup.find_all(class_=lambda x: x and any(pattern in cls.lower() for cls in x))
                if elements:
                    components.append({
                        'type': component_type,
                        'pattern': pattern,
                        'count': len(elements),
                        'classes': list(set([' '.join(el.get('class', [])) for el in elements]))
                    })
        
        return components
    
    def _detect_layout_patterns(self, soup: BeautifulSoup) -> Dict:
        """Detect common layout patterns."""
        patterns = {
            'grid_layouts': 0,
            'flex_layouts': 0,
            'containers': 0,
            'rows': 0,
            'columns': 0
        }
        
        # Look for grid/flex patterns in class names
        grid_patterns = ['grid', 'masonry']
        flex_patterns = ['flex', 'd-flex']
        container_patterns = ['container', 'wrapper']
        row_patterns = ['row']
        col_patterns = ['col', 'column']
        
        all_elements = soup.find_all(class_=True)
        
        for element in all_elements:
            classes = ' '.join(element.get('class', [])).lower()
            
            if any(p in classes for p in grid_patterns):
                patterns['grid_layouts'] += 1
            if any(p in classes for p in flex_patterns):
                patterns['flex_layouts'] += 1
            if any(p in classes for p in container_patterns):
                patterns['containers'] += 1
            if any(p in classes for p in row_patterns):
                patterns['rows'] += 1
            if any(p in classes for p in col_patterns):
                patterns['columns'] += 1
        
        return patterns
