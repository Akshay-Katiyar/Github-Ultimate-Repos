"""
Unit tests for the Transparent Ranking System (scripts.ranking.ranking_engine).
Validates all 9 scoring signals, penalty policies, elimination gates, weighting profiles,
deterministic tie-breaking, and explainability audit breakdowns.
"""

import math
import pytest
from scripts.ranking.ranking_engine import (
    TransparentRankingEngine,
    RepositoryMetadata,
    TaskRequirement,
    QualityGate,
    LicenseCategory,
    WeightProfile,
    WEIGHT_PROFILES,
    rank_repositories,
)


@pytest.fixture
def engine():
    return TransparentRankingEngine(default_profile="ENTERPRISE_PRODUCTION")


@pytest.fixture
def base_repo():
    return RepositoryMetadata(
        name="test-org/high-perf-engine",
        url="https://github.com/test-org/high-perf-engine",
        stars=15000,
        forks=2500,
        language="Python",
        category_id=2,
        category_name="Artificial Intelligence, LLMs, Foundation Models & Quantization",
        description="High-performance inference engine with streaming tokens and CUDA acceleration",
        architecture_workflow="Token Stream -> Continuous Batching -> Kernel Acceleration -> Logits",
        quality_gate=QualityGate.CERTIFIED,
        license="Apache-2.0",
        license_category=LicenseCategory.PERMISSIVE,
        days_since_last_commit=5,
        open_issues=12,
        closed_issues=180,
        has_security_policy=True,
        cve_critical_count=0,
        cve_medium_count=0,
        is_archived=False,
        supported_os=["windows", "linux", "darwin"],
        has_quickstart=True,
        has_examples=True,
        readme_length_chars=4500,
        dependency_count=3,
        has_package_manager_dist=True,
        requires_specialized_hardware=False,
    )


# -----------------------------------------------------------------------------
# 1. Individual Scoring Signals Validation
# -----------------------------------------------------------------------------

def test_task_relevance_signal(engine, base_repo):
    # Perfect match query
    task_match = TaskRequirement(query="high-performance inference engine")
    score_match, desc = engine.compute_task_relevance(base_repo, task_match)
    assert 0.0 <= score_match <= 1.0
    assert score_match > 0.60
    assert "overlap" in desc.lower()

    # Irrelevant query
    task_irrelevant = TaskRequirement(query="underwater acoustic submarine navigation")
    score_irrel, _ = engine.compute_task_relevance(base_repo, task_irrelevant)
    assert score_irrel < score_match


def test_feature_fit_signal(engine, base_repo):
    # Required features matching repo surface
    task_req = TaskRequirement(
        query="inference",
        required_features=["streaming", "batching"],
        optional_features=["cuda", "quantization"],
    )
    score, desc = engine.compute_feature_fit(base_repo, task_req)
    assert 0.80 <= score <= 1.0
    assert "Matched 2/2 required" in desc

    # Missing features
    task_missing = TaskRequirement(
        query="inference",
        required_features=["blockchain", "solidity"],
    )
    score_missing, desc_missing = engine.compute_feature_fit(base_repo, task_missing)
    assert score_missing == 0.0
    assert "Matched 0/2 required" in desc_missing


def test_maintenance_evidence_decay(engine, base_repo):
    task = TaskRequirement(query="inference")

    # Fresh repository (5 days)
    base_repo.days_since_last_commit = 5
    score_fresh, _ = engine.compute_maintenance_evidence(base_repo, task)

    # 180 days old (one half-life)
    base_repo.days_since_last_commit = 180
    score_half_life, _ = engine.compute_maintenance_evidence(base_repo, task)

    # 800 days old (severely stale)
    base_repo.days_since_last_commit = 800
    score_stale, _ = engine.compute_maintenance_evidence(base_repo, task)

    assert 0.0 <= score_stale < score_half_life < score_fresh <= 1.0
    assert score_fresh > 0.85
    assert score_stale < 0.40


def test_documentation_clarity_signal(engine, base_repo):
    task = TaskRequirement(query="inference")

    # Full documentation
    score_full, _ = engine.compute_documentation_clarity(base_repo, task)
    assert score_full >= 0.90

    # Degraded documentation
    base_repo.architecture_workflow = ""
    base_repo.has_quickstart = False
    base_repo.has_examples = False
    base_repo.readme_length_chars = 150
    score_degraded, _ = engine.compute_documentation_clarity(base_repo, task)

    assert score_degraded < 0.30


