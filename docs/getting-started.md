# Getting Started with Github Ultimate Repos

Welcome to **Github Ultimate Repos**! This guide covers installation, environment setup, database exploration, and command-line usage.

## Overview

Github Ultimate Repos provides an audited registry of **11,730 starred open-source repositories and multi-agent system blueprints** across **55 DeepTech disciplines**.

All data is available in multiple formats:
- **Interactive Web Explorer**: [index.html](../index.html) (Zero dependencies, pure client-side search).
- **SQLite FTS5 Registry**: [registry/agents_registry.db](../registry/agents_registry.db) (High-performance full-text search).
- **Tabular Datasets**: [starred_repos_master_catalog.csv](../starred_repos_master_catalog.csv) and [STARRED_REPOSITORIES_CATEGORIZED_LIST.txt](../STARRED_REPOSITORIES_CATEGORIZED_LIST.txt).
- **Machine-Readable JSON**: [reports/repository-inventory.json](../reports/repository-inventory.json).

---

## Prerequisites

- **Python 3.9+** (Standard library only; no pip dependencies required for core CLI or registry).
- **SQLite 3.30+** (Compiled with FTS5 enabled; standard in Python 3.9+).
- **Git 2.25+**.

---

## 5-Minute Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/Akshay-Katiyar/Github-Ultimate-Repos.git
cd Github-Ultimate-Repos
```

### 2. Verify or Rebuild the SQLite Registry
The SQLite database is pre-built, but can be regenerated at any time from source CSV:
```bash
python scripts/inventory/build_sqlite_registry.py
```

### 3. Query Catalog Statistics
```bash
python scripts/cli/ultimate_agent_cli.py stats
```

### 4. Search Repositories
Search by keyword, language, or discipline:
```bash
# Keyword search across all 11,730 repositories
python scripts/cli/ultimate_agent_cli.py search "langchain"

# Search with star filter and category constraint
python scripts/cli/ultimate_agent_cli.py search "autonomous agent" --min-stars 20000 --limit 5

# View detailed dossier for a specific repository
python scripts/cli/ultimate_agent_cli.py get "Significant-Gravitas/AutoGPT"
```

### 5. Export Filtered Subsets
```bash
# Export all Robotics repositories with >5,000 stars to JSON
python scripts/cli/ultimate_agent_cli.py export --category "Robotics" --min-stars 5000 --format json --output robotics_top.json
```

---

## Next Steps

- Explore the [Architecture Overview](architecture.md).
- Browse the [Agent Catalog & Discipline Taxonomy](agent-catalog.md).
- Learn about [Testing & Quality Gates](testing.md).
