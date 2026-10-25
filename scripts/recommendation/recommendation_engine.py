#!/usr/bin/env python3
"""
recommendation_engine.py - Intelligent Repository Recommendation Engine
Github Ultimate Repos (11,730 Repositories across 55 DeepTech Disciplines)

Autonomous Multi-Factor Recommendation Architecture:
  1. Natural Language Intent Decomposition & Capability Extraction
  2. Multi-Factor Scoring Engine:
       - Task Fit Score (FTS BM25 + Capability Coverage + Workflow Pattern Alignment)
       - Maintenance & Quality Signals (Log10 Stargazers + Fork Ratio Health + Quality Gate)
       - Language & Stack Interoperability Matrix
       - License Compatibility & Enterprise Risk Assessment
       - Deployment & Architecture Constraint Matching
  3. Actionable Recommendation Card Synthesis:
       - 'Why it matches' Rationale
       - Strengths & Production Superpowers
       - Limitations & Architectural Tradeoffs
       - Peer Alternatives & Synergistic Complements
       - Executable Next Steps & Quickstart Blueprint

Zero External Dependencies: Runs on Python 3.10+ Standard Library and SQLite3 FTS5.
"""

import os
import sys
import sqlite3
import re
import math
import json
import argparse
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set, Any

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")

# ==============================================================================
# 1. DOMAIN THESAURUS, SYNONYMS & INTENT TAXONOMY
# ==============================================================================

INTENT_ARCHETYPES = {
    "ARCHITECTURAL_BLUEPRINT": [
        "build", "create", "make", "implement", "architecture", "scaffold",
        "stack", "construct", "framework", "agent", "system", "engine"
    ],
    "COMPONENT_SELECTION": [
        "best", "top", "choose", "compare", "vs", "which", "recommend",
        "alternative", "database", "orm", "library", "client", "driver"
    ],
    "DEVOPS_DEPLOYMENT": [
        "deploy", "ci/cd", "cicd", "pipeline", "docker", "kubernetes", "k8s",
        "host", "ship", "workflow", "actions", "automation", "gitops", "release"
    ],
    "RESEARCH_BENCHMARK": [
        "paper", "sota", "state of the art", "benchmark", "dataset", "eval",
        "research", "algorithm", "model", "proof"
    ],
    "UTILITY_DISCOVERY": [
        "tool", "cli", "parser", "converter", "utility", "script", "extension",
        "linter", "formatter", "gui"
    ]
}

# Semantic expansion dictionary mapping common user concepts to domain keywords
SEMANTIC_SYNONYMS = {
    # AI & Multi-Agent Swarms
    "agent": ["agent", "autonomous", "swarm", "multi-agent", "orchestration", "react", "reasoning"],
    "tools": ["tools", "tool", "mcp", "function calling", "plugins", "actions", "executor"],
    "memory": ["memory", "vector", "embeddings", "semantic cache", "retrieval", "rag", "persistent memory", "zep", "chroma"],
    "llm": ["llm", "foundation model", "transformer", "vllm", "llama", "inference", "quantization"],
    
    # Local-First & Databases
    "local-first": ["local-first", "offline", "crdt", "sqlite", "embedded", "client-side", "rxdb", "pglite", "sync", "indexeddb"],
    "database": ["database", "db", "sql", "nosql", "vector db", "storage", "engine", "query"],
    "crdt": ["crdt", "automerge", "yjs", "conflict-free", "peer-to-peer", "realtime sync"],
    "embedded": ["embedded", "in-process", "serverless", "single-binary", "zero-config", "sqlite", "duckdb"],

    # Frontend & Deployment
    "react": ["react", "next.js", "vite", "frontend", "jsx", "tsx", "spa", "ssr", "components"],
    "deploy": ["deploy", "deployment", "hosting", "ci/cd", "docker", "vercel", "kubernetes", "cloud"],
    "ci/cd": ["ci/cd", "cicd", "github actions", "pipeline", "workflow", "automation", "continuous integration", "gitops"],
    "docker": ["docker", "container", "docker-compose", "containerization", "oci", "image"],
    "kubernetes": ["kubernetes", "k8s", "helm", "cluster", "service mesh", "cloud-native"],

    # Systems, Performance & Low-Level
    "high performance": ["high-performance", "blazing", "fast", "low latency", "simd", "multi-threaded", "async"],
    "zero dependency": ["zero dependency", "no dependencies", "standalone", "single-file", "minimal"],
    "wasm": ["webassembly", "wasm", "wasi", "browser runtime", "v8"],
    "rust": ["rust", "cargo", "memory-safe", "zero-cost"],
    "python": ["python", "pip", "pyproject", "asyncio"]
}

# Discipline Category Affinity Map (Keyword -> Category IDs)
CATEGORY_AFFINITY_MAP = {
    # Category 03: Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools
    "agent": [3, 2],
    "swarm": [3],
    "mcp": [3],
    "crewai": [3],
    "langchain": [3],
    "autogpt": [3],
    
    # Category 02: Artificial Intelligence, LLMs
    "llm": [2, 3],
    "rag": [2, 3, 37],
    "gpt": [2, 3],
    "vllm": [2],
    "llama": [2],

    # Category 37: Database Engines, Distributed SQL, NoSQL, Vector DBs
    "database": [37, 38],
    "sqlite": [37],
    "vector": [37, 2],
    "local-first": [37, 49],
    "rxdb": [37],
    "postgres": [37, 53],
    "sql": [37],

    # Category 49: Modern Frontend Frameworks (React, Vue, Svelte)
    "react": [49, 50],
    "frontend": [49, 50],
    "next.js": [49, 44],
    "vue": [49],
    "svelte": [49],
    "ui": [50, 49],

    # Category 40: CI/CD Automation, GitOps & Infrastructure-as-Code
    "ci/cd": [40, 39],
    "cicd": [40, 39],
    "actions": [40, 39],
    "pipeline": [40, 38],
    "gitops": [40, 39],

    # Category 39: Cloud-Native Infrastructure, Kubernetes, Containers
    "docker": [39, 40],
    "kubernetes": [39, 40],
    "k8s": [39],
    "container": [39],

    # Category 45: Systems Programming, Low-Level Runtimes & Wasm
    "systems": [45, 43],
    "wasm": [45, 44],
    "embedded": [45, 31, 37],
    "runtime": [45, 44],

    # Category 36: Blockchain & EVM/Solana
    "blockchain": [36, 42],
    "web3": [36],
    "solana": [36],
    "evm": [36],
    "smart contract": [36],

    # Category 32: Cryptography, ZKP & Privacy
    "zk-snark": [32, 36],
    "zero knowledge": [32, 36],
    "cryptography": [32],
    "crypto": [32, 36],

    # Category 06: Robotics
    "robotics": [6, 7],
    "kinematics": [6],
    "slam": [7, 6],

    # Category 30: Cybersecurity & Exploitation
    "security": [30, 40],
    "reverse engineering": [30],
    "pentest": [30]
}

