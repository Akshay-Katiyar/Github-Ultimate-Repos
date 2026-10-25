import os
import sys
import json
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLI_SCRIPT = os.path.join(REPO_ROOT, "scripts", "cli", "ultimate_agent_cli.py")

class TestCompareCLIIntegration(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, CLI_SCRIPT] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, encoding="utf-8")
        return res

    def test_cli_compare_terminal_three_repos(self):
        res = self.run_cli(["compare", "AutoGPT", "crewAI", "langchain"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("REPOSITORY COMPARISON & ARCHITECTURAL TRADE-OFF MATRIX", res.stdout)
        self.assertIn("BENCHMARK SCORECARD", res.stdout)
        self.assertIn("AutoGPT", res.stdout)
        self.assertIn("crewAI", res.stdout)
        self.assertIn("langchain", res.stdout)
        self.assertIn("STRATEGIC DECISION GUIDE", res.stdout)

    def test_cli_compare_markdown_format(self):
        res = self.run_cli(["compare", "AutoGPT", "crewAI", "--format", "markdown"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("# Repository Comparison & Architectural Trade-off Dossier", res.stdout)
        self.assertIn("| Dimension |", res.stdout)
        self.assertIn("## 4. Strategic Decision Guide", res.stdout)

    def test_cli_compare_json_format(self):
        res = self.run_cli(["compare", "AutoGPT", "crewAI", "--format", "json"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["repository_count"], 2)
        self.assertIn("repositories", data)
        self.assertIn("tradeoff_analysis", data)

    def test_cli_compare_single_repo_fails(self):
        res = self.run_cli(["compare", "AutoGPT"])
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Error", res.stdout + res.stderr)

if __name__ == "__main__":
    unittest.main()
