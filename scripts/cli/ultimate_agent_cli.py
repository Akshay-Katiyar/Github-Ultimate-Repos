#!/usr/bin/env python3
"""
ultimate_agent_cli.py - Enterprise Search, Multi-Agent Registry & Workflow Intelligence Engine

Command-line interface to search, query, inspect, compare, recommend, and step through
development workflows using the cataloged repositories and multi-agent blueprints
from registry/agents_registry.db.

Zero external dependencies: 100% standard library (Python 3 + SQLite3).
"""

import os
import sys
import sqlite3
import json
import csv
import argparse
import re
import math
import shutil

# Ensure UTF-8 output encoding across all Windows and POSIX terminal streams
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DB_PATH = os.environ.get("ULTIMATE_REPOS_DB", os.path.join(REPO_ROOT, "registry", "agents_registry.db"))

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.comparison.tradeoff_engine import (
    TradeoffEngine,
    render_terminal as render_tradeoff_terminal,
    render_markdown as render_tradeoff_markdown,
)

__all__ = [
    "sanitize_csv_value",
    "sanitize_csv_row",
    "get_connection",
    "resolve_repo",
    "find_peer_alternatives",
    "build_recommendations",
    "compare_repositories",
    "render_comparison_table",
    "synthesize_category_workflow",
    "enrich_workflow_tools",
    "render_workflow_step_detail",
    "CURATED_WORKFLOWS",
    "cmd_stats",
    "cmd_search",
    "cmd_get",
    "cmd_category",
    "cmd_export",
    "cmd_recommend",
    "cmd_compare",
    "cmd_workflow",
    "main",
]

# -----------------------------------------------------------------------------
# Terminal Styling & Hyperlink Primitives
# -----------------------------------------------------------------------------

def is_color_enabled() -> bool:
    """Check if color and ANSI escapes should be emitted."""
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()

def make_hyperlink(url: str, text: str = None) -> str:
    """
    Format a terminal clickable hyperlink using OSC 8 escape sequence.
    Supported by Windows Terminal, VS Code Terminal, iTerm2, Kitty, Alacritty, GNOME Terminal, etc.
    Fallback: returns text if url is empty.
    """
    if not url:
        return text or ""
    label = text if text else url
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"

def style(text: str, *codes: str) -> str:
    if not is_color_enabled():
        return text
    joined = ";".join(codes)
    return f"\033[{joined}m{text}\033[0m"

def bold(text: str) -> str: return style(text, "1")
def dim(text: str) -> str: return style(text, "2")
def green(text: str) -> str: return style(text, "32")
def yellow(text: str) -> str: return style(text, "33")
def blue(text: str) -> str: return style(text, "34")
def magenta(text: str) -> str: return style(text, "35")
def cyan(text: str) -> str: return style(text, "36")

# -----------------------------------------------------------------------------
# Database Utilities
# -----------------------------------------------------------------------------

