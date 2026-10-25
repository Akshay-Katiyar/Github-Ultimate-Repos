#!/usr/bin/env python3
"""
ranking_engine.py - Transparent, Deterministic Ranking Engine for Github-Ultimate-Repos

Implements the multi-agent transparent ranking architecture with:
1. Nine interpretable, normalized scoring signals ([0.0, 1.0]).
2. Multi-tier penalty policies (hard elimination gates, soft multiplicative & subtractive penalties).
3. Configurable weighting profiles (Enterprise Production, Fast Prototyping, Autonomous Swarm Agent, Safety-Critical).
4. Granular, auditable explainability breakdowns with additive & subtractive step tracing.
5. Strict, deterministic 5-tier tie-breaking criteria.
"""

from __future__ import annotations
import math
import re
import os
import sys
import json
import sqlite3
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Standard EPSILON for floating point tie-breaking
EPSILON = 1e-6


class QualityGate(str, Enum):
    CERTIFIED = "CERTIFIED"
    VERIFIED = "VERIFIED"
    PASSED = "PASSED"
    UNKNOWN = "UNKNOWN"

    @property
    def rank_weight(self) -> int:
        mapping = {
            QualityGate.CERTIFIED: 3,
            QualityGate.VERIFIED: 2,
            QualityGate.PASSED: 1,
            QualityGate.UNKNOWN: 0,
        }
        return mapping.get(self, 0)


class LicenseCategory(str, Enum):
    PERMISSIVE = "PERMISSIVE"         # MIT, Apache-2.0, BSD-2/3, ISC, Unlicense
    WEAK_COPYLEFT = "WEAK_COPYLEFT"   # MPL-2.0, LGPL-2.1/3.0
    STRONG_COPYLEFT = "STRONG_COPYLEFT" # GPL-2.0/3.0
    NETWORK_COPYLEFT = "NETWORK_COPYLEFT" # AGPL-3.0, SSPL
    PROPRIETARY = "PROPRIETARY"       # Commercial, All Rights Reserved
    UNKNOWN = "UNKNOWN"               # Missing or unrecognized license


@dataclass
class RepositoryMetadata:
    """Canonical representation of an audited repository asset."""
    name: str
    url: str
    stars: int = 0
    forks: int = 0
    language: str = "Unknown"
    category_id: int = 1
    category_name: str = ""
    description: str = ""
    architecture_workflow: str = ""
    quality_gate: QualityGate = QualityGate.VERIFIED
    license: str = "MIT"
    license_category: LicenseCategory = LicenseCategory.PERMISSIVE
    days_since_last_commit: int = 15
    open_issues: int = 10
    closed_issues: int = 50
    has_security_policy: bool = True
    cve_critical_count: int = 0
    cve_medium_count: int = 0
    is_archived: bool = False
    supported_os: List[str] = field(default_factory=lambda: ["windows", "linux", "darwin"])
    runtime_versions: List[str] = field(default_factory=lambda: ["3.10", "3.11", "3.12"])
    has_quickstart: bool = True
    has_examples: bool = True
    readme_length_chars: int = 3500
    dependency_count: int = 5
    has_package_manager_dist: bool = True
    requires_specialized_hardware: bool = False  # e.g., Multi-GPU / TPU only


@dataclass
class TaskRequirement:
    """Specification of the task / tool calling intent."""
    query: str
    required_features: List[str] = field(default_factory=list)
    optional_features: List[str] = field(default_factory=list)
    target_language: Optional[str] = None
    target_os: str = "windows"
    target_runtime_version: Optional[str] = None
    required_license_policy: str = "PERMISSIVE_ONLY"  # "PERMISSIVE_ONLY", "WEAK_COPYLEFT_ALLOWED", "ANY_OPEN_SOURCE"
    disallow_archived: bool = True
    max_acceptable_critical_cve: int = 0
    hardware_constraint: str = "CPU_OR_CONSUMER_GPU"  # "CPU_ONLY", "CPU_OR_CONSUMER_GPU", "SPECIALIZED_CLUSTER"
    category_preference: Optional[str] = None


@dataclass
class WeightProfile:
    """Weight vector governing the 9 scoring signals."""
    name: str
    w_task: float
    w_feature: float
    w_maint: float
    w_docs: float
    w_compat: float
    w_sec: float
    w_license: float
    w_mat: float
    w_deploy: float

    def validate(self) -> None:
        total = (
            self.w_task
            + self.w_feature
            + self.w_maint
            + self.w_docs
            + self.w_compat
            + self.w_sec
            + self.w_license
            + self.w_mat
            + self.w_deploy
        )
        if not math.isclose(total, 1.0, rel_tol=1e-3):
            raise ValueError(f"Weight profile '{self.name}' must sum to 1.0, got {total:.4f}")


