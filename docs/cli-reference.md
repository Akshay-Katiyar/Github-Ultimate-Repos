# CLI Reference Manual (`ultimate_agent_cli.py`)

The **Ultimate Agent CLI** (`scripts/cli/ultimate_agent_cli.py`) is the primary command-line interface for querying, inspecting, filtering, comparing, recommending, and orchestrating development workflows across 11,730 verified repositories and autonomous agent blueprints from the SQLite FTS5 registry.

---

## 1. Global Syntax & Overview

```bash
python scripts/cli/ultimate_agent_cli.py [-h] [--json] [--no-color] [--db-path DB_PATH] {stats,search,get,category,export,recommend,rec,compare,cmp,workflow,wf} ...
```

### Global Options

| Option | Shorthand | Type | Default | Description |
| :--- | :---: | :---: | :--- | :--- |
| `--help` | `-h` | Flag | `False` | Display help message and exit. |
| `--json` | — | Flag | `False` | Output results strictly as structured JSON across all subcommands. |
| `--no-color` | — | Flag | `False` | Disable ANSI color codes and styling. Can also be controlled via `NO_COLOR=1` environment variable. |
| `--db-path` | — | Path | `registry/agents_registry.db` | Custom filesystem path to the SQLite registry database (or `ULTIMATE_REPOS_DB`). |

### Environment Requirements
- Python 3.9+ with native standard library `sqlite3`.
- The database file must exist at `registry/agents_registry.db` (can be built via `python scripts/inventory/build_sqlite_registry.py`).
- Console output is automatically reconfigured to UTF-8 (`sys.stdout.reconfigure(encoding='utf-8')`).

### Exit Codes
- `0`: Successful execution.
- `1`: Error encountered (e.g., database missing, repository not found, invalid argument).

---

## 2. Command Reference

### 2.1 `stats` — Executive Intelligence Dashboard
Displays high-level statistics across the entire catalog, including total record volume, cumulative stars and forks, language counts, and top disciplines.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py stats [--json]
```

#### Options
- `--json`: Output statistics as structured JSON payload.

#### Example Output
```text
================================================================================
 🚀 GITHUB ULTIMATE REPOS & AGENT REGISTRY — EXECUTIVE INTELLIGENCE DASHBOARD
================================================================================
 Total Repositories / Blueprints : 11,730
 Cumulative Stargazers           : 183,294,158★
 Cumulative Forks                : 28,001,912
 Granular Disciplines            : 55
 Programming Languages           : 146
 Architectural Workflow Coverage : 100% (VERIFIED)
--------------------------------------------------------------------------------

[Top 10 Disciplines by Volume]:
   1. Cloud-Native Infrastructure, Kubernetes, Containers & Service Meshes | 2,472 repos | 33,213,842★
   2. Modern Frontend Frameworks, Reactive Web Engines (React/Vue/Svelte) & Bundlers | 2,249 repos | 35,702,770★
   3. Systems Programming, Low-Level Runtimes, Memory Safety & WebAssembly (Wasm) | 1,321 repos | 16,676,337★
   4. Python Ecosystem, Data Science, Scientific Computing & Analytics | 1,228 repos | 14,904,058★
   5. Artificial Intelligence, Large Language Models, Foundation Models & Quantization | 1,101 repos | 22,083,549★
   6. Curated Knowledge, Developer Guides, Books & Awesome Collections |   689 repos | 16,178,214★
   7. Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools |   303 repos |  7,471,295★
   8. Database Engines, Distributed SQL, NoSQL, Vector DBs & Persistent Caches |   291 repos |  5,032,498★
   9. Developer Tooling, Shell Environments, Terminal Emulators & CLI Utilities |   164 repos |  3,596,484★
  10. Game Development Engines, 2D/3D Graphics APIs & Shaders (WebGL/Vulkan) |   140 repos |  1,720,397★

