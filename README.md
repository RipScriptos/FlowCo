# 🧠 FlowCo - AI Business Success Evaluation System

**Comprehensive AI-powered business concept evaluation and success prediction platform**

FlowCo is a sophisticated AI system that analyzes business concepts across multiple dimensions to predict success probability, provide market insights, competitive analysis, and generate comprehensive branding recommendations. Built for cross-platform compatibility (macOS, Windows, Linux) with support for multiple AI providers.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🎯 Core Capabilities
- **AI-Powered Analysis**: Comprehensive business concept evaluation using advanced AI models
- **Success Prediction**: Numerical scores for market demand, viability, and execution difficulty
- **Market Research**: Automated demographic analysis and location-specific demand assessment
- **Competitive Analysis**: Direct and indirect competitor identification with differentiation opportunities
- **Vision Processing**: Product image analysis with AI-powered visual insights
- **Branding Generation**: Complete branding recommendations including logos, colors, and messaging

### 📊 Analysis Dimensions
- **Market Demand Score** (0-100): Quantifies market appetite for your concept
- **Concept Viability Score** (0-100): Assesses feasibility and realistic implementation
- **Execution Difficulty Score** (0-100): Evaluates complexity and resource requirements
- **Overall Success Score** (0-100): Comprehensive probability of business success

### 🎨 Generated Outputs
- **Comprehensive Reports**: PDF, HTML, Markdown, and JSON formats
- **Landing Pages**: Professional website templates with your branding
- **Marketing Materials**: Social media content, email templates, business cards
- **Commercial Scripts**: AI-generated advertising copy
- **Financial Projections**: Revenue estimates and funding recommendations

### 🔧 Technical Features
- **Multi-AI Support**: OpenAI GPT, Anthropic Claude, and local models (Ollama)
- **Cross-Platform**: Native support for macOS, Windows, and Linux
- **Web Interface**: Modern, responsive UI built with FastAPI and Bootstrap
- **REST API**: Complete API for integration with other systems
- **Image Processing**: Computer vision analysis with PIL and OpenCV
- **Report Generation**: Professional documents with Jinja2 and WeasyPrint

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- At least one AI service configured (OpenAI, Anthropic, or Ollama)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RipScriptos/FlowCo.git
   cd FlowCo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AI services**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env file with your API keys
   nano .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the web interface**
   Open your browser to `http://localhost:12000`

### Configuration Options

#### Environment Variables (.env file)
```bash
# AI Service Configuration
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
DEFAULT_AI_MODEL=gpt-3.5-turbo

# Local Models (optional)
USE_LOCAL_MODELS=false
OLLAMA_BASE_URL=http://localhost:11434

# Server Configuration
WEB_HOST=0.0.0.0
WEB_PORT=12000
DEBUG=false
```

#### YAML Configuration (config.yaml)
```yaml
ai:
  openai_api_key: "your-key-here"
  anthropic_api_key: "your-key-here"
  default_model: "gpt-3.5-turbo"
  use_local_models: false

web:
  host: "0.0.0.0"
  port: 12000
  debug: false

processing:
  max_image_size: 5242880  # 5MB
  supported_formats: ["jpg", "jpeg", "png", "webp"]
```

## 📖 Usage

### Web Interface

1. **Navigate to the evaluation page** at `http://localhost:12000/evaluate`
2. **Fill out the business concept form**:
   - Business concept description
   - Target demographics (age, income, location, interests)
   - Product information (name, description, features)
   - Optional product image upload
   - Competitive advantages
3. **Submit for analysis** - The AI will process your concept
4. **View comprehensive results** including:
   - Success probability scores
   - Market insights and trends
   - Competitive analysis
   - Branding recommendations
   - Financial projections
   - Risk assessment

### API Usage

