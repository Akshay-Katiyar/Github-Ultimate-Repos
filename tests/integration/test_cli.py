import os
import sys
import subprocess
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLI_SCRIPT = os.path.join(REPO_ROOT, "scripts", "cli", "ultimate_agent_cli.py")

class TestCLIIntegration(unittest.TestCase):
    def run_cli(self, args):
        cmd = [sys.executable, CLI_SCRIPT] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, encoding="utf-8")
        return res

    def test_cli_stats(self):
        res = self.run_cli(["stats"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("11,730", res.stdout)
        self.assertIn("55", res.stdout)

    def test_cli_search(self):
        res = self.run_cli(["search", "kubernetes", "--limit", "3"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("kubernetes", res.stdout.lower())

    def test_cli_get(self):
        res = self.run_cli(["get", "awesome"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("sindresorhus/awesome", res.stdout)
        self.assertIn("Workflow", res.stdout)

    def test_cli_category(self):
        res = self.run_cli(["category", "Robotics", "--limit", "3"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Category", res.stdout)

if __name__ == "__main__":
    unittest.main()
