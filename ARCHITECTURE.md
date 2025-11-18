# Architecture Documentation

## System Overview

The Webflow Design Scraper is built with a modular architecture that separates concerns into specialized analyzers and processors. Each module has a specific responsibility and can be used independently or as part of the complete analysis pipeline.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Main CLI                            │
│                       (main.py)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Webflow Scraper                           │
│                   (scraper.py)                              │
│              [Orchestrates all modules]                     │
└───┬──────────────┬──────────────┬──────────────┬───────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐
│  HTML  │  │  Webflow   │  │   CSS    │  │   Tech   │
│Fetcher │  │ Detector   │  │Collector │  │ Analyzer │
└────┬───┘  └──────┬─────┘  └─────┬────┘  └─────┬────┘
     │             │              │             │
     └─────────────┴──────────────┴─────────────┘
                   │
                   ▼
     ┌─────────────────────────┐
     │    CSS Analyzer         │
     │  (Design System)        │
     └────────────┬────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │  Structure Analyzer     │
     │   (DOM & Patterns)      │
     └────────────┬────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │   Report Generator      │
     │  (JSON/HTML/Markdown)   │
     └─────────────────────────┘
```

## Module Descriptions

### 1. HTML Fetcher (`html_fetcher.py`)

**Purpose**: Downloads and processes HTML content from URLs

**Key Features**:
- HTTP/HTTPS request handling
- Redirect following
- Asset URL extraction
- Custom user agent support
- Timeout configuration
- SSL verification options

**Key Classes**:
```python
class HTMLFetcher:
    def fetch(url) -> dict
    def fetch_asset(url) -> str
    def get_final_url(url) -> str
```

**Output**:
```python
{
    'html': str,           # HTML content
    'final_url': str,      # URL after redirects
    'status_code': int,    # HTTP status
    'css_links': list,     # External CSS URLs
    'js_links': list       # External JS URLs
}
```

### 2. Webflow Detector (`webflow_detector.py`)

**Purpose**: Identifies Webflow-powered websites with confidence scoring

**Detection Methods**:
- Webflow CSS file patterns
- Webflow JavaScript patterns
- Webflow-specific CSS classes
- Meta tags and attributes
- CDN patterns

**Key Classes**:
```python
class WebflowDetector:
    def detect(html, css_links) -> dict
    def _check_webflow_css(links) -> int
    def _check_webflow_js(links) -> int
    def _check_webflow_classes(html) -> int
    def _check_webflow_attributes(html) -> int
```

**Confidence Scoring**:
- 0-30: Not Webflow
- 31-60: Possibly Webflow
- 61-80: Likely Webflow
- 81-100: Definitely Webflow

**Output**:
```python
{
    'is_webflow': bool,
    'confidence_score': int,
    'indicators': list
}
```

### 3. CSS Collector (`css_collector.py`)

**Purpose**: Gathers CSS from all sources (external, inline, style attributes)

**Collection Sources**:
- External stylesheets
- `<style>` tags
- Inline `style` attributes
- CSS variables
- `@import` rules

**Key Classes**:
```python
class CSSCollector:
    def collect(html, css_links, fetcher) -> dict
    def _extract_inline_styles(html) -> str
    def _extract_style_attributes(html) -> str
    def _resolve_imports(css, base_url) -> str
```

**Output**:
```python
{
    'external_css': list,     # External stylesheet contents
    'inline_css': str,        # Inline <style> tags
    'style_attributes': str,  # style="" attributes
    'total_size': int,        # Total CSS bytes
    'sources': list           # List of CSS sources
}
```

### 4. CSS Analyzer (`css_analyzer.py`)

**Purpose**: Analyzes CSS to extract design system patterns

**Analysis Categories**:
- **Colors**: Hex, RGB, RGBA, HSL, color names
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Margins, padding, gaps
- **Layout**: Flexbox, Grid properties
- **Animations**: Keyframes, transitions
- **CSS Variables**: Custom properties
- **Media Queries**: Breakpoints

**Key Classes**:
```python
class CSSAnalyzer:
    def analyze(css_content) -> dict
    def _extract_colors(css) -> list
    def _extract_typography(css) -> dict
    def _extract_spacing(css) -> dict
    def _extract_animations(css) -> dict
    def _extract_variables(css) -> dict