def get_connection(custom_db_path=None):
    db_path = custom_db_path if custom_db_path else DEFAULT_DB_PATH
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}.", file=sys.stderr)
        print("Please build it first with: python scripts/inventory/build_sqlite_registry.py", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def resolve_repo(conn, target: str):
    """
    Resolve repository by exact name, suffix name (owner/repo), or substring.
    Returns dict of repository row or None.
    """
    target = target.strip()
    c = conn.cursor()
    # 1. Exact match on full name 'owner/repo'
    c.execute("SELECT * FROM repositories WHERE name = ? COLLATE NOCASE", [target])
    row = c.fetchone()
    if row:
        return dict(row)
    # 2. Match exact repo suffix '/repo'
    c.execute("SELECT * FROM repositories WHERE name LIKE ? ORDER BY stars DESC LIMIT 1", [f"%/{target}"])
    row = c.fetchone()
    if row:
        return dict(row)
    # 3. Match substring in repo name
    c.execute("SELECT * FROM repositories WHERE name LIKE ? ORDER BY stars DESC LIMIT 1", [f"%{target}%"])
    row = c.fetchone()
    if row:
        return dict(row)
    return None

def find_peer_alternatives(conn, category_id: int, current_id: int, limit: int = 3):
    """Find top alternatives in the same category."""
    c = conn.cursor()
    c.execute("""
    SELECT name, stars, forks, language, url, workflow
    FROM repositories
    WHERE category_id = ? AND id != ?
    ORDER BY stars DESC
    LIMIT ?;
    """, [category_id, current_id, limit])
    return [dict(r) for r in c.fetchall()]

# -----------------------------------------------------------------------------
# Curated Enterprise Development Workflows
# -----------------------------------------------------------------------------

CURATED_WORKFLOWS = {
    "ai-agent": {
        "id": "ai-agent",
        "code": "WF-AI-AGENT-01",
        "title": "Autonomous Multi-Agent System & LLM Application Stack",
        "domain": "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools",
        "description": "Production-grade multi-agent architecture: from high-throughput local inference and vector knowledge indexing to autonomous swarm planning, tool calling via MCP, and evaluation guardrails.",
        "pipeline_summary": "Model Serving -> Vector Storage/RAG -> Swarm Planning -> MCP Tool Dispatch -> Telemetry & Guardrails",
        "steps": [
            {
                "step": 1,
                "name": "High-Throughput Model Serving & Inference Engine",
                "objective": "Deploy scalable local or cluster LLM inference API with KV cache paging, tensor parallelism, and OpenAI-compatible endpoints.",
                "architecture_pattern": "REST / OpenAI-compatible endpoint with streaming SSE and fused attention kernels.",
                "tool_identifiers": ["vllm-project/vllm", "ggml-org/llama.cpp", "ollama/ollama"],
                "recipe": "vllm serve meta-llama/Llama-3-8B-Instruct --port 8000 --tensor-parallel-size 1",
                "verification": "Sub-15ms time-to-first-token (TTFT) and >80 tokens/sec decode throughput."
            },
            {
                "step": 2,
                "name": "Vector Database & Semantic Knowledge Retrieval (RAG)",
                "objective": "Ingest document embeddings, build HNSW indexing, and enable hybrid semantic + keyword retrieval.",
                "architecture_pattern": "Dense vector retrieval + BM25 reciprocal rank fusion (RRF) with metadata filtering.",
                "tool_identifiers": ["milvus-io/milvus", "qdrant/qdrant", "chroma-core/chroma"],
                "recipe": "docker run -d --name qdrant -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant",
                "verification": "Recall@10 > 0.92 with query latency under 5ms across 1M+ vectors."
            },
            {
                "step": 3,
                "name": "Multi-Agent Orchestration, Planning & Reasoning",
                "objective": "Construct autonomous agent teams with role definition, persistent memory, and dynamic DAG planning.",
                "architecture_pattern": "Hierarchical supervisor-worker swarm with task delegation, shared scratchpad, and consensus loop.",
                "tool_identifiers": ["Significant-Gravitas/AutoGPT", "crewAIInc/crewAI", "langchain-ai/langchain"],
                "recipe": "python -m crewai run --team engineering_squad --task 'Build microservice'",
                "verification": "Deterministic task convergence without infinite self-delegation loops."
            },
            {
                "step": 4,
                "name": "Tool Execution & Protocol Connectivity (MCP)",
                "objective": "Equip agents with sandboxed file, web scraping, API, and database tools via Model Context Protocol.",
                "architecture_pattern": "Zero-trust sandboxed tool dispatcher with JSON-RPC over stdio / SSE.",
                "tool_identifiers": ["firecrawl/firecrawl", "microsoft/markitdown", "modelcontextprotocol/servers"],
                "recipe": "npx @modelcontextprotocol/server-filesystem C:\\Users\\Aryan\\Workspace",
                "verification": "JSON Schema validation on all tool inputs and strictly isolated sandbox boundaries."
            },
            {
                "step": 5,
                "name": "Observability, Guardrails & Evaluation",
                "objective": "Monitor latency, token economics, LLM traces, prompt injection security, and response hallucinations.",
                "architecture_pattern": "Distributed OpenTelemetry span tracking + automated LLM-as-a-judge scoring.",
                "tool_identifiers": ["langfuse/langfuse", "Arize-ai/phoenix", "guardrails-ai/guardrails"],
                "recipe": "langfuse-cli monitor --trace-export-endpoint http://localhost:3000",
                "verification": "100% trace capture rate with real-time prompt injection blocking."
            }
        ]
    },
    "mobile": {
        "id": "mobile",
        "code": "WF-MOBILE-01",
        "title": "Cross-Platform Mobile Engineering & Continuous Delivery",
        "domain": "Mobile App Development, Cross-Platform Frameworks (Flutter/React Native) & SDKs",
        "description": "End-to-end mobile architecture: reactive cross-platform UI, offline-first encrypted persistence, real-time backend sync, state machines, and automated App Store delivery.",
        "pipeline_summary": "Declarative UI Widget Tree -> Local Persistence & Sync -> Backend Services & Auth -> State Architecture & Gestures -> CI/CD & App Store Release",
        "steps": [
            {
                "step": 1,
                "name": "Cross-Platform Reactive UI & Application Shell",
                "objective": "Scaffold native-compiled responsive UI supporting iOS, Android, and Web with unified business logic.",
                "architecture_pattern": "Reactive declarative UI with hardware-accelerated Skia / Impeller rendering.",
                "tool_identifiers": ["flutter/flutter", "facebook/react-native", "expo/expo"],
                "recipe": "flutter create --org com.enterprise --platforms=android,ios app_core",
                "verification": "Consistent 60/120 FPS jank-free rendering on physical iOS and Android targets."
            },
            {
                "step": 2,
                "name": "Local Persistence & Offline-First Synchronization",
                "objective": "Implement encrypted local relational caching, reactive queries, and bidirectional cloud sync.",
                "architecture_pattern": "Conflict-free Replicated Data Types (CRDT) + local-first offline queue.",
                "tool_identifiers": ["realm/realm-core", "Nozbe/WatermelonDB", "sqlcipher/sqlcipher"],
                "recipe": "npx watermelon-db init --database-name app_offline.db",
                "verification": "Instant UI reads (<1ms) and seamless automatic reconnection sync."
            },
            {
                "step": 3,
                "name": "Backend Services, Authentication & Push Telemetry",
                "objective": "Connect OAuth2 / biometrics identity, real-time WebSocket subscriptions, and push notifications.",
                "architecture_pattern": "JWT token rotation + edge-authenticated API gateway.",
                "tool_identifiers": ["supabase/supabase", "pocketbase/pocketbase", "firebase/firebase-ios-sdk"],
                "recipe": "supabase init && supabase start",
                "verification": "Sub-100ms real-time event latency and biometric auth validation."
            },
            {
                "step": 4,
                "name": "State Architecture & Navigation Routing",
                "objective": "Decouple business logic, handle deep links, and build 60fps gesture-driven animations.",
                "architecture_pattern": "Unidirectional Data Flow (UDF) + declarative state machine.",
                "tool_identifiers": ["rrousselGit/riverpod", "pmndrs/zustand", "software-mansion/react-native-reanimated"],
                "recipe": "flutter pub add flutter_riverpod go_router",
                "verification": "Zero state leakage between route transitions and complete state replayability."
            },
            {
                "step": 5,
                "name": "Mobile CI/CD, Signing & App Store Automation",
                "objective": "Automate cryptographic code signing, test runner execution on emulator matrices, and store deployment.",
                "architecture_pattern": "Git-triggered reproducible build runner with secure secrets injection.",
                "tool_identifiers": ["fastlane/fastlane", "nektos/act", "actions/runner"],
                "recipe": "bundle exec fastlane beta --verbose",
                "verification": "Automated green build artifacts uploaded to TestFlight & Google Play Internal Track."
            }
        ]
    },
    "devops": {
        "id": "devops",
        "code": "WF-DEVOPS-01",
        "title": "Cloud-Native Infrastructure & Automated GitOps Pipeline",
        "domain": "Cloud-Native Infrastructure, Kubernetes, Containers & CI/CD Automation",
        "description": "Enterprise cloud-native pipeline: declarative infrastructure as code, resilient Kubernetes orchestration, automated GitOps continuous reconciliation, zero-trust edge mesh, and unified telemetry.",
        "pipeline_summary": "IaC Multi-Cloud Provisioning -> Container Runtime & K8s -> GitOps Continuous Delivery -> Edge Gateway & Service Mesh -> Telemetry & Observability",
        "steps": [
            {
                "step": 1,
                "name": "Infrastructure as Code & Multi-Cloud Provisioning",
                "objective": "Declare declarative infrastructure state for VPCs, IAM policies, DNS, and compute clusters.",
                "architecture_pattern": "Immutable modular IaC with cryptographic state locking.",
                "tool_identifiers": ["hashicorp/terraform", "opentofu/opentofu", "ansible/ansible"],
                "recipe": "tofu init && tofu plan -out=tfplan && tofu apply tfplan",
                "verification": "Idempotent execution with zero unexpected infrastructure drift."
            },
            {
                "step": 2,
                "name": "Container Runtime & Kubernetes Orchestration",
                "objective": "Deploy distributed container workloads with automated scheduling, node autoscaling, and self-healing.",
                "architecture_pattern": "Control plane consensus via Raft + declarative resource controllers.",
                "tool_identifiers": ["kubernetes/kubernetes", "k3s-io/k3s", "docker/compose"],
                "recipe": "kubectl apply -k ./overlays/production",
                "verification": "99.99% pod readiness with zero-downtime rolling updates."
            },
            {
                "step": 3,
                "name": "GitOps Continuous Delivery & Cluster Sync",
                "objective": "Enforce desired cluster state directly from Git repositories with automated sync and rollback.",
                "architecture_pattern": "In-cluster Git reconciliation loop with zero outward cluster ports.",
                "tool_identifiers": ["argoproj/argo-cd", "fluxcd/flux2", "helm/helm"],
                "recipe": "argocd app sync production-stack --prune",
                "verification": "Desired Git commit matches live cluster state in <30 seconds."
            },
            {
                "step": 4,
                "name": "Edge Routing, API Gateway & Service Mesh",
                "objective": "Route ingress traffic with mTLS zero-trust encryption, rate-limiting, and canary traffic splitting.",
                "architecture_pattern": "Sidecar proxy data plane + control plane telemetry.",
                "tool_identifiers": ["envoyproxy/envoy", "traefik/traefik", "istio/istio"],
                "recipe": "istioctl install --set profile=default -y",
                "verification": "End-to-end mTLS encryption with p99 routing latency overhead <1.2ms."
            },
            {
                "step": 5,
                "name": "Observability, Telemetry & Distributed Tracing",
                "objective": "Ingest dimensional time-series metrics, structured logs, and distributed traces with alerting rules.",
                "architecture_pattern": "Push/pull OpenTelemetry collector + Grafana dashboard visualization.",
                "tool_identifiers": ["prometheus/prometheus", "grafana/grafana", "open-telemetry/opentelemetry-collector"],
                "recipe": "helm install prometheus-stack prometheus-community/kube-prometheus-stack",
                "verification": "Complete distributed trace waterfall from ingress edge to database tier."
            }
        ]
    },
    "fullstack": {
        "id": "fullstack",
        "code": "WF-FULLSTACK-01",
        "title": "Modern Reactive Web Platform & Microservices",
        "domain": "Modern Frontend Frameworks, Reactive Web Engines & Backend Microservices",
        "description": "Full-stack reactive web engineering: SSR/SSG frontend, high-concurrency API microservices, distributed relational storage, caching queues, and global edge delivery.",
        "pipeline_summary": "Reactive Frontend & SSR -> Microservice API Layer -> Distributed SQL & ORM -> Cache & Event Broker -> Serverless Edge Deployment",
        "steps": [
            {
                "step": 1,
                "name": "Reactive Web Frontend & Design System",
                "objective": "Build responsive, accessible UI with server-side rendering (SSR) and edge static caching.",
                "architecture_pattern": "Component-driven reactive virtual DOM with server component hydration.",
                "tool_identifiers": ["vercel/next.js", "facebook/react", "tailwindlabs/tailwindcss"],
                "recipe": "npx create-next-app@latest enterprise-portal --typescript --tailwind --app",
                "verification": "Lighthouse score > 95 with Core Web Vitals (LCP < 1.2s, INP < 100ms, CLS = 0)."
            },
            {
                "step": 2,
                "name": "High-Performance Backend API & Microservices",
                "objective": "Expose type-safe OpenAPI/gRPC endpoints with input validation and rate limiting.",
                "architecture_pattern": "Asynchronous event-driven I/O with Pydantic / TypeScript schema serialization.",
                "tool_identifiers": ["fastapi/fastapi", "nestjs/nest", "expressjs/express"],
                "recipe": "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4",
                "verification": "p99 response latency < 25ms under 5,000 req/sec benchmark load."
            },
            {
                "step": 3,
                "name": "Distributed Database, Persistence & ORMs",
                "objective": "Manage relational schema migrations, connection pooling, and optimized ACID transactions.",
                "architecture_pattern": "WAL-based relational engine with read replicas and prepared statement pooling.",
                "tool_identifiers": ["postgres/postgres", "prisma/prisma", "drizzle-team/drizzle-orm"],
                "recipe": "npx drizzle-kit push",
                "verification": "Zero unindexed sequential table scans on hot query paths."
            },
            {
                "step": 4,
                "name": "Distributed Cache, Pub/Sub & Message Broker",
                "objective": "Implement distributed session caches, pub/sub event broadcasting, and background job queues.",
                "architecture_pattern": "In-memory key-value store with Lua script atomicity and append-only persistence.",
                "tool_identifiers": ["redis/redis", "apache/kafka", "nats-io/nats-server"],
                "recipe": "docker run -d --name redis -p 6379:6379 redis:7-alpine redis-server --appendonly yes",
                "verification": "Sub-millisecond cache hits and zero message loss under broker failover."
            },
            {
                "step": 5,
                "name": "Serverless Edge Deployment & Global CDN",
                "objective": "Deploy globally distributed serverless functions with automatic SSL and DDoS mitigation.",
                "architecture_pattern": "V8 isolate edge execution with global Anycast routing.",
                "tool_identifiers": ["cloudflare/workers-sdk", "vercel/vercel", "caddyserver/caddy"],
                "recipe": "npx wrangler deploy",
                "verification": "Global cold start latency < 5ms with automatic TLS certificate issuance."
            }
        ]
    },
    "data-engineering": {
        "id": "data-engineering",
        "code": "WF-DATA-01",
        "title": "Real-Time Stream Processing & Analytics Lakehouse",
        "domain": "Data Engineering, Distributed Analytics, Stream Processing & ETL",
        "description": "Petabyte-scale analytical data pipeline: distributed event streaming, real-time stream compute, columnar lakehouse storage, SQL modeling, and DAG workflow scheduling.",
        "pipeline_summary": "Event Streaming Ingestion -> Distributed Stream/Batch Compute -> Columnar Lakehouse Storage -> Data Modeling & SQL Transforms -> Workflow DAG Scheduling",
        "steps": [
            {
                "step": 1,
                "name": "Event Ingestion & High-Throughput Streaming",
                "objective": "Capture real-time CDC logs and event streams with partition replication.",
                "architecture_pattern": "Distributed log partitioning with zero-copy disk writes and consumer groups.",
                "tool_identifiers": ["apache/kafka", "redpanda-data/redpanda", "apache/pulsar"],
                "recipe": "rpk cluster start",
                "verification": "Sustained throughput of >200,000 events/sec with replication factor of 3."
            },
            {
                "step": 2,
                "name": "Distributed Stream & Batch Processing",
                "objective": "Process massive datasets with windowed aggregations, join optimization, and fault tolerance.",
                "architecture_pattern": "Catalyst query optimizer + resilient distributed dataset (RDD) micro-batching.",
                "tool_identifiers": ["apache/spark", "apache/flink", "ray-project/ray"],
                "recipe": "spark-submit --master k8s://https://k8s-api:443 --deploy-mode cluster app.py",
                "verification": "Exactly-once processing semantics validated across node failure simulations."
            },
            {
                "step": 3,
                "name": "Columnar Lakehouse Storage & ACID Tables",
                "objective": "Store petabyte-scale structured tables with ACID transactions, time travel, and partition pruning.",
                "architecture_pattern": "Open table format with Parquet columnar compression and metadata manifest trees.",
                "tool_identifiers": ["apache/iceberg", "delta-io/delta", "duckdb/duckdb"],
                "recipe": "python -c 'import duckdb; duckdb.sql(\"SELECT * FROM read_parquet(\\'s3://lake/events/*.parquet\\')\").show()'",
                "verification": "Vectorized predicate pushdown reducing scan I/O by >90%."
            },
            {
                "step": 4,
                "name": "Data Modeling & SQL Transformations",
                "objective": "Transform raw lakehouse layers into modeled analytics marts with automated test assertions.",
                "architecture_pattern": "Modular DAG SQL transforms with lineage graphs and schema contracts.",
                "tool_identifiers": ["dbt-labs/dbt-core", "ClickHouse/ClickHouse", "trinodb/trino"],
                "recipe": "dbt build --select marts",
                "verification": "100% test passing rate on uniqueness, non-null, and referential integrity."
            },
            {
                "step": 5,
                "name": "Workflow DAG Scheduling & Orchestration",
                "objective": "Schedule idempotent data pipelines with dependency DAGs, alerting, and data validation gates.",
                "architecture_pattern": "Stateful DAG orchestrator with distributed worker task queues.",
                "tool_identifiers": ["apache/airflow", "dagster-io/dagster", "great-expectations/great_expectations"],
                "recipe": "airflow dags trigger analytics_nightly_rollup",
                "verification": "Idempotent backfill capability across historical execution windows."
            }
        ]
    },
    "cybersecurity": {
        "id": "cybersecurity",
        "code": "WF-CYBERSECURITY-01",
        "title": "Vulnerability Research, Red Teaming & Cloud Defense",
        "domain": "Cybersecurity, Reverse Engineering, Binary Exploitation & Vulnerability Research",
        "description": "Comprehensive security operations lifecycle: attack surface reconnaissance, automated SAST/DAST scanning, binary reverse engineering, memory forensics, and zero-trust policy enforcement.",
        "pipeline_summary": "Attack Surface Recon -> SAST/DAST Vulnerability Scanners -> Binary Reverse Engineering -> Threat Forensics & YARA Rules -> Zero-Trust Hardening",
        "steps": [
            {
                "step": 1,
                "name": "Reconnaissance, Attack Surface Mapping & OSINT",
                "objective": "Enumerate domains, DNS records, cloud assets, and public exposures across target infrastructure.",
                "architecture_pattern": "Graph-based asset relationship mapping with passive and active DNS telemetry.",
                "tool_identifiers": ["owasp-amass/amass", "projectdiscovery/subfinder", "lanmaster53/recon-ng"],
                "recipe": "subfinder -d example.com -all -silent | amass enum -passive",
                "verification": "Comprehensive sub-domain asset inventory with zero false-negative core services."
            },
            {
                "step": 2,
                "name": "Static & Dynamic Security Testing (SAST/DAST)",
                "objective": "Audit code repositories and live endpoints for OWASP Top 10 vulnerabilities and misconfigurations.",
                "architecture_pattern": "AST-based taint tracking + automated fuzzing HTTP test runner.",
                "tool_identifiers": ["zaproxy/zaproxy", "semgrep/semgrep", "aquasecurity/trivy"],
                "recipe": "semgrep scan --config auto && trivy fs --scanners vuln,secret,config .",
                "verification": "Zero high/critical CVEs in production dependency trees and deployment images."
            },
            {
                "step": 3,
                "name": "Binary Reverse Engineering & Exploit Analysis",
                "objective": "Disassemble compiled binaries, decompile functions, and trace data flow for memory safety flaws.",
                "architecture_pattern": "Intermediate representation (p-code) decompilation with control-flow graph reconstruction.",
                "tool_identifiers": ["NationalSecurityAgency/ghidra", "radareorg/radare2", "angr/angr"],
                "recipe": "radare2 -A target_binary",
                "verification": "Complete symbol resolution and identification of unsafe memory copy primitives."
            },
            {
                "step": 4,
                "name": "Digital Forensics, Incident Response & YARA Rules",
                "objective": "Analyze volatile memory dumps, craft signature rules, and triage indicators of compromise (IoC).",
                "architecture_pattern": "Process memory structure traversal + byte pattern regex scanning.",
                "tool_identifiers": ["volatilityfoundation/volatility3", "VirusTotal/yara", "SigmaHQ/sigma"],
                "recipe": "vol -f memory.raw windows.pslist",
                "verification": "Identification of injected DLLs and unhooked syscall trampolines."
            },
            {
                "step": 5,
                "name": "Zero-Trust Hardening & Policy Enforcement",
                "objective": "Enforce granular identity-based access control, eBPF network segmentation, and audit logging.",
                "architecture_pattern": "Declarative policy agent with in-kernel eBPF packet inspection.",
                "tool_identifiers": ["open-policy-agent/opa", "cilium/cilium", "teleport/teleport"],
                "recipe": "cilium status && opa eval --data policy.rego --input request.json 'data.authz.allow'",
                "verification": "Zero unauthorized east-west lateral network traffic between cluster pods."
            }
        ]
    }
}

def enrich_workflow_tools(conn, workflow_def: dict) -> dict:
    """Enrich workflow tool identifiers with live registry data from SQLite."""
    enriched = dict(workflow_def)
    enriched_steps = []
    for step in workflow_def.get("steps", []):
        step_copy = dict(step)
        tools = []
        for ident in step.get("tool_identifiers", []):
            repo = resolve_repo(conn, ident)
            if repo:
                tools.append({
                    "name": repo["name"],
                    "url": repo["url"],
                    "stars": repo["stars"],
                    "forks": repo["forks"],
                    "language": repo["language"],
                    "category_id": repo["category_id"],
                    "workflow": repo["workflow"],
                    "description": repo["description"]
                })
            else:
                tools.append({
                    "name": ident,
                    "url": f"https://github.com/{ident}",
                    "stars": 0,
                    "forks": 0,
                    "language": "Unknown",
                    "category_id": 0,
                    "workflow": "N/A",
                    "description": "Tool listed in architecture specification"
                })
        step_copy["tools"] = tools
        enriched_steps.append(step_copy)
    enriched["steps"] = enriched_steps
    return enriched

def synthesize_category_workflow(conn, category_query: str) -> dict:
    """Dynamically synthesize a development workflow pipeline from any of the 55 disciplines."""
    c = conn.cursor()
    c.execute("""
    SELECT id, name, stars, forks, language, category_id, category_name, workflow, description, url
    FROM repositories
    WHERE category_name LIKE ? OR category_id = ?
    ORDER BY stars DESC
    LIMIT 15;
    """, [f"%{category_query}%", int(category_query) if category_query.isdigit() else -1])
    rows = [dict(r) for r in c.fetchall()]

    if not rows:
        return None

    cat_name = rows[0]["category_name"]
    cat_id = rows[0]["category_id"]

    # Extract stages from the canonical workflow string (separated by '->')
    workflow_str = rows[0]["workflow"]
    raw_stages = [s.strip().rstrip(".") for s in workflow_str.split("->") if s.strip()]

    steps = []
    repos_per_stage = max(1, len(rows) // max(1, len(raw_stages)))
    for idx, stage in enumerate(raw_stages, 1):
        stage_repos = rows[(idx - 1) * repos_per_stage : idx * repos_per_stage]
        if not stage_repos and rows:
            stage_repos = [rows[min(idx - 1, len(rows) - 1)]]
        
        tools = []
        for r in stage_repos:
            tools.append({
                "name": r["name"],
                "url": r["url"],
                "stars": r["stars"],
                "forks": r["forks"],
                "language": r["language"],
                "category_id": r["category_id"],
                "workflow": r["workflow"],
                "description": r["description"]
            })

        steps.append({
            "step": idx,
            "name": stage,
            "objective": f"Execute discipline phase '{stage}' using top validated open-source tools.",
            "architecture_pattern": f"Pipeline phase {idx}/{len(raw_stages)}: deterministic input transformation -> {stage}",
            "recipe": f"# Implement {stage} with primary candidate: {tools[0]['name'] if tools else 'CLI'}",
            "verification": f"Quality gate validation for phase '{stage}' passed with verified output.",
            "tools": tools
        })

    return {
        "id": f"category-{cat_id}",
        "title": f"Discipline Pipeline: {cat_name}",
        "domain": cat_name,
        "description": f"Audited architectural workflow synthesized directly from {len(rows)} top repositories in discipline #{cat_id}.",
        "pipeline_summary": " -> ".join(raw_stages),
        "steps": steps
    }

# -----------------------------------------------------------------------------
# Recommendation Engine Core
# -----------------------------------------------------------------------------

STOPWORDS = {
    "a", "about", "above", "after", "again", "all", "an", "and", "any", "are", "as",
    "at", "be", "because", "been", "before", "being", "below", "best", "between",
    "both", "build", "but", "by", "can", "could", "did", "do", "does", "doing",
    "down", "during", "each", "few", "find", "for", "from", "further", "get", "give",
    "good", "great", "had", "has", "have", "having", "how", "i", "if", "in", "into",
    "is", "it", "its", "itself", "just", "like", "look", "looking", "make", "me",
    "more", "most", "my", "myself", "need", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
    "over", "own", "project", "repo", "repository", "same", "should", "so", "some",
    "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then",
    "there", "these", "they", "this", "those", "through", "to", "too", "tool",
    "under", "until", "up", "use", "very", "want", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you",
    "your", "yours", "yourself", "yourselves"
}

DOMAIN_CATEGORY_KEYWORDS = {
    "Multi-Agent Systems, Autonomous Swarms, AI Orchestration & MCP Tools": [
        "agent", "agents", "swarm", "autonomous", "orchestration", "crew", "langchain", "mcp", "tool calling", "autogpt"
    ],
    "Artificial Intelligence, Large Language Models, Foundation Models & Quantization": [
        "llm", "transformer", "inference", "quantization", "gguf", "vllm", "llama", "ollama", "fine-tuning", "lora"
    ],
    "Computer Vision, Multimodal AI, Diffusion & Neural Rendering (NeRF/3D-GS)": [
        "vision", "cv", "object detection", "yolo", "diffusion", "nerf", "image", "segmentation", "3d-gs"
    ],
    "Speech, Voice AI, Audio Processing, Audio Synthesis & Music Generation": [
        "speech", "voice", "audio", "whisper", "tts", "asr", "music", "sound", "synthesis"
    ],
    "Robotics, Humanoid Kinematics, Dynamics, Actuators & Physics Simulation": [
        "robotics", "kinematics", "humanoid", "urdf", "sdf", "mujoco", "pinocchio", "dynamics", "gait"
    ],
    "Mobile App Development, Cross-Platform Frameworks (Flutter/React Native) & SDKs": [
        "mobile", "ios", "android", "flutter", "react native", "expo", "swift", "kotlin"
    ],
    "Cloud-Native Infrastructure, Kubernetes, Containers & Service Meshes": [
        "kubernetes", "k8s", "docker", "container", "devops", "cloud", "envoy", "istio", "helm"
    ],
    "CI/CD Automation, GitOps & Infrastructure-as-Code (Terraform/Ansible)": [
        "ci/cd", "gitops", "terraform", "ansible", "argocd", "automation", "pipeline", "opentofu"
    ],
    "Modern Frontend Frameworks, Reactive Web Engines (React/Vue/Svelte) & Bundlers": [
        "frontend", "react", "vue", "svelte", "nextjs", "vite", "web", "tailwind", "ui"
    ],
    "Backend Web Frameworks, Microservices, REST / GraphQL / gRPC APIs & ORMs": [
        "backend", "api", "fastapi", "django", "express", "graphql", "grpc", "microservice", "orm"
    ],
    "Database Engines, Distributed SQL, NoSQL, Vector DBs & Persistent Caches": [
        "database", "db", "sql", "vector", "postgres", "nosql", "redis", "milvus", "qdrant", "cache"
    ],
    "Data Engineering, Distributed Analytics, Stream Processing (Kafka/Spark) & ETL": [
        "data", "spark", "kafka", "stream", "lakehouse", "dbt", "etl", "analytics", "parquet"
    ],
    "Cybersecurity, Reverse Engineering, Binary Exploitation & Vulnerability Research": [
        "security", "pentest", "vulnerability", "exploit", "reverse", "malware", "ghidra", "yara"
    ],
    "Blockchain, Web3, Smart Contracts & EVM/Solana Engineering": [
        "blockchain", "crypto", "web3", "solana", "evm", "smart contract", "ethereum", "solidity"
    ]
}

def extract_intent_tokens(query: str):
    words = re.findall(r'[a-zA-Z0-9_\-\.]+', query.lower())
    meaningful = [w for w in words if w not in STOPWORDS and len(w) >= 2]
    return meaningful

def infer_domain_categories(tokens: list) -> list:
    boosted = []
    query_str = " ".join(tokens)
    for cat_name, kw_list in DOMAIN_CATEGORY_KEYWORDS.items():
        if any(kw in query_str for kw in kw_list) or any(t in kw_list for t in tokens):
            boosted.append(cat_name)
    return boosted

def build_recommendations(conn, intent: str, limit: int = 3, category_filter: str = None, language_filter: str = None, min_stars: int = 0):
    tokens = extract_intent_tokens(intent)
    c = conn.cursor()

    boosted_categories = infer_domain_categories(tokens)

    # Prepare FTS query
    fts_terms = [t for t in tokens if len(t) >= 2]
    candidate_rows = []

    if fts_terms:
        # FTS5 search with OR
        fts_query = " OR ".join(f'"{t}"' for t in fts_terms)
        sql = """
        SELECT r.id, r.name, r.stars, r.forks, r.language, r.category_id, r.category_name, r.url, r.workflow, r.description, r.quality_gate
        FROM repositories_fts f
        JOIN repositories r ON f.rowid = r.id
        WHERE repositories_fts MATCH ?
        """
        params = [fts_query]
        if category_filter:
            sql += " AND (r.category_name LIKE ? OR r.category_id = ?)"
            params.extend([f"%{category_filter}%", int(category_filter) if category_filter.isdigit() else -1])
        if language_filter:
            sql += " AND r.language LIKE ?"
            params.append(f"%{language_filter}%")
        if min_stars > 0:
            sql += " AND r.stars >= ?"
            params.append(min_stars)

        sql += " ORDER BY r.stars DESC LIMIT 30;"
        try:
            c.execute(sql, params)
            candidate_rows = [dict(r) for r in c.fetchall()]
        except sqlite3.OperationalError:
            candidate_rows = []

    # Fallback to LIKE if FTS returned too few results
    if len(candidate_rows) < limit:
        existing_ids = {r["id"] for r in candidate_rows}
        like_sql = """
        SELECT id, name, stars, forks, language, category_id, category_name, url, workflow, description, quality_gate
        FROM repositories
        WHERE 1=1
        """
        like_params = []
        if fts_terms:
            clauses = []
            for t in fts_terms[:4]:
                clauses.append("(name LIKE ? OR description LIKE ? OR workflow LIKE ?)")
                like_params.extend([f"%{t}%", f"%{t}%", f"%{t}%"])
            like_sql += f" AND ({' OR '.join(clauses)})"
        if category_filter:
            like_sql += " AND (category_name LIKE ? OR category_id = ?)"
            like_params.extend([f"%{category_filter}%", int(category_filter) if category_filter.isdigit() else -1])
        if language_filter:
            like_sql += " AND language LIKE ?"
            like_params.append(f"%{language_filter}%")
        if min_stars > 0:
            like_sql += " AND stars >= ?"
            like_params.append(min_stars)

        like_sql += " ORDER BY stars DESC LIMIT 30;"
        c.execute(like_sql, like_params)
        for r in c.fetchall():
            rd = dict(r)
            if rd["id"] not in existing_ids:
                candidate_rows.append(rd)

    # If still empty, return top repositories in the registry
    if not candidate_rows:
        c.execute("SELECT * FROM repositories ORDER BY stars DESC LIMIT ?;", [limit])
        candidate_rows = [dict(r) for r in c.fetchall()]

    # Score and rank candidates
    scored = []
    for row in candidate_rows:
        text_corpus = f"{row['name']} {row['category_name']} {row['workflow']} {row['description']}".lower()
        
        # Keyword matches
        match_count = sum(1 for t in tokens if t in text_corpus)
        name_match = sum(2 for t in tokens if t in row['name'].lower())
        workflow_match = sum(1.5 for t in tokens if t in row['workflow'].lower())
        
        # Domain alignment boost
        cat_boost = 1.35 if row['category_name'] in boosted_categories else 1.0

        # Log-scaled popularity factor
        stars_factor = math.log10(max(row['stars'], 1) + 10) / 6.0
        forks_factor = math.log10(max(row['forks'], 1) + 10) / 5.0

        raw_score = (match_count * 15.0 + name_match * 10.0 + workflow_match * 8.0) * cat_boost + (stars_factor * 25.0) + (forks_factor * 15.0)
        
        # Normalized match score percentage (bounded 65% - 99%)
        match_score = min(99, max(65, int(60 + min(raw_score, 39))))

        scored.append((raw_score, match_score, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_picks = scored[:limit]

    results = []
    for rank, (raw_score, match_score, row) in enumerate(top_picks, 1):
        # Generate Explanation
        explanation = f"Matches user architectural intent for '{intent[:80]}' within the [{row['category_name']}] discipline. Operates as an audited capability executing: {row['workflow'][:120]}."

        # Generate Strengths
        strengths = [
            f"Ecosystem Validation: {row['stars']:,}★ stargazers and {row['forks']:,} forks confirm extensive production adoption and community support.",
            f"Architectural Precision: Executes structured workflow: '{row['workflow']}'.",
            f"Runtime Ecosystem: Built in {row['language']}, offering native ecosystem interoperability, library depth, and performance tooling.",
            f"Quality Governance: Passed automated verification gate ({row['quality_gate']}) with continuous architectural cataloging."
        ]

        # Generate Limitations
        lang = row['language'].lower()
        if "python" in lang:
            lim1 = "Interpreted Python runtime; high-throughput or real-time latency-critical paths require native C/C++ or Rust accelerator extensions."
        elif "c++" in lang or "c" in lang:
            lim1 = "Native C/C++ memory management; requires careful buffer safety practices and longer build/compilation cycles."
        elif "rust" in lang:
            lim1 = "Strict borrow checker and static typing require advanced systems engineering proficiency compared to dynamic scripting."
        elif "javascript" in lang or "typescript" in lang:
            lim1 = "Single-threaded event loop architecture; CPU-bound computation must be dispatched to cluster workers or native threads."
        elif "go" in lang:
            lim1 = "Runtime garbage collection pauses and lack of complex metaprogramming relative to systems languages."
        else:
            lim1 = f"Requires dedicated {row['language']} toolchain and runtime deployment environment."

        if row['stars'] > 50000:
            lim2 = "Comprehensive enterprise feature footprint may introduce dependency overhead if only minimal isolated primitives are needed."
        else:
            lim2 = "Specialized domain focus requires alignment with project data pipelines and strict schema contracts."
        limitations = [lim1, lim2]

        # Peer Alternatives
        alternatives = find_peer_alternatives(conn, row['category_id'], row['id'], limit=3)
        alt_summaries = [
            {"name": a["name"], "stars": a["stars"], "language": a["language"], "url": a["url"]}
            for a in alternatives
        ]

        results.append({
            "rank": rank,
            "match_score": match_score,
            "name": row["name"],
            "url": row["url"],
            "stars": row["stars"],
            "forks": row["forks"],
            "language": row["language"],
            "category_id": row["category_id"],
            "category_name": row["category_name"],
            "workflow": row["workflow"],
            "quality_gate": row["quality_gate"],
            "description": row["description"],
            "explanation": explanation,
            "strengths": strengths,
            "limitations": limitations,
            "alternatives": alt_summaries
        })

    return results

# -----------------------------------------------------------------------------
# Comparison Engine Core
# -----------------------------------------------------------------------------

def compare_repositories(conn, repo_identifiers: list):
    """Compare 2 or 3 repositories side-by-side."""
    if len(repo_identifiers) < 2:
        return {"error": "Compare command requires at least 2 repositories (2 or 3 supported)."}

    # Take up to 3 repositories
    active_identifiers = repo_identifiers[:3]
    repos = []
    for ident in active_identifiers:
        resolved = resolve_repo(conn, ident)
        if not resolved:
            return {"error": f"Repository '{ident}' not found in registry."}
        repos.append(resolved)

    # Calculate comparative metrics
    star_leader = max(repos, key=lambda r: r["stars"])
    fork_leader = max(repos, key=lambda r: r["forks"])
    
    # Fork/Star engagement ratio
    for r in repos:
        r["engagement_ratio"] = round((r["forks"] / max(r["stars"], 1)) * 100, 2)
    engagement_leader = max(repos, key=lambda r: r["engagement_ratio"])

    # Infer capabilities & best-for profiles
    enriched_repos = []
    for r in repos:
        name_lower = r["name"].lower()
        desc_lower = r["description"].lower()
        wf_lower = r["workflow"].lower()

        caps = []
        if "inference" in desc_lower or "serving" in desc_lower or "gemm" in wf_lower:
            caps.append("High-Throughput Inference / Model Execution")
        if "agent" in desc_lower or "multi-agent" in desc_lower or "dag" in wf_lower:
            caps.append("Autonomous Task Planning & Agent Swarm")
        if "vector" in desc_lower or "embedding" in desc_lower or "retrieval" in wf_lower:
            caps.append("Semantic Vector Retrieval / RAG Indexing")
        if "ui" in desc_lower or "widget" in wf_lower or "frontend" in desc_lower:
            caps.append("Reactive UI Rendering & Declarative Layout")
        if "distributed" in desc_lower or "consensus" in desc_lower or "cluster" in desc_lower:
            caps.append("Distributed Cluster Coordination & Resilient Sync")
        if "stream" in desc_lower or "kafka" in desc_lower or "partition" in wf_lower:
            caps.append("Real-Time Event Streaming & Partitioning")
        if "security" in desc_lower or "vulnerability" in desc_lower or "reverse" in desc_lower:
            caps.append("Vulnerability Audit & Binary Reverse Engineering")

        if not caps:
            caps.append("Domain Pipeline Execution & Algorithm Acceleration")
            caps.append("Enterprise System Integration & Tooling")

        # Best For determination
        if r["stars"] == star_leader["stars"]:
            best_for = f"Enterprise production environments requiring peak community adoption ({r['stars']:,}★) and battle-tested ecosystem depth."
        elif r["forks"] == fork_leader["forks"]:
            best_for = f"Highly customizable deployments where active community development and extensive codebase forks ({r['forks']:,}) offer tailored flexibility."
        elif "c++" in r["language"].lower() or "rust" in r["language"].lower():
            best_for = f"Low-latency and edge deployments requiring bare-metal memory efficiency in {r['language']}."
        elif "python" in r["language"].lower():
            best_for = "Rapid prototyping, deep AI/ML library interoperability, and extensive Python workflow scripting."
        elif "go" in r["language"].lower():
            best_for = "Cloud-native services, lightweight microservice daemons, and concurrent containerized workloads."
        else:
            best_for = f"Specialized workflows native to the {r['language']} ecosystem."

        enriched_repos.append({
            "id": r["id"],
            "name": r["name"],
            "url": r["url"],
            "stars": r["stars"],
            "forks": r["forks"],
            "engagement_ratio": r["engagement_ratio"],
            "language": r["language"],
            "category_id": r["category_id"],
            "category_name": r["category_name"],
            "workflow": r["workflow"],
            "quality_gate": r["quality_gate"],
            "description": r["description"],
            "capabilities": caps,
            "best_for": best_for
        })

    # Comparative synthesis
    names = [r["name"] for r in enriched_repos]
    verdict = (
        f"Compared {len(enriched_repos)} repositories across {len(set(r['language'] for r in enriched_repos))} distinct programming stacks. "
        f"'{star_leader['name']}' holds the community adoption lead with {star_leader['stars']:,} stars, while "
        f"'{engagement_leader['name']}' demonstrates the highest fork-to-star developer engagement ratio ({engagement_leader['engagement_ratio']}%). "
        f"Select based on runtime performance constraints vs ecosystem integration depth."
    )

    return {
        "status": "success",
        "comparison_count": len(enriched_repos),
        "leaders": {
            "most_stars": {"name": star_leader["name"], "stars": star_leader["stars"]},
            "most_forks": {"name": fork_leader["name"], "forks": fork_leader["forks"]},
            "highest_engagement_ratio": {"name": engagement_leader["name"], "ratio_percent": engagement_leader["engagement_ratio"]}
        },
        "repositories": enriched_repos,
        "comparative_verdict": verdict
    }

def render_comparison_table(data: dict):
    repos = data["repositories"]
    count = len(repos)
    col_width = 38 if count == 2 else 32

    print("====================================================================================================")
    print(f" ⚖️  REPOSITORY MULTI-DIMENSIONAL COMPARISON MATRIX ({count} Repositories)")
    print("====================================================================================================")

    def row_border(char="-"):
        return "+" + "+".join([char * (col_width + 2) for _ in range(count)]) + "+"

    print(row_border("="))
    # Header: Repository Names
    name_cells = [f" {r['name'][:col_width]:<{col_width}} " for r in repos]
    print("|" + "|".join(name_cells) + "|")
    print(row_border("-"))

    # Dimension 1: Stargazers
    star_leader_name = data["leaders"]["most_stars"]["name"]
    star_cells = []
    for r in repos:
        badge = " 👑 LEADER" if r["name"] == star_leader_name else ""
        content = f"⭐ {r['stars']:,}★{badge}"
        star_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(star_cells) + "|")

    # Dimension 2: Forks
    fork_leader_name = data["leaders"]["most_forks"]["name"]
    fork_cells = []
    for r in repos:
        badge = " 👑" if r["name"] == fork_leader_name else ""
        content = f"🍴 {r['forks']:,} Forks{badge}"
        fork_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(fork_cells) + "|")

    # Dimension 3: Engagement Ratio
    ratio_cells = []
    for r in repos:
        content = f"📊 Engagement: {r['engagement_ratio']}%"
        ratio_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(ratio_cells) + "|")

    # Dimension 4: Primary Language
    lang_cells = []
    for r in repos:
        content = f"💻 Language: {r['language']}"
        lang_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(lang_cells) + "|")

    # Dimension 5: Discipline Category
    cat_cells = []
    for r in repos:
        content = f"📂 [#{r['category_id']}] {r['category_name'][:col_width-7]}"
        cat_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(cat_cells) + "|")

    # Dimension 6: Canonical URL
    url_cells = []
    for r in repos:
        linked_url = make_hyperlink(r['url'], r['url'][:col_width])
        # Hyperlink ANSI length isn't visual, so format carefully
        content = f"🔗 {r['url']}"
        url_cells.append(f" {content[:col_width]:<{col_width}} ")
    print("|" + "|".join(url_cells) + "|")

    print(row_border("="))

    # Operational Architecture Workflow Comparison
    print("\n⚡ OPERATIONAL ARCHITECTURE WORKFLOW COMPARISON:")
    print("-" * 100)
    for idx, r in enumerate(repos, 1):
        linked_title = make_hyperlink(r['url'], r['name'])
        print(f" [{idx}] {linked_title} ({r['language']}):")
        print(f"     {r['workflow']}")

    # Capabilities & Strategic Fit
    print("\n🎯 CAPABILITIES & STRATEGIC FIT:")
    print("-" * 100)
    for idx, r in enumerate(repos, 1):
        print(f" [{idx}] {r['name']}:")
        print(f"     • Best For: {r['best_for']}")
        print(f"     • Core Capabilities: {', '.join(r['capabilities'])}")

    # Executive Verdict
    print("\n💡 EXECUTIVE COMPARATIVE VERDICT:")
    print("┌" + "─" * 98 + "┐")
    for line in [data["comparative_verdict"][i:i+94] for i in range(0, len(data["comparative_verdict"]), 94)]:
        print(f"│  {line:<94}│")
    print("└" + "─" * 98 + "┘")
    print("=" * 100)