#### Evaluate Business Concept
```python
import requests

# Prepare business concept data
concept_data = {
    "concept_description": "A mobile app that connects local farmers with consumers",
    "target_demographics": {
        "age_min": 25,
        "age_max": 45,
        "income_range": "middle",
        "location": "San Francisco, CA, USA",
        "interests": ["organic food", "sustainability", "local business"]
    },
    "product_info": {
        "name": "FarmConnect",
        "description": "Mobile marketplace for local produce",
        "category": "technology",
        "features": ["GPS-based farmer discovery", "In-app payments", "Delivery scheduling"]
    },
    "competitive_advantages": ["Direct farmer relationships", "Fresher produce", "Lower prices"]
}

# Submit evaluation
response = requests.post("http://localhost:12000/api/v1/evaluate", json=concept_data)
evaluation_id = response.json()["evaluation_id"]

# Check status
status_response = requests.get(f"http://localhost:12000/api/v1/status/{evaluation_id}")
print(status_response.json())

# Get results (when completed)
results_response = requests.get(f"http://localhost:12000/api/v1/results/{evaluation_id}")
results = results_response.json()
```

#### Download Reports
```python
# Download PDF report
pdf_response = requests.get(f"http://localhost:12000/api/v1/report/{evaluation_id}?format=pdf")
with open("business_evaluation.pdf", "wb") as f:
    f.write(pdf_response.content)

# Generate landing page
landing_response = requests.get(f"http://localhost:12000/api/v1/landing-page/{evaluation_id}")
with open("landing_page.html", "w") as f:
    f.write(landing_response.text)
```

### Command Line Usage

```bash
# Start server with custom configuration
python main.py --host 0.0.0.0 --port 8080 --config config.yaml

# Enable development mode with auto-reload
python main.py --reload

# Run with multiple workers (production)
python main.py --workers 4
```

## 🏗️ Architecture

### System Components

```
FlowCo/
├── flowco/
│   ├── core/           # Core engine and AI client
│   ├── models/         # Data models and schemas
│   ├── processing/     # Input and image processing
│   ├── research/       # Market analysis and research
│   ├── branding/       # Content and branding generation
│   ├── output/         # Report and template generation
│   └── web/           # Web interface and API
├── templates/         # Report and web templates
├── data/             # Database and cache files
├── examples/         # Usage examples
└── docs/            # Documentation
```

### AI Pipeline

1. **Input Processing**: Validates and normalizes business concept data
2. **Vision Analysis**: Processes product images using AI vision models
3. **Market Research**: Analyzes demographics, location demand, and trends
4. **Competitive Analysis**: Identifies competitors and market gaps
5. **Success Scoring**: Calculates probability scores using AI evaluation
6. **Branding Generation**: Creates marketing materials and recommendations
7. **Report Generation**: Compiles comprehensive analysis reports

### Supported AI Models

#### OpenAI Models
- **GPT-4**: Advanced reasoning and analysis
- **GPT-4 Turbo**: Faster processing with large context
- **GPT-3.5 Turbo**: Cost-effective general analysis
- **GPT-4 Vision**: Image analysis and product evaluation

#### Anthropic Models
- **Claude-3 Opus**: Highest capability model
- **Claude-3 Sonnet**: Balanced performance and speed
- **Claude-3 Haiku**: Fast and efficient processing

#### Local Models (Ollama)
- **Llama 2**: Open-source language model
- **Mistral**: Efficient multilingual model
- **CodeLlama**: Specialized for technical analysis

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/RipScriptos/FlowCo.git
cd FlowCo

# Create development environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8

# Run in development mode
python main.py --reload --debug
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flowco

# Run specific test file
pytest tests/test_core.py
```

### Code Formatting

```bash
# Format code with Black
black flowco/

