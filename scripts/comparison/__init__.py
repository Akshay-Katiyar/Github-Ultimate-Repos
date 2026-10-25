"""
scripts.comparison - Repository Comparison & Trade-off Engine
"""
from .tradeoff_engine import (
    TradeoffEngine,
    EvaluatedRepository,
    TradeoffEvaluation,
    compare_repositories,
)

__all__ = [
    "TradeoffEngine",
    "EvaluatedRepository",
    "TradeoffEvaluation",
    "compare_repositories",
]
