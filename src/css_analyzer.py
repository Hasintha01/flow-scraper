"""
Module D: CSS Analyzer
Extracts all design-related data from CSS.
"""

from typing import Dict, List, Set, Optional
import re
from collections import Counter


class CSSAnalyzer:
    """Analyzes CSS to extract design system information."""
    
    def __init__(self):
        """Initialize the CSS Analyzer."""
        pass
    
    def analyze(self, css_data: Dict) -> Dict:
        """
        Analyze CSS content to extract design information.
        
        Args:
            css_data: CSS data from CSSCollector
            
        Returns:
            Dictionary with design system data
        """
        css_content = css_data.get('combined_css', '')
        
        analysis = {
            'colors': self._extract_colors(css_content),
            'typography': self._extract_typography(css_content),
            'spacing': self._extract_spacing(css_content),
            'shadows': self._extract_shadows(css_content),
            'borders': self._extract_borders(css_content),
            'animations': self._extract_animations(css_content),
            'css_variables': self._extract_css_variables(css_content),
            'components': self._extract_components(css_content)
        }
        
        return analysis
    
    def _extract_colors(self, css: str) -> Dict:
        """Extract all color values from CSS."""
        colors = {
            'all': [],
            'hex': [],
            'rgb': [],
            'rgba': [],
            'hsl': [],
            'hsla': [],
            'named': [],
            'frequency': {},
            'primary_colors': []
        }
        
        # HEX colors
        hex_pattern = r'#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})\b'
        hex_colors = re.findall(hex_pattern, css)
        colors['hex'] = ['#' + c for c in hex_colors]
        
        # RGB colors
        rgb_pattern = r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
        rgb_colors = re.findall(rgb_pattern, css)
        colors['rgb'] = [f'rgb({r}, {g}, {b})' for r, g, b in rgb_colors]
        
        # RGBA colors
        rgba_pattern = r'rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)'
        rgba_colors = re.findall(rgba_pattern, css)
        colors['rgba'] = [f'rgba({r}, {g}, {b}, {a})' for r, g, b, a in rgba_colors]
        
        # HSL colors
        hsl_pattern = r'hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*\)'
        hsl_colors = re.findall(hsl_pattern, css)
        colors['hsl'] = [f'hsl({h}, {s}%, {l}%)' for h, s, l in hsl_colors]
        
        # HSLA colors
        hsla_pattern = r'hsla\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*,\s*([\d.]+)\s*\)'
        hsla_colors = re.findall(hsla_pattern, css)
        colors['hsla'] = [f'hsla({h}, {s}%, {l}%, {a})' for h, s, l, a in hsla_colors]
        
        # Combine all colors
        all_colors = colors['hex'] + colors['rgb'] + colors['rgba'] + colors['hsl'] + colors['hsla']
        colors['all'] = list(set(all_colors))
        
        # Calculate frequency
        color_counter = Counter(all_colors)
        colors['frequency'] = dict(color_counter.most_common())
        
        # Identify primary colors (most frequent)
        colors['primary_colors'] = [color for color, _ in color_counter.most_common(5)]
        
        return colors
    
    def _extract_typography(self, css: str) -> Dict:
        """Extract typography information from CSS."""
        typography = {
            'font_families': [],
            'font_sizes': [],
            'font_weights': [],
            'line_heights': [],
            'letter_spacing': [],
            'google_fonts': [],
            'font_imports': []
        }
        
        # Font families
        font_family_pattern = r'font-family\s*:\s*([^;]+);'
        font_families = re.findall(font_family_pattern, css, re.IGNORECASE)
        typography['font_families'] = list(set([f.strip() for f in font_families]))
        
        # Font sizes
        font_size_pattern = r'font-size\s*:\s*([^;]+);'
        font_sizes = re.findall(font_size_pattern, css, re.IGNORECASE)
        typography['font_sizes'] = sorted(list(set([s.strip() for s in font_sizes])))
        
        # Font weights
        font_weight_pattern = r'font-weight\s*:\s*([^;]+);'
        font_weights = re.findall(font_weight_pattern, css, re.IGNORECASE)
        typography['font_weights'] = sorted(list(set([w.strip() for w in font_weights])))
        
        # Line heights
        line_height_pattern = r'line-height\s*:\s*([^;]+);'
        line_heights = re.findall(line_height_pattern, css, re.IGNORECASE)
        typography['line_heights'] = sorted(list(set([l.strip() for l in line_heights])))
        
        # Letter spacing
        letter_spacing_pattern = r'letter-spacing\s*:\s*([^;]+);'
        letter_spacings = re.findall(letter_spacing_pattern, css, re.IGNORECASE)
        typography['letter_spacing'] = sorted(list(set([l.strip() for l in letter_spacings])))
        
        # Google Fonts imports
        google_fonts_pattern = r'@import\s+url\([\'"]?https?://fonts\.googleapis\.com/css[^)]+\)'
        google_fonts = re.findall(google_fonts_pattern, css)
        typography['google_fonts'] = google_fonts
        
        # All @import statements
        import_pattern = r'@import\s+[^;]+;'
        imports = re.findall(import_pattern, css)
        typography['font_imports'] = imports
        
        return typography
    
    def _extract_spacing(self, css: str) -> Dict:
        """Extract spacing (margin, padding) information."""
        spacing = {
            'margins': [],
            'paddings': [],
            'gaps': [],
            'common_spacing': []
        }
        
        # Margins
        margin_pattern = r'margin(?:-(?:top|right|bottom|left))?\s*:\s*([^;]+);'
        margins = re.findall(margin_pattern, css, re.IGNORECASE)
        spacing['margins'] = sorted(list(set([m.strip() for m in margins])))
        
        # Paddings
        padding_pattern = r'padding(?:-(?:top|right|bottom|left))?\s*:\s*([^;]+);'
        paddings = re.findall(padding_pattern, css, re.IGNORECASE)
        spacing['paddings'] = sorted(list(set([p.strip() for p in paddings])))
        
        # Gap (for flexbox/grid)
        gap_pattern = r'gap\s*:\s*([^;]+);'
        gaps = re.findall(gap_pattern, css, re.IGNORECASE)
        spacing['gaps'] = sorted(list(set([g.strip() for g in gaps])))
        
        # Identify common spacing values
        all_spacing = margins + paddings + gaps
        spacing_counter = Counter(all_spacing)
        spacing['common_spacing'] = [val for val, _ in spacing_counter.most_common(10)]
        
        return spacing
    
    def _extract_shadows(self, css: str) -> Dict:
        """Extract box-shadow values."""
        shadows = {
            'box_shadows': [],
            'text_shadows': []
        }
        
        # Box shadows
        box_shadow_pattern = r'box-shadow\s*:\s*([^;]+);'
        box_shadows = re.findall(box_shadow_pattern, css, re.IGNORECASE)
        shadows['box_shadows'] = list(set([s.strip() for s in box_shadows]))
        
        # Text shadows
        text_shadow_pattern = r'text-shadow\s*:\s*([^;]+);'
        text_shadows = re.findall(text_shadow_pattern, css, re.IGNORECASE)
        shadows['text_shadows'] = list(set([s.strip() for s in text_shadows]))
        
        return shadows
    
    def _extract_borders(self, css: str) -> Dict:
        """Extract border information."""
        borders = {
            'border_widths': [],
            'border_colors': [],
            'border_styles': [],
            'border_radius': []
        }
        
        # Border widths
        border_width_pattern = r'border(?:-(?:top|right|bottom|left))?-width\s*:\s*([^;]+);'
        widths = re.findall(border_width_pattern, css, re.IGNORECASE)
        borders['border_widths'] = sorted(list(set([w.strip() for w in widths])))
        
        # Border styles
        border_style_pattern = r'border(?:-(?:top|right|bottom|left))?-style\s*:\s*([^;]+);'
        styles = re.findall(border_style_pattern, css, re.IGNORECASE)
        borders['border_styles'] = list(set([s.strip() for s in styles]))
        
        # Border radius
        border_radius_pattern = r'border-radius\s*:\s*([^;]+);'
        radiuses = re.findall(border_radius_pattern, css, re.IGNORECASE)
        borders['border_radius'] = sorted(list(set([r.strip() for r in radiuses])))
        
        return borders
    
    def _extract_animations(self, css: str) -> Dict:
        """Extract animation and transition information."""
        animations = {
            'keyframes': [],
            'animations': [],
            'transitions': [],
            'transforms': []
        }
        
        # @keyframes
        keyframes_pattern = r'@keyframes\s+([^\s{]+)'
        keyframes = re.findall(keyframes_pattern, css, re.IGNORECASE)
        animations['keyframes'] = list(set(keyframes))
        
        # Animation properties
        animation_pattern = r'animation\s*:\s*([^;]+);'
        animation_props = re.findall(animation_pattern, css, re.IGNORECASE)
        animations['animations'] = list(set([a.strip() for a in animation_props]))
        
        # Transitions
        transition_pattern = r'transition\s*:\s*([^;]+);'
        transitions = re.findall(transition_pattern, css, re.IGNORECASE)
        animations['transitions'] = list(set([t.strip() for t in transitions]))
        
        # Transforms
        transform_pattern = r'transform\s*:\s*([^;]+);'
        transforms = re.findall(transform_pattern, css, re.IGNORECASE)
        animations['transforms'] = list(set([t.strip() for t in transforms]))
        
        return animations
    
    def _extract_css_variables(self, css: str) -> Dict:
        """Extract CSS custom properties (variables)."""
        variables = {
            'all': {},
            'colors': {},
            'fonts': {},
            'spacing': {},
            'other': {}
        }
        
        # CSS variable definitions
        var_pattern = r'--([a-zA-Z0-9-]+)\s*:\s*([^;]+);'
        var_matches = re.findall(var_pattern, css)
        
        for var_name, var_value in var_matches:
            full_name = f'--{var_name}'
            value = var_value.strip()
            variables['all'][full_name] = value
            
            # Categorize variables
            if 'color' in var_name.lower() or 'bg' in var_name.lower():
                variables['colors'][full_name] = value
            elif 'font' in var_name.lower() or 'text' in var_name.lower():
                variables['fonts'][full_name] = value
            elif any(term in var_name.lower() for term in ['margin', 'padding', 'space', 'gap']):
                variables['spacing'][full_name] = value
            else:
                variables['other'][full_name] = value
        
        return variables
    
    def _extract_components(self, css: str) -> Dict:
        """Extract common UI component styles."""
        components = {
            'buttons': [],
            'cards': [],
            'containers': [],
            'navigation': [],
            'forms': []
        }
        
        # Common component class patterns
        component_patterns = {
            'buttons': r'\.(?:btn|button)[-_a-zA-Z0-9]*\s*\{',
            'cards': r'\.(?:card)[-_a-zA-Z0-9]*\s*\{',
            'containers': r'\.(?:container|wrapper)[-_a-zA-Z0-9]*\s*\{',
            'navigation': r'\.(?:nav|menu|header)[-_a-zA-Z0-9]*\s*\{',
            'forms': r'\.(?:form|input)[-_a-zA-Z0-9]*\s*\{'
        }
        
        for component_type, pattern in component_patterns.items():
            matches = re.findall(pattern, css, re.IGNORECASE)
            components[component_type] = list(set([m.strip().rstrip('{').strip() for m in matches]))
        
        return components