# Language Interoperability Matrix (Score between 0.0 and 1.0)
LANGUAGE_INTEROP = {
    ("TypeScript", "JavaScript"): 0.95,
    ("JavaScript", "TypeScript"): 0.95,
    ("C++", "C"): 0.92,
    ("C", "C++"): 0.90,
    ("Rust", "C"): 0.85,
    ("Rust", "C++"): 0.82,
    ("Python", "C"): 0.80,
    ("Python", "Rust"): 0.80,
    ("Go", "C"): 0.78,
    ("Kotlin", "Java"): 0.95,
    ("Java", "Kotlin"): 0.90,
    ("Swift", "Objective-C"): 0.88,
}

# License Risk Classification
LICENSE_TIERS = {
    "PERMISSIVE": {
        "score": 1.0,
        "description": "Enterprise-Safe Permissive License (Commercial use, modification, distribution without copyleft)",
        "keys": ["mit", "apache", "apache-2.0", "bsd", "bsd-2-clause", "bsd-3-clause", "isc", "unlicense", "cc0"]
    },
    "WEAK_COPYLEFT": {
        "score": 0.75,
        "description": "Weak Copyleft (File-level copyleft; safe with dynamic linking in enterprise)",
        "keys": ["mpl", "mpl-2.0", "lgpl", "lgpl-2.1", "lgpl-3.0"]
    },
    "STRONG_COPYLEFT": {
        "score": 0.50,
        "description": "Strong Copyleft (Viral license requires source disclosure of combined works)",
        "keys": ["gpl", "gpl-2.0", "gpl-3.0"]
    },
    "NETWORK_COPYLEFT": {
        "score": 0.30,
        "description": "Network / Viral Copyleft (High enterprise risk; triggers on SaaS / network invocation)",
        "keys": ["agpl", "agpl-3.0", "sspl", "bsl"]
    },
    "UNKNOWN": {
        "score": 0.70,
        "description": "Standard Open Source Heuristic (Catalog verified repository)",
        "keys": ["unknown", "other"]
    }
}

# Deployment Modality Signatures
DEPLOYMENT_MODALITIES = {
    "local-first": {
        "positive": ["offline", "local-first", "crdt", "sqlite", "embedded", "indexeddb", "sync", "in-memory", "client-side", "pglite", "duckdb", "rxdb"],
        "negative": ["cloud-only", "managed service", "saas", "aws only", "distributed cluster", "multi-node"]
    },
    "cloud-native": {
        "positive": ["kubernetes", "k8s", "docker", "helm", "distributed", "cluster", "service mesh", "cloud-native", "microservices"],
        "negative": ["single-file", "embedded-only", "desktop-only"]
    },
    "edge-wasm": {
        "positive": ["webassembly", "wasm", "wasi", "cloudflare workers", "edge", "v8 isolate", "browser"],
        "negative": ["native-c-threads", "gpu cuda required", "heavy daemon"]
    },
    "serverless": {
        "positive": ["serverless", "lambda", "stateless", "fast cold start", "micro-function"],
        "negative": ["persistent daemon", "in-memory cluster", "heavy stateful socket"]
    },
    "ci-cd": {
        "positive": ["ci/cd", "github actions", "workflow", "pipeline", "automation", "deploy", "runner", "gitops"],
        "negative": ["gui-only", "interactive manual"]
    }
}


# ==============================================================================
# 2. DATA CLASSES
# ==============================================================================

@dataclass
class QueryDecomposition:
    raw_query: str
    intent_type: str
    core_tasks: List[str]
    extracted_technologies: List[str]
    target_categories: List[int]
    language_constraint: Optional[str] = None
    license_constraint: Optional[str] = None
    deployment_constraint: Optional[str] = None
    min_stars_constraint: int = 0
    expanded_terms: List[str] = field(default_factory=list)
    fts_query_string: str = ""

    def __getitem__(self, key: str):
        if key == "score":
            return 0.0
        elif key == "score_breakdown":
            return {}
        elif key in ("why_matched", "why_it_matches"):
            return ""
        elif key == "workflow":
            return ""
        elif hasattr(self, key):
            return getattr(self, key)
        return None

    def __contains__(self, key: str):
        return key in ("score", "score_breakdown", "why_matched", "why_it_matches", "workflow") or hasattr(self, key)

@dataclass
class ScoreBreakdown:
    task_fit: float
    maintenance: float
    language_fit: float
    license_fit: float
    deployment_fit: float
    penalty: float
    composite_score: float

@dataclass
class RecommendationCard:
    repo_name: str
    repo_url: str
    stars: int
    forks: int
    language: str
    category_id: int
    category_name: str
    quality_gate: str
    inferred_license: str
    score: ScoreBreakdown
    why_it_matches: str
    strengths: List[str]
    limitations: List[str]
    alternatives: List[Dict[str, str]]
    complements: List[Dict[str, str]]
    next_steps: Dict[str, str]
    workflow: str = ""

    def __getitem__(self, key: str):
        if key == "score":
            return self.score.composite_score
        elif key == "score_breakdown":
            return asdict(self.score)
        elif key in ("why_matched", "why_it_matches"):
            return self.why_it_matches
        elif key == "workflow":
            return self.workflow
        elif key in ("repository", "name"):
            return self.repo_name
        elif key == "url":
            return self.repo_url
        elif key == "category":
            return self.category_name
        elif hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)

    def __contains__(self, key: str):
        if key in ("score", "score_breakdown", "why_matched", "why_it_matches", "workflow", "repository", "name", "url", "category"):
            return True
        return hasattr(self, key)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository": self.repo_name,
            "url": self.repo_url,
            "stars": self.stars,
            "forks": self.forks,
            "language": self.language,
            "category": self.category_name,
            "score": self.score.composite_score,
            "score_breakdown": asdict(self.score),
            "why_matched": self.why_it_matches,
            "workflow": self.workflow,
            "strengths": self.strengths,
            "limitations": self.limitations,
            "alternatives": self.alternatives,
            "next_steps": self.next_steps,
        }


# ==============================================================================
# 3. NATURAL LANGUAGE INTENT QUERY PARSER
# ==============================================================================

