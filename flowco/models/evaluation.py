"""Evaluation result data models."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MarketInsights(BaseModel):
    """Market research and insights."""
    
    market_size: Optional[str] = Field(None, description="Estimated market size")
    competition_level: str = Field(..., description="Competition level (low/medium/high)")
    market_trends: List[str] = Field(default_factory=list, description="Current market trends")
    seasonal_factors: List[str] = Field(default_factory=list, description="Seasonal considerations")
    regulatory_considerations: List[str] = Field(default_factory=list, description="Regulatory factors")
    target_market_analysis: str = Field(..., description="Target market analysis")
    demographic_fit_score: float = Field(..., ge=0, le=100, description="Demographic fit score (0-100)")
    location_demand_score: float = Field(..., ge=0, le=100, description="Location demand score (0-100)")


class BrandingRecommendations(BaseModel):
    """Branding and marketing recommendations."""
    
    brand_positioning: str = Field(..., description="Recommended brand positioning")
    key_messaging: List[str] = Field(default_factory=list, description="Key marketing messages")
    visual_identity_suggestions: List[str] = Field(default_factory=list, description="Visual identity suggestions")
    marketing_channels: List[str] = Field(default_factory=list, description="Recommended marketing channels")
    content_strategy: str = Field(..., description="Content marketing strategy")
    logo_concepts: List[str] = Field(default_factory=list, description="Logo concept ideas")
    color_palette: List[str] = Field(default_factory=list, description="Suggested color palette")
    commercial_script: Optional[str] = Field(None, description="Sample commercial script")


class CompetitiveAnalysis(BaseModel):
    """Competitive analysis results."""
    
    direct_competitors: List[str] = Field(default_factory=list, description="Direct competitors")
    indirect_competitors: List[str] = Field(default_factory=list, description="Indirect competitors")
    competitive_advantages: List[str] = Field(default_factory=list, description="Your competitive advantages")
    market_gaps: List[str] = Field(default_factory=list, description="Identified market gaps")
    differentiation_opportunities: List[str] = Field(default_factory=list, description="Differentiation opportunities")


class FinancialProjections(BaseModel):
    """Financial projections and estimates."""
    
    startup_costs: Optional[str] = Field(None, description="Estimated startup costs")
    revenue_projections: Dict[str, str] = Field(default_factory=dict, description="Revenue projections by year")
    break_even_timeline: Optional[str] = Field(None, description="Estimated break-even timeline")
    funding_recommendations: List[str] = Field(default_factory=list, description="Funding recommendations")
    cost_structure: List[str] = Field(default_factory=list, description="Key cost components")


class RiskAssessment(BaseModel):
    """Risk assessment and mitigation strategies."""
    
    high_risks: List[str] = Field(default_factory=list, description="High-priority risks")
    medium_risks: List[str] = Field(default_factory=list, description="Medium-priority risks")
    low_risks: List[str] = Field(default_factory=list, description="Low-priority risks")
    mitigation_strategies: Dict[str, str] = Field(default_factory=dict, description="Risk mitigation strategies")
    success_factors: List[str] = Field(default_factory=list, description="Critical success factors")


class EvaluationResult(BaseModel):
    """Complete business evaluation result."""
    
    # Core scores
    overall_success_score: float = Field(..., ge=0, le=100, description="Overall success probability (0-100)")
    market_demand_score: float = Field(..., ge=0, le=100, description="Market demand score (0-100)")
    concept_viability_score: float = Field(..., ge=0, le=100, description="Concept viability score (0-100)")
    execution_difficulty_score: float = Field(..., ge=0, le=100, description="Execution difficulty score (0-100)")
    
    # Detailed analysis
    market_insights: MarketInsights = Field(..., description="Market research insights")
    branding_recommendations: BrandingRecommendations = Field(..., description="Branding recommendations")
    competitive_analysis: CompetitiveAnalysis = Field(..., description="Competitive analysis")
    financial_projections: FinancialProjections = Field(..., description="Financial projections")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment")
    
    # Summary and recommendations
    executive_summary: str = Field(..., description="Executive summary")
    key_recommendations: List[str] = Field(default_factory=list, description="Key recommendations")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    
    # Metadata
    evaluation_date: datetime = Field(default_factory=datetime.now, description="Evaluation timestamp")
    model_version: str = Field(default="1.0.0", description="Model version used")
    confidence_level: float = Field(..., ge=0, le=100, description="Confidence in evaluation (0-100)")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }