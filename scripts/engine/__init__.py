"""
scripts.engine - Stack Blueprint & Repository Recommendation Engine
Provides intent-based repository recommendations, explainable multi-factor scoring,
trade-off evaluations, and curated technology stack blueprints.
"""

from .recommendation_engine import (
    RecommendationEngine,
    INTENT_TAXONOMY,
    STOPWORDS,
    RecommendationEngine as StackRecommendationEngine,
)

__all__ = [
    "RecommendationEngine",
    "StackRecommendationEngine",
    "INTENT_TAXONOMY",
    "STOPWORDS",
]
