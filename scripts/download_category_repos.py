#!/usr/bin/env python3
"""
download_category_repos.py - Concurrent Downloader / Cloner for Categorized Repositories

Features:
- Shallow git cloning (--mode clone, uses git clone --depth 1 --single-branch)
- Direct Zip archiving (--mode zip, downloads repo archive directly)
- Multi-threaded concurrent execution
- Resume & skip existing repositories
- Category filter and limit controls
"""

import os
import sys
import json
import argparse
import subprocess
import urllib.request
import concurrent.futures
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Aryan\Github-Ultimate-Repos")
INVENTORY_PATH = REPO_ROOT / "reports" / "repository-inventory.json"
DEFAULT_DOWNLOADS = REPO_ROOT / "downloads"

def clone_repo(record, target_dir):
    name = record["name"]
    url = record["url"]
    dest_path = target_dir / name.replace("/", "__")
    
    if dest_path.exists() and (dest_path / ".git").exists():
        return f"[SKIP] {name} already exists."
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth", "1", "--single-branch", f"{url}.git", str(dest_path)]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=120)
        if res.returncode == 0:
            return f"[OK] Cloned: {name}"
        else:
            return f"[ERR] {name}: {res.stderr.strip()[:100]}"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT] {name} clone timed out (>120s)"
    except Exception as e:
        return f"[FAIL] {name}: {str(e)}"

def download_zip(record, target_dir):
    name = record["name"]
    dest_file = target_dir / f"{name.replace('/', '__')}.zip"
    
    if dest_file.exists() and dest_file.stat().st_size > 0:
        return f"[SKIP] {name}.zip already exists."
    
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    # Try main first, then master
    urls_to_try = [
        f"https://github.com/{name}/archive/refs/heads/main.zip",
        f"https://github.com/{name}/archive/refs/heads/master.zip"
    ]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp, open(dest_file, "wb") as out_f:
                out_f.write(resp.read())
            return f"[OK] Downloaded Zip: {name}"
        except Exception:
            continue
            
    return f"[FAIL] {name} Zip download failed on main/master branches"

def main():
    parser = argparse.ArgumentParser(description="Download or clone repositories by category")
    parser.add_argument("--category", type=int, default=1, help="Category ID (1 to 55, default: 1)")
    parser.add_argument("--mode", choices=["clone", "zip"], default="clone", help="Download mode: 'clone' (shallow git clone) or 'zip' (source archive)")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of repos to download (0 for all)")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent worker threads")
    parser.add_argument("--output", type=str, default="", help="Custom output directory")
    args = parser.parse_args()

    if not INVENTORY_PATH.exists():
        print(f"Error: Inventory not found at {INVENTORY_PATH}")
        sys.exit(1)

    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    category_repos = [r for r in data["records"] if r["category_id"] == args.category]
    if not category_repos:
        print(f"No repositories found for Category {args.category}")
        sys.exit(1)

    category_name = category_repos[0]["category_name"]
    print(f"\n=======================================================")
    print(f"Category [{args.category:02d}]: {category_name}")
    print(f"Total Repos in Category: {len(category_repos)}")
    print(f"Mode: {args.mode.upper()} | Limit: {args.limit if args.limit > 0 else 'ALL'}")
    print(f"=======================================================\n")

    target_repos = category_repos[:args.limit] if args.limit > 0 else category_repos
    out_dir = Path(args.output) if args.output else DEFAULT_DOWNLOADS / f"category_{args.category:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving to: {out_dir}\n")

    download_fn = clone_repo if args.mode == "clone" else download_zip

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_fn, r, out_dir): r["name"] for r in target_repos}
        for future in concurrent.futures.as_completed(futures):
            repo_name = futures[future]
            try:
                res = future.result()
                print(res)
            except Exception as e:
                print(f"[ERROR] {repo_name}: {e}")

    print(f"\nFinished processing {len(target_repos)} repositories in Category {args.category:02d}.\n")

if __name__ == "__main__":
    main()