def test_compatibility_signal(engine, base_repo):
    # Matching Windows target
    task_win = TaskRequirement(query="inference", target_os="windows", target_language="Python")
    score_win, _ = engine.compute_compatibility(base_repo, task_win)
    assert score_win > 0.85

    # Target language mismatch
    task_rust = TaskRequirement(query="inference", target_os="windows", target_language="Rust")
    score_rust, _ = engine.compute_compatibility(base_repo, task_rust)
    assert score_rust < score_win


def test_security_signals(engine, base_repo):
    task = TaskRequirement(query="inference")

    # Clean certified repo
    base_repo.quality_gate = QualityGate.CERTIFIED
    base_repo.cve_critical_count = 0
    score_clean, _ = engine.compute_security_signals(base_repo, task)
    assert score_clean >= 0.95

    # Vulnerable repo with open CVEs
    base_repo.cve_critical_count = 2
    base_repo.cve_medium_count = 3
    base_repo.quality_gate = QualityGate.PASSED
    score_cve, _ = engine.compute_security_signals(base_repo, task)
    assert score_cve < 0.35


def test_license_fit_policies(engine, base_repo):
    # Strict Permissive Policy
    task_strict = TaskRequirement(query="test", required_license_policy="PERMISSIVE_ONLY")
    base_repo.license_category = LicenseCategory.PERMISSIVE
    score_perm, _ = engine.compute_license_fit(base_repo, task_strict)
    assert score_perm == 1.0

    base_repo.license_category = LicenseCategory.STRONG_COPYLEFT
    score_gpl, _ = engine.compute_license_fit(base_repo, task_strict)
    assert score_gpl <= 0.10

    # Open Source permissive of GPL
    task_open = TaskRequirement(query="test", required_license_policy="ANY_OPEN_SOURCE")
    score_open_gpl, _ = engine.compute_license_fit(base_repo, task_open)
    assert score_open_gpl == 1.0


def test_maturity_logarithmic_damping(engine, base_repo):
    task = TaskRequirement(query="test")

    # 1,000 stars vs 100,000 stars
    base_repo.stars = 1000
    base_repo.forks = 200
    score_1k, _ = engine.compute_maturity(base_repo, task)

    base_repo.stars = 100000
    base_repo.forks = 20000
    score_100k, _ = engine.compute_maturity(base_repo, task)

    assert 0.0 <= score_1k <= 1.0
    assert 0.0 <= score_100k <= 1.0
    assert score_100k > score_1k
    # 100x stars must NOT result in a 100x score due to logarithmic scaling
    assert score_100k < 3.0 * score_1k


def test_deployment_fit(engine, base_repo):
    task_cpu = TaskRequirement(query="test", hardware_constraint="CPU_ONLY")
    base_repo.requires_specialized_hardware = False
    score_cpu_ok, _ = engine.compute_deployment_fit(base_repo, task_cpu)
    assert score_cpu_ok == 1.0

    # Repo requiring multi-GPU on CPU constraint
    base_repo.requires_specialized_hardware = True
    score_gpu_req, _ = engine.compute_deployment_fit(base_repo, task_cpu)
    assert score_gpu_req < 0.60


# -----------------------------------------------------------------------------
# 2. Penalty Policies & Elimination Gates
# -----------------------------------------------------------------------------

def test_hard_elimination_critical_cve(engine, base_repo):
    task = TaskRequirement(query="test", max_acceptable_critical_cve=0)
    base_repo.cve_critical_count = 1

    explanation = engine.score_repository(base_repo, task)
    assert explanation.is_disqualified is True
    assert explanation.final_score == 0.0
    assert "Critical CVE" in explanation.disqualification_reason


def test_hard_elimination_archived_repo(engine, base_repo):
    task = TaskRequirement(query="test", disallow_archived=True)
    base_repo.is_archived = True

    explanation = engine.score_repository(base_repo, task)
    assert explanation.is_disqualified is True
    assert explanation.final_score == 0.0
    assert "archived" in explanation.disqualification_reason.lower()


def test_hard_elimination_license_incompatibility(engine, base_repo):
    task = TaskRequirement(query="test", required_license_policy="PERMISSIVE_ONLY")
    base_repo.license = "AGPL-3.0"
    base_repo.license_category = LicenseCategory.NETWORK_COPYLEFT

    explanation = engine.score_repository(base_repo, task)
    assert explanation.is_disqualified is True
    assert explanation.final_score == 0.0
    assert "strictly disallowed" in explanation.disqualification_reason


def test_hard_elimination_os_mismatch(engine, base_repo):
    task = TaskRequirement(query="test", target_os="windows")
    base_repo.supported_os = ["linux"]

    explanation = engine.score_repository(base_repo, task)
    assert explanation.is_disqualified is True
    assert explanation.final_score == 0.0
    assert "Target OS 'windows' not supported" in explanation.disqualification_reason


