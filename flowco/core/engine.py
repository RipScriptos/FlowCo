"""Core business evaluation engine."""

import asyncio
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from ..models.business import BusinessConcept
from ..models.evaluation import EvaluationResult, MarketInsights, BrandingRecommendations
from ..processing.input_processor import InputProcessor
from ..processing.vision_processor import VisionProcessor
from ..research.market_analyzer import MarketAnalyzer
from ..branding.content_generator import ContentGenerator
from ..core.ai_client import AIClient
from ..core.config import config

logger = logging.getLogger(__name__)


class BusinessEvaluationEngine:
    """Main engine for business concept evaluation."""
    
    def __init__(self):
        """Initialize the evaluation engine."""
        self.ai_client = AIClient()
        self.input_processor = InputProcessor()
        self.vision_processor = VisionProcessor()
        self.market_analyzer = MarketAnalyzer()
        self.content_generator = ContentGenerator()
        
    async def evaluate_business_concept(
        self, 
        business_concept: BusinessConcept,
        include_branding: bool = True,
        include_financial: bool = True
    ) -> EvaluationResult:
        """
        Evaluate a business concept and return comprehensive analysis.
        
        Args:
            business_concept: The business concept to evaluate
            include_branding: Whether to include branding recommendations
            include_financial: Whether to include financial projections
            
        Returns:
            Complete evaluation result
        """
        logger.info(f"Starting evaluation for business concept: {business_concept.concept_description[:100]}...")
        
        try:
            # Step 1: Process and validate inputs
            processed_concept = await self.input_processor.process_business_concept(business_concept)
            
            # Step 2: Analyze product if image provided
            product_analysis = None
            if business_concept.product_info.image_path or business_concept.product_info.image_data:
                product_analysis = await self.vision_processor.analyze_product_image(
                    business_concept.product_info
                )
            
            # Step 3: Conduct market research
            market_insights = await self.market_analyzer.analyze_market(
                processed_concept, product_analysis
            )
            
            # Step 4: Calculate core scores
            scores = await self._calculate_core_scores(processed_concept, market_insights, product_analysis)
            
            # Step 5: Generate branding recommendations (if requested)
            branding_recommendations = None
            if include_branding:
                branding_recommendations = await self.content_generator.generate_branding_recommendations(
                    processed_concept, market_insights, product_analysis
                )
            
            # Step 6: Perform competitive analysis
            competitive_analysis = await self.market_analyzer.analyze_competition(
                processed_concept, market_insights
            )
            
            # Step 7: Generate financial projections (if requested)
            financial_projections = None
            if include_financial:
                financial_projections = await self._generate_financial_projections(
                    processed_concept, market_insights, scores
                )
            
            # Step 8: Assess risks
            risk_assessment = await self._assess_risks(processed_concept, market_insights, scores)
            
            # Step 9: Generate executive summary and recommendations
            executive_summary, recommendations, next_steps = await self._generate_summary_and_recommendations(
                processed_concept, scores, market_insights, competitive_analysis
            )
            
            # Step 10: Compile final result
            evaluation_result = EvaluationResult(
                overall_success_score=scores["overall_success_score"],
                market_demand_score=scores["market_demand_score"],
                concept_viability_score=scores["concept_viability_score"],
                execution_difficulty_score=scores["execution_difficulty_score"],
                market_insights=market_insights,
                branding_recommendations=branding_recommendations or BrandingRecommendations(
                    brand_positioning="Not generated",
                    content_strategy="Not generated"
                ),
                competitive_analysis=competitive_analysis,
                financial_projections=financial_projections or {},
                risk_assessment=risk_assessment,
                executive_summary=executive_summary,
                key_recommendations=recommendations,
                next_steps=next_steps,
                confidence_level=scores.get("confidence_level", 75.0)
            )
            
            logger.info(f"Evaluation completed. Overall success score: {scores['overall_success_score']:.1f}")
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Error during business evaluation: {str(e)}")
            raise
    
    async def _calculate_core_scores(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights,
        product_analysis: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """Calculate core evaluation scores."""
        
        # Prepare context for AI scoring
        context = {
            "concept": concept.concept_description,
            "demographics": {
                "age_range": f"{concept.target_demographics.age_min}-{concept.target_demographics.age_max}",
                "income": concept.target_demographics.income_range,
                "location": concept.target_demographics.location,
                "interests": concept.target_demographics.interests
            },
            "market_insights": {
                "competition_level": market_insights.competition_level,
                "demographic_fit": market_insights.demographic_fit_score,
                "location_demand": market_insights.location_demand_score,
                "trends": market_insights.market_trends
            },
            "product": {
                "description": concept.product_info.description,
                "features": concept.product_info.features,
                "analysis": product_analysis
            }
        }
        
        scoring_prompt = f"""
        Analyze the following business concept and provide numerical scores (0-100) for each category:

        Business Concept: {context['concept']}
        Target Demographics: {context['demographics']}
        Market Context: {context['market_insights']}
        Product Information: {context['product']}

        Please provide scores for:
        1. Market Demand Score (0-100): How much demand exists for this product/service
        2. Concept Viability Score (0-100): How viable and realistic the concept is
        3. Execution Difficulty Score (0-100): How difficult it would be to execute (higher = more difficult)
        4. Overall Success Score (0-100): Overall probability of business success

        Consider factors like:
        - Market size and growth potential
        - Competition level and market saturation
        - Target demographic alignment
        - Product-market fit
        - Execution complexity and resource requirements
        - Geographic market conditions
        - Current trends and timing

        Respond with only the numerical scores in this format:
        Market Demand Score: XX
        Concept Viability Score: XX
        Execution Difficulty Score: XX
        Overall Success Score: XX
        Confidence Level: XX
        """
        
        try:
            response = await self.ai_client.generate_text(scoring_prompt)
            scores = self._parse_scores(response)
            
            # Validate and adjust scores if needed
            for key, value in scores.items():
                if not 0 <= value <= 100:
                    logger.warning(f"Invalid score for {key}: {value}. Clamping to valid range.")
                    scores[key] = max(0, min(100, value))
            
            return scores
            
        except Exception as e:
            logger.error(f"Error calculating scores: {str(e)}")
            # Return default scores if AI fails
            return {
                "market_demand_score": 50.0,
                "concept_viability_score": 50.0,
                "execution_difficulty_score": 50.0,
                "overall_success_score": 50.0,
                "confidence_level": 25.0
            }
    
    def _parse_scores(self, response: str) -> Dict[str, float]:
        """Parse scores from AI response."""
        scores = {}
        lines = response.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                try:
                    score = float(value.strip())
                    scores[key] = score
                except ValueError:
                    continue
        
        # Ensure all required scores are present
        required_scores = [
            "market_demand_score", "concept_viability_score", 
            "execution_difficulty_score", "overall_success_score", "confidence_level"
        ]
        
        for score_key in required_scores:
            if score_key not in scores:
                scores[score_key] = 50.0  # Default score
        
        return scores
    
    async def _generate_financial_projections(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights,
        scores: Dict[str, float]
    ):
        """Generate financial projections."""
        # This would be implemented with more sophisticated financial modeling
        # For now, return a placeholder
        from ..models.evaluation import FinancialProjections
        
        return FinancialProjections(
            startup_costs="$10,000 - $50,000",
            revenue_projections={
                "Year 1": "$50,000 - $100,000",
                "Year 2": "$100,000 - $250,000",
                "Year 3": "$200,000 - $500,000"
            },
            break_even_timeline="12-18 months",
            funding_recommendations=["Bootstrap", "Angel investment", "Small business loan"],
            cost_structure=["Product development", "Marketing", "Operations", "Personnel"]
        )
    
    async def _assess_risks(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights,
        scores: Dict[str, float]
    ):
        """Assess business risks."""
        from ..models.evaluation import RiskAssessment
        
        # Generate risk assessment using AI
        risk_prompt = f"""
        Analyze the risks for this business concept:
        
        Concept: {concept.concept_description}
        Market Competition: {market_insights.competition_level}
        Target Market: {concept.target_demographics.location}
        
        Identify and categorize risks as high, medium, or low priority.
        Also suggest mitigation strategies and critical success factors.
        """
        
        try:
            response = await self.ai_client.generate_text(risk_prompt)
            # Parse response and create structured risk assessment
            # For now, return a basic structure
            return RiskAssessment(
                high_risks=["Market competition", "Customer acquisition"],
                medium_risks=["Regulatory changes", "Economic downturn"],
                low_risks=["Technology obsolescence"],
                mitigation_strategies={
                    "Market competition": "Focus on unique value proposition",
                    "Customer acquisition": "Develop strong marketing strategy"
                },
                success_factors=["Product-market fit", "Strong execution", "Adequate funding"]
            )
        except Exception as e:
            logger.error(f"Error assessing risks: {str(e)}")
            return RiskAssessment()
    
    async def _generate_summary_and_recommendations(
        self,
        concept: BusinessConcept,
        scores: Dict[str, float],
        market_insights: MarketInsights,
        competitive_analysis
    ) -> tuple:
        """Generate executive summary and recommendations."""
        
        summary_prompt = f"""
        Create an executive summary and recommendations for this business evaluation:
        
        Business Concept: {concept.concept_description}
        Overall Success Score: {scores['overall_success_score']:.1f}/100
        Market Demand Score: {scores['market_demand_score']:.1f}/100
        Competition Level: {market_insights.competition_level}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}, {concept.target_demographics.location}
        
        Provide:
        1. A concise executive summary (2-3 paragraphs)
        2. 5-7 key recommendations
        3. 5-7 immediate next steps
        """
        
        try:
            response = await self.ai_client.generate_text(summary_prompt)
            
            # Parse the response (simplified parsing)
            parts = response.split('\n\n')
            executive_summary = parts[0] if parts else "Summary not available"
            
            # Extract recommendations and next steps (simplified)
            recommendations = [
                "Conduct detailed market research",
                "Develop minimum viable product",
                "Test with target audience",
                "Secure initial funding",
                "Build strong team"
            ]
            
            next_steps = [
                "Validate product-market fit",
                "Create business plan",
                "Develop prototype",
                "Identify key partnerships",
                "Plan go-to-market strategy"
            ]
            
            return executive_summary, recommendations, next_steps
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Summary not available", [], []