# Example Outputs

This directory contains example outputs from the Webflow Design Scraper.

## Sample Reports

When you run the tool, you can generate reports in three formats:

### 1. JSON Output
```bash
python main.py https://example.com --format json --output example_report.json
```

See: `example_report.json` (generated after running)

### 2. HTML Output
```bash
python main.py https://example.com --format html --output example_report.html
```

See: `example_report.html` (generated after running)

### 3. Markdown Output
```bash
python main.py https://example.com --format markdown --output example_report.md
```

See: `example_report.md` (generated after running)

## Running Examples

To run the example script:

```bash
cd examples
python example_usage.py
```

This will demonstrate:
- Basic usage
- Report generation
- Custom analysis
- Website comparison

## Sample Data Structure

Here's what the JSON output looks like:

```json
{
  "metadata": {
    "version": "1.0.0",
    "timestamp": "2025-11-18T10:30:00",
    "url_requested": "https://example.com",
    "url_final": "https://example.com"
  },
  "general_info": {
    "url": "https://example.com",
    "title": "Example Website",
    "meta_description": "An example website",
    "is_webflow": true
  },
  "webflow_detection": {
    "is_webflow": true,
    "confidence": 95.5,
    "webflow_data": {
      "site_id": "abc123",
      "page_id": "xyz789",
      "version": "1.0",
      "components": ["navigation", "slider", "form"]
    }
  },
  "design_system": {
    "colors": {
      "primary_colors": ["#0066FF", "#FF6B6B", "#FFFFFF"],
      "all": [...],
      "hex": [...],
      "rgb": [...],
      "frequency": {...}
    },
    "typography": {
      "font_families": ["Inter", "Roboto"],
      "font_sizes": ["16px", "18px", "24px"],
      "font_weights": ["400", "500", "700"]
    },
    "spacing": {
      "margins": [...],
      "paddings": [...],
      "common_spacing": [...]
    },
    "css_variables": {
      "all": {...},
      "colors": {...},
      "fonts": {...}
    }
  },
  "tech_stack": {
    "cms": ["Webflow"],
    "frameworks": [],
    "libraries": ["jQuery", "GSAP"],
    "analytics": ["Google Analytics"],
    "fonts": ["Google Fonts"],
    "hosting": {
      "provider": "Webflow",
      "confidence": "high"
    }
  },
  "structure": {
    "page_info": {...},
    "sections": [...],
    "navigation": {...},
    "classes": {...},
    "layout_patterns": {...}
  },
  "assets_summary": {
    "css_files_count": 5,
    "js_files_count": 8,
    "images_count": 45,
    "total_css_size_kb": 128.5
  }
}
```

## Notes

- Reports are generated dynamically based on the website analyzed
- HTML reports include styled, interactive elements
- JSON reports contain complete raw data
- Markdown reports are great for documentation
