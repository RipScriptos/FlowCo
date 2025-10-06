# 🧠 FlowCo - AI Business Success Evaluation System

**Comprehensive AI-powered business concept evaluation and success prediction platform**

FlowCo is a sophisticated AI system that analyzes business concepts across multiple dimensions to predict success probability, provide market insights, competitive analysis, and generate comprehensive branding recommendations. Built for cross-platform compatibility (macOS, Windows, Linux) with support for multiple AI providers.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Quick Command Reference](#-quick-command-reference)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Capabilities

- **AI-Powered Analysis**: Comprehensive business concept evaluation using advanced AI models (GPT-4, Claude, Llama)
- **Success Prediction**: Numerical scores for market demand, viability, and execution difficulty
- **Market Research**: Automated demographic analysis and location-specific demand assessment
- **Competitive Analysis**: Direct and indirect competitor identification with differentiation opportunities
- **Vision Processing**: Product image analysis with AI-powered visual insights (GPT-4 Vision, Claude Vision)
- **Branding Generation**: Complete branding recommendations including logos, colors, and messaging
- **Financial Projections**: Revenue estimates, funding requirements, and ROI analysis
- **Risk Assessment**: Comprehensive risk identification and mitigation strategies

### 📊 Analysis Dimensions

| Metric | Range | Description |
|--------|-------|-------------|
| **Overall Success Score** | 0-100 | Comprehensive probability of business success |
| **Market Demand Score** | 0-100 | Quantifies market appetite for your concept |
| **Concept Viability Score** | 0-100 | Assesses feasibility and realistic implementation |
| **Execution Difficulty Score** | 0-100 | Evaluates complexity and resource requirements |

### 🎨 Generated Outputs

- **Comprehensive Reports**: PDF, HTML, Markdown, and JSON formats
- **Landing Pages**: Professional website templates with your branding
- **Marketing Materials**: Social media content, email templates, business cards
- **Commercial Scripts**: AI-generated advertising copy
- **Brand Guidelines**: Color palettes, typography, logo concepts
- **Financial Models**: Revenue projections, cost analysis, funding roadmap

### 🔧 Technical Features

- **Multi-AI Support**: OpenAI GPT, Anthropic Claude, and local models (Ollama)
- **Cross-Platform**: Native support for macOS, Windows, and Linux
- **Web Interface**: Modern, responsive UI built with FastAPI and Bootstrap 5
- **REST API**: Complete API for integration with other systems
- **Async Processing**: Non-blocking evaluation pipeline for high performance
- **Image Processing**: Computer vision analysis with PIL, OpenCV, and scikit-image
- **Report Generation**: Professional documents with Jinja2 and WeasyPrint
- **Caching System**: In-memory caching for faster repeated evaluations

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10 or higher** (Python 3.9 works but 3.10+ recommended)
- **At least one AI service** configured:
  - OpenAI API key (recommended for best results)
  - Anthropic API key (alternative)
  - Ollama installed locally (free option)

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone https://github.com/RipScriptos/FlowCo.git
cd FlowCo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AI service
cp .env.example .env
nano .env  # Add your OpenAI API key

# 5. Run FlowCo
python main.py

# 6. Open browser
# Navigate to: http://localhost:12000
```

**That's it!** You're ready to evaluate your first business concept. 🎉

### Starting the Web UI

Once installed, start the locally hosted web server:

**macOS/Linux Terminal:**
```bash
cd FlowCo
source venv/bin/activate
python3 main.py
```

**Windows Command Prompt:**
```cmd
cd FlowCo
venv\Scripts\activate
python main.py
```

**Windows PowerShell:**
```powershell
cd FlowCo
venv\Scripts\Activate.ps1
python main.py
```

Then open your browser to: **http://localhost:12000**

To stop the server, press `CTRL+C` in the terminal.

---

## 📦 Installation

### Automated Setup (Recommended)

#### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows
```cmd
setup.bat
```

### Manual Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/RipScriptos/FlowCo.git
cd FlowCo
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python verify_system.py
```

#### Step 4: Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration file
nano .env  # or use your preferred editor
```

#### Step 5: Verify Installation
```bash
# Run verification script
python verify_system.py

# Expected output:
# ✅ Python version: 3.10.x
# ✅ All dependencies installed
# ✅ File structure complete
# ✅ Configuration files present
```

---

## ⚙️ Configuration

### Environment Variables (.env file)

Create a `.env` file in the project root:

```bash
# ============================================
# AI Service Configuration
# ============================================

# OpenAI (Recommended - Best Quality)
OPENAI_API_KEY=sk-your-openai-api-key-here
DEFAULT_AI_MODEL=gpt-4

# Anthropic Claude (Alternative)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Local Models (Free Option)
USE_LOCAL_MODELS=false
OLLAMA_BASE_URL=http://localhost:11434

# ============================================
# Server Configuration
# ============================================
WEB_HOST=0.0.0.0
WEB_PORT=12000
DEBUG=false

# ============================================
# Processing Configuration
# ============================================
MAX_IMAGE_SIZE=5242880  # 5MB
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,webp

# ============================================
# Output Configuration
# ============================================
DEFAULT_REPORT_FORMAT=pdf
ENABLE_LANDING_PAGES=true
```

### AI Provider Setup

#### Option 1: OpenAI (Recommended)

**Best for**: Highest quality results, vision analysis

1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   DEFAULT_AI_MODEL=gpt-4
   ```
3. Recommended models:
   - `gpt-4` - Best quality
   - `gpt-4-turbo` - Faster, large context
   - `gpt-3.5-turbo` - Cost-effective

#### Option 2: Anthropic Claude

**Best for**: High-quality alternative to OpenAI

1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=your-key-here
   DEFAULT_AI_MODEL=claude-3-opus-20240229
   ```
3. Available models:
   - `claude-3-opus-20240229` - Highest capability
   - `claude-3-sonnet-20240229` - Balanced
   - `claude-3-haiku-20240307` - Fast and efficient

#### Option 3: Ollama (Free, Local)

**Best for**: Free usage, privacy, offline operation

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama2
   # or: ollama pull mistral
   ```
3. Configure `.env`:
   ```bash
   USE_LOCAL_MODELS=true
   OLLAMA_BASE_URL=http://localhost:11434
   DEFAULT_AI_MODEL=llama2
   ```

### YAML Configuration (Optional)

Create `config.yaml` for advanced settings:

```yaml
# AI Configuration
ai:
  openai_api_key: "${OPENAI_API_KEY}"
  anthropic_api_key: "${ANTHROPIC_API_KEY}"
  default_model: "gpt-4"
  use_local_models: false
  ollama_base_url: "http://localhost:11434"
  
  # Model-specific settings
  temperature: 0.7
  max_tokens: 4000
  timeout: 120

# Web Server Configuration
web:
  host: "0.0.0.0"
  port: 12000
  debug: false
  workers: 1
  reload: false

# Processing Configuration
processing:
  max_image_size: 5242880  # 5MB
  supported_formats: ["jpg", "jpeg", "png", "webp"]
  enable_vision_analysis: true
  enable_opencv_analysis: true

# Output Configuration
output:
  default_format: "pdf"
  enable_landing_pages: true
  report_template: "default"
  
# Cache Configuration
cache:
  enabled: true
  ttl: 3600  # 1 hour
  max_size: 100

# Logging Configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/flowco.log"
```

---

## 📖 Usage

### Web Interface

#### 1. Start the Server

**macOS/Linux:**
```bash
# Navigate to FlowCo directory
cd /path/to/FlowCo

# Activate virtual environment
source venv/bin/activate

# Start the web server
python3 main.py
```

**Windows (Command Prompt):**
```cmd
# Navigate to FlowCo directory
cd C:\path\to\FlowCo

# Activate virtual environment
venv\Scripts\activate

# Start the web server
python main.py
```

**Windows (PowerShell):**
```powershell
# Navigate to FlowCo directory
cd C:\path\to\FlowCo

# Activate virtual environment
venv\Scripts\Activate.ps1

# Start the web server
python main.py
```

#### 2. Access the Interface
Open your browser to: **http://localhost:12000**

**Server Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:12000 (Press CTRL+C to quit)
```

#### 3. Evaluate a Business Concept

1. **Navigate to Evaluation Page**: Click "Evaluate Business" or go to `/evaluate`

2. **Fill Out the Form**:
   - **Business Concept**: Describe your business idea in detail
   - **Target Demographics**:
     - Age range (e.g., 25-45)
     - Income level (low, middle, high)
     - Location (city, state, country)
     - Interests and preferences
   - **Product Information**:
     - Product name
     - Description
     - Category
     - Key features
   - **Product Image** (optional): Upload product photo or mockup
   - **Competitive Advantages**: What makes you unique?

3. **Submit for Analysis**: Click "Evaluate" button

4. **View Results**: Comprehensive analysis including:
   - Success probability scores
   - Market insights and trends
   - Competitive landscape
   - Branding recommendations
   - Financial projections
   - Risk assessment
   - Marketing strategy

5. **Download Reports**: Get PDF, HTML, or Markdown reports

#### Example Evaluation

**Business Concept**: "A mobile app that connects local farmers directly with consumers for fresh produce delivery"

**Target Demographics**:
- Age: 25-45
- Income: Middle to high
- Location: San Francisco Bay Area
- Interests: Organic food, sustainability, local business support

**Product**: FarmConnect Mobile App
- GPS-based farmer discovery
- In-app payments
- Delivery scheduling
- Quality ratings

**Competitive Advantages**:
- Direct farmer relationships
- Fresher produce (24-hour farm-to-table)
- Lower prices (no middleman)
- Support local economy

### REST API Usage

#### Python Example

```python
import requests
import time

# Base URL
BASE_URL = "http://localhost:12000/api/v1"

# Prepare business concept data
concept_data = {
    "concept_description": "A mobile app that connects local farmers with consumers for fresh produce delivery",
    "target_demographics": {
        "age_min": 25,
        "age_max": 45,
        "income_range": "middle",
        "location": "San Francisco, CA, USA",
        "interests": ["organic food", "sustainability", "local business"]
    },
    "product_info": {
        "name": "FarmConnect",
        "description": "Mobile marketplace for local produce with same-day delivery",
        "category": "technology",
        "features": [
            "GPS-based farmer discovery",
            "In-app payments",
            "Delivery scheduling",
            "Quality ratings"
        ]
    },
    "competitive_advantages": [
        "Direct farmer relationships",
        "Fresher produce (24-hour farm-to-table)",
        "Lower prices (no middleman)"
    ]
}

# Submit evaluation
print("Submitting evaluation...")
response = requests.post(f"{BASE_URL}/evaluate", json=concept_data)
evaluation_id = response.json()["evaluation_id"]
print(f"Evaluation ID: {evaluation_id}")

# Poll for completion
print("Processing...")
while True:
    status_response = requests.get(f"{BASE_URL}/status/{evaluation_id}")
    status_data = status_response.json()
    
    print(f"Status: {status_data['status']} - Progress: {status_data.get('progress', 0)}%")
    
    if status_data["status"] == "completed":
        break
    elif status_data["status"] == "failed":
        print(f"Evaluation failed: {status_data.get('error')}")
        exit(1)
    
    time.sleep(2)

# Get results
print("\nFetching results...")
results_response = requests.get(f"{BASE_URL}/results/{evaluation_id}")
results = results_response.json()

# Display scores
print("\n=== EVALUATION RESULTS ===")
print(f"Overall Success Score: {results['overall_success_score']}/100")
print(f"Market Demand Score: {results['market_demand_score']}/100")
print(f"Concept Viability Score: {results['concept_viability_score']}/100")
print(f"Execution Difficulty Score: {results['execution_difficulty_score']}/100")

print(f"\nExecutive Summary:\n{results['executive_summary']}")

# Download PDF report
print("\nDownloading PDF report...")
pdf_response = requests.get(f"{BASE_URL}/report/{evaluation_id}?format=pdf")
with open("business_evaluation.pdf", "wb") as f:
    f.write(pdf_response.content)
print("Report saved to: business_evaluation.pdf")

# Generate landing page
print("\nGenerating landing page...")
landing_response = requests.get(f"{BASE_URL}/landing-page/{evaluation_id}")
with open("landing_page.html", "w") as f:
    f.write(landing_response.text)
print("Landing page saved to: landing_page.html")
```

#### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:12000/api/v1';

async function evaluateBusiness() {
    // Submit evaluation
    const response = await fetch(`${BASE_URL}/evaluate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            concept_description: "A mobile app for local farmers",
            target_demographics: {
                age_min: 25,
                age_max: 45,
                income_range: "middle",
                location: "San Francisco, CA",
                interests: ["organic food", "sustainability"]
            },
            product_info: {
                name: "FarmConnect",
                description: "Mobile marketplace for local produce",
                category: "technology",
                features: ["GPS discovery", "In-app payments"]
            },
            competitive_advantages: ["Direct relationships", "Fresh produce"]
        })
    });
    
    const { evaluation_id } = await response.json();
    console.log('Evaluation ID:', evaluation_id);
    
    // Poll for completion
    while (true) {
        const statusResponse = await fetch(`${BASE_URL}/status/${evaluation_id}`);
        const status = await statusResponse.json();
        
        console.log(`Status: ${status.status} - ${status.progress}%`);
        
        if (status.status === 'completed') break;
        if (status.status === 'failed') throw new Error(status.error);
        
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Get results
    const resultsResponse = await fetch(`${BASE_URL}/results/${evaluation_id}`);
    const results = await resultsResponse.json();
    
    console.log('Results:', results);
    return results;
}

