"""Basic functionality tests for FlowCo."""

import pytest
from pathlib import Path

from flowco.models.business import BusinessConcept, Demographics, ProductInfo, IncomeRange, BusinessCategory
from flowco.core.config import Config
from flowco.processing.input_processor import InputProcessor
from flowco.output.report_generator import ReportGenerator


def test_config_initialization():
    """Test configuration system initialization."""
    config = Config()
    
    # Test basic configuration access
    assert config.get("web.host") is not None
    assert config.get("web.port") is not None
    assert isinstance(config.get("web.port"), int)
    
    # Test default values
    assert config.get("nonexistent.key", "default") == "default"
    
    # Test available models
    models = config.get_available_models()
    assert isinstance(models, list)


def test_business_concept_creation():
    """Test business concept model creation and validation."""
    
    # Create valid demographics
    demographics = Demographics(
        age_min=25,
        age_max=45,
        income_range=IncomeRange.MIDDLE,
        location="San Francisco, CA, USA",
        interests=["technology", "sustainability"]
    )
    
    # Create valid product info
    product_info = ProductInfo(
        name="TestProduct",
        description="A test product for validation",
        category=BusinessCategory.TECHNOLOGY,
        features=["feature1", "feature2"]
    )
    
    # Create business concept
    concept = BusinessConcept(
        concept_description="A test business concept for validation purposes",
        target_demographics=demographics,
        product_info=product_info,
        competitive_advantages=["advantage1", "advantage2"]
    )
    
    # Validate creation
    assert concept.concept_description is not None
    assert concept.target_demographics.age_min == 25
    assert concept.target_demographics.age_max == 45
    assert concept.product_info.name == "TestProduct"
    assert len(concept.competitive_advantages) == 2


def test_demographics_validation():
    """Test demographics validation."""
    
    # Test valid demographics
    demographics = Demographics(
        age_min=18,
        age_max=65,
        income_range=IncomeRange.HIGH,
        location="New York, NY, USA",
        interests=["business", "finance"]
    )
    
    assert demographics.age_min < demographics.age_max
    assert demographics.location is not None
    
    # Test invalid age range (should raise validation error)
    with pytest.raises(ValueError):
        Demographics(
            age_min=50,
            age_max=30,  # Invalid: max < min
            income_range=IncomeRange.MIDDLE,
            location="Test Location"
        )


def test_input_processor():
    """Test input processing functionality."""
    
    processor = InputProcessor()
    
    # Test text cleaning
    dirty_text = "  This is   a test   with extra   spaces  "
    clean_text = processor._clean_text(dirty_text)
    assert clean_text == "This is a test with extra spaces"
    
    # Test keyword extraction
    text = "This is a test about artificial intelligence and machine learning"
    keywords = processor.extract_keywords(text)
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert "artificial" in keywords
    assert "intelligence" in keywords
    
    # Test sentiment analysis
    positive_text = "This is an amazing and wonderful opportunity"
    sentiment = processor.analyze_sentiment(positive_text)
    assert sentiment["sentiment"] in ["positive", "negative", "neutral"]
    assert 0 <= sentiment["confidence"] <= 1


@pytest.mark.asyncio
async def test_report_generation():
    """Test report generation functionality."""
    
    # Create test business concept
    demographics = Demographics(
        age_min=25,
        age_max=45,
        income_range=IncomeRange.MIDDLE,
        location="Test City, USA",
        interests=["test"]
    )
    
    product_info = ProductInfo(
        name="TestProduct",
        description="Test product description"
    )
    
    concept = BusinessConcept(
        concept_description="Test business concept",
        target_demographics=demographics,
        product_info=product_info
    )
    
    # Create mock evaluation result
    from flowco.models.evaluation import (
        EvaluationResult, MarketInsights, BrandingRecommendations,
        CompetitiveAnalysis, FinancialProjections, RiskAssessment
    )
    
    market_insights = MarketInsights(
        market_size="Test market",
        competition_level="medium",
        target_market_analysis="Test analysis",
        demographic_fit_score=75.0,
        location_demand_score=80.0
    )
    
    branding = BrandingRecommendations(
        brand_positioning="Test positioning",
        content_strategy="Test strategy"
    )
    
    competitive_analysis = CompetitiveAnalysis()
    financial_projections = FinancialProjections()
    risk_assessment = RiskAssessment()
    
    result = EvaluationResult(
        overall_success_score=75.0,
        market_demand_score=80.0,
        concept_viability_score=70.0,
        execution_difficulty_score=60.0,
        market_insights=market_insights,
        branding_recommendations=branding,
        competitive_analysis=competitive_analysis,
        financial_projections=financial_projections,
        risk_assessment=risk_assessment,
        executive_summary="Test summary",
        confidence_level=85.0
    )
    
    # Test report generation
    generator = ReportGenerator()
    
    # Test markdown generation
    markdown_content = await generator.generate_report(
        concept, result, format="markdown"
    )
    assert isinstance(markdown_content, str)
    assert "Business Evaluation Report" in markdown_content
    assert "Test business concept" in markdown_content
    
    # Test JSON generation
    json_content = await generator.generate_report(
        concept, result, format="json"
    )
    assert isinstance(json_content, str)
    assert "business_concept" in json_content
    
    # Test summary generation
    summary = await generator.generate_summary_report(concept, result)
    assert isinstance(summary, dict)
    assert "overall_score" in summary
    assert summary["overall_score"] == 75.0


def test_model_serialization():
    """Test model serialization and deserialization."""
    
    demographics = Demographics(
        age_min=30,
        age_max=50,
        income_range=IncomeRange.HIGH,
        location="Test Location",
        interests=["test1", "test2"]
    )
    
    # Test serialization
    data = demographics.dict()
    assert isinstance(data, dict)
    assert data["age_min"] == 30
    assert data["age_max"] == 50
    assert data["income_range"] == "high"
    
    # Test deserialization
    new_demographics = Demographics(**data)
    assert new_demographics.age_min == demographics.age_min
    assert new_demographics.age_max == demographics.age_max
    assert new_demographics.income_range == demographics.income_range


def test_file_structure():
    """Test that required files and directories exist."""
    
    base_path = Path(__file__).parent.parent
    
    # Test main files
    assert (base_path / "main.py").exists()
    assert (base_path / "requirements.txt").exists()
    assert (base_path / "README.md").exists()
    assert (base_path / ".gitignore").exists()
    
    # Test package structure
    flowco_path = base_path / "flowco"
    assert flowco_path.exists()
    assert (flowco_path / "__init__.py").exists()
    
    # Test core modules
    assert (flowco_path / "core" / "__init__.py").exists()
    assert (flowco_path / "core" / "engine.py").exists()
    assert (flowco_path / "core" / "config.py").exists()
    
    # Test models
    assert (flowco_path / "models" / "__init__.py").exists()
    assert (flowco_path / "models" / "business.py").exists()
    assert (flowco_path / "models" / "evaluation.py").exists()
    
    # Test web interface
    assert (flowco_path / "web" / "__init__.py").exists()
    assert (flowco_path / "web" / "app.py").exists()
    assert (flowco_path / "web" / "api.py").exists()


if __name__ == "__main__":
    pytest.main([__file__])