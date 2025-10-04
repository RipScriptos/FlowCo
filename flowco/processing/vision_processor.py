"""Vision processing for product image analysis."""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import base64

from PIL import Image
from io import BytesIO
import cv2
import numpy as np

from ..models.business import ProductInfo
from ..core.ai_client import AIClient
from ..core.config import config

logger = logging.getLogger(__name__)


class VisionProcessor:
    """Processes and analyzes product images."""
    
    def __init__(self):
        """Initialize vision processor."""
        self.ai_client = AIClient()
        self.max_dimension = 1024  # Max image dimension for processing
    
    async def analyze_product_image(self, product_info: ProductInfo) -> Dict[str, Any]:
        """
        Analyze product image and extract insights.
        
        Args:
            product_info: Product information with image
            
        Returns:
            Analysis results including visual features, style, and recommendations
        """
        logger.info("Starting product image analysis")
        
        try:
            # Load image data
            image_data = await self._load_image_data(product_info)
            if not image_data:
                logger.warning("No valid image data found")
                return {"error": "No valid image data"}
            
            # Resize image if needed
            processed_image = self._preprocess_image(image_data)
            
            # Perform AI-based analysis
            ai_analysis = await self._analyze_with_ai(processed_image, product_info)
            
            # Perform computer vision analysis
            cv_analysis = self._analyze_with_cv(processed_image)
            
            # Combine results
            analysis_result = {
                "ai_analysis": ai_analysis,
                "visual_features": cv_analysis,
                "image_quality": self._assess_image_quality(processed_image),
                "recommendations": self._generate_image_recommendations(ai_analysis, cv_analysis)
            }
            
            logger.info("Product image analysis completed")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing product image: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    async def _load_image_data(self, product_info: ProductInfo) -> Optional[bytes]:
        """Load image data from file path or direct data."""
        
        if product_info.image_data:
            return product_info.image_data
        
        if product_info.image_path:
            try:
                with open(product_info.image_path, 'rb') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error loading image from path {product_info.image_path}: {str(e)}")
        
        return None
    
    def _preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess image for analysis."""
        
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        if max(image.size) > self.max_dimension:
            ratio = self.max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array for OpenCV
        return np.array(image)
    
    async def _analyze_with_ai(self, image: np.ndarray, product_info: ProductInfo) -> Dict[str, Any]:
        """Analyze image using AI vision models."""
        
        # Convert numpy array back to bytes for AI analysis
        pil_image = Image.fromarray(image)
        from io import BytesIO
        buffer = BytesIO()
        pil_image.save(buffer, format='JPEG', quality=85)
        image_bytes = buffer.getvalue()
        
        analysis_prompt = f"""
        Analyze this product image and provide detailed insights:
        
        Product Context:
        - Name: {product_info.name or 'Unknown'}
        - Description: {product_info.description or 'Not provided'}
        - Features: {', '.join(product_info.features) if product_info.features else 'None listed'}
        
        Please analyze and provide:
        1. Product Category: What type of product is this?
        2. Visual Appeal: Rate the visual appeal (1-10) and explain
        3. Design Quality: Assess the design quality and professionalism
        4. Target Audience: Who would this product appeal to?
        5. Strengths: What are the visual strengths?
        6. Weaknesses: What could be improved visually?
        7. Market Positioning: How would you position this product?
        8. Branding Suggestions: What branding approach would work?
        
        Provide specific, actionable insights based on what you see in the image.
        """
        
        try:
            response = await self.ai_client.analyze_image(image_bytes, analysis_prompt)
            return self._parse_ai_analysis(response)
        except Exception as e:
            logger.error(f"AI image analysis failed: {str(e)}")
            return {"error": f"AI analysis failed: {str(e)}"}
    
    def _analyze_with_cv(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze image using computer vision techniques."""
        
        try:
            # Convert to different color spaces
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Color analysis
            color_analysis = self._analyze_colors(image, hsv)
            
            # Texture analysis
            texture_analysis = self._analyze_texture(gray)
            
            # Edge and shape analysis
            edge_analysis = self._analyze_edges(gray)
            
            # Composition analysis
            composition_analysis = self._analyze_composition(image)
            
            return {
                "colors": color_analysis,
                "texture": texture_analysis,
                "edges": edge_analysis,
                "composition": composition_analysis,
                "dimensions": {"width": image.shape[1], "height": image.shape[0]}
            }
            
        except Exception as e:
            logger.error(f"Computer vision analysis failed: {str(e)}")
            return {"error": f"CV analysis failed: {str(e)}"}
    
    def _analyze_colors(self, image: np.ndarray, hsv: np.ndarray) -> Dict[str, Any]:
        """Analyze color properties of the image."""
        
        # Dominant colors
        pixels = image.reshape(-1, 3)
        from sklearn.cluster import KMeans
        
        try:
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixels)
            dominant_colors = kmeans.cluster_centers_.astype(int).tolist()
        except:
            dominant_colors = []
        
        # Color distribution
        color_hist = cv2.calcHist([hsv], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
        
        # Average color
        avg_color = np.mean(image, axis=(0, 1)).astype(int).tolist()
        
        # Color variance (measure of color diversity)
        color_variance = np.var(image, axis=(0, 1)).tolist()
        
        return {
            "dominant_colors": dominant_colors,
            "average_color": avg_color,
            "color_variance": color_variance,
            "color_diversity": float(np.mean(color_variance))
        }
    
    def _analyze_texture(self, gray: np.ndarray) -> Dict[str, Any]:
        """Analyze texture properties."""
        
        # Calculate texture using Local Binary Pattern
        try:
            from skimage.feature import local_binary_pattern
            lbp = local_binary_pattern(gray, 24, 8, method='uniform')
            texture_hist = np.histogram(lbp.ravel(), bins=26)[0]
            texture_uniformity = np.sum(texture_hist[:25]) / np.sum(texture_hist)
        except:
            texture_uniformity = 0.5
        
        # Edge density as texture measure
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Contrast measure
        contrast = gray.std()
        
        return {
            "texture_uniformity": float(texture_uniformity),
            "edge_density": float(edge_density),
            "contrast": float(contrast),
            "texture_complexity": "high" if edge_density > 0.1 else "medium" if edge_density > 0.05 else "low"
        }
    
    def _analyze_edges(self, gray: np.ndarray) -> Dict[str, Any]:
        """Analyze edge and shape properties."""
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze shapes
        shape_count = len(contours)
        
        # Calculate edge strength
        edge_strength = np.mean(edges)
        
        # Find dominant shapes
        shape_types = []
        for contour in contours[:10]:  # Analyze top 10 contours
            if len(contour) > 5:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                vertices = len(approx)
                
                if vertices == 3:
                    shape_types.append("triangle")
                elif vertices == 4:
                    shape_types.append("rectangle")
                elif vertices > 8:
                    shape_types.append("circle")
                else:
                    shape_types.append("polygon")
        
        return {
            "edge_strength": float(edge_strength),
            "shape_count": shape_count,
            "dominant_shapes": list(set(shape_types)),
            "geometric_complexity": "high" if shape_count > 20 else "medium" if shape_count > 5 else "low"
        }
    
    def _analyze_composition(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze image composition."""
        
        height, width = image.shape[:2]
        
        # Rule of thirds analysis
        third_h, third_w = height // 3, width // 3
        
        # Calculate brightness in different regions
        regions = {
            "top_left": image[:third_h, :third_w],
            "top_center": image[:third_h, third_w:2*third_w],
            "top_right": image[:third_h, 2*third_w:],
            "center": image[third_h:2*third_h, third_w:2*third_w],
            "bottom": image[2*third_h:, :]
        }
        
        region_brightness = {}
        for region_name, region in regions.items():
            region_brightness[region_name] = float(np.mean(region))
        
        # Overall composition balance
        balance_score = 1.0 - (np.std(list(region_brightness.values())) / 255.0)
        
        return {
            "aspect_ratio": width / height,
            "region_brightness": region_brightness,
            "balance_score": float(balance_score),
            "composition_quality": "good" if balance_score > 0.7 else "fair" if balance_score > 0.5 else "poor"
        }
    
    def _assess_image_quality(self, image: np.ndarray) -> Dict[str, Any]:
        """Assess overall image quality."""
        
        # Convert to grayscale for quality metrics
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Sharpness (Laplacian variance)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Brightness
        brightness = np.mean(gray)
        
        # Contrast
        contrast = gray.std()
        
        # Overall quality score
        quality_score = min(100, (sharpness / 1000 * 40) + (min(brightness, 255-brightness) / 127.5 * 30) + (contrast / 127.5 * 30))
        
        return {
            "sharpness": float(sharpness),
            "brightness": float(brightness),
            "contrast": float(contrast),
            "overall_quality": float(quality_score),
            "quality_rating": "excellent" if quality_score > 80 else "good" if quality_score > 60 else "fair" if quality_score > 40 else "poor"
        }
    
    def _parse_ai_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI analysis response into structured data."""
        
        # Simple parsing - in production, this would be more sophisticated
        analysis = {
            "raw_response": response,
            "product_category": "Unknown",
            "visual_appeal_score": 5,
            "design_quality": "Fair",
            "target_audience": "General",
            "strengths": [],
            "weaknesses": [],
            "market_positioning": "Standard",
            "branding_suggestions": []
        }
        
        # Extract key information using simple text parsing
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for section headers
            if 'product category' in line.lower():
                current_section = 'category'
            elif 'visual appeal' in line.lower():
                current_section = 'appeal'
            elif 'design quality' in line.lower():
                current_section = 'quality'
            elif 'target audience' in line.lower():
                current_section = 'audience'
            elif 'strengths' in line.lower():
                current_section = 'strengths'
            elif 'weaknesses' in line.lower():
                current_section = 'weaknesses'
            elif 'market positioning' in line.lower():
                current_section = 'positioning'
            elif 'branding' in line.lower():
                current_section = 'branding'
            
            # Extract content based on current section
            if current_section and ':' in line:
                content = line.split(':', 1)[1].strip()
                if content:
                    if current_section == 'category':
                        analysis['product_category'] = content
                    elif current_section == 'appeal':
                        # Try to extract numeric score
                        import re
                        score_match = re.search(r'(\d+)', content)
                        if score_match:
                            analysis['visual_appeal_score'] = int(score_match.group(1))
                    elif current_section == 'quality':
                        analysis['design_quality'] = content
                    elif current_section == 'audience':
                        analysis['target_audience'] = content
                    elif current_section == 'positioning':
                        analysis['market_positioning'] = content
        
        return analysis
    
    def _generate_image_recommendations(self, ai_analysis: Dict[str, Any], cv_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on image analysis."""
        
        recommendations = []
        
        # Quality-based recommendations
        if cv_analysis.get("image_quality", {}).get("overall_quality", 50) < 60:
            recommendations.append("Consider using a higher quality image with better lighting and focus")
        
        # Color recommendations
        color_diversity = cv_analysis.get("colors", {}).get("color_diversity", 0)
        if color_diversity < 1000:
            recommendations.append("Add more visual interest with varied colors or textures")
        
        # Composition recommendations
        composition_quality = cv_analysis.get("composition", {}).get("composition_quality", "fair")
        if composition_quality == "poor":
            recommendations.append("Improve image composition by following the rule of thirds")
        
        # AI-based recommendations
        if ai_analysis.get("visual_appeal_score", 5) < 6:
            recommendations.append("Enhance visual appeal through better styling or presentation")
        
        # Generic recommendations
        recommendations.extend([
            "Ensure the product is the main focus of the image",
            "Use consistent lighting and background across product images",
            "Consider multiple angles or lifestyle shots to showcase the product"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations