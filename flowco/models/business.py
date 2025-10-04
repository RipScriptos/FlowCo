"""Business-related data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class IncomeRange(str, Enum):
    """Income range categories."""
    LOW = "low"  # <$30k
    LOWER_MIDDLE = "lower_middle"  # $30k-$50k
    MIDDLE = "middle"  # $50k-$80k
    UPPER_MIDDLE = "upper_middle"  # $80k-$120k
    HIGH = "high"  # >$120k


class BusinessCategory(str, Enum):
    """Business category types."""
    TECHNOLOGY = "technology"
    RETAIL = "retail"
    FOOD_BEVERAGE = "food_beverage"
    HEALTH_FITNESS = "health_fitness"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    FINANCE = "finance"
    REAL_ESTATE = "real_estate"
    AUTOMOTIVE = "automotive"
    FASHION = "fashion"
    HOME_GARDEN = "home_garden"
    TRAVEL = "travel"
    PROFESSIONAL_SERVICES = "professional_services"
    OTHER = "other"


class Demographics(BaseModel):
    """Target demographic information."""
    
    age_min: int = Field(..., ge=0, le=100, description="Minimum age")
    age_max: int = Field(..., ge=0, le=100, description="Maximum age")
    income_range: IncomeRange = Field(..., description="Target income range")
    location: str = Field(..., description="Geographic location (city, state, country)")
    interests: List[str] = Field(default_factory=list, description="Target interests/hobbies")
    gender: Optional[str] = Field(None, description="Target gender (optional)")
    education_level: Optional[str] = Field(None, description="Education level (optional)")
    lifestyle: Optional[str] = Field(None, description="Lifestyle description (optional)")
    
    @field_validator('age_max')
    @classmethod
    def age_max_greater_than_min(cls, v, info):
        if info.data and 'age_min' in info.data and v < info.data['age_min']:
            raise ValueError('age_max must be greater than or equal to age_min')
        return v


class ProductInfo(BaseModel):
    """Product information."""
    
    name: Optional[str] = Field(None, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    image_path: Optional[str] = Field(None, description="Path to product image")
    image_data: Optional[bytes] = Field(None, description="Raw image data")
    category: Optional[BusinessCategory] = Field(None, description="Product category")
    price_range: Optional[str] = Field(None, description="Expected price range")
    features: List[str] = Field(default_factory=list, description="Key product features")
    
    @field_validator('description')
    @classmethod
    def require_description_or_image(cls, v, info):
        if not v and info.data and not info.data.get('image_path') and not info.data.get('image_data'):
            raise ValueError('Either description or image must be provided')
        return v


class BusinessConcept(BaseModel):
    """Complete business concept information."""
    
    concept_description: str = Field(..., description="Business concept description")
    target_demographics: Demographics = Field(..., description="Target demographic information")
    product_info: ProductInfo = Field(..., description="Product information")
    business_model: Optional[str] = Field(None, description="Business model description")
    competitive_advantages: List[str] = Field(default_factory=list, description="Competitive advantages")
    funding_requirements: Optional[str] = Field(None, description="Funding requirements")
    timeline: Optional[str] = Field(None, description="Expected timeline to market")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True