evaluateBusiness().catch(console.error);
```

#### cURL Example

```bash
# Submit evaluation
curl -X POST http://localhost:12000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "concept_description": "A mobile app for local farmers",
    "target_demographics": {
      "age_min": 25,
      "age_max": 45,
      "income_range": "middle",
      "location": "San Francisco, CA",
      "interests": ["organic food"]
    },
    "product_info": {
      "name": "FarmConnect",
      "description": "Mobile marketplace",
      "category": "technology",
      "features": ["GPS", "Payments"]
    },
    "competitive_advantages": ["Direct relationships"]
  }'

# Check status
curl http://localhost:12000/api/v1/status/{evaluation_id}

# Get results
curl http://localhost:12000/api/v1/results/{evaluation_id}

# Download PDF report
curl http://localhost:12000/api/v1/report/{evaluation_id}?format=pdf \
  --output report.pdf
```

### Command Line Usage

```bash
# Start server with default settings
python main.py

# Custom host and port
python main.py --host 0.0.0.0 --port 8080

# Enable development mode with auto-reload
python main.py --reload

# Run with multiple workers (production)
python main.py --workers 4

# Use custom configuration file
python main.py --config custom_config.yaml

# Enable debug mode
python main.py --debug

# Combine options
python main.py --host 0.0.0.0 --port 8080 --workers 4 --config production.yaml
```

### Programmatic Usage

```python
from flowco.core.engine import FlowCoEngine
from flowco.models.business import BusinessConcept, TargetDemographics, ProductInfo

