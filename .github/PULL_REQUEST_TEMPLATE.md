## Description

Please provide a summary of your proposed changes and the problem they solve.

## Type of Change

- [ ] New repository / agent blueprint addition
- [ ] Correction of existing repository metadata or workflow
- [ ] CLI query engine enhancement
- [ ] Schema or validation rule update
- [ ] Documentation improvement
- [ ] CI/CD or testing addition

## Quality Checklist

- [ ] My code adheres to the style guidelines of this project (PEP 8).
- [ ] I have run local schema validation (`python scripts/inventory/generate_inventory.py --validate-only`).
- [ ] I have run the unit and integration test suite (`python -m unittest discover tests -v`).
- [ ] I have updated relevant documentation if applicable.
- [ ] The SQLite database builds cleanly without warnings (`python scripts/inventory/build_sqlite_registry.py`).