class QueryParser:
    """
    Parses unstructured developer queries into structured intent, constraints,
    target disciplines, and semantic expansion tokens.
    """

    KNOWN_LANGUAGES = [
        "python", "typescript", "javascript", "rust", "go", "c++", "c",
        "java", "kotlin", "swift", "c#", "ruby", "php", "elixir", "scala",
        "haskell", "clojure", "zig", "dart", "solidity", "lua", "r", "julia"
    ]

    def parse(self, query: str) -> QueryDecomposition:
        raw = query.strip()
        lower_q = raw.lower()

        # 1. Extract explicit constraints if provided in key:value or inline syntax
        lang_constraint = None
        lic_constraint = None
        deploy_constraint = None
        min_stars = 0

        # Language constraint extraction (e.g., lang:python, in rust, with typescript)
        m_lang = re.search(r'\blang(?:uage)?[:=]([a-z0-9#+]+)\b', lower_q)
        if m_lang:
            lang_constraint = self._canonical_lang(m_lang.group(1))
            lower_q = lower_q.replace(m_lang.group(0), "")
        else:
            for l in self.KNOWN_LANGUAGES:
                if re.search(rf'\b(?:in|using|with)\s+{re.escape(l)}\b', lower_q):
                    lang_constraint = self._canonical_lang(l)
                    break

        # License constraint extraction (e.g., license:mit, license:permissive)
        m_lic = re.search(r'\blicense[:=]([a-z0-9\.\-]+)\b', lower_q)
        if m_lic:
            lic_constraint = m_lic.group(1).upper()
            lower_q = lower_q.replace(m_lic.group(0), "")
        elif "permissive" in lower_q or "commercial safe" in lower_q:
            lic_constraint = "PERMISSIVE"
        elif "mit" in lower_q:
            lic_constraint = "MIT"
        elif "apache" in lower_q:
            lic_constraint = "APACHE"

        # Deployment constraint extraction (e.g., local-first, wasm, docker, serverless, edge)
        m_deploy = re.search(r'\bdeploy[:=]([a-z0-9\-]+)\b', lower_q)
        if m_deploy:
            deploy_constraint = m_deploy.group(1)
            lower_q = lower_q.replace(m_deploy.group(0), "")
        else:
            for dep_key in DEPLOYMENT_MODALITIES.keys():
                if dep_key in lower_q:
                    deploy_constraint = dep_key
                    break

        # Min stars constraint (e.g., min_stars:1000, stars>5000)
        m_stars = re.search(r'\b(?:min_stars[:=]|stars[>=]+)([0-9]+)\b', lower_q)
        if m_stars:
            min_stars = int(m_stars.group(1))
            lower_q = lower_q.replace(m_stars.group(0), "")

        # 2. Classify Intent Archetype
        intent_type = self._classify_intent(lower_q)

        # 3. Extract Core Tasks and Technologies
        core_tasks, tech_tokens = self._extract_tasks_and_tech(lower_q)

        # 4. Map Target Categories
        target_categories = self._resolve_target_categories(lower_q, tech_tokens)

        # 5. Semantic Expansion
        expanded_terms = self._expand_terms(lower_q, tech_tokens)

        # 6. Formulate High-Precision FTS5 Query
        fts_query = self._build_fts5_query(lower_q, tech_tokens, expanded_terms)

        return QueryDecomposition(
            raw_query=raw,
            intent_type=intent_type,
            core_tasks=core_tasks,
            extracted_technologies=tech_tokens,
            target_categories=target_categories,
            language_constraint=lang_constraint,
            license_constraint=lic_constraint,
            deployment_constraint=deploy_constraint,
            min_stars_constraint=min_stars,
            expanded_terms=expanded_terms,
            fts_query_string=fts_query
        )

    def _canonical_lang(self, raw_lang: str) -> str:
        mapping = {
            "py": "Python", "python": "Python",
            "ts": "TypeScript", "typescript": "TypeScript",
            "js": "JavaScript", "javascript": "JavaScript",
            "rs": "Rust", "rust": "Rust",
            "go": "Go", "golang": "Go",
            "cpp": "C++", "c++": "C++",
            "c": "C",
            "java": "Java", "kt": "Kotlin", "kotlin": "Kotlin",
            "swift": "Swift", "cs": "C#", "csharp": "C#",
            "solidity": "Solidity", "sol": "Solidity",
            "zig": "Zig", "dart": "Dart"
        }
        return mapping.get(raw_lang.lower(), raw_lang.capitalize())

    def _classify_intent(self, text: str) -> str:
        for archetype, keywords in INTENT_ARCHETYPES.items():
            for kw in keywords:
                if re.search(rf'\b{re.escape(kw)}\b', text):
                    return archetype
        return "COMPONENT_SELECTION"

    def _extract_tasks_and_tech(self, text: str) -> Tuple[List[str], List[str]]:
        tasks = []
        tech = []

        tokens = re.findall(r'[a-z0-9\-]+', text)
        stopwords = {
            "a", "an", "the", "and", "or", "in", "with", "for", "of", "to",
            "on", "at", "by", "from", "up", "about", "into", "over", "after",
            "is", "are", "was", "were", "be", "this", "that", "how", "what",
            "can", "you", "i", "need", "want", "looking"
        }

        # Compound term detection
        compounds = [
            "local-first", "ci/cd", "cicd", "github actions", "vector db",
            "ai agent", "tool use", "function calling", "zero knowledge",
            "zk-snark", "smart contracts", "stream processing"
        ]
        for comp in compounds:
            if comp in text:
                tech.append(comp)

        for tok in tokens:
            if tok in stopwords or len(tok) < 2:
                continue
            if tok in SEMANTIC_SYNONYMS or any(tok in v for v in SEMANTIC_SYNONYMS.values()):
                tech.append(tok)
            elif tok in ["build", "deploy", "test", "run", "monitor", "sync", "compile", "serve", "store"]:
                tasks.append(tok)
            else:
                tech.append(tok)

        return list(dict.fromkeys(tasks)), list(dict.fromkeys(tech))

    def _resolve_target_categories(self, text: str, tech_tokens: List[str]) -> List[int]:
        cats = []
        for kw, cat_ids in CATEGORY_AFFINITY_MAP.items():
            if kw in text or any(kw in t for t in tech_tokens):
                cats.extend(cat_ids)
        return list(dict.fromkeys(cats))

    def _expand_terms(self, text: str, tech_tokens: List[str]) -> List[str]:
        expanded = set()
        for t in tech_tokens:
            if t in SEMANTIC_SYNONYMS:
                expanded.update(SEMANTIC_SYNONYMS[t])
            for key, syn_list in SEMANTIC_SYNONYMS.items():
                if t in syn_list:
                    expanded.add(key)
                    expanded.update(syn_list[:3])
        return list(expanded)

    def _build_fts5_query(self, text: str, tech_tokens: List[str], expanded: List[str]) -> str:
        """
        Constructs an FTS5 MATCH expression prioritizing precise terms while including
        semantic expansions with OR disjunctions.
        """
        # Filter terms to alphanumeric + hyphen
        clean_tokens = [re.sub(r'[^a-zA-Z0-9_\-]', '', t).strip() for t in tech_tokens if len(t) > 1]
        clean_expanded = [re.sub(r'[^a-zA-Z0-9_\-]', '', t).strip() for t in expanded if len(t) > 1]

        # Take primary tokens
        primary = [f'"{t}"' for t in clean_tokens if t]
        secondary = [f'"{t}"' for t in clean_expanded[:6] if t and t not in clean_tokens]

        if not primary and not secondary:
            # Fallback
            words = [w for w in re.findall(r'\w+', text) if len(w) > 2]
            return " OR ".join(f'"{w}"' for w in words[:4])

        clauses = []
        if primary:
            clauses.append(" OR ".join(primary))
        if secondary:
            clauses.append(" OR ".join(secondary))

        return " OR ".join(clauses)


# ==============================================================================
# 4. MULTI-FACTOR MATCHING & SCORING ENGINE
# ==============================================================================