# Initialize engine
engine = FlowCoEngine()

# Create business concept
concept = BusinessConcept(
    concept_description="A mobile app for local farmers",
    target_demographics=TargetDemographics(
        age_min=25,
        age_max=45,
        income_range="middle",
        location="San Francisco, CA",
        interests=["organic food", "sustainability"]
    ),
    product_info=ProductInfo(
        name="FarmConnect",
        description="Mobile marketplace for local produce",
        category="technology",
        features=["GPS discovery", "In-app payments"]
    ),
    competitive_advantages=["Direct relationships", "Fresh produce"]
)

# Run evaluation (async)
import asyncio

async def evaluate():
    result = await engine.evaluate_concept(concept)
    print(f"Overall Success Score: {result.overall_success_score}")
    print(f"Market Demand Score: {result.market_demand_score}")
    print(f"Executive Summary: {result.executive_summary}")
    return result

# Run evaluation
result = asyncio.run(evaluate())
```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        FlowCo System                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │ Web Interface│      │   REST API   │                     │
│  │  (Bootstrap) │      │  (FastAPI)   │                     │
│  └──────┬───────┘      └──────┬───────┘                     │
│         │                     │                              │
│         └──────────┬──────────┘                              │
│                    │                                         │
│         ┌──────────▼──────────┐                             │
│         │   FlowCo Engine     │                             │
│         │  (Core Orchestrator)│                             │
│         └──────────┬──────────┘                             │
│                    │                                         │
│    ┌───────────────┼───────────────┐                        │
│    │               │               │                        │
│ ┌──▼───┐      ┌───▼────┐     ┌───▼────┐                   │
│ │ AI   │      │ Vision │     │ Market │                    │
│ │Client│      │Processor│    │Analyzer│                    │
│ └──┬───┘      └───┬────┘     └───┬────┘                   │
│    │              │              │                          │
│ ┌──▼──────────────▼──────────────▼────┐                   │
│ │      Branding & Content Generator    │                   │
│ └──────────────────┬───────────────────┘                   │
│                    │                                         │
│         ┌──────────▼──────────┐                             │
│         │  Report Generator   │                             │
│         │ (PDF/HTML/Markdown) │                             │
│         └─────────────────────┘                             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
FlowCo/
├── flowco/                      # Main package
│   ├── core/                    # Core components
│   │   ├── engine.py           # Main evaluation engine
│   │   ├── ai_client.py        # Multi-provider AI client
│   │   └── config.py           # Configuration management
│   │
│   ├── models/                  # Data models
│   │   ├── business.py         # Business concept models
│   │   ├── evaluation.py       # Evaluation result models
│   │   └── config.py           # Configuration models
│   │
│   ├── processing/              # Input processing
│   │   ├── input_processor.py  # Input validation
│   │   ├── text_processor.py   # Text cleaning
│   │   └── vision_processor.py # Image analysis
│   │
│   ├── research/                # Market research
│   │   ├── market_analyzer.py  # Market analysis
│   │   ├── competitor_analyzer.py # Competition research
│   │   └── trend_analyzer.py   # Trend identification
│   │
│   ├── branding/                # Branding & content
│   │   ├── content_generator.py # Content generation
│   │   ├── brand_analyzer.py   # Brand positioning
│   │   └── marketing_generator.py # Marketing materials
│   │
│   ├── output/                  # Output generation
│   │   ├── report_generator.py # Report generation
│   │   └── template_generator.py # Template rendering
│   │
│   └── web/                     # Web interface
│       ├── app.py              # FastAPI application
│       ├── api.py              # API endpoints
│       ├── static/             # Static files
│       └── templates/          # HTML templates
│
├── templates/                   # Report templates
│   ├── report_template.html    # HTML report template
│   ├── report_template.md      # Markdown template
│   └── landing_page.html       # Landing page template
│
├── tests/                       # Test suite
│   ├── test_core.py            # Core tests
│   ├── test_models.py          # Model tests
│   └── test_api.py             # API tests
│
├── examples/                    # Usage examples
│   ├── example_usage.py        # Basic usage
│   └── api_example.py          # API usage
│
├── data/                        # Data directory
│   └── cache/                  # Evaluation cache
│
├── logs/                        # Log files
│
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
├── config.yaml                  # Configuration file
├── setup.sh                     # Unix setup script
├── setup.bat                    # Windows setup script
└── verify_system.py             # Verification script
```

