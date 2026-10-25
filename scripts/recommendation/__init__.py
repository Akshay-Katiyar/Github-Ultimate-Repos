"""
scripts.recommendation - Intelligent Repository Recommendation Engine
Autonomous natural language query decomposition, multi-factor scoring (BM25 + coverage +
maintenance + language + license + deployment), and actionable recommendation cards.
"""

from .recommendation_engine import (
    QueryParser,
    MultiFactorScorer,
    RecommendationCardGenerator,
    RecommendationEngine,
    RecommendationEngine as IntelligentRecommendationEngine,
    format_card_terminal,
    ScoreBreakdown,
    RecommendationCard,
    QueryDecomposition,
    INTENT_ARCHETYPES,
    SEMANTIC_SYNONYMS,
    CATEGORY_AFFINITY_MAP,
)

__all__ = [
    "QueryParser",
    "MultiFactorScorer",
    "RecommendationCardGenerator",
    "RecommendationEngine",
    "IntelligentRecommendationEngine",
    "format_card_terminal",
    "ScoreBreakdown",
    "RecommendationCard",
    "QueryDecomposition",
    "INTENT_ARCHETYPES",
    "SEMANTIC_SYNONYMS",
    "CATEGORY_AFFINITY_MAP",
]
