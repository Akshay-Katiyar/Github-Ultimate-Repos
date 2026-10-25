# Testing & Quality Engineering Guide

Github Ultimate Repos enforces strict automated quality gates.

## Running Tests

### Complete Suite
```bash
python -m unittest discover tests -v
```

### Individual Test Suites
```bash
# Test JSON Schemas
python -m unittest tests/unit/test_schemas.py

# Test SQLite Registry & FTS5 Queries
python -m unittest tests/unit/test_registry.py

# Test Data Validation Logic
python -m unittest tests/unit/test_validation.py

# Test CLI Interface
python -m unittest tests/integration/test_cli.py
```