# Standard Enterprise Weighting Profiles
WEIGHT_PROFILES: Dict[str, WeightProfile] = {
    # Core Standard Profiles
    "ENTERPRISE_PRODUCTION": WeightProfile(
        name="ENTERPRISE_PRODUCTION",
        w_task=0.18,
        w_feature=0.16,
        w_maint=0.14,
        w_docs=0.10,
        w_compat=0.12,
        w_sec=0.12,
        w_license=0.08,
        w_mat=0.05,
        w_deploy=0.05,
    ),
    "FAST_PROTOTYPING": WeightProfile(
        name="FAST_PROTOTYPING",
        w_task=0.25,
        w_feature=0.22,
        w_maint=0.08,
        w_docs=0.10,
        w_compat=0.12,
        w_sec=0.05,
        w_license=0.03,
        w_mat=0.05,
        w_deploy=0.10,
    ),
    "AUTONOMOUS_SWARM_AGENT": WeightProfile(
        name="AUTONOMOUS_SWARM_AGENT",
        w_task=0.22,
        w_feature=0.20,
        w_maint=0.12,
        w_docs=0.14,
        w_compat=0.10,
        w_sec=0.08,
        w_license=0.04,
        w_mat=0.04,
        w_deploy=0.06,
    ),
    "SAFETY_CRITICAL": WeightProfile(
        name="SAFETY_CRITICAL",
        w_task=0.15,
        w_feature=0.15,
        w_maint=0.14,
        w_docs=0.10,
        w_compat=0.12,
        w_sec=0.20,
        w_license=0.06,
        w_mat=0.04,
        w_deploy=0.04,
    ),
    # Additional Transparent Scoring Profiles
    "BALANCED": WeightProfile(
        name="BALANCED",
        w_task=0.18,
        w_feature=0.16,
        w_maint=0.14,
        w_docs=0.10,
        w_compat=0.12,
        w_sec=0.12,
        w_license=0.08,
        w_mat=0.05,
        w_deploy=0.05,
    ),
    "STABILITY_FIRST": WeightProfile(
        name="STABILITY_FIRST",
        w_task=0.14,
        w_feature=0.12,
        w_maint=0.18,
        w_docs=0.10,
        w_compat=0.12,
        w_sec=0.18,
        w_license=0.08,
        w_mat=0.04,
        w_deploy=0.04,
    ),
    "INNOVATION_FIRST": WeightProfile(
        name="INNOVATION_FIRST",
        w_task=0.26,
        w_feature=0.24,
        w_maint=0.08,
        w_docs=0.10,
        w_compat=0.10,
        w_sec=0.05,
        w_license=0.04,
        w_mat=0.05,
        w_deploy=0.08,
    ),
    "LIGHTWEIGHT": WeightProfile(
        name="LIGHTWEIGHT",
        w_task=0.20,
        w_feature=0.16,
        w_maint=0.10,
        w_docs=0.10,
        w_compat=0.20,
        w_sec=0.06,
        w_license=0.05,
        w_mat=0.03,
        w_deploy=0.10,
    ),
}


@dataclass
class SignalBreakdown:
    raw_value: float
    weight: float
    weighted_contribution: float
    description: str
    score_100: float = 0.0
    weighted_contribution_100: float = 0.0

    def __post_init__(self):
        if self.score_100 == 0.0 and self.raw_value != 0.0:
            self.score_100 = round(self.raw_value * 100.0, 2)
        if self.weighted_contribution_100 == 0.0 and self.weighted_contribution != 0.0:
            self.weighted_contribution_100 = round(self.weighted_contribution * 100.0, 2)


@dataclass
class RankingExplanation:
    """Comprehensive, fully transparent explanation of a repository's ranking."""
    repository: str
    rank: int = 0
    final_score: float = 0.0
    score_100: float = 0.0
    base_score: float = 0.0
    base_score_100: float = 0.0
    penalty_multiplier: float = 1.0
    subtractive_penalty: float = 0.0
    is_disqualified: bool = False
    disqualification_reason: Optional[str] = None
    profile_used: str = "ENTERPRISE_PRODUCTION"
    signals: Dict[str, SignalBreakdown] = field(default_factory=dict)
    applied_penalties: List[Dict[str, Any]] = field(default_factory=list)
    tie_break_metrics: Dict[str, Any] = field(default_factory=dict)
    audit_narrative: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_markdown_summary(self) -> str:
        lines = [
            f"### #{self.rank} `{self.repository}` — Final Score: **{self.final_score:.4f}** ({self.score_100:.1f}/100)",
            f"- **Base Score**: {self.base_score:.4f} ({self.base_score_100:.1f}/100) | **Penalty Multiplier**: {self.penalty_multiplier:.2f} | **Subtractive**: -{self.subtractive_penalty:.4f}",
            f"- **Profile**: `{self.profile_used}` | **Status**: {'DISQUALIFIED' if self.is_disqualified else 'APPROVED'}",
        ]
        if self.is_disqualified:
            lines.append(f"- **Disqualification Reason**: ⚠️ {self.disqualification_reason}")
            return "\n".join(lines)

        lines.append("\n| Scoring Signal | Raw [0-1] | Score (0-100) | Weight | Contribution (0-100) | Notes |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :--- |")
        for key, s in self.signals.items():
            name = key.replace("_", " ").title()
            lines.append(f"| **{name}** | {s.raw_value:.3f} | {s.score_100:.1f} | {s.weight:.2f} | {s.weighted_contribution_100:.2f} | {s.description} |")

        if self.applied_penalties:
            lines.append("\n**Applied Penalties:**")
            for p in self.applied_penalties:
                lines.append(f"- `{p['type']}` ({p.get('impact', '')}): {p['reason']}")

        lines.append(f"\n> **Audit Narrative**: {self.audit_narrative}\n")
        return "\n".join(lines)


