# Webflow Design Scraper

A powerful Python tool that analyzes and extracts design systems, CSS patterns, and technical stack information from Webflow-powered websites.

## Features

- **Webflow Detection**: Automatically detects Webflow sites with confidence scoring
- **Design System Analysis**: Extracts colors, typography, spacing, and layout patterns
- **CSS Analysis**: Comprehensive CSS collection and analysis including animations and variables
- **Structure Analysis**: Maps DOM structure and identifies UI components
- **Tech Stack Detection**: Identifies 50+ technologies, frameworks, and libraries
- **Multiple Output Formats**: JSON, HTML, and Markdown reports

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hasintha01/flow-scraper.git
cd flow-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run setup verification:
```bash
python setup.py
```

## Quick Start

Analyze a website:
```bash
python main.py https://example.com
```

Specify output format:
```bash
python main.py https://example.com --format json
python main.py https://example.com --format html
python main.py https://example.com --format markdown
```

Save to custom location:
```bash
python main.py https://example.com --output ./reports/analysis.json
```

## Usage

See [USAGE.md](USAGE.md) for detailed usage instructions and examples.

## Architecture

The tool is built with a modular architecture:

- **HTML Fetcher**: Downloads and processes HTML content
- **Webflow Detector**: Identifies Webflow sites
- **CSS Collector**: Gathers all CSS sources
- **CSS Analyzer**: Analyzes design patterns
- **Structure Analyzer**: Maps DOM and UI components
- **Tech Analyzer**: Detects technologies
- **Report Generator**: Creates output reports

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Requirements

- Python 3.8 or higher
- Internet connection for downloading web content
- Chrome/Chromium browser (for Selenium support)

## Dependencies

- requests: HTTP requests
- beautifulsoup4: HTML parsing
- lxml: XML/HTML processing
- cssutils: CSS parsing
- tinycss2: Modern CSS parsing
- selenium: Dynamic content handling
- rich: CLI formatting
- colorama: Cross-platform colored output
- jinja2: Template rendering
- markdown: Markdown processing

## Output Examples

The tool generates comprehensive reports including:

- Color palettes with hex codes and usage frequency
- Typography system (fonts, sizes, weights)
- Spacing and layout patterns
- CSS animations and transitions
- Technology stack detection
- DOM structure visualization
- UI component patterns

## Legal Disclaimer

This tool is intended for educational and research purposes only. When using this tool:

- Always respect robots.txt and website terms of service
- Obtain permission before scraping websites
- Use responsibly and ethically
- Be aware of rate limiting and server load
- Comply with applicable laws and regulations regarding web scraping

The authors and contributors are not responsible for any misuse of this tool.

## License

Copyright (c) 2024 Hasintha01

See [LICENSE](LICENSE) for full license text.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Author

Created by Hasintha01

## Acknowledgments

Built with Python and powered by industry-standard libraries for web scraping and analysis.