### Evaluation Pipeline

```
1. Input Processing
   ├── Validate business concept data
   ├── Clean and normalize text
   └── Process product images (if provided)

2. Vision Analysis (if image provided)
   ├── AI Vision Analysis (GPT-4 Vision / Claude Vision)
   ├── Computer Vision Analysis (OpenCV)
   └── Extract visual features and insights

3. Market Research
   ├── Demographic Fit Analysis
   ├── Location Demand Assessment
   ├── Market Trend Identification
   └── Market Size Estimation

4. Competitive Analysis
   ├── Identify Direct Competitors
   ├── Identify Indirect Competitors
   ├── Analyze Market Gaps
   └── Assess Differentiation Opportunities

5. Success Scoring
   ├── Calculate Market Demand Score
   ├── Calculate Concept Viability Score
   ├── Calculate Execution Difficulty Score
   └── Calculate Overall Success Score

6. Branding Generation
   ├── Brand Positioning
   ├── Messaging Strategy
   ├── Visual Identity (colors, fonts)
   └── Marketing Materials

7. Financial Projections
   ├── Revenue Estimates
   ├── Cost Analysis
   ├── Funding Requirements
   └── ROI Projections

8. Risk Assessment
   ├── Identify Key Risks
   ├── Assess Risk Severity
   └── Recommend Mitigation Strategies

9. Report Generation
   ├── Compile Analysis Results
   ├── Generate Executive Summary
   ├── Create Visualizations
   └── Export to PDF/HTML/Markdown
```