def test_soft_multiplicative_penalties(engine, base_repo):
    task = TaskRequirement(query="test")

    # Stale maintenance + missing workflow
    base_repo.days_since_last_commit = 400
    base_repo.architecture_workflow = ""

    explanation = engine.score_repository(base_repo, task)
    assert explanation.is_disqualified is False
    assert explanation.penalty_multiplier < 0.70
    assert any(p["type"] == "STALE_MAINTENANCE_MODERATE" for p in explanation.applied_penalties)
    assert any(p["type"] == "MISSING_WORKFLOW" for p in explanation.applied_penalties)


def test_subtractive_penalties(engine, base_repo):
    task = TaskRequirement(query="test")

    # Massive issue backlog skew
    base_repo.open_issues = 500
    base_repo.closed_issues = 20
    base_repo.cve_medium_count = 2

    explanation = engine.score_repository(base_repo, task)
    assert explanation.subtractive_penalty > 0.10
    assert any(p["type"] == "ISSUE_BACKLOG_SKEW" for p in explanation.applied_penalties)
    assert any(p["type"] == "MEDIUM_SECURITY_EXPOSURE" for p in explanation.applied_penalties)


# -----------------------------------------------------------------------------
# 3. Weighting Profiles & Consistency
# -----------------------------------------------------------------------------

def test_weight_profiles_sum_to_one():
    for name, profile in WEIGHT_PROFILES.items():
        profile.validate()
        total = (
            profile.w_task
            + profile.w_feature
            + profile.w_maint
            + profile.w_docs
            + profile.w_compat
            + profile.w_sec
            + profile.w_license
            + profile.w_mat
            + profile.w_deploy
        )
        assert math.isclose(total, 1.0, rel_tol=1e-3), f"Profile {name} sum was {total}"


def test_profile_differentiation(engine, base_repo):
    task = TaskRequirement(
        query="high-performance inference engine",
        required_features=["streaming", "batching"],
    )

    # Base repo with weak security and high relevance
    base_repo.quality_gate = QualityGate.UNKNOWN
    base_repo.has_security_policy = False
    base_repo.cve_medium_count = 3

    exp_prod = engine.score_repository(base_repo, task, profile_name="ENTERPRISE_PRODUCTION")
    exp_proto = engine.score_repository(base_repo, task, profile_name="FAST_PROTOTYPING")
    exp_sec = engine.score_repository(base_repo, task, profile_name="SAFETY_CRITICAL")

    # Fast prototyping weighs security much less (0.05) and relevance/features higher (0.47),
    # so it must yield a substantially higher score than safety critical (sec=0.20).
    assert exp_proto.final_score > exp_sec.final_score


# -----------------------------------------------------------------------------
# 4. Strict 5-Tier Deterministic Tie-Breaking
# -----------------------------------------------------------------------------

def test_deterministic_tie_breaking(engine):
    task = TaskRequirement(query="framework")

    # Create two candidates with virtually identical scores
    repo_a = RepositoryMetadata(
        name="alpha-org/framework",
        url="https://github.com/alpha-org/framework",
        stars=10000,
        quality_gate=QualityGate.CERTIFIED,
        days_since_last_commit=10,
        architecture_workflow="A -> B -> C",
        description="framework",
    )
    repo_b = RepositoryMetadata(
        name="beta-org/framework",
        url="https://github.com/beta-org/framework",
        stars=10000,
        quality_gate=QualityGate.VERIFIED,  # Lower gate
        days_since_last_commit=10,
        architecture_workflow="A -> B -> C",
        description="framework",
    )

    ranked = engine.rank([repo_b, repo_a], task)
    # repo_a must win because of CERTIFIED quality gate
    assert ranked[0].repository == "alpha-org/framework"
    assert ranked[0].rank == 1
    assert ranked[1].repository == "beta-org/framework"
    assert ranked[1].rank == 2


def test_alphabetical_final_tie_break(engine):
    task = TaskRequirement(query="tool")

    # Identical in all 4 preceding tiers
    repo_z = RepositoryMetadata(name="zeta/tool", url="https://github.com/zeta/tool", stars=5000, description="tool")
    repo_a = RepositoryMetadata(name="alpha/tool", url="https://github.com/alpha/tool", stars=5000, description="tool")

    # Submit in reverse order (zeta first)
    ranked = engine.rank([repo_z, repo_a], task)
    # Deterministic alphabetical ordering: alpha/tool must be #1, zeta/tool #2
    assert ranked[0].repository == "alpha/tool"
    assert ranked[0].rank == 1
    assert ranked[1].repository == "zeta/tool"
    assert ranked[1].rank == 2


