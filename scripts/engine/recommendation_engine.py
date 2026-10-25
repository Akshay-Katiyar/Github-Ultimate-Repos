#!/usr/bin/env python3
"""
recommendation_engine.py - Transparent, Multi-Factor Intelligent Repository Recommendation Engine

Provides intent-based repository recommendations, explainable multi-factor scoring,
trade-off evaluations, and alternatives discovery over 11,730 cataloged assets.
"""

import os
import sys
import sqlite3
import math
import re
import json
from typing import List, Dict, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")
BLUEPRINTS_DIR = os.path.join(REPO_ROOT, "blueprints")

STOPWORDS = {
    "with", "and", "the", "for", "from", "that", "this", "build", "want", 
    "which", "what", "how", "best", "some", "need", "using", "into", "over"
}

# Intent keyword taxonomy
INTENT_TAXONOMY = {
    "agent": {
        "keywords": ["agent", "autonomous", "swarm", "crew", "multi-agent", "mcp", "tool"],
        "category_hints": ["Multi-Agent Systems", "Artificial Intelligence"]
    },
    "rag": {
        "keywords": ["rag", "retrieval", "embedding", "vector", "qdrant", "milvus", "chroma", "knowledge"],
        "category_hints": ["Database Engines", "Artificial Intelligence", "Multi-Agent Systems"]
    },
    "database": {
        "keywords": ["database", "sql", "nosql", "postgres", "sqlite", "cache", "key-value", "local-first"],
        "category_hints": ["Database Engines", "Distributed Systems"]
    },
    "mobile": {
        "keywords": ["mobile", "flutter", "react native", "ios", "android", "cross-platform", "app"],
        "category_hints": ["Mobile App Development"]
    },
    "frontend": {
        "keywords": ["frontend", "ui", "react", "vue", "svelte", "nextjs", "tailwind", "component"],
        "category_hints": ["Modern Frontend Frameworks", "UI Component Systems"]
    },
    "devops": {
        "keywords": ["kubernetes", "k8s", "docker", "container", "ci/cd", "deploy", "terraform", "helm"],
        "category_hints": ["Cloud-Native Infrastructure", "CI/CD Automation"]
    },
    "security": {
        "keywords": ["security", "pentest", "vulnerability", "audit", "reverse engineering", "ghidra", "exploit"],
        "category_hints": ["Cybersecurity, Penetration Testing", "Digital Forensics"]
    },
    "robotics": {
        "keywords": ["robotics", "robot", "humanoid", "kinematics", "slam", "ros", "ros2", "simulation"],
        "category_hints": ["Robotics, Humanoid Kinematics", "Autonomous Vehicles"]
    },
    "seo": {
        "keywords": ["seo", "scraping", "crawler", "browser", "growth", "serp", "content"],
        "category_hints": ["Curated Knowledge", "Multi-Agent Systems", "Data Engineering"]
    }
}

# Re-exports of intelligent recommendation components for cross-module compatibility
try:
    from scripts.recommendation.recommendation_engine import (
        QueryParser,
        MultiFactorScorer,
        RecommendationCardGenerator,
        format_card_terminal,
        ScoreBreakdown,
        RecommendationCard,
        QueryDecomposition,
        INTENT_ARCHETYPES,
        SEMANTIC_SYNONYMS,
        CATEGORY_AFFINITY_MAP,
    )
except ImportError:
    pass

class RecommendationEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Registry DB not found at {self.db_path}")

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def detect_intents(self, query: str) -> List[str]:
        q_lower = query.lower()
        detected = []
        for intent, meta in INTENT_TAXONOMY.items():
            if any(k in q_lower for k in meta["keywords"]):
                detected.append(intent)
        return detected

    def filter_query_terms(self, query: str) -> List[str]:
        raw_tokens = re.split(r'[\s,+-]+', query.lower())
        return [t for t in raw_tokens if len(t) >= 3 and t not in STOPWORDS]

    def score_repository(self, repo: Dict[str, Any], query_terms: List[str], detected_intents: List[str], preferred_lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Interpretable multi-factor scoring policy:
        - Task Relevance (0 - 40 pts)
        - Architecture Fit (0 - 20 pts)
        - Community Maturity (0 - 20 pts)
        - Engagement Ratio (0 - 10 pts)
        - Language Match (0 - 10 pts)
        Total Score: 0 - 100 pts
        """
        name = repo["name"].lower()
        desc = repo["description"].lower()
        wf = repo["workflow"].lower()
        cat = repo["category_name"].lower()
        lang = repo["language"].lower()
        stars = repo["stars"]
        forks = repo["forks"]

        # 1. Task Relevance (0 - 40 pts)
        relevance_score = 0.0
        matched_terms = []
        for term in query_terms:
            term_score = 0.0
            if term in name:
                term_score += 15.0
            if term in desc:
                term_score += 10.0
            if term in cat:
                term_score += 8.0
            if term_score > 0:
                matched_terms.append(term)
                relevance_score += term_score

        # Significant boost if discipline matches detected intent
        for intent in detected_intents:
            meta = INTENT_TAXONOMY[intent]
            if any(h.lower() in cat for h in meta["category_hints"]):
                relevance_score += 15.0
                if intent not in matched_terms:
                    matched_terms.append(intent)

        relevance_score = min(40.0, relevance_score)

        # 2. Architecture Fit (0 - 20 pts)
        arch_score = 0.0
        if any(term in wf for term in query_terms):
            arch_score += 12.0
        if "->" in wf and len(wf) > 20:
            arch_score += 8.0
        arch_score = min(20.0, arch_score)

        # 3. Community Maturity (0 - 20 pts)
        if stars > 0:
            maturity_score = min(20.0, math.log10(stars) * 4.0)
        else:
            maturity_score = 0.0

        # 4. Engagement / Fork Ratio (0 - 10 pts)
        if stars > 0:
            fork_ratio = forks / stars
            engagement_score = min(10.0, fork_ratio * 40.0)
        else:
            engagement_score = 0.0

        # 5. Language Match (0 - 10 pts)
        lang_score = 5.0 # baseline neutral
        if preferred_lang:
            if preferred_lang.lower() in lang:
                lang_score = 10.0
            else:
                lang_score = 0.0

        total_score = round(relevance_score + arch_score + maturity_score + engagement_score + lang_score, 1)

        # Formulate strengths & limitations
        strengths = []
        if stars >= 50000:
            strengths.append(f"Industry gold-standard adoption ({stars:,}★, {forks:,} forks)")
        elif stars >= 10000:
            strengths.append(f"Strong production maturity ({stars:,}★)")
        else:
            strengths.append(f"Focused specialized tooling ({stars:,}★)")

        if len(wf) > 30:
            strengths.append(f"Verified operational pipeline: {wf[:80]}...")

        limitations = []
        if stars > 100000:
            limitations.append("Large enterprise codebase with significant dependencies; verify lightweight footprint requirement.")
        elif forks < 500:
            limitations.append("Smaller contributor base; evaluate community support responsiveness.")
        else:
            limitations.append("Ensure runtime compatibility with your target deployment environment.")

        why_matched = (
            f"Matches key term(s) [{', '.join(set(matched_terms[:3]))}] in "
            f"discipline '{repo['category_name']}' with strong architecture fit."
        ) if matched_terms else f"High topical alignment with discipline '{repo['category_name']}'."

        return {
            "total_score": total_score,
            "breakdown": {
                "relevance": round(relevance_score, 1),
                "architecture_fit": round(arch_score, 1),
                "community_maturity": round(maturity_score, 1),
                "engagement": round(engagement_score, 1),
                "language_fit": round(lang_score, 1)
            },
            "why_matched": why_matched,
            "strengths": strengths,
            "limitations": limitations
        }

    def recommend(self, query: str, limit: int = 5, category_filter: Optional[str] = None, preferred_lang: Optional[str] = None, min_stars: int = 0, category: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
        category_filter = category_filter or category
        clean_q = query.strip()
        terms = self.filter_query_terms(clean_q)
        detected_intents = self.detect_intents(clean_q)

        conn = self.get_connection()
        cursor = conn.cursor()

        candidates = []
        search_terms = terms.copy()
        for intent in detected_intents:
            search_terms.extend(INTENT_TAXONOMY[intent]["keywords"][:2])

        if search_terms:
            fts_query = " OR ".join(f'"{t}"' for t in search_terms[:6])
            try:
                cursor.execute("""
                SELECT r.* FROM repositories_fts f
                JOIN repositories r ON f.rowid = r.id
                WHERE repositories_fts MATCH ?
                LIMIT 200;
                """, [fts_query])
                candidates = [dict(row) for row in cursor.fetchall()]
            except sqlite3.OperationalError:
                candidates = []

        if not candidates and search_terms:
            like_clause = " OR ".join(["description LIKE ? OR name LIKE ? OR workflow LIKE ?" for _ in search_terms[:3]])
            params = []
            for t in search_terms[:3]:
                params.extend([f"%{t}%", f"%{t}%", f"%{t}%"])
            cursor.execute(f"SELECT * FROM repositories WHERE {like_clause} LIMIT 100;", params)
            candidates = [dict(row) for row in cursor.fetchall()]

        if not candidates:
            cursor.execute("SELECT * FROM repositories ORDER BY stars DESC LIMIT 50;")
            candidates = [dict(row) for row in cursor.fetchall()]

        # Filter and score candidates
        scored_candidates = []
        seen_names = set()

        for repo in candidates:
            if repo["name"] in seen_names:
                continue
            seen_names.add(repo["name"])

            if category_filter and category_filter.lower() not in repo["category_name"].lower():
                continue
            if min_stars > 0 and repo["stars"] < min_stars:
                continue

            scoring = self.score_repository(repo, terms, detected_intents, preferred_lang)
            
            # Find alternatives in same category
            cursor.execute("""
            SELECT name, stars, language, url FROM repositories
            WHERE category_id = ? AND name != ?
            ORDER BY stars DESC LIMIT 3;
            """, [repo["category_id"], repo["name"]])
            alts = [dict(alt_row) for alt_row in cursor.fetchall()]

            scored_candidates.append({
                "repository": repo["name"],
                "url": repo["url"],
                "stars": repo["stars"],
                "forks": repo["forks"],
                "language": repo["language"],
                "category": repo["category_name"],
                "description": repo["description"],
                "workflow": repo["workflow"],
                "score": scoring["total_score"],
                "score_breakdown": scoring["breakdown"],
                "why_matched": scoring["why_matched"],
                "strengths": scoring["strengths"],
                "limitations": scoring["limitations"],
                "alternatives": alts,
                "next_steps": [
                    f"Clone repository: git clone {repo['url']}.git",
                    f"Inspect architecture pipeline: {repo['workflow'][:90]}...",
                    "Review licensing and dependency requirements before production integration."
                ]
            })

        conn.close()

        # Sort by total_score descending
        scored_candidates.sort(key=lambda x: (x["score"], x["stars"]), reverse=True)
        return scored_candidates[:limit]

    def compare(self, repo_names: List[str]) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        results = []

        for name in repo_names:
            clean_name = name.strip()
            cursor.execute("""
            SELECT * FROM repositories
            WHERE name = ? OR name LIKE ? LIMIT 1;
            """, [clean_name, f"%/{clean_name}"])
            row = cursor.fetchone()
            if row:
                r = dict(row)
                results.append({
                    "name": r["name"],
                    "url": r["url"],
                    "stars": r["stars"],
                    "forks": r["forks"],
                    "language": r["language"],
                    "category": r["category_name"],
                    "description": r["description"],
                    "workflow": r["workflow"],
                    "maturity_tier": "Enterprise Gold" if r["stars"] >= 50000 else ("Production Standard" if r["stars"] >= 10000 else "Frontier Specialized")
                })
        conn.close()
        return results

    def load_blueprints(self) -> List[Dict[str, Any]]:
        """Load all curated technology stack blueprints from the blueprints directory."""
        if not os.path.exists(BLUEPRINTS_DIR):
            return []
        index_file = os.path.join(BLUEPRINTS_DIR, "index.json")
        blueprints = []
        if os.path.exists(index_file):
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    index_data = json.load(f)
                for item in index_data.get("blueprints", []):
                    bp_path = os.path.join(REPO_ROOT, item["file"])
                    if os.path.exists(bp_path):
                        with open(bp_path, "r", encoding="utf-8") as bf:
                            bp_content = json.load(bf)
                            bp_content["_tags"] = item.get("tags", [])
                            blueprints.append(bp_content)
            except Exception:
                pass
        if not blueprints:
            for fn in os.listdir(BLUEPRINTS_DIR):
                if fn.endswith(".json") and fn != "index.json":
                    p = os.path.join(BLUEPRINTS_DIR, fn)
                    try:
                        with open(p, "r", encoding="utf-8") as f:
                            blueprints.append(json.load(f))
                    except Exception:
                        pass
        return blueprints

    def list_blueprints(self) -> List[Dict[str, Any]]:
        """Return executive summaries of all curated stack blueprints."""
        bps = self.load_blueprints()
        summaries = []
        for bp in bps:
            primary_repos = []
            for t in bp.get("tiers", []):
                p = t.get("primary_component", {})
                if "repo" in p:
                    primary_repos.append(p["repo"])
            summaries.append({
                "blueprint_id": bp.get("blueprint_id", ""),
                "name": bp.get("name", ""),
                "category": bp.get("category", ""),
                "target_audience": bp.get("target_audience", ""),
                "summary": bp.get("summary", ""),
                "tier_count": len(bp.get("tiers", [])),
                "primary_repos": primary_repos,
                "workflow": bp.get("end_to_end_workflow", "")
            })
        return summaries

    def get_blueprint(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a curated stack blueprint by ID, slug, or tag,
        and enrich component repositories with live metrics from agents_registry.db.
        """
        bps = self.load_blueprints()
        clean_id = identifier.lower().strip()
        matched_bp = None
        for bp in bps:
            bp_id = bp.get("blueprint_id", "").lower()
            bp_name = bp.get("name", "").lower()
            if clean_id == bp_id or clean_id in bp_id or clean_id in bp_name:
                matched_bp = bp
                break
            if clean_id in [t.lower() for t in bp.get("_tags", [])]:
                matched_bp = bp
                break

        if not matched_bp:
            return None

        bp_copy = json.loads(json.dumps(matched_bp))
        
        # Enrich repos with live metrics
        conn = self.get_connection()
        cursor = conn.cursor()
        for tier in bp_copy.get("tiers", []):
            prim = tier.get("primary_component")
            if prim and "repo" in prim:
                cursor.execute("""
                SELECT stars, forks, language, url, workflow, category_name
                FROM repositories WHERE name = ? OR LOWER(name) = ?
                """, (prim["repo"], prim["repo"].lower()))
                row = cursor.fetchone()
                if row:
                    prim["stars"] = row["stars"]
                    prim["forks"] = row["forks"]
                    prim["url"] = row["url"]
                    prim["workflow"] = row["workflow"]
                    prim["category_name"] = row["category_name"]

            for alt in tier.get("alternative_components", []):
                if "repo" in alt:
                    cursor.execute("""
                    SELECT stars, forks, language, url, workflow, category_name
                    FROM repositories WHERE name = ? OR LOWER(name) = ?
                    """, (alt["repo"], alt["repo"].lower()))
                    row = cursor.fetchone()
                    if row:
                        alt["stars"] = row["stars"]
                        alt["forks"] = row["forks"]
                        alt["url"] = row["url"]
                        alt["workflow"] = row["workflow"]
                        alt["category_name"] = row["category_name"]

        conn.close()
        return bp_copy

    def recommend_blueprint(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Recommend the most relevant curated technology stack blueprint for a user query.
        Returns the enriched blueprint with confidence score and matching rationale.
        """
        bps = self.load_blueprints()
        q_lower = query.lower()
        q_terms = set(self.filter_query_terms(query))
        
        best_bp = None
        best_score = 0.0
        best_reasons = []

        for bp in bps:
            score = 0.0
            reasons = []
            name = bp.get("name", "").lower()
            summary = bp.get("summary", "").lower()
            category = bp.get("category", "").lower()
            tags = [t.lower() for t in bp.get("_tags", [])]

            for tag in tags:
                if tag in q_lower:
                    score += 25.0
                    reasons.append(f"tag '{tag}'")

            for term in q_terms:
                if term in name:
                    score += 15.0
                    reasons.append(f"keyword '{term}'")
                elif term in category:
                    score += 10.0
                    reasons.append(f"domain '{term}'")
                elif term in summary:
                    score += 5.0

            for tier in bp.get("tiers", []):
                prim = tier.get("primary_component", {})
                r_name = prim.get("repo", "").lower()
                r_short = r_name.split("/")[-1] if "/" in r_name else r_name
                if r_short in q_lower or r_name in q_lower:
                    score += 30.0
                    reasons.append(f"core component '{prim.get('repo')}'")

            if score > best_score:
                best_score = score
                best_bp = bp
                best_reasons = reasons

        if best_bp and best_score >= 15.0:
            enriched = self.get_blueprint(best_bp["blueprint_id"])
            confidence = min(1.0, round(best_score / 60.0, 2))
            unique_reasons = list(dict.fromkeys(best_reasons))[:4]
            reason_str = f"Matches {', '.join(unique_reasons)}" if unique_reasons else "Direct domain match"
            return {
                "blueprint": enriched,
                "confidence": confidence,
                "reason": reason_str
            }
        return None

    def recommend_stack(self, query: str, limit: int = 5, category_filter: Optional[str] = None, preferred_lang: Optional[str] = None, min_stars: int = 0) -> Dict[str, Any]:
        """
        Complete architectural recommendation combining individual ranked repositories
        with curated technology stack blueprints.
        """
        repos = self.recommend(query, limit=limit, category_filter=category_filter, preferred_lang=preferred_lang, min_stars=min_stars)
        matched_bp = self.recommend_blueprint(query)
        return {
            "query": query,
            "matched_blueprint": matched_bp,
            "recommended_repositories": repos
        }

StackRecommendationEngine = RecommendationEngine

__all__ = [
    "RecommendationEngine",
    "StackRecommendationEngine",
    "INTENT_TAXONOMY",
    "STOPWORDS",
]

if __name__ == "__main__":
    engine = RecommendationEngine()
    print("Testing Recommendation Engine with query: 'build an AI agent with tools and memory'...")
    recs = engine.recommend("build an AI agent with tools and memory", limit=3)
    for idx, rec in enumerate(recs, 1):
        print(f"\n[{idx}] {rec['repository']} | Score: {rec['score']}/100 | ⭐ {rec['stars']:,}★ | 💻 {rec['language']}")
        print(f"    📂 Category   : {rec['category']}")
        print(f"    💡 Why Matched: {rec['why_matched']}")
        print(f"    ⚡ Workflow   : {rec['workflow']}")
        print(f"    📊 Breakdown  : {rec['score_breakdown']}")
        print(f"    🔄 Alternatives: {', '.join(a['name'] for a in rec['alternatives'])}")
