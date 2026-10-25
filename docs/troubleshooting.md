# Troubleshooting Guide

### 1. `sqlite3.OperationalError: no such table: repositories_fts`
**Cause**: The SQLite build on your system was compiled without FTS5 support, or the registry database was not yet generated.
**Fix**: Run:
```bash
python scripts/inventory/build_sqlite_registry.py
```

### 2. Windows UnicodeEncodeError (cp1252)
**Cause**: The default Windows terminal console encoding is cp1252, which cannot encode emoji characters.
**Fix**: Run in PowerShell with UTF-8 encoding:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python scripts/cli/ultimate_agent_cli.py stats
```
All repository scripts include `sys.stdout.reconfigure(encoding='utf-8')` to prevent encoding crashes automatically.