# -----------------------------------------------------------------------------
# 5. Explainability Breakdown & Audit Trails
# -----------------------------------------------------------------------------

def test_explainability_audit_trail(engine, base_repo):
    task = TaskRequirement(query="inference", required_features=["streaming"])
    exp = engine.score_repository(base_repo, task)

    # 9 signals must all be populated
    assert len(exp.signals) == 9
    for name, s in exp.signals.items():
        assert 0.0 <= s.raw_value <= 1.0
        assert s.weight > 0.0
        assert math.isclose(s.weighted_contribution, s.raw_value * s.weight, abs_tol=1e-3)

    # Narrative generation
    assert exp.audit_narrative != ""
    assert "profile" in exp.audit_narrative.lower()

    # Markdown output
    md = exp.to_markdown_summary()
    assert "### #0 `test-org/high-perf-engine`" in md
    assert "| **Task Relevance** |" in md

    # Dictionary serializability for JSON logging
    data = exp.to_dict()
    assert isinstance(data, dict)
    assert data["final_score"] == exp.final_score
    assert "score_100" in data
    assert data["score_100"] == exp.score_100


# -----------------------------------------------------------------------------
# 6. Transparent Profiles (BALANCED, STABILITY_FIRST, INNOVATION_FIRST, LIGHTWEIGHT)
# -----------------------------------------------------------------------------

def test_transparent_profiles_catalog():
    """Verify all 8 standard & transparent scoring profiles exist, validate, and sum to 1.0."""
    required_profiles = [
        "BALANCED",
        "STABILITY_FIRST",
        "INNOVATION_FIRST",
        "LIGHTWEIGHT",
        "ENTERPRISE_PRODUCTION",
        "FAST_PROTOTYPING",
        "AUTONOMOUS_SWARM_AGENT",
        "SAFETY_CRITICAL",
    ]
    for p_name in required_profiles:
        assert p_name in WEIGHT_PROFILES, f"Missing required profile: {p_name}"
        profile = WEIGHT_PROFILES[p_name]
        profile.validate()
        total_weight = (
            profile.w_task
            + profile.w_feature
            + profile.w_maint
            + profile.w_docs
            + profile.w_compat
            + profile.w_sec
            + profile.w_license
            + profile.w_mat
            + profile.w_deploy
        )
        assert math.isclose(total_weight, 1.0, rel_tol=1e-3), f"{p_name} weight sum {total_weight} != 1.0"

    # Case-insensitive profile loading
    engine_lower = TransparentRankingEngine(default_profile="balanced")
    assert engine_lower.default_profile == "BALANCED"


def test_score_breakdowns_and_100_bounds(engine, base_repo):
    """Verify that all scores and signal breakdowns adhere strictly to [0, 100] bounds."""
    task = TaskRequirement(query="inference engine", required_features=["streaming"])
    exp = engine.score_repository(base_repo, task, profile_name="BALANCED")

    # Bounded in [0.0, 1.0] and [0.0, 100.0]
    assert 0.0 <= exp.final_score <= 1.0
    assert 0.0 <= exp.score_100 <= 100.0
    assert math.isclose(exp.score_100, round(exp.final_score * 100.0, 2), abs_tol=0.01)

    assert 0.0 <= exp.base_score <= 1.0
    assert 0.0 <= exp.base_score_100 <= 100.0
    assert math.isclose(exp.base_score_100, round(exp.base_score * 100.0, 2), abs_tol=0.01)

    # Every signal breakdown must have bounded score_100 and weighted_contribution_100
    for name, s in exp.signals.items():
        assert 0.0 <= s.raw_value <= 1.0, f"Signal {name} raw_value {s.raw_value} out of bounds"
        assert 0.0 <= s.score_100 <= 100.0, f"Signal {name} score_100 {s.score_100} out of bounds"
        assert 0.0 <= s.weighted_contribution_100 <= 100.0, f"Signal {name} contrib {s.weighted_contribution_100} out of bounds"
        assert math.isclose(s.score_100, round(s.raw_value * 100.0, 2), abs_tol=0.01)
        assert math.isclose(s.weighted_contribution_100, round(s.weighted_contribution * 100.0, 2), abs_tol=0.01)

    # Markdown representation checks
    md = exp.to_markdown_summary()
    assert "/100)" in md
    assert "Score (0-100)" in md
    assert "Contribution (0-100)" in md


