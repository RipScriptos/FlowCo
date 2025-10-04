"""
FlowCo - AI Business Success Evaluation Model

A comprehensive AI system that predicts business concept success within
specified target demographics and geographic locations.
"""

__version__ = "1.0.0"
__author__ = "FlowCo Team"
__description__ = "AI Business Success Evaluation Model"

from .core.engine import BusinessEvaluationEngine
from .core.config import Config

__all__ = ["BusinessEvaluationEngine", "Config"]