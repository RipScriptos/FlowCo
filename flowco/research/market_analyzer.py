"""Market research and analysis functionality."""

import asyncio
import logging
from typing import Dict, Any, List, Optional
import re
import json

import requests
from bs4 import BeautifulSoup
import aiohttp

from ..models.business import BusinessConcept, Demographics
from ..models.evaluation import MarketInsights, CompetitiveAnalysis
from ..core.ai_client import AIClient
from ..core.config import config

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyzes market conditions and competitive landscape."""
    
    def __init__(self):
        """Initialize market analyzer."""
        self.ai_client = AIClient()
        self.enable_web_scraping = config.get("research.enable_web_scraping", True)
        self.max_search_results = config.get("research.max_search_results", 10)
    
    async def analyze_market(
        self, 
        concept: BusinessConcept, 
        product_analysis: Optional[Dict[str, Any]] = None
    ) -> MarketInsights:
        """
        Analyze market conditions for the business concept.
        
        Args:
            concept: Business concept to analyze
            product_analysis: Optional product image analysis results
            
        Returns:
            Market insights and analysis
        """
        logger.info(f"Analyzing market for concept in {concept.target_demographics.location}")
        
        try:
            # Analyze target demographics fit
            demographic_fit = await self._analyze_demographic_fit(concept)
            
            # Analyze location-specific demand
            location_demand = await self._analyze_location_demand(concept)
            
            # Research market trends
            market_trends = await self._research_market_trends(concept)
            
            # Assess competition level
            competition_level = await self._assess_competition_level(concept)
            
            # Analyze market size
            market_size = await self._estimate_market_size(concept)
            
            # Identify seasonal factors
            seasonal_factors = await self._identify_seasonal_factors(concept)
            
            # Research regulatory considerations
            regulatory_considerations = await self._research_regulatory_factors(concept)
            
            # Generate target market analysis
            target_market_analysis = await self._generate_target_market_analysis(
                concept, demographic_fit, location_demand, market_trends
            )
            
            return MarketInsights(
                market_size=market_size,
                competition_level=competition_level,
                market_trends=market_trends,
                seasonal_factors=seasonal_factors,
                regulatory_considerations=regulatory_considerations,
                target_market_analysis=target_market_analysis,
                demographic_fit_score=demographic_fit,
                location_demand_score=location_demand
            )
            
        except Exception as e:
            logger.error(f"Error analyzing market: {str(e)}")
            # Return default insights if analysis fails
            return MarketInsights(
                market_size="Unknown",
                competition_level="medium",
                market_trends=["Unable to determine trends"],
                seasonal_factors=[],
                regulatory_considerations=[],
                target_market_analysis="Market analysis unavailable",
                demographic_fit_score=50.0,
                location_demand_score=50.0
            )
    
    async def analyze_competition(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights
    ) -> CompetitiveAnalysis:
        """
        Analyze competitive landscape.
        
        Args:
            concept: Business concept
            market_insights: Market analysis results
            
        Returns:
            Competitive analysis
        """
        logger.info("Analyzing competitive landscape")
        
        try:
            # Research direct competitors
            direct_competitors = await self._research_direct_competitors(concept)
            
            # Research indirect competitors
            indirect_competitors = await self._research_indirect_competitors(concept)
            
            # Identify competitive advantages
            competitive_advantages = await self._identify_competitive_advantages(concept, direct_competitors)
            
            # Find market gaps
            market_gaps = await self._identify_market_gaps(concept, direct_competitors, market_insights)
            
            # Identify differentiation opportunities
            differentiation_opportunities = await self._identify_differentiation_opportunities(
                concept, direct_competitors, indirect_competitors
            )
            
            return CompetitiveAnalysis(
                direct_competitors=direct_competitors,
                indirect_competitors=indirect_competitors,
                competitive_advantages=competitive_advantages,
                market_gaps=market_gaps,
                differentiation_opportunities=differentiation_opportunities
            )
            
        except Exception as e:
            logger.error(f"Error analyzing competition: {str(e)}")
            return CompetitiveAnalysis()
    
    async def _analyze_demographic_fit(self, concept: BusinessConcept) -> float:
        """Analyze how well the concept fits the target demographics."""
        
        demographics = concept.target_demographics
        
        # Create analysis prompt
        analysis_prompt = f"""
        Analyze how well this business concept fits the target demographics:
        
        Business Concept: {concept.concept_description}
        Product: {concept.product_info.description or 'Not specified'}
        
        Target Demographics:
        - Age: {demographics.age_min}-{demographics.age_max}
        - Income: {demographics.income_range}
        - Location: {demographics.location}
        - Interests: {', '.join(demographics.interests) if demographics.interests else 'Not specified'}
        - Gender: {demographics.gender or 'Not specified'}
        - Education: {demographics.education_level or 'Not specified'}
        
        Rate the demographic fit on a scale of 0-100, considering:
        1. Age appropriateness of the product/service
        2. Income level alignment with pricing expectations
        3. Interest alignment with the concept
        4. Geographic relevance
        5. Lifestyle compatibility
        
        Provide only a numerical score (0-100).
        """
        
        try:
            response = await self.ai_client.generate_text(analysis_prompt, max_tokens=50)
            score = self._extract_score(response)
            return max(0, min(100, score))
        except Exception as e:
            logger.error(f"Error analyzing demographic fit: {str(e)}")
            return 50.0
    
    async def _analyze_location_demand(self, concept: BusinessConcept) -> float:
        """Analyze demand in the target location."""
        
        location = concept.target_demographics.location
        
        # Create location analysis prompt
        location_prompt = f"""
        Analyze the market demand for this business concept in {location}:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Target Location: {location}
        
        Consider:
        1. Local market conditions and economy
        2. Population density and demographics
        3. Competition saturation in the area
        4. Local preferences and culture
        5. Infrastructure and accessibility
        6. Regulatory environment
        
        Rate the location demand on a scale of 0-100.
        Provide only a numerical score (0-100).
        """
        
        try:
            response = await self.ai_client.generate_text(location_prompt, max_tokens=50)
            score = self._extract_score(response)
            return max(0, min(100, score))
        except Exception as e:
            logger.error(f"Error analyzing location demand: {str(e)}")
            return 50.0
    
    async def _research_market_trends(self, concept: BusinessConcept) -> List[str]:
        """Research current market trends relevant to the concept."""
        
        trends_prompt = f"""
        Identify current market trends relevant to this business concept:
        
        Business Concept: {concept.concept_description}
        Product Category: {concept.product_info.category or 'General'}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        
        List 5-7 current market trends that could impact this business, including:
        - Industry trends
        - Consumer behavior trends
        - Technology trends
        - Economic trends
        - Social trends
        
        Format as a simple list, one trend per line.
        """
        
        try:
            response = await self.ai_client.generate_text(trends_prompt, max_tokens=300)
            trends = self._parse_list_response(response)
            return trends[:7]  # Limit to 7 trends
        except Exception as e:
            logger.error(f"Error researching market trends: {str(e)}")
            return ["Unable to determine current trends"]
    
    async def _assess_competition_level(self, concept: BusinessConcept) -> str:
        """Assess the level of competition in the market."""
        
        competition_prompt = f"""
        Assess the competition level for this business concept:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Target Market: {concept.target_demographics.location}
        
        Consider:
        1. Number of existing competitors
        2. Market saturation
        3. Barriers to entry
        4. Brand loyalty in the market
        5. Innovation rate in the industry
        
        Classify competition level as one of: low, medium, high
        Provide only the classification word.
        """
        
        try:
            response = await self.ai_client.generate_text(competition_prompt, max_tokens=20)
            level = response.strip().lower()
            if level in ['low', 'medium', 'high']:
                return level
            return 'medium'
        except Exception as e:
            logger.error(f"Error assessing competition level: {str(e)}")
            return 'medium'
    
    async def _estimate_market_size(self, concept: BusinessConcept) -> str:
        """Estimate the market size for the concept."""
        
        market_size_prompt = f"""
        Estimate the market size for this business concept:
        
        Business Concept: {concept.concept_description}
        Target Location: {concept.target_demographics.location}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        
        Provide a market size estimate considering:
        1. Total addressable market (TAM)
        2. Serviceable addressable market (SAM)
        3. Local market potential
        
        Format as a brief description (e.g., "Small local market ($1M-5M)", "Large regional market ($50M+)", etc.)
        """
        
        try:
            response = await self.ai_client.generate_text(market_size_prompt, max_tokens=100)
            return response.strip()
        except Exception as e:
            logger.error(f"Error estimating market size: {str(e)}")
            return "Market size unknown"
    
    async def _identify_seasonal_factors(self, concept: BusinessConcept) -> List[str]:
        """Identify seasonal factors that might affect the business."""
        
        seasonal_prompt = f"""
        Identify seasonal factors that could affect this business:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Location: {concept.target_demographics.location}
        
        Consider:
        1. Seasonal demand patterns
        2. Weather-related factors
        3. Holiday and event impacts
        4. School calendar effects
        5. Economic cycles
        
        List 3-5 key seasonal factors, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(seasonal_prompt, max_tokens=200)
            factors = self._parse_list_response(response)
            return factors[:5]
        except Exception as e:
            logger.error(f"Error identifying seasonal factors: {str(e)}")
            return []
    
    async def _research_regulatory_factors(self, concept: BusinessConcept) -> List[str]:
        """Research regulatory considerations for the business."""
        
        regulatory_prompt = f"""
        Identify regulatory considerations for this business:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Location: {concept.target_demographics.location}
        
        Consider:
        1. Licensing requirements
        2. Industry regulations
        3. Safety standards
        4. Tax implications
        5. Zoning restrictions
        6. Professional certifications needed
        
        List 3-5 key regulatory considerations, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(regulatory_prompt, max_tokens=200)
            considerations = self._parse_list_response(response)
            return considerations[:5]
        except Exception as e:
            logger.error(f"Error researching regulatory factors: {str(e)}")
            return []
    
    async def _generate_target_market_analysis(
        self, 
        concept: BusinessConcept, 
        demographic_fit: float, 
        location_demand: float, 
        market_trends: List[str]
    ) -> str:
        """Generate comprehensive target market analysis."""
        
        analysis_prompt = f"""
        Provide a comprehensive target market analysis for this business concept:
        
        Business Concept: {concept.concept_description}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}, {concept.target_demographics.location}
        Demographic Fit Score: {demographic_fit}/100
        Location Demand Score: {location_demand}/100
        Key Market Trends: {', '.join(market_trends[:3])}
        
        Provide a 2-3 paragraph analysis covering:
        1. Target market characteristics and size
        2. Market opportunity and potential
        3. Key challenges and considerations
        4. Recommendations for market entry
        """
        
        try:
            response = await self.ai_client.generate_text(analysis_prompt, max_tokens=400)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating target market analysis: {str(e)}")
            return "Target market analysis unavailable"
    
    async def _research_direct_competitors(self, concept: BusinessConcept) -> List[str]:
        """Research direct competitors."""
        
        competitors_prompt = f"""
        Identify direct competitors for this business concept:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Target Market: {concept.target_demographics.location}
        
        List 5-7 direct competitors (companies offering similar products/services to similar customers).
        Include both local and national competitors if relevant.
        Format as company names, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(competitors_prompt, max_tokens=200)
            competitors = self._parse_list_response(response)
            return competitors[:7]
        except Exception as e:
            logger.error(f"Error researching direct competitors: {str(e)}")
            return []
    
    async def _research_indirect_competitors(self, concept: BusinessConcept) -> List[str]:
        """Research indirect competitors."""
        
        indirect_prompt = f"""
        Identify indirect competitors for this business concept:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        
        List 3-5 indirect competitors (companies solving the same customer problem with different approaches).
        Format as company names or categories, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(indirect_prompt, max_tokens=150)
            competitors = self._parse_list_response(response)
            return competitors[:5]
        except Exception as e:
            logger.error(f"Error researching indirect competitors: {str(e)}")
            return []
    
    async def _identify_competitive_advantages(self, concept: BusinessConcept, competitors: List[str]) -> List[str]:
        """Identify competitive advantages."""
        
        advantages_prompt = f"""
        Identify competitive advantages for this business concept:
        
        Business Concept: {concept.concept_description}
        Product Features: {', '.join(concept.product_info.features) if concept.product_info.features else 'Not specified'}
        Listed Advantages: {', '.join(concept.competitive_advantages) if concept.competitive_advantages else 'None listed'}
        Key Competitors: {', '.join(competitors[:3]) if competitors else 'None identified'}
        
        List 3-5 potential competitive advantages, considering:
        1. Unique features or capabilities
        2. Cost advantages
        3. Market positioning
        4. Customer experience
        5. Innovation potential
        
        Format as advantages, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(advantages_prompt, max_tokens=200)
            advantages = self._parse_list_response(response)
            return advantages[:5]
        except Exception as e:
            logger.error(f"Error identifying competitive advantages: {str(e)}")
            return concept.competitive_advantages or []
    
    async def _identify_market_gaps(
        self, 
        concept: BusinessConcept, 
        competitors: List[str], 
        market_insights: MarketInsights
    ) -> List[str]:
        """Identify market gaps and opportunities."""
        
        gaps_prompt = f"""
        Identify market gaps and opportunities for this business concept:
        
        Business Concept: {concept.concept_description}
        Competition Level: {market_insights.competition_level}
        Key Competitors: {', '.join(competitors[:3]) if competitors else 'None identified'}
        Market Trends: {', '.join(market_insights.market_trends[:3])}
        
        List 3-5 market gaps or underserved segments, considering:
        1. Unmet customer needs
        2. Underserved demographics
        3. Geographic gaps
        4. Service/feature gaps
        5. Price point gaps
        
        Format as opportunities, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(gaps_prompt, max_tokens=200)
            gaps = self._parse_list_response(response)
            return gaps[:5]
        except Exception as e:
            logger.error(f"Error identifying market gaps: {str(e)}")
            return []
    
    async def _identify_differentiation_opportunities(
        self, 
        concept: BusinessConcept, 
        direct_competitors: List[str], 
        indirect_competitors: List[str]
    ) -> List[str]:
        """Identify differentiation opportunities."""
        
        differentiation_prompt = f"""
        Identify differentiation opportunities for this business concept:
        
        Business Concept: {concept.concept_description}
        Direct Competitors: {', '.join(direct_competitors[:3]) if direct_competitors else 'None'}
        Indirect Competitors: {', '.join(indirect_competitors[:3]) if indirect_competitors else 'None'}
        
        List 3-5 ways to differentiate from competitors:
        1. Product/service differentiation
        2. Customer experience differentiation
        3. Pricing strategy differentiation
        4. Brand positioning differentiation
        5. Distribution channel differentiation
        
        Format as differentiation strategies, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(differentiation_prompt, max_tokens=200)
            opportunities = self._parse_list_response(response)
            return opportunities[:5]
        except Exception as e:
            logger.error(f"Error identifying differentiation opportunities: {str(e)}")
            return []
    
    def _extract_score(self, response: str) -> float:
        """Extract numerical score from AI response."""
        # Look for numbers in the response
        import re
        numbers = re.findall(r'\d+\.?\d*', response)
        
        if numbers:
            try:
                score = float(numbers[0])
                return max(0, min(100, score))
            except ValueError:
                pass
        
        return 50.0  # Default score
    
    def _parse_list_response(self, response: str) -> List[str]:
        """Parse list items from AI response."""
        lines = response.strip().split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove bullet points, numbers, etc.
            line = re.sub(r'^[\d\.\-\*\+\s]+', '', line).strip()
            
            if line and len(line) > 3:  # Ignore very short items
                items.append(line)
        
        return items