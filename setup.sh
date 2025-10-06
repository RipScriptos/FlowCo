#!/bin/bash

# FlowCo Setup Script
# This script helps you set up the FlowCo AI Business Evaluation System

set -e

echo "========================================="
echo "FlowCo AI Business Evaluation System"
echo "Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.10+ is available
required_version="3.10"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "⚠️  Warning: Python 3.10+ is recommended, but found $python_version"
    echo "The system may still work, but some features might not be available."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p data
mkdir -p temp
mkdir -p reports
mkdir -p templates
mkdir -p flowco/web/static/css
mkdir -p flowco/web/static/js
mkdir -p flowco/web/templates
echo "✓ Directories created"

# Check if .env file exists
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY (for GPT models)"
    echo "   - ANTHROPIC_API_KEY (for Claude models)"
    echo "   Or set USE_LOCAL_MODELS=true to use Ollama"
else
    echo ".env file already exists"
fi

# Check if config.yaml exists
echo ""
if [ ! -f "config.yaml" ]; then
    echo "Creating config.yaml from template..."
    cp config.yaml.example config.yaml
    echo "✓ config.yaml created"
else
    echo "config.yaml already exists"
fi

# Run tests
echo ""
read -p "Run tests to verify installation? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running tests..."
    pytest tests/ -v || echo "⚠️  Some tests failed, but the system may still work"
fi

echo ""
echo "========================================="
echo "✓ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run the application:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "3. Open your browser to http://localhost:12000"
echo ""
echo "For more information, see README.md"
echo ""