### AI Provider Integration

```python
# Multi-provider AI client with automatic fallback
class AIClient:
    def __init__(self):
        self.providers = {
            'openai': OpenAIProvider(),
            'anthropic': AnthropicProvider(),
            'ollama': OllamaProvider()
        }
    
    async def generate(self, prompt, model=None):
        # Try primary provider
        try:
            return await self.primary_provider.generate(prompt, model)
        except Exception as e:
            # Fallback to secondary provider
            return await self.fallback_provider.generate(prompt, model)
```

### Supported AI Models

#### OpenAI Models
| Model | Use Case | Context | Cost |
|-------|----------|---------|------|
| `gpt-4` | Best quality analysis | 8K tokens | $$$ |
| `gpt-4-turbo` | Fast, large context | 128K tokens | $$ |
| `gpt-3.5-turbo` | Cost-effective | 16K tokens | $ |
| `gpt-4-vision-preview` | Image analysis | 128K tokens | $$$ |

#### Anthropic Models
| Model | Use Case | Context | Cost |
|-------|----------|---------|------|
| `claude-3-opus-20240229` | Highest capability | 200K tokens | $$$ |
| `claude-3-sonnet-20240229` | Balanced | 200K tokens | $$ |
| `claude-3-haiku-20240307` | Fast & efficient | 200K tokens | $ |

#### Ollama Models (Local, Free)
| Model | Use Case | Size | Quality |
|-------|----------|------|---------|
| `llama2` | General analysis | 7B-70B | Good |
| `mistral` | Efficient analysis | 7B | Good |
| `codellama` | Technical analysis | 7B-34B | Good |

---

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: http://localhost:12000/docs
- **ReDoc**: http://localhost:12000/redoc

### API Endpoints

#### POST `/api/v1/evaluate`
**Evaluate a business concept**

**Request Body:**
```json
{
  "concept_description": "string (required)",
  "target_demographics": {
    "age_min": 18,
    "age_max": 65,
    "income_range": "low|middle|high",
    "location": "string",
    "interests": ["string"]
  },
  "product_info": {
    "name": "string",
    "description": "string",
    "category": "string",
    "features": ["string"],
    "price_point": "string (optional)"
  },
  "product_image": "base64_string (optional)",
  "competitive_advantages": ["string"]
}
```

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "processing",
  "message": "Evaluation started successfully",
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### GET `/api/v1/status/{evaluation_id}`
**Check evaluation status**

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "processing|completed|failed",
  "progress": 75,
  "current_stage": "market_analysis",
  "created_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:05:00Z"
}
```

#### GET `/api/v1/results/{evaluation_id}`
**Get evaluation results**

**Response:**
```json
{
  "evaluation_id": "uuid",
  "overall_success_score": 78.5,
  "market_demand_score": 82.0,
  "concept_viability_score": 75.0,
  "execution_difficulty_score": 65.0,
  "executive_summary": "Your business concept shows strong potential...",
  "market_insights": {
    "market_size": "Large regional market ($50M+)",
    "competition_level": "medium",
    "demographic_fit_score": 85.0,
    "location_demand_score": 80.0,
    "trends": ["Growing demand for local produce", "Sustainability focus"]
  },
  "competitive_analysis": {
    "direct_competitors": ["Competitor A", "Competitor B"],
    "indirect_competitors": ["Alternative C"],
    "market_gaps": ["Gap 1", "Gap 2"],
    "differentiation_opportunities": ["Opportunity 1"]
  },
  "branding_recommendations": {
    "brand_positioning": "Premium local marketplace",
    "target_messaging": "Fresh from farm to table",
    "color_palette": ["#2E7D32", "#FFA726"],
    "logo_concepts": ["Concept 1", "Concept 2"]
  },
  "financial_projections": {
    "estimated_revenue_year1": 500000,
    "estimated_costs_year1": 300000,
    "funding_required": 200000,
    "break_even_months": 18
  },
  "key_recommendations": [
    "Focus on mobile-first user experience",
    "Develop partnerships with local farmers",
    "Implement quality rating system"
  ],
  "risk_assessment": {
    "high_risks": ["Market competition", "Farmer adoption"],
    "medium_risks": ["Logistics complexity"],
    "low_risks": ["Technology implementation"]
  }
}
```

#### GET `/api/v1/report/{evaluation_id}`
**Download evaluation report**

**Query Parameters:**
- `format`: Report format (`pdf`, `html`, `markdown`, `json`)

**Response:** File download

**Example:**
```bash
curl http://localhost:12000/api/v1/report/{evaluation_id}?format=pdf \
  --output report.pdf
