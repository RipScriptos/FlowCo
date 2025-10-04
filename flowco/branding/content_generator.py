"""Branding and marketing content generation."""

import logging
from typing import Dict, Any, List, Optional
import random
import colorsys

from ..models.business import BusinessConcept
from ..models.evaluation import BrandingRecommendations, MarketInsights
from ..core.ai_client import AIClient

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates branding and marketing content."""
    
    def __init__(self):
        """Initialize content generator."""
        self.ai_client = AIClient()
        
        # Color palettes for different business types
        self.color_palettes = {
            "technology": ["#007ACC", "#4A90E2", "#50C878", "#FF6B35", "#2E3440"],
            "retail": ["#E74C3C", "#F39C12", "#27AE60", "#8E44AD", "#34495E"],
            "food_beverage": ["#E67E22", "#C0392B", "#F1C40F", "#27AE60", "#8B4513"],
            "health_fitness": ["#2ECC71", "#3498DB", "#E74C3C", "#F39C12", "#95A5A6"],
            "education": ["#3498DB", "#9B59B6", "#E67E22", "#1ABC9C", "#34495E"],
            "entertainment": ["#E91E63", "#9C27B0", "#FF5722", "#FFC107", "#607D8B"],
            "finance": ["#2C3E50", "#34495E", "#1ABC9C", "#3498DB", "#95A5A6"],
            "professional_services": ["#34495E", "#2C3E50", "#3498DB", "#1ABC9C", "#95A5A6"],
            "default": ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6"]
        }
    
    async def generate_branding_recommendations(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights,
        product_analysis: Optional[Dict[str, Any]] = None
    ) -> BrandingRecommendations:
        """
        Generate comprehensive branding recommendations.
        
        Args:
            concept: Business concept
            market_insights: Market analysis results
            product_analysis: Optional product image analysis
            
        Returns:
            Branding recommendations
        """
        logger.info("Generating branding recommendations")
        
        try:
            # Generate brand positioning
            brand_positioning = await self._generate_brand_positioning(concept, market_insights)
            
            # Generate key messaging
            key_messaging = await self._generate_key_messaging(concept, market_insights)
            
            # Generate visual identity suggestions
            visual_identity = await self._generate_visual_identity_suggestions(concept, product_analysis)
            
            # Recommend marketing channels
            marketing_channels = await self._recommend_marketing_channels(concept, market_insights)
            
            # Generate content strategy
            content_strategy = await self._generate_content_strategy(concept, market_insights)
            
            # Generate logo concepts
            logo_concepts = await self._generate_logo_concepts(concept)
            
            # Generate color palette
            color_palette = self._generate_color_palette(concept)
            
            # Generate commercial script
            commercial_script = await self._generate_commercial_script(concept, brand_positioning)
            
            return BrandingRecommendations(
                brand_positioning=brand_positioning,
                key_messaging=key_messaging,
                visual_identity_suggestions=visual_identity,
                marketing_channels=marketing_channels,
                content_strategy=content_strategy,
                logo_concepts=logo_concepts,
                color_palette=color_palette,
                commercial_script=commercial_script
            )
            
        except Exception as e:
            logger.error(f"Error generating branding recommendations: {str(e)}")
            return BrandingRecommendations(
                brand_positioning="Brand positioning unavailable",
                content_strategy="Content strategy unavailable"
            )
    
    async def _generate_brand_positioning(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights
    ) -> str:
        """Generate brand positioning statement."""
        
        positioning_prompt = f"""
        Create a brand positioning statement for this business concept:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}, {concept.target_demographics.location}
        Competition Level: {market_insights.competition_level}
        Key Market Trends: {', '.join(market_insights.market_trends[:3])}
        
        Create a clear, compelling brand positioning statement that:
        1. Defines the target audience
        2. Identifies the category/market
        3. States the unique value proposition
        4. Differentiates from competitors
        
        Format as a concise positioning statement (2-3 sentences).
        """
        
        try:
            response = await self.ai_client.generate_text(positioning_prompt, max_tokens=200)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating brand positioning: {str(e)}")
            return "Brand positioning statement unavailable"
    
    async def _generate_key_messaging(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights
    ) -> List[str]:
        """Generate key marketing messages."""
        
        messaging_prompt = f"""
        Generate key marketing messages for this business concept:
        
        Business Concept: {concept.concept_description}
        Product Features: {', '.join(concept.product_info.features) if concept.product_info.features else 'Not specified'}
        Competitive Advantages: {', '.join(concept.competitive_advantages) if concept.competitive_advantages else 'Not specified'}
        Target Audience: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        
        Create 5-7 key marketing messages that:
        1. Highlight unique benefits
        2. Address customer pain points
        3. Emphasize value proposition
        4. Resonate with target audience
        5. Differentiate from competitors
        
        Format as short, punchy messages, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(messaging_prompt, max_tokens=300)
            messages = self._parse_list_response(response)
            return messages[:7]
        except Exception as e:
            logger.error(f"Error generating key messaging: {str(e)}")
            return ["Key messaging unavailable"]
    
    async def _generate_visual_identity_suggestions(
        self, 
        concept: BusinessConcept, 
        product_analysis: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate visual identity suggestions."""
        
        visual_prompt = f"""
        Generate visual identity suggestions for this business concept:
        
        Business Concept: {concept.concept_description}
        Product Category: {concept.product_info.category or 'General'}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        Product Analysis: {product_analysis.get('ai_analysis', {}).get('design_quality', 'Not available') if product_analysis else 'Not available'}
        
        Suggest visual identity elements including:
        1. Overall design style (modern, classic, minimalist, etc.)
        2. Typography recommendations
        3. Imagery style
        4. Visual tone and mood
        5. Brand personality expression
        
        Format as specific suggestions, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(visual_prompt, max_tokens=250)
            suggestions = self._parse_list_response(response)
            return suggestions[:6]
        except Exception as e:
            logger.error(f"Error generating visual identity suggestions: {str(e)}")
            return ["Visual identity suggestions unavailable"]
    
    async def _recommend_marketing_channels(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights
    ) -> List[str]:
        """Recommend marketing channels."""
        
        channels_prompt = f"""
        Recommend marketing channels for this business concept:
        
        Business Concept: {concept.concept_description}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}, {concept.target_demographics.location}
        Target Interests: {', '.join(concept.target_demographics.interests) if concept.target_demographics.interests else 'Not specified'}
        Market Size: {market_insights.market_size}
        Competition Level: {market_insights.competition_level}
        
        Recommend 5-7 marketing channels considering:
        1. Target audience preferences
        2. Budget efficiency
        3. Market reach potential
        4. Competition level
        5. Local vs. digital opportunities
        
        Format as specific channels, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(channels_prompt, max_tokens=200)
            channels = self._parse_list_response(response)
            return channels[:7]
        except Exception as e:
            logger.error(f"Error recommending marketing channels: {str(e)}")
            return ["Marketing channel recommendations unavailable"]
    
    async def _generate_content_strategy(
        self, 
        concept: BusinessConcept, 
        market_insights: MarketInsights
    ) -> str:
        """Generate content marketing strategy."""
        
        content_prompt = f"""
        Create a content marketing strategy for this business concept:
        
        Business Concept: {concept.concept_description}
        Target Demographics: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        Target Interests: {', '.join(concept.target_demographics.interests) if concept.target_demographics.interests else 'Not specified'}
        Market Trends: {', '.join(market_insights.market_trends[:3])}
        
        Provide a content strategy covering:
        1. Content themes and topics
        2. Content formats and types
        3. Publishing frequency and schedule
        4. Audience engagement approach
        5. Content distribution strategy
        
        Format as a comprehensive strategy (2-3 paragraphs).
        """
        
        try:
            response = await self.ai_client.generate_text(content_prompt, max_tokens=400)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating content strategy: {str(e)}")
            return "Content strategy unavailable"
    
    async def _generate_logo_concepts(self, concept: BusinessConcept) -> List[str]:
        """Generate logo concept ideas."""
        
        logo_prompt = f"""
        Generate logo concept ideas for this business:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Business Name: {concept.product_info.name or 'Not specified'}
        
        Create 5-6 logo concept ideas that:
        1. Reflect the business nature
        2. Appeal to target audience
        3. Are memorable and distinctive
        4. Work across different media
        5. Convey brand personality
        
        Format as concept descriptions, one per line.
        """
        
        try:
            response = await self.ai_client.generate_text(logo_prompt, max_tokens=250)
            concepts = self._parse_list_response(response)
            return concepts[:6]
        except Exception as e:
            logger.error(f"Error generating logo concepts: {str(e)}")
            return ["Logo concept ideas unavailable"]
    
    def _generate_color_palette(self, concept: BusinessConcept) -> List[str]:
        """Generate color palette based on business category."""
        
        # Get category-specific palette
        category = concept.product_info.category
        if category and category.value in self.color_palettes:
            base_palette = self.color_palettes[category.value]
        else:
            base_palette = self.color_palettes["default"]
        
        # Add some variation to the base palette
        palette = base_palette.copy()
        
        # Generate complementary colors
        for color in base_palette[:2]:
            try:
                # Convert hex to RGB
                rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                # Convert to HSV
                hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
                # Create complementary color
                comp_hsv = ((hsv[0] + 0.5) % 1.0, hsv[1], hsv[2])
                comp_rgb = colorsys.hsv_to_rgb(*comp_hsv)
                comp_hex = "#{:02x}{:02x}{:02x}".format(
                    int(comp_rgb[0] * 255),
                    int(comp_rgb[1] * 255),
                    int(comp_rgb[2] * 255)
                )
                if comp_hex not in palette:
                    palette.append(comp_hex)
            except:
                continue
        
        return palette[:8]  # Return up to 8 colors
    
    async def _generate_commercial_script(
        self, 
        concept: BusinessConcept, 
        brand_positioning: str
    ) -> str:
        """Generate a sample commercial script."""
        
        script_prompt = f"""
        Create a 30-second commercial script for this business:
        
        Business Concept: {concept.concept_description}
        Product/Service: {concept.product_info.description or 'Not specified'}
        Brand Positioning: {brand_positioning}
        Target Audience: Age {concept.target_demographics.age_min}-{concept.target_demographics.age_max}, {concept.target_demographics.income_range}
        
        Create an engaging 30-second commercial script that:
        1. Grabs attention in the first 5 seconds
        2. Clearly communicates the value proposition
        3. Includes a strong call to action
        4. Resonates with the target audience
        5. Reflects the brand positioning
        
        Format as a proper script with scene descriptions and dialogue.
        """
        
        try:
            response = await self.ai_client.generate_text(script_prompt, max_tokens=400)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating commercial script: {str(e)}")
            return "Commercial script unavailable"
    
    def _parse_list_response(self, response: str) -> List[str]:
        """Parse list items from AI response."""
        import re
        
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
    
    async def generate_website_copy(self, concept: BusinessConcept, branding: BrandingRecommendations) -> Dict[str, str]:
        """Generate website copy sections."""
        
        copy_prompt = f"""
        Generate website copy for this business:
        
        Business Concept: {concept.concept_description}
        Brand Positioning: {branding.brand_positioning}
        Key Messages: {', '.join(branding.key_messaging[:3])}
        
        Create copy for:
        1. Hero headline (compelling, benefit-focused)
        2. About section (2-3 sentences)
        3. Services/Products section (brief description)
        4. Call-to-action text
        
        Format as:
        HERO: [headline]
        ABOUT: [about text]
        SERVICES: [services text]
        CTA: [call-to-action]
        """
        
        try:
            response = await self.ai_client.generate_text(copy_prompt, max_tokens=300)
            
            # Parse the response
            copy_sections = {}
            lines = response.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('HERO:'):
                    copy_sections['hero'] = line.replace('HERO:', '').strip()
                elif line.startswith('ABOUT:'):
                    copy_sections['about'] = line.replace('ABOUT:', '').strip()
                elif line.startswith('SERVICES:'):
                    copy_sections['services'] = line.replace('SERVICES:', '').strip()
                elif line.startswith('CTA:'):
                    copy_sections['cta'] = line.replace('CTA:', '').strip()
            
            return copy_sections
            
        except Exception as e:
            logger.error(f"Error generating website copy: {str(e)}")
            return {
                'hero': 'Transform Your Business Today',
                'about': 'We provide innovative solutions for modern businesses.',
                'services': 'Our comprehensive services are designed to meet your needs.',
                'cta': 'Get Started Now'
            }