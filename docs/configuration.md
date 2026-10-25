# Configuration, Customization & Runtime Tuning

Github Ultimate Repos is designed to operate out-of-the-box with sensible zero-configuration defaults. However, for enterprise deployments, embedded microservices, and high-concurrency multi-agent swarms, the runtime behavior can be customized via environment variables, SQLite engine PRAGMAs, and tokenization settings.

---

## 1. Environment Variables

The registry, builder, and CLI engine respect the following environment variables:

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `ULTIMATE_REPOS_ROOT` | Repository directory | Base working path of Github Ultimate Repos. |
| `ULTIMATE_REPOS_DB` | `registry/agents_registry.db` | Absolute or relative path to the SQLite FTS5 database (overridden by `--db-path`). |
| `ULTIMATE_REPOS_CSV` | `starred_repos_master_catalog.csv` | Absolute or relative path to the master catalog CSV. |
| `NO_COLOR` | Unset | When set to any value (e.g. `NO_COLOR=1`), disables ANSI color codes and styling per the NO_COLOR standard (overridden by `--no-color`). |
| `PYTHONIOENCODING` | `utf-8` | Forces standard I/O stream encoding across terminal child processes and MCP servers. |

### Setting Environment Variables

#### In Bash / Zsh (Linux / macOS):
```bash
export ULTIMATE_REPOS_DB="/var/data/github-ultimate/agents_registry.db"
export ULTIMATE_REPOS_LIMIT=25
python scripts/cli/ultimate_agent_cli.py search "robotics"
```

#### In PowerShell (Windows):
```powershell
$env:ULTIMATE_REPOS_DB = "C:\Data\agents_registry.db"
$env:ULTIMATE_REPOS_LIMIT = "25"
python scripts\cli\ultimate_agent_cli.py search "robotics"
```

---

## 2. SQLite Engine PRAGMAs & Performance Tuning

The SQLite database at `registry/agents_registry.db` is built and accessed with performance-critical PRAGMAs configured in `scripts/inventory/build_sqlite_registry.py`.

```sql
-- 1. Enable Write-Ahead Logging (WAL) for non-blocking concurrent reads
PRAGMA journal_mode = WAL;

-- 2. Relax disk synchronization to safe, high-speed mode
PRAGMA synchronous = NORMAL;

-- 3. Store temporary tables and intermediate sort operations in RAM
PRAGMA temp_store = MEMORY;

-- 4. Enable 256MB memory-mapped file I/O for zero-copy page reads
PRAGMA mmap_size = 268435456;

-- 5. Allocate 64MB dedicated cache in memory (negative value denotes kilobytes)
PRAGMA cache_size = -64000;

-- 6. Enforce UTF-8 text encoding
PRAGMA encoding = "UTF-8";
```

### PRAGMA Impact Analysis:
- `journal_mode = WAL`: Prevents database locks when multiple background agent processes perform concurrent queries while an audit updates table metadata.
- `mmap_size = 268435456`: Allows the operating system kernel to map database pages directly into process virtual memory, eliminating syscall read overhead.
- `cache_size = -64000`: Retains frequently accessed index branches and b-trees in RAM.

---

## 3. Resource-Constrained & Embedded Tuning

For deployment in constrained environments (e.g. Raspberry Pi, lightweight Docker containers, or micro-VMs with <512MB RAM):

```sql
-- Low-memory profile for micro-instances
PRAGMA cache_size = -8000;  -- 8MB cache
PRAGMA mmap_size = 33554432; -- 32MB memory map
PRAGMA temp_store = FILE;
```

---

## 4. FTS5 Tokenizer & Index Customization

The FTS5 virtual table utilizes SQLite's default `unicode61` tokenizer. This can be customized to support advanced stemming, diacritic removal, or specialized language tokenizers.

### Enabling the Porter Stemmer (Optional)
To stem English search terms automatically (e.g. searching for `running` also matches `runs`, `ran`, `run`):

```sql
CREATE VIRTUAL TABLE repositories_fts USING fts5(
    name,
    description,
    workflow,
    language,
    category_name,
    content='repositories',
    content_rowid='id',
    tokenize='porter unicode61'
);
```

### Custom Prefix Indexing
To accelerate prefix wildcard searches (e.g. `robot*` or `trans*`), prefix indexing can be configured directly in the virtual table declaration:

```sql
CREATE VIRTUAL TABLE repositories_fts USING fts5(
    name,
    description,
    workflow,
    language,
    category_name,
    content='repositories',
    content_rowid='id',
    prefix='2 3 4'
);
```

---

## 5. Cross-Platform Terminal Encoding

On Windows, terminal consoles traditionally default to legacy code pages (e.g., `cp1252` or `cp437`), which causes `UnicodeEncodeError` when rendering emoji glyphs (🚀, ★, 💻, ⚡).

All CLI scripts in `scripts/cli/` include standard re-encoding safeguards:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

If invoking Python commands in PowerShell or CMD manually, set the console encoding to UTF-8:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```