```

#### GET `/api/v1/landing-page/{evaluation_id}`
**Generate landing page HTML**

**Response:** HTML content with embedded branding and marketing content

#### GET `/api/v1/health`
**Health check endpoint**

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "ai_providers": {
    "openai": "available",
    "anthropic": "not_configured",
    "ollama": "not_available"
  }
}
```

### Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message describing what went wrong",
  "status_code": 400,
  "error_type": "validation_error|not_found|server_error"
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (evaluation ID not found)
- `500`: Internal Server Error
- `503`: Service Unavailable (AI provider error)

---

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/RipScriptos/FlowCo.git
cd FlowCo

# Create development environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black flake8 mypy

# Run in development mode
python main.py --reload --debug
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flowco --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::test_engine_initialization

# Run with verbose output
pytest -v

# Run async tests
pytest -v tests/test_async.py
```

### Code Quality

```bash
# Format code with Black
black flowco/

# Check code style with Flake8
flake8 flowco/ --max-line-length=100

# Type checking with mypy
mypy flowco/

# Run all quality checks
black flowco/ && flake8 flowco/ && mypy flowco/ && pytest
```

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test Changes**
   ```bash
   pytest
   black flowco/
   flake8 flowco/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Adding New AI Providers

```python
# flowco/core/ai_providers/custom_provider.py

from flowco.core.ai_client import AIProvider

class CustomProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = CustomAIClient(api_key)
    
    async def generate(self, prompt: str, model: str = None) -> str:
        response = await self.client.complete(
            prompt=prompt,
            model=model or "default-model"
        )
        return response.text
    
    async def generate_with_vision(self, prompt: str, image: bytes) -> str:
        # Implement vision analysis
        pass

# Register in ai_client.py
from flowco.core.ai_providers.custom_provider import CustomProvider

class AIClient:
    def __init__(self):
        self.providers['custom'] = CustomProvider(api_key)
```

### Adding Custom Report Templates

```html
<!-- templates/custom_report.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ business_name }} - Evaluation Report</title>
    <style>
        /* Your custom styles */
    </style>
</head>
<body>
    <h1>{{ business_name }}</h1>
    <h2>Overall Success Score: {{ overall_success_score }}/100</h2>
    
    <!-- Your custom template content -->
    
    {% for recommendation in key_recommendations %}
    <li>{{ recommendation }}</li>
    {% endfor %}
</body>
</html>
```

---

## 🚀 Deployment

### Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data /app/logs

# Expose port
EXPOSE 12000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WEB_HOST=0.0.0.0
ENV WEB_PORT=12000

# Run application
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "12000"]
```

#### Build and Run

```bash
# Build image
docker build -t flowco:latest .

# Run container
docker run -d \
  --name flowco \
  -p 12000:12000 \
  -e OPENAI_API_KEY=your-key-here \
  -v $(pwd)/data:/app/data \
  flowco:latest

# View logs
docker logs -f flowco

# Stop container
docker stop flowco
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  flowco:
    build: .
    ports:
      - "12000:12000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - WEB_HOST=0.0.0.0
      - WEB_PORT=12000
      - DEBUG=false
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Server (Gunicorn + Nginx)

#### Install Gunicorn

```bash
pip install gunicorn uvicorn[standard]
```

#### Run with Gunicorn

```bash
# Basic
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  flowco.web.app:app \
  --bind 0.0.0.0:12000

# With configuration
gunicorn -c gunicorn_config.py flowco.web.app:app
```

#### Gunicorn Configuration

```python
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:12000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "flowco"

# Server mechanics
daemon = False
pidfile = "flowco.pid"
```

#### Nginx Configuration

```nginx
# /etc/nginx/sites-available/flowco
server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static {
        alias /path/to/FlowCo/flowco/web/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:12000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

#### Enable Nginx Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/flowco /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Systemd Service

```ini
# /etc/systemd/system/flowco.service
[Unit]
Description=FlowCo AI Business Evaluation System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/FlowCo
Environment="PATH=/path/to/FlowCo/venv/bin"
Environment="OPENAI_API_KEY=your-key-here"
ExecStart=/path/to/FlowCo/venv/bin/gunicorn \
    -c gunicorn_config.py \
    flowco.web.app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable flowco
sudo systemctl start flowco

# Check status
sudo systemctl status flowco

