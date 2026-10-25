# Changelog

All notable changes to the **Github Ultimate Repos** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-25

### Added
- **Master Catalog**: Initial public release of 11,730 starred gold-standard repositories across 55 granular DeepTech disciplines.
- **Architectural Workflows**: Concrete 1-line engineering pipeline descriptions for 100% of repositories derived from multi-agent forensic analysis.
- **Interactive Web Explorer**: Single-file standalone HTML explorer (`index.html`) featuring client-side search, filtering, and instant pagination.
- **Machine-Readable Formats**: Full master catalog available in TSV/TXT (`STARRED_REPOSITORIES_CATEGORIZED_LIST.txt`) and CSV (`starred_repos_master_catalog.csv`).
- **Category Matrix**: 55 dedicated Markdown files under `categories/` for seamless browsing on GitHub web UI.
- **Legal & Governance**: Added MIT License (`LICENSE`), Code of Conduct (`CODE_OF_CONDUCT.md`), Security Policy (`SECURITY.md`), and Contribution Guidelines (`CONTRIBUTING.md`).
- **Enterprise Schemas**: Formal JSON Schema definitions (`schemas/repository_schema.json` and `schemas/agent_schema.json`).
- **SQLite FTS5 Registry**: High-performance SQLite database (`registry/agents_registry.db`) enabling sub-5ms full-text and semantic search.
- **Enterprise CLI**: Production-grade search utility (`scripts/cli/ultimate_agent_cli.py`) supporting keyword queries, category filters, and JSON exports.
- **Automated Quality Gates**: Complete unit and integration test suite (`tests/`) ensuring schema compliance and catalog integrity.
- **CI/CD Workflows**: GitHub Actions automation for automated schema validation, security scanning, and registry synchronization.