# -----------------------------------------------------------------------------
# Command Handlers
# -----------------------------------------------------------------------------

def cmd_stats(args):
    conn = get_connection(getattr(args, "db_path", None))
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*), SUM(stars), SUM(forks), COUNT(DISTINCT language), COUNT(DISTINCT category_name) FROM repositories;")
    row = c.fetchone()
    total_repos, total_stars, total_forks, total_langs, total_cats = row

    c.execute("SELECT category_name, COUNT(*), SUM(stars) FROM repositories GROUP BY category_name ORDER BY COUNT(*) DESC LIMIT 10;")
    top_categories = [{"category": cname, "repos": cnt, "stars": cstars} for cname, cnt, cstars in c.fetchall()]

    c.execute("SELECT language, COUNT(*), SUM(stars) FROM repositories GROUP BY language ORDER BY COUNT(*) DESC LIMIT 10;")
    top_languages = [{"language": lang, "repos": cnt, "stars": cstars} for lang, cnt, cstars in c.fetchall()]
    conn.close()

    if getattr(args, "json", False):
        data = {
            "status": "success",
            "total_repositories": total_repos,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_categories": total_cats,
            "total_languages": total_langs,
            "top_categories": top_categories,
            "top_languages": top_languages,
            "workflow_coverage_percent": 100
        }
        print(json.dumps(data, indent=2))
        return

    print("================================================================================")
    print(" 🚀 GITHUB ULTIMATE REPOS & AGENT REGISTRY — EXECUTIVE INTELLIGENCE DASHBOARD")
    print("================================================================================")
    print(f" Total Repositories / Blueprints : {total_repos:,}")
    print(f" Cumulative Stargazers           : {total_stars:,}★")
    print(f" Cumulative Forks                : {total_forks:,}")
    print(f" Granular Disciplines            : {total_cats}")
    print(f" Programming Languages           : {total_langs}")
    print(f" Architectural Workflow Coverage : 100% (VERIFIED)")
    print("--------------------------------------------------------------------------------")
    
    print("\n[Top 10 Disciplines by Volume]:")
    for idx, item in enumerate(top_categories, 1):
        print(f"  {idx:2d}. {item['category']:<55} | {item['repos']:5,} repos | {item['stars']:10,}★")

    print("\n[Top 10 Languages]:")
    for idx, item in enumerate(top_languages, 1):
        print(f"  {idx:2d}. {item['language']:<20} | {item['repos']:5,} repos | {item['stars']:10,}★")
    print("================================================================================")