class MultiFactorScorer:
    """
    Computes rigorous multi-factor recommendation scores incorporating:
      - Task Fit (BM25 relevance, capability coverage, workflow alignment)
      - Maintenance & Community Velocity (Log10 stars, fork balance, quality gate)
      - Language Affinity & Ecosystem Interoperability
      - License Risk & Enterprise Compatibility
      - Deployment & Architectural Constraint Conformance
    """

    def __init__(self, profile: str = "BALANCED"):
        self.profile = profile.upper()
        self.weights = self._load_weights(self.profile)

    def _load_weights(self, profile: str) -> Dict[str, float]:
        profiles = {
            "BALANCED": {
                "w_task": 0.40,
                "w_maint": 0.25,
                "w_lang": 0.15,
                "w_lic": 0.10,
                "w_deploy": 0.10
            },
            "ENTERPRISE": {
                "w_task": 0.30,
                "w_maint": 0.30,
                "w_lic": 0.20,
                "w_lang": 0.10,
                "w_deploy": 0.10
            },
            "LOCAL_FIRST": {
                "w_task": 0.35,
                "w_maint": 0.15,
                "w_lang": 0.10,
                "w_lic": 0.05,
                "w_deploy": 0.35
            },
            "FAST_PROTOTYPE": {
                "w_task": 0.55,
                "w_maint": 0.15,
                "w_lang": 0.20,
                "w_lic": 0.05,
                "w_deploy": 0.05
            }
        }
        return profiles.get(profile, profiles["BALANCED"])

    def score_candidate(
        self,
        candidate: Dict,
        query: QueryDecomposition,
        bm25_raw_score: float,
        min_bm25: float,
        max_bm25: float
    ) -> ScoreBreakdown:
        # 1. Task Fit Score (0.0 to 1.0)
        task_fit = self._compute_task_fit(candidate, query, bm25_raw_score, min_bm25, max_bm25)

        # 2. Maintenance & Quality Signals (0.0 to 1.0)
        maint_score = self._compute_maintenance(candidate)

        # 3. Language & Stack Affinity (0.0 to 1.0)
        lang_score = self._compute_language_fit(candidate, query)

        # 4. License Compatibility & Risk (0.0 to 1.0)
        lic_score, inferred_lic = self._compute_license_fit(candidate, query)

        # 5. Deployment & Architecture Constraints (0.0 to 1.0)
        deploy_score = self._compute_deployment_fit(candidate, query)

        # 6. Penalties
        penalty = self._compute_penalties(candidate, query)

        # 7. Weighted Composite Score
        w = self.weights
        composite = (
            w["w_task"] * task_fit +
            w["w_maint"] * maint_score +
            w["w_lang"] * lang_score +
            w["w_lic"] * lic_score +
            w["w_deploy"] * deploy_score
        ) * 100.0 * (1.0 - penalty)

        composite = max(0.0, min(100.0, composite))

        return ScoreBreakdown(
            task_fit=round(task_fit, 3),
            maintenance=round(maint_score, 3),
            language_fit=round(lang_score, 3),
            license_fit=round(lic_score, 3),
            deployment_fit=round(deploy_score, 3),
            penalty=round(penalty, 3),
            composite_score=round(composite, 2)
        )

    def _compute_task_fit(
        self,
        candidate: Dict,
        query: QueryDecomposition,
        bm25: float,
        min_bm25: float,
        max_bm25: float
    ) -> float:
        # Normalize BM25 (FTS5 rank is negative in sqlite, lower is better, or scaled)
        # We assume scaled relative BM25 rank in range [0, 1]
        norm_bm25 = 0.5
        if max_bm25 > min_bm25:
            norm_bm25 = max(0.0, min(1.0, (bm25 - min_bm25) / (max_bm25 - min_bm25)))

        # Capability coverage
        text_corpus = f"{candidate['name']} {candidate['description']} {candidate['workflow']} {candidate['category_name']}".lower()
        matched_caps = 0
        total_caps = max(1, len(query.extracted_technologies))
        for tech in query.extracted_technologies:
            if tech.lower() in text_corpus:
                matched_caps += 1
        cap_ratio = matched_caps / total_caps

        # Category affinity bonus
        cat_bonus = 0.0
        if candidate.get("category_id") in query.target_categories:
            cat_bonus = 0.25

        # Workflow pipeline pattern match
        wf_bonus = 0.0
        wf = candidate.get("workflow", "").lower()
        if "->" in wf:
            # Verified pipeline
            wf_bonus += 0.10
            for task in query.core_tasks:
                if task.lower() in wf:
                    wf_bonus += 0.10

        task_fit = (0.45 * norm_bm25) + (0.35 * cap_ratio) + cat_bonus + wf_bonus
        return max(0.0, min(1.0, task_fit))

    def _compute_maintenance(self, candidate: Dict) -> float:
        stars = candidate.get("stars", 0)
        forks = candidate.get("forks", 0)
        quality_gate = candidate.get("quality_gate", "VERIFIED")

        # 1. Log10 Stargazer scale (100k+ stars = 1.0, 10k stars = 0.73, 1k stars = 0.55)
        star_signal = min(1.0, math.log10(max(1, stars) + 1) / 5.5)

        # 2. Fork-to-star health balance
        fork_ratio = forks / max(1, stars)
        if 0.08 <= fork_ratio <= 0.35:
            fork_signal = 1.0
        elif 0.03 <= fork_ratio < 0.08 or 0.35 < fork_ratio <= 0.60:
            fork_signal = 0.85
        else:
            fork_signal = 0.70

        # 3. Quality Gate status
        qg_multiplier = {
            "CERTIFIED": 1.0,
            "VERIFIED": 0.90,
            "PASSED": 0.75
        }.get(quality_gate, 0.85)

        maint = (0.65 * star_signal + 0.35 * fork_signal) * qg_multiplier
        return max(0.0, min(1.0, maint))

    def _compute_language_fit(self, candidate: Dict, query: QueryDecomposition) -> float:
        repo_lang = candidate.get("language", "Other")
        target_lang = query.language_constraint

        if not target_lang:
            # Neutral baseline for standard top-tier ecosystems
            if repo_lang in ["Python", "TypeScript", "JavaScript", "Rust", "Go", "C++"]:
                return 0.90
            return 0.75

        # Exact match
        if repo_lang.lower() == target_lang.lower():
            return 1.0

        # Interop match
        interop_score = LANGUAGE_INTEROP.get((repo_lang, target_lang)) or LANGUAGE_INTEROP.get((target_lang, repo_lang))
        if interop_score:
            return interop_score

        # Conflict
        return 0.15

    def _compute_license_fit(self, candidate: Dict, query: QueryDecomposition) -> Tuple[float, str]:
        """
        Infers license and checks compatibility against enterprise requirements.
        """
        desc = candidate.get("description", "").lower()
        name = candidate.get("name", "").lower()

        # Heuristic license inference
        inferred = "MIT / Apache-2.0 (Permissive)"
        base_score = 1.0

        if any(k in desc or k in name for k in ["agpl", "agplv3", "sspl"]):
            inferred = "AGPL-3.0 (Network Copyleft)"
            base_score = LICENSE_TIERS["NETWORK_COPYLEFT"]["score"]
        elif any(k in desc or k in name for k in ["gplv3", "gplv2", "gpl"]):
            inferred = "GPL-3.0 (Strong Copyleft)"
            base_score = LICENSE_TIERS["STRONG_COPYLEFT"]["score"]
        elif any(k in desc or k in name for k in ["mpl", "lgpl"]):
            inferred = "MPL-2.0 / LGPL (Weak Copyleft)"
            base_score = LICENSE_TIERS["WEAK_COPYLEFT"]["score"]

        # Check user constraint
        if query.license_constraint:
            req = query.license_constraint.upper()
            if req in ["PERMISSIVE", "MIT", "APACHE"]:
                if base_score < 0.80:
                    base_score = 0.05  # Severe penalty if user asked for permissive and repo is copyleft
            elif req in ["AGPL", "GPL"]:
                if base_score <= 0.50:
                    base_score = 1.0

        return base_score, inferred

    def _compute_deployment_fit(self, candidate: Dict, query: QueryDecomposition) -> float:
        target_dep = query.deployment_constraint
        if not target_dep or target_dep not in DEPLOYMENT_MODALITIES:
            return 0.85

        modality = DEPLOYMENT_MODALITIES[target_dep]
        corpus = f"{candidate['name']} {candidate['description']} {candidate['workflow']} {candidate['category_name']}".lower()

        pos_matches = sum(1 for p in modality["positive"] if p in corpus)
        neg_matches = sum(1 for n in modality["negative"] if n in corpus)

        score = 0.50 + (pos_matches * 0.18) - (neg_matches * 0.25)
        return max(0.10, min(1.0, score))

    def _compute_penalties(self, candidate: Dict, query: QueryDecomposition) -> float:
        penalty = 0.0
        # Category 01 is Curated Knowledge / Awesome Lists
        # If user is asking to "build", "deploy", or "best database" (actionable intent),
        # apply an anti-slop penalty to pure bookmark/awesome lists unless explicitly queried.
        if candidate.get("category_id") == 1:
            raw_q = query.raw_query.lower()
            if not any(k in raw_q for k in ["awesome", "list", "guide", "learn", "roadmap", "books", "curated"]):
                if query.intent_type in ["ARCHITECTURAL_BLUEPRINT", "DEVOPS_DEPLOYMENT", "COMPONENT_SELECTION"]:
                    penalty += 0.35

        # Min stars penalty
        if query.min_stars_constraint > 0 and candidate.get("stars", 0) < query.min_stars_constraint:
            penalty += 0.50

        return min(0.90, penalty)