```

**Output**:
```python
{
    'colors': [
        {'hex': '#FF5733', 'count': 42, 'type': 'hex'},
        ...
    ],
    'typography': {
        'fonts': [{'family': 'Inter', 'weights': [400, 700]}],
        'sizes': ['16px', '24px', '32px'],
        'line_heights': ['1.5', '1.75']
    },
    'spacing': {
        'margins': ['8px', '16px', '24px'],
        'paddings': ['12px', '20px'],
        'gaps': ['1rem', '2rem']
    },
    'animations': [...],
    'variables': {...}
}
```

### 5. Structure Analyzer (`structure_analyzer.py`)

**Purpose**: Maps DOM structure and identifies UI component patterns

**Analysis Features**:
- DOM tree depth calculation
- Element type distribution
- CSS class extraction
- ID attribute collection
- UI pattern detection (navigation, forms, cards, modals)
- Semantic HTML analysis

**Key Classes**:
```python
class StructureAnalyzer:
    def analyze(soup) -> dict
    def _calculate_depth(element) -> int
    def _extract_classes(soup) -> list
    def _detect_ui_patterns(soup) -> dict
```

**UI Pattern Detection**:
- Navigation bars
- Hero sections
- Card grids
- Forms
- Modals/dialogs
- Footers
- Galleries

**Output**:
```python
{
    'total_elements': int,
    'depth': int,
    'elements_by_type': dict,
    'classes': list,
    'ids': list,
    'ui_patterns': {
        'navigation': [...],
        'cards': [...],
        'forms': [...]
    }
}
```

### 6. Tech Analyzer (`tech_analyzer.py`)

**Purpose**: Detects technologies, frameworks, and libraries used on the website

**Detection Categories**:
- **CMS**: WordPress, Webflow, Shopify, Wix, Squarespace
- **Frameworks**: React, Vue, Angular, Svelte, Next.js
- **Libraries**: jQuery, Lodash, GSAP, Three.js
- **Analytics**: Google Analytics, Mixpanel, Hotjar
- **CDNs**: Cloudflare, Fastly, AWS CloudFront
- **Fonts**: Google Fonts, Adobe Fonts
- **APIs**: Stripe, Mailchimp, etc.

**Key Classes**:
```python
class TechAnalyzer:
    def detect(html, css_data) -> dict
    def _detect_frameworks(html) -> list
    def _detect_libraries(html) -> list
    def _detect_cms(html, css) -> list
```

**Output**:
```python
{
    'technologies': [
        {
            'name': 'React',
            'category': 'framework',
            'confidence': 'high',
            'version': '18.2.0'
        },
        ...
    ],
    'total_count': int
}
```

### 7. Report Generator (`report_generator.py`)

**Purpose**: Generates formatted reports in multiple formats

**Output Formats**:
- **JSON**: Structured data format
- **HTML**: Interactive visual report with styling
- **Markdown**: Human-readable documentation

**Key Classes**:
```python
class ReportGenerator:
    def generate(data, format) -> str
    def _generate_json(data) -> str
    def _generate_html(data) -> str
    def _generate_markdown(data) -> str
```

**HTML Report Features**:
- Responsive design
- Color palette visualization
- Font samples
- Technology badges
- Collapsible sections
- Syntax highlighting
- Copy-to-clipboard functionality

### 8. Main Scraper (`scraper.py`)

**Purpose**: Orchestrates all modules and manages the analysis pipeline

**Analysis Pipeline**:
1. Fetch HTML content
2. Detect Webflow
3. Collect CSS
4. Analyze design system
5. Analyze structure
6. Detect technologies
7. Compile results

**Key Classes**:
```python
class WebflowScraper:
    def __init__(html_fetcher=None)
    def analyze(url) -> dict
    def _compile_results(data) -> dict