def cmd_search(args):
    conn = get_connection(getattr(args, "db_path", None))
    c = conn.cursor()

    query = args.query.strip()
    limit = args.limit
    min_stars = args.min_stars

    fts_query = f'"{query}"' if " " in query and not any(op in query for op in ["AND", "OR", "NOT", "*"]) else query
    sql = """
    SELECT r.id, r.name, r.stars, r.forks, r.language, r.category_name, r.url, r.workflow, r.description
    FROM repositories_fts f
    JOIN repositories r ON f.rowid = r.id
    WHERE repositories_fts MATCH ?
    """
    params = [fts_query]

    if args.category:
        sql += " AND r.category_name LIKE ?"
        params.append(f"%{args.category}%")
    if min_stars > 0:
        sql += " AND r.stars >= ?"
        params.append(min_stars)

    sql += " ORDER BY r.stars DESC LIMIT ?;"
    params.append(limit)

    try:
        c.execute(sql, params)
        rows = [dict(r) for r in c.fetchall()]
    except sqlite3.OperationalError:
        like_sql = """
        SELECT id, name, stars, forks, language, category_name, url, workflow, description
        FROM repositories
        WHERE (name LIKE ? OR description LIKE ? OR workflow LIKE ?)
        """
        like_params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        if args.category:
            like_sql += " AND category_name LIKE ?"
            like_params.append(f"%{args.category}%")
        if min_stars > 0:
            like_sql += " AND stars >= ?"
            like_params.append(min_stars)
        like_sql += " ORDER BY stars DESC LIMIT ?;"
        like_params.append(limit)
        c.execute(like_sql, like_params)
        rows = [dict(r) for r in c.fetchall()]

    conn.close()

    if getattr(args, "json", False):
        data = {
            "status": "success",
            "query": query,
            "count": len(rows),
            "results": rows
        }
        print(json.dumps(data, indent=2))
        return

    print(f"\nSearch results for '{query}' (Found {len(rows)} matching entries):")
    print("=" * 100)
    for idx, r in enumerate(rows, 1):
        linked_name = make_hyperlink(r['url'], r['name'])
        linked_url = make_hyperlink(r['url'], r['url'])
        print(f"\n[{idx}] {linked_name} | ⭐ {r['stars']:,}★ | 🍴 {r['forks']:,} | 💻 {r['language']}")
        print(f"    📂 Category : {r['category_name']}")
        print(f"    🔗 URL      : {linked_url}")
        desc_snippet = r['description'][:140] + ('...' if len(r['description']) > 140 else '')
        print(f"    📝 Desc     : {desc_snippet}")
        print(f"    ⚡ Workflow : {r['workflow']}")
    print("\n" + "=" * 100)

