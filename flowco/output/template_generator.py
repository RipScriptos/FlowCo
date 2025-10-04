"""Website and landing page template generation."""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json

from jinja2 import Environment, Template

from ..models.business import BusinessConcept
from ..models.evaluation import EvaluationResult, BrandingRecommendations
from ..branding.content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class TemplateGenerator:
    """Generates website templates and landing pages."""
    
    def __init__(self):
        """Initialize template generator."""
        self.content_generator = ContentGenerator()
        self.templates_dir = Path(__file__).parent.parent.parent / "templates" / "web"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Create default web templates
        self._create_default_web_templates()
    
    def _create_default_web_templates(self):
        """Create default website templates."""
        
        # Landing page template
        landing_page_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business_name }} - {{ tagline }}</title>
    <meta name="description" content="{{ meta_description }}">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Header */
        header {
            background: {{ primary_color }};
            color: white;
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }
        
        .nav-links a:hover {
            opacity: 0.8;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, {{ primary_color }} 0%, {{ secondary_color }} 100%);
            color: white;
            padding: 120px 0 80px;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .cta-button {
            display: inline-block;
            background: {{ accent_color }};
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Features Section */
        .features {
            padding: 80px 0;
            background: #f8f9fa;
        }
        
        .features h2 {
            text-align: center;
            margin-bottom: 3rem;
            font-size: 2.5rem;
            color: #333;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 3rem;
            color: {{ primary_color }};
            margin-bottom: 1rem;
        }
        
        /* About Section */
        .about {
            padding: 80px 0;
        }
        
        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            align-items: center;
        }
        
        .about h2 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .about p {
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }
        
        /* Contact Section */
        .contact {
            background: {{ primary_color }};
            color: white;
            padding: 80px 0;
            text-align: center;
        }
        
        .contact h2 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .contact p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        /* Footer */
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem 0;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2rem;
            }
            
            .nav-links {
                display: none;
            }
            
            .about-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav class="container">
            <div class="logo">{{ business_name }}</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section id="home" class="hero">
        <div class="container">
            <h1>{{ hero_headline }}</h1>
            <p>{{ hero_subtext }}</p>
            <a href="#contact" class="cta-button">{{ cta_text }}</a>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2>Why Choose {{ business_name }}?</h2>
            <div class="features-grid">
                {% for feature in features %}
                <div class="feature-card">
                    <div class="feature-icon">{{ feature.icon }}</div>
                    <h3>{{ feature.title }}</h3>
                    <p>{{ feature.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <div class="about-content">
                <div>
                    <h2>About {{ business_name }}</h2>
                    <p>{{ about_text }}</p>
                    <p>{{ mission_statement }}</p>
                </div>
                <div>
                    <img src="https://via.placeholder.com/500x400/{{ primary_color|replace('#', '') }}/ffffff?text=Your+Business" alt="About {{ business_name }}" style="width: 100%; border-radius: 10px;">
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2>Ready to Get Started?</h2>
            <p>{{ contact_text }}</p>
            <a href="mailto:info@{{ business_name|lower|replace(' ', '') }}.com" class="cta-button">Contact Us Today</a>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 {{ business_name }}. All rights reserved.</p>
            <p>Generated by FlowCo AI Business Evaluation System</p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>"""
        
        # Business card template
        business_card_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business_name }} - Business Card</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f0f0f0;
        }
        
        .business-card {
            width: 3.5in;
            height: 2in;
            background: {{ primary_color }};
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .business-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: {{ secondary_color }};
            border-radius: 50%;
            opacity: 0.1;
        }
        
        .card-content {
            position: relative;
            z-index: 1;
        }
        
        .business-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .tagline {
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 15px;
        }
        
        .contact-info {
            font-size: 10px;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="business-card">
        <div class="card-content">
            <div class="business-name">{{ business_name }}</div>
            <div class="tagline">{{ tagline }}</div>
            <div class="contact-info">
                <div>📧 info@{{ business_name|lower|replace(' ', '') }}.com</div>
                <div>📱 (555) 123-4567</div>
                <div>🌐 www.{{ business_name|lower|replace(' ', '') }}.com</div>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        # Save templates
        (self.templates_dir / "landing_page.html").write_text(landing_page_template)
        (self.templates_dir / "business_card.html").write_text(business_card_template)
    
    async def generate_landing_page(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate a landing page for the business concept.
        
        Args:
            concept: Business concept
            evaluation: Evaluation results
            output_path: Optional output file path
            
        Returns:
            Generated HTML content or file path
        """
        logger.info("Generating landing page")
        
        try:
            # Generate website copy
            website_copy = await self.content_generator.generate_website_copy(
                concept, evaluation.branding_recommendations
            )
            
            # Prepare template context
            context = await self._prepare_landing_page_context(
                concept, evaluation, website_copy
            )
            
            # Load and render template
            template_path = self.templates_dir / "landing_page.html"
            template_content = template_path.read_text()
            template = Template(template_content)
            
            html_content = template.render(**context)
            
            if output_path:
                Path(output_path).write_text(html_content, encoding='utf-8')
                return output_path
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating landing page: {str(e)}")
            raise
    
    async def generate_business_card(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate a business card design.
        
        Args:
            concept: Business concept
            evaluation: Evaluation results
            output_path: Optional output file path
            
        Returns:
            Generated HTML content or file path
        """
        logger.info("Generating business card")
        
        try:
            # Prepare context
            context = {
                "business_name": concept.product_info.name or "Your Business",
                "tagline": evaluation.branding_recommendations.key_messaging[0] if evaluation.branding_recommendations.key_messaging else "Your Success Partner",
                "primary_color": evaluation.branding_recommendations.color_palette[0] if evaluation.branding_recommendations.color_palette else "#007bff",
                "secondary_color": evaluation.branding_recommendations.color_palette[1] if len(evaluation.branding_recommendations.color_palette) > 1 else "#6c757d"
            }
            
            # Load and render template
            template_path = self.templates_dir / "business_card.html"
            template_content = template_path.read_text()
            template = Template(template_content)
            
            html_content = template.render(**context)
            
            if output_path:
                Path(output_path).write_text(html_content, encoding='utf-8')
                return output_path
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating business card: {str(e)}")
            raise
    
    async def _prepare_landing_page_context(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult,
        website_copy: Dict[str, str]
    ) -> Dict[str, Any]:
        """Prepare context for landing page template."""
        
        branding = evaluation.branding_recommendations
        
        # Extract business name
        business_name = concept.product_info.name or "Your Business"
        
        # Generate features from product features and competitive advantages
        features = []
        feature_icons = ["🚀", "⭐", "💡", "🎯", "🔧", "📈"]
        
        # Add product features
        for i, feature in enumerate(concept.product_info.features[:3]):
            features.append({
                "icon": feature_icons[i % len(feature_icons)],
                "title": feature.title(),
                "description": f"Experience the power of {feature.lower()} in our innovative solution."
            })
        
        # Add competitive advantages
        for i, advantage in enumerate(concept.competitive_advantages[:3]):
            if len(features) < 6:
                features.append({
                    "icon": feature_icons[(i + 3) % len(feature_icons)],
                    "title": advantage.title(),
                    "description": f"We excel in {advantage.lower()} to deliver exceptional value."
                })
        
        # Ensure we have at least 3 features
        while len(features) < 3:
            features.append({
                "icon": "✨",
                "title": "Quality Service",
                "description": "We are committed to delivering the highest quality service to our customers."
            })
        
        return {
            "business_name": business_name,
            "tagline": branding.key_messaging[0] if branding.key_messaging else "Your Success Partner",
            "meta_description": f"{business_name} - {concept.concept_description[:150]}",
            "hero_headline": website_copy.get('hero', f"Transform Your Experience with {business_name}"),
            "hero_subtext": website_copy.get('about', concept.concept_description[:200]),
            "cta_text": website_copy.get('cta', "Get Started Today"),
            "about_text": website_copy.get('about', concept.concept_description),
            "mission_statement": f"At {business_name}, we are dedicated to {concept.concept_description.lower()}",
            "contact_text": f"Ready to experience the {business_name} difference? Contact us today to get started.",
            "features": features,
            "primary_color": branding.color_palette[0] if branding.color_palette else "#007bff",
            "secondary_color": branding.color_palette[1] if len(branding.color_palette) > 1 else "#6c757d",
            "accent_color": branding.color_palette[2] if len(branding.color_palette) > 2 else "#28a745"
        }
    
    async def generate_marketing_materials(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult,
        output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a complete set of marketing materials.
        
        Args:
            concept: Business concept
            evaluation: Evaluation results
            output_dir: Optional output directory
            
        Returns:
            Dictionary of generated file paths
        """
        logger.info("Generating complete marketing materials set")
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path("marketing_materials")
            output_path.mkdir(exist_ok=True)
        
        generated_files = {}
        
        try:
            # Generate landing page
            landing_page_path = output_path / "landing_page.html"
            await self.generate_landing_page(concept, evaluation, str(landing_page_path))
            generated_files["landing_page"] = str(landing_page_path)
            
            # Generate business card
            business_card_path = output_path / "business_card.html"
            await self.generate_business_card(concept, evaluation, str(business_card_path))
            generated_files["business_card"] = str(business_card_path)
            
            # Generate social media content
            social_content = await self._generate_social_media_content(concept, evaluation)
            social_path = output_path / "social_media_content.json"
            social_path.write_text(json.dumps(social_content, indent=2))
            generated_files["social_media"] = str(social_path)
            
            # Generate email templates
            email_templates = await self._generate_email_templates(concept, evaluation)
            email_path = output_path / "email_templates.json"
            email_path.write_text(json.dumps(email_templates, indent=2))
            generated_files["email_templates"] = str(email_path)
            
            logger.info(f"Generated {len(generated_files)} marketing materials")
            return generated_files
            
        except Exception as e:
            logger.error(f"Error generating marketing materials: {str(e)}")
            raise
    
    async def _generate_social_media_content(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult
    ) -> Dict[str, Any]:
        """Generate social media content."""
        
        business_name = concept.product_info.name or "Your Business"
        
        return {
            "facebook_posts": [
                f"🚀 Exciting news! {business_name} is here to {concept.concept_description.lower()}. Join us on this amazing journey! #Innovation #Business",
                f"✨ What makes {business_name} special? {evaluation.branding_recommendations.key_messaging[0] if evaluation.branding_recommendations.key_messaging else 'We deliver exceptional value!'} #Quality #Service",
                f"🎯 Ready to transform your experience? {business_name} is your trusted partner for success. Contact us today! #Success #Partnership"
            ],
            "twitter_posts": [
                f"🚀 {business_name} is revolutionizing the way you {concept.concept_description.lower()[:50]}... #Innovation",
                f"✨ Why choose {business_name}? Because we deliver results that matter. #Results #Quality",
                f"🎯 Ready for change? {business_name} is here to help. Get started today! #GetStarted"
            ],
            "instagram_captions": [
                f"✨ Welcome to {business_name}! We're passionate about {concept.concept_description.lower()}. Follow our journey! 📸 #Business #Passion #Journey",
                f"🌟 Behind the scenes at {business_name}. Every day we work to deliver exceptional value to our customers. #BehindTheScenes #Value #Customers",
                f"🚀 The future is here with {business_name}. Join us as we {concept.concept_description.lower()}! #Future #Innovation #JoinUs"
            ],
            "linkedin_posts": [
                f"We're excited to announce {business_name}, a new venture focused on {concept.concept_description}. Our mission is to deliver exceptional value through innovation and dedication to our customers.",
                f"At {business_name}, we believe in the power of {concept.concept_description.lower()}. Our team is committed to excellence and customer satisfaction in everything we do.",
                f"Looking for a partner who understands your needs? {business_name} combines expertise with innovation to deliver results that exceed expectations."
            ]
        }
    
    async def _generate_email_templates(
        self, 
        concept: BusinessConcept, 
        evaluation: EvaluationResult
    ) -> Dict[str, Any]:
        """Generate email templates."""
        
        business_name = concept.product_info.name or "Your Business"
        
        return {
            "welcome_email": {
                "subject": f"Welcome to {business_name}!",
                "body": f"Dear Valued Customer,\n\nWelcome to {business_name}! We're thrilled to have you join our community.\n\nAt {business_name}, we are dedicated to {concept.concept_description.lower()}. Our team is committed to providing you with exceptional service and value.\n\nWhat you can expect from us:\n- {evaluation.branding_recommendations.key_messaging[0] if evaluation.branding_recommendations.key_messaging else 'Exceptional service'}\n- Dedicated customer support\n- Innovative solutions tailored to your needs\n\nThank you for choosing {business_name}. We look forward to serving you!\n\nBest regards,\nThe {business_name} Team"
            },
            "promotional_email": {
                "subject": f"Discover What Makes {business_name} Different",
                "body": f"Hello,\n\nAre you ready to experience the {business_name} difference?\n\n{concept.concept_description}\n\nWhy choose us?\n{chr(10).join(f'• {msg}' for msg in evaluation.branding_recommendations.key_messaging[:3])}\n\nReady to get started? Contact us today to learn more about how we can help you succeed.\n\nBest regards,\nThe {business_name} Team"
            },
            "follow_up_email": {
                "subject": f"Thank you for your interest in {business_name}",
                "body": f"Dear Potential Customer,\n\nThank you for your interest in {business_name}. We wanted to follow up and provide you with more information about our services.\n\n{concept.concept_description}\n\nOur commitment to you:\n- Quality service and support\n- Innovative solutions\n- Customer satisfaction guarantee\n\nWe would love to discuss how {business_name} can help you achieve your goals. Please don't hesitate to reach out with any questions.\n\nBest regards,\nThe {business_name} Team"
            }
        }