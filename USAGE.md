# Usage Guide

## Command Line Interface

### Basic Usage

```bash
python main.py <url> [options]
```

### Options

- `url`: The website URL to analyze (required)
- `--format`: Output format - json, html, or markdown (default: json)
- `--output`: Output file path (default: auto-generated)
- `--user-agent`: Custom user agent string
- `--timeout`: Request timeout in seconds (default: 30)
- `--no-verify-ssl`: Disable SSL certificate verification

### Examples

#### Analyze with default settings
```bash
python main.py https://webflow.com
```

#### Generate HTML report
```bash
python main.py https://webflow.com --format html
```

#### Save to specific location
```bash
python main.py https://webflow.com --output reports/webflow.json
```

#### Custom user agent
```bash
python main.py https://example.com --user-agent "MyBot/1.0"
```

#### Multiple options
```bash
python main.py https://example.com --format html --output analysis.html --timeout 60
```

## Programmatic Usage

### Import and Use

```python
from src.scraper import WebflowScraper

# Create scraper instance
scraper = WebflowScraper()

# Analyze a website
result = scraper.analyze("https://example.com")

# Access results
print(f"Is Webflow: {result['is_webflow']}")
print(f"Colors found: {len(result['design_system']['colors'])}")
print(f"Technologies: {result['tech_stack']['technologies']}")
```

### Custom Configuration

```python
from src.scraper import WebflowScraper
from src.html_fetcher import HTMLFetcher

# Custom fetcher with specific user agent
fetcher = HTMLFetcher(
    user_agent="CustomBot/1.0",
    timeout=60
)

scraper = WebflowScraper(html_fetcher=fetcher)
result = scraper.analyze("https://example.com")
```

### Generate Reports

```python
from src.scraper import WebflowScraper
from src.report_generator import ReportGenerator

scraper = WebflowScraper()
result = scraper.analyze("https://example.com")

generator = ReportGenerator()

# JSON report
json_report = generator.generate(result, format='json')
with open('report.json', 'w') as f:
    f.write(json_report)

# HTML report
html_report = generator.generate(result, format='html')
with open('report.html', 'w') as f:
    f.write(html_report)

# Markdown report
md_report = generator.generate(result, format='markdown')
with open('report.md', 'w') as f:
    f.write(md_report)
```

## Output Formats

### JSON Format

Structured data format with complete analysis:

```json
{
  "url": "https://example.com",
  "timestamp": "2024-01-01T12:00:00",
  "is_webflow": true,
  "confidence_score": 95,
  "design_system": {
    "colors": [...],
    "typography": {...},
    "spacing": {...}
  },
  "structure": {...},
  "tech_stack": {...}
}
```

### HTML Format

Interactive visual report with:
- Summary cards
- Color palettes
- Typography samples
- Technology badges
- Code examples
- Collapsible sections

### Markdown Format

Human-readable documentation with:
- Structured headings
- Tables for data
- Code blocks
- Lists and formatting

## Understanding Results

### Webflow Detection

```python
result['is_webflow']  # Boolean
result['confidence_score']  # 0-100
result['webflow_indicators']  # List of detected signals
```

### Design System

**Colors:**
```python
result['design_system']['colors']
# [{'hex': '#FF5733', 'count': 42}, ...]
```

**Typography:**
```python
result['design_system']['typography']['fonts']
# [{'family': 'Inter', 'weights': [400, 700]}, ...]
```

**Spacing:**
```python
result['design_system']['spacing']
# {'margins': [...], 'paddings': [...], 'gaps': [...]}
```

### Structure Analysis

```python
result['structure']['total_elements']  # Element count
result['structure']['depth']  # DOM depth
result['structure']['classes']  # CSS classes used
result['structure']['ui_patterns']  # Detected components
```

### Technology Stack

```python
result['tech_stack']['technologies']
# [{'name': 'React', 'category': 'framework', 'confidence': 'high'}, ...]
```

## Best Practices

### Rate Limiting

Add delays between requests:

```python
import time
from src.scraper import WebflowScraper

scraper = WebflowScraper()
urls = ['https://site1.com', 'https://site2.com', 'https://site3.com']

for url in urls:
    result = scraper.analyze(url)
    # Process result
    time.sleep(5)  # Wait 5 seconds between requests
```

### Error Handling

```python
from src.scraper import WebflowScraper

scraper = WebflowScraper()

try:
    result = scraper.analyze("https://example.com")
    print("Analysis successful!")
except Exception as e:
    print(f"Analysis failed: {e}")
```

### Large Scale Analysis

```python
from src.scraper import WebflowScraper
import json

scraper = WebflowScraper()
urls = [...]  # Your URL list
results = []

for url in urls:
    try:
        result = scraper.analyze(url)
        results.append(result)
        
        # Save incrementally
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
    except Exception as e:
        print(f"Failed {url}: {e}")
        continue
```

## Troubleshooting

### Connection Issues

If you encounter connection errors:

```bash
# Increase timeout
python main.py https://example.com --timeout 120

# Disable SSL verification (use cautiously)
python main.py https://example.com --no-verify-ssl
```

### Large Websites

For large sites with lots of CSS:

```python
# The analyzer automatically handles large CSS files
# Results are optimized and deduplicated
```

### Dynamic Content

For JavaScript-heavy sites:

```python
# Selenium support is built-in
# Dynamic content is automatically rendered
```

## Advanced Features

### Custom CSS Analysis

```python
from src.css_analyzer import CSSAnalyzer

analyzer = CSSAnalyzer()
css_code = "body { color: #333; font-size: 16px; }"
analysis = analyzer.analyze(css_code)
```

### Structure Pattern Detection

```python
from src.structure_analyzer import StructureAnalyzer
from bs4 import BeautifulSoup

analyzer = StructureAnalyzer()
soup = BeautifulSoup(html, 'html.parser')
structure = analyzer.analyze(soup)
```

### Technology Detection

```python
from src.tech_analyzer import TechAnalyzer

analyzer = TechAnalyzer()
technologies = analyzer.detect(html_content, collected_css)
```

## Getting Help

- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See [examples/](examples/) for more code samples
- Open an issue on GitHub for bugs or questions