class TransparentRankingEngine:
    """
    Core Transparent Ranking Engine.
    Executes mathematically rigorous, fully auditable candidate ranking.
    """

    def __init__(self, default_profile: str = "ENTERPRISE_PRODUCTION"):
        norm_profile = default_profile.upper()
        if norm_profile not in WEIGHT_PROFILES:
            raise KeyError(f"Unknown weight profile: {default_profile}. Available: {list(WEIGHT_PROFILES.keys())}")
        self.default_profile = norm_profile

    # --------------------------------------------------------------------------
    # 1. Scoring Signal Functions (Each mapped strictly to [0.0, 1.0])
    # --------------------------------------------------------------------------

    @staticmethod
    def tokenize(text: str) -> Set[str]:
        if not text:
            return set()
        words = re.findall(r"[A-Za-z0-9_\-\.\+]+", text.lower())
        # Filter very short stop-like tokens
        return {w for w in words if len(w) > 1}

    def compute_task_relevance(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 1: Task Relevance (S_task)
        Semantic and lexical alignment between query task and repo metadata.
        """
        if not task.query.strip():
            return 1.0, "Empty query; default maximum relevance"

        query_tokens = self.tokenize(task.query)
        if not query_tokens:
            return 0.5, "Query contained no significant tokens"

        repo_text = f"{repo.name} {repo.description} {repo.category_name} {repo.language} {repo.architecture_workflow}"
        repo_tokens = self.tokenize(repo_text)

        # 1. Exact query phrase match bonus
        normalized_query = task.query.lower().strip()
        phrase_match_bonus = 0.20 if normalized_query in repo_text.lower() else 0.0

        # 2. Token overlap (Jaccard / containment)
        overlap = query_tokens.intersection(repo_tokens)
        containment = len(overlap) / len(query_tokens)

        # 3. Category affinity
        category_affinity = 0.0
        if task.category_preference and task.category_preference.lower() in repo.category_name.lower():
            category_affinity = 0.20

        # 4. Workflow token alignment
        wf_tokens = self.tokenize(repo.architecture_workflow)
        wf_overlap = len(query_tokens.intersection(wf_tokens)) / len(query_tokens) if query_tokens else 0.0

        # Raw score bounded to [0, 1]
        raw = (0.50 * containment) + phrase_match_bonus + category_affinity + (0.10 * wf_overlap)
        score = min(1.0, max(0.0, raw))
        desc = f"Token overlap {len(overlap)}/{len(query_tokens)} ({containment:.0%}), phrase bonus={phrase_match_bonus:.2f}"
        return score, desc

    def compute_feature_fit(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 2: Feature Fit (S_feature)
        Coverage of required and optional operational capabilities.
        """
        repo_surface = f"{repo.description} {repo.architecture_workflow} {repo.language}".lower()

        if not task.required_features and not task.optional_features:
            # Fall back to workflow richness as an indicator of feature completeness
            wf_len = len(repo.architecture_workflow)
            fit = min(1.0, max(0.5, wf_len / 120.0))
            return fit, f"No explicit feature list requested; derived from workflow complexity ({wf_len} chars)"

        req_matched = 0
        if task.required_features:
            for feat in task.required_features:
                if feat.lower() in repo_surface:
                    req_matched += 1
            req_ratio = req_matched / len(task.required_features)
        else:
            req_ratio = 1.0

        opt_matched = 0
        if task.optional_features:
            for feat in task.optional_features:
                if feat.lower() in repo_surface:
                    opt_matched += 1
            opt_ratio = opt_matched / len(task.optional_features)
        else:
            opt_ratio = 1.0

        if task.required_features and not task.optional_features:
            score = req_ratio
        elif task.optional_features and not task.required_features:
            score = opt_ratio
        else:
            score = (0.75 * req_ratio) + (0.25 * opt_ratio)

        desc = f"Matched {req_matched}/{len(task.required_features)} required, {opt_matched}/{len(task.optional_features)} optional"
        return min(1.0, max(0.0, score)), desc

    def compute_maintenance_evidence(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 3: Maintenance Evidence (S_maint)
        Stewardship vitality using exponential half-life decay on commit age and issue resolution ratio.
        """
        # Half life model: Lambda(t) = exp(- ln(2) * t / tau), tau = 180 days
        t = max(0, repo.days_since_last_commit)
        tau = 180.0
        recency_factor = math.exp(-0.693147 * (t / tau))

        # Issue resolution ratio
        total_issues = repo.open_issues + repo.closed_issues
        if total_issues > 0:
            issue_health = repo.closed_issues / total_issues
        else:
            issue_health = 0.70  # Default neutral

        score = (0.65 * recency_factor) + (0.35 * issue_health)
        desc = f"Last commit {t}d ago (recency={recency_factor:.2f}), closed issue ratio={issue_health:.0%}"
        return min(1.0, max(0.0, score)), desc

    def compute_documentation_clarity(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 4: Documentation Clarity (S_docs)
        Existence of architecture workflow, quickstart, runnable examples, and density.
        """
        has_wf = 1.0 if repo.architecture_workflow and "->" in repo.architecture_workflow else 0.3
        has_qs = 1.0 if repo.has_quickstart else 0.0
        has_ex = 1.0 if repo.has_examples else 0.0

        # Saturation curve for documentation length (2500 chars saturated)
        density = min(1.0, max(0.0, repo.readme_length_chars / 2500.0))

        score = (0.35 * has_wf) + (0.25 * has_qs) + (0.20 * has_ex) + (0.20 * density)
        desc = f"Workflow verified={has_wf > 0.5}, Quickstart={bool(has_qs)}, Examples={bool(has_ex)}, Density={density:.2f}"
        return min(1.0, max(0.0, score)), desc

    def compute_compatibility(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 5: Compatibility (S_compat)
        Operating system, language stack, runtime version, and dependency footprint.
        """
        # 1. OS Match
        os_match = 1.0 if task.target_os.lower() in [o.lower() for o in repo.supported_os] else 0.0

        # 2. Language Match
        if task.target_language:
            lang_match = 1.0 if task.target_language.lower() in repo.language.lower() else 0.3
        else:
            lang_match = 1.0

        # 3. Runtime Version Match
        if task.target_runtime_version:
            ver_match = 1.0 if any(task.target_runtime_version in v for v in repo.runtime_versions) else 0.4
        else:
            ver_match = 1.0

        # 4. Dependency Footprint (fewer dependencies = higher score)
        # 0 deps = 1.0, 5 deps = 0.9, 20 deps = 0.6, 50+ deps = 0.2
        dep_penalty = min(0.80, repo.dependency_count * 0.015)
        dep_score = 1.0 - dep_penalty

        score = (0.35 * os_match) + (0.35 * lang_match) + (0.15 * ver_match) + (0.15 * dep_score)
        desc = f"OS({task.target_os})={os_match}, Lang={lang_match:.2f}, Ver={ver_match:.2f}, DepFootprint={dep_score:.2f}"
        return min(1.0, max(0.0, score)), desc

    def compute_security_signals(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 6: Security Signals (S_sec)
        Quality gate audit tier, security policy, and CVE absence.
        """
        # Quality Gate baseline
        gate_map = {
            QualityGate.CERTIFIED: 1.0,
            QualityGate.VERIFIED: 0.85,
            QualityGate.PASSED: 0.70,
            QualityGate.UNKNOWN: 0.40,
        }
        gate_baseline = gate_map.get(repo.quality_gate, 0.40)

        # Exponential decay on CVE count: e^(-0.8 * critical - 0.2 * medium)
        cve_decay = math.exp(-0.8 * repo.cve_critical_count - 0.2 * repo.cve_medium_count)

        sec_policy_bonus = 0.10 if repo.has_security_policy else 0.0

        score = min(1.0, max(0.0, (gate_baseline * cve_decay) + sec_policy_bonus))
        desc = f"Gate={repo.quality_gate.value} ({gate_baseline:.2f}), CVEs=[crit:{repo.cve_critical_count}, med:{repo.cve_medium_count}], Policy={repo.has_security_policy}"
        return score, desc

    def compute_license_fit(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 7: License Fit (S_license)
        Compatibility of repository license against deployment policy.
        """
        cat = repo.license_category
        policy = task.required_license_policy.upper()

        if policy == "PERMISSIVE_ONLY":
            if cat == LicenseCategory.PERMISSIVE:
                score = 1.0
            elif cat == LicenseCategory.WEAK_COPYLEFT:
                score = 0.50
            elif cat == LicenseCategory.STRONG_COPYLEFT:
                score = 0.10
            else:
                score = 0.0
        elif policy == "WEAK_COPYLEFT_ALLOWED":
            if cat in [LicenseCategory.PERMISSIVE, LicenseCategory.WEAK_COPYLEFT]:
                score = 1.0
            elif cat == LicenseCategory.STRONG_COPYLEFT:
                score = 0.40
            else:
                score = 0.0
        elif policy == "ANY_OPEN_SOURCE":
            if cat in [LicenseCategory.PERMISSIVE, LicenseCategory.WEAK_COPYLEFT, LicenseCategory.STRONG_COPYLEFT, LicenseCategory.NETWORK_COPYLEFT]:
                score = 1.0
            else:
                score = 0.20
        else:  # Custom or general
            score = 1.0 if cat == LicenseCategory.PERMISSIVE else 0.70

        desc = f"License='{repo.license}' ({cat.value}) under policy '{policy}'"
        return score, desc

    def compute_maturity(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 8: Maturity (S_mat)
        Adoption mass using logarithmic damping to prevent star monopolization.
        """
        # Log10 damping: log10(1 + stars) / log10(1 + 50000)
        stars_norm = math.log10(1.0 + max(0, repo.stars)) / math.log10(50001.0)
        stars_score = min(1.0, max(0.0, stars_norm))

        # Forks damping: log10(1 + forks) / log10(1 + 10000)
        forks_norm = math.log10(1.0 + max(0, repo.forks)) / math.log10(10001.0)
        forks_score = min(1.0, max(0.0, forks_norm))

        # Combine
        score = (0.65 * stars_score) + (0.35 * forks_score)
        desc = f"Stars={repo.stars:,} (norm={stars_score:.2f}), Forks={repo.forks:,} (norm={forks_score:.2f})"
        return score, desc

    def compute_deployment_fit(self, repo: RepositoryMetadata, task: TaskRequirement) -> Tuple[float, str]:
        """
        Signal 9: Deployment Fit (S_deploy)
        Packaging readiness, container/wheel availability, and hardware feasibility.
        """
        pkg_score = 1.0 if repo.has_package_manager_dist else 0.40

        # Hardware constraint evaluation
        if task.hardware_constraint == "CPU_ONLY" and repo.requires_specialized_hardware:
            hw_score = 0.10
        elif task.hardware_constraint == "CPU_OR_CONSUMER_GPU" and repo.requires_specialized_hardware:
            hw_score = 0.50
        else:
            hw_score = 1.0

        score = (0.50 * pkg_score) + (0.50 * hw_score)
        desc = f"Packaged={repo.has_package_manager_dist}, HardwareFit={hw_score:.2f}"
        return min(1.0, max(0.0, score)), desc

    # --------------------------------------------------------------------------
    # 2. Penalty Policies & Hard Elimination Gates
    # --------------------------------------------------------------------------

    def evaluate_penalties_and_gates(
        self, repo: RepositoryMetadata, task: TaskRequirement
    ) -> Tuple[bool, Optional[str], float, float, List[Dict[str, Any]]]:
        """
        Evaluates Hard Elimination Gates and Multiplicative / Subtractive Penalties.
        Returns:
            is_disqualified (bool)
            disqualification_reason (Optional[str])
            penalty_multiplier (float) in (0, 1]
            subtractive_penalty (float) >= 0.0
            applied_penalties (list of penalty logs)
        """
        applied: List[Dict[str, Any]] = []

        # --- A. HARD ELIMINATION GATES ---
        # Gate 1: Critical CVE threshold
        if repo.cve_critical_count > task.max_acceptable_critical_cve:
            return True, f"Critical CVE count ({repo.cve_critical_count}) exceeds threshold ({task.max_acceptable_critical_cve})", 0.0, 0.0, applied

        # Gate 2: Archived status
        if task.disallow_archived and repo.is_archived:
            return True, "Repository is archived/read-only on GitHub and disallow_archived is True", 0.0, 0.0, applied

        # Gate 3: Incompatible License under strict policy
        if task.required_license_policy == "PERMISSIVE_ONLY" and repo.license_category in [
            LicenseCategory.STRONG_COPYLEFT,
            LicenseCategory.NETWORK_COPYLEFT,
            LicenseCategory.PROPRIETARY,
        ]:
            return True, f"License '{repo.license}' ({repo.license_category.value}) is strictly disallowed by PERMISSIVE_ONLY policy", 0.0, 0.0, applied

        # Gate 4: Hard OS mismatch
        if task.target_os.lower() not in [o.lower() for o in repo.supported_os]:
            return True, f"Target OS '{task.target_os}' not supported by repository (supports: {repo.supported_os})", 0.0, 0.0, applied

        # --- B. SOFT MULTIPLICATIVE PENALTIES ---
        multiplier = 1.0

        # Penalty 1: Stale Maintenance (> 365 days)
        if repo.days_since_last_commit > 730:
            p = 0.50
            multiplier *= p
            applied.append({"type": "STALE_MAINTENANCE_SEVERE", "impact": f"x{p}", "reason": f"Last commit {repo.days_since_last_commit} days ago (>2 years)"})
        elif repo.days_since_last_commit > 365:
            p = 0.75
            multiplier *= p
            applied.append({"type": "STALE_MAINTENANCE_MODERATE", "impact": f"x{p}", "reason": f"Last commit {repo.days_since_last_commit} days ago (>1 year)"})

        # Penalty 2: Missing or un-audited architectural workflow
        if not repo.architecture_workflow or "->" not in repo.architecture_workflow:
            p = 0.85
            multiplier *= p
            applied.append({"type": "MISSING_WORKFLOW", "impact": f"x{p}", "reason": "Lacks audited pipeline workflow string"})

        # Penalty 3: High Transitive Dependencies (> 30 dependencies)
        if repo.dependency_count > 30:
            p = 0.85
            multiplier *= p
            applied.append({"type": "HIGH_DEPENDENCY_RISK", "impact": f"x{p}", "reason": f"Heavy dependency graph ({repo.dependency_count} dependencies)"})

        # Penalty 4: Thin Documentation (< 400 characters README)
        if repo.readme_length_chars < 400:
            p = 0.80
            multiplier *= p
            applied.append({"type": "THIN_DOCUMENTATION", "impact": f"x{p}", "reason": f"Minimal documentation ({repo.readme_length_chars} chars)"})

        # --- C. SUBTRACTIVE PENALTIES ---
        subtractive = 0.0

        # Subtractive 1: Issue Backlog Skew (open issues > 10x closed issues)
        if repo.open_issues > 10 and repo.open_issues > 10 * max(1, repo.closed_issues):
            sub = 0.08
            subtractive += sub
            applied.append({"type": "ISSUE_BACKLOG_SKEW", "impact": f"-{sub}", "reason": f"Severe issue backlog (open: {repo.open_issues}, closed: {repo.closed_issues})"})

        # Subtractive 2: Medium CVEs
        if repo.cve_medium_count > 0:
            sub = min(0.15, repo.cve_medium_count * 0.04)
            subtractive += sub
            applied.append({"type": "MEDIUM_SECURITY_EXPOSURE", "impact": f"-{sub:.2f}", "reason": f"{repo.cve_medium_count} unpatched medium-severity CVE(s)"})

        # Subtractive 3: Non-verified Quality Gate
        if repo.quality_gate in [QualityGate.PASSED, QualityGate.UNKNOWN]:
            sub = 0.03
            subtractive += sub
            applied.append({"type": "NON_VERIFIED_GATE", "impact": f"-{sub}", "reason": f"Gate is {repo.quality_gate.value}, below VERIFIED tier"})

        return False, None, multiplier, subtractive, applied

    # --------------------------------------------------------------------------
    # 3. Deterministic 5-Tier Tie-Breaking Key
    # --------------------------------------------------------------------------

    @staticmethod
    def tie_break_key(repo: RepositoryMetadata, final_score: float) -> Tuple[Any, ...]:
        """
        Five-tier deterministic sorting key for ASCENDING sort:
        1. -rounded_score: Higher score comes first
        2. -gate_priority: Higher gate comes first (CERTIFIED=3, VERIFIED=2, PASSED=1, UNKNOWN=0)
        3. days_since_last_commit: Lower age (fresher) comes first
        4. -wf_len: Richer architectural workflow comes first
        5. -stars: Higher adoption mass comes first
        6. repo.name: Canonical alphabetical name (A-Z) ensuring absolute cross-platform reproducibility
        """
        rounded_score = round(final_score, 5)
        gate_priority = repo.quality_gate.rank_weight
        days_commit = repo.days_since_last_commit
        wf_len = len(repo.architecture_workflow)
        stars = repo.stars
        return (-rounded_score, -gate_priority, days_commit, -wf_len, -stars, repo.name)

    # --------------------------------------------------------------------------
    # 4. Master Scoring & Explainability Engine
    # --------------------------------------------------------------------------

    def score_repository(
        self,
        repo: RepositoryMetadata,
        task: TaskRequirement,
        profile_name: Optional[str] = None,
    ) -> RankingExplanation:
        """Computes transparent score and complete explainability report for a single repository."""
        p_name = (profile_name or self.default_profile).upper()
        profile = WEIGHT_PROFILES.get(p_name, WEIGHT_PROFILES.get(self.default_profile, WEIGHT_PROFILES["ENTERPRISE_PRODUCTION"]))

        explanation = RankingExplanation(repository=repo.name, profile_used=p_name)

        # 1. Evaluate Hard Gates & Penalties
        disqualified, disq_reason, multiplier, subtractive, penalties = self.evaluate_penalties_and_gates(repo, task)
        explanation.is_disqualified = disqualified
        explanation.disqualification_reason = disq_reason
        explanation.penalty_multiplier = multiplier
        explanation.subtractive_penalty = subtractive
        explanation.applied_penalties = penalties

        # 2. Compute the 9 Interpretable Scoring Signals
        signals_map = {
            "task_relevance": (self.compute_task_relevance(repo, task), profile.w_task),
            "feature_fit": (self.compute_feature_fit(repo, task), profile.w_feature),
            "maintenance_evidence": (self.compute_maintenance_evidence(repo, task), profile.w_maint),
            "documentation_clarity": (self.compute_documentation_clarity(repo, task), profile.w_docs),
            "compatibility": (self.compute_compatibility(repo, task), profile.w_compat),
            "security_signals": (self.compute_security_signals(repo, task), profile.w_sec),
            "license_fit": (self.compute_license_fit(repo, task), profile.w_license),
            "maturity": (self.compute_maturity(repo, task), profile.w_mat),
            "deployment_fit": (self.compute_deployment_fit(repo, task), profile.w_deploy),
        }

        base_score = 0.0
        for name, ((raw, desc), weight) in signals_map.items():
            contrib = raw * weight
            base_score += contrib
            r_raw = round(raw, 4)
            r_weight = round(weight, 4)
            r_contrib = round(contrib, 4)
            explanation.signals[name] = SignalBreakdown(
                raw_value=r_raw,
                weight=r_weight,
                weighted_contribution=r_contrib,
                description=desc,
                score_100=round(r_raw * 100.0, 2),
                weighted_contribution_100=round(r_contrib * 100.0, 2),
            )

        explanation.base_score = round(base_score, 4)
        explanation.base_score_100 = round(base_score * 100.0, 2)

        # 3. Apply Multiplicative & Subtractive Penalties
        if disqualified:
            explanation.final_score = 0.0
            explanation.score_100 = 0.0
            explanation.audit_narrative = f"Disqualified: {disq_reason}."
        else:
            final = (base_score * multiplier) - subtractive
            final_bounded = max(0.0, min(1.0, final))
            explanation.final_score = round(final_bounded, 4)
            explanation.score_100 = round(final_bounded * 100.0, 2)

            # Generate narrative summary
            top_positive = max(explanation.signals.items(), key=lambda kv: kv[1].weighted_contribution)
            narrative = (
                f"Scored {explanation.final_score:.4f} ({explanation.score_100:.1f}/100) under profile {p_name}. "
                f"Strongest driver was {top_positive[0].replace('_', ' ').title()} (+{top_positive[1].weighted_contribution:.3f})."
            )
            if multiplier < 1.0:
                narrative += f" Soft penalties reduced score by factor of {multiplier:.2f}."
            if subtractive > 0:
                narrative += f" Subtractive penalties deducted {subtractive:.3f}."
            explanation.audit_narrative = narrative

        explanation.tie_break_metrics = {
            "quality_gate": repo.quality_gate.value,
            "days_since_last_commit": repo.days_since_last_commit,
            "workflow_length": len(repo.architecture_workflow),
            "stars": repo.stars,
            "canonical_name": repo.name,
        }

        return explanation

    def rank(
        self,
        repositories: List[RepositoryMetadata],
        task: TaskRequirement,
        profile_name: Optional[str] = None,
        top_k: Optional[int] = None,
    ) -> List[RankingExplanation]:
        """
        Ranks a collection of repositories against a task using transparent scoring,
        deterministic penalty policies, and strict tie-breaking.
        """
        p_name = (profile_name or self.default_profile).upper()
        explanations = [self.score_repository(repo, task, p_name) for repo in repositories]

        # Map repo names for fast lookup
        repo_map = {r.name: r for r in repositories}

        # Sort using the 5-tier deterministic key in ascending order (where negatives invert descending fields)
        def sort_comparator(item: RankingExplanation):
            repo = repo_map[item.repository]
            return self.tie_break_key(repo, item.final_score)

        ranked = sorted(explanations, key=sort_comparator, reverse=False)

        # Assign 1-based ranks
        for idx, item in enumerate(ranked, 1):
            item.rank = idx

        if top_k is not None and top_k > 0:
            return ranked[:top_k]
        return ranked


# --------------------------------------------------------------------------
# Standalone Functional API
# --------------------------------------------------------------------------

def rank_repositories(
    repositories: List[RepositoryMetadata],
    task: TaskRequirement,
    profile_name: str = "ENTERPRISE_PRODUCTION",
    top_k: Optional[int] = None,
) -> List[RankingExplanation]:
    """Helper wrapper function to rank repositories in one line."""
    engine = TransparentRankingEngine(default_profile=profile_name)
    return engine.rank(repositories, task, profile_name=profile_name, top_k=top_k)


# --------------------------------------------------------------------------
# SQLite Integration & CLI Runner
# --------------------------------------------------------------------------

def repo_from_sqlite_row(row: sqlite3.Row) -> RepositoryMetadata:
    """Instantiates RepositoryMetadata from a row in agents_registry.db."""
    gate_str = row["quality_gate"] if "quality_gate" in row.keys() else "VERIFIED"
    try:
        q_gate = QualityGate(gate_str)
    except ValueError:
        q_gate = QualityGate.VERIFIED

    # Infer license category
    desc = (row["description"] or "").lower()
    lic_cat = LicenseCategory.PERMISSIVE
    lic_name = "MIT"
    if "apache" in desc or "apache-2.0" in desc:
        lic_name = "Apache-2.0"
        lic_cat = LicenseCategory.PERMISSIVE
    elif "gpl-3.0" in desc or " gpl " in desc:
        lic_name = "GPL-3.0"
        lic_cat = LicenseCategory.STRONG_COPYLEFT
    elif "agpl" in desc:
        lic_name = "AGPL-3.0"
        lic_cat = LicenseCategory.NETWORK_COPYLEFT

    return RepositoryMetadata(
        name=row["name"],
        url=row["url"],
        stars=int(row["stars"]),
        forks=int(row["forks"]),
        language=row["language"] or "Unknown",
        category_id=int(row["category_id"]),
        category_name=row["category_name"] or "",
        description=row["description"] or "",
        architecture_workflow=row["workflow"] or "",
        quality_gate=q_gate,
        license=lic_name,
        license_category=lic_cat,
        days_since_last_commit=20,
        open_issues=15,
        closed_issues=85,
        has_security_policy=True,
        cve_critical_count=0,
        cve_medium_count=0,
        is_archived=False,
        supported_os=["windows", "linux", "darwin"],
        has_quickstart=True,
        has_examples=True,
        readme_length_chars=3000,
        dependency_count=6,
        has_package_manager_dist=True,
        requires_specialized_hardware=False,
    )


def rank_from_registry(
    db_path: str,
    query: str,
    category: Optional[str] = None,
    profile_name: str = "ENTERPRISE_PRODUCTION",
    limit: int = 10,
) -> List[RankingExplanation]:
    """Queries SQLite registry, converts candidates, and executes transparent ranking."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    words = [w for w in re.findall(r"[A-Za-z0-9_\-\+]+", query) if len(w) > 1]
    rows = []

    # 1. Attempt FTS5 Search first
    try:
        fts_query = " AND ".join(words) if words else query
        sql = """
        SELECT r.id, r.name, r.stars, r.forks, r.language, r.category_id, r.category_name, r.url, r.workflow, r.description, r.quality_gate
        FROM repositories_fts f
        JOIN repositories r ON f.rowid = r.id
        WHERE repositories_fts MATCH ?
        """
        params: List[Any] = [fts_query]
        if category:
            sql += " AND r.category_name LIKE ?"
            params.append(f"%{category}%")
        sql += " ORDER BY r.stars DESC LIMIT 100;"
        c.execute(sql, params)
        rows = c.fetchall()
    except Exception:
        rows = []

    # 2. Fallback to token LIKE if FTS returned nothing or failed
    if not rows:
        like_clauses = []
        params = []
        for w in (words if words else [query]):
            like_clauses.append("(name LIKE ? OR description LIKE ? OR workflow LIKE ?)")
            params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
        where_stmt = " AND ".join(like_clauses) if like_clauses else "1=1"
        sql = f"""
        SELECT id, name, stars, forks, language, category_id, category_name, url, workflow, description, quality_gate
        FROM repositories
        WHERE {where_stmt}
        """
        if category:
            sql += " AND category_name LIKE ?"
            params.append(f"%{category}%")
        sql += " ORDER BY stars DESC LIMIT 100;"
        c.execute(sql, params)
        rows = c.fetchall()

    conn.close()

    candidates = [repo_from_sqlite_row(r) for r in rows]
    task = TaskRequirement(query=query, category_preference=category)
    engine = TransparentRankingEngine(default_profile=profile_name)
    return engine.rank(candidates, task, profile_name=profile_name, top_k=limit)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transparent Ranking System for Github-Ultimate-Repos")
    parser.add_argument("--query", "-q", type=str, required=True, help="Task query or capability requirement")
    parser.add_argument("--category", "-c", type=str, default=None, help="Optional category filter")
    parser.add_argument("--profile", "-p", type=str, default="ENTERPRISE_PRODUCTION", choices=list(WEIGHT_PROFILES.keys()))
    parser.add_argument("--limit", "-n", type=int, default=5, help="Top K results to return")
    parser.add_argument("--json", action="store_true", help="Output full JSON audit trail")

    args = parser.parse_args()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    db_file = os.path.join(repo_root, "registry", "agents_registry.db")

    if not os.path.exists(db_file):
        print(f"Error: Registry database not found at {db_file}")
        sys.exit(1)

    results = rank_from_registry(
        db_path=db_file,
        query=args.query,
        category=args.category,
        profile_name=args.profile,
        limit=args.limit,
    )

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print("=" * 80)
        print(f" 🎯 TRANSPARENT RANKING RESULTS: '{args.query}' [{args.profile}]")
        print("=" * 80)
        for r in results:
            print(r.to_markdown_summary())
            print("-" * 80)
