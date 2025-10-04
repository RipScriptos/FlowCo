"""FastAPI web application for FlowCo."""

import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .api import router as api_router
from ..core.config import config

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="FlowCo - AI Business Evaluation System",
        description="Comprehensive AI system for evaluating business concepts and predicting success",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Setup static files and templates
    static_dir = Path(__file__).parent / "static"
    templates_dir = Path(__file__).parent / "templates"
    
    # Create directories if they don't exist
    static_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Setup templates
    templates = Jinja2Templates(directory=str(templates_dir))
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
    
    # Create default templates
    _create_default_templates(templates_dir)
    _create_default_static_files(static_dir)
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Home page."""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/evaluate", response_class=HTMLResponse)
    async def evaluate_page(request: Request):
        """Business evaluation page."""
        return templates.TemplateResponse("evaluate.html", {"request": request})
    
    @app.get("/results/{evaluation_id}", response_class=HTMLResponse)
    async def results_page(request: Request, evaluation_id: str):
        """Results page."""
        return templates.TemplateResponse("results.html", {
            "request": request, 
            "evaluation_id": evaluation_id
        })
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": "1.0.0"}
    
    return app


def _create_default_templates(templates_dir: Path):
    """Create default HTML templates."""
    
    # Base template
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}FlowCo - AI Business Evaluation{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-chart-line me-2"></i>FlowCo
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/evaluate">Evaluate Business</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/docs">API Docs</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; 2024 FlowCo - AI Business Evaluation System</p>
            <p class="small">Powered by advanced AI for comprehensive business analysis</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>"""
    
    # Home page template
    index_template = """{% extends "base.html" %}

{% block content %}
<div class="hero-section bg-gradient-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">AI-Powered Business Success Evaluation</h1>
                <p class="lead mb-4">
                    Predict your business concept's success with our comprehensive AI analysis. 
                    Get market insights, competitive analysis, and branding recommendations.
                </p>
                <a href="/evaluate" class="btn btn-light btn-lg">
                    <i class="fas fa-rocket me-2"></i>Start Evaluation
                </a>
            </div>
            <div class="col-lg-6">
                <div class="text-center">
                    <i class="fas fa-brain fa-10x opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="container py-5">
    <div class="row">
        <div class="col-lg-8 mx-auto text-center mb-5">
            <h2 class="display-5 mb-4">How FlowCo Works</h2>
            <p class="lead">Our AI system analyzes your business concept across multiple dimensions to provide comprehensive insights.</p>
        </div>
    </div>
    
    <div class="row g-4">
        <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center p-4">
                    <div class="feature-icon bg-primary text-white rounded-circle mx-auto mb-3">
                        <i class="fas fa-upload fa-2x"></i>
                    </div>
                    <h5 class="card-title">1. Input Your Concept</h5>
                    <p class="card-text">Describe your business idea, target demographics, and upload product images if available.</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center p-4">
                    <div class="feature-icon bg-success text-white rounded-circle mx-auto mb-3">
                        <i class="fas fa-cogs fa-2x"></i>
                    </div>
                    <h5 class="card-title">2. AI Analysis</h5>
                    <p class="card-text">Our AI analyzes market conditions, competition, demographics, and product viability.</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body text-center p-4">
                    <div class="feature-icon bg-info text-white rounded-circle mx-auto mb-3">
                        <i class="fas fa-chart-bar fa-2x"></i>
                    </div>
                    <h5 class="card-title">3. Get Insights</h5>
                    <p class="card-text">Receive detailed reports with success predictions, recommendations, and marketing materials.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="bg-light py-5">
    <div class="container">
        <div class="row">
            <div class="col-lg-8 mx-auto text-center">
                <h2 class="display-6 mb-4">What You'll Get</h2>
                <div class="row g-3">
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Success probability scores</span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Market demand analysis</span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Competitive landscape</span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Branding recommendations</span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Financial projections</span>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-check-circle text-success me-3"></i>
                            <span>Marketing materials</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
    
    # Evaluation form template
    evaluate_template = """{% extends "base.html" %}