[Top 10 Languages]:
   1. Python               | 2,326 repos | 37,097,592★
   2. TypeScript           | 1,484 repos | 28,469,095★
   3. JavaScript           | 1,296 repos | 20,424,395★
   4. Other                |   935 repos | 16,579,787★
   5. Go                   |   850 repos | 13,433,768★
   6. C++                  |   649 repos |  8,367,302★
   7. Java                 |   566 repos |  7,539,480★
   8. Rust                 |   513 repos |  9,443,695★
   9. C                    |   448 repos |  5,428,366★
  10. Jupyter Notebook     |   290 repos |  4,151,568★
================================================================================
```

---

### 2.2 `search` — Full-Text & Relational Query
Performs high-speed FTS5 full-text queries against names, descriptions, languages, and workflows, combined with relational star and category filters.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py search <query> [options]
```

#### Arguments & Options
- `<query>`: Search string. Supports phrases in quotes (`"multi-agent"`), boolean logic (`AND`, `OR`, `NOT`), and prefix wildcards (`robot*`).
- `--limit <int>`: Maximum number of records to return. Default: `10`.
- `--category <str>`: Filter matches to categories matching name or ID substring.
- `--min-stars <int>`: Filter matches to repositories having at least this many stars. Default: `0`.
- `--json`: Output search results as structured JSON.

#### Examples
```bash
# Basic keyword search
python scripts/cli/ultimate_agent_cli.py search "langchain"

# Complex boolean search with star threshold and category filter
python scripts/cli/ultimate_agent_cli.py search "autonomous OR multi-agent" --category "Multi-Agent" --min-stars 10000 --limit 5

# JSON output format
python scripts/cli/ultimate_agent_cli.py search "kubernetes" --limit 3 --json
```

---

### 2.3 `get` — Retrieve Repository Dossier
Fetches the complete audited dossier for a specific repository by full coordinate (`owner/repo`) or trailing name (`repo`).

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py get <repo> [--json]
```

#### Arguments & Options
- `<repo>`: Full GitHub coordinate (`vllm-project/vllm`) or repo name (`vllm`).
- `--json`: Output dossier as structured JSON.

#### Example
```bash
python scripts/cli/ultimate_agent_cli.py get "vllm-project/vllm"
```

#### Example Output
```text
================================================================================
 📦 REPOSITORY DOSSIER: vllm-project/vllm
