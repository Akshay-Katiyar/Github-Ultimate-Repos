"""
scripts.inventory - Catalog Data Ingestion, SQLite Building & Taxonomy Tools
Handles SQLite registry construction, FTS5 index creation, discipline definitions, and catalog metrics.
"""

from .calculate_metrics import get_stats

__all__ = [
    "get_stats",
]
