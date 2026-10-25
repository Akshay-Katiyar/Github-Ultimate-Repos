import sys
import os

sys.path.insert(0, "C:/Users/Aryan/Github-Ultimate-Repos")
from scripts.engine.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
bps = engine.list_blueprints()
print(f"Loaded {len(bps)} blueprints:")
for b in bps:
    print(f"  [{b['blueprint_id']}] {b['name']} ({b['tier_count']} tiers) -> {b['primary_repos']}")

print("\nTesting get_blueprint('BP-AI-AGENT-01'):")
ai_bp = engine.get_blueprint("BP-AI-AGENT-01")
for t in ai_bp["tiers"]:
    p = t["primary_component"]
    print(f"  Tier: {t['tier_id']} | Repo: {p['repo']} | Stars: {p.get('stars', 0):,}★ | URL: {p.get('url', '')}")

print("\nTesting recommend_blueprint queries:")
test_queries = [
    "build a production autonomous AI agent swarm with LangGraph and Qdrant",
    "create a startup fullstack SaaS MVP with Next.js and Supabase",
    "offline local-first edge AI with llama.cpp and tauri",
    "enterprise data engineering lakehouse pipeline with kafka and iceberg",
    "cybersecurity penetration testing and vulnerability scanning lab"
]
for q in test_queries:
    rec = engine.recommend_blueprint(q)
    if rec:
        print(f"  Query: '{q}'")
        print(f"    -> Matched: [{rec['blueprint']['blueprint_id']}] {rec['blueprint']['name']} (Confidence: {rec['confidence']})")
        print(f"    -> Reason: {rec['reason']}")
    else:
        print(f"  Query: '{q}' -> NO MATCH")