# View logs
sudo journalctl -u flowco -f
```

### Environment Variables for Production

```bash
# Production .env
OPENAI_API_KEY=your-production-key
ANTHROPIC_API_KEY=your-production-key

WEB_HOST=0.0.0.0
WEB_PORT=12000
DEBUG=false

MAX_IMAGE_SIZE=10485760  # 10MB
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,webp

LOG_LEVEL=INFO
LOG_FILE=/var/log/flowco/flowco.log

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ORIGINS=https://your-domain.com

# Performance
WORKERS=4
WORKER_TIMEOUT=120
KEEP_ALIVE=5
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Dependencies Installation Fails

**Problem**: `pip install -r requirements.txt` fails

**Solutions**:
```bash
# Update pip
pip install --upgrade pip

# Install build tools (macOS)
xcode-select --install

# Install build tools (Ubuntu/Debian)
sudo apt-get install python3-dev build-essential

# Install build tools (Windows)
# Download and install Microsoft C++ Build Tools
```

#### 2. OpenAI API Key Not Working

**Problem**: "Invalid API key" error

**Solutions**:
- Verify API key is correct in `.env` file
- Check for extra spaces or quotes
- Ensure API key has sufficient credits
- Test API key:
  ```bash
  curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer YOUR_API_KEY"
  ```

#### 3. Port Already in Use

**Problem**: "Address already in use" error

**Solutions**:
```bash
# Find process using port 12000
lsof -i :12000  # macOS/Linux
netstat -ano | findstr :12000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
python main.py --port 8080
```

#### 4. Module Import Errors

**Problem**: "ModuleNotFoundError" when running

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python verify_system.py
```

#### 5. Image Processing Fails

**Problem**: Vision analysis not working

**Solutions**:
- Ensure image is in supported format (JPG, PNG, WEBP)
- Check image size (max 5MB by default)
- Verify AI provider supports vision:
  - OpenAI: Use `gpt-4-vision-preview`
  - Anthropic: Use `claude-3-opus-20240229`
  - Ollama: Vision not supported
- Test with smaller image

#### 6. Slow Evaluation Performance

**Problem**: Evaluations take too long

**Solutions**:
- Use faster AI models:
  - OpenAI: `gpt-3.5-turbo` instead of `gpt-4`
  - Anthropic: `claude-3-haiku` instead of `claude-3-opus`
- Disable vision analysis if not needed
- Increase timeout in config:
  ```yaml
  ai:
    timeout: 180  # 3 minutes
  ```
- Run with multiple workers:
  ```bash
  python main.py --workers 4
  ```

#### 7. PDF Generation Fails

**Problem**: "WeasyPrint error" when generating PDF

**Solutions**:
```bash
# Install system dependencies

# macOS
brew install cairo pango gdk-pixbuf libffi

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0

# Windows
# Download GTK3 runtime from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
```

### Debug Mode

Enable debug mode for detailed error messages:

```bash
# Command line
python main.py --debug

# Environment variable
export DEBUG=true
python main.py

# In code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Logging

Check logs for detailed error information:

```bash
# View logs
tail -f logs/flowco.log

# Search for errors
grep ERROR logs/flowco.log

# View last 100 lines
tail -n 100 logs/flowco.log
```

### Getting Help

1. **Check Documentation**:
   - README.md (this file)
   - QUICKSTART.md
   - GET_STARTED.md

2. **Run Verification Script**:
   ```bash
   python verify_system.py
   ```

3. **Check System Status**:
   ```bash
   curl http://localhost:12000/api/v1/health
   ```

4. **Report Issues**:
   - GitHub Issues: https://github.com/RipScriptos/FlowCo/issues
   - Include:
     - Error message
     - Python version
     - Operating system
     - Steps to reproduce

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- **Report Bugs**: Submit detailed bug reports
- **Suggest Features**: Propose new features or improvements
- **Improve Documentation**: Fix typos, add examples, clarify instructions
- **Submit Code**: Fix bugs, add features, improve performance
- **Write Tests**: Increase test coverage
- **Share Feedback**: Tell us about your experience

### Development Workflow

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR_USERNAME/FlowCo.git
   cd FlowCo
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

4. **Test Changes**
   ```bash
   pytest
   black flowco/
   flake8 flowco/
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: amazing feature description"
   ```

6. **Push to GitHub**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Describe your changes
   - Submit for review

### Commit Message Guidelines

Use conventional commit format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: add support for Google Gemini AI provider
fix: resolve PDF generation error on Windows
docs: update installation instructions for macOS
test: add tests for market analyzer
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Maximum line length: 100 characters
- Use type hints
- Write docstrings for functions and classes

```python
def evaluate_concept(
    concept: BusinessConcept,
    use_vision: bool = True
) -> EvaluationResult:
    """
    Evaluate a business concept and return success scores.
    
    Args:
        concept: Business concept to evaluate
        use_vision: Whether to use vision analysis for product images
        
    Returns:
        EvaluationResult containing scores and insights
        
    Raises:
        ValueError: If concept data is invalid
        AIProviderError: If AI service fails
    """
    pass
```

