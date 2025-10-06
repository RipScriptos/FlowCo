# 🚀 Get Started with FlowCo in 5 Minutes

Welcome to **FlowCo** - Your AI-powered business success evaluation system!

---

## ⚡ Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# 3. Run FlowCo
python main.py
```

Then open: **http://localhost:12000** 🎉

---

## 📋 What You Need

### Required
- **Python 3.9+** (check with `python3 --version`)
- **One AI Service** (choose one):
  - OpenAI API key (recommended) - Get it at [platform.openai.com](https://platform.openai.com/api-keys)
  - Anthropic API key - Get it at [console.anthropic.com](https://console.anthropic.com/)
  - Ollama installed (free, offline) - Get it at [ollama.ai](https://ollama.ai/)

### Optional
- Virtual environment (recommended)
- Docker (for containerized deployment)

---

## 🎯 Step-by-Step Setup

### Step 1: Get the Code
You already have it! You're in the FlowCo directory.

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages (takes 2-3 minutes).

### Step 4: Configure Your AI Service

#### Option A: OpenAI (Recommended)
```bash
# Copy the example config
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor

# Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
DEFAULT_AI_MODEL=gpt-4
```

#### Option B: Anthropic Claude
```bash
# Edit .env file
nano .env

# Add your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
DEFAULT_AI_MODEL=claude-3-sonnet-20240229
```

#### Option C: Local Models (Free, No API Key)
```bash
# Install Ollama first: https://ollama.ai/

# Pull a model
ollama pull llama2

# Edit .env file
nano .env

# Enable local models
USE_LOCAL_MODELS=true
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 5: Run FlowCo
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:12000
```

### Step 6: Open Your Browser
Navigate to: **http://localhost:12000**

---

## 🎨 Your First Evaluation

### Using the Web Interface

1. **Click "Evaluate Business"** in the navigation menu

2. **Fill out the form:**
   - **Business Concept**: "A mobile app that connects local farmers with consumers for fresh produce delivery"
   - **Product Name**: "FarmConnect"
   - **Product Description**: "Mobile marketplace for local produce with same-day delivery"
   - **Category**: Technology
   - **Target Age**: 25-45
   - **Income Range**: Middle
   - **Location**: "San Francisco, CA"
   - **Interests**: "organic food, sustainability, local business"
   - **Features**: "GPS farmer discovery, In-app payments, Delivery scheduling"
   - **Competitive Advantages**: "Direct farmer relationships, 24-hour freshness guarantee"

3. **Click "Evaluate"**

4. **Wait 30-60 seconds** for AI analysis

5. **View your results!** You'll see:
   - ✅ Overall Success Score
   - ✅ Market Demand Score
   - ✅ Concept Viability Score
   - ✅ Execution Difficulty Score
   - ✅ Market Insights
   - ✅ Competitive Analysis
   - ✅ Branding Recommendations
   - ✅ Financial Projections
   - ✅ Risk Assessment
   - ✅ Next Steps

6. **Download Reports** in PDF, HTML, or Markdown format

---

## 🔧 Using the API

### Python Example
```python
import requests
import time

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

# Get evaluation ID
evaluation_id = response.json()["evaluation_id"]
print(f"Evaluation ID: {evaluation_id}")

# Wait for completion
while True:
    status = requests.get(f"http://localhost:12000/api/v1/status/{evaluation_id}")
    if status.json()["status"] == "completed":
        break
    time.sleep(2)

# Get results
results = requests.get(f"http://localhost:12000/api/v1/results/{evaluation_id}")
data = results.json()

print(f"\n🎯 Overall Success Score: {data['overall_success_score']}/100")
print(f"📊 Market Demand: {data['market_demand_score']}/100")
print(f"✅ Viability: {data['concept_viability_score']}/100")
print(f"⚡ Execution Difficulty: {data['execution_difficulty_score']}/100")

# Download PDF report
pdf = requests.get(f"http://localhost:12000/api/v1/report/{evaluation_id}?format=pdf")
with open("business_evaluation.pdf", "wb") as f:
    f.write(pdf.content)
print("\n📄 Report saved as business_evaluation.pdf")
```

### cURL Example
```bash
# Submit evaluation
curl -X POST "http://localhost:12000/api/v1/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
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
      "features": ["GPS-based farmer discovery"]
    },
    "competitive_advantages": ["Direct farmer relationships"]
  }'
```

---

## 📚 Explore More

### API Documentation
- **Swagger UI**: http://localhost:12000/docs
- **ReDoc**: http://localhost:12000/redoc

### Example Code
```bash
# Run the example script
python examples/example_usage.py
```

### Run Tests
```bash
# Install pytest if needed
pip install pytest

