# Enterprise Test Suite
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

for sub in ["scripts", os.path.join("scripts", "cli"), os.path.join("scripts", "engine"), os.path.join("scripts", "inventory"), os.path.join("scripts", "ranking")]:
    p = os.path.join(REPO_ROOT, sub)
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)
