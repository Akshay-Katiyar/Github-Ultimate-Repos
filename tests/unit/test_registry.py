import os
import sqlite3
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(DB_PATH), f"Registry DB must exist at {DB_PATH}")
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_database_record_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM repositories;")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 11730, "Database must contain exactly 11,730 repositories")

    def test_fts5_virtual_table_sync(self):
        self.cursor.execute("SELECT COUNT(*) FROM repositories_fts;")
        fts_count = self.cursor.fetchone()[0]
        self.assertEqual(fts_count, 11730, "FTS5 table must index all 11,730 records")

    def test_categories_count(self):
        self.cursor.execute("SELECT COUNT(DISTINCT category_name) FROM repositories;")
        cats = self.cursor.fetchone()[0]
        self.assertEqual(cats, 55, "Database must represent exactly 55 categories")

    def test_fts5_fulltext_search(self):
        self.cursor.execute("""
        SELECT r.name, r.stars
        FROM repositories_fts f
        JOIN repositories r ON f.rowid = r.id
        WHERE repositories_fts MATCH 'langchain'
        ORDER BY r.stars DESC
        LIMIT 5;
        """)
        rows = self.cursor.fetchall()
        self.assertGreater(len(rows), 0, "FTS query for 'langchain' should return results")

if __name__ == "__main__":
    unittest.main()
