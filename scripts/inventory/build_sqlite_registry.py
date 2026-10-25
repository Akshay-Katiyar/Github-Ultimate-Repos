#!/usr/bin/env python3
"""
build_sqlite_registry.py - SQLite FTS5 High-Performance Registry Builder

Builds registry/agents_registry.db indexing all 11,730 repositories with
full-text search (FTS5) across names, descriptions, languages, workflows, and categories.
"""

import os
import sys
import sqlite3
import csv
import time

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "starred_repos_master_catalog.csv")
REGISTRY_DIR = os.path.join(REPO_ROOT, "registry")
DB_PATH = os.path.join(REGISTRY_DIR, "agents_registry.db")

def build_database():
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception as e:
            print(f"Warning: could not remove existing db: {e}")

    print(f"Building SQLite FTS5 registry at {DB_PATH}...")
    start_time = time.perf_counter()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable WAL mode for high read/write concurrency
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")

    # 1. Main repositories table
    cursor.execute("""
    CREATE TABLE repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        url TEXT NOT NULL,
        stars INTEGER NOT NULL,
        forks INTEGER NOT NULL,
        language TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        description TEXT NOT NULL,
        workflow TEXT NOT NULL,
        quality_gate TEXT NOT NULL DEFAULT 'VERIFIED'
    );
    """)

    # 2. Indexes for fast relational queries
    cursor.execute("CREATE INDEX idx_repos_stars ON repositories(stars DESC);")
    cursor.execute("CREATE INDEX idx_repos_lang ON repositories(language);")
    cursor.execute("CREATE INDEX idx_repos_cat_id ON repositories(category_id);")
    cursor.execute("CREATE INDEX idx_repos_cat_name ON repositories(category_name);")

    # 3. FTS5 Virtual Table for full-text and semantic searching
    cursor.execute("""
    CREATE VIRTUAL TABLE repositories_fts USING fts5(
        name,
        description,
        workflow,
        language,
        category_name,
        content='repositories',
        content_rowid='id'
    );
    """)

    # 4. Triggers to keep FTS index synchronized
    cursor.execute("""
    CREATE TRIGGER repositories_ai AFTER INSERT ON repositories BEGIN
        INSERT INTO repositories_fts(rowid, name, description, workflow, language, category_name)
        VALUES (new.id, new.name, new.description, new.workflow, new.language, new.category_name);
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER repositories_ad AFTER DELETE ON repositories BEGIN
        INSERT INTO repositories_fts(repositories_fts, rowid, name, description, workflow, language, category_name)
        VALUES ('delete', old.id, old.name, old.description, old.workflow, old.language, old.category_name);
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER repositories_au AFTER UPDATE ON repositories BEGIN
        INSERT INTO repositories_fts(repositories_fts, rowid, name, description, workflow, language, category_name)
        VALUES ('delete', old.id, old.name, old.description, old.workflow, old.language, old.category_name);
        INSERT INTO repositories_fts(rowid, name, description, workflow, language, category_name)
        VALUES (new.id, new.name, new.description, new.workflow, new.language, new.category_name);
    END;
    """)

    # Canonical category IDs
    cat_names_ordered = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row.get("Category", "").strip()
            if cat and cat not in cat_names_ordered:
                cat_names_ordered.append(cat)
    cat_to_id = {cat: idx for idx, cat in enumerate(cat_names_ordered, 1)}

    # Ingest rows
    rows_to_insert = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Repository", "").strip()
            cat_name = row.get("Category", "General").strip()
            cat_id = cat_to_id.get(cat_name, 1)
            try:
                stars = int(row.get("Stars", 0))
            except ValueError:
                stars = 0
            try:
                forks = int(row.get("Forks", 0))
            except ValueError:
                forks = 0
            lang = row.get("Language", "Other").strip() or "Other"
            url = row.get("URL", f"https://github.com/{name}").strip()
            desc = row.get("Description", "").strip()
            workflow = row.get("Workflow", "").strip()

            rows_to_insert.append((
                name, url, stars, forks, lang, cat_id, cat_name, desc, workflow, 'VERIFIED'
            ))

    cursor.executemany("""
    INSERT INTO repositories (name, url, stars, forks, language, category_id, category_name, description, workflow, quality_gate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, rows_to_insert)

    conn.commit()

    # Optimize FTS index
    cursor.execute("INSERT INTO repositories_fts(repositories_fts) VALUES('optimize');")
    conn.commit()

    elapsed = time.perf_counter() - start_time
    cursor.execute("SELECT COUNT(*) FROM repositories;")
    total_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM repositories_fts;")
    fts_count = cursor.fetchone()[0]

    db_size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)

    print(f"Database built in {elapsed:.2f}s:")
    print(f"  - Repositories Indexed: {total_count:,}")
    print(f"  - FTS5 Documents: {fts_count:,}")
    print(f"  - Database Size: {db_size_mb:.2f} MB")

    # Sample FTS query
    q_start = time.perf_counter()
    cursor.execute("""
    SELECT r.name, r.stars, r.category_name, r.workflow
    FROM repositories_fts f
    JOIN repositories r ON f.rowid = r.id
    WHERE repositories_fts MATCH 'transformers OR langchain OR "multi-agent"'
    ORDER BY r.stars DESC
    LIMIT 5;
    """)
    results = cursor.fetchall()
    q_elapsed_ms = (time.perf_counter() - q_start) * 1000

    print(f"FTS5 Benchmark Test Query completed in {q_elapsed_ms:.2f} ms:")
    for r in results:
        print(f"  * {r[0]} | {r[1]:,}★ | {r[2]}")

    conn.close()

if __name__ == "__main__":
    build_database()
