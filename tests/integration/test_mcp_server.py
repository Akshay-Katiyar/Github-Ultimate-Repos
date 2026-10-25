import sys
import os
import json
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MCP_SERVER_SCRIPT = os.path.join(REPO_ROOT, "scripts", "cli", "mcp_server.py")
MCP_SCHEMA_FILE = os.path.join(REPO_ROOT, "schemas", "mcp_tools_schema.json")

class TestMCPServerIntegration(unittest.TestCase):
    def test_mcp_protocol_exchange(self):
        proc = subprocess.Popen(
            [sys.executable, MCP_SERVER_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=REPO_ROOT
        )

        def send_and_recv(msg):
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()
            line = proc.stdout.readline()
            return json.loads(line)

        try:
            # 1. initialize handshake
            init_req = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0"}
                }
            }
            init_res = send_and_recv(init_req)
            self.assertEqual(init_res["id"], 1)
            self.assertEqual(init_res["result"]["serverInfo"]["name"], "github-ultimate-repos-mcp")
            self.assertEqual(init_res["result"]["serverInfo"]["version"], "1.0.0")
            self.assertIn("tools", init_res["result"]["capabilities"])
            self.assertIn("resources", init_res["result"]["capabilities"])

            # 2. tools/list verification and schema validation
            tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
            tools_res = send_and_recv(tools_req)
            self.assertEqual(tools_res["id"], 2)
            tool_list = tools_res["result"]["tools"]
            tool_names = [t["name"] for t in tool_list]

            expected_tools = [
                "search_repositories",
                "get_repository",
                "get_repository_details",
                "recommend_stack",
                "recommend_repositories",
                "compare_repositories",
                "get_workflow",
                "list_categories",
                "get_catalog_stats"
            ]
            for tool_name in expected_tools:
                self.assertIn(tool_name, tool_names, f"Expected tool '{tool_name}' missing from tools/list")

            # Validate tools payload against schemas/mcp_tools_schema.json
            with open(MCP_SCHEMA_FILE, "r", encoding="utf-8") as sf:
                mcp_schema = json.load(sf)
            try:
                import jsonschema
                schema_payload = {
                    "server": "github-ultimate-repos-mcp",
                    "protocol_version": "2024-11-05",
                    "transport": "stdio",
                    "tools": tool_list
                }
                jsonschema.validate(instance=schema_payload, schema=mcp_schema)
            except ImportError:
                # Fallback structural checks
                allowed_names = set(mcp_schema["properties"]["tools"]["items"]["properties"]["name"]["enum"])
                for t in tool_list:
                    self.assertIn(t["name"], allowed_names)
                    self.assertIn("description", t)
                    self.assertIn("inputSchema", t)

            # 3. tools/call -> search_repositories
            call_search = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_repositories",
                    "arguments": {"query": "cline", "limit": 2}
                }
            }
            search_res = send_and_recv(call_search)
            self.assertEqual(search_res["id"], 3)
            content_text = json.loads(search_res["result"]["content"][0]["text"])
            self.assertGreater(content_text["count"], 0)
            self.assertIn("repositories", content_text)

            # 4. tools/call -> get_repository
            call_get = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_repository",
                    "arguments": {"name": "AutoGPT"}
                }
            }
            get_res = send_and_recv(call_get)
            self.assertEqual(get_res["id"], 4)
            get_content = json.loads(get_res["result"]["content"][0]["text"])
            self.assertIn("Significant-Gravitas/AutoGPT", get_content["repository"]["name"])

            # 5. tools/call -> get_repository_details (alias)
            call_get_alias = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "get_repository_details",
                    "arguments": {"name": "cline/cline"}
                }
            }
            get_alias_res = send_and_recv(call_get_alias)
            self.assertEqual(get_alias_res["id"], 5)
            get_alias_content = json.loads(get_alias_res["result"]["content"][0]["text"])
            self.assertEqual(get_alias_content["repository"]["name"], "cline/cline")

            # 6. tools/call -> recommend_stack
            call_rec = {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {
                    "name": "recommend_stack",
                    "arguments": {"intent": "build autonomous ai agent", "limit": 3}
                }
            }
            rec_res = send_and_recv(call_rec)
            self.assertEqual(rec_res["id"], 6)
            rec_content = json.loads(rec_res["result"]["content"][0]["text"])
            self.assertIn("recommendations", rec_content)

            # 7. tools/call -> recommend_repositories (alias)
            call_rec_alias = {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "tools/call",
                "params": {
                    "name": "recommend_repositories",
                    "arguments": {"intent": "multi-agent swarm orchestration", "limit": 2}
                }
            }
            rec_alias_res = send_and_recv(call_rec_alias)
            self.assertEqual(rec_alias_res["id"], 7)
            rec_alias_content = json.loads(rec_alias_res["result"]["content"][0]["text"])
            self.assertIn("recommendations", rec_alias_content)

            # 8. tools/call -> compare_repositories
            call_comp = {
                "jsonrpc": "2.0",
                "id": 8,
                "method": "tools/call",
                "params": {
                    "name": "compare_repositories",
                    "arguments": {"repos": ["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI"]}
                }
            }
            comp_res = send_and_recv(call_comp)
            self.assertEqual(comp_res["id"], 8)
            comp_content = json.loads(comp_res["result"]["content"][0]["text"])
            self.assertEqual(len(comp_content["comparison"]), 2)

            # 9. tools/call -> get_workflow
            call_wf = {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "tools/call",
                "params": {
                    "name": "get_workflow",
                    "arguments": {}
                }
            }
            wf_res = send_and_recv(call_wf)
            self.assertEqual(wf_res["id"], 9)
            wf_content = json.loads(wf_res["result"]["content"][0]["text"])
            self.assertIn("available_workflows", wf_content)

            # 10. tools/call -> list_categories
            call_cat = {
                "jsonrpc": "2.0",
                "id": 10,
                "method": "tools/call",
                "params": {
                    "name": "list_categories",
                    "arguments": {}
                }
            }
            cat_res = send_and_recv(call_cat)
            self.assertEqual(cat_res["id"], 10)
            cat_content = json.loads(cat_res["result"]["content"][0]["text"])
            self.assertEqual(cat_content["total_categories"], 55)

            # 11. tools/call -> get_catalog_stats
            call_stats = {
                "jsonrpc": "2.0",
                "id": 11,
                "method": "tools/call",
                "params": {
                    "name": "get_catalog_stats",
                    "arguments": {}
                }
            }
            stats_res = send_and_recv(call_stats)
            self.assertEqual(stats_res["id"], 11)
            stats_content = json.loads(stats_res["result"]["content"][0]["text"])
            self.assertEqual(stats_content["total_repositories"], 11730)
            self.assertEqual(stats_content["total_disciplines"], 55)

            # 12. resources/list
            res_list_req = {"jsonrpc": "2.0", "id": 12, "method": "resources/list", "params": {}}
            res_list_res = send_and_recv(res_list_req)
            self.assertEqual(res_list_res["id"], 12)
            self.assertGreaterEqual(len(res_list_res["result"]["resources"]), 3)

            # 13. resources/read
            res_req = {
                "jsonrpc": "2.0",
                "id": 13,
                "method": "resources/read",
                "params": {"uri": "ultimate-repos://stats"}
            }
            read_res = send_and_recv(res_req)
            self.assertEqual(read_res["id"], 13)
            res_stats = json.loads(read_res["result"]["contents"][0]["text"])
            self.assertEqual(res_stats["total_repositories"], 11730)

            # 14. error handling: unknown tool
            call_unknown = {
                "jsonrpc": "2.0",
                "id": 14,
                "method": "tools/call",
                "params": {
                    "name": "non_existent_tool",
                    "arguments": {}
                }
            }
            unknown_res = send_and_recv(call_unknown)
            self.assertEqual(unknown_res["id"], 14)
            self.assertIn("error", unknown_res)
            self.assertEqual(unknown_res["error"]["code"], -32601)

        finally:
            proc.stdin.close()
            proc.stdout.close()
            proc.stderr.close()
            proc.wait(timeout=5)

if __name__ == "__main__":
    unittest.main()

