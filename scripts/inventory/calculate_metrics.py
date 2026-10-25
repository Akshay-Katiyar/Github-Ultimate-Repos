import os
import csv
import json
import statistics
import sys
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "starred_repos_master_catalog.csv")

def get_stats():
    repos_by_cat = defaultdict(list)
    cat_names = []

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["Category"].strip()
            if cat not in cat_names:
                cat_names.append(cat)
            stars = int(row["Stars"]) if row["Stars"] else 0
            forks = int(row["Forks"]) if row["Forks"] else 0
            repos_by_cat[cat].append({
                "name": row["Repository"].strip(),
                "stars": stars,
                "forks": forks,
                "lang": row["Language"].strip() or "Other",
                "desc": row["Description"].strip(),
                "workflow": row["Workflow"].strip(),
                "url": row["URL"].strip()
            })

    total_repos_all = sum(len(r) for r in repos_by_cat.values())
    total_stars_all = sum(sum(r["stars"] for r in rlist) for rlist in repos_by_cat.values())
    total_forks_all = sum(sum(r["forks"] for r in rlist) for rlist in repos_by_cat.values())

    cat_stats = {}
    for idx, cat in enumerate(cat_names, 1):
        repos = repos_by_cat[cat]
        stars = [r["stars"] for r in repos]
        forks = [r["forks"] for r in repos]
        langs = Counter(r["lang"] for r in repos)

        brackets = {
            "tier_50k_plus": sum(1 for s in stars if s >= 50000),
            "tier_20k_50k": sum(1 for s in stars if 20000 <= s < 50000),
            "tier_5k_20k": sum(1 for s in stars if 5000 <= s < 20000),
            "tier_1k_5k": sum(1 for s in stars if 1000 <= s < 5000),
            "tier_under_1k": sum(1 for s in stars if s < 1000)
        }

        top_repos = sorted(repos, key=lambda x: x["stars"], reverse=True)[:5]
        top_languages = []
        for l, count in langs.most_common(5):
            top_languages.append({
                "language": l,
                "count": count,
                "percentage": round((count / len(repos)) * 100, 2)
            })

        cat_stats[idx] = {
            "id": idx,
            "name": cat,
            "total_repositories": len(repos),
            "total_stars": sum(stars),
            "total_forks": sum(forks),
            "average_stars": round(statistics.mean(stars), 1) if stars else 0,
            "median_stars": round(statistics.median(stars), 1) if stars else 0,
            "star_percentage": round((sum(stars) / total_stars_all) * 100, 2),
            "repo_percentage": round((len(repos) / total_repos_all) * 100, 2),
            "star_distribution": brackets,
            "primary_languages": top_languages,
            "top_repositories": [
                {
                    "name": r["name"],
                    "stars": r["stars"],
                    "forks": r["forks"],
                    "language": r["lang"],
                    "url": r["url"],
                    "workflow": r["workflow"]
                }
                for r in top_repos
            ]
        }

    return {
        "total_repositories": total_repos_all,
        "total_stars": total_stars_all,
        "total_forks": total_forks_all,
        "category_stats": cat_stats
    }

if __name__ == "__main__":
    data = get_stats()
    print(f"Total Repos: {data['total_repositories']}")
    print(f"Total Stars: {data['total_stars']:,}")
    print(f"Total Forks: {data['total_forks']:,}")
    for i in range(1, 11):
        cs = data["category_stats"][i]
        print(f"[{i:02d}] {cs['name'][:40]} | Repos: {cs['total_repositories']:,} | Stars: {cs['total_stars']:,}★ | Med: {cs['median_stars']}")
