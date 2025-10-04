#!/usr/bin/env python3
"""
FlowCo Example Usage

This script demonstrates how to use FlowCo programmatically to evaluate
business concepts and generate reports.
"""

import asyncio
import json
from pathlib import Path

from flowco.models.business import BusinessConcept, Demographics, ProductInfo, IncomeRange, BusinessCategory
from flowco.core.engine import BusinessEvaluationEngine
from flowco.output.report_generator import ReportGenerator
from flowco.output.template_generator import TemplateGenerator


async def example_evaluation():
    """Example business concept evaluation."""
    
    print("🚀 FlowCo Example: Business Concept Evaluation")
    print("=" * 50)
    
    # Create example business concept
    demographics = Demographics(
        age_min=25,
        age_max=45,
        income_range=IncomeRange.MIDDLE,
        location="San Francisco, CA, USA",
        interests=["organic food", "sustainability", "local business", "technology"],
        gender=None,
        education_level="bachelors"
    )
    
    product_info = ProductInfo(
        name="FarmConnect",
        description="A mobile marketplace that connects local farmers directly with consumers, enabling fresh produce delivery within 24 hours of harvest.",
        category=BusinessCategory.TECHNOLOGY,
        features=[
            "GPS-based farmer discovery",
            "Real-time inventory tracking",
            "In-app payment processing",
            "Delivery scheduling",
            "Quality guarantee system",
            "Farmer rating and reviews"
        ]
    )
    
    business_concept = BusinessConcept(
        concept_description="FarmConnect is a mobile platform that revolutionizes the local food supply chain by connecting consumers directly with nearby farmers. Our app eliminates middlemen, ensuring fresher produce at better prices while supporting local agriculture and reducing environmental impact through shorter supply chains.",
        target_demographics=demographics,
        product_info=product_info,
        business_model="Commission-based marketplace (5% per transaction) with premium farmer subscriptions",
        competitive_advantages=[
            "Direct farmer-to-consumer relationships",
            "24-hour freshness guarantee",
            "Lower prices than traditional retail",
            "Support for local agriculture",
            "Reduced environmental impact",
            "Transparent supply chain"
        ],
        funding_requirements="$250,000 for initial development and market launch",
        timeline="6 months to MVP, 12 months to full market launch"
    )
    
    print(f"📋 Evaluating: {business_concept.concept_description[:100]}...")
    print(f"🎯 Target: {demographics.location}, Ages {demographics.age_min}-{demographics.age_max}")
    print(f"💰 Income: {demographics.income_range}")
    print()
    
    # Initialize evaluation engine
    engine = BusinessEvaluationEngine()
    
    try:
        # Perform evaluation
        print("🔍 Starting AI evaluation...")
        result = await engine.evaluate_business_concept(business_concept)
        
        print("✅ Evaluation completed!")
        print()
        
        # Display key results
        print("📊 EVALUATION SCORES")
        print("-" * 30)
        print(f"Overall Success Score:     {result.overall_success_score:.1f}/100")
        print(f"Market Demand Score:       {result.market_demand_score:.1f}/100")
        print(f"Concept Viability Score:   {result.concept_viability_score:.1f}/100")
        print(f"Execution Difficulty:      {result.execution_difficulty_score:.1f}/100")
        print(f"Confidence Level:          {result.confidence_level:.1f}/100")
        print()
        
        # Display market insights
        print("🏪 MARKET INSIGHTS")
        print("-" * 30)
        print(f"Market Size:               {result.market_insights.market_size}")
        print(f"Competition Level:         {result.market_insights.competition_level.title()}")
        print(f"Demographic Fit:           {result.market_insights.demographic_fit_score:.1f}/100")
        print(f"Location Demand:           {result.market_insights.location_demand_score:.1f}/100")
        print()
        
        # Display top recommendations
        print("💡 TOP RECOMMENDATIONS")
        print("-" * 30)
        for i, rec in enumerate(result.key_recommendations[:5], 1):
            print(f"{i}. {rec}")
        print()
        
        # Display market trends
        if result.market_insights.market_trends:
            print("📈 MARKET TRENDS")
            print("-" * 30)
            for trend in result.market_insights.market_trends[:5]:
                print(f"• {trend}")
            print()
        
        # Generate reports
        print("📄 Generating reports...")
        report_generator = ReportGenerator()
        
        # Create output directory
        output_dir = Path("example_output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate different report formats
        formats = ["markdown", "html", "json"]
        for format_type in formats:
            try:
                output_path = output_dir / f"business_evaluation.{format_type}"
                await report_generator.generate_report(
                    business_concept, result, format=format_type, output_path=str(output_path)
                )
                print(f"✅ Generated {format_type.upper()} report: {output_path}")
            except Exception as e:
                print(f"❌ Failed to generate {format_type} report: {str(e)}")
        
        # Generate marketing materials
        print("\n🎨 Generating marketing materials...")
        template_generator = TemplateGenerator()
        
        try:
            # Generate landing page
            landing_page_path = output_dir / "landing_page.html"
            await template_generator.generate_landing_page(
                business_concept, result, str(landing_page_path)
            )
            print(f"✅ Generated landing page: {landing_page_path}")
            
            # Generate business card
            business_card_path = output_dir / "business_card.html"
            await template_generator.generate_business_card(
                business_concept, result, str(business_card_path)
            )
            print(f"✅ Generated business card: {business_card_path}")
            
            # Generate complete marketing materials
            marketing_files = await template_generator.generate_marketing_materials(
                business_concept, result, str(output_dir / "marketing")
            )
            print(f"✅ Generated marketing materials:")
            for material_type, file_path in marketing_files.items():
                print(f"   • {material_type}: {file_path}")
                
        except Exception as e:
            print(f"❌ Failed to generate marketing materials: {str(e)}")
        
        print(f"\n🎉 Evaluation complete! Check the '{output_dir}' directory for all generated files.")
        
        return result
        
    except Exception as e:
        print(f"❌ Evaluation failed: {str(e)}")
        print("💡 Make sure you have configured AI API keys in your .env file")
        return None


async def example_api_simulation():
    """Simulate API usage patterns."""
    
    print("\n" + "=" * 50)
    print("🌐 FlowCo Example: API Simulation")
    print("=" * 50)
    
    # This would normally be done via HTTP requests
    # Here we simulate the API workflow
    
    from flowco.web.api import EvaluationRequest
    
    # Create API request
    api_request = EvaluationRequest(
        concept_description="A subscription service for personalized workout plans generated by AI based on user fitness goals, available equipment, and time constraints.",
        target_demographics=Demographics(
            age_min=22,
            age_max=40,
            income_range=IncomeRange.UPPER_MIDDLE,
            location="Austin, TX, USA",
            interests=["fitness", "technology", "health", "wellness"]
        ),
        product_info=ProductInfo(
            name="FitAI",
            description="AI-powered personalized fitness coaching app",
            category=BusinessCategory.HEALTH_FITNESS,
            features=[
                "AI workout generation",
                "Progress tracking",
                "Nutrition guidance",
                "Video demonstrations",
                "Community features"
            ]
        ),
        competitive_advantages=[
            "Personalized AI coaching",
            "Adaptive workout plans",
            "Affordable pricing",
            "No gym required"
        ],
        funding_requirements="$150,000",
        timeline="8 months to launch"
    )
    
    print(f"📱 API Request: {api_request.concept_description[:80]}...")
    print(f"🎯 Target: {api_request.target_demographics.location}")
    print(f"💼 Category: {api_request.product_info.category}")
    
    # Convert to business concept
    business_concept = BusinessConcept(
        concept_description=api_request.concept_description,
        target_demographics=api_request.target_demographics,
        product_info=api_request.product_info,
        competitive_advantages=api_request.competitive_advantages,
        funding_requirements=api_request.funding_requirements,
        timeline=api_request.timeline
    )
    
    # Evaluate
    engine = BusinessEvaluationEngine()
    
    try:
        result = await engine.evaluate_business_concept(business_concept)
        
        # Generate summary (like API would return)
        report_generator = ReportGenerator()
        summary = await report_generator.generate_summary_report(business_concept, result)
        
        print("\n📊 API Response Summary:")
        print(json.dumps(summary, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ API simulation failed: {str(e)}")


def main():
    """Main example function."""
    print("🧠 FlowCo - AI Business Success Evaluation System")
    print("Example Usage Demonstration")
    print("=" * 60)
    
    # Run examples
    asyncio.run(example_evaluation())
    asyncio.run(example_api_simulation())
    
    print("\n" + "=" * 60)
    print("✨ Examples completed!")
    print("💡 To run FlowCo web interface: python main.py")
    print("📚 For more information, see README.md")


if __name__ == "__main__":
    main()