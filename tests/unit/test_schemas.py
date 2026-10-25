import os
import json
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class TestSchemas(unittest.TestCase):
    def test_repository_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "repository_schema.json")
        self.assertTrue(os.path.exists(schema_path), "repository_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "RepositoryRecord")
        self.assertIn("required", schema)
        self.assertIn("name", schema["required"])
        self.assertIn("stars", schema["required"])
        self.assertIn("architecture_workflow", schema["required"])

    def test_agent_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "agent_schema.json")
        self.assertTrue(os.path.exists(schema_path), "agent_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "AgentSpecification")
        self.assertIn("required", schema)
        self.assertIn("agent_id", schema["required"])
        self.assertIn("capabilities", schema["required"])

if __name__ == "__main__":
    unittest.main()
