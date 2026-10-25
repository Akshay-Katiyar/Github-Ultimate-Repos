"""
scripts.cli - Command Line Interface & Model Context Protocol (MCP) Service
Provides interactive search, ranking, multi-agent recommendation, and JSON-RPC tooling.
"""

from .ultimate_agent_cli import (
    main,
    sanitize_csv_value,
    sanitize_csv_row,
    get_connection,
)

__all__ = [
    "main",
    "sanitize_csv_value",
    "sanitize_csv_row",
    "get_connection",
]