{% block title %}Evaluate Business Concept - FlowCo{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <div class="text-center mb-5">
                <h1 class="display-5">Evaluate Your Business Concept</h1>
                <p class="lead">Fill out the form below to get comprehensive AI-powered insights about your business idea.</p>
            </div>
            
            <div class="card shadow">
                <div class="card-body p-4">
                    <form id="evaluationForm">
                        <!-- Business Concept Section -->
                        <div class="mb-4">
                            <h4 class="text-primary mb-3">
                                <i class="fas fa-lightbulb me-2"></i>Business Concept
                            </h4>
                            
                            <div class="mb-3">
                                <label for="conceptDescription" class="form-label">Business Concept Description *</label>
                                <textarea class="form-control" id="conceptDescription" name="conceptDescription" rows="4" 
                                    placeholder="Describe your business idea, what problem it solves, and how it works..." required></textarea>
                            </div>
                            
                            <div class="mb-3">
                                <label for="businessModel" class="form-label">Business Model</label>
                                <input type="text" class="form-control" id="businessModel" name="businessModel" 
                                    placeholder="e.g., Subscription, One-time purchase, Freemium...">
                            </div>
                        </div>
                        
                        <!-- Product Information Section -->
                        <div class="mb-4">
                            <h4 class="text-primary mb-3">
                                <i class="fas fa-box me-2"></i>Product Information
                            </h4>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="productName" class="form-label">Product/Service Name</label>
                                    <input type="text" class="form-control" id="productName" name="productName" 
                                        placeholder="Enter your product or service name">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="productCategory" class="form-label">Category</label>
                                    <select class="form-select" id="productCategory" name="productCategory">
                                        <option value="">Select category...</option>
                                        <option value="technology">Technology</option>
                                        <option value="retail">Retail</option>
                                        <option value="food_beverage">Food & Beverage</option>
                                        <option value="health_fitness">Health & Fitness</option>
                                        <option value="education">Education</option>
                                        <option value="entertainment">Entertainment</option>
                                        <option value="finance">Finance</option>
                                        <option value="real_estate">Real Estate</option>
                                        <option value="automotive">Automotive</option>
                                        <option value="fashion">Fashion</option>
                                        <option value="home_garden">Home & Garden</option>
                                        <option value="travel">Travel</option>
                                        <option value="professional_services">Professional Services</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="productDescription" class="form-label">Product Description</label>
                                <textarea class="form-control" id="productDescription" name="productDescription" rows="3" 
                                    placeholder="Describe your product or service in detail..."></textarea>
                            </div>
                            
                            <div class="mb-3">
                                <label for="productFeatures" class="form-label">Key Features (one per line)</label>
                                <textarea class="form-control" id="productFeatures" name="productFeatures" rows="3" 
                                    placeholder="List key features or benefits, one per line..."></textarea>
                            </div>
                            
                            <div class="mb-3">
                                <label for="productImage" class="form-label">Product Image (optional)</label>
                                <input type="file" class="form-control" id="productImage" name="productImage" 
                                    accept="image/*">
                                <div class="form-text">Upload an image of your product for visual analysis</div>
                            </div>
                        </div>
                        
                        <!-- Target Demographics Section -->
                        <div class="mb-4">
                            <h4 class="text-primary mb-3">
                                <i class="fas fa-users me-2"></i>Target Demographics
                            </h4>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="ageMin" class="form-label">Minimum Age *</label>
                                    <input type="number" class="form-control" id="ageMin" name="ageMin" 
                                        min="0" max="100" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="ageMax" class="form-label">Maximum Age *</label>
                                    <input type="number" class="form-control" id="ageMax" name="ageMax" 
                                        min="0" max="100" required>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="incomeRange" class="form-label">Income Range *</label>
                                    <select class="form-select" id="incomeRange" name="incomeRange" required>
                                        <option value="">Select income range...</option>
                                        <option value="low">Low (Under $30k)</option>
                                        <option value="lower_middle">Lower Middle ($30k-$50k)</option>
                                        <option value="middle">Middle ($50k-$80k)</option>
                                        <option value="upper_middle">Upper Middle ($80k-$120k)</option>
                                        <option value="high">High (Over $120k)</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="location" class="form-label">Target Location *</label>
                                    <input type="text" class="form-control" id="location" name="location" 
                                        placeholder="e.g., New York, NY, USA" required>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="interests" class="form-label">Target Interests (comma-separated)</label>
                                <input type="text" class="form-control" id="interests" name="interests" 
                                    placeholder="e.g., technology, fitness, cooking, travel">
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="gender" class="form-label">Gender (optional)</label>
                                    <select class="form-select" id="gender" name="gender">
                                        <option value="">Any</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                        <option value="non-binary">Non-binary</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="educationLevel" class="form-label">Education Level (optional)</label>
                                    <select class="form-select" id="educationLevel" name="educationLevel">
                                        <option value="">Any</option>
                                        <option value="high_school">High School</option>
                                        <option value="some_college">Some College</option>
                                        <option value="bachelors">Bachelor's Degree</option>
                                        <option value="masters">Master's Degree</option>
                                        <option value="doctorate">Doctorate</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Additional Information Section -->
                        <div class="mb-4">
                            <h4 class="text-primary mb-3">
                                <i class="fas fa-plus-circle me-2"></i>Additional Information
                            </h4>
                            
                            <div class="mb-3">
                                <label for="competitiveAdvantages" class="form-label">Competitive Advantages (one per line)</label>
                                <textarea class="form-control" id="competitiveAdvantages" name="competitiveAdvantages" rows="3" 
                                    placeholder="What makes your business unique? List advantages, one per line..."></textarea>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="fundingRequirements" class="form-label">Funding Requirements</label>
                                    <input type="text" class="form-control" id="fundingRequirements" name="fundingRequirements" 
                                        placeholder="e.g., $50,000 startup capital">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="timeline" class="form-label">Timeline to Market</label>
                                    <input type="text" class="form-control" id="timeline" name="timeline" 
                                        placeholder="e.g., 6 months">
                                </div>
                            </div>
                        </div>
                        
                        <!-- Submit Button -->
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg px-5" id="submitBtn">
                                <i class="fas fa-chart-line me-2"></i>Evaluate Business Concept
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Loading Modal -->
<div class="modal fade" id="loadingModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body text-center py-5">
                <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h5>Analyzing Your Business Concept</h5>
                <p class="text-muted">Our AI is evaluating your business idea. This may take a few minutes...</p>
                <div class="progress mt-3">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%"></div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="/static/js/evaluate.js"></script>
{% endblock %}"""
    
    # Results template
    results_template = """{% extends "base.html" %}

{% block title %}Evaluation Results - FlowCo{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-12">
            <div class="text-center mb-5">
                <h1 class="display-5">Business Evaluation Results</h1>
                <p class="lead">Comprehensive AI analysis of your business concept</p>
            </div>
            
            <div id="resultsContainer">
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading results...</span>
                    </div>
                    <p class="mt-3">Loading your evaluation results...</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    const evaluationId = "{{ evaluation_id }}";
</script>
<script src="/static/js/results.js"></script>
{% endblock %}"""
    
    # Save templates
    (templates_dir / "base.html").write_text(base_template)
    (templates_dir / "index.html").write_text(index_template)
    (templates_dir / "evaluate.html").write_text(evaluate_template)
    (templates_dir / "results.html").write_text(results_template)


def _create_default_static_files(static_dir: Path):
    """Create default static files."""
    
    # Create subdirectories
    (static_dir / "css").mkdir(exist_ok=True)
    (static_dir / "js").mkdir(exist_ok=True)
    
    # CSS file
    css_content = """/* Custom styles for FlowCo */
.bg-gradient-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-icon {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-section {
    min-height: 60vh;
    display: flex;
    align-items: center;
}

.card {
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-5px);
}

.progress-bar-animated {
    animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
    0% { background-position: 1rem 0; }
    100% { background-position: 0 0; }
}

.score-card {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-left: 4px solid #007bff;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}

.score-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #007bff;
}

.recommendation-item {
    background: #e7f3ff;
    border-left: 4px solid #007bff;
    padding: 1rem;
    margin-bottom: 0.5rem;
    border-radius: 0.25rem;
}

.risk-high { color: #dc3545; }
.risk-medium { color: #ffc107; }
.risk-low { color: #28a745; }"""
    
    # JavaScript files
    app_js = """// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});"""
    
    evaluate_js = """// Evaluation form JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('evaluationForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading modal
        loadingModal.show();
        
        // Simulate progress
        let progress = 0;
        const progressBar = document.querySelector('.progress-bar');
        const progressInterval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress > 90) progress = 90;
            progressBar.style.width = progress + '%';
        }, 500);
        
        try {
            // Collect form data
            const formData = new FormData(form);
            
            // Convert features and advantages to arrays
            const features = formData.get('productFeatures')?.split('\\n').filter(f => f.trim()) || [];
            const advantages = formData.get('competitiveAdvantages')?.split('\\n').filter(a => a.trim()) || [];
            const interests = formData.get('interests')?.split(',').map(i => i.trim()).filter(i => i) || [];
            
            // Prepare request data
            const requestData = {
                concept_description: formData.get('conceptDescription'),
                business_model: formData.get('businessModel') || null,
                target_demographics: {
                    age_min: parseInt(formData.get('ageMin')),
                    age_max: parseInt(formData.get('ageMax')),
                    income_range: formData.get('incomeRange'),
                    location: formData.get('location'),
                    interests: interests,
                    gender: formData.get('gender') || null,
                    education_level: formData.get('educationLevel') || null
                },
                product_info: {
                    name: formData.get('productName') || null,
                    description: formData.get('productDescription') || null,
                    category: formData.get('productCategory') || null,
                    features: features
                },
                competitive_advantages: advantages,
                funding_requirements: formData.get('fundingRequirements') || null,
                timeline: formData.get('timeline') || null
            };
            
            // Submit evaluation
            const response = await fetch('/api/v1/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error('Evaluation failed');
            }
            
            const result = await response.json();
            
            // Complete progress
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            
            // Redirect to results
            setTimeout(() => {
                window.location.href = `/results/${result.evaluation_id}`;
            }, 1000);
            
        } catch (error) {
            console.error('Error:', error);
            clearInterval(progressInterval);
            loadingModal.hide();
            alert('An error occurred during evaluation. Please try again.');
        }
    });
});"""
    
    results_js = """// Results page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadResults();
});

async function loadResults() {
    try {
        const response = await fetch(`/api/v1/results/${evaluationId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load results');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error loading results:', error);
        document.getElementById('resultsContainer').innerHTML = `
            <div class="alert alert-danger text-center">
                <h4>Error Loading Results</h4>
                <p>Unable to load evaluation results. Please try again later.</p>
                <a href="/evaluate" class="btn btn-primary">Start New Evaluation</a>
            </div>
        `;
    }
}

function displayResults(data) {
    const container = document.getElementById('resultsContainer');
    
    const html = `
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h3 class="mb-0"><i class="fas fa-chart-line me-2"></i>Evaluation Scores</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3 mb-3">
                                <div class="score-card text-center">
                                    <div class="score-value">${data.overall_success_score}/100</div>
                                    <div class="fw-bold">Overall Success</div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="score-card text-center">
                                    <div class="score-value">${data.market_demand_score}/100</div>
                                    <div class="fw-bold">Market Demand</div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="score-card text-center">
                                    <div class="score-value">${data.concept_viability_score}/100</div>
                                    <div class="fw-bold">Concept Viability</div>
                                </div>
                            </div>
                            <div class="col-md-3 mb-3">
                                <div class="score-card text-center">
                                    <div class="score-value">${data.execution_difficulty_score}/100</div>
                                    <div class="fw-bold">Execution Difficulty</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-lg-8">
                <div class="card mb-4">
                    <div class="card-header">
                        <h4 class="mb-0"><i class="fas fa-file-alt me-2"></i>Executive Summary</h4>
                    </div>
                    <div class="card-body">
                        <p>${data.executive_summary}</p>
                    </div>
                </div>
                
                <div class="card mb-4">
                    <div class="card-header">
                        <h4 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Key Recommendations</h4>
                    </div>
                    <div class="card-body">
                        ${data.key_recommendations.map((rec, index) => `
                            <div class="recommendation-item">
                                <strong>${index + 1}.</strong> ${rec}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Market Insights</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Market Size:</strong> ${data.market_insights.market_size}</p>
                        <p><strong>Competition:</strong> ${data.market_insights.competition_level}</p>
                        <p><strong>Demographic Fit:</strong> ${data.market_insights.demographic_fit_score}/100</p>
                        <p><strong>Location Demand:</strong> ${data.market_insights.location_demand_score}/100</p>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-download me-2"></i>Download Reports</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary" onclick="downloadReport('pdf')">
                                <i class="fas fa-file-pdf me-2"></i>PDF Report
                            </button>
                            <button class="btn btn-outline-success" onclick="downloadReport('html')">
                                <i class="fas fa-file-code me-2"></i>HTML Report
                            </button>
                            <button class="btn btn-outline-info" onclick="downloadReport('json')">
                                <i class="fas fa-file-code me-2"></i>JSON Data
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

async function downloadReport(format) {
    try {
        const response = await fetch(`/api/v1/report/${evaluationId}?format=${format}`);
        
        if (!response.ok) {
            throw new Error('Failed to generate report');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `business_evaluation_${evaluationId}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        console.error('Error downloading report:', error);
        alert('Failed to download report. Please try again.');
    }
}"""
    
    # Save static files
    (static_dir / "css" / "style.css").write_text(css_content)
    (static_dir / "js" / "app.js").write_text(app_js)
    (static_dir / "js" / "evaluate.js").write_text(evaluate_js)
    (static_dir / "js" / "results.js").write_text(results_js)