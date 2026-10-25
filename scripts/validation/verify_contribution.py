#!/usr/bin/env python3
"""
verify_contribution.py - Automated Pre-PR Contributor Verification Tool

Comprehensive, zero-dependency validation runner that verifies all quality gates
locally before submitting a pull request to Github Ultimate Repos.

Checks performed:
1. System runtime & SQLite3 FTS5 capability
2. JSON Schema syntax and integrity (repository_schema.json, agent_schema.json)
3. Master catalog CSV records & schema compliance
4. Category documentation coverage (55 categories in categories/*.md)
5. SQLite FTS5 database integrity and full-text search
6. Automated test suite execution (tests/unit/ and tests/integration/)
7. CLI engine command sanity checks
"""

import os
import sys
import json
import csv
import sqlite3
import subprocess
import time

# Ensure clean UTF-8 output across Windows, macOS, and Linux
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "starred_repos_master_catalog.csv")
REGISTRY_DB = os.path.join(REPO_ROOT, "registry", "agents_registry.db")
SCHEMAS_DIR = os.path.join(REPO_ROOT, "schemas")
CATEGORIES_DIR = os.path.join(REPO_ROOT, "categories")
TESTS_DIR = os.path.join(REPO_ROOT, "tests")

# ANSI Color codes (gracefully handles terminals without color support)
USE_COLOR = os.environ.get("TERM") != "dumb" and not os.environ.get("NO_COLOR")
GREEN = "\033[92m" if USE_COLOR else ""
RED = "\033[91m" if USE_COLOR else ""
YELLOW = "\033[93m" if USE_COLOR else ""
CYAN = "\033[96m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""

class GateResult:
    def __init__(self, name):
        self.name = name
        self.passed = True
        self.errors = []
        self.warnings = []
        self.details = []

    def fail(self, msg):
        self.passed = False
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def info(self, msg):
        self.details.append(msg)

def check_system_environment():
    gate = GateResult("System Runtime & SQLite3 FTS5 Capability")
    py_major, py_minor = sys.version_info[:2]
    gate.info(f"Python Runtime: {sys.version.split()[0]} ({sys.platform})")
    if (py_major, py_minor) < (3, 9):
        gate.fail(f"Python 3.9+ required; found {py_major}.{py_minor}")
    
    # Check SQLite3 FTS5
    try:
        conn = sqlite3.connect(":memory:")
        c = conn.cursor()
        c.execute("CREATE VIRTUAL TABLE fts5_test USING fts5(content);")
        c.execute("INSERT INTO fts5_test (content) VALUES ('autonomous agent swarms');")
        c.execute("SELECT * FROM fts5_test WHERE fts5_test MATCH 'agent';")
        rows = c.fetchall()
        conn.close()
        if len(rows) == 1:
            gate.info(f"SQLite3 Engine: {sqlite3.sqlite_version} with FTS5 [ENABLED]")
        else:
            gate.fail("SQLite3 FTS5 test query failed to match")
    except Exception as e:
        gate.fail(f"SQLite3 lacks FTS5 extension support: {e}")

    return gate

def check_json_schemas():
    gate = GateResult("JSON Schema Validation & Structural Integrity")
    schema_files = ["repository_schema.json", "agent_schema.json"]
    for sf in schema_files:
        path = os.path.join(SCHEMAS_DIR, sf)
        if not os.path.exists(path):
            gate.fail(f"Missing required schema: {sf}")
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "$schema" not in data or "required" not in data:
                gate.fail(f"Schema {sf} missing '$schema' or 'required' field")
            else:
                gate.info(f"Schema {sf}: Valid Draft-07 ({len(data.get('properties', {}))} properties)")
        except json.JSONDecodeError as jde:
            gate.fail(f"Invalid JSON in {sf}: {jde}")
    return gate

