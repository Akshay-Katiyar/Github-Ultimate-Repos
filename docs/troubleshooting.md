# Technical Troubleshooting & Diagnostics Guide

This document catalogs common operational issues, environment quirks, and resolution procedures encountered when developing, querying, or testing Github Ultimate Repos.

---

## 1. Quick Diagnostic Checklist

If you encounter unexpected errors, run this diagnostic sequence from the repository root:

```bash
# 1. Verify Python version (requires 3.9+)
python --version

# 2. Verify SQLite and FTS5 availability
python -c "import sqlite3; conn = sqlite3.connect(':memory:'); conn.execute('CREATE VIRTUAL TABLE t USING fts5(x);'); print('FTS5 is AVAILABLE')"

# 3. Rebuild the database from canonical CSV
python scripts/inventory/build_sqlite_registry.py

# 4. Run automated self-test
python -m unittest tests/unit/test_registry.py
```

---

## 2. Common Issues & Solutions

### Issue 1: `sqlite3.OperationalError: no such table: repositories_fts`
#### Symptom:
Queries to `ultimate_agent_cli.py search` fail with `OperationalError: no such table: repositories_fts`.
#### Root Causes:
1. The database file has not been built yet.
2. The local Python SQLite binary was compiled without FTS5 extension support.
#### Resolution:
1. Rebuild the registry database:
   ```bash
   python scripts/inventory/build_sqlite_registry.py
   ```
2. Verify FTS5 support:
   ```bash
   python -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('CREATE VIRTUAL TABLE f USING fts5(a);')"
   ```
   If this raises an `OperationalError`, install an official standard Python build from [python.org](https://www.python.org/) which includes FTS5 by default.

---

### Issue 2: Windows UnicodeEncodeError (`charmap` / `cp1252`)
#### Symptom:
Running CLI commands on Windows cmd or PowerShell fails with:
`UnicodeEncodeError: 'charmap' codec can't encode character '\u2b50' in position 14`
#### Root Cause:
Windows command prompts historically default to legacy single-byte code pages (such as `cp1252` or `cp437`), which cannot encode Unicode emojis (★, 🚀, ⚡).
#### Resolution:
1. Configure PowerShell output encoding to UTF-8:
   ```powershell
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   $env:PYTHONIOENCODING = "utf-8"
   ```
2. All repository scripts include `sys.stdout.reconfigure(encoding='utf-8')`, but setting environment variables guarantees safety across all child tools.

---

### Issue 3: `sqlite3.OperationalError: database is locked`
#### Symptom:
Database writes or rebuild scripts fail with `database is locked`.
#### Root Cause:
Another process (such as an IDE database explorer, an unclosed background agent script, or an SQLite GUI tool) holds an active exclusive write lock or uncommitted transaction on `agents_registry.db`.
#### Resolution:
1. Close external SQLite viewers (e.g., DB Browser for SQLite, DBeaver, VS Code SQLite extensions).
2. On Windows, locate and terminate any hanging Python processes:
   ```powershell
   Get-Process python | Where-Object { $_.MainWindowTitle -eq "" } | Stop-Process
   ```
3. Rebuild with WAL mode enabled:
   ```bash
   python scripts/inventory/build_sqlite_registry.py
   ```

---

### Issue 4: FTS5 Query Syntax Errors on Punctuation or Unmatched Quotes
#### Symptom:
Search queries containing special characters (e.g. `c++`, `react/router`, or unmatched quotes like `foo"bar`) fail or return no results.
#### Root Cause:
SQLite FTS5 treats characters like `-`, `*`, `+`, and unbalanced `"` as query operators.
#### Resolution:
- Wrap complex or punctuated phrases in explicit double quotes:
  ```bash
  python scripts/cli/ultimate_agent_cli.py search '"c++"'
  ```
- The CLI includes an automatic fallback mechanism that catches FTS5 syntax errors and re-executes the query using standard parameterized SQL `LIKE`, ensuring zero application crashes.

---

### Issue 5: Web Explorer (`index.html`) Not Loading or Showing Blank Table
#### Symptom:
Opening `index.html` in a web browser displays a blank table or an error in the developer console:
`Access to fetch at 'reports/repository-inventory.json' from origin 'null' has been blocked by CORS policy`.
#### Root Cause:
Modern web browsers (especially Chrome and Brave) block local `fetch()` calls to local files when opened directly via the `file://` protocol.
#### Resolution:
Launch a zero-dependency local HTTP server from the repository root:
```bash
python -m http.server 8000
```
Then navigate to:
```text
http://localhost:8000/index.html
```

---

### Issue 6: Path Resolution Errors When Invoking From Outside Repo Root
#### Symptom:
Running `python scripts/cli/ultimate_agent_cli.py` from another working directory fails with:
`Error: Database not found at ...`
#### Root Cause:
Relative file paths resolving against the caller's working directory rather than the repository root.
#### Resolution:
1. Navigate to the repository root before running commands:
   ```bash
   cd C:\Users\Aryan\Github-Ultimate-Repos
   python scripts/cli/ultimate_agent_cli.py stats
   ```
2. Or set the `ULTIMATE_REPOS_DB` environment variable:
   ```bash
   export ULTIMATE_REPOS_DB="/path/to/Github-Ultimate-Repos/registry/agents_registry.db"
   ```

---

### Issue 7: MCP Server Connection Hangs or Protocol Timeout in IDE
#### Symptom:
Connecting Claude Desktop, Cursor, or Cline to `scripts/cli/mcp_server.py` times out or fails to discover tools.
#### Root Cause:
1. Stdio buffering or stdin/stdout encoding conflicts.
2. The MCP client sends notifications before the handshake completes.
#### Resolution:
1. Ensure `PYTHONIOENCODING=utf-8` is set in your MCP client's environment block.
2. Use absolute paths to both Python interpreter and `mcp_server.py` in your client JSON configuration.
3. Verify the MCP server locally using the integration test:
   ```bash
   python tests/integration/test_mcp_server.py
   ```

---

### Issue 8: ANSI Escape Sequences / Garbled Colors in CI Logs
#### Symptom:
Terminal output shows raw escape codes like `\033[1m` or `\033]8;;` in automated logs or non-TTY pipes.
#### Root Cause:
Log aggregators or CI runners that do not interpret ANSI colors or OSC 8 hyperlinks.
#### Resolution:
Pass `--no-color` or set the standard `NO_COLOR=1` environment variable:
```bash
python scripts/cli/ultimate_agent_cli.py search "ai" --no-color
```

---

## 3. Contact & Support

If your issue is not resolved by the steps above:
- Search existing discussions and issues on [GitHub Issues](https://github.com/Akshay-Katiyar/Github-Ultimate-Repos/issues).
- Consult the [Architecture Guide](architecture.md) and [CLI Reference](cli-reference.md).
- Open a detailed issue report containing your Python version, OS platform, and full terminal traceback.
