"""
test_taxonomy.py - Comprehensive Unit Tests for the 55-Discipline DeepTech Taxonomy
"""

import os
import json
import csv
import sqlite3
import re
import unittest
import jsonschema

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TAX_PATH = os.path.join(REPO_ROOT, "registry", "taxonomy.json")
SCHEMA_PATH = os.path.join(REPO_ROOT, "schemas", "taxonomy_schema.json")
CSV_PATH = os.path.join(REPO_ROOT, "starred_repos_master_catalog.csv")
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")
CATEGORIES_DIR = os.path.join(REPO_ROOT, "categories")

class TestTaxonomy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertTrue(cls, os.path.exists(TAX_PATH), "taxonomy.json must exist")
        with open(TAX_PATH, "r", encoding="utf-8") as f:
            cls.tax_data = json.load(f)

        cls.assertTrue(cls, os.path.exists(SCHEMA_PATH), "taxonomy_schema.json must exist")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema_data = json.load(f)

        cls.assertTrue(cls, os.path.exists(CSV_PATH), "starred_repos_master_catalog.csv must exist")
        cls.csv_counts = {}
        with open(CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row["Category"].strip()
                cls.csv_counts[cat] = cls.csv_counts.get(cat, 0) + 1

        cls.assertTrue(cls, os.path.exists(DB_PATH), "agents_registry.db must exist")
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        rows = cur.execute(
            "SELECT category_id, category_name, count(*) FROM repositories GROUP BY category_id, category_name ORDER BY category_id"
        ).fetchall()
        conn.close()
        cls.db_counts = {row[0]: (row[1], row[2]) for row in rows}

    def test_taxonomy_file_integrity(self):
        """Verifies taxonomy.json exists, has required root keys, and correct metadata."""
        self.assertIn("version", self.tax_data)
        self.assertEqual(self.tax_data["total_disciplines"], 55)
        self.assertEqual(len(self.tax_data["disciplines"]), 55)
        self.assertIn("clusters", self.tax_data)
        self.assertGreaterEqual(len(self.tax_data["clusters"]), 8)

    def test_schema_conformance(self):
        """Validates taxonomy.json against schemas/taxonomy_schema.json using jsonschema."""
        jsonschema.validate(instance=self.tax_data, schema=self.schema_data)

    def test_unique_stable_ids(self):
        """Verifies all 55 disciplines have strictly sequential IDs 1-55 and valid unique stable_id strings."""
        seen_ids = set()
        seen_stable_ids = set()
        stable_id_pattern = re.compile(r"^cat-[0-9]{2}-[a-z0-9-]+$")

        for idx, discipline in enumerate(self.tax_data["disciplines"], start=1):
            did = discipline.get("id")
            self.assertEqual(did, idx, f"Discipline at index {idx-1} must have id={idx}, found {did}")
            self.assertNotIn(did, seen_ids, f"Duplicate id {did} detected")
            seen_ids.add(did)

            stable_id = discipline.get("stable_id")
            self.assertIsNotNone(stable_id, f"Discipline {did} must have stable_id")
            self.assertTrue(
                bool(stable_id_pattern.match(stable_id)),
                f"Discipline {did} stable_id '{stable_id}' does not match pattern ^cat-[0-9]{{2}}-[a-z0-9-]+$"
            )
            self.assertNotIn(stable_id, seen_stable_ids, f"Duplicate stable_id '{stable_id}' detected")
            seen_stable_ids.add(stable_id)

        self.assertEqual(seen_ids, set(range(1, 56)), "IDs must be exact sequence 1..55")
        self.assertEqual(len(seen_stable_ids), 55)

    def test_canonical_names_and_slugs(self):
        """Verifies every discipline has a valid canonical name and slug."""
        seen_names = set()
        seen_slugs = set()
        for d in self.tax_data["disciplines"]:
            name = d.get("name")
            self.assertTrue(isinstance(name, str) and len(name) >= 5, f"Invalid name for discipline {d.get('id')}")
            self.assertNotIn(name, seen_names, f"Duplicate canonical name: {name}")
            seen_names.add(name)

            slug = d.get("slug")
            self.assertTrue(isinstance(slug, str) and len(slug) >= 3, f"Invalid slug for discipline {d.get('id')}")
            self.assertNotIn(slug, seen_slugs, f"Duplicate slug: {slug}")
            seen_slugs.add(slug)

        self.assertEqual(len(seen_names), 55)
        self.assertEqual(len(seen_slugs), 55)

    def test_comprehensive_descriptions(self):
        """Verifies all 55 disciplines have substantive, comprehensive technical descriptions."""
        for d in self.tax_data["disciplines"]:
            desc = d.get("description")
            self.assertIsNotNone(desc, f"Missing description for discipline {d.get('id')}: {d.get('name')}")
            self.assertIsInstance(desc, str)
            self.assertGreaterEqual(
                len(desc.strip()), 30,
                f"Description for discipline {d.get('id')} ({d.get('name')}) is too short ({len(desc.strip())} chars)"
            )

    def test_keywords_and_synonyms(self):
        """Verifies all 55 disciplines have a comprehensive list of keywords and synonyms."""
        for d in self.tax_data["disciplines"]:
            keywords = d.get("keywords")
            self.assertIsNotNone(keywords, f"Missing keywords for discipline {d.get('id')}")
            self.assertIsInstance(keywords, list)
            self.assertGreaterEqual(
                len(keywords), 3,
                f"Discipline {d.get('id')} has fewer than 3 keywords: {keywords}"
            )
            for kw in keywords:
                self.assertIsInstance(kw, str)
                self.assertGreater(len(kw.strip()), 0)

    def test_parent_cluster_membership(self):
        """Verifies each discipline has a parent_cluster belonging to the top-level clusters list."""
        valid_clusters = set(self.tax_data["clusters"])
        for d in self.tax_data["disciplines"]:
            cluster = d.get("parent_cluster")
            self.assertIsNotNone(cluster, f"Missing parent_cluster for discipline {d.get('id')}")
            self.assertIn(
                cluster, valid_clusters,
                f"Discipline {d.get('id')} has invalid or orphaned parent_cluster: '{cluster}'"
            )

    def test_repository_counts_match_csv(self):
        """Verifies exact repository counts between taxonomy.json and starred_repos_master_catalog.csv."""
        total_repos = 0
        for d in self.tax_data["disciplines"]:
            name = d["name"]
            tax_count = d["metrics"]["repository_count"]
            self.assertIn(name, self.csv_counts, f"Discipline '{name}' not found in master catalog CSV")
            csv_count = self.csv_counts[name]
            self.assertEqual(
                tax_count, csv_count,
                f"Discipline '{name}' count mismatch: taxonomy has {tax_count}, CSV has {csv_count}"
            )
            total_repos += tax_count

        self.assertEqual(total_repos, 11730, "Total repositories across all 55 disciplines must be exactly 11,730")

    def test_repository_counts_match_sqlite(self):
        """Verifies exact repository counts and category names between taxonomy.json and agents_registry.db."""
        for d in self.tax_data["disciplines"]:
            did = d["id"]
            name = d["name"]
            tax_count = d["metrics"]["repository_count"]

            self.assertIn(did, self.db_counts, f"Discipline ID {did} not found in agents_registry.db")
            db_name, db_count = self.db_counts[did]
            self.assertEqual(name, db_name, f"Discipline ID {did} name mismatch: taxonomy='{name}', db='{db_name}'")
            self.assertEqual(
                tax_count, db_count,
                f"Discipline ID {did} count mismatch: taxonomy has {tax_count}, DB has {db_count}"
            )

    def test_zero_orphaned_categories_or_drift(self):
        """Verifies zero orphaned categories across taxonomy.json, catalog CSV, and SQLite registry."""
        tax_names = {d["name"] for d in self.tax_data["disciplines"]}
        csv_names = set(self.csv_counts.keys())
        db_names = {name for did, (name, cnt) in self.db_counts.items()}

        csv_orphans = csv_names - tax_names
        self.assertEqual(csv_orphans, set(), f"Orphaned categories in CSV not in taxonomy: {csv_orphans}")

        db_orphans = db_names - tax_names
        self.assertEqual(db_orphans, set(), f"Orphaned categories in DB not in taxonomy: {db_orphans}")

        tax_orphans = tax_names - csv_names
        self.assertEqual(tax_orphans, set(), f"Disciplines in taxonomy not in CSV: {tax_orphans}")

    def test_category_markdown_files_exist(self):
        """Verifies each of the 55 disciplines has a corresponding curated markdown file in categories/."""
        for d in self.tax_data["disciplines"]:
            did = d["id"]
            slug = d["slug"]
            # File prefix pattern is {did:02d}_
            matches = [f for f in os.listdir(CATEGORIES_DIR) if f.startswith(f"{did:02d}_")]
            self.assertEqual(
                len(matches), 1,
                f"Discipline {did:02d} ({d['name']}) must have exactly one markdown file in categories/, found {matches}"
            )

if __name__ == "__main__":
    unittest.main()
