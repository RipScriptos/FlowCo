# 🚀 FlowCo Quick Start Guide

Get up and running with FlowCo AI Business Evaluation System in minutes!

## Prerequisites

- **Python 3.10+** (Python 3.9 may work but 3.10+ is recommended)
- **At least one AI service**:
  - OpenAI API key (recommended for best results)
  - Anthropic API key (alternative)
  - Ollama installed locally (free, offline option)

## Installation

### Option 1: Automated Setup (Recommended)

#### macOS/Linux:
```bash
./setup.sh
```

#### Windows:
```cmd
setup.bat
```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   
   # Activate on Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Configuration

### OpenAI Setup (Recommended)

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   DEFAULT_AI_MODEL=gpt-4
   ```

### Anthropic Setup (Alternative)

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Edit `.env` file:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-api-key-here
   DEFAULT_AI_MODEL=claude-3-sonnet-20240229
   ```

### Local Models Setup (Free, Offline)

1. Install [Ollama](https://ollama.ai/)
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. Edit `.env` file:
   ```bash
   USE_LOCAL_MODELS=true
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## Running FlowCo

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Access the web interface:**
   Open your browser to: `http://localhost:12000`

3. **Start evaluating!**
   - Click "Evaluate Business" in the navigation
   - Fill out the form with your business concept
   - Upload a product image (optional)
   - Submit and wait for AI analysis

## Example Usage

### Via Web Interface

1. Navigate to `http://localhost:12000/evaluate`
2. Fill in the form:
   - **Business Concept**: "A mobile app connecting local farmers with consumers"
   - **Product Name**: "FarmConnect"
   - **Target Age**: 25-45
   - **Income Range**: Middle
   - **Location**: "San Francisco, CA"
   - **Interests**: "organic food, sustainability"
3. Click "Evaluate"
4. View comprehensive results including:
   - Success probability scores
   - Market analysis
   - Competitive landscape
   - Branding recommendations
   - Financial projections

### Via API

```python
import requests

# Submit evaluation
response = requests.post("http://localhost:12000/api/v1/evaluate", json={
    "concept_description": "A mobile app connecting local farmers with consumers",
    "target_demographics": {
        "age_min": 25,
        "age_max": 45,
        "income_range": "middle",
        "location": "San Francisco, CA",
        "interests": ["organic food", "sustainability"]
    },
    "product_info": {
        "name": "FarmConnect",
        "description": "Mobile marketplace for local produce",
        "category": "technology",
        "features": ["GPS-based farmer discovery", "In-app payments"]
    },
    "competitive_advantages": ["Direct farmer relationships", "Fresher produce"]
})

evaluation_id = response.json()["evaluation_id"]

# Check status
status = requests.get(f"http://localhost:12000/api/v1/status/{evaluation_id}")
print(status.json())

# Get results (when completed)
results = requests.get(f"http://localhost:12000/api/v1/results/{evaluation_id}")
print(results.json())

# Download PDF report
pdf = requests.get(f"http://localhost:12000/api/v1/report/{evaluation_id}?format=pdf")
with open("report.pdf", "wb") as f:
    f.write(pdf.content)
```

## Command Line Options

```bash
# Custom host and port
python main.py --host 0.0.0.0 --port 8080

# Development mode with auto-reload
python main.py --reload

# Multiple workers (production)
python main.py --workers 4

# Custom configuration file
python main.py --config custom_config.yaml
```

## Troubleshooting

### "No AI service available" error

**Solution**: Make sure you've configured at least one AI service in your `.env` file:
- Add `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Or set `USE_LOCAL_MODELS=true` and install Ollama

### Import errors

**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port already in use

**Solution**: Use a different port:
```bash
python main.py --port 8080
```

### Image processing errors

**Solution**: Make sure image processing libraries are installed:
```bash
pip install Pillow opencv-python scikit-image
```

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Customize settings in `config.yaml`
- 🧪 Run tests: `pytest tests/`
- 📊 Explore the API documentation at `http://localhost:12000/docs`
- 🎨 Customize templates in the `templates/` directory

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review example usage in `examples/example_usage.py`
- Open an issue on GitHub for bugs or feature requests

## Key Features to Try

1. **Image Analysis**: Upload a product image to get AI-powered visual insights
2. **Market Research**: Get location-specific demand analysis
3. **Competitive Analysis**: Identify competitors and market gaps
4. **Branding**: Generate logo concepts, color palettes, and marketing materials
5. **Financial Projections**: Get revenue estimates and funding recommendations
6. **Reports**: Download comprehensive reports in PDF, HTML, or Markdown

---

**Happy Evaluating! 🚀**