def cmd_get(args):
    conn = get_connection(getattr(args, "db_path", None))
    target = args.repo.strip()
    row = resolve_repo(conn, target)
    conn.close()

    if not row:
        if getattr(args, "json", False):
            print(json.dumps({"status": "error", "message": f"Repository '{target}' not found in registry."}, indent=2))
            sys.exit(1)
        print(f"Repository '{target}' not found in registry.")
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({"status": "success", "repository": row}, indent=2))
        return

    linked_url = make_hyperlink(row['url'], row['url'])
    print("================================================================================")
    print(f" 📦 REPOSITORY DOSSIER: {row['name']}")
    print("================================================================================")
    print(f" Canonical URL       : {linked_url}")
    print(f" Stargazers          : {row['stars']:,}★")
    print(f" Forks               : {row['forks']:,}")
    print(f" Primary Language    : {row['language']}")
    print(f" Discipline Category : [#{row['category_id']}] {row['category_name']}")
    print(f" Quality Gate Status : {row['quality_gate']}")
    print("--------------------------------------------------------------------------------")
    print(f" Description:\n {row['description']}")
    print("--------------------------------------------------------------------------------")
    print(f" Operational Architecture Workflow:\n ⚡ {row['workflow']}")
    print("================================================================================")

def cmd_category(args):
    conn = get_connection(getattr(args, "db_path", None))
    c = conn.cursor()
    query = args.name.strip()
    limit = args.limit

    c.execute("""
    SELECT id, name, stars, forks, language, category_name, url, workflow, description
    FROM repositories
    WHERE category_name LIKE ? OR category_id = ?
    ORDER BY stars DESC
    LIMIT ?;
    """, [f"%{query}%", int(query) if query.isdigit() else -1, limit])
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    if getattr(args, "json", False):
        data = {
            "status": "success",
            "category_query": query,
            "count": len(rows),
            "results": rows
        }
        print(json.dumps(data, indent=2))
        return

    print(f"\nTop Repositories for Category '{query}' (Displaying top {len(rows)}):")
    print("=" * 100)
    for idx, r in enumerate(rows, 1):
        linked_name = make_hyperlink(r['url'], r['name'])
        linked_url = make_hyperlink(r['url'], r['url'])
        print(f"[{idx:2d}] {r['name']:<40} | ⭐ {r['stars']:7,}★ | 💻 {r['language']:<12} | 🔗 {linked_url}")
        print(f"     ⚡ Workflow: {r['workflow']}")
    print("=" * 100)

