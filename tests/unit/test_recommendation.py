import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.engine.recommendation_engine import RecommendationEngine

class TestRecommendationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = RecommendationEngine()

    def test_intent_detection(self):
        intents = self.engine.detect_intents("build an autonomous AI agent with tools")
        self.assertIn("agent", intents)

    def test_recommendation_scoring_bounds(self):
        recs = self.engine.recommend("fastapi kubernetes deployment", limit=3)
        self.assertGreater(len(recs), 0)
        for r in recs:
            self.assertGreaterEqual(r["score"], 0)
            self.assertLessEqual(r["score"], 100)
            self.assertIn("score_breakdown", r)
            self.assertIn("why_matched", r)
            self.assertIn("workflow", r)

    def test_compare_repositories(self):
        comparison = self.engine.compare(["Significant-Gravitas/AutoGPT", "langchain-ai/langchain"])
        self.assertEqual(len(comparison), 2)
        self.assertEqual(comparison[0]["name"], "Significant-Gravitas/AutoGPT")
        self.assertEqual(comparison[1]["name"], "langchain-ai/langchain")

if __name__ == "__main__":
    unittest.main()
