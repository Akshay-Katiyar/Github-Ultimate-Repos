import os
import sys
import ast
import sqlite3
import tempfile
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "cli"))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "validation"))

from ultimate_agent_cli import sanitize_csv_value, sanitize_csv_row, get_connection
from security_audit import ASTSecurityAuditor, scan_ast_security, scan_secret_leakage


class TestSecurityDefenses(unittest.TestCase):
    """Defensive security test suite verifying injection and supply-chain protections."""

    def test_csv_formula_injection_sanitization(self):
        """Verify that dangerous CSV formula triggers (=, +, -, @, \\t, \\r) are sanitized."""
        # 1. Direct triggers
        self.assertEqual(sanitize_csv_value("=1+1"), "'=1+1")
        self.assertEqual(sanitize_csv_value("+SUM(A1:A10)"), "'+SUM(A1:A10)")
        self.assertEqual(sanitize_csv_value("-2+3+cmd|' /C calc'!A0"), "'-2+3+cmd|' /C calc'!A0")
        self.assertEqual(sanitize_csv_value("@import"), "'@import")
        self.assertEqual(sanitize_csv_value("\t=DDE(1)"), "'\t=DDE(1)")
        self.assertEqual(sanitize_csv_value("\r=cmd"), "'\r=cmd")

        # 2. Whitespace padded triggers (frequently used to bypass naive checks)
        self.assertEqual(sanitize_csv_value("  =1+1"), "'  =1+1")
        self.assertEqual(sanitize_csv_value("   +cmd"), "'   +cmd")
        self.assertEqual(sanitize_csv_value("\t\t@calc"), "'\t\t@calc")

        # 3. Safe values must NOT be altered
        self.assertEqual(sanitize_csv_value("huggingface/transformers"), "huggingface/transformers")
        self.assertEqual(sanitize_csv_value("LangChain Ecosystem"), "LangChain Ecosystem")
        self.assertEqual(sanitize_csv_value(168000), 168000)
        self.assertEqual(sanitize_csv_value(0), 0)
        self.assertEqual(sanitize_csv_value(""), "")
        self.assertIsNone(sanitize_csv_value(None))

    def test_csv_row_sanitization(self):
        """Verify dictionary row sanitization for CSV export."""
        malicious_row = {
            "name": "=cmd|' /C calc'!A0",
            "stars": 50000,
            "url": "https://github.com/example/repo",
            "description": "@malicious formula payload",
            "workflow": "+step1 -> +step2"
        }
        clean = sanitize_csv_row(malicious_row)
        self.assertTrue(clean["name"].startswith("'="))
        self.assertEqual(clean["stars"], 50000)
        self.assertTrue(clean["description"].startswith("'@"))
        self.assertTrue(clean["workflow"].startswith("'+"))

    def test_sqlite_injection_resistance(self):
        """Verify SQLite database immunity against SQL injection payloads."""
        conn = get_connection()
        cursor = conn.cursor()

        # Check baseline count
        cursor.execute("SELECT COUNT(*) FROM repositories;")
        baseline_count = cursor.fetchone()[0]

        # 1. SQL Injection attempt via name lookup
        sqli_payload = "test' OR '1'='1' --"
        cursor.execute("SELECT * FROM repositories WHERE name = ? OR name LIKE ? LIMIT 1;", [sqli_payload, f"%/{sqli_payload}"])
        res = cursor.fetchall()
        self.assertEqual(len(res), 0, "Parameterized query must treat payload as literal string, returning 0 rows")

        # 2. SQL Injection attempt via DROP TABLE in search
        drop_payload = "'; DROP TABLE repositories; --"
        cursor.execute("""
            SELECT id, name FROM repositories
            WHERE (name LIKE ? OR description LIKE ?)
            LIMIT 5;
        """, [f"%{drop_payload}%", f"%{drop_payload}%"])
        _ = cursor.fetchall()

        # Verify table integrity
        cursor.execute("SELECT COUNT(*) FROM repositories;")
        after_count = cursor.fetchone()[0]
        self.assertEqual(after_count, baseline_count, "Repositories table must remain intact after injection payload")

        # 3. FTS5 MATCH parameterization
        fts_payload = 'malicious" OR 1=1 --'
        try:
            cursor.execute("""
                SELECT r.id FROM repositories_fts f
                JOIN repositories r ON f.rowid = r.id
                WHERE repositories_fts MATCH ?
                LIMIT 5;
            """, [fts_payload])
            _ = cursor.fetchall()
        except sqlite3.OperationalError:
            pass  # FTS parser error on syntax is safe and expected

        conn.close()

    def test_ast_auditor_detects_unsafe_primitives(self):
        """Verify ASTSecurityAuditor detects eval, exec, and pickle."""
        test_snippet = """
import pickle
from marshal import dumps

def bad_func():
    eval('2 + 2')
    exec('x = 1')
    pickle.loads(b'payload')
    import os
    os.system('rm -rf /')
"""
        tree = ast.parse(test_snippet)
        auditor = ASTSecurityAuditor("test_snippet.py")
        auditor.visit(tree)

        finding_msgs = [f[2] for f in auditor.findings]
        self.assertTrue(any("pickle" in m for m in finding_msgs), "Should detect pickle import")
        self.assertTrue(any("marshal" in m for m in finding_msgs), "Should detect marshal import")
        self.assertTrue(any("eval()" in m for m in finding_msgs), "Should detect eval call")
        self.assertTrue(any("exec()" in m for m in finding_msgs), "Should detect exec call")
        self.assertTrue(any("pickle.loads()" in m for m in finding_msgs), "Should detect pickle.loads call")
        self.assertTrue(any("os.system()" in m for m in finding_msgs), "Should detect os.system call")

    def test_full_repository_ast_is_clean(self):
        """Verify that zero unsafe AST patterns exist in the repository."""
        findings = scan_ast_security(REPO_ROOT)
        self.assertEqual(len(findings), 0, f"Repository must have 0 unsafe AST calls, found: {findings}")

    def test_full_repository_has_zero_secrets(self):
        """Verify that zero hardcoded credentials or API tokens exist in the repository."""
        findings = scan_secret_leakage(REPO_ROOT)
        self.assertEqual(len(findings), 0, f"Repository must have 0 secret findings, found: {findings}")


if __name__ == "__main__":
    unittest.main()