def test_deterministic_reproducibility_100_runs(engine):
    """Verify that ranking is 100% deterministic across 100 repeated executions."""
    task = TaskRequirement(query="machine learning compiler", target_os="windows")

    repos = [
        RepositoryMetadata(name="repo-c", url="https://github.com/c/c", stars=5000, description="compiler"),
        RepositoryMetadata(name="repo-a", url="https://github.com/a/a", stars=5000, description="compiler"),
        RepositoryMetadata(name="repo-b", url="https://github.com/b/b", stars=12000, description="machine learning compiler"),
        RepositoryMetadata(name="repo-d", url="https://github.com/d/d", stars=100, description="compiler"),
    ]

    baseline_ranked = engine.rank(repos, task, profile_name="BALANCED")
    baseline_names = [r.repository for r in baseline_ranked]
    baseline_scores = [r.final_score for r in baseline_ranked]
    baseline_narratives = [r.audit_narrative for r in baseline_ranked]

    for iteration in range(100):
        current_ranked = engine.rank(repos, task, profile_name="BALANCED")
        current_names = [r.repository for r in current_ranked]
        current_scores = [r.final_score for r in current_ranked]
        current_narratives = [r.audit_narrative for r in current_ranked]

        assert current_names == baseline_names, f"Ordinal mismatch at iteration {iteration}"
        assert current_scores == baseline_scores, f"Score mismatch at iteration {iteration}"
        assert current_narratives == baseline_narratives, f"Narrative mismatch at iteration {iteration}"


def test_explainable_narrative_and_penalties(engine, base_repo):
    """Verify that narrative explanation clearly explains drivers, penalties, and disqualifications."""
    task = TaskRequirement(query="inference", required_features=["streaming"])

    # Normal execution narrative
    exp_normal = engine.score_repository(base_repo, task, profile_name="BALANCED")
    assert "Strongest driver was" in exp_normal.audit_narrative
    assert f"({exp_normal.score_100:.1f}/100)" in exp_normal.audit_narrative

    # Penalized execution narrative
    base_repo.days_since_last_commit = 450
    base_repo.cve_medium_count = 1
    exp_penalized = engine.score_repository(base_repo, task, profile_name="BALANCED")
    assert "Soft penalties reduced score" in exp_penalized.audit_narrative
    assert "Subtractive penalties deducted" in exp_penalized.audit_narrative

    # Disqualified execution narrative
    base_repo.cve_critical_count = 1
    exp_disq = engine.score_repository(base_repo, task, profile_name="BALANCED")
    assert exp_disq.is_disqualified is True
    assert "Disqualified:" in exp_disq.audit_narrative


def test_profile_behavior_stability_vs_innovation_vs_lightweight(engine):
    """Verify distinct profile behaviors reflecting operational tradeoffs."""
    task = TaskRequirement(
        query="data processing framework",
        required_features=["distributed"],
        target_os="windows",
    )

    # Repo A: Bleeding-edge, high features, but high dependencies and medium security issues
    bleeding_edge = RepositoryMetadata(
        name="bleeding/edge-tool",
        url="https://github.com/bleeding/edge-tool",
        stars=8000,
        description="distributed data processing framework with new features",
        architecture_workflow="A -> B -> C",
        dependency_count=45,
        cve_medium_count=2,
        quality_gate=QualityGate.PASSED,
        days_since_last_commit=2,
    )

    # Repo B: Lean, zero-dep, rock solid, certified quality gate
    lean_stable = RepositoryMetadata(
        name="lean/rock-solid",
        url="https://github.com/lean/rock-solid",
        stars=6000,
        description="distributed data processing framework",
        architecture_workflow="A -> B -> C",
        dependency_count=0,
        cve_medium_count=0,
        quality_gate=QualityGate.CERTIFIED,
        days_since_last_commit=15,
    )

    # Under INNOVATION_FIRST, bleeding-edge scores higher or competitively
    exp_inno_edge = engine.score_repository(bleeding_edge, task, profile_name="INNOVATION_FIRST")
    exp_stab_edge = engine.score_repository(bleeding_edge, task, profile_name="STABILITY_FIRST")

    # Innovation first values bleeding edge higher than Stability first does
    assert exp_inno_edge.final_score > exp_stab_edge.final_score

    # Under LIGHTWEIGHT, lean_stable gets maximum compatibility and dependency footprint score
    exp_light_lean = engine.score_repository(lean_stable, task, profile_name="LIGHTWEIGHT")
    exp_light_edge = engine.score_repository(bleeding_edge, task, profile_name="LIGHTWEIGHT")
    assert exp_light_lean.final_score > exp_light_edge.final_score

