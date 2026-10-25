# -*- coding: utf-8 -*-
"""
Unit tests for README.md structure, links, counts, and contributor experience.
"""

import os
import re
import unittest

class TestReadmeExperience(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.readme_path = os.path.join(cls.repo_root, "README.md")
        with open(cls.readme_path, "r", encoding="utf-8") as f:
            cls.content = f.read()

    def test_readme_essential_questions(self):
        """Verify that all 5 essential questions are answered in the executive value proposition."""
        questions = [
            "1. What is Github Ultimate Repos?",
            "2. Why does it exist? (The Problem It Solves)",
            "3. Who is it for?",
            "4. How do I use it?",
            "5. How can I trust the data?"
        ]
        for q in questions:
            self.assertIn(q, self.content, f"Missing essential question: {q}")

    def test_readme_quickstart_coverage(self):
        """Verify quickstart covers CLI, Web Explorer, and MCP Server."""
        self.assertIn("scripts/cli/ultimate_agent_cli.py", self.content)
        self.assertIn("index.html", self.content)
        self.assertIn("scripts/cli/mcp_server.py", self.content)
        self.assertIn("claude_desktop_config.json", self.content)

    def test_readme_repository_and_discipline_counts(self):
        """Verify exact repository count (11,730) and 55 disciplines."""
        repo_entries = re.findall(r"^\d+\.\s+\*\*\[([^\]]+)\]\(", self.content, re.MULTILINE)
        self.assertEqual(len(repo_entries), 11730, f"Expected 11,730 repositories, found {len(repo_entries)}")

        cat_headers = re.findall(r"^###\s+\[\d{2}\]", self.content, re.MULTILINE)
        self.assertEqual(len(cat_headers), 55, f"Expected 55 disciplines, found {len(cat_headers)}")

    def test_readme_local_links_exist(self):
        """Verify 100% of relative markdown links point to valid files on disk."""
        file_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", self.content)
        missing_files = []
        for text, link in file_links:
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            file_part = link.split("#")[0]
            if not file_part:
                continue
            full_path = os.path.normpath(os.path.join(self.repo_root, file_part))
            if not os.path.exists(full_path):
                missing_files.append((text, link, full_path))

        self.assertEqual(len(missing_files), 0, f"Found broken relative links: {missing_files}")

    def test_readme_anchors_valid(self):
        """Verify anchor links have matching targets in the document."""
        file_links = re.findall(r"\[([^\]]+)\]\((#[^)]+)\)", self.content)
        for text, anchor in file_links:
            target_id = anchor[1:]
            pattern = rf'id=["\']{re.escape(target_id)}["\']'
            self.assertTrue(re.search(pattern, self.content, re.IGNORECASE), f"Missing target for anchor {anchor}")

    def test_readme_documentation_suite(self):
        """Verify that all 20 core documentation guides are linked in the documentation table."""
        docs_to_check = [
            "docs/getting-started.md",
            "docs/architecture.md",
            "docs/search-and-ranking.md",
            "docs/category-taxonomy.md",
            "docs/workflow-engine.md",
            "docs/repository-schema.md",
            "docs/data-sources-and-provenance.md",
            "docs/data-maintenance.md",
            "docs/cli-reference.md",
            "docs/security.md",
            "docs/testing.md",
            "docs/troubleshooting.md",
            "docs/contributing.md",
            "docs/release-process.md",
            "docs/faq.md",
            "docs/agent-catalog.md",
            "docs/configuration.md",
            "docs/ai-coding-and-mcp-integration.md",
            "docs/ranking-system.md",
            "docs/recommendation-engine.md",
        ]
        for doc in docs_to_check:
            self.assertIn(doc, self.content, f"Missing documentation link: {doc}")

if __name__ == "__main__":
    unittest.main()
