# Contributing to Github Ultimate Repos

Thank you for your interest in contributing to **Github Ultimate Repos**! This repository is an enterprise-grade catalog and knowledge base of 11,730+ gold-standard repositories and multi-agent system blueprints across 55 DeepTech disciplines.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Suggesting New Repositories & Agent Blueprints](#suggesting-new-repositories--agent-blueprints)
  - [Updating Architectural Workflows](#updating-architectural-workflows)
  - [Reporting Bugs or Metadata Discrepancies](#reporting-bugs-or-metadata-discrepancies)
  - [Improving Documentation & Tooling](#improving-documentation--tooling)
- [Development & Validation Workflow](#development--validation-workflow)
- [Style Guide & Conventions](#style-guide--conventions)
- [Pull Request Process](#pull-request-process)
- [Licensing](#licensing)

---

## Code of Conduct

This project adheres to the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

## How Can I Contribute?

### Suggesting New Repositories & Agent Blueprints

To maintain catalog excellence, we enforce a strict quality threshold:
1. **Star Threshold**: Target repository should generally possess 5,000+ stars or represent critical frontier infrastructure.
2. **Active Maintenance**: Active commits within the past 12 months.
3. **Architecture Workflow**: Every suggested repository must include a verified 1-line architectural workflow pipeline (e.g., `Input -> Core Processing -> Output`).
4. **Schema Compliance**: All entries must validate against `schemas/repository_schema.json`.

Please submit an issue using the [New Repository Submission Template](.github/ISSUE_TEMPLATE/new_agent_submission.yml).

### Updating Architectural Workflows

If an existing repository's architecture has evolved:
1. Locate the entry in `starred_repos_master_catalog.csv` and the corresponding category markdown in `categories/`.
2. Formulate the precise architectural flow adhering to the format: `[Component A] -> [Component B] -> [Component C]`.
3. Verify that changes match the verified technical implementation.

---

## Development & Validation Workflow

### Prerequisites
- Python 3.9+
- Git 2.25+
- SQLite3 (with FTS5 support)

### Local Environment Setup
```bash
# Clone the repository
git clone https://github.com/Akshay-Katiyar/Github-Ultimate-Repos.git
cd Github-Ultimate-Repos

# Verify dependencies (standard library only; zero external heavy dependencies)
python --version
sqlite3 --version
```

### Running Automated Quality Gates
Before submitting any pull request, ensure all test suites pass:

```bash
# Run complete unit and integration test suite
python -m unittest discover tests -v

# Run schema validation
python scripts/inventory/generate_inventory.py --validate-only

# Run registry integrity check
python scripts/cli/ultimate_agent_cli.py stats
```

---

## Style Guide & Conventions

- **Filenames**: Use lowercase with hyphens or underscores (`kebab-case` for docs, `snake_case` for Python).
- **Code Standards**: Adhere to PEP 8 for Python code.
- **Commit Messages**: Follow Conventional Commits:
  - `feat: add AI agent swarm evaluation benchmark`
  - `fix: correct architectural workflow for langchain-ai/langchain`
  - `docs: update getting started guide with CLI examples`
  - `test: add integration test for FTS5 full-text query`

---

## Pull Request Process

1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b feat/my-improvement
   ```
2. Make your additions or improvements.
3. Ensure automated tests pass locally.
4. Ensure the SQLite registry builds cleanly without schema errors:
   ```bash
   python scripts/inventory/build_sqlite_registry.py
   ```
5. Submit a Pull Request targeting `main`. A CI/CD workflow will validate your changes against schema rules.

---

## Licensing

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