### Testing Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Use pytest for testing
- Test both success and failure cases

```python
import pytest
from flowco.core.engine import FlowCoEngine

def test_engine_initialization():
    """Test that engine initializes correctly."""
    engine = FlowCoEngine()
    assert engine is not None
    assert engine.ai_client is not None

@pytest.mark.asyncio
async def test_concept_evaluation():
    """Test business concept evaluation."""
    engine = FlowCoEngine()
    concept = create_test_concept()
    result = await engine.evaluate_concept(concept)
    assert result.overall_success_score >= 0
    assert result.overall_success_score <= 100
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 FlowCo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

FlowCo is built with amazing open-source technologies:

### AI Providers
- **OpenAI** - GPT models and vision capabilities
- **Anthropic** - Claude models
- **Ollama** - Local model support

### Core Technologies
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Jinja2** - Template engine

### Processing & Analysis
- **Pillow (PIL)** - Image processing
- **OpenCV** - Computer vision
- **scikit-image** - Image analysis
- **NumPy** - Numerical computing

### Report Generation
- **WeasyPrint** - PDF generation
- **Markdown** - Markdown processing
- **Bootstrap** - UI framework

### Development Tools
- **pytest** - Testing framework
- **Black** - Code formatter
- **Flake8** - Linter
- **mypy** - Type checker

### Special Thanks
- The open-source community for countless libraries and tools
- Contributors and users who provide feedback and improvements
- AI research community for advancing the field

---

## 📞 Support & Resources

### Documentation
- **README.md** - Complete documentation (this file)
- **QUICKSTART.md** - Quick start guide
- **GET_STARTED.md** - 5-minute getting started
- **SYSTEM_STATUS.md** - System overview
- **API Documentation** - http://localhost:12000/docs

### Community
- **GitHub Repository**: https://github.com/RipScriptos/FlowCo
- **Issues**: https://github.com/RipScriptos/FlowCo/issues
- **Discussions**: https://github.com/RipScriptos/FlowCo/discussions
- **Wiki**: https://github.com/RipScriptos/FlowCo/wiki

### Getting Help

1. **Check Documentation**: Start with GET_STARTED.md
2. **Run Verification**: `python verify_system.py`
3. **Search Issues**: Check if your issue is already reported
4. **Ask Questions**: Use GitHub Discussions
5. **Report Bugs**: Create a detailed issue report

### Stay Updated

- **Watch Repository**: Get notified of new releases
- **Star Project**: Show your support
- **Follow Updates**: Check releases for new features

---

## 🎯 What's Next?

### Roadmap

#### Version 1.1 (Coming Soon)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Multi-user support
- [ ] Evaluation history and comparison
- [ ] Advanced analytics dashboard

#### Version 1.2
- [ ] Additional AI providers (Google Gemini, Cohere)
- [ ] Custom report templates
- [ ] Batch evaluation support
- [ ] API rate limiting
- [ ] Webhook notifications

#### Version 2.0
- [ ] Real-time collaboration
- [ ] Team workspaces
- [ ] Advanced financial modeling
- [ ] Integration marketplace
- [ ] Mobile app

### Feature Requests

Have an idea? We'd love to hear it!
- Submit feature requests on GitHub Issues
- Vote on existing feature requests
- Contribute code for new features

---

## ⚡ Quick Command Reference

### Start Web UI (Locally Hosted Server)

| Platform | Commands |
|----------|----------|
| **macOS/Linux** | `cd FlowCo`<br>`source venv/bin/activate`<br>`python3 main.py` |
| **Windows (CMD)** | `cd FlowCo`<br>`venv\Scripts\activate`<br>`python main.py` |
| **Windows (PowerShell)** | `cd FlowCo`<br>`venv\Scripts\Activate.ps1`<br>`python main.py` |

**Access**: Open browser to http://localhost:12000  
**Stop Server**: Press `CTRL+C` in terminal

### Common Commands

**macOS/Linux:**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Verify system
python3 verify_system.py

# Run with custom port
python3 main.py --port 8080

# Run in development mode (auto-reload)
python3 main.py --reload

# Run tests
pytest

# View help
python3 main.py --help
```

**Windows:**
```cmd
# Install dependencies
pip install -r requirements.txt

# Verify system
python verify_system.py

# Run with custom port
python main.py --port 8080

# Run in development mode (auto-reload)
python main.py --reload

# Run tests
pytest

# View help
python main.py --help
```

---

## 🚀 Quick Links

- **Get Started**: [GET_STARTED.md](GET_STARTED.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **API Docs**: http://localhost:12000/docs
- **Examples**: [examples/](examples/)
- **Tests**: [tests/](tests/)
- **Issues**: https://github.com/RipScriptos/FlowCo/issues

---

<div align="center">

**FlowCo** - Empowering entrepreneurs with AI-driven business insights 🚀

Made with ❤️ by the FlowCo Team

[Get Started](GET_STARTED.md) • [Documentation](#) • [API Reference](http://localhost:12000/docs) • [GitHub](https://github.com/RipScriptos/FlowCo)

</div>