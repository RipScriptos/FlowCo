"""AI client for handling different AI service providers."""

import asyncio
import logging
from typing import Optional, Dict, Any, List
import base64
from io import BytesIO

from ..core.config import config

logger = logging.getLogger(__name__)


class AIClient:
    """Unified client for different AI services."""
    
    def __init__(self):
        """Initialize AI client."""
        self.openai_client = None
        self.anthropic_client = None
        self.ollama_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize available AI clients."""
        # OpenAI client
        if config.get("ai.openai_api_key"):
            try:
                import openai
                self.openai_client = openai.AsyncOpenAI(
                    api_key=config.get("ai.openai_api_key")
                )
                logger.info("OpenAI client initialized")
            except ImportError:
                logger.warning("OpenAI library not available")
        
        # Anthropic client
        if config.get("ai.anthropic_api_key"):
            try:
                import anthropic
                self.anthropic_client = anthropic.AsyncAnthropic(
                    api_key=config.get("ai.anthropic_api_key")
                )
                logger.info("Anthropic client initialized")
            except ImportError:
                logger.warning("Anthropic library not available")
        
        # Ollama client (for local models)
        if config.get("ai.use_local_models"):
            try:
                import ollama
                self.ollama_client = ollama.AsyncClient(
                    host=config.get("ai.ollama_base_url")
                )
                logger.info("Ollama client initialized")
            except ImportError:
                logger.warning("Ollama library not available")
    
    async def generate_text(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using the best available AI service.
        
        Args:
            prompt: The input prompt
            model: Specific model to use (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        model = model or config.get("ai.default_model", "gpt-3.5-turbo")
        
        # Try OpenAI first
        if self.openai_client and ("gpt" in model.lower() or model.startswith("gpt")):
            return await self._generate_openai(prompt, model, max_tokens, temperature)
        
        # Try Anthropic
        if self.anthropic_client and "claude" in model.lower():
            return await self._generate_anthropic(prompt, model, max_tokens, temperature)
        
        # Try Ollama for local models
        if self.ollama_client and config.get("ai.use_local_models"):
            return await self._generate_ollama(prompt, model, max_tokens, temperature)
        
        # Fallback to any available service
        if self.openai_client:
            return await self._generate_openai(prompt, "gpt-3.5-turbo", max_tokens, temperature)
        elif self.anthropic_client:
            return await self._generate_anthropic(prompt, "claude-3-haiku-20240307", max_tokens, temperature)
        elif self.ollama_client:
            return await self._generate_ollama(prompt, "llama2", max_tokens, temperature)
        
        raise RuntimeError("No AI service available. Please configure API keys or local models.")
    
    async def analyze_image(
        self, 
        image_data: bytes, 
        prompt: str,
        model: Optional[str] = None
    ) -> str:
        """
        Analyze an image with AI vision capabilities.
        
        Args:
            image_data: Raw image data
            prompt: Analysis prompt
            model: Specific model to use
            
        Returns:
            Analysis result
        """
        model = model or "gpt-4-vision-preview"
        
        # Convert image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        if self.openai_client and "gpt" in model.lower():
            return await self._analyze_image_openai(image_b64, prompt, model)
        elif self.anthropic_client and "claude" in model.lower():
            return await self._analyze_image_anthropic(image_b64, prompt, model)
        
        # Fallback: describe image without vision model
        return await self.generate_text(
            f"Based on this prompt about an image: {prompt}\n"
            "Please provide a general analysis assuming this is a product image."
        )
    
    async def _generate_openai(
        self, 
        prompt: str, 
        model: str, 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate text using OpenAI."""
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation error: {str(e)}")
            raise
    
    async def _generate_anthropic(
        self, 
        prompt: str, 
        model: str, 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate text using Anthropic."""
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation error: {str(e)}")
            raise
    
    async def _generate_ollama(
        self, 
        prompt: str, 
        model: str, 
        max_tokens: int, 
        temperature: float
    ) -> str:
        """Generate text using Ollama."""
        try:
            response = await self.ollama_client.generate(
                model=model,
                prompt=prompt,
                options={
                    "num_predict": max_tokens,
                    "temperature": temperature
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation error: {str(e)}")
            raise
    
    async def _analyze_image_openai(
        self, 
        image_b64: str, 
        prompt: str, 
        model: str
    ) -> str:
        """Analyze image using OpenAI vision."""
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI image analysis error: {str(e)}")
            raise
    
    async def _analyze_image_anthropic(
        self, 
        image_b64: str, 
        prompt: str, 
        model: str
    ) -> str:
        """Analyze image using Anthropic vision."""
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_b64
                                }
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic image analysis error: {str(e)}")
            raise
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        models = []
        
        if self.openai_client:
            models.extend([
                "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4-vision-preview"
            ])
        
        if self.anthropic_client:
            models.extend([
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229", 
                "claude-3-haiku-20240307"
            ])
        
        if self.ollama_client:
            models.extend(["llama2", "mistral", "codellama"])
        
        return models
    
    def is_available(self) -> bool:
        """Check if any AI service is available."""
        return bool(self.openai_client or self.anthropic_client or self.ollama_client)