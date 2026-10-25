import os
import glob
import json
import sqlite3
import unittest
import jsonschema

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORKFLOWS_DIR = os.path.join(REPO_ROOT, "workflows")
SCHEMA_PATH = os.path.join(REPO_ROOT, "schemas", "workflow_schema.json")
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")

class TestWorkflows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)
        cls.conn = sqlite3.connect(DB_PATH)
        cls.c = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_workflow_schema_validity(self):
        """Verify workflow_schema.json is a valid Draft-07 JSON Schema."""
        self.assertTrue(os.path.exists(SCHEMA_PATH))
        self.assertEqual(self.schema["title"], "WorkflowSpecification")
        self.assertIn("required", self.schema)
        self.assertIn("workflow_id", self.schema["required"])
        self.assertIn("stages", self.schema["required"])
        self.assertIn("governance", self.schema["required"])

    def test_all_workflow_files_exist_and_validate(self):
        """Verify all 6 workflow JSON files validate against the schema."""
        workflow_files = sorted(glob.glob(os.path.join(WORKFLOWS_DIR, "workflow-*.json")))
        self.assertEqual(len(workflow_files), 6, "Expected exactly 6 domain workflow files")

        for wf_file in workflow_files:
            with self.subTest(file=os.path.basename(wf_file)):
                with open(wf_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                jsonschema.validate(instance=data, schema=self.schema)
                self.assertEqual(len(data["stages"]), data["total_stages"])
                self.assertTrue(data["workflow_id"].startswith("WORKFLOW-"))

    def test_yaml_mirrors_exist(self):
        """Verify each JSON workflow file has a corresponding YAML file."""
        json_files = glob.glob(os.path.join(WORKFLOWS_DIR, "workflow-*.json"))
        for jf in json_files:
            yf = jf.replace(".json", ".yaml")
            self.assertTrue(os.path.exists(yf), f"Missing YAML mirror for {jf}")

    def test_index_manifest(self):
        """Verify workflow_index.json exists and catalogs all 6 workflows."""
        index_file = os.path.join(WORKFLOWS_DIR, "workflow_index.json")
        self.assertTrue(os.path.exists(index_file))
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
        self.assertEqual(index["total_workflows"], 6)
        self.assertEqual(len(index["workflows"]), 6)

    def test_repository_references_exist_in_database(self):
        """Verify that every recommended repository in every stage exists in agents_registry.db."""
        workflow_files = glob.glob(os.path.join(WORKFLOWS_DIR, "workflow-*.json"))
        missing = []
        for wf_file in workflow_files:
            with open(wf_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for stage in data["stages"]:
                for repo in stage["recommended_repositories"]:
                    name = repo["name"]
                    self.c.execute("SELECT id FROM repositories WHERE name = ?", (name,))
                    if not self.c.fetchone():
                        missing.append((os.path.basename(wf_file), stage["stage_name"], name))

        self.assertEqual(len(missing), 0, f"Found uncataloged repositories: {missing}")

    def test_stage_pipeline_integrity(self):
        """Verify that stages have complete input/output handoffs and quality gates."""
        workflow_files = glob.glob(os.path.join(WORKFLOWS_DIR, "workflow-*.json"))
        for wf_file in workflow_files:
            with open(wf_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for stage in data["stages"]:
                self.assertTrue(len(stage["purpose"]) > 10)
                self.assertTrue(len(stage["input_handoff"]["artifacts"]) >= 1)
                self.assertTrue(len(stage["output_handoff"]["artifacts"]) >= 1)
                self.assertTrue(len(stage["dependencies"]) >= 1)
                self.assertTrue(len(stage["alternatives"]) >= 1)
                self.assertTrue(len(stage["quality_gate"]) > 5)

if __name__ == "__main__":
    unittest.main()