# Run tests
pytest tests/ -v
```

### Verify Installation
```bash
# Run verification script
python3 verify_system.py
```

---

## 🎯 What Can You Evaluate?

FlowCo can evaluate any business concept:

### Examples
- 🍕 **Food & Beverage**: Restaurant, food truck, catering service
- 💻 **Technology**: Mobile app, SaaS platform, AI tool
- 🏪 **Retail**: E-commerce store, boutique, marketplace
- 💪 **Health & Fitness**: Gym, fitness app, wellness coaching
- 🎓 **Education**: Online courses, tutoring, training platform
- 🎨 **Creative**: Design agency, photography, content creation
- 🏠 **Services**: Cleaning, landscaping, consulting
- 🚗 **Automotive**: Car wash, repair shop, rental service

### What You Get
- ✅ Success probability scores (0-100)
- ✅ Market demand analysis
- ✅ Competition assessment
- ✅ Target audience fit
- ✅ Financial projections
- ✅ Risk analysis
- ✅ Branding recommendations
- ✅ Marketing strategy
- ✅ Next steps roadmap

---

## 💡 Pro Tips

### For Best Results
1. **Be Specific**: Provide detailed business descriptions
2. **Know Your Audience**: Clearly define target demographics
3. **Upload Images**: Product images improve analysis quality
4. **List Features**: Include key product/service features
5. **Highlight Advantages**: Explain what makes you unique

### Cost Optimization
- Use **GPT-3.5 Turbo** for faster, cheaper evaluations
- Use **Ollama** (local models) for free evaluations
- Cache results to avoid re-evaluating same concepts

### Performance Tips
- Run with `--workers 4` for production
- Use `--reload` for development
- Enable caching for repeated evaluations

---

## 🐛 Troubleshooting

### "No AI service available"
**Problem**: No API key configured  
**Solution**: Add API key to `.env` file
```bash
OPENAI_API_KEY=sk-your-key-here
```

### "Module not found" errors
**Problem**: Dependencies not installed  
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### "Port already in use"
**Problem**: Port 12000 is occupied  
**Solution**: Use different port
```bash
python main.py --port 8080
```

### "Connection refused"
**Problem**: Server not running  
**Solution**: Start the server
```bash
python main.py
```

### Slow evaluations
**Problem**: Using large AI models  
**Solution**: Use faster model
```bash
# In .env file
DEFAULT_AI_MODEL=gpt-3.5-turbo
```

---

## 🎓 Learning Resources

### Documentation
- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick start guide
- **SYSTEM_STATUS.md** - System overview
- **IMPLEMENTATION_COMPLETE.md** - Implementation details

### Code Examples
- **examples/example_usage.py** - Programmatic usage
- **tests/test_basic_functionality.py** - Test examples

### API Reference
- **http://localhost:12000/docs** - Interactive API docs
- **http://localhost:12000/redoc** - Alternative API docs

---

## 🚀 Advanced Usage

### Custom Configuration
```bash
# Create custom config
cp config.yaml.example config.yaml

# Edit config.yaml
nano config.yaml

# Run with custom config
python main.py --config config.yaml
```

### Development Mode
```bash
# Auto-reload on code changes
python main.py --reload --debug
```

### Production Deployment
```bash
# Multiple workers
python main.py --workers 4 --host 0.0.0.0 --port 80
```

### Docker Deployment
```bash
# Build image
docker build -t flowco:latest .

# Run container
docker run -p 12000:12000 \
  -e OPENAI_API_KEY=your-key \
  flowco:latest
```

---

## 📞 Need Help?

### Quick Checks
1. ✅ Python 3.9+ installed?
2. ✅ Dependencies installed?
3. ✅ API key configured?
4. ✅ Server running?
5. ✅ Port 12000 available?

### Verification
```bash
# Run system verification
python3 verify_system.py
```

### Documentation
- Check **README.md** for detailed info
- Check **QUICKSTART.md** for setup help
- Check **API docs** at /docs endpoint

---

## 🎉 You're Ready!

You now have a fully functional AI business evaluation system!

### What's Next?
1. ✅ Evaluate your first business concept
2. ✅ Try the API with example code
3. ✅ Generate reports in different formats
4. ✅ Explore branding recommendations
5. ✅ Download marketing materials

### Start Evaluating!
```bash
# Make sure server is running
python main.py

# Open browser
open http://localhost:12000
```

---

**🚀 Happy Evaluating!**

*FlowCo - AI-Powered Business Success Evaluation*