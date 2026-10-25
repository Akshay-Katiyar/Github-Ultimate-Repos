import os
import glob
import json
import sqlite3
import unittest
import jsonschema

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BLUEPRINTS_DIR = os.path.join(REPO_ROOT, "blueprints")
SCHEMA_PATH = os.path.join(REPO_ROOT, "schemas", "stack_blueprint_schema.json")
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")

class TestBlueprints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)
        cls.conn = sqlite3.connect(DB_PATH)
        cls.c = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_blueprint_schema_validity(self):
        """Verify stack_blueprint_schema.json is a valid Draft-07 JSON Schema."""
        self.assertTrue(os.path.exists(SCHEMA_PATH))
        self.assertEqual(self.schema["title"], "StackBlueprint")
        self.assertIn("required", self.schema)
        self.assertIn("blueprint_id", self.schema["required"])
        self.assertIn("tiers", self.schema["required"])
        self.assertIn("data_flow_stages", self.schema["required"])
        self.assertIn("production_readiness", self.schema["required"])

    def test_all_blueprint_files_exist_and_validate(self):
        """Verify all 5 blueprint JSON files validate against the schema."""
        bp_files = sorted([
            f for f in glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json"))
            if not f.endswith("index.json")
        ])
        self.assertEqual(len(bp_files), 5, "Expected exactly 5 blueprint stack files")

        for bp_file in bp_files:
            with self.subTest(file=os.path.basename(bp_file)):
                with open(bp_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                jsonschema.validate(instance=data, schema=self.schema)
                self.assertTrue(data["blueprint_id"].startswith("BP-"))
                self.assertGreaterEqual(len(data["tiers"]), 3)
                self.assertGreaterEqual(len(data["data_flow_stages"]), 2)

    def test_index_manifest(self):
        """Verify blueprints/index.json exists and catalogs all 5 blueprints."""
        index_file = os.path.join(BLUEPRINTS_DIR, "index.json")
        self.assertTrue(os.path.exists(index_file))
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
        self.assertEqual(index["total_blueprints"], 5)
        self.assertEqual(len(index["blueprints"]), 5)

    def test_repository_references_exist_in_database(self):
        """Verify all primary and alternative component repositories exist in agents_registry.db."""
        bp_files = [
            f for f in glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json"))
            if not f.endswith("index.json")
        ]
        missing = []
        for bp_file in bp_files:
            with open(bp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for tier in data["tiers"]:
                prim = tier["primary_component"]["repo"]
                self.c.execute("SELECT id FROM repositories WHERE name = ? OR LOWER(name) = ?", (prim, prim.lower()))
                if not self.c.fetchone():
                    missing.append((os.path.basename(bp_file), tier["tier_id"], prim))
                for alt in tier.get("alternative_components", []):
                    alt_repo = alt["repo"]
                    self.c.execute("SELECT id FROM repositories WHERE name = ? OR LOWER(name) = ?", (alt_repo, alt_repo.lower()))
                    if not self.c.fetchone():
                        missing.append((os.path.basename(bp_file), tier["tier_id"], alt_repo))

        self.assertEqual(len(missing), 0, f"Found uncataloged repositories in blueprints: {missing}")

    def test_production_readiness_and_quickstart(self):
        """Verify production readiness and quickstart setup steps are actionable."""
        bp_files = [
            f for f in glob.glob(os.path.join(BLUEPRINTS_DIR, "*.json"))
            if not f.endswith("index.json")
        ]
        for bp_file in bp_files:
            with open(bp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            pr = data["production_readiness"]
            self.assertTrue(len(pr["sla_target"]) > 5)
            self.assertGreaterEqual(len(pr["security_considerations"]), 2)
            self.assertGreaterEqual(len(pr["failure_modes_and_mitigations"]), 2)
            
            qs = data["quickstart"]
            self.assertGreaterEqual(len(qs["setup_commands"]), 2)
            self.assertTrue(len(qs["sample_config_or_code"]) > 20)

    def test_engine_recommendations(self):
        """Verify RecommendationEngine can query and match blueprints."""
        from scripts.engine.recommendation_engine import RecommendationEngine
        engine = RecommendationEngine(DB_PATH)
        bps = engine.list_blueprints()
        self.assertEqual(len(bps), 5)
        
        # Test exact retrieval
        ai_bp = engine.get_blueprint("BP-AI-AGENT-01")
        self.assertIsNotNone(ai_bp)
        self.assertEqual(ai_bp["blueprint_id"], "BP-AI-AGENT-01")
        
        # Test query matching
        rec = engine.recommend_blueprint("build an autonomous AI agent with LangGraph")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["blueprint"]["blueprint_id"], "BP-AI-AGENT-01")
        self.assertGreaterEqual(rec["confidence"], 0.5)

if __name__ == "__main__":
    unittest.main()