def check_master_catalog():
    gate = GateResult("Master Catalog Dataset & Schema Conformance")
    if not os.path.exists(CSV_PATH):
        gate.fail(f"Master catalog CSV not found at {CSV_PATH}")
        return gate

    record_count = 0
    invalid_rows = []
    required_cols = {"id", "name", "url", "stars", "forks", "language", "category_id", "category_name", "description", "architecture_workflow"}

    with open(CSV_PATH, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        is_title_case = "Repository" in fieldnames
        if not is_title_case:
            missing_cols = required_cols - fieldnames
            if missing_cols:
                gate.fail(f"CSV missing mandatory columns: {missing_cols}")
                return gate

        for idx, row in enumerate(reader, start=1):
            record_count += 1
            name = (row.get("Repository") if is_title_case else row.get("name")) or ""
            if "/" not in name:
                invalid_rows.append(f"Row {idx}: Invalid name '{name}' (must be owner/repo)")
            url = (row.get("URL") if is_title_case else row.get("url")) or ""
            if not url.startswith("http"):
                invalid_rows.append(f"Row {idx}: Invalid URL '{url}'")
            try:
                stars_val = (row.get("Stars") if is_title_case else row.get("stars")) or 0
                stars = int(stars_val)
                if stars < 0:
                    invalid_rows.append(f"Row {idx}: Negative stars '{stars}'")
            except ValueError:
                invalid_rows.append(f"Row {idx}: Non-integer stars '{stars_val}'")
            if not is_title_case:
                try:
                    cat_id = int(row.get("category_id", 0))
                    if cat_id < 1 or cat_id > 55:
                        invalid_rows.append(f"Row {idx}: Category ID {cat_id} out of bounds (1-55)")
                except ValueError:
                    invalid_rows.append(f"Row {idx}: Non-integer category_id")
            workflow = ((row.get("Workflow") if is_title_case else row.get("architecture_workflow")) or "").strip()
            if not workflow or len(workflow) < 5:
                invalid_rows.append(f"Row {idx}: Missing or trivial architecture workflow")

            if len(invalid_rows) >= 10:
                break

    if invalid_rows:
        for err in invalid_rows[:5]:
            gate.fail(err)
        if len(invalid_rows) > 5:
            gate.fail(f"... and {len(invalid_rows) - 5} more validation errors")
    else:
        gate.info(f"Verified {record_count:,} records in CSV: 100% Schema Valid")

    return gate

def check_category_markdown():
    gate = GateResult("Category Markdown Coverage (55 Disciplines)")
    if not os.path.exists(CATEGORIES_DIR):
        gate.fail("categories/ directory not found")
        return gate

    files = [f for f in os.listdir(CATEGORIES_DIR) if f.endswith(".md")]
    if len(files) != 55:
        gate.fail(f"Expected 55 category markdown files, found {len(files)}")
    else:
        gate.info("All 55 DeepTech category discipline files present")
    return gate

def check_sqlite_registry():
    gate = GateResult("SQLite FTS5 Registry Integrity & Search Benchmark")
    if not os.path.exists(REGISTRY_DB):
        gate.warn("registry/agents_registry.db not found. Run 'python scripts/inventory/build_sqlite_registry.py'")
        gate.fail("Registry database missing")
        return gate

    try:
        conn = sqlite3.connect(REGISTRY_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM repositories;")
        repo_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM repositories_fts;")
        fts_count = cursor.fetchone()[0]

        if repo_count != fts_count:
            gate.fail(f"Mismatch: repositories ({repo_count}) != repositories_fts ({fts_count})")
        else:
            gate.info(f"Database contains {repo_count:,} synced records with FTS5 index")

        # Test query benchmark
        t0 = time.perf_counter()
        cursor.execute("""
            SELECT r.name, r.stars
            FROM repositories_fts f
            JOIN repositories r ON f.rowid = r.id
            WHERE repositories_fts MATCH 'langchain'
            ORDER BY r.stars DESC LIMIT 3;
        """)
        results = cursor.fetchall()
        t_delta = (time.perf_counter() - t0) * 1000
        conn.close()

        if not results:
            gate.fail("FTS5 benchmark query for 'langchain' returned 0 results")
        else:
            gate.info(f"FTS5 Query Benchmark: {t_delta:.2f} ms ({len(results)} matches returned)")

    except Exception as e:
        gate.fail(f"Error accessing SQLite registry: {e}")

    return gate

def check_automated_tests():
    gate = GateResult("Automated Unit & Integration Test Suite")
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", TESTS_DIR, "-t", REPO_ROOT]
    try:
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            gate.fail(f"Unit tests failed (exit code {res.returncode}):\n{res.stderr.strip() or res.stdout.strip()}")
        else:
            # Parse output for test count
            output = res.stderr or res.stdout
            lines = output.strip().split("\n")
            summary_line = [l for l in lines if "Ran" in l and "tests" in l]
            summary = summary_line[0] if summary_line else "All tests passed"
            gate.info(f"Test Suite: {summary}")
    except subprocess.TimeoutExpired:
        gate.fail("Test suite execution timed out after 60s")
    except Exception as e:
        gate.fail(f"Failed to execute tests: {e}")

    return gate

def check_cli_sanity():
    gate = GateResult("CLI Query Engine Sanity Verification")
    cli_path = os.path.join(REPO_ROOT, "scripts", "cli", "ultimate_agent_cli.py")
    if not os.path.exists(cli_path):
        gate.fail(f"CLI script missing at {cli_path}")
        return gate

    cmd = [sys.executable, cli_path, "stats"]
    try:
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            gate.fail(f"CLI 'stats' failed:\n{res.stderr.strip()}")
        elif "EXECUTIVE INTELLIGENCE DASHBOARD" not in res.stdout:
            gate.fail("CLI 'stats' returned unexpected output format")
        else:
            gate.info("CLI 'stats' command executed successfully")
    except Exception as e:
        gate.fail(f"Failed to run CLI sanity check: {e}")

    return gate

def main():
    print(f"\n{BOLD}{CYAN}========================================================================{RESET}")
    print(f"{BOLD}{CYAN} 🛡️  GITHUB ULTIMATE REPOS — CONTRIBUTOR QUALITY GATE VERIFIER{RESET}")
    print(f"{BOLD}{CYAN}========================================================================{RESET}\n")

    start_time = time.perf_counter()
    gates = [
        check_system_environment(),
        check_json_schemas(),
        check_master_catalog(),
        check_category_markdown(),
        check_sqlite_registry(),
        check_automated_tests(),
        check_cli_sanity(),
    ]

    all_passed = True
    total_errors = 0

    for i, gate in enumerate(gates, start=1):
        status_label = f"{GREEN}[PASS]{RESET}" if gate.passed else f"{RED}[FAIL]{RESET}"
        print(f"{BOLD}{i}. {gate.name}{RESET} ... {status_label}")
        for detail in gate.details:
            print(f"   {CYAN}ℹ{RESET} {detail}")
        for warn in gate.warnings:
            print(f"   {YELLOW}⚠ Warning:{RESET} {warn}")
        for err in gate.errors:
            print(f"   {RED}✖ Error:{RESET} {err}")
            all_passed = False
            total_errors += 1
        print()

    duration = time.perf_counter() - start_time
    print(f"{BOLD}------------------------------------------------------------------------{RESET}")

    if all_passed:
        print(f"{BOLD}{GREEN}🎉 ALL 7 QUALITY GATES PASSED in {duration:.2f}s!{RESET}")
        print(f"{GREEN}Your local workspace is in pristine condition and ready for PR submission.{RESET}\n")
        sys.exit(0)
    else:
        print(f"{BOLD}{RED}❌ {total_errors} QUALITY GATE(S) FAILED in {duration:.2f}s.{RESET}")
        print(f"{RED}Please review and resolve the errors above before opening your Pull Request.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
