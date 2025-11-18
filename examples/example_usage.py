"""
Example: Using the Webflow Scraper programmatically
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scraper import WebflowScraper


def example_basic_usage():
    """Basic usage example."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 80)
    
    # Initialize scraper
    scraper = WebflowScraper(timeout=30)
    
    # Scrape a website
    url = 'https://webflow.com'  # Example Webflow site
    
    try:
        results = scraper.scrape(url)
        
        # Access specific data
        print(f"\n✅ Analysis Complete!")
        print(f"\nWebsite: {results['general_info']['url']}")
        print(f"Title: {results['general_info']['title']}")
        print(f"Is Webflow: {results['webflow_detection']['is_webflow']}")
        
        if results['webflow_detection']['is_webflow']:
            print(f"Confidence: {results['webflow_detection']['confidence']}%")
        
        print(f"\nColors found: {len(results['design_system']['colors']['all'])}")
        print(f"Primary colors: {results['design_system']['colors']['primary_colors'][:5]}")
        
        print(f"\nFont families: {results['design_system']['typography']['font_families'][:3]}")
        
        print(f"\nTechnologies: {len(results['tech_stack']['all'])} detected")
        for tech in results['tech_stack']['all'][:5]:
            print(f"  - {tech['name']} ({tech['category']})")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def example_generate_reports():
    """Generate reports in different formats."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Generate Reports")
    print("=" * 80)
    
    scraper = WebflowScraper()
    url = 'https://webflow.com'
    
    try:
        # Generate JSON report
        print("\n📄 Generating JSON report...")
        json_report = scraper.scrape_and_report(url, format='json', output_file='example_report.json')
        print("✓ JSON report saved to: example_report.json")
        
        # Generate HTML report
        print("\n📄 Generating HTML report...")
        html_report = scraper.scrape_and_report(url, format='html', output_file='example_report.html')
        print("✓ HTML report saved to: example_report.html")
        
        # Generate Markdown report
        print("\n📄 Generating Markdown report...")
        md_report = scraper.scrape_and_report(url, format='markdown', output_file='example_report.md')
        print("✓ Markdown report saved to: example_report.md")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def example_custom_analysis():
    """Custom analysis focusing on specific aspects."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Custom Analysis")
    print("=" * 80)
    
    scraper = WebflowScraper()
    url = 'https://webflow.com'
    
    try:
        results = scraper.scrape(url)
        
        # Analyze color palette
        print("\n🎨 COLOR PALETTE ANALYSIS")
        print("-" * 40)
        colors = results['design_system']['colors']
        print(f"Total unique colors: {len(colors['all'])}")
        print(f"HEX colors: {len(colors['hex'])}")
        print(f"RGB colors: {len(colors['rgb'])}")
        print(f"RGBA colors: {len(colors['rgba'])}")
        
        print("\nMost used colors:")
        for color, count in list(colors['frequency'].items())[:10]:
            print(f"  {color}: used {count} times")
        
        # Analyze typography
        print("\n✍️ TYPOGRAPHY ANALYSIS")
        print("-" * 40)
        typo = results['design_system']['typography']
        print(f"Font families: {', '.join(typo['font_families'][:5])}")
        print(f"Font sizes: {len(typo['font_sizes'])} different sizes")
        print(f"Font weights: {', '.join(typo['font_weights'][:5])}")
        
        # Analyze CSS variables
        print("\n🔧 CSS VARIABLES")
        print("-" * 40)
        variables = results['design_system']['css_variables']
        print(f"Total CSS variables: {len(variables['all'])}")
        print(f"Color variables: {len(variables['colors'])}")
        print(f"Font variables: {len(variables['fonts'])}")
        print(f"Spacing variables: {len(variables['spacing'])}")
        
        # Analyze page structure
        print("\n🏗️ PAGE STRUCTURE")
        print("-" * 40)
        structure = results['structure']
        print(f"Sections: {len(structure['sections'])}")
        print(f"Unique CSS classes: {structure['classes']['total_unique']}")
        print(f"Total links: {structure['navigation']['total_links']}")
        print(f"Grid layouts: {structure['layout_patterns']['grid_layouts']}")
        print(f"Flex layouts: {structure['layout_patterns']['flex_layouts']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def example_compare_websites():
    """Compare design systems of multiple websites."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Compare Multiple Websites")
    print("=" * 80)
    
    scraper = WebflowScraper()
    
    websites = [
        'https://webflow.com',
        'https://www.apple.com'
    ]
    
    results_list = []
    
    for url in websites:
        try:
            print(f"\n📊 Analyzing: {url}")
            results = scraper.scrape(url)
            results_list.append({
                'url': url,
                'data': results
            })
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    # Compare results
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    
    for site in results_list:
        print(f"\n{site['url']}")
        print("-" * 40)
        data = site['data']
        print(f"  Colors: {len(data['design_system']['colors']['all'])}")
        print(f"  Fonts: {len(data['design_system']['typography']['font_families'])}")
        print(f"  Technologies: {data['tech_stack']['summary']['total_technologies']}")
        print(f"  Sections: {len(data['structure']['sections'])}")


if __name__ == '__main__':
    print("\n🎨 Webflow Design Scraper - Examples\n")
    
    # Run examples
    try:
        example_basic_usage()
        
        # Uncomment to run other examples:
        # example_generate_reports()
        # example_custom_analysis()
        # example_compare_websites()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
