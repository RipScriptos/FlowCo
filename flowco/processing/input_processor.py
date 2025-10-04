"""Input processing and validation."""

import re
import logging
from typing import Dict, Any, List
from pathlib import Path

from ..models.business import BusinessConcept, Demographics, ProductInfo
from ..core.config import config

logger = logging.getLogger(__name__)


class InputProcessor:
    """Processes and validates business concept inputs."""
    
    def __init__(self):
        """Initialize input processor."""
        self.max_image_size = config.get("processing.max_image_size", 5242880)  # 5MB
        self.supported_formats = config.get("processing.supported_formats", ["jpg", "jpeg", "png", "webp"])
    
    async def process_business_concept(self, concept: BusinessConcept) -> BusinessConcept:
        """
        Process and validate business concept input.
        
        Args:
            concept: Raw business concept
            
        Returns:
            Processed and validated business concept
        """
        logger.info("Processing business concept input")
        
        # Clean and validate concept description
        concept.concept_description = self._clean_text(concept.concept_description)
        
        # Process demographics
        concept.target_demographics = await self._process_demographics(concept.target_demographics)
        
        # Process product information
        concept.product_info = await self._process_product_info(concept.product_info)
        
        # Extract and clean competitive advantages
        if concept.competitive_advantages:
            concept.competitive_advantages = [
                self._clean_text(advantage) for advantage in concept.competitive_advantages
                if advantage and advantage.strip()
            ]
        
        logger.info("Business concept processing completed")
        return concept
    
    async def _process_demographics(self, demographics: Demographics) -> Demographics:
        """Process and validate demographics."""
        
        # Clean location string
        demographics.location = self._clean_text(demographics.location)
        
        # Standardize location format
        demographics.location = self._standardize_location(demographics.location)
        
        # Clean and validate interests
        if demographics.interests:
            demographics.interests = [
                self._clean_text(interest.lower()) for interest in demographics.interests
                if interest and interest.strip()
            ]
            # Remove duplicates while preserving order
            demographics.interests = list(dict.fromkeys(demographics.interests))
        
        # Clean optional fields
        if demographics.gender:
            demographics.gender = self._clean_text(demographics.gender.lower())
        
        if demographics.education_level:
            demographics.education_level = self._clean_text(demographics.education_level)
        
        if demographics.lifestyle:
            demographics.lifestyle = self._clean_text(demographics.lifestyle)
        
        return demographics
    
    async def _process_product_info(self, product_info: ProductInfo) -> ProductInfo:
        """Process and validate product information."""
        
        # Clean text fields
        if product_info.name:
            product_info.name = self._clean_text(product_info.name)
        
        if product_info.description:
            product_info.description = self._clean_text(product_info.description)
        
        if product_info.price_range:
            product_info.price_range = self._clean_text(product_info.price_range)
        
        # Process features
        if product_info.features:
            product_info.features = [
                self._clean_text(feature) for feature in product_info.features
                if feature and feature.strip()
            ]
        
        # Validate image if provided
        if product_info.image_path:
            product_info.image_path = await self._validate_image_path(product_info.image_path)
        
        if product_info.image_data:
            product_info.image_data = await self._validate_image_data(product_info.image_data)
        
        return product_info
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text input."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\-.,!?()&$%]', '', text)
        
        return text
    
    def _standardize_location(self, location: str) -> str:
        """Standardize location format."""
        if not location:
            return ""
        
        # Basic location standardization
        location = location.title()
        
        # Handle common abbreviations
        abbreviations = {
            'Us': 'US', 'Usa': 'USA', 'Uk': 'UK',
            'Ca': 'CA', 'Ny': 'NY', 'Tx': 'TX', 'Fl': 'FL'
        }
        
        for abbr, full in abbreviations.items():
            location = re.sub(rf'\b{abbr}\b', full, location)
        
        return location
    
    async def _validate_image_path(self, image_path: str) -> str:
        """Validate image file path."""
        if not image_path:
            return ""
        
        path = Path(image_path)
        
        # Check if file exists
        if not path.exists():
            logger.warning(f"Image file not found: {image_path}")
            return ""
        
        # Check file extension
        if path.suffix.lower().lstrip('.') not in self.supported_formats:
            logger.warning(f"Unsupported image format: {path.suffix}")
            return ""
        
        # Check file size
        if path.stat().st_size > self.max_image_size:
            logger.warning(f"Image file too large: {path.stat().st_size} bytes")
            return ""
        
        return str(path.absolute())
    
    async def _validate_image_data(self, image_data: bytes) -> bytes:
        """Validate raw image data."""
        if not image_data:
            return b""
        
        # Check size
        if len(image_data) > self.max_image_size:
            logger.warning(f"Image data too large: {len(image_data)} bytes")
            return b""
        
        # Basic validation - check for common image headers
        if not self._is_valid_image_data(image_data):
            logger.warning("Invalid image data format")
            return b""
        
        return image_data
    
    def _is_valid_image_data(self, data: bytes) -> bool:
        """Check if data appears to be valid image data."""
        if len(data) < 10:
            return False
        
        # Check for common image file signatures
        signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'RIFF',  # WebP (starts with RIFF)
            b'GIF87a',  # GIF87a
            b'GIF89a',  # GIF89a
        ]
        
        for sig in signatures:
            if data.startswith(sig):
                return True
        
        return False
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for analysis."""
        if not text:
            return []
        
        # Simple keyword extraction
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) >= 3]
        
        # Return unique keywords
        return list(dict.fromkeys(keywords))
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis of text."""
        if not text:
            return {"sentiment": "neutral", "confidence": 0.0}
        
        # Simple sentiment analysis using keyword matching
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'innovative', 'unique', 'revolutionary', 'successful', 'profitable',
            'growing', 'popular', 'trending', 'opportunity', 'potential'
        }
        
        negative_words = {
            'bad', 'poor', 'terrible', 'awful', 'difficult', 'challenging',
            'expensive', 'risky', 'saturated', 'declining', 'competitive',
            'limited', 'restricted', 'problematic', 'complex'
        }
        
        words = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.8, (positive_count - negative_count) / len(words) * 10)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.8, (negative_count - positive_count) / len(words) * 10)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count
        }