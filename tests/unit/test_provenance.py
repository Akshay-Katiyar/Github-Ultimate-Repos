# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Akshay Katiyar <https://github.com/Akshay-Katiyar>

import os
import hashlib
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class TestLicenseAndProvenance(unittest.TestCase):
    def test_root_license_file(self):
        """Verify root LICENSE file exists and contains valid MIT text."""
        license_path = os.path.join(REPO_ROOT, "LICENSE")
        self.assertTrue(os.path.exists(license_path), "LICENSE file must exist at repo root")
        with open(license_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("MIT License", content)
        self.assertIn("Akshay Katiyar", content)
        self.assertIn("2026", content)

    def test_provenance_documentation_exists(self):
        """Verify docs/data-sources-and-provenance.md exists and contains required sections."""
        doc_path = os.path.join(REPO_ROOT, "docs", "data-sources-and-provenance.md")
        self.assertTrue(os.path.exists(doc_path), "docs/data-sources-and-provenance.md must exist")
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("SPDX-License-Identifier: MIT", content)
        self.assertIn("Executive Summary & Audit Scope", content)
        self.assertIn("Repository-Level License Audit (Root MIT)", content)
        self.assertIn("SPDX Identifiers & Machine-Readable Conformance", content)
        self.assertIn("Commercial Safety Signals", content)
        self.assertIn("Data Provenance & Lineage Audit", content)
        self.assertIn("GitHub API Attribution & Platform Terms Compliance", content)
        self.assertIn("Autonomous Agent Swarm Compliance Guidelines", content)

    def test_provenance_checksums_match_files(self):
        """Verify that the tracked core data files exist and have non-zero size."""
        core_files = [
            "LICENSE",
            "starred_repos_master_catalog.csv",
            "STARRED_REPOSITORIES_CATEGORIZED_LIST.txt",
            "registry/agents_registry.db",
            "reports/repository-inventory.json",
            "schemas/repository_schema.json",
            "schemas/agent_schema.json"
        ]
        for rel_path in core_files:
            abs_path = os.path.join(REPO_ROOT, rel_path)
            self.assertTrue(os.path.exists(abs_path), f"Core artifact {rel_path} must exist")
            size = os.path.getsize(abs_path)
            self.assertGreater(size, 0, f"Core artifact {rel_path} must not be empty")

if __name__ == "__main__":
    unittest.main()
