import os
import sys
import json
import unittest
import jsonschema

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.comparison.tradeoff_engine import (
    TradeoffEngine,
    compare_repositories,
    render_terminal,
    render_markdown
)

class TestTradeoffEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TradeoffEngine()
        self.schema_path = os.path.join(REPO_ROOT, "schemas", "comparison_schema.json")
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_compare_two_repositories(self):
        result = self.engine.compare(["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI"])
        self.assertEqual(result.repository_count, 2)
        self.assertEqual(len(result.repositories), 2)

        repo1, repo2 = result.repositories
        self.assertIn("AutoGPT", repo1.name)
        self.assertIn("crewAI", repo2.name)

        # Check the 6 required evaluation dimensions
        for r in [repo1, repo2]:
            # 1. Primary use case fit
            self.assertTrue(len(r.primary_use_case_fit.summary) > 10)
            self.assertTrue(len(r.primary_use_case_fit.sweet_spot) >= 1)
            self.assertTrue(len(r.primary_use_case_fit.anti_patterns) >= 1)

            # 2. Architectural approach
            self.assertTrue(len(r.architectural_approach.paradigm) > 5)
            self.assertTrue(len(r.architectural_approach.execution_model) > 5)
            self.assertTrue(len(r.architectural_approach.state_management) > 5)
            self.assertTrue(len(r.architectural_approach.tool_routing) > 5)

            # 3. Strengths and key advantages
            self.assertTrue(len(r.strengths_and_advantages) >= 2)

            # 4. Known limitations and bottlenecks
            self.assertTrue(len(r.limitations_and_bottlenecks) >= 2)

            # 5. Ideal developer persona
            self.assertTrue(len(r.ideal_developer_persona.title) > 5)
            self.assertTrue(len(r.ideal_developer_persona.profile) > 10)
            self.assertIn(r.ideal_developer_persona.cognitive_overhead, ["Low", "Moderate", "High", "Very High"])

            # 6. Licensing and deployment model
            self.assertTrue(len(r.licensing_and_deployment.license) > 2)
            self.assertTrue(len(r.licensing_and_deployment.commercial_use) > 5)
            self.assertTrue(len(r.licensing_and_deployment.deployment_models) >= 1)
            self.assertTrue(len(r.licensing_and_deployment.operational_footprint) > 5)

            # Scores
            self.assertGreaterEqual(r.scores.composite_score, 0)
            self.assertLessEqual(r.scores.composite_score, 100)

        # Trade-off analysis
        self.assertIn(repo1.name, result.decision_guide)
        self.assertIn(repo2.name, result.decision_guide)
        self.assertTrue(len(result.scenario_recommendations) >= 2)
        self.assertTrue(len(result.comparative_summary) > 20)

    def test_compare_three_repositories(self):
        targets = ["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI", "langchain-ai/langchain"]
        result = self.engine.compare(targets)
        self.assertEqual(result.repository_count, 3)
        self.assertEqual(len(result.repositories), 3)

        names = [r.name for r in result.repositories]
        self.assertTrue(any("AutoGPT" in n for n in names))
        self.assertTrue(any("crewAI" in n for n in names))
        self.assertTrue(any("langchain" in n for n in names))

    def test_invalid_repository_counts(self):
        with self.assertRaises(ValueError):
            self.engine.compare(["Significant-Gravitas/AutoGPT"])

        with self.assertRaises(ValueError):
            self.engine.compare([
                "Significant-Gravitas/AutoGPT",
                "crewAIInc/crewAI",
                "langchain-ai/langchain",
                "run-llama/llama_index"
            ])

    def test_heuristic_fallback_for_arbitrary_repos(self):
        result = self.engine.compare(["tiangolo/fastapi", "pallets/flask"])
        self.assertEqual(result.repository_count, 2)
        for r in result.repositories:
            self.assertTrue(len(r.primary_use_case_fit.summary) > 0)
            self.assertTrue(len(r.architectural_approach.paradigm) > 0)
            self.assertTrue(len(r.strengths_and_advantages) >= 1)
            self.assertTrue(len(r.limitations_and_bottlenecks) >= 1)
            self.assertGreater(r.scores.composite_score, 0)

    def test_schema_conformance(self):
        result = self.engine.compare(["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI", "langchain-ai/langchain"])
        data = result.to_dict()
        # Validate against comparison_schema.json
        jsonschema.validate(instance=data, schema=self.schema)

    def test_renderers(self):
        result = self.engine.compare(["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI"])
        term_output = render_terminal(result)
        self.assertIn("REPOSITORY COMPARISON & ARCHITECTURAL TRADE-OFF MATRIX", term_output)
        self.assertIn("BENCHMARK SCORECARD", term_output)
        self.assertIn("STRATEGIC DECISION GUIDE", term_output)

        md_output = render_markdown(result)
        self.assertIn("# Repository Comparison & Architectural Trade-off Dossier", md_output)
        self.assertIn("## 1. Quantitative Benchmark Scorecard", md_output)
        self.assertIn("## 4. Strategic Decision Guide", md_output)

if __name__ == "__main__":
    unittest.main()