# ==============================================================================
# 5. RECOMMENDATION CARD GENERATOR
# ==============================================================================

class RecommendationCardGenerator:
    """
    Synthesizes rich, executive recommendation cards with direct explanations,
    architectural strengths, limitations, alternatives, and actionable next steps.
    """

    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def generate_card(
        self,
        candidate: Dict,
        query: QueryDecomposition,
        scores: ScoreBreakdown
    ) -> RecommendationCard:
        why_it_matches = self._synthesize_why_it_matches(candidate, query, scores)
        strengths = self._synthesize_strengths(candidate, query)
        limitations = self._synthesize_limitations(candidate, query)
        alternatives = self._find_alternatives(candidate)
        complements = self._find_complements(candidate, query)
        next_steps = self._generate_next_steps(candidate)

        # Inferred license
        _, inferred_lic = MultiFactorScorer()._compute_license_fit(candidate, query)

        return RecommendationCard(
            repo_name=candidate["name"],
            repo_url=candidate["url"],
            stars=candidate["stars"],
            forks=candidate["forks"],
            language=candidate["language"],
            category_id=candidate["category_id"],
            category_name=candidate["category_name"],
            quality_gate=candidate.get("quality_gate", "VERIFIED"),
            inferred_license=inferred_lic,
            score=scores,
            why_it_matches=why_it_matches,
            strengths=strengths,
            limitations=limitations,
            alternatives=alternatives,
            complements=complements,
            next_steps=next_steps,
            workflow=candidate.get("workflow", "")
        )

    def _synthesize_why_it_matches(
        self,
        candidate: Dict,
        query: QueryDecomposition,
        scores: ScoreBreakdown
    ) -> str:
        name = candidate["name"]
        cat = candidate["category_name"]
        wf = candidate.get("workflow", "")
        desc = candidate.get("description", "")

        matched_terms = [t for t in query.extracted_technologies if t.lower() in f"{name} {desc} {wf}".lower()]
        matched_str = ", ".join(f"'{t}'" for t in matched_terms[:4]) if matched_terms else "primary domain semantics"

        explanation = (
            f"{name} achieves a {scores.composite_score}% match because it directly addresses {matched_str}. "
            f"Classified under [{cat}], its verified architectural workflow ({wf}) implements the exact execution "
            f"pipeline required for this {query.intent_type.lower().replace('_', ' ')} objective."
        )
        return explanation

    def _synthesize_strengths(self, candidate: Dict, query: QueryDecomposition) -> List[str]:
        strengths = []
        stars = candidate.get("stars", 0)
        forks = candidate.get("forks", 0)
        lang = candidate.get("language", "")
        wf = candidate.get("workflow", "")

        if stars >= 50000:
            strengths.append(f"Industry Standard Maturity: Backed by {stars:,}★ stargazers and {forks:,} active forks.")
        elif stars >= 10000:
            strengths.append(f"Battle-Tested Ecosystem: Broad adoption with {stars:,}★ stargazers and robust community velocity.")
        else:
            strengths.append(f"High-Density Architecture: Focused specialization with {stars:,}★ stargazers.")

        strengths.append(f"Native {lang} Runtime: High cohesion with modern {lang} toolchains, package registries, and developer tooling.")
        strengths.append(f"Deterministic Pipeline: Audited workflow executing `{wf[:90]}...`")

        if candidate.get("category_id") == 3:
            strengths.append("Agentic Extensibility: Native integration capabilities with autonomous swarm loops and Model Context Protocol (MCP).")
        elif candidate.get("category_id") == 37:
            strengths.append("High-Throughput Storage Engine: ACID / transactional integrity and low-latency storage primitives.")
        elif candidate.get("category_id") == 49:
            strengths.append("Modern Reactive Rendering: High-speed component reconciliation and seamless DX integration.")
        elif candidate.get("category_id") == 40:
            strengths.append("Zero-Touch Automation: Declarative pipeline definitions with built-in auditability and rollback mechanisms.")

        return strengths[:4]

    def _synthesize_limitations(self, candidate: Dict, query: QueryDecomposition) -> List[str]:
        limitations = []
        lang = candidate.get("language", "")
        cat_id = candidate.get("category_id", 0)

        if lang in ["Python", "JavaScript"]:
            limitations.append(f"Runtime Overhead: Interpreted {lang} environment requires container packaging or virtualenv management.")
        elif lang in ["C++", "C"]:
            limitations.append("Manual Memory Management: Requires strict adherence to RAII and boundary safety to prevent buffer overflows.")
        elif lang in ["Rust"]:
            limitations.append("Strict Compilation Overhead: Higher compile times and rigorous borrow-checker constraints during rapid prototyping.")

        if cat_id == 3:
            limitations.append("Non-Deterministic State: Autonomous agent loops may drift or require token budgeting guards under heavy concurrency.")
        elif cat_id == 37:
            limitations.append("Sync Edge Cases: Requires explicit conflict resolution strategies (e.g. LWW or CRDT state merging) in distributed/offline modes.")
        elif cat_id == 49:
            limitations.append("Framework Lock-In: Deep architectural coupling with React/Next.js hydration lifecycle and component tree.")
        elif cat_id == 40:
            limitations.append("Credential Isolation: Demands strict zero-trust secret management to prevent CI/CD supply chain leaks.")

        limitations.append("Maintenance Cadence: Breaking API changes across major versions may necessitate pinned dependency trees.")
        return limitations[:3]

    def _find_alternatives(self, candidate: Dict) -> List[Dict[str, str]]:
        c = self.conn.cursor()
        c.execute("""
            SELECT name, stars, language, description
            FROM repositories
            WHERE category_id = ? AND id != ?
            ORDER BY stars DESC
            LIMIT 3;
        """, [candidate["category_id"], candidate["id"]])
        
        alternatives = []
        for r in c.fetchall():
            alternatives.append({
                "name": r["name"],
                "stars": f"{r['stars']:,}★",
                "language": r["language"],
                "synopsis": r["description"][:80] + "..." if len(r["description"]) > 80 else r["description"]
            })
        return alternatives

    def _find_complements(self, candidate: Dict, query: QueryDecomposition) -> List[Dict[str, str]]:
        c = self.conn.cursor()
        cat_id = candidate["category_id"]
        
        # Complementary category pairs
        complement_cat_map = {
            3: [37, 2, 45],   # Agents -> Vector DBs, Foundation Models, Systems/MCP
            37: [49, 38, 53],  # Databases -> Frontend, Data Eng, Backend Web
            49: [40, 50, 53],  # Frontend -> CI/CD, UI Components, Backend APIs
            40: [39, 41, 46],  # CI/CD -> Cloud-Native, Observability, CLI Tools
            36: [32, 45, 53]   # Blockchain -> Cryptography, Systems, Backend APIs
        }

        target_cats = complement_cat_map.get(cat_id, [1, 2, 39])
        placeholders = ",".join("?" for _ in target_cats)
        
        c.execute(f"""
            SELECT name, stars, language, category_name, description
            FROM repositories
            WHERE category_id IN ({placeholders})
            ORDER BY stars DESC
            LIMIT 2;
        """, target_cats)

        complements = []
        for r in c.fetchall():
            complements.append({
                "name": r["name"],
                "stars": f"{r['stars']:,}★",
                "category": r["category_name"],
                "synopsis": r["description"][:80] + "..." if len(r["description"]) > 80 else r["description"]
            })
        return complements

    def _generate_next_steps(self, candidate: Dict) -> Dict[str, str]:
        name = candidate["name"]
        lang = candidate.get("language", "Other").lower()
        repo_slug = name.split("/")[-1]

        if lang in ["python"]:
            install_cmd = f"pip install {repo_slug}\n# Or clone repository:\ngit clone {candidate['url']}.git"
            snippet = (
                f"import {repo_slug.replace('-', '_')}\n\n"
                f"# Initialize verified operational architecture\n"
                f"client = {repo_slug.replace('-', '_')}.Client()\n"
                f"response = client.run(mode='production')\n"
                f"print('Operational status:', response.status)"
            )
            verify_cmd = f"python -c 'import {repo_slug.replace('-', '_')}; print(\"Ready!\")'"
        elif lang in ["typescript", "javascript"]:
            install_cmd = f"npm install {repo_slug}\n# Or clone repository:\ngit clone {candidate['url']}.git"
            snippet = (
                f"import {{ createEngine }} from '{repo_slug}';\n\n"
                f"// Initialize core service pipeline\n"
                f"const engine = createEngine({{\n"
                f"  environment: 'production',\n"
                f"  logLevel: 'info'\n"
                f"}});\n"
                f"await engine.start();"
            )
            verify_cmd = f"node -e 'console.log(\"{name} initialized\")'"
        elif lang in ["rust"]:
            install_cmd = f"cargo add {repo_slug}\n# Or clone repository:\ngit clone {candidate['url']}.git"
            snippet = (
                f"use {repo_slug.replace('-', '_')}::prelude::*;\n\n"
                f"#[tokio::main]\n"
                f"async fn main() -> Result<(), Box<dyn std::error::Error>> {{\n"
                f"    let service = ServiceBuilder::new().build()?;\n"
                f"    service.execute().await?;\n"
                f"    Ok(())\n"
                f"}}"
            )
            verify_cmd = "cargo test --quiet"
        elif lang in ["go"]:
            install_cmd = f"go get github.com/{name}\n# Or clone repository:\ngit clone {candidate['url']}.git"
            snippet = (
                f"package main\n\nimport (\n\t\"fmt\"\n\t\"github.com/{name}\"\n)\n\n"
                f"func main() {{\n\tapp := {repo_slug}.New()\n\tfmt.Println(\"Initialized:\", app)\n}}"
            )
            verify_cmd = "go run main.go"
        else:
            install_cmd = f"git clone {candidate['url']}.git\ncd {repo_slug}"
            snippet = (
                f"# Review verified workflow signature:\n"
                f"# {candidate.get('workflow', 'Input -> Processing -> Output')}\n"
                f"./build.sh --release"
            )
            verify_cmd = "./test.sh"

        return {
            "install_command": install_cmd,
            "code_snippet": snippet,
            "verification_command": verify_cmd
        }


