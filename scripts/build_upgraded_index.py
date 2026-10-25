# -*- coding: utf-8 -*-
"""
build_upgraded_index.py
Build and verification utility for index.html in GitHub Ultimate Repos.
Ensures zero-dependency client-side architecture and validates that all 11,730
repository data records and animated system architecture components are intact.
"""

import os
import sys
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_HTML = os.path.join(REPO_ROOT, "index.html")
BACKUP_HTML = os.path.join(REPO_ROOT, "index.html.bak")

def verify_and_sync_index():
    """Verify index.html integrity, total records, and accessibility markers."""
    if not os.path.exists(INDEX_HTML):
        if os.path.exists(BACKUP_HTML):
            print(f"Restoring {INDEX_HTML} from backup...")
            with open(BACKUP_HTML, "r", encoding="utf-8") as f_in, open(INDEX_HTML, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        else:
            raise FileNotFoundError(f"Neither {INDEX_HTML} nor {BACKUP_HTML} exists.")

    print(f"Verifying {INDEX_HTML}...")
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify zero-dependency
    assert "<script" in content, "Missing script tags in index.html"
    assert "https://cdn." not in content, "External CDN dependency detected; must remain zero-dependency"
    
    # Verify records
    data_marker = "const allData = "
    assert data_marker in content, "Missing const allData definition"
    start_pos = content.find(data_marker) + len(data_marker)
    end_pos = content.find(";\n", start_pos)
    if end_pos == -1:
        end_pos = content.find(";", start_pos)
    
    data_json_str = content[start_pos:end_pos].strip()
    records = json.loads(data_json_str)
    assert len(records) == 11730, f"Expected 11,730 records, found {len(records)}"

    # Verify key architectural elements
    assert "arch-pipeline-section" in content, "Missing animated architecture visualizer"
    assert "class=\"skip-link\"" in content, "Missing skip-link accessibility feature"
    assert ":focus-visible" in content, "Missing focus-visible styling"
    assert "@media (prefers-reduced-motion: reduce)" in content, "Missing prefers-reduced-motion CSS support"

    print(f"[OK] index.html successfully verified! {len(records):,} records present and zero dependencies.")
    return True

if __name__ == "__main__":
    verify_and_sync_index()
