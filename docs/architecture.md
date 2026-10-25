# System Architecture & Multi-Agent Swarm Design

Github Ultimate Repos bridges enterprise open-source software discovery with high-capacity autonomous agent workforce orchestration.

## High-Level System Architecture

```mermaid
graph TD
    User([Developer / AI Agent Swarm]) --> CLI[Ultimate Agent CLI<br/>ultimate_agent_cli.py]
    User --> Web[Interactive Web Explorer<br/>index.html]
    User --> Docs[55 Category Markdown Catalogs<br/>categories/]

    subgraph Data Tier
        DB[(SQLite3 FTS5 Registry<br/>agents_registry.db)]
        CSV[Master CSV Catalog<br/>starred_repos_master_catalog.csv]
        TXT[Raw Categorized Text<br/>STARRED_REPOSITORIES_CATEGORIZED_LIST.txt]
        JSON[Validated Inventory JSON<br/>repository-inventory.json]
    end

    subgraph Governance & Quality Tier
        Schemas[JSON Schemas Draft-07<br/>schemas/repository_schema.json]
        Tests[Automated Test Suite<br/>tests/unit & tests/integration]
        CI[GitHub Actions CI/CD<br/>.github/workflows/]
    end

    CLI --> DB
    Web --> JSON
    CSV -->|build_sqlite_registry.py| DB
    CSV -->|generate_inventory.py| JSON
    JSON --> Schemas
    Tests --> DB
    Tests --> Schemas
    CI --> Tests
```

---

## Architectural Principles

1. **Zero External Dependencies**:
   Core ingestion, CLI search, validation, and registry engines run entirely on standard Python 3 and SQLite3. No npm packages, external Python wheels, or proprietary services are required.

2. **Sub-5ms Search Latency**:
   The registry uses SQLite's `fts5` virtual table with BM25 ranking, prefix matching, and optimized indexing, returning complex queries over 11,730 records in under 2 milliseconds.

3. **Multi-Agent Task Allocation**:
   Each cataloged repository represents a logical capability node. Agents in large swarms (e.g. 10,000+ to 200,000+ agent architectures) query the registry to resolve execution tools dynamically rather than loading monolithic codebases.

4. **100% Operational Architecture Workflow Coverage**:
   Every repository has an audited 1-line architectural workflow string formatted as `Input -> Processing -> Output` derived from specialist audits.

---

## Database Schema (agents_registry.db)

```mermaid
erDiagram
    REPOSITORIES {
        int id PK
        string name UK
        string url
        int stars
        int forks
        string language
        int category_id
        string category_name
        string description
        string workflow
        string quality_gate
    }
    REPOSITORIES_FTS {
        string name
        string description
        string workflow
        string language
        string category_name
    }
    REPOSITORIES ||--|| REPOSITORIES_FTS : "synchronizes via triggers"
```