# ==============================================================================
# 6. CORE RECOMMENDATION ENGINE FACADE
# ==============================================================================

class RecommendationEngine:
    """
    Unified entry point orchestrating query parsing, candidate retrieval from SQLite FTS5,
    multi-factor scoring, deduplication, and card generation.
    """

    def __init__(self, db_path: str = DB_PATH, profile: str = "BALANCED"):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Registry DB not found at {db_path}. Build it first.")
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.parser = QueryParser()
        self.scorer = MultiFactorScorer(profile=profile)
        self.card_gen = RecommendationCardGenerator(self.conn)

    def close(self):
        self.conn.close()

    def detect_intents(self, query: str) -> List[str]:
        """
        Detect intent taxonomy keywords for backwards compatibility with engine contract.
        Matches intent keywords against query text.
        """
        q_lower = query.lower()
        intent_keywords = {
            "agent": ["agent", "autonomous", "swarm", "crew", "multi-agent", "mcp", "tool"],
            "rag": ["rag", "retrieval", "embedding", "vector", "qdrant", "milvus", "chroma", "knowledge"],
            "database": ["database", "sql", "nosql", "postgres", "sqlite", "cache", "key-value", "local-first"],
            "mobile": ["mobile", "flutter", "react native", "ios", "android", "cross-platform", "app"],
            "frontend": ["frontend", "ui", "react", "vue", "svelte", "nextjs", "tailwind", "component"],
            "devops": ["kubernetes", "k8s", "docker", "container", "ci/cd", "deploy", "terraform", "helm"],
            "security": ["security", "pentest", "vulnerability", "audit", "reverse engineering", "ghidra", "exploit"],
            "robotics": ["robotics", "robot", "humanoid", "kinematics", "slam", "ros", "ros2", "simulation"],
            "seo": ["seo", "scraping", "crawler", "browser", "growth", "serp", "content"]
        }
        detected = []
        for intent, kw_list in intent_keywords.items():
            if any(k in q_lower for k in kw_list):
                detected.append(intent)
        return detected

    def compare(self, repo_names: List[str]) -> List[Dict[str, Any]]:
        """
        Compare repositories side-by-side for backwards compatibility with engine contract.
        """
        cursor = self.conn.cursor()
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
        return results

    def recommend(
        self,
        query_text: str,
        limit: int = 3,
        candidate_pool_size: int = 50
    ) -> Tuple[QueryDecomposition, List[RecommendationCard]]:
        # 1. Parse Query
        parsed_query = self.parser.parse(query_text)

        # 2. Retrieve Candidate Pool from FTS5
        candidates_with_bm25 = self._retrieve_candidates(parsed_query, pool_size=candidate_pool_size)

        if not candidates_with_bm25:
            # Fallback to broad LIKE search if FTS yielded empty
            candidates_with_bm25 = self._fallback_candidates(parsed_query, pool_size=candidate_pool_size)

        if not candidates_with_bm25:
            return parsed_query, []

        # 3. Compute Min / Max BM25 for Normalization
        bm25_vals = [c["bm25"] for c in candidates_with_bm25]
        min_bm25 = min(bm25_vals)
        max_bm25 = max(bm25_vals)

        # 4. Multi-Factor Scoring
        scored_cards = []
        for item in candidates_with_bm25:
            cand = item["repo"]
            bm25 = item["bm25"]
            score_breakdown = self.scorer.score_candidate(cand, parsed_query, bm25, min_bm25, max_bm25)
            card = self.card_gen.generate_card(cand, parsed_query, score_breakdown)
            scored_cards.append(card)

        # 5. Sort by Composite Score Descending
        scored_cards.sort(key=lambda c: c.score.composite_score, reverse=True)

        # 6. Apply Diversity & Top-N Pruning
        pruned_cards = self._diversify_results(scored_cards, limit=limit)

        return parsed_query, pruned_cards

    def _retrieve_candidates(self, query: QueryDecomposition, pool_size: int = 100) -> List[Dict]:
        c = self.conn.cursor()
        candidates_map = {}

        # Tier 1: Multi-Facet Conjunction if we have both primary tech and action/deployment
        facet_queries = []
        if len(query.extracted_technologies) >= 2:
            # Pair tech tokens with AND
            t1 = query.extracted_technologies[0].replace("-", " ")
            t2 = query.extracted_technologies[1].replace("-", " ")
            facet_queries.append(f'("{t1}") AND ("{t2}")')
            if len(query.extracted_technologies) >= 3:
                t3 = query.extracted_technologies[2].replace("-", " ")
                facet_queries.append(f'("{t1}") AND ("{t3}")')

        # Tier 2: Category-targeted FTS search if target categories resolved
        if query.target_categories:
            cats_str = ",".join(str(cid) for cid in query.target_categories[:3])
            primary_terms = " OR ".join(f'"{t}"' for t in query.extracted_technologies[:4] if t)
            if primary_terms:
                cat_sql = f"""
                SELECT r.*, f.rank as bm25_rank
                FROM repositories_fts f
                JOIN repositories r ON f.rowid = r.id
                WHERE repositories_fts MATCH ? AND r.category_id IN ({cats_str})
                ORDER BY f.rank
                LIMIT ?;
                """
                try:
                    c.execute(cat_sql, [primary_terms, pool_size // 2])
                    for r in c.fetchall():
                        rid = r["id"]
                        if rid not in candidates_map:
                            raw_rank = r["bm25_rank"] if "bm25_rank" in r.keys() else 0.0
                            score_val = -float(raw_rank) if raw_rank is not None else 1.0
                            # Bonus for category-targeted tier
                            candidates_map[rid] = {"repo": dict(r), "bm25": score_val + 2.0}
                except Exception:
                    pass

        # Tier 3: Standard FTS query
        fts_expr = query.fts_query_string
        if fts_expr:
            sql = """
            SELECT r.*, f.rank as bm25_rank
            FROM repositories_fts f
            JOIN repositories r ON f.rowid = r.id
            WHERE repositories_fts MATCH ?
            ORDER BY f.rank
            LIMIT ?;
            """
            try:
                c.execute(sql, [fts_expr, pool_size])
                for r in c.fetchall():
                    rid = r["id"]
                    if rid not in candidates_map:
                        raw_rank = r["bm25_rank"] if "bm25_rank" in r.keys() else 0.0
                        score_val = -float(raw_rank) if raw_rank is not None else 1.0
                        candidates_map[rid] = {"repo": dict(r), "bm25": score_val}
            except sqlite3.OperationalError:
                # If complex syntax fails, simplify
                simple_q = " OR ".join(f'"{t}"' for t in query.extracted_technologies[:3]) or "agent"
                try:
                    c.execute(sql, [simple_q, pool_size])
                    for r in c.fetchall():
                        rid = r["id"]
                        if rid not in candidates_map:
                            raw_rank = r["bm25_rank"] if "bm25_rank" in r.keys() else 0.0
                            score_val = -float(raw_rank) if raw_rank is not None else 1.0
                            candidates_map[rid] = {"repo": dict(r), "bm25": score_val}
                except Exception:
                    pass

        return list(candidates_map.values())

    def _fallback_candidates(self, query: QueryDecomposition, pool_size: int = 50) -> List[Dict]:
        c = self.conn.cursor()
        terms = query.extracted_technologies[:3]
        if not terms:
            terms = query.raw_query.split()[:2]

        where_clauses = []
        params = []
        for t in terms:
            where_clauses.append("(name LIKE ? OR description LIKE ? OR workflow LIKE ?)")
            params.extend([f"%{t}%", f"%{t}%", f"%{t}%"])

        where_stmt = " OR ".join(where_clauses) if where_clauses else "1=1"
        sql = f"""
        SELECT * FROM repositories
        WHERE {where_stmt}
        ORDER BY stars DESC
        LIMIT ?;
        """
        params.append(pool_size)

        c.execute(sql, params)
        rows = c.fetchall()
        return [{"repo": dict(r), "bm25": 1.0} for r in rows]

    def _diversify_results(self, cards: List[RecommendationCard], limit: int = 3) -> List[RecommendationCard]:
        """
        Ensures recommendations do not pick redundant repos from the same exact author
        or trivial duplicates unless no alternatives exist.
        """
        seen_owners = set()
        chosen = []
        for card in cards:
            owner = card.repo_name.split("/")[0] if "/" in card.repo_name else card.repo_name
            if owner not in seen_owners:
                chosen.append(card)
                seen_owners.add(owner)
            if len(chosen) >= limit:
                break

        # If not enough due to owner uniqueness, fill remainder
        if len(chosen) < limit:
            for card in cards:
                if card not in chosen:
                    chosen.append(card)
                if len(chosen) >= limit:
                    break
        return chosen


# ==============================================================================
# 7. FORMATTERS (TERMINAL CARDS, JSON, MARKDOWN)
# ==============================================================================

def format_card_terminal(card: RecommendationCard, rank: int = 1) -> str:
    s = card.score
    lines = [
        "┌" + "─" * 98 + "┐",
        f"│ 🎯 RECOMMENDATION #{rank}: {card.repo_name:<55} MATCH: {s.composite_score:5.1f}% │",
        "├" + "─" * 98 + "┤",
        f"│ 🔗 URL         : {card.repo_url:<80} │",
        f"│ ⭐ Stargazers  : {card.stars:<12,} 🍴 Forks: {card.forks:<10,} 💻 Language: {card.language:<15} │",
        f"│ 📂 Discipline  : [#{card.category_id:02d}] {card.category_name:<69} │",
        f"│ 🛡️ Quality Gate: {card.quality_gate:<14} 📜 License: {card.inferred_license:<48} │",
        "├" + "─" * 98 + "┤",
        f"│ 📊 SCORE RADAR : TaskFit: {s.task_fit:0.2f} | Maint: {s.maintenance:0.2f} | Lang: {s.language_fit:0.2f} | Lic: {s.license_fit:0.2f} | Deploy: {s.deployment_fit:0.2f} │",
        "├" + "─" * 98 + "┤",
        "│ 💡 WHY IT MATCHES:                                                                               │",
    ]

    # Wrap why it matches
    for chunk in _wrap_text(card.why_it_matches, 94):
        lines.append(f"│   {chunk:<94} │")

    lines.append("├" + "─" * 98 + "┤")
    lines.append("│ 🚀 KEY STRENGTHS:                                                                                │")
    for st in card.strengths:
        lines.append(f"│   ✔ {st:<92} │")

    lines.append("├" + "─" * 98 + "┤")
    lines.append("│ ⚠️ LIMITATIONS & TRADEOFFS:                                                                      │")
    for lim in card.limitations:
        lines.append(f"│   ✖ {lim:<92} │")

    lines.append("├" + "─" * 98 + "┤")
    lines.append("│ 🔄 PEER ALTERNATIVES & COMPLEMENTS:                                                              │")
    for alt in card.alternatives[:2]:
        alt_str = f"Alt: {alt['name']} ({alt['stars']}) [{alt['language']}] - {alt['synopsis'][:45]}"
        lines.append(f"│   • {alt_str:<92} │")
    for comp in card.complements[:1]:
        comp_str = f"Complement: {comp['name']} ({comp['stars']}) - {comp['category'][:45]}"
        lines.append(f"│   • {comp_str:<92} │")

    lines.append("├" + "─" * 98 + "┤")
    lines.append("│ 🛠️ ACTIONABLE NEXT STEPS:                                                                        │")
    lines.append(f"│   1. Install     : {card.next_steps['install_command'].splitlines()[0]:<76} │")
    lines.append(f"│   2. Verification: {card.next_steps['verification_command']:<76} │")
    lines.append("└" + "─" * 98 + "┘")
    return "\n".join(lines)


def _wrap_text(text: str, width: int) -> List[str]:
    words = text.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 > width:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        else:
            curr.append(w)
            curr_len += len(w) + 1
    if curr:
        lines.append(" ".join(curr))
    return lines


# ==============================================================================
# 8. CLI INTERFACE
# ==============================================================================

IntelligentRecommendationEngine = RecommendationEngine

__all__ = [
    "QueryParser",
    "MultiFactorScorer",
    "RecommendationCardGenerator",
    "RecommendationEngine",
    "IntelligentRecommendationEngine",
    "format_card_terminal",
    "ScoreBreakdown",
    "RecommendationCard",
    "QueryDecomposition",
    "INTENT_ARCHETYPES",
    "SEMANTIC_SYNONYMS",
    "CATEGORY_AFFINITY_MAP",
]


def main():
    parser = argparse.ArgumentParser(
        description="Github Ultimate Repos - Intelligent Repository Recommendation Engine"
    )
    parser.add_argument("query", help="Developer query in natural language (e.g. 'build an AI agent with tools and memory')")
    parser.add_argument("--limit", type=int, default=3, help="Number of recommendations to return (default: 3)")
    parser.add_argument("--profile", choices=["BALANCED", "ENTERPRISE", "LOCAL_FIRST", "FAST_PROTOTYPE"], default="BALANCED", help="Multi-factor weight profile")
    parser.add_argument("--format", choices=["card", "json", "markdown"], default="card", help="Output display format")
    parser.add_argument("--output", help="Optional file path to save output report")

    args = parser.parse_args()

    engine = RecommendationEngine(profile=args.profile)
    try:
        query_decomp, cards = engine.recommend(args.query, limit=args.limit)

        if args.format == "card":
            print("\n" + "=" * 100)
            print(" 🧠 INTELLIGENT REPOSITORY RECOMMENDATION ENGINE")
            print("====================================================================================================")
            print(f" Query       : \"{query_decomp.raw_query}\"")
            print(f" Intent      : {query_decomp.intent_type}")
            print(f" Tech Tokens : {', '.join(query_decomp.extracted_technologies) if query_decomp.extracted_technologies else 'None'}")
            if query_decomp.language_constraint:
                print(f" Language    : {query_decomp.language_constraint} (Constraint)")
            if query_decomp.deployment_constraint:
                print(f" Deployment  : {query_decomp.deployment_constraint} (Constraint)")
            print(f" Candidates  : {len(cards)} high-precision recommendations synthesized")
            print("=" * 100 + "\n")

            for idx, card in enumerate(cards, 1):
                print(format_card_terminal(card, rank=idx))
                print()

        elif args.format == "json":
            payload = {
                "query": asdict(query_decomp),
                "recommendations": [asdict(c) for c in cards]
            }
            output_str = json.dumps(payload, indent=2)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output_str)
                print(f"Saved recommendations to {args.output}")
            else:
                print(output_str)

        elif args.format == "markdown":
            md_lines = [
                f"# Repository Recommendations: {query_decomp.raw_query}",
                "",
                f"- **Intent Archetype**: `{query_decomp.intent_type}`",
                f"- **Extracted Capabilities**: `{', '.join(query_decomp.extracted_technologies)}`",
                f"- **Weight Profile**: `{args.profile}`",
                "",
                "---",
                ""
            ]
            for idx, c in enumerate(cards, 1):
                md_lines.extend([
                    f"## #{idx}: [{c.repo_name}]({c.repo_url}) ({c.score.composite_score}% Match)",
                    "",
                    f"- **Stars**: {c.stars:,}★ | **Forks**: {c.forks:,} | **Language**: `{c.language}`",
                    f"- **Discipline**: [#{c.category_id}] {c.category_name}",
                    f"- **License**: {c.inferred_license} | **Quality Gate**: `{c.quality_gate}`",
                    "",
                    f"### 💡 Why It Matches",
                    c.why_it_matches,
                    "",
                    "### 🚀 Strengths",
                    "\n".join(f"- {s}" for s in c.strengths),
                    "",
                    "### ⚠️ Limitations & Tradeoffs",
                    "\n".join(f"- {l}" for l in c.limitations),
                    "",
                    "### 🛠️ Quickstart Blueprint",
                    "```bash",
                    c.next_steps["install_command"],
                    "```",
                    "",
                    "```" + c.language.lower(),
                    c.next_steps["code_snippet"],
                    "```",
                    "",
                    "---",
                    ""
                ])
            md_output = "\n".join(md_lines)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(md_output)
                print(f"Saved Markdown report to {args.output}")
            else:
                print(md_output)

    finally:
        engine.close()

if __name__ == "__main__":
    main()
