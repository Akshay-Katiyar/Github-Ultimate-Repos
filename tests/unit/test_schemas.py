import os
import glob
import json
import unittest
import jsonschema
from jsonschema import Draft7Validator

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

    def test_mcp_tools_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "mcp_tools_schema.json")
        self.assertTrue(os.path.exists(schema_path), "mcp_tools_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "MCPToolsCatalogSchema")
        self.assertIn("tools", schema["required"])

    def test_agent_discovery_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "agent_discovery_schema.json")
        self.assertTrue(os.path.exists(schema_path), "agent_discovery_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "AgentDiscoverySchema")
        self.assertIn("query_contract", schema["required"])

    def test_comparison_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "comparison_schema.json")
        self.assertTrue(os.path.exists(schema_path), "comparison_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "RepositoryComparisonMatrix")
        self.assertIn("repositories", schema["required"])
        self.assertIn("tradeoff_analysis", schema["required"])

    def test_workflow_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "workflow_schema.json")
        self.assertTrue(os.path.exists(schema_path), "workflow_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "WorkflowSpecification")
        self.assertIn("required", schema)
        self.assertIn("workflow_id", schema["required"])
        self.assertIn("stages", schema["required"])
        self.assertIn("governance", schema["required"])

    def test_stack_blueprint_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "stack_blueprint_schema.json")
        self.assertTrue(os.path.exists(schema_path), "stack_blueprint_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "StackBlueprint")
        self.assertIn("required", schema)
        self.assertIn("blueprint_id", schema["required"])
        self.assertIn("tiers", schema["required"])
        self.assertIn("data_flow_stages", schema["required"])
        self.assertIn("production_readiness", schema["required"])

    def test_taxonomy_schema_structure(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "taxonomy_schema.json")
        self.assertTrue(os.path.exists(schema_path), "taxonomy_schema.json must exist")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        self.assertEqual(schema["title"], "DisciplineTaxonomySpecification")
        self.assertIn("required", schema)
        self.assertIn("version", schema["required"])
        self.assertIn("total_disciplines", schema["required"])
        self.assertIn("clusters", schema["required"])
        self.assertIn("disciplines", schema["required"])

    def test_taxonomy_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "taxonomy_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        tax_path = os.path.join(REPO_ROOT, "registry", "taxonomy.json")
        self.assertTrue(os.path.exists(tax_path), "registry/taxonomy.json must exist")
        with open(tax_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        jsonschema.validate(instance=data, schema=schema)

    def test_all_schemas_conform_to_draft07(self):
        schemas_dir = os.path.join(REPO_ROOT, "schemas")
        schema_files = [
            "agent_discovery_schema.json",
            "agent_schema.json",
            "comparison_schema.json",
            "mcp_tools_schema.json",
            "repository_schema.json",
            "stack_blueprint_schema.json",
            "taxonomy_schema.json",
            "workflow_schema.json"
        ]
        for sfile in schema_files:
            spath = os.path.join(schemas_dir, sfile)
            self.assertTrue(os.path.exists(spath), f"{sfile} must exist")
            with open(spath, "r", encoding="utf-8") as f:
                schema_data = json.load(f)
            # Metaschema validation
            Draft7Validator.check_schema(schema_data)
            self.assertEqual(schema_data.get("$schema"), "http://json-schema.org/draft-07/schema#", f"{sfile} must declare Draft-07 $schema")

    def test_workflow_sample_payloads(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "workflow_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        wf_files = sorted(glob.glob(os.path.join(REPO_ROOT, "workflows", "workflow-*.json")))
        self.assertGreaterEqual(len(wf_files), 6, "Expected at least 6 workflow files")
        for wf_file in wf_files:
            with open(wf_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            jsonschema.validate(instance=data, schema=schema)

    def test_blueprint_sample_payloads(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "stack_blueprint_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        bp_files = sorted([
            f for f in glob.glob(os.path.join(REPO_ROOT, "blueprints", "*.json"))
            if not f.endswith("index.json")
        ])
        self.assertGreaterEqual(len(bp_files), 5, "Expected at least 5 blueprint files")
        for bp_file in bp_files:
            with open(bp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            jsonschema.validate(instance=data, schema=schema)

    def test_comparison_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "comparison_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        cmp_file = os.path.join(REPO_ROOT, "reports", "comparison_autogpt_crewai_langchain.json")
        self.assertTrue(os.path.exists(cmp_file), "comparison sample file must exist")
        with open(cmp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        jsonschema.validate(instance=data, schema=schema)

    def test_mcp_tools_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "mcp_tools_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        import sys
        cli_dir = os.path.join(REPO_ROOT, "scripts", "cli")
        if cli_dir not in sys.path:
            sys.path.insert(0, cli_dir)
        from mcp_server import SERVER_NAME, PROTOCOL_VERSION, MCP_TOOLS
        
        payload = {
            "server": SERVER_NAME,
            "protocol_version": PROTOCOL_VERSION,
            "tools": MCP_TOOLS
        }
        jsonschema.validate(instance=payload, schema=schema)

    def test_agent_discovery_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "agent_discovery_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        payload = {
            "service_identifier": "github-ultimate-repos-agent-service",
            "version": "1.0.0",
            "catalog_summary": {
                "total_repositories": 11730,
                "disciplines_count": 55,
                "storage_engine": "SQLite FTS5",
                "full_text_search": "BM25"
            },
            "capabilities": [
                "full_text_search_fts5",
                "intent_recommendation",
                "side_by_side_comparison",
                "architecture_workflow_extraction",
                "discipline_taxonomy_browsing",
                "mcp_stdio_transport",
                "cli_json_export"
            ],
            "discovery_endpoints": {
                "mcp_stdio": {
                    "command": "python",
                    "args": ["scripts/cli/mcp_server.py"],
                    "protocol": "jsonrpc-2.0"
                },
                "cli_exec": {
                    "entrypoint": "scripts/cli/ultimate_agent_cli.py",
                    "commands": ["search", "get", "recommend", "compare", "workflow", "categories", "stats"]
                },
                "sqlite_direct": {
                    "path": "registry/agents_registry.db",
                    "tables": ["repositories", "repositories_fts"]
                }
            },
            "supported_agent_clients": [
                {"name": "cline", "integration_mode": "mcp", "configuration_file": ".cursor/mcp.json"},
                {"name": "claude-code", "integration_mode": "cli", "configuration_file": "config.json"}
            ],
            "query_contract": {
                "action": "search",
                "query": "vector database",
                "limit": 10
            },
            "response_contract": {
                "status": "success",
                "data": [],
                "execution_metadata": {
                    "engine": "FTS5",
                    "latency_ms": 1.2
                }
            }
        }
        jsonschema.validate(instance=payload, schema=schema)


    def test_repository_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "repository_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        sample = {
            "id": 1,
            "name": "sindresorhus/awesome",
            "url": "https://github.com/sindresorhus/awesome",
            "stars": 338000,
            "forks": 29000,
            "language": "Other",
            "category_id": 1,
            "category_name": "Curated Knowledge, Developer Guides, Books & Awesome Collections",
            "description": "Awesome lists about all kinds of interesting topics",
            "architecture_workflow": "Markdown Catalog -> Static Generator -> GitHub Pages",
            "quality_gate": "VERIFIED"
        }
        jsonschema.validate(instance=sample, schema=schema)

    def test_agent_sample_payload(self):
        schema_path = os.path.join(REPO_ROOT, "schemas", "agent_schema.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        
        sample = {
            "agent_id": "AGENT-00001",
            "name": "AutoGPT Autonomous Agent Swarm",
            "category": "Multi-Agent Systems, Autonomous Swarms & MCP Tools",
            "role": "Autonomous Task Planner & Orchestrator",
            "capabilities": ["task_planning", "tool_execution", "recursive_reasoning"],
            "architecture_workflow": "Goal -> Recursive Task Decomposition -> Tool Execution Loop",
            "source_repository": "Significant-Gravitas/AutoGPT",
            "status": "ready"
        }
        jsonschema.validate(instance=sample, schema=schema)

if __name__ == "__main__":
    unittest.main()

