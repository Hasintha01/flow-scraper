"""
Report Generator
Generates reports in various formats (JSON, HTML, Markdown).
"""

import json
from typing import Dict
from datetime import datetime
import os


class ReportGenerator:
    """Generates reports from analysis data."""
    
    def __init__(self):
        """Initialize the Report Generator."""
        pass
    
    def generate(self, data: Dict, format: str = 'json', output_file: str = None) -> str:
        """
        Generate a report in the specified format.
        
        Args:
            data: Analysis data dictionary
            format: Output format ('json', 'html', 'markdown')
            output_file: Optional output file path
            
        Returns:
            Report content as string
        """
        if format == 'json':
            report = self._generate_json(data)
        elif format == 'html':
            report = self._generate_html(data)
        elif format == 'markdown':
            report = self._generate_markdown(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_file:
            self._save_report(report, output_file)
        
        return report
    
    def _generate_json(self, data: Dict) -> str:
        """Generate JSON report."""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _generate_html(self, data: Dict) -> str:
        """Generate HTML report."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Analysis Report - {data['general_info']['url']}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        
        h3 {{
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .info-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }}
        
        .info-card strong {{
            display: block;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            background: #3498db;
            color: white;
            border-radius: 3px;
            font-size: 12px;
            margin: 2px;
        }}
        
        .badge.success {{
            background: #27ae60;
        }}
        
        .badge.warning {{
            background: #f39c12;
        }}
        
        .color-swatch {{
            display: inline-block;
            width: 40px;
            height: 40px;
            border-radius: 4px;
            border: 1px solid #ddd;
            margin: 5px;
            vertical-align: middle;
        }}
        
        .color-label {{
            display: inline-block;
            margin-left: 10px;
            vertical-align: middle;
            font-family: monospace;
        }}
        
        ul {{
            margin-left: 20px;
            margin-top: 10px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: 600;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-palette"></i> Website Analysis Report</h1>
        
        {self._html_general_info(data['general_info'])}
        {self._html_webflow_detection(data['webflow_detection'])}
        {self._html_design_system(data['design_system'])}
        {self._html_tech_stack(data['tech_stack'])}
        {self._html_structure(data['structure'])}
        {self._html_assets(data['assets_summary'])}
        
        <div class="footer">
            <p>Generated on {data['metadata']['timestamp']}</p>
            <p>Webflow Design Scraper v{data['metadata']['version']}</p>
        </div>
    </div>
</body>
</html>"""
        return html
    
    def _html_general_info(self, info: Dict) -> str:
        """Generate HTML for general information section."""
        webflow_badge = '<span class="badge success"><i class="fas fa-check"></i> Webflow Site</span>' if info.get('is_webflow') else '<span class="badge">Not Webflow</span>'
        
        return f"""
        <div class="section">
            <h2><i class="fas fa-file-alt"></i> General Information</h2>
            <div class="info-grid">
                <div class="info-card">
                    <strong>URL</strong>
                    <a href="{info['url']}" target="_blank">{info['url']}</a>
                </div>
                <div class="info-card">
                    <strong>Title</strong>
                    {info.get('title', 'N/A')}
                </div>
                <div class="info-card">
                    <strong>Platform</strong>
                    {webflow_badge}
                </div>
                <div class="info-card">
                    <strong>Language</strong>
                    {info.get('lang', 'N/A')}
                </div>
            </div>
            <p><strong>Description:</strong> {info.get('meta_description', 'N/A')}</p>
        </div>
        """
    
    def _html_webflow_detection(self, detection: Dict) -> str:
        """Generate HTML for Webflow detection section."""
        if not detection['is_webflow']:
            return ""
        
        components_html = ' '.join([f'<span class="badge">{comp}</span>' for comp in detection['webflow_data'].get('components', [])])
        
        return f"""
        <div class="section">
            <h2><i class="fas fa-bullseye"></i> Webflow Detection</h2>
            <div class="info-grid">
                <div class="info-card">
                    <strong>Confidence</strong>
                    {detection['confidence']}%
                </div>
                <div class="info-card">
                    <strong>Site ID</strong>
                    {detection['webflow_data'].get('site_id', 'N/A')}
                </div>
                <div class="info-card">
                    <strong>Version</strong>
                    {detection['webflow_data'].get('version', 'N/A')}
                </div>
            </div>
            <h3>Detected Components</h3>
            <p>{components_html if components_html else 'None detected'}</p>
        </div>
        """
    
    def _html_design_system(self, design: Dict) -> str:
        """Generate HTML for design system section."""
        colors_html = ""
        primary_colors = design['colors'].get('primary_colors', [])[:10]
        for color in primary_colors:
            colors_html += f'<div><span class="color-swatch" style="background-color: {color};"></span><span class="color-label">{color}</span></div>'
        
        fonts_html = ', '.join(design['typography'].get('font_families', [])[:5])
        
        return f"""
        <div class="section">
            <h2><i class="fas fa-palette"></i> Design System</h2>
            
            <h3>Primary Colors</h3>
            <div style="margin: 15px 0;">
                {colors_html if colors_html else '<p>No colors detected</p>'}
            </div>
            
            <h3>Typography</h3>
            <div class="info-grid">
                <div class="info-card">
                    <strong>Font Families</strong>
                    {fonts_html if fonts_html else 'None detected'}
                </div>
                <div class="info-card">
                    <strong>Total Font Sizes</strong>
                    {len(design['typography'].get('font_sizes', []))}
                </div>
                <div class="info-card">
                    <strong>Total Colors</strong>
                    {len(design['colors'].get('all', []))}
                </div>
            </div>
            
            <h3>CSS Variables</h3>
            <p>Found {len(design['css_variables'].get('all', {}))} CSS custom properties</p>
        </div>
        """
    
    def _html_tech_stack(self, tech: Dict) -> str:
        """Generate HTML for tech stack section."""
        all_techs = tech.get('all', [])
        techs_by_category = {}
        
        for item in all_techs:
            category = item['category']
            if category not in techs_by_category:
                techs_by_category[category] = []
            techs_by_category[category].append(item['name'])
        
        tech_html = ""
        for category, techs in techs_by_category.items():
            badges = ' '.join([f'<span class="badge">{t}</span>' for t in techs])
            tech_html += f"<h3>{category.title()}</h3><p>{badges}</p>"
        
        return f"""
        <div class="section">
            <h2><i class="fas fa-cogs"></i> Technology Stack</h2>
            <p><strong>Total Technologies Detected:</strong> {tech['summary']['total_technologies']}</p>
            {tech_html}
            <h3>Hosting</h3>
            <p><span class="badge">{tech['hosting']['provider']}</span> (Confidence: {tech['hosting']['confidence']})</p>
        </div>
        """
    
    def _html_structure(self, structure: Dict) -> str:
        """Generate HTML for structure section."""
        sections_count = len(structure.get('sections', []))
        classes_count = structure['classes'].get('total_unique', 0)
        
        return f"""
        <div class="section">
            <h2><i class="fas fa-building"></i> Page Structure</h2>
            <div class="info-grid">
                <div class="info-card">
                    <strong>Total Sections</strong>
                    {sections_count}
                </div>
                <div class="info-card">
                    <strong>Unique CSS Classes</strong>
                    {classes_count}
                </div>
                <div class="info-card">
                    <strong>Total Links</strong>
                    {structure['navigation'].get('total_links', 0)}
                </div>
                <div class="info-card">
                    <strong>Grid Layouts</strong>
                    {structure['layout_patterns'].get('grid_layouts', 0)}
                </div>
            </div>
        </div>
        """
    
    def _html_assets(self, assets: Dict) -> str:
        """Generate HTML for assets section."""
        return f"""
        <div class="section">
            <h2><i class="fas fa-box"></i> Assets Summary</h2>
            <div class="info-grid">
                <div class="info-card">
                    <strong>CSS Files</strong>
                    {assets.get('css_files_count', 0)}
                </div>
                <div class="info-card">
                    <strong>JavaScript Files</strong>
                    {assets.get('js_files_count', 0)}
                </div>
                <div class="info-card">
                    <strong>Images</strong>
                    {assets.get('images_count', 0)}
                </div>
                <div class="info-card">
                    <strong>Total CSS Size</strong>
                    {assets.get('total_css_size_kb', 0)} KB
                </div>
            </div>
        </div>
        """
    
    def _generate_markdown(self, data: Dict) -> str:
        """Generate Markdown report."""
        md = f"""# Website Analysis Report

## General Information

- **URL**: {data['general_info']['url']}
- **Title**: {data['general_info'].get('title', 'N/A')}
- **Platform**: {'Webflow' if data['general_info'].get('is_webflow') else 'Not Webflow'}
- **Description**: {data['general_info'].get('meta_description', 'N/A')}

---

"""

        # Webflow Detection
        if data['webflow_detection']['is_webflow']:
            md += f"""## Webflow Detection

- **Confidence**: {data['webflow_detection']['confidence']}%
- **Site ID**: {data['webflow_detection']['webflow_data'].get('site_id', 'N/A')}
- **Version**: {data['webflow_detection']['webflow_data'].get('version', 'N/A')}
- **Components**: {', '.join(data['webflow_detection']['webflow_data'].get('components', []))}

---

"""

        # Design System
        md += f"""## Design System

### Colors

**Primary Colors** (Top 10):
"""
        for color in data['design_system']['colors'].get('primary_colors', [])[:10]:
            md += f"- `{color}`\n"
        
        md += f"\n**Total Unique Colors**: {len(data['design_system']['colors'].get('all', []))}\n\n"
        
        md += "### Typography\n\n"
        md += f"**Font Families**: {', '.join(data['design_system']['typography'].get('font_families', [])[:5])}\n\n"
        md += f"**Font Sizes**: {len(data['design_system']['typography'].get('font_sizes', []))} different sizes\n\n"
        
        md += f"### CSS Variables\n\n"
        md += f"Found {len(data['design_system']['css_variables'].get('all', {}))} CSS custom properties\n\n"
        
        md += "---\n\n"
        
        # Tech Stack
        md += "## Technology Stack\n\n"
        md += f"**Total Technologies**: {data['tech_stack']['summary']['total_technologies']}\n\n"
        
        for category in ['cms', 'frameworks', 'libraries', 'analytics', 'fonts']:
            if data['tech_stack'].get(category):
                md += f"### {category.title()}\n\n"
                for tech in data['tech_stack'][category]:
                    md += f"- {tech}\n"
                md += "\n"
        
        md += f"### Hosting\n\n"
        md += f"- **Provider**: {data['tech_stack']['hosting']['provider']}\n"
        md += f"- **Confidence**: {data['tech_stack']['hosting']['confidence']}\n\n"
        
        md += "---\n\n"
        
        # Structure
        md += "## Page Structure\n\n"
        md += f"- **Total Sections**: {len(data['structure'].get('sections', []))}\n"
        md += f"- **Unique CSS Classes**: {data['structure']['classes'].get('total_unique', 0)}\n"
        md += f"- **Total Links**: {data['structure']['navigation'].get('total_links', 0)}\n"
        md += f"- **Grid Layouts**: {data['structure']['layout_patterns'].get('grid_layouts', 0)}\n\n"
        
        md += "---\n\n"
        
        # Assets
        md += "## Assets Summary\n\n"
        md += f"- **CSS Files**: {data['assets_summary'].get('css_files_count', 0)}\n"
        md += f"- **JavaScript Files**: {data['assets_summary'].get('js_files_count', 0)}\n"
        md += f"- **Images**: {data['assets_summary'].get('images_count', 0)}\n"
        md += f"- **Total CSS Size**: {data['assets_summary'].get('total_css_size_kb', 0)} KB\n\n"
        
        md += "---\n\n"
        md += f"*Generated on {data['metadata']['timestamp']}*\n"
        md += f"*Webflow Design Scraper v{data['metadata']['version']}*\n"
        
        return md
    
    def _save_report(self, content: str, filepath: str):
        """Save report to file."""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
