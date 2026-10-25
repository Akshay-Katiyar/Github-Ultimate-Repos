# Configuration & Customization Guide

## Environment Variables

The registry and CLI operate with sensible zero-config defaults, but honor the following environment variables:

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `ULTIMATE_REPOS_DB` | `registry/agents_registry.db` | Override SQLite database location |
| `ULTIMATE_REPOS_CSV` | `starred_repos_master_catalog.csv` | Override source CSV location |
| `ULTIMATE_REPOS_LIMIT` | `10` | Default CLI search result limit |

## SQLite Performance Tuning
The database is built with high-throughput PRAGMAs:
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000; -- 64MB memory cache
```