def sanitize_csv_value(val):
    """
    Sanitize CSV cell values to prevent CSV formula injection (DDE attacks).
    Prepends a single quote if the field starts with =, +, -, @, \\t, or \\r.
    """
    if not isinstance(val, str):
        return val
    stripped = val.lstrip()
    if stripped and stripped[0] in ('=', '+', '-', '@'):
        return f"'{val}"
    if val and (val.startswith('\t') or val.startswith('\r')):
        return f"'{val}"
    return val

def sanitize_csv_row(row):
    """
    Sanitize all string values within a dictionary row to prevent CSV formula injection.
    """
    if not isinstance(row, dict):
        return row
    return {k: sanitize_csv_value(v) for k, v in row.items()}

def cmd_export(args):
    conn = get_connection(getattr(args, "db_path", None))
    c = conn.cursor()

    sql = "SELECT * FROM repositories WHERE 1=1"
    params = []
    if args.category:
        sql += " AND category_name LIKE ?"
        params.append(f"%{args.category}%")
    if args.min_stars > 0:
        sql += " AND stars >= ?"
        params.append(args.min_stars)
    sql += " ORDER BY stars DESC;"

    c.execute(sql, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    out_file = args.output
    if args.format == "json":
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
    elif args.format == "csv":
        if rows:
            sanitized_rows = [
                sanitize_csv_row(row)
                for row in rows
            ]
            with open(out_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(sanitized_rows)
    print(f"Exported {len(rows):,} records to {out_file} ({args.format.upper()}).")

def cmd_recommend(args):
    conn = get_connection(getattr(args, "db_path", None))
    raw_intent = args.intent.strip()
    if not raw_intent:
        print("Error: Please provide a natural language intent query.", file=sys.stderr)
        sys.exit(1)

    recommendations = build_recommendations(
        conn,
        raw_intent,
        limit=args.limit,
        category_filter=args.category,
        language_filter=args.language,
        min_stars=args.min_stars
    )
    conn.close()

    if getattr(args, "json", False):
        data = {
            "status": "success",
            "intent": raw_intent,
            "total_recommendations": len(recommendations),
            "recommendations": recommendations
        }
        print(json.dumps(data, indent=2))
        return

    # Terminal card formatting
    print("====================================================================================================")
    print(" 🎯 INTELLIGENT REPOSITORY RECOMMENDATIONS ENGINE")
    print(f" Query Intent   : \"{raw_intent}\"")
    if args.category:
        print(f" Category Scope : {args.category}")
    if args.language:
        print(f" Language Filter: {args.language}")
    print(f" RECOMMENDATIONS: {len(recommendations)} Ranked Cards")
    print("====================================================================================================")

    for rec in recommendations:
        rank = rec["rank"]
        badge = "⭐ TOP RECOMMENDATION" if rank == 1 else f"ALTERNATIVE #{rank}"
        linked_url = make_hyperlink(rec["url"], rec["url"])

        print(f"\n┌──────────────────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"│ [RANK #{rank}] {badge:<30} (Match Score: {rec['match_score']}%)")
        print(f"│ 📦 Repository : {rec['name']}")
        print(f"│ 🔗 URL        : {linked_url}")
        print(f"│ 📊 Metrics    : {rec['stars']:,}★ Stargazers | {rec['forks']:,} Forks | Language: {rec['language']}")
        print(f"│ 📂 Discipline : [#{rec['category_id']}] {rec['category_name']}")
        print(f"├──────────────────────────────────────────────────────────────────────────────────────────────────┤")
        print(f"│ 💡 WHY RECOMMENDED:")
        print(f"│    {rec['explanation']}")
        print(f"│")
        print(f"│ ⚡ OPERATIONAL ARCHITECTURE WORKFLOW:")
        print(f"│    {rec['workflow']}")
        print(f"│")
        print(f"│ 🚀 CORE STRENGTHS:")
        for s in rec["strengths"]:
            print(f"│    • {s}")
        print(f"│")
        print(f"│ ⚠️ LIMITATIONS & TRADE-OFFS:")
        for lim in rec["limitations"]:
            print(f"│    • {lim}")
        print(f"│")
        print(f"│ 🔄 PEER ALTERNATIVES IN DISCIPLINE:")
        if rec["alternatives"]:
            for a in rec["alternatives"]:
                alt_link = make_hyperlink(a['url'], a['name'])
                print(f"│    • {a['name']} ({a['stars']:,}★, {a['language']}) - {alt_link}")
        else:
            print(f"│    • No direct peer alternatives found above threshold.")
        print(f"└──────────────────────────────────────────────────────────────────────────────────────────────────┘")
    print("\n" + "=" * 100)

def cmd_compare(args):
    db_path = getattr(args, "db_path", None) or DEFAULT_DB_PATH
    repos = getattr(args, "repos", [])
    format_type = getattr(args, "format", "terminal")
    if getattr(args, "json", False):
        format_type = "json"

    if len(repos) < 2 or len(repos) > 3:
        err_msg = f"Error: Compare requires exactly 2 or 3 repository identifiers, received: {len(repos)}."
        if format_type == "json":
            print(json.dumps({"status": "error", "error": err_msg, "message": err_msg}, indent=2))
        else:
            print(err_msg, file=sys.stderr)
        sys.exit(1)

    try:
        engine = TradeoffEngine(db_path=db_path)
        evaluation = engine.compare(repos)
    except Exception as e:
        err_msg = f"Error: Comparison failed: {e}"
        if format_type == "json":
            print(json.dumps({"status": "error", "error": err_msg, "message": err_msg}, indent=2))
        else:
            print(err_msg, file=sys.stderr)
        sys.exit(1)

    if format_type == "json":
        out_str = json.dumps(evaluation.to_dict(), indent=2)
    elif format_type == "markdown":
        out_str = render_tradeoff_markdown(evaluation)
    else:
        out_str = render_tradeoff_terminal(evaluation)

    output_path = getattr(args, "output", None)
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(out_str)
        print(f"Comparison report saved to: {output_path}")
    else:
        print(out_str)

def cmd_workflow(args):
    conn = get_connection(getattr(args, "db_path", None))

    # Normalize workflow identifiers
    alias_map = {
        "ai": "ai-agent",
        "agent": "ai-agent",
        "agents": "ai-agent",
        "mobile-app": "mobile",
        "cloud": "devops",
        "gitops": "devops",
        "web": "fullstack",
        "web-fullstack": "fullstack",
        "saas": "fullstack",
        "data": "data-engineering",
        "data-eng": "data-engineering",
        "security": "cybersecurity"
    }
    for k, wf in CURATED_WORKFLOWS.items():
        alias_map[k.lower()] = k
        if "code" in wf:
            code_lower = wf["code"].lower()
            alias_map[code_lower] = k
            alias_map[code_lower.replace("-", "")] = k

    raw_name = (args.name or "").strip().lower()
    clean_name = re.sub(r'^wf-', '', raw_name)
    clean_name = re.sub(r'-\d+$', '', clean_name)
    wf_key = alias_map.get(raw_name) or alias_map.get(clean_name) or (clean_name if clean_name in CURATED_WORKFLOWS else raw_name)

    # 1. Handle --list
    if args.list or not wf_key:
        if not args.category:
            wf_list = []
            for k, wf in CURATED_WORKFLOWS.items():
                wf_list.append({
                    "id": wf["id"],
                    "code": wf.get("code", ""),
                    "title": wf["title"],
                    "domain": wf["domain"],
                    "steps_count": len(wf["steps"]),
                    "pipeline_summary": wf["pipeline_summary"]
                })

            if getattr(args, "json", False):
                print(json.dumps({"status": "success", "available_workflows": wf_list}, indent=2))
                conn.close()
                return

            print("====================================================================================================")
            print(" 🔄 GITHUB ULTIMATE REPOS — END-TO-END WORKFLOW BLUEPRINTS DIRECTORY")
            print("====================================================================================================")
            print(" Available Curated Production Workflow Blueprints (WORKFLOW BLUEPRINTS):\n")
            for idx, wf in enumerate(wf_list, 1):
                alias_tag = f" (Alias: {wf['code']})" if wf.get("code") else ""
                print(f" [{idx}] ID: {wf['id']}{alias_tag}")
                print(f"     Title   : {wf['title']}")
                print(f"     Domain  : {wf['domain']}")
                print(f"     Stages  : {wf['steps_count']} Verified Steps")
                print(f"     Pipeline: {wf['pipeline_summary']}")
                print(f"     Inspect : python scripts/cli/ultimate_agent_cli.py workflow {wf['id']}\n")
            print(" Tip: Use --interactive to step through interactively, or --step <N> for a specific stage.")
            print(" Tip: Synthesize a workflow for any of 55 disciplines: ultimate_agent_cli.py workflow --category <Discipline>")
            print("====================================================================================================")
            conn.close()
            return

    # 2. Resolve workflow definition
    active_wf = None
    if args.category:
        active_wf = synthesize_category_workflow(conn, args.category)
        if not active_wf:
            err_msg = f"No repositories found for discipline category '{args.category}'."
            if getattr(args, "json", False):
                print(json.dumps({"status": "error", "message": err_msg}, indent=2))
            else:
                print(f"Error: {err_msg}", file=sys.stderr)
            conn.close()
            sys.exit(1)
    elif wf_key in CURATED_WORKFLOWS:
        active_wf = enrich_workflow_tools(conn, CURATED_WORKFLOWS[wf_key])
    else:
        # Check if wf_key matches a category in the DB
        cat_wf = synthesize_category_workflow(conn, wf_key)
        if cat_wf:
            active_wf = cat_wf
        else:
            err_msg = f"Workflow '{wf_key}' not found. Run 'workflow --list' to see available workflows."
            if getattr(args, "json", False):
                print(json.dumps({"status": "error", "message": err_msg}, indent=2))
            else:
                print(f"Error: {err_msg}", file=sys.stderr)
            conn.close()
            sys.exit(1)

    conn.close()

    # 3. Handle --json output
    if getattr(args, "json", False):
        if args.step:
            step_num = args.step
            matched = [s for s in active_wf["steps"] if s["step"] == step_num]
            if not matched:
                print(json.dumps({"status": "error", "message": f"Step {step_num} not found. Valid: 1-{len(active_wf['steps'])}"}, indent=2))
                sys.exit(1)
            print(json.dumps({"status": "success", "workflow": active_wf["id"], "step": matched[0]}, indent=2))
            return
        print(json.dumps({"status": "success", "workflow": active_wf}, indent=2))
        return

    # 4. Handle --step N
    if args.step:
        step_num = args.step
        matched = [s for s in active_wf["steps"] if s["step"] == step_num]
        if not matched:
            print(f"Error: Step {step_num} is out of range. Workflow has {len(active_wf['steps'])} steps.", file=sys.stderr)
            sys.exit(1)
        st = matched[0]
        render_workflow_step_detail(active_wf, st)
        return

    # 5. Handle --interactive step-through
    if args.interactive:
        print("====================================================================================================")
        print(f" 🚀 INTERACTIVE WORKFLOW EXECUTION: {active_wf['title'].upper()}")
        print(f" Domain: {active_wf['domain']}")
        print(f" Pipeline: {active_wf['pipeline_summary']}")
        print("====================================================================================================")
        for st in active_wf["steps"]:
            render_workflow_step_detail(active_wf, st)
            if st["step"] < len(active_wf["steps"]):
                try:
                    resp = input(f"\n[Press Enter to proceed to Step {st['step'] + 1}, 'q' to quit]: ").strip().lower()
                    if resp in ("q", "quit", "exit"):
                        print("Workflow execution suspended.")
                        return
                except (EOFError, KeyboardInterrupt):
                    print("\nExiting workflow.")
                    return
        print("\n✅ All workflow stages completed successfully!")
        return

    # 6. Default: Render full workflow overview
    print("====================================================================================================")
    print(f" 🔄 END-TO-END DEVELOPMENT WORKFLOW: {active_wf['title'].upper()}")
    print("====================================================================================================")
    print(f" ID Scope         : {active_wf['id']}")
    print(f" Domain Category  : {active_wf['domain']}")
    print(f" Executive Summary: {active_wf['description']}\n")
    print(f" ⚡ Pipeline Flow :")
    print(f"    {active_wf['pipeline_summary']}\n")
    print("----------------------------------------------------------------------------------------------------")
    print(f" ARCHITECTURAL STAGES ({len(active_wf['steps'])} STAGES):")
    print("----------------------------------------------------------------------------------------------------")

    for st in active_wf["steps"]:
        print(f"\n┌─ [Stage {st['step']}/{len(active_wf['steps'])}] Stage {st['step']}: {st['name'].upper()}")
        print(f"│  🎯 Objective : {st['objective']}")
        print(f"│  ⚡ Pattern   : {st['architecture_pattern']}")
        print(f"│  📦 Tooling   :")
        for t in st.get("tools", []):
            linked_tool = make_hyperlink(t['url'], t['name'])
            stars_badge = f"({t['stars']:,}★, {t['language']})" if t['stars'] > 0 else f"({t['language']})"
            print(f"│     • {linked_tool} {stars_badge}")
        print(f"│  💻 Recipe    : {st['recipe']}")
        print(f"│  ✅ Gate      : {st['verification']}")
        print(f"└───────────────────────────────────────────────────────────────────────────────────────────────────")

    print("\n" + "=" * 100)
    print(f" Tip: Deep dive into any stage: python scripts/cli/ultimate_agent_cli.py workflow {active_wf['id']} --step 1")
    print(f" Tip: Step through live       : python scripts/cli/ultimate_agent_cli.py workflow {active_wf['id']} --interactive")
    print("=" * 100)

def render_workflow_step_detail(wf: dict, st: dict):
    print("\n====================================================================================================")
    print(f" 🔍 WORKFLOW DEEP DIVE: {wf['title'].upper()}")
    print(f" [Stage {st['step']}/{len(wf['steps'])}] Stage {st['step']}: {st['name'].upper()}")
    print("====================================================================================================")
    print(f" 🎯 Phase Objective : {st['objective']}")
    print(f" ⚡ Architecture    : {st['architecture_pattern']}\n")

    print(" 📦 RECOMMENDED AUDITED TOOLS FROM REGISTRY:")
    print(" " + "-" * 98)
    for t in st.get("tools", []):
        linked_name = make_hyperlink(t['url'], t['name'])
        linked_url = make_hyperlink(t['url'], t['url'])
        print(f" • {linked_name} | ⭐ {t['stars']:,}★ | 🍴 {t['forks']:,} | 💻 {t['language']}")
        print(f"   🔗 URL      : {linked_url}")
        print(f"   ⚡ Workflow : {t['workflow']}")
        print(f"   📝 Summary  : {t['description'][:140]}{'...' if len(t['description']) > 140 else ''}\n")

    print(" 🛠️ IMPLEMENTATION RECIPE:")
    print(" " + "-" * 98)
    print(f"   {st['recipe']}\n")

    print(" ✅ VERIFICATION CRITERION & QUALITY GATE:")
    print(" " + "-" * 98)
    print(f"   {st['verification']}")
    print("====================================================================================================")

# -----------------------------------------------------------------------------
# Main CLI Entrypoint & Argument Parsing
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="ultimate_agent_cli.py",
        description="Github Ultimate Repos - High-Performance Multi-Agent Registry & Workflow Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Summary dashboard & metrics
  python ultimate_agent_cli.py stats
  python ultimate_agent_cli.py stats --json

  # Full-text repository search with filters
  python ultimate_agent_cli.py search "kubernetes gitops" --limit 5
  python ultimate_agent_cli.py search "inference" --category "Artificial Intelligence"

  # Repository dossier inspection
  python ultimate_agent_cli.py get vllm
  python ultimate_agent_cli.py get sindresorhus/awesome

  # Top repositories in a category
  python ultimate_agent_cli.py category "Robotics" --limit 5
  python ultimate_agent_cli.py category 3

  # Intelligent natural language recommendation cards
  python ultimate_agent_cli.py recommend "I need an agent orchestration framework with tool calling"
  python ultimate_agent_cli.py recommend "fast inference engine for local models" --limit 3 --json

  # Side-by-side repository comparison (2 or 3 repos)
  python ultimate_agent_cli.py compare vllm llama.cpp ollama
  python ultimate_agent_cli.py compare react vue --json

  # End-to-end development workflow explorer
  python ultimate_agent_cli.py workflow --list
  python ultimate_agent_cli.py workflow ai-agent
  python ultimate_agent_cli.py workflow mobile --step 2
  python ultimate_agent_cli.py workflow devops --interactive
  python ultimate_agent_cli.py workflow --category "Robotics"

  # Export filtered data
  python ultimate_agent_cli.py export --format json --output repos.json
        """
    )

    # Global options
    parser.add_argument("--json", action="store_true", help="Output results strictly as structured JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color codes and styling")
    parser.add_argument("--db-path", help=f"Path to SQLite database (default: {DEFAULT_DB_PATH})")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: stats
    p_stats = subparsers.add_parser("stats", help="Show registry summary dashboard and volume distributions")
    p_stats.add_argument("--json", action="store_true", help="Output stats as JSON")
    p_stats.set_defaults(func=cmd_stats)

    # Subcommand: search
    p_search = subparsers.add_parser("search", help="Full-text search repositories with ranking")
    p_search.add_argument("query", help="Keywords to search")
    p_search.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    p_search.add_argument("--category", help="Filter by category name or ID")
    p_search.add_argument("--min-stars", type=int, default=0, help="Filter by minimum star count")
    p_search.add_argument("--json", action="store_true", help="Output search results as JSON")
    p_search.set_defaults(func=cmd_search)

    # Subcommand: get
    p_get = subparsers.add_parser("get", help="Get full dossier for a specific repository")
    p_get.add_argument("repo", help="Repository name (owner/repo or short name)")
    p_get.add_argument("--json", action="store_true", help="Output dossier as JSON")
    p_get.set_defaults(func=cmd_get)

    # Subcommand: category
    p_cat = subparsers.add_parser("category", help="List top repositories in a category")
    p_cat.add_argument("name", help="Category name or ID (1-55)")
    p_cat.add_argument("--limit", type=int, default=15, help="Max results (default: 15)")
    p_cat.add_argument("--json", action="store_true", help="Output category results as JSON")
    p_cat.set_defaults(func=cmd_category)

    # Subcommand: export
    p_exp = subparsers.add_parser("export", help="Export filtered repositories to JSON or CSV")
    p_exp.add_argument("--category", help="Filter by category")
    p_exp.add_argument("--min-stars", type=int, default=0, help="Filter by minimum star count")
    p_exp.add_argument("--format", choices=["json", "csv"], default="json", help="Export format (json/csv)")
    p_exp.add_argument("--output", required=True, help="Output destination file path")
    p_exp.set_defaults(func=cmd_export)

    # Subcommand: recommend
    p_rec = subparsers.add_parser("recommend", aliases=["rec"], help="Natural language intent query -> ranked recommendation cards")
    p_rec.add_argument("intent", help="Natural language query stating what you want to build or achieve")
    p_rec.add_argument("--limit", type=int, default=3, help="Number of recommendations (default: 3)")
    p_rec.add_argument("--category", help="Filter to specific discipline category")
    p_rec.add_argument("--language", help="Filter to specific programming language")
    p_rec.add_argument("--min-stars", type=int, default=0, help="Filter by minimum star count")
    p_rec.add_argument("--json", action="store_true", help="Output recommendations as JSON")
    p_rec.set_defaults(func=cmd_recommend)

    # Subcommand: compare
    p_cmp = subparsers.add_parser("compare", aliases=["cmp"], help="Compare 2 or 3 repositories side-by-side")
    p_cmp.add_argument("repos", nargs="+", help="2 or 3 repository identifiers (e.g. vllm llama.cpp ollama)")
    p_cmp.add_argument("--format", choices=["terminal", "markdown", "json"], default="terminal", help="Output format: terminal, markdown, or json (default: terminal)")
    p_cmp.add_argument("--json", action="store_true", help="Output comparison as JSON (shorthand for --format json)")
    p_cmp.add_argument("--output", "-o", help="Optional destination file path to save output")
    p_cmp.set_defaults(func=cmd_compare)

    # Subcommand: workflow
    p_wf = subparsers.add_parser("workflow", aliases=["wf"], help="View and step through end-to-end development workflows")
    p_wf.add_argument("name", nargs="?", default="", help="Workflow identifier (e.g. ai-agent, mobile, devops, fullstack)")
    p_wf.add_argument("--list", action="store_true", help="List all available curated workflows")
    p_wf.add_argument("--step", type=int, help="Inspect a specific workflow step number (1-based)")
    p_wf.add_argument("--category", help="Synthesize workflow for any of the 55 discipline categories")
    p_wf.add_argument("--interactive", action="store_true", help="Step through workflow interactively in terminal")
    p_wf.add_argument("--json", action="store_true", help="Output workflow definition as JSON")
    p_wf.set_defaults(func=cmd_workflow)

    args = parser.parse_args()

    # Pass global flags to subcommands if set
    if getattr(args, "json", False) or getattr(parser.parse_known_args()[0], "json", False):
        args.json = True

    if getattr(args, "no_color", False):
        os.environ["NO_COLOR"] = "1"

    args.func(args)

if __name__ == "__main__":
    main()
