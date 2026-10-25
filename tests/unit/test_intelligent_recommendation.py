import os
import sys
import unittest
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.recommendation.recommendation_engine import (
    QueryParser,
    MultiFactorScorer,
    RecommendationCardGenerator,
    RecommendationEngine,
    format_card_terminal,
    ScoreBreakdown,
    RecommendationCard,
    QueryDecomposition
)

class TestIntelligentRecommendationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = RecommendationEngine()
        cls.parser = QueryParser()
        cls.scorer = MultiFactorScorer(profile="BALANCED")

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    # --------------------------------------------------------------------------
    # 1. Natural Language Intent Parsing & Decomposition Tests
    # --------------------------------------------------------------------------
    def test_query_parser_agent_intent(self):
        query = "build an AI agent with tools and memory"
        parsed = self.parser.parse(query)
        self.assertEqual(parsed.intent_type, "ARCHITECTURAL_BLUEPRINT")
        self.assertTrue(any("agent" in t for t in parsed.extracted_technologies))
        self.assertTrue(any("tool" in t for t in parsed.extracted_technologies))
        self.assertTrue(any("memory" in t for t in parsed.extracted_technologies))
        self.assertIn(3, parsed.target_categories, "Category 03 (Multi-Agent Systems) should be targeted")

    def test_query_parser_local_first_database(self):
        query = "best database for local-first"
        parsed = self.parser.parse(query)
        self.assertEqual(parsed.intent_type, "COMPONENT_SELECTION")
        self.assertTrue(any("database" in t for t in parsed.extracted_technologies))
        self.assertTrue(any("local-first" in t for t in parsed.extracted_technologies))
        self.assertEqual(parsed.deployment_constraint, "local-first")
        self.assertIn(37, parsed.target_categories, "Category 37 (Database Engines) should be targeted")

    def test_query_parser_react_cicd_deployment(self):
        query = "deploy React with CI/CD"
        parsed = self.parser.parse(query)
        self.assertEqual(parsed.intent_type, "DEVOPS_DEPLOYMENT")
        self.assertTrue(any("react" in t for t in parsed.extracted_technologies))
        self.assertTrue(any("ci" in t for t in parsed.extracted_technologies))
        self.assertIn(40, parsed.target_categories, "Category 40 (CI/CD Automation) should be targeted")

    def test_query_parser_explicit_constraints(self):
        query = "high performance web server lang:rust license:permissive min_stars:5000 deploy:edge-wasm"
        parsed = self.parser.parse(query)
        self.assertEqual(parsed.language_constraint, "Rust")
        self.assertEqual(parsed.license_constraint, "PERMISSIVE")
        self.assertEqual(parsed.min_stars_constraint, 5000)
        self.assertEqual(parsed.deployment_constraint, "edge-wasm")

    # --------------------------------------------------------------------------
    # 2. Multi-Factor Scoring Engine Tests
    # --------------------------------------------------------------------------
    def test_scorer_language_affinity(self):
        cand_ts = {"language": "TypeScript", "stars": 10000, "forks": 1000, "description": "", "name": "test/ts", "workflow": "", "category_name": ""}
        cand_py = {"language": "Python", "stars": 10000, "forks": 1000, "description": "", "name": "test/py", "workflow": "", "category_name": ""}

        q_ts = self.parser.parse("react state management in typescript")
        score_exact = self.scorer._compute_language_fit(cand_ts, q_ts)
        score_conflict = self.scorer._compute_language_fit(cand_py, q_ts)

        self.assertEqual(score_exact, 1.0, "Exact language match should receive 1.0")
        self.assertLess(score_conflict, 0.30, "Conflicting language should receive penalty")

    def test_scorer_license_tiers(self):
        q_perm = self.parser.parse("vector database license:permissive")
        cand_mit = {"name": "test/mit", "description": "Fast vector search with MIT license"}
        cand_agpl = {"name": "test/agpl", "description": "Vector database under AGPLv3 license"}

        score_mit, _ = self.scorer._compute_license_fit(cand_mit, q_perm)
        score_agpl, _ = self.scorer._compute_license_fit(cand_agpl, q_perm)

        self.assertEqual(score_mit, 1.0, "Permissive license should score 1.0")
        self.assertLess(score_agpl, 0.20, "Copyleft license with permissive constraint should score <= 0.20")

    def test_scorer_deployment_constraint(self):
        q_local = self.parser.parse("best database for local-first")
        cand_local = {
            "name": "pubkey/rxdb",
            "description": "The local-first database that runs on every JS runtime with offline sync",
            "workflow": "Client storage -> offline sync -> CRDT merge",
            "category_name": "Database Engines"
        }
        cand_cloud = {
            "name": "cloud/k8s-db",
            "description": "Distributed cloud-only database cluster managed service",
            "workflow": "Cloud cluster -> multi-node consensus",
            "category_name": "Database Engines"
        }

        score_local = self.scorer._compute_deployment_fit(cand_local, q_local)
        score_cloud = self.scorer._compute_deployment_fit(cand_cloud, q_local)

        self.assertGreater(score_local, 0.80, "Local-first candidate should score high on local-first constraint")
        self.assertLess(score_cloud, score_local, "Cloud-only candidate should score lower on local-first constraint")

    def test_anti_slop_penalty_for_curated_lists(self):
        q = self.parser.parse("build an AI agent with tools and memory")
        cand_list = {"category_id": 1, "name": "awesome/agent-list", "stars": 100000}
        cand_engine = {"category_id": 3, "name": "framework/agent-core", "stars": 100000}

        pen_list = self.scorer._compute_penalties(cand_list, q)
        pen_engine = self.scorer._compute_penalties(cand_engine, q)

        self.assertGreater(pen_list, 0.30, "Curated list category should receive anti-slop penalty for actionable build queries")
        self.assertEqual(pen_engine, 0.0, "Dedicated framework category should receive 0 penalty")

    # --------------------------------------------------------------------------
    # 3. End-to-End Recommendation Engine Tests
    # --------------------------------------------------------------------------
    def test_recommend_agent_query(self):
        decomp, recs = self.engine.recommend("build an AI agent with tools and memory", limit=3)
        self.assertGreaterEqual(len(recs), 1)
        for r in recs:
            self.assertIsInstance(r, RecommendationCard)
            self.assertGreater(r.score.composite_score, 70.0)
            self.assertTrue(len(r.strengths) >= 2)
            self.assertTrue(len(r.limitations) >= 1)
            self.assertTrue(len(r.why_it_matches) > 20)
            self.assertIn("install_command", r.next_steps)
            self.assertIn("code_snippet", r.next_steps)

    def test_recommend_local_first_db(self):
        decomp, recs = self.engine.recommend("best database for local-first", limit=3)
        self.assertGreaterEqual(len(recs), 1)
        top = recs[0]
        # Verify top recommendation is a database engine
        self.assertIn(top.category_id, [37, 49, 38])
        self.assertGreater(top.score.deployment_fit, 0.65)

    def test_recommend_react_cicd(self):
        decomp, recs = self.engine.recommend("deploy React with CI/CD", limit=3)
        self.assertGreaterEqual(len(recs), 1)
        top = recs[0]
        # Should be in CI/CD, Frontend, or Cloud-Native
        self.assertIn(top.category_id, [40, 49, 39])
        self.assertGreater(top.score.composite_score, 75.0)

    # --------------------------------------------------------------------------
    # 4. Formatter & Output Serialization Tests
    # --------------------------------------------------------------------------
    def test_card_terminal_rendering(self):
        _, recs = self.engine.recommend("build an AI agent with tools and memory", limit=1)
        self.assertGreater(len(recs), 0)
        card_text = format_card_terminal(recs[0], rank=1)
        self.assertIn("RECOMMENDATION #1", card_text)
        self.assertIn("WHY IT MATCHES", card_text)
        self.assertIn("KEY STRENGTHS", card_text)
        self.assertIn("LIMITATIONS & TRADEOFFS", card_text)
        self.assertIn("ACTIONABLE NEXT STEPS", card_text)

if __name__ == "__main__":
    unittest.main()
