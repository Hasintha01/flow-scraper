"""
Main CLI entry point for the Webflow Design Scraper.
"""

import argparse
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper import WebflowScraper


def main():
    """Main CLI function."""
    console = Console()
    
    # Print banner
    console.print(Panel.fit(
        "[bold cyan]🎨 Webflow Design Scraper[/bold cyan]\n"
        "[dim]Extract design systems and technology stacks from any website[/dim]",
        border_style="cyan"
    ))
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Analyze websites and extract design systems, technology stacks, and CSS structures.'
    )
    parser.add_argument('url', help='Website URL to analyze')
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'html', 'markdown'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (if not specified, prints to stdout)'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        console.print("[red]Error: URL must start with http:// or https://[/red]")
        sys.exit(1)
    
    # Auto-generate output filename if format is specified but no output file
    if not args.output:
        from urllib.parse import urlparse
        import re
        
        # Extract domain and clean it
        parsed = urlparse(args.url)
        domain = parsed.netloc.replace('www.', '')
        
        # Convert domain to website name (e.g., webflow.com -> Webflow)
        website_name = domain.split('.')[0].capitalize()
        
        # Clean website name to be filesystem-safe
        website_name = re.sub(r'[^\w\s-]', '', website_name)
        
        extension = args.format if args.format != 'markdown' else 'md'
        args.output = f"{website_name}_Analysis.{extension}"
    
    try:
        # Initialize scraper
        scraper = WebflowScraper(timeout=args.timeout)
        
        # Perform analysis and generate report
        report = scraper.scrape_and_report(args.url, args.format, args.output)
        
        # Print report if no output file specified
        if not args.output:
            console.print("\n" + "="*80 + "\n")
            console.print(report)
        
        console.print("\n[bold green]✨ Done![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        import traceback
        if '--debug' in sys.argv:
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