# Check code style with Flake8
flake8 flowco/
```

### Project Structure

```
flowco/
├── core/
│   ├── __init__.py
│   ├── engine.py          # Main evaluation engine
│   ├── ai_client.py       # AI service client
│   └── config.py          # Configuration management
├── models/
│   ├── __init__.py
│   ├── business.py        # Business concept models
│   └── evaluation.py      # Evaluation result models
├── processing/
│   ├── __init__.py
│   ├── input_processor.py # Input validation and processing
│   └── vision_processor.py # Image analysis
├── research/
│   ├── __init__.py
│   └── market_analyzer.py # Market research and analysis
├── branding/
│   ├── __init__.py
│   └── content_generator.py # Branding and content generation
├── output/
│   ├── __init__.py
│   ├── report_generator.py # Report generation
│   └── template_generator.py # Website template generation
└── web/
    ├── __init__.py
    ├── app.py             # FastAPI application
    ├── api.py             # API endpoints
    ├── static/            # Static files (CSS, JS)
    └── templates/         # HTML templates
```

## 📚 API Documentation

### Endpoints

#### POST `/api/v1/evaluate`
Evaluate a business concept

**Request Body:**
```json
{
  "concept_description": "string",
  "target_demographics": {
    "age_min": 25,
    "age_max": 45,
    "income_range": "middle",
    "location": "San Francisco, CA",
    "interests": ["technology", "sustainability"]
  },
  "product_info": {
    "name": "ProductName",
    "description": "Product description",
    "category": "technology",
    "features": ["feature1", "feature2"]
  },
  "competitive_advantages": ["advantage1", "advantage2"]
}
```

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "processing",
  "message": "Evaluation started"
}
```

#### GET `/api/v1/status/{evaluation_id}`
Check evaluation status

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-01T12:00:00",
  "completed_at": "2024-01-01T12:05:00"
}
```

#### GET `/api/v1/results/{evaluation_id}`
Get evaluation results

**Response:**
```json
{
  "overall_success_score": 78.5,
  "market_demand_score": 82.0,
  "concept_viability_score": 75.0,
  "execution_difficulty_score": 65.0,
  "executive_summary": "Your business concept shows strong potential...",
  "market_insights": {
    "market_size": "Large regional market ($50M+)",
    "competition_level": "medium",
    "demographic_fit_score": 85.0
  },
  "key_recommendations": [
    "Focus on mobile-first user experience",
    "Develop partnerships with local farmers"
  ]
}
```

#### GET `/api/v1/report/{evaluation_id}?format=pdf`
Download evaluation report

**Query Parameters:**
- `format`: Report format (`pdf`, `html`, `markdown`, `json`)

**Response:** File download

#### GET `/api/v1/landing-page/{evaluation_id}`
Generate landing page HTML

**Response:** HTML content

### Error Responses

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## 🔒 Security Considerations

### API Keys
- Store API keys in environment variables or secure configuration files
- Never commit API keys to version control
- Use different keys for development and production
- Regularly rotate API keys

### Data Privacy
- Business concept data is processed in memory and not permanently stored by default
- Image uploads are temporarily stored and should be cleaned up
- Consider implementing data retention policies
- Use HTTPS in production environments

### Production Deployment
- Set `DEBUG=false` in production
- Configure proper CORS settings
- Use a reverse proxy (nginx) for static files
- Implement rate limiting for API endpoints
- Set up proper logging and monitoring

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 12000

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "12000"]
```

```bash
# Build and run
docker build -t flowco .
docker run -p 12000:12000 -e OPENAI_API_KEY=your-key flowco
```

### Production Server

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker flowco.web.app:create_app --bind 0.0.0.0:12000
```

### Environment Variables for Production

```bash
export OPENAI_API_KEY=your-production-key
export WEB_HOST=0.0.0.0
export WEB_PORT=12000
export DEBUG=false
export DATABASE_PATH=/data/flowco.db
export LOG_LEVEL=INFO
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Format code with Black
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Reporting Issues

Please use the [GitHub Issues](https://github.com/RipScriptos/FlowCo/issues) page to report bugs or request features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models and vision capabilities
- Anthropic for Claude models
- Ollama for local model support
- FastAPI for the excellent web framework
- The open-source community for various libraries and tools

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/RipScriptos/FlowCo/wiki)
- **Issues**: [GitHub Issues](https://github.com/RipScriptos/FlowCo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RipScriptos/FlowCo/discussions)

---

**FlowCo** - Empowering entrepreneurs with AI-driven business insights 🚀
