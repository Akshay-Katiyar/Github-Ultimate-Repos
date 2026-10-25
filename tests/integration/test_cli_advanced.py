import os
import sys
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLI_SCRIPT = os.path.join(REPO_ROOT, "scripts", "cli", "ultimate_agent_cli.py")

class TestCLIAdvanced(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, CLI_SCRIPT] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, encoding="utf-8")
        return res

    def test_cli_recommend(self):
        res = self.run_cli(["recommend", "ai agent tools", "--limit", "2"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("RECOMMENDATION", res.stdout.upper())
        self.assertIn("Match Score", res.stdout)

    def test_cli_compare(self):
        res = self.run_cli(["compare", "AutoGPT", "langchain"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("COMPARISON MATRIX", res.stdout)

    def test_cli_workflow(self):
        res = self.run_cli(["workflow"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("WORKFLOW", res.stdout.upper())

        res2 = self.run_cli(["workflow", "ai-agent"])
        self.assertEqual(res2.returncode, 0)
        self.assertIn("STAGE 1", res2.stdout.upper())

if __name__ == "__main__":
    unittest.main()
