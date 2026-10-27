#!/usr/bin/env python3
"""
build_sets.py - Generate 100-repository batches/sets from the master inventory
"""

import os
import json
import csv
from pathlib import Path

REPO_ROOT = Path(r"C:\Users\Aryan\Github-Ultimate-Repos")
INVENTORY_PATH = REPO_ROOT / "reports" / "repository-inventory.json"
SETS_DIR = REPO_ROOT / "sets"

def build_set(set_index=1, batch_size=100, category_id=1):
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if category_id:
        repos = [r for r in data["records"] if r["category_id"] == category_id]
    else:
        repos = data["records"]

    start = (set_index - 1) * batch_size
    end = start + batch_size
    batch = repos[start:end]

    if not batch:
        print(f"No repositories for set {set_index}")
        return

    set_dir = SETS_DIR / f"set_{set_index:02d}"
    set_dir.mkdir(parents=True, exist_ok=True)

    # 1. URLs
    with open(set_dir / "urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(r["url"] for r in batch))

    # 2. Clone URLs
    with open(set_dir / "clone_urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(r["url"] + ".git" for r in batch))

    # 3. CSV
    with open(set_dir / "catalog.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Name", "Stars", "Forks", "Language", "URL", "Workflow", "Description"])
        for idx, r in enumerate(batch, start + 1):
            writer.writerow([idx, r["name"], r["stars"], r["forks"], r["language"], r["url"], r.get("architecture_workflow", ""), r.get("description", "")])

    # 4. JSON
    with open(set_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump({
            "set_id": set_index,
            "category_id": category_id,
            "start_rank": start + 1,
            "end_rank": start + len(batch),
            "count": len(batch),
            "repositories": batch
        }, f, indent=2)

    # 5. README Markdown
    cat_name = batch[0].get("category_name", "All Categories")
    lines = [
        f"# 📦 Set {set_index:02d} — Top {len(batch)} Repositories",
        "",
        f"**Category [{category_id:02d}]**: {cat_name}  ",
        f"**Batch Scope**: Repositories #{start + 1} to #{start + len(batch)}  ",
        f"**Stars Range**: {batch[-1]['stars']:,}★ to {batch[0]['stars']:,}★  ",
        "",
        "| # | Repository | Stars | Language | Description |",
        "| :---: | :--- | :---: | :---: | :--- |"
    ]
    for idx, r in enumerate(batch, start + 1):
        desc = (r.get("description") or "").replace("\n", " ").replace("|", "-")[:85]
        lines.append(f"| {idx:03d} | [{r['name']}]({r['url']}) | {r['stars']:,}★ | `{r.get('language', 'Other')}` | {desc}... |")

    with open(set_dir / "README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Successfully generated Set {set_index:02d} with {len(batch)} repositories in {set_dir}")

if __name__ == "__main__":
    build_set(set_index=1, batch_size=100, category_id=1)
