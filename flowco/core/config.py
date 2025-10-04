"""Configuration management for FlowCo."""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
import yaml


class Config:
    """Configuration manager for FlowCo system."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config_path = config_path
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment and files."""
        # Load environment variables
        load_dotenv()
        
        # Default configuration
        self._config = {
            "ai": {
                "openai_api_key": os.getenv("OPENAI_API_KEY"),
                "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
                "default_model": os.getenv("DEFAULT_AI_MODEL", "gpt-3.5-turbo"),
                "use_local_models": os.getenv("USE_LOCAL_MODELS", "false").lower() == "true",
                "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            },
            "database": {
                "path": os.getenv("DATABASE_PATH", "data/flowco.db"),
            },
            "web": {
                "host": os.getenv("WEB_HOST", "0.0.0.0"),
                "port": int(os.getenv("WEB_PORT", "12000")),
                "debug": os.getenv("DEBUG", "false").lower() == "true",
            },
            "processing": {
                "max_image_size": int(os.getenv("MAX_IMAGE_SIZE", "5242880")),  # 5MB
                "supported_formats": ["jpg", "jpeg", "png", "webp"],
            },
            "research": {
                "enable_web_scraping": os.getenv("ENABLE_WEB_SCRAPING", "true").lower() == "true",
                "max_search_results": int(os.getenv("MAX_SEARCH_RESULTS", "10")),
            }
        }
        
        # Load from config file if provided
        if self.config_path and Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(file_config)
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration with existing."""
        def merge_dict(base: dict, new: dict):
            for key, value in new.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self._config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ai.openai_api_key')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'ai.openai_api_key')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def has_ai_key(self) -> bool:
        """Check if any AI API key is configured."""
        return bool(
            self.get("ai.openai_api_key") or 
            self.get("ai.anthropic_api_key") or
            self.get("ai.use_local_models")
        )
    
    def get_available_models(self) -> list:
        """Get list of available AI models."""
        models = []
        
        if self.get("ai.openai_api_key"):
            models.extend([
                "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
                "gpt-4-vision-preview"
            ])
        
        if self.get("ai.anthropic_api_key"):
            models.extend([
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ])
        
        if self.get("ai.use_local_models"):
            models.extend([
                "llama2", "mistral", "codellama"
            ])
        
        return models
    
    def save_config(self, path: Optional[str] = None):
        """Save current configuration to file.
        
        Args:
            path: Path to save configuration (optional)
        """
        save_path = path or self.config_path or "config.yaml"
        
        with open(save_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)


# Global configuration instance
config = Config()