```

**Output**:
```python
{
    'url': str,
    'timestamp': str,
    'is_webflow': bool,
    'confidence_score': int,
    'webflow_indicators': list,
    'design_system': dict,
    'structure': dict,
    'tech_stack': dict,
    'css_data': dict
}
```

## Data Flow

```
URL Input
    ↓
HTML Fetcher → HTML + CSS Links
    ↓
Webflow Detector → Detection Results
    ↓
CSS Collector → Combined CSS
    ↓
CSS Analyzer → Design System
    ↓
Structure Analyzer → DOM Structure
    ↓
Tech Analyzer → Technology Stack
    ↓
Scraper → Compiled Results
    ↓
Report Generator → Final Output
```

## Design Principles

### Modularity
Each analyzer is independent and can be used separately. This allows for:
- Easy testing
- Component reusability
- Flexible integration

### Separation of Concerns
Each module has a single, well-defined responsibility:
- Fetcher: Only downloads content
- Detectors: Only identify patterns
- Analyzers: Only process data
- Generator: Only formats output

### Extensibility
New analyzers can be added without modifying existing code:
```python
from src.scraper import WebflowScraper
from custom_analyzer import CustomAnalyzer

scraper = WebflowScraper()
result = scraper.analyze(url)
custom_analysis = CustomAnalyzer().analyze(result)
```

### Error Handling
Each module handles its own errors gracefully:
- Network errors in fetcher
- Parse errors in analyzers
- Invalid data in generator

### Performance
Optimizations throughout:
- Caching of external resources
- Deduplication of CSS rules
- Efficient DOM traversal
- Lazy evaluation where possible

## Configuration

### Environment Variables
```bash
# Optional configurations
WEBFLOW_SCRAPER_TIMEOUT=30
WEBFLOW_SCRAPER_USER_AGENT="Mozilla/5.0..."
WEBFLOW_SCRAPER_MAX_CSS_SIZE=10485760
```

### Programmatic Configuration
```python
from src.scraper import WebflowScraper
from src.html_fetcher import HTMLFetcher

fetcher = HTMLFetcher(
    timeout=60,
    user_agent="CustomBot/1.0",
    verify_ssl=True
)

scraper = WebflowScraper(html_fetcher=fetcher)
```

## Testing

Each module includes comprehensive tests:

```
tests/
├── test_html_fetcher.py
├── test_webflow_detector.py
├── test_css_collector.py
├── test_css_analyzer.py
├── test_structure_analyzer.py
├── test_tech_analyzer.py
├── test_report_generator.py
└── test_scraper.py
```

Run tests:
```bash
python -m pytest tests/
```

## Dependencies

**Core Dependencies**:
- `requests`: HTTP client
- `beautifulsoup4`: HTML parsing
- `lxml`: Fast XML/HTML parser
- `cssutils`: CSS parsing and manipulation
- `tinycss2`: Modern CSS parser

**Optional Dependencies**:
- `selenium`: JavaScript-heavy sites
- `playwright`: Alternative to Selenium

**CLI Dependencies**:
- `rich`: Pretty CLI output
- `colorama`: Cross-platform colors

**Report Dependencies**:
- `jinja2`: HTML templating
- `markdown`: Markdown processing

## Performance Considerations

### Memory Usage
- CSS is processed in chunks
- Large DOM trees are traversed efficiently
- Results are deduplicated

### Network Usage
- Respects rate limits
- Caches external resources
- Configurable timeouts

### CPU Usage
- Regex patterns are compiled once
- BeautifulSoup uses fast parsers
- Parallel processing where safe

## Security Considerations

### Input Validation
- URL validation
- HTML sanitization
- CSS parsing in safe mode

### Resource Limits
- Maximum CSS size limits
- Timeout controls
- Redirect limits

### Privacy
- No data sent to external services
- All processing done locally
- No persistent storage

## Future Enhancements

Planned features:
- Screenshot capture
- Accessibility analysis
- Performance metrics
- Component extraction
- Style guide generation
- Figma export
- API endpoint

## Contributing

To add a new analyzer:

1. Create module in `src/`
2. Implement analyzer class
3. Add tests
4. Update scraper.py to use it
5. Document in this file

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.
