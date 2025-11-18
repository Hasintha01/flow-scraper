"""
Main Webflow Scraper
Orchestrates all modules to perform complete website analysis.
"""

from typing import Dict, Optional
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from html_fetcher import HTMLFetcher
from webflow_detector import WebflowDetector
from css_collector import CSSCollector
from css_analyzer import CSSAnalyzer
from structure_analyzer import PageStructureAnalyzer
from tech_analyzer import TechnologyStackAnalyzer
from report_generator import ReportGenerator


class WebflowScraper:
    """Main scraper class that orchestrates all analysis modules."""
    
    VERSION = "1.0.0"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the Webflow Scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.fetcher = HTMLFetcher(timeout)
        self.webflow_detector = WebflowDetector()
        self.css_collector = CSSCollector(self.fetcher)
        self.css_analyzer = CSSAnalyzer()
        self.structure_analyzer = PageStructureAnalyzer()
        self.tech_analyzer = TechnologyStackAnalyzer()
        self.report_generator = ReportGenerator()
    
    def scrape(self, url: str) -> Dict:
        """
        Scrape and analyze a website.
        
        Args:
            url: Target website URL
            
        Returns:
            Complete analysis data dictionary
        """
        print(f"🌐 Fetching: {url}")
        
        # Step 1: Fetch HTML
        try:
            html, soup, assets = self.fetcher.fetch(url)
            print("✓ HTML fetched successfully")
        except Exception as e:
            print(f"✗ Failed to fetch HTML: {str(e)}")
            raise
        
        # Step 2: Detect Webflow
        print("🔍 Detecting Webflow...")
        webflow_detection = self.webflow_detector.detect(html, soup, assets)
        if webflow_detection['is_webflow']:
            print(f"✓ Webflow detected (Confidence: {webflow_detection['confidence']}%)")
        else:
            print("ℹ Not a Webflow site")
        
        # Step 3: Collect CSS
        print("📄 Collecting CSS...")
        css_data = self.css_collector.collect(soup, assets)
        css_stats = self.css_collector.get_css_statistics(css_data)
        print(f"✓ Collected {css_stats['external_files_count']} CSS files ({css_stats['total_size_kb']} KB)")
        
        # Step 4: Analyze CSS
        print("🎨 Analyzing design system...")
        design_system = self.css_analyzer.analyze(css_data)
        print(f"✓ Found {len(design_system['colors']['all'])} colors, {len(design_system['typography']['font_families'])} fonts")
        
        # Step 5: Analyze Structure
        print("🏗️ Analyzing page structure...")
        structure = self.structure_analyzer.analyze(soup)
        print(f"✓ Analyzed {len(structure['sections'])} sections, {structure['classes']['total_unique']} unique classes")
        
        # Step 6: Analyze Technology Stack
        print("⚙️ Detecting technologies...")
        tech_stack = self.tech_analyzer.analyze(soup, assets)
        tech_summary = self.tech_analyzer.get_technology_summary(tech_stack)
        print(f"✓ Detected {tech_summary['total_technologies']} technologies")
        
        # Compile results
        final_url = self.fetcher.get_final_url(url)
        
        results = {
            'metadata': {
                'version': self.VERSION,
                'timestamp': datetime.now().isoformat(),
                'url_requested': url,
                'url_final': final_url
            },
            'general_info': {
                'url': final_url,
                'title': structure['page_info']['title'],
                'meta_description': structure['page_info']['meta_description'],
                'favicon': structure['page_info']['favicon'],
                'lang': structure['page_info']['lang'],
                'charset': structure['page_info']['charset'],
                'is_webflow': webflow_detection['is_webflow']
            },
            'webflow_detection': webflow_detection,
            'design_system': design_system,
            'structure': structure,
            'tech_stack': {
                **tech_stack,
                'summary': tech_summary
            },
            'css_data': {
                'statistics': css_stats,
                'sources': css_data['sources']
            },
            'assets_summary': {
                'css_files_count': len(assets.get('css', [])),
                'js_files_count': len(assets.get('js', [])),
                'images_count': len(assets.get('images', [])),
                'total_css_size_kb': css_stats['total_size_kb'],
                'css_files': assets.get('css', [])[:10],  # First 10 only
                'js_files': assets.get('js', [])[:10]
            }
        }
        
        print("✅ Analysis complete!")
        return results
    
    def scrape_and_report(self, url: str, format: str = 'json', 
                         output_file: Optional[str] = None) -> str:
        """
        Scrape a website and generate a report.
        
        Args:
            url: Target website URL
            format: Report format ('json', 'html', 'markdown')
            output_file: Optional output file path
            
        Returns:
            Report content as string
        """
        # Perform analysis
        results = self.scrape(url)
        
        # Generate report
        print(f"📊 Generating {format.upper()} report...")
        report = self.report_generator.generate(results, format, output_file)
        
        if output_file:
            print(f"✓ Report saved to: {output_file}")
        
        return report
