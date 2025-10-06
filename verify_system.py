#!/usr/bin/env python3
"""
FlowCo System Verification Script

This script verifies that all components of the FlowCo system are properly
installed and configured.
"""

import sys
import os
from pathlib import Path
import importlib.util


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_status(check_name, status, message=""):
    """Print a status message."""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} {check_name:<40} {message}")


def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version >= (3, 10):
        print_status("Python Version", True, f"v{version_str} (Recommended)")
        return True
    elif version >= (3, 9):
        print_status("Python Version", True, f"v{version_str} (Compatible)")
        return True
    else:
        print_status("Python Version", False, f"v{version_str} (Too old, need 3.9+)")
        return False


def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("Dependency Check")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("PIL", "Pillow"),
        ("cv2", "OpenCV"),
        ("jinja2", "Jinja2"),
        ("dotenv", "python-dotenv"),
        ("yaml", "PyYAML"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("sklearn", "scikit-learn"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
    ]
    
    all_installed = True
    for module_name, package_name in required_packages:
        try:
            importlib.import_module(module_name)
            print_status(package_name, True, "Installed")
        except ImportError:
            print_status(package_name, False, "Not installed")
            all_installed = False
    
    return all_installed


def check_file_structure():
    """Check if all required files and directories exist."""
    print_header("File Structure Check")
    
    base_path = Path(__file__).parent
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        ".env.example",
        "setup.sh",
        "setup.bat",
        "flowco/__init__.py",
        "flowco/core/__init__.py",
        "flowco/core/engine.py",
        "flowco/core/ai_client.py",
        "flowco/core/config.py",
        "flowco/models/__init__.py",
        "flowco/models/business.py",
        "flowco/models/evaluation.py",
        "flowco/processing/__init__.py",
        "flowco/processing/input_processor.py",
        "flowco/processing/vision_processor.py",
        "flowco/research/__init__.py",
        "flowco/research/market_analyzer.py",
        "flowco/branding/__init__.py",
        "flowco/branding/content_generator.py",
        "flowco/output/__init__.py",
        "flowco/output/report_generator.py",
        "flowco/output/template_generator.py",
        "flowco/web/__init__.py",
        "flowco/web/app.py",
        "flowco/web/api.py",
        "tests/__init__.py",
        "tests/test_basic_functionality.py",
        "examples/example_usage.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        exists = full_path.exists()
        print_status(file_path, exists)
        if not exists:
            all_exist = False
    
    return all_exist


def check_configuration():
    """Check configuration files."""
    print_header("Configuration Check")
    
    base_path = Path(__file__).parent
    
    # Check .env file
    env_file = base_path / ".env"
    if env_file.exists():
        print_status(".env file", True, "Exists")
        
        # Check if API keys are configured
        with open(env_file, 'r') as f:
            content = f.read()
            
        has_openai = "OPENAI_API_KEY=" in content and not content.count("OPENAI_API_KEY=\n")
        has_anthropic = "ANTHROPIC_API_KEY=" in content and not content.count("ANTHROPIC_API_KEY=\n")
        has_local = "USE_LOCAL_MODELS=true" in content
        
        if has_openai:
            print_status("OpenAI API Key", True, "Configured")
        else:
            print_status("OpenAI API Key", False, "Not configured")
        
        if has_anthropic:
            print_status("Anthropic API Key", True, "Configured")
        else:
            print_status("Anthropic API Key", False, "Not configured")
        
        if has_local:
            print_status("Local Models", True, "Enabled")
        else:
            print_status("Local Models", False, "Disabled")
        
        if not (has_openai or has_anthropic or has_local):
            print("\n⚠️  Warning: No AI service configured!")
            print("   Please configure at least one AI service in .env file:")
            print("   - OPENAI_API_KEY for GPT models")
            print("   - ANTHROPIC_API_KEY for Claude models")
            print("   - USE_LOCAL_MODELS=true for Ollama")
            return False
        
        return True
    else:
        print_status(".env file", False, "Not found")
        print("\n💡 Run: cp .env.example .env")
        return False


def check_imports():
    """Check if FlowCo modules can be imported."""
    print_header("Module Import Check")
    
    modules_to_check = [
        "flowco.core.config",
        "flowco.core.engine",
        "flowco.core.ai_client",
        "flowco.models.business",
        "flowco.models.evaluation",
        "flowco.processing.input_processor",
        "flowco.processing.vision_processor",
        "flowco.research.market_analyzer",
        "flowco.branding.content_generator",
        "flowco.output.report_generator",
        "flowco.output.template_generator",
        "flowco.web.app",
        "flowco.web.api",
    ]
    
    all_imported = True
    for module_name in modules_to_check:
        try:
            importlib.import_module(module_name)
            print_status(module_name, True, "OK")
        except Exception as e:
            print_status(module_name, False, f"Error: {str(e)[:30]}")
            all_imported = False
    
    return all_imported


def check_models():
    """Check if data models work correctly."""
    print_header("Data Model Check")
    
    try:
        from flowco.models.business import (
            BusinessConcept, Demographics, ProductInfo, 
            IncomeRange, BusinessCategory
        )
        
        # Test Demographics
        demographics = Demographics(
            age_min=25,
            age_max=45,
            income_range=IncomeRange.MIDDLE,
            location="Test City, USA",
            interests=["test"]
        )
        print_status("Demographics Model", True, "OK")
        
        # Test ProductInfo
        product_info = ProductInfo(
            name="TestProduct",
            description="Test description"
        )
        print_status("ProductInfo Model", True, "OK")
        
        # Test BusinessConcept
        concept = BusinessConcept(
            concept_description="Test concept",
            target_demographics=demographics,
            product_info=product_info
        )
        print_status("BusinessConcept Model", True, "OK")
        
        return True
        
    except Exception as e:
        print_status("Data Models", False, f"Error: {str(e)}")
        return False


def check_config_system():
    """Check if configuration system works."""
    print_header("Configuration System Check")
    
    try:
        from flowco.core.config import Config
        
        config = Config()
        
        # Test basic configuration access
        host = config.get("web.host")
        port = config.get("web.port")
        
        print_status("Config Loading", True, "OK")
        print_status("Web Host", True, f"{host}")
        print_status("Web Port", True, f"{port}")
        
        # Test available models
        models = config.get_available_models()
        print_status("Available Models", True, f"{len(models)} models")
        
        return True
        
    except Exception as e:
        print_status("Configuration System", False, f"Error: {str(e)}")
        return False


def run_verification():
    """Run all verification checks."""
    print("\n" + "🧠" * 30)
    print("FlowCo System Verification")
    print("🧠" * 30)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Configuration", check_configuration),
        ("Module Imports", check_imports),
        ("Data Models", check_models),
        ("Config System", check_config_system),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {str(e)}")
            results[check_name] = False
    
    # Print summary
    print_header("Verification Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        print_status(check_name, result)
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! FlowCo is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Make sure AI API keys are configured in .env")
        print("   2. Run: python main.py")
        print("   3. Open: http://localhost:12000")
        return True
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Configure .env: cp .env.example .env")
        print("   - Add API keys to .env file")
        return False


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)