================================================================================
 Canonical URL       : https://github.com/vllm-project/vllm
 Stargazers          : 95,401★
 Forks               : 23,918
 Primary Language    : Python
 Discipline Category : [#2] Artificial Intelligence, Large Language Models, Foundation Models & Quantization
 Quality Gate Status : VERIFIED
--------------------------------------------------------------------------------
 Description:
 A high-throughput and memory-efficient LLM serving engine powered by PagedAttention.
--------------------------------------------------------------------------------
 Operational Architecture Workflow:
 ⚡ Continuous iteration-level batching -> PagedAttention virtual block table allocation -> chunked prefill tensor parallel forward pass -> streaming token delivery.
================================================================================
```

---

### 2.4 `category` — List Repositories by Discipline
Lists top repositories in a specific category ordered by community stargazers.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py category <name_or_id> [options]
```

#### Arguments & Options
- `<name_or_id>`: Category title substring (e.g. `Robotics`) or numeric category ID (`1` through `55`).
- `--limit <int>`: Maximum number of repositories to display. Default: `15`.
- `--json`: Output category results as structured JSON.

#### Examples
```bash
# Query by numeric ID
python scripts/cli/ultimate_agent_cli.py category 9 --limit 5

# Query by category name substring
python scripts/cli/ultimate_agent_cli.py category "Quantum Computing" --limit 5
```

---

### 2.5 `export` — Filtered Dataset Export
Extracts and serializes filtered subsets of catalog records to JSON or CSV format.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py export --output <path> [options]
```

#### Arguments & Options
- `--output <path>`: Destination file path (**Required**).
- `--format {json,csv}`: Target serialization format. Default: `json`.
- `--category <str>`: Filter by category substring.
- `--min-stars <int>`: Minimum star count filter. Default: `0`.

#### Examples
```bash
# Export all AI repositories with >20,000 stars to JSON
python scripts/cli/ultimate_agent_cli.py export \
  --category "Artificial Intelligence" \
  --min-stars 20000 \
  --format json \
  --output top_ai_repos.json

# Export all high-star repositories to CSV
python scripts/cli/ultimate_agent_cli.py export \
  --min-stars 10000 \
  --format csv \
  --output high_star_repos.csv
```

---

### 2.6 `recommend` (alias: `rec`) — Intelligent Multi-Factor Recommendations
Deconstructs natural language queries into architectural intent, filters candidates, scores across multi-factor dimensions (task fit, maturity, language, license, deployment), and outputs rich recommendation decision cards.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py recommend <intent> [options]
python scripts/cli/ultimate_agent_cli.py rec <intent> [options]
```

#### Arguments & Options
- `<intent>`: Natural language query stating what you want to build or achieve (e.g. `"fast inference engine for local models"`).
- `--limit <int>`: Number of recommendations to return. Default: `3`.
- `--category <str>`: Constrain recommendation to a specific discipline category.
- `--language <str>`: Prefer or require a specific programming language (e.g. `Python`, `Rust`, `TypeScript`).
- `--min-stars <int>`: Filter by minimum star count. Default: `0`.
- `--json`: Output recommendation cards as structured JSON for autonomous AI agents.

#### Example
```bash
python scripts/cli/ultimate_agent_cli.py recommend "agent orchestration framework with tool calling" --limit 2
```

#### Example Output
```text
====================================================================================================
 🎯 INTELLIGENT REPOSITORY RECOMMENDATIONS ENGINE
 Query Intent   : "agent orchestration framework with tool calling"
 RECOMMENDATIONS: 2 Ranked Cards
====================================================================================================

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [RANK #1] ⭐ TOP RECOMMENDATION           (Match Score: 99%)
│ 📦 Repository : langchain-ai/langchain
│ 🔗 URL        : https://github.com/langchain-ai/langchain
│ 📊 Metrics    : 148,406★ Stargazers | 24,906 Forks | Language: Python
│ 📂 Discipline : [#3] Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 💡 WHY RECOMMENDED:
│    Matches user architectural intent within the Multi-Agent Systems discipline. Operates as an
│    audited capability executing dynamic tool routing (MCP JSON-RPC) and shared memory graphs.
│
│ ⚡ OPERATIONAL ARCHITECTURE WORKFLOW:
│    Goal decomposition DAG -> dynamic tool routing (MCP JSON-RPC) -> state graph & shared memory scratchpad -> multi-agent execution swarm -> critic-refiner consensus loop.
│
│ 🚀 CORE STRENGTHS:
│    • Ecosystem Validation: 148,406★ stargazers and 24,906 forks confirm extensive production adoption.
│    • Architectural Precision: Executes structured workflow with native MCP JSON-RPC tool calling.
│    • Runtime Ecosystem: Built in Python with deep tool calling and agent memory support.
│
│ ⚠️ LIMITATIONS & TRADE-OFFS:
│    • Comprehensive enterprise footprint may introduce dependency overhead for minimal scripts.
│
│ 🔄 PEER ALTERNATIVES IN DISCIPLINE:
│    • Significant-Gravitas/AutoGPT (187,737★, Python)
│    • crewAIInc/crewAI (60,081★, Python)
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.7 `compare` (alias: `cmp`) — Side-by-Side Architectural Trade-off Engine
Performs a deep multi-dimensional comparative audit between 2 or 3 candidate repositories, rendering a benchmark scorecard, deep-dive comparison cards, and a strategic decision guide with scenario winners.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py compare <repo1> <repo2> [<repo3>] [options]
python scripts/cli/ultimate_agent_cli.py cmp <repo1> <repo2> [<repo3>] [options]
```

#### Arguments & Options
- `<repos...>`: 2 or 3 repository coordinates or short names (e.g. `vllm llama.cpp ollama`).
- `--format {terminal,markdown,json}`: Output presentation format. Default: `terminal`.
- `--json`: Output comparison strictly as JSON (shorthand for `--format json`).
- `--output <path>`, `-o <path>`: Optional destination file path to save output.

#### Example
```bash
# Terminal comparison of 3 LLM inference runtimes
python scripts/cli/ultimate_agent_cli.py compare vllm llama.cpp ollama

# Markdown comparison report exported to file
python scripts/cli/ultimate_agent_cli.py compare react vue --format markdown -o comparison.md

# JSON output for agent swarm consumption
python scripts/cli/ultimate_agent_cli.py compare fastapi express --json
```

#### Example Output Highlights
- **Benchmark Scorecard**: Evaluates Stars, Forks, Primary Language, Production Readiness, Modularity, Velocity, Integrations, Efficiency, and Composite Score.
- **Deep-Dive Comparison Cards**: Details Primary Use Case Fit, Sweet Spots, Anti-Patterns, Architectural Approach, Strengths, Limitations, Developer Persona, and Licensing Model.
- **Strategic Decision Guide**: Highlights Scenario Winners for Rapid Prototyping, Enterprise Production, and Autonomous Exploration.

---

### 2.8 `workflow` (alias: `wf`) — Development Workflow Explorer
Inspects, lists, synthesizes, and steps through end-to-end development workflow pipelines across software engineering, AI agent architectures, mobile, DevOps, and cloud-native platforms.

#### Syntax
```bash
python scripts/cli/ultimate_agent_cli.py workflow [name] [options]
python scripts/cli/ultimate_agent_cli.py wf [name] [options]
```

#### Arguments & Options
- `[name]`: Workflow identifier (e.g. `ai-agent`, `mobile`, `devops`, `fullstack`, `data-engineering`, `cybersecurity`).
- `--list`: List all available curated enterprise workflows with stage counts and domains.
- `--step <int>`: Inspect a specific workflow step number (1-based).
- `--category <str>`: Synthesize a custom end-to-end workflow for any of the 55 discipline categories.
- `--interactive`: Step through workflow stages interactively in the terminal.
- `--json`: Output workflow definition as structured JSON.

#### Examples
```bash
# List all curated workflows
python scripts/cli/ultimate_agent_cli.py workflow --list

# Inspect the AI Agent enterprise workflow
python scripts/cli/ultimate_agent_cli.py workflow ai-agent

# Inspect stage 2 of the DevOps pipeline
python scripts/cli/ultimate_agent_cli.py workflow devops --step 2

# Synthesize a workflow for Robotics
python scripts/cli/ultimate_agent_cli.py workflow --category "Robotics"

# Interactive walkthrough
python scripts/cli/ultimate_agent_cli.py workflow mobile --interactive
```

---

## 3. Programmatic Usage in Python

The CLI and its underlying engines can be imported directly into Python applications and agent runtimes:

### 3.1 Direct SQLite Querying
```python
import sqlite3

def find_candidate_tools(keyword: str, min_stars: int = 5000):
    conn = sqlite3.connect("registry/agents_registry.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = """
    SELECT r.name, r.stars, r.workflow, r.url
    FROM repositories_fts f
    JOIN repositories r ON f.rowid = r.id
    WHERE repositories_fts MATCH ? AND r.stars >= ?
    ORDER BY r.stars DESC
    LIMIT 10;
    """
    c.execute(query, [keyword, min_stars])
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

# Example invocation
tools = find_candidate_tools("finite element OR fea")
for t in tools:
    print(f"{t['name']} ({t['stars']}★): {t['workflow']}")
```

### 3.2 Tradeoff Engine Integration
```python
from scripts.comparison.tradeoff_engine import TradeoffEngine

engine = TradeoffEngine(db_path="registry/agents_registry.db")
report = engine.compare(["vllm-project/vllm", "ggml-org/llama.cpp"])
print(f"Comparison ID: {report['evaluation_id']}")
print(f"Top Option: {report['winner']['name']}")
```
