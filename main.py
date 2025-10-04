#!/usr/bin/env python3
"""
FlowCo - AI Business Success Evaluation System

Main entry point for the application.
"""

import logging
import sys
import argparse
from pathlib import Path

import uvicorn

from flowco.web.app import create_app
from flowco.core.config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('flowco.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="FlowCo AI Business Evaluation System")
    parser.add_argument(
        "--host", 
        default=config.get("web.host", "0.0.0.0"),
        help="Host to bind to"
    )
    parser.add_argument(
        "--port", 
        type=int,
        default=config.get("web.port", 12000),
        help="Port to bind to"
    )
    parser.add_argument(
        "--reload", 
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--workers", 
        type=int,
        default=1,
        help="Number of worker processes"
    )
    parser.add_argument(
        "--config", 
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Load custom config if provided
    if args.config:
        from flowco.core.config import Config
        global config
        config = Config(args.config)
    
    # Check if AI services are configured
    if not config.has_ai_key():
        logger.warning(
            "No AI API keys configured. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, "
            "or enable local models in your .env file or configuration."
        )
        print("\n" + "="*60)
        print("⚠️  AI CONFIGURATION REQUIRED")
        print("="*60)
        print("FlowCo requires AI services to function. Please configure at least one:")
        print("\n1. OpenAI API:")
        print("   export OPENAI_API_KEY='your-api-key'")
        print("\n2. Anthropic API:")
        print("   export ANTHROPIC_API_KEY='your-api-key'")
        print("\n3. Local models (Ollama):")
        print("   export USE_LOCAL_MODELS=true")
        print("   export OLLAMA_BASE_URL=http://localhost:11434")
        print("\n4. Create a .env file with your API keys")
        print("="*60)
        
        # Continue anyway for demo purposes
        print("Continuing with limited functionality...")
    
    # Create FastAPI app
    app = create_app()
    
    logger.info(f"Starting FlowCo server on {args.host}:{args.port}")
    logger.info(f"Available models: {config.get_available_models()}")
    
    # Run server
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,
        access_log=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()