"""
Quick setup and test script for Webflow Design Scraper
"""

import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def test_imports():
    """Test if all modules can be imported."""
    print("\n🔍 Testing imports...")
    
    modules = [
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4'),
        ('colorama', 'colorama'),
        ('rich', 'rich')
    ]
    
    success = True
    for module_name, package_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"❌ {package_name} not found")
            success = False
    
    return success


def test_basic_functionality():
    """Test basic scraper functionality."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.html_fetcher import HTMLFetcher
        from src.webflow_detector import WebflowDetector
        from src.css_collector import CSSCollector
        from src.css_analyzer import CSSAnalyzer
        from src.structure_analyzer import PageStructureAnalyzer
        from src.tech_analyzer import TechnologyStackAnalyzer
        from src.report_generator import ReportGenerator
        from src.scraper import WebflowScraper
        
        print("✓ All modules imported successfully")
        
        # Test basic initialization
        scraper = WebflowScraper(timeout=30)
        print("✓ Scraper initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "="*80)
    print("✨ Setup Complete!")
    print("="*80)
    print("\n📚 Next Steps:\n")
    print("1. Try the basic command:")
    print("   python main.py https://webflow.com\n")
    print("2. Generate an HTML report:")
    print("   python main.py https://webflow.com --format html --output report.html\n")
    print("3. Check the documentation:")
    print("   - USAGE.md for detailed usage")
    print("   - ARCHITECTURE.md for technical details")
    print("   - examples/ for code examples\n")
    print("4. Run the example script:")
    print("   python examples/example_usage.py\n")
    print("="*80)


def main():
    """Main setup function."""
    print("="*80)
    print("🎨 Webflow Design Scraper - Setup")
    print("="*80)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n⚠️ Some dependencies are missing. Please run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test functionality
    if not test_basic_functionality():
        print("\n⚠️ Basic functionality test failed.")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
