#!/usr/bin/env python3
"""
generate_workflows.py - Workflow Intelligence & Schema Generator for Github Ultimate Repos

Generates concrete, multi-stage, production-grade workflow specifications in both JSON and YAML
for the 6 core enterprise development and AI agent domains, referencing verified catalog repositories.
"""

import os
import sys
import json
import sqlite3
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")
WORKFLOWS_DIR = os.path.join(REPO_ROOT, "workflows")
SCHEMAS_DIR = os.path.join(REPO_ROOT, "schemas")

os.makedirs(WORKFLOWS_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
c = conn.cursor()

def fetch_repo_meta(handle, role):
    c.execute("""
        SELECT name, stars, category_name, url, workflow
        FROM repositories
        WHERE name = ? OR name LIKE ?
        ORDER BY stars DESC LIMIT 1
    """, (handle, f"%/{handle}"))
    row = c.fetchone()
    if not row:
        c.execute("""
            SELECT name, stars, category_name, url, workflow
            FROM repositories
            WHERE name LIKE ?
            ORDER BY stars DESC LIMIT 1
        """, (f"%{handle}%",))
        row = c.fetchone()
    if not row:
        raise ValueError(f"Repository not found in registry: {handle}")
    return {
        "name": row["name"],
        "stars": row["stars"],
        "category": row["category_name"],
        "url": row["url"],
        "workflow_pipeline": row["workflow"],
        "role_in_stage": role
    }

workflows_data = [
    # --------------------------------------------------------------------------
    # 1. PRODUCTION AI AGENT WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-001",
        "name": "Production AI Agent Enterprise Lifecycle",
        "domain": "Artificial Intelligence & Autonomous Agent Swarms",
        "description": "Comprehensive 7-stage engineering lifecycle for enterprise multi-agent systems, from declarative prompt/specification optimization through low-latency quantized inference, structured multimodal document ingestion, scalable vector retrieval, dynamic swarm coordination via Model Context Protocol (MCP), LLM observability with automated evaluation guardrails, to production-grade gateway deployment.",
        "total_stages": 7,
        "governance": {
            "quality_gate_standard": "7-Gate Enterprise Multi-Agent Governance",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Requirements & Specification Engineering",
                "purpose": "Compile operational agent specifications, optimize prompt templates systematically, enforce deterministic typed schemas, and generate test assert suites.",
                "recommended_repositories": [
                    fetch_repo_meta("stanfordnlp/dspy", "Algorithmic prompt optimization and compiler for LLM pipeline programming"),
                    fetch_repo_meta("promptfoo/promptfoo", "Security red-teaming, prompt regression test harness and eval matrix"),
                    fetch_repo_meta("567-labs/instructor", "Pydantic-enforced structured LLM outputs, schema validation and automatic retries")
                ],
                "input_handoff": {
                    "source_stage": "User Requirements / Product Specification (PRD)",
                    "artifacts": ["PRD Document", "Domain Persona Briefs", "Target Tool List", "JSON Schema Contracts"],
                    "format": "Markdown / JSON Schema"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: Foundation Model & Inference Optimization",
                    "artifacts": ["Compiled DSPy Signatures", "Pydantic Output Models", "Promptfoo Evaluation Assertions", "System Prompts"],
                    "format": "Python Modules / YAML Assertions"
                },
                "dependencies": ["Python 3.10+", "Pydantic v2", "API Keys / Access to Reference Foundation Models"],
                "alternatives": [
                    {"name": "MadcowD/ell", "tradeoff": "Functional prompt engineering with rich state tracking but less mathematical optimization than DSPy"},
                    {"name": "guidance-ai/guidance", "tradeoff": "Interleaved generation with fine control over constrained token generation, higher token-level complexity"}
                ],
                "quality_gate": "Gate 1: Schema Integrity & Promptfoo 95%+ Pass Rate on Synthesized Test Cases"
            },
            {
                "stage_id": 2,
                "stage_name": "Foundation Model & Inference Optimization",
                "purpose": "Deploy and configure high-throughput local and cloud inference engines with continuous batching, quantized weights (GGUF/AWQ/GPTQ), and unified multi-provider routing.",
                "recommended_repositories": [
                    fetch_repo_meta("vllm-project/vllm", "High-throughput serving engine with PagedAttention and continuous iteration batching"),
                    fetch_repo_meta("ollama/ollama", "Lightweight, container-ready local LLM runtime with fast modelfile management"),
                    fetch_repo_meta("ggml-org/llama.cpp", "Bare-metal CPU/GPU quantized GGUF inference engine with zero external dependencies"),
                    fetch_repo_meta("BerriAI/litellm", "Universal proxy and load balancer translating 100+ LLM APIs into OpenAI-compatible endpoints")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Requirements & Specification Engineering",
                    "artifacts": ["Model Capability Matrix", "Token Budget Specifications", "Quantization Thresholds"],
                    "format": "JSON / YAML"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: Multimodal Ingestion & Document Parsing",
                    "artifacts": ["Standardized OpenAI-Compatible API Endpoints", "Health-Checked Model Workers", "Inference Fallback Policies"],
                    "format": "HTTPS / SSE Streaming"
                },
                "dependencies": ["NVIDIA CUDA Toolkit 12.x / ROCm or Apple Silicon Metal", "vLLM / Ollama Daemon", "Minimum 16GB VRAM for 8B-14B models"],
                "alternatives": [
                    {"name": "huggingface/text-generation-inference", "tradeoff": "Enterprise-grade Docker deployment, stricter licensing than vLLM"},
                    {"name": "unslothai/unsloth", "tradeoff": "Ultra-fast LoRA/QLoRA fine-tuning runtime, primarily training-focused rather than serving"}
                ],
                "quality_gate": "Gate 2: Sub-50ms Time-to-First-Token (TTFT) and 40+ tokens/sec throughput under concurrency"
            },
            {
                "stage_id": 3,
                "stage_name": "Multimodal Ingestion & Document Parsing",
                "purpose": "Extract, normalize, chunk, and enrich heterogeneous document formats (PDFs, DOCX, scans, spreadsheets, code) into structured Markdown AST with bounding boxes and table preservation.",
                "recommended_repositories": [
                    fetch_repo_meta("docling-project/docling", "State-of-the-art document layout analysis, OCR and universal Markdown conversion"),
                    fetch_repo_meta("datalab-to/marker", "High-speed PDF to Markdown conversion with LaTeX equation extraction"),
                    fetch_repo_meta("google/langextract", "Semantic text extraction and linguistic structure normalization")
                ],
                "input_handoff": {
                    "source_stage": "External Data Lakes / Cloud Buckets / Enterprise Storage",
                    "artifacts": ["Raw PDFs", "Technical Manuals", "Financial Spreadsheets", "API Documentation"],
                    "format": "Binary / PDF / DOCX / HTML"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Knowledge Indexing & Hybrid Vector Retrieval",
                    "artifacts": ["Structured Markdown Documents", "Extracted Tables as JSON/HTML", "Semantic Chunks with Provenance Metadata"],
                    "format": "JSON Lines (JSONL) / Parquet"
                },
                "dependencies": ["Tesseract OCR / EasyOCR", "PyMuPDF / pdfplumber", "Pandas / NumPy"],
                "alternatives": [
                    {"name": "Unstructured-IO/unstructured", "tradeoff": "Extensive connector ecosystem, but heavier dependency footprint than Docling"},
                    {"name": "nlpaueb/spacy-transformers", "tradeoff": "Deep linguistic tagging, requires significant CPU/memory overhead"}
                ],
                "quality_gate": "Gate 3: 98%+ Table and Structure Extraction Fidelity with Zero Content Truncation"
            },
            {
                "stage_id": 4,
                "stage_name": "Knowledge Indexing & Hybrid Vector Retrieval",
                "purpose": "Compute dense and sparse embeddings, index high-dimensional vectors, and execute hybrid BM25 + dense search with reciprocal rank fusion (RRF) and re-ranking.",
                "recommended_repositories": [
                    fetch_repo_meta("qdrant/qdrant", "High-performance Rust-powered vector database with rich payload filtering and HNSW indexing"),
                    fetch_repo_meta("milvus-io/milvus", "Cloud-native distributed vector database designed for billion-scale similarity search"),
                    fetch_repo_meta("facebookresearch/faiss", "Low-level optimized library for dense vector clustering and billion-scale search")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: Multimodal Ingestion & Document Parsing",
                    "artifacts": ["Chunked Documents", "Metadata Attributes (author, date, tags)", "Embedding Model Specification"],
                    "format": "JSONL"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Swarm Orchestration & Tool Execution",
                    "artifacts": ["Vector Collection Collections", "RRF Hybrid Search Retriever Endpoints", "Contextual Reranking Pipeline"],
                    "format": "gRPC / REST Endpoints"
                },
                "dependencies": ["Text Embedding Model (e.g. BGE-M3 / OpenAI text-embedding-3)", "Qdrant Cluster or Docker Container", "FastAPI / gRPC Client"],
                "alternatives": [
                    {"name": "chroma-core/chroma", "tradeoff": "Zero-config embedded local database, lower throughput than Qdrant in distributed multi-node clusters"},
                    {"name": "pgvector/pgvector", "tradeoff": "Consolidates vector search inside PostgreSQL, lower maximum QPS on billion-scale collections"}
                ],
                "quality_gate": "Gate 4: Recall@10 >= 0.88 and Sub-15ms Hybrid Query Retrieval Latency"
            },
            {
                "stage_id": 5,
                "stage_name": "Swarm Orchestration & Tool Execution",
                "purpose": "Coordinate multi-agent collaboration, manage dynamic task decomposition DAGs, implement Model Context Protocol (MCP) tool bindings, and maintain stateful conversational memory.",
                "recommended_repositories": [
                    fetch_repo_meta("FoundationAgents/MetaGPT", "Multi-agent collaborative framework encoding Standard Operating Procedures (SOPs) into agent teams"),
                    fetch_repo_meta("microsoft/autogen", "Event-driven multi-agent conversation framework with code execution and human-in-the-loop"),
                    fetch_repo_meta("crewAIInc/crewAI", "Role-based autonomous agent orchestration platform with built-in task delegation"),
                    fetch_repo_meta("langchain-ai/langgraph", "Graph-based cyclic state machine for reliable multi-agent workflows and checkpoints")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1 (Specs), Stage 2 (Models), Stage 4 (Retrievers)",
                    "artifacts": ["Agent Role Definitions", "MCP Tool Servers", "Retriever Tools", "Execution Graph"],
                    "format": "Python Classes / LangGraph StateGraph / YAML"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Continuous Evaluation, Observability & Guardrails",
                    "artifacts": ["Multi-Agent Execution Traces", "Tool Call Payloads", "Intermediate Reasoning Chains", "Final Agent Outputs"],
                    "format": "OpenTelemetry Spans / JSON Lines"
                },
                "dependencies": ["Python 3.11+", "LangGraph / CrewAI SDK", "Docker Sandbox for Safe Code Execution", "Model Context Protocol (MCP) Server Runtimes"],
                "alternatives": [
                    {"name": "huggingface/smolagents", "tradeoff": "Minimalist code-based agent framework, lightweight but fewer enterprise team SOP primitives"},
                    {"name": "microsoft/semantic-kernel", "tradeoff": "Polyglot enterprise SDK (C#, Python, Java), more verbose enterprise abstractions"}
                ],
                "quality_gate": "Gate 5: Zero Tool Hallucination Rate and Non-Cyclical Termination Guarantee within Configured Max Steps"
            },
            {
                "stage_id": 6,
                "stage_name": "Continuous Evaluation, Observability & Guardrails",
                "purpose": "Monitor agent traces in real time, evaluate groundedness, answer relevancy, and hallucination scores, and apply runtime security guardrails against prompt injections.",
                "recommended_repositories": [
                    fetch_repo_meta("langfuse/langfuse", "Open-source LLM engineering platform for distributed tracing, evals, prompt management and latency monitoring"),
                    fetch_repo_meta("vibrantlabsai/ragas", "Automated RAG evaluation framework measuring Faithfulness, Answer Relevance, and Context Precision"),
                    fetch_repo_meta("Portkey-AI/gateway", "Fast AI gateway with routing, fallbacks, load-balancing, rate-limiting, and guardrails")
                ],
                "input_handoff": {
                    "source_stage": "Stage 5: Swarm Orchestration & Tool Execution",
                    "artifacts": ["Real-Time Execution Traces", "Prompt/Response Pairs", "Context Documents"],
                    "format": "OTel Traces / JSON"
                },
                "output_handoff": {
                    "next_stage": "Stage 7: Production Deployment, Gateway & Scaling",
                    "artifacts": ["Quality Scorecards", "Safety Policy Verification", "Latency Profiles", "Filtered Production Prompts"],
                    "format": "Dashboard Analytics / Prometheus Metrics"
                },
                "dependencies": ["Langfuse Server / PostgreSQL", "Ragas Benchmark Datasets", "OpenTelemetry SDK"],
                "alternatives": [
                    {"name": "Arize-ai/phoenix", "tradeoff": "AI observability with deep embedding space clustering, specialized in drift detection"},
                    {"name": "NVIDIA/NeMo-Guardrails", "tradeoff": "Colang programmable safety rails, requires learning Colang domain-specific language"}
                ],
                "quality_gate": "Gate 6: Faithfulness >= 0.92, Context Relevance >= 0.85, and 100% Guardrail Block on Adversarial Injections"
            },
            {
                "stage_id": 7,
                "stage_name": "Production Deployment, Gateway & Scaling",
                "purpose": "Package agent swarms into production microservices, configure intelligent edge routing, enforce rate limits, and provide enterprise user interfaces.",
                "recommended_repositories": [
                    fetch_repo_meta("bentoml/BentoML", "Enterprise framework for building reliable, performant, and scalable AI services and APIs"),
                    fetch_repo_meta("open-webui/open-webui", "Extensible, self-hosted AI interface with comprehensive multi-model chat, RAG, and MCP integrations")
                ],
                "input_handoff": {
                    "source_stage": "Stage 6: Continuous Evaluation, Observability & Guardrails",
                    "artifacts": ["Validated Agent Workflows", "Model Serving Containers", "Guardrail Rulesets"],
                    "format": "Docker Images / Helm Charts"
                },
                "output_handoff": {
                    "next_stage": "End Users / Enterprise API Consumers",
                    "artifacts": ["Production HTTPS API Gateway", "Web UI Portal", "Telemetry Dashboards"],
                    "format": "Web Applications / REST / gRPC"
                },
                "dependencies": ["Kubernetes / Docker Compose", "Reverse Proxy (Traefik / Nginx / Envoy)", "Redis for Rate Limiting"],
                "alternatives": [
                    {"name": "ray-project/ray", "tradeoff": "Massive distributed computing and Ray Serve scaling, heavier operational footprint"},
                    {"name": "kserve/kserve", "tradeoff": "Kubernetes-native standard serving on Knative/Istio, complex control-plane prerequisites"}
                ],
                "quality_gate": "Gate 7: 99.95% API Availability SLA, Sub-200ms Non-Streaming Latency Overhead, Zero-Trust TLS 1.3 Encryption"
            }
        ]
    },

    # --------------------------------------------------------------------------
    # 2. CROSS-PLATFORM MOBILE APP WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-002",
        "name": "Cross-Platform Mobile Application Development Lifecycle",
        "domain": "Mobile Engineering & Cross-Platform Applications",
        "description": "End-to-end multi-stage architecture for high-performance cross-platform mobile apps (iOS, Android, Desktop), bridging declarative design systems, reactive unidirectional state management, local-first offline relational persistence, native platform channels & hardware APIs, resilient networking, automated UI regression testing, and automated store release deployment.",
        "total_stages": 7,
        "governance": {
            "quality_gate_standard": "Mobile App Store Excellence & Zero-Crash Standard",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Cross-Platform UI Framework & Design System",
                "purpose": "Establish high-performance declarative UI architecture, compile responsive multi-screen layouts, and enforce tokenized theme standards across iOS and Android.",
                "recommended_repositories": [
                    fetch_repo_meta("flutter/flutter", "Google's multi-platform UI toolkit compiled natively to ARM64 machine code via Skia/Impeller"),
                    fetch_repo_meta("react/react-native", "Industry-leading framework for building native Android and iOS apps using React and Hermes JS engine"),
                    fetch_repo_meta("expo/expo", "Ecosystem of universal tools and SDKs for React Native with file-based routing and EAS builds")
                ],
                "input_handoff": {
                    "source_stage": "Figma / UI/UX Design Token Specifications",
                    "artifacts": ["Design Tokens (JSON)", "Responsive Screen Layouts", "Component Wireframes", "Asset Bundles"],
                    "format": "Figma Tokens / SVG"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: State Management & Reactive Dataflow",
                    "artifacts": ["Reusable Component Library", "Theme Context Providers", "Dynamic Route Navigation Tree"],
                    "format": "Dart / TypeScript React Native Code"
                },
                "dependencies": ["Flutter SDK 3.x / Node.js 20+ with React Native CLI", "Android Studio (SDK 34) & Xcode 15+", "Hermes / Impeller Runtime"],
                "alternatives": [
                    {"name": "tauri-apps/tauri", "tradeoff": "Rust-powered lightweight webview wrapper, minimal binary size, less native feel on complex mobile touch gestures"},
                    {"name": "JetBrains/compose-multiplatform", "tradeoff": "Kotlin Multiplatform native UI, rapid Android code sharing, evolving iOS ecosystem"}
                ],
                "quality_gate": "Gate 1: 60/120 FPS Jitter-Free Scroll Rendering on Target Mobile Baseline Hardware"
            },
            {
                "stage_id": 2,
                "stage_name": "State Management & Reactive Dataflow",
                "purpose": "Architect predictable unidirectional state management, isolate business logic from UI widgets, and implement atomic reactive subscriptions.",
                "recommended_repositories": [
                    fetch_repo_meta("pmndrs/zustand", "Small, fast and scalable bearbones state-management using simplified flux principles for React Native"),
                    fetch_repo_meta("reduxjs/redux", "Predictable state container with Redux Toolkit (RTK) for immutable state and middleware pipelines")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Cross-Platform UI Framework & Design System",
                    "artifacts": ["UI Component Hierarchy", "User Action Events", "Form Input Payloads"],
                    "format": "Code Modules"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: Offline-First Embedded Storage & Edge DB",
                    "artifacts": ["Global Store Definitions", "Selectors & Reducers", "Action Dispatch Handlers"],
                    "format": "Typed Stores (TypeScript / Dart Riverpod)"
                },
                "dependencies": ["TypeScript 5.x / Dart 3.x", "Zustand / Redux Toolkit / Riverpod"],
                "alternatives": [
                    {"name": "rrousselGit/riverpod", "tradeoff": "Compile-safe dependency injection and state management for Flutter, steep learning curve"},
                    {"name": "felangel/bloc", "tradeoff": "Strict enterprise BLoC pattern for Flutter, highly testable but involves boilerplate"}
                ],
                "quality_gate": "Gate 2: 100% Unidirectional Dataflow Audit and Zero Unnecessary Re-render Cycles"
            },
            {
                "stage_id": 3,
                "stage_name": "Offline-First Embedded Storage & Edge DB",
                "purpose": "Provide instant local reads and writes, relational schema migration, and encrypted disk storage with background cloud synchronization.",
                "recommended_repositories": [
                    fetch_repo_meta("tursodatabase/turso", "Distributed database powered by libSQL (open-source SQLite fork) with embedded replica sync"),
                    fetch_repo_meta("typeorm/typeorm", "ORM for TypeScript with support for Cordova/React Native SQLite storage engines")
                ],
                "input_handoff": {
                    "source_stage": "Stage 2: State Management & Reactive Dataflow",
                    "artifacts": ["Domain Entity Models", "Local Query Schemas", "Sync Conflict Policies"],
                    "format": "TypeScript / Dart Schema Classes"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Native Device Channels & Hardware Telemetry",
                    "artifacts": ["Encrypted SQLite Database Instances", "Local Repositories & DAO Interfaces", "Offline Sync Queue Engine"],
                    "format": "SQLite / libSQL Embedded Storage"
                },
                "dependencies": ["libSQL / SQLite3 C bindings", "SQLCipher for encryption", "AsyncStorage / MMKV Native Module"],
                "alternatives": [
                    {"name": "Nozbe/WatermelonDB", "tradeoff": "Lazy-loading SQLite architecture for React Native, complex setup for non-React Native targets"},
                    {"name": "realm/realm-js", "tradeoff": "Fast object-oriented embedded engine, larger binary footprint and proprietary licensing concerns"}
                ],
                "quality_gate": "Gate 3: Sub-5ms Local Query Latency and Deterministic Offline-to-Online Conflict Resolution"
            },
            {
                "stage_id": 4,
                "stage_name": "Native Device Channels & Hardware Telemetry",
                "purpose": "Bridge cross-platform code to native iOS/Android hardware sensors (Camera, Biometrics, Bluetooth BLE, Geolocation, Background Workers).",
                "recommended_repositories": [
                    fetch_repo_meta("expo/expo", "Comprehensive universal native API modules covering camera, sensors, filesystem, and notifications"),
                    fetch_repo_meta("flutter/flutter", "Low-latency asynchronous Platform Channels communicating directly with Kotlin/Swift host runtimes")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: Offline-First Embedded Storage & Edge DB",
                    "artifacts": ["Hardware Permission Requests", "Sensor Sampling Frequencies", "Background Worker Callbacks"],
                    "format": "API Declarations"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Network Resilience & API Interfacing",
                    "artifacts": ["Hardware Controller Facades", "Biometric Auth Tokens", "Location / Camera Frame Streams"],
                    "format": "Event Streams / Observables"
                },
                "dependencies": ["iOS Info.plist & Android AndroidManifest.xml permissions", "Platform channel bridges"],
                "alternatives": [
                    {"name": "react-native-sensors", "tradeoff": "Direct sensor streaming for React Native, requires manual permission and maintenance hooks"},
                    {"name": "flutter_blue_plus", "tradeoff": "Specialized BLE library for Flutter, focused strictly on Bluetooth Low Energy"}
                ],
                "quality_gate": "Gate 4: Graceful Permission Rejection Handling and Zero Native Memory Leaks across Background App State Transitions"
            },
            {
                "stage_id": 5,
                "stage_name": "Network Resilience & API Interfacing",
                "purpose": "Execute resilient network requests with automatic exponential backoff, request batching, SSL pinning, and payload compression.",
                "recommended_repositories": [
                    fetch_repo_meta("react/react-native", "Native fetch with SSL Certificate Pinning and HTTP/2 multiplexing support"),
                    fetch_repo_meta("pmndrs/zustand", "Reactive caching and optimistic UI updates based on network fetch states")
                ],
                "input_handoff": {
                    "source_stage": "Stage 4: Native Device Channels",
                    "artifacts": ["OpenAPI / gRPC Specifications", "JWT Auth Tokens", "Retry Configuration"],
                    "format": "JSON / Proto3"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Automated UI Testing & Device Lab Verification",
                    "artifacts": ["Typed API Client SDK", "Request Interceptor Stack", "Network Error Handler"],
                    "format": "TypeScript / Dart Client Packages"
                },
                "dependencies": ["HTTP/2 or HTTP/3 Protocol Support", "SSL Pinning Certificates", "Network Reachability Monitor"],
                "alternatives": [
                    {"name": "TanStack/query", "tradeoff": "World-class query caching for React Native, adds external library footprint"},
                    {"name": "cfug/dio", "tradeoff": "Premier Dart HTTP client with interceptors and FormData support for Flutter"}
                ],
                "quality_gate": "Gate 5: Network Timeout Handling under Simulated 2G/3G Packet Drop and SSL Certificate Verification"
            },
            {
                "stage_id": 6,
                "stage_name": "Automated UI Testing & Device Lab Verification",
                "purpose": "Run deterministic black-box and grey-box end-to-end integration tests across real physical devices and emulators with visual regression checks.",
                "recommended_repositories": [
                    fetch_repo_meta("mobile-dev-inc/Maestro", "Modern, declarative, multi-platform UI test automation framework built for mobile apps"),
                    fetch_repo_meta("appium/appium", "Cross-platform test automation tool for native, hybrid and mobile web apps")
                ],
                "input_handoff": {
                    "source_stage": "Stage 5: Network Resilience & API Interfacing",
                    "artifacts": ["Compiled iOS (.ipa/.app) and Android (.apk/.aab) Debug Builds", "User Journey Test Scripts"],
                    "format": "Application Binaries & YAML Flows"
                },
                "output_handoff": {
                    "next_stage": "Stage 7: CI/CD Pipeline, App Store Signing & Telemetry",
                    "artifacts": ["E2E Test Execution Reports", "Screen Recording Artifacts", "Visual Diff Screenshots"],
                    "format": "JUnit XML / HTML Test Reports"
                },
                "dependencies": ["Android Emulator / iOS Simulator or Device Farm", "Maestro CLI / Node.js runtime"],
                "alternatives": [
                    {"name": "wix/Detox", "tradeoff": "Grey-box synchronization for React Native, faster than Appium but sensitive to framework versions"},
                    {"name": "leancodepl/patrol", "tradeoff": "Flutter-first testing tool enabling native permission and system dialog interactions"}
                ],
                "quality_gate": "Gate 6: 100% Core Checkout & Auth Flows Passing Across iOS 16-18 and Android 12-14"
            },
            {
                "stage_id": 7,
                "stage_name": "CI/CD Pipeline, App Store Signing & Telemetry",
                "purpose": "Automate cryptographic code signing, provisioning profile management, App Store / Google Play distribution, and real-time crash reporting.",
                "recommended_repositories": [
                    fetch_repo_meta("fastlane/fastlane", "Industry standard tool to automate building and releasing your iOS and Android apps"),
                    fetch_repo_meta("getsentry/sentry", "Real-time error tracking and performance monitoring with deep mobile stack traces")
                ],
                "input_handoff": {
                    "source_stage": "Stage 6: Automated UI Testing & Device Lab Verification",
                    "artifacts": ["Release Candidate Source Tag", "Apple Distribution Certificates", "Google Play Service Account Key"],
                    "format": "Git Commit / Cryptographic Keystores"
                },
                "output_handoff": {
                    "next_stage": "Apple App Store / Google Play Store",
                    "artifacts": ["Signed Android App Bundle (.aab)", "Signed iOS Binary (.ipa)", "Symbolication dSYM & Proguard Mapping Files"],
                    "format": "Production Store Artifacts"
                },
                "dependencies": ["Apple Developer Program Account", "Google Play Developer Account", "Fastlane Fastfile & Match Git Repository"],
                "alternatives": [
                    {"name": "expo/eas-cli", "tradeoff": "Managed cloud building and submission for Expo/React Native, fee-based cloud service"},
                    {"name": "firebase/firebase-crashlytics", "tradeoff": "Google-backed free crash reporting, proprietary telemetry telemetry pipeline"}
                ],
                "quality_gate": "Gate 7: Automated Match Cryptographic Signing, Zero Crash-Free Session Degradation (<0.1% crash rate)"
            }
        ]
    },

    # --------------------------------------------------------------------------
    # 3. CLOUD-NATIVE KUBERNETES DEVOPS WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-003",
        "name": "Cloud-Native Kubernetes & GitOps Platform Engineering Workflow",
        "domain": "DevOps, Cloud-Native Infrastructure & Platform Engineering",
        "description": "Production-ready 7-stage Kubernetes infrastructure lifecycle implementing declarative Infrastructure-as-Code, immutable packaging, automated GitOps cluster reconciliation, eBPF service mesh and ingress routing, zero-trust secrets management, full-stack metrics/tracing observability, and security posture enforcement.",
        "total_stages": 7,
        "governance": {
            "quality_gate_standard": "Production Cloud-Native Architecture & Zero-Drift GitOps Standard",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Declarative Infrastructure as Code Provisioning",
                "purpose": "Provision immutable VPC networks, managed Kubernetes clusters (EKS/GKE/Talos), and cloud resource backbones with state-locking.",
                "recommended_repositories": [
                    fetch_repo_meta("hashicorp/terraform", "Declarative Infrastructure as Code engine delivering reproducible cloud provisioning via HCL"),
                    fetch_repo_meta("opentofu/manifesto", "Open-source, community-driven Infrastructure as Code engine maintaining open governance"),
                    fetch_repo_meta("gruntwork-io/terragrunt", "Thin wrapper that provides extra tools for keeping Terraform configurations DRY and modular")
                ],
                "input_handoff": {
                    "source_stage": "Cloud Architecture Design / Network Topology Spec",
                    "artifacts": ["VPC Architecture Blueprint", "CIDR Block Allocations", "IAM Role Mapping Matrix"],
                    "format": "HCL / JSON"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: Package Management & Application Templating",
                    "artifacts": ["Live Kubernetes Clusters", "Kubeconfig Credentials", "VPC & Subnet IDs", "IAM OIDC Providers"],
                    "format": "Terraform State / Kubeconfig YAML"
                },
                "dependencies": ["AWS / GCP / Azure / Hetzner Cloud API Keys", "Terraform / OpenTofu CLI", "S3 / GCS Remote State Backend with DynamoDB Locking"],
                "alternatives": [
                    {"name": "pulumi/pulumi", "tradeoff": "General-purpose programming languages (TypeScript, Python, Go) for IaC, higher complexity than HCL"},
                    {"name": "crossplane/crossplane", "tradeoff": "Kubernetes-native control plane managing cloud infrastructure via CRDs, requires existing K8s cluster"}
                ],
                "quality_gate": "Gate 1: Idempotent terraform plan with Zero Unintended Destruction and Strict Static Policy Verification"
            },
            {
                "stage_id": 2,
                "stage_name": "Package Management & Application Templating",
                "purpose": "Package containerized microservices into parameterized, versioned, and reusable application manifests with dependency resolution.",
                "recommended_repositories": [
                    fetch_repo_meta("helm/helm", "The package manager for Kubernetes managing charts with parameterized values and lifecycle hooks"),
                    fetch_repo_meta("helm/charts", "Curated collection of production-grade Kubernetes deployment chart blueprints")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Declarative Infrastructure as Code Provisioning",
                    "artifacts": ["Container Image Digest Tags", "Service Configuration Variables", "Resource CPU/Memory Limit Requests"],
                    "format": "Docker Image SHAs / YAML Values"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: GitOps Continuous Delivery & Cluster Reconciliation",
                    "artifacts": ["Versioned Helm Charts (.tgz / OCI Registries)", "Rendered Kubernetes Manifests", "Chart.yaml Contracts"],
                    "format": "OCI Artifacts / Helm Package"
                },
                "dependencies": ["Kubernetes 1.28+", "Helm CLI v3.x", "OCI Artifact Registry (GHCR / Harbor / ECR)"],
                "alternatives": [
                    {"name": "kubernetes-sigs/kustomize", "tradeoff": "Template-free overlay engine built into kubectl, simpler for minor patches but lacks release management"},
                    {"name": "stefanprodan/timoni", "tradeoff": "CUE-powered package manager for Kubernetes with strong type validation, smaller community"}
                ],
                "quality_gate": "Gate 2: Helm Lint Validation, Schema Compliance Check, and Vulnerability Scan on Target Base Images"
            },
            {
                "stage_id": 3,
                "stage_name": "GitOps Continuous Delivery & Cluster Reconciliation",
                "purpose": "Maintain zero-drift declarative state between Git repositories and live Kubernetes clusters via continuous automated reconciliation.",
                "recommended_repositories": [
                    fetch_repo_meta("argoproj/argo-cd", "Declarative, GitOps continuous delivery tool for Kubernetes with automated self-healing and sync windows")
                ],
                "input_handoff": {
                    "source_stage": "Stage 2: Package Management & Application Templating",
                    "artifacts": ["GitOps Fleet Configuration Repository", "ApplicationSet Manifests", "Target Environment Values"],
                    "format": "Git Commits"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Service Mesh, Ingress & eBPF Networking",
                    "artifacts": ["Synced Cluster Workloads", "Reconciliation Audit History", "Health Status Metrics"],
                    "format": "Kubernetes API State"
                },
                "dependencies": ["ArgoCD Controller installed on target cluster", "Git Deploy Keys with Read Access", "RBAC Service Accounts"],
                "alternatives": [
                    {"name": "fluxcd/flux2", "tradeoff": "Modular GitOps toolkit based on native K8s controllers, lighter UI but excellent multi-tenancy"},
                    {"name": "weaveworks/flagger", "tradeoff": "Progressive delivery operator managing canary releases, works on top of ArgoCD/Flux"}
                ],
                "quality_gate": "Gate 3: Automated Sync Verification with Zero Configuration Drift (Sync Status: Synced, Health: Healthy)"
            },
            {
                "stage_id": 4,
                "stage_name": "Service Mesh, Ingress & eBPF Networking",
                "purpose": "Provide high-performance eBPF-based pod routing, Layer 7 traffic management, mutual TLS (mTLS) encryption, and Gateway API ingress.",
                "recommended_repositories": [
                    fetch_repo_meta("cilium/cilium", "eBPF-powered networking, observability, and security connecting Kubernetes workloads with zero sidecar overhead"),
                    fetch_repo_meta("istio/istio", "Industry-standard service mesh providing traffic routing, mTLS security, and fine-grained authorization"),
                    fetch_repo_meta("linkerd/linkerd2", "Ultralight, security-focused service mesh for Kubernetes written in Rust and Go")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: GitOps Continuous Delivery & Cluster Reconciliation",
                    "artifacts": ["Ingress Route Definitions", "TLS Domain Certificates", "NetworkPolicy / CiliumNetworkPolicy Specifications"],
                    "format": "YAML Manifests"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Zero-Trust Security, Secret Storage & Vulnerability Scanning",
                    "artifacts": ["Encrypted L7 Service Mesh Fabric", "Ingress Gateway Endpoints", "Network Telemetry Streams (Hubble)"],
                    "format": "eBPF BPF Maps / Envoy Dynamic Routes"
                },
                "dependencies": ["Linux Kernel 5.4+ with eBPF support", "Cilium CNI / Istio Operator", "Cert-Manager for Let's Encrypt TLS"],
                "alternatives": [
                    {"name": "traefik/traefik", "tradeoff": "Lightweight cloud-native HTTP reverse proxy and ingress, simpler than full service mesh"},
                    {"name": "envoyproxy/gateway", "tradeoff": "Official Envoy Gateway API implementation, growing community"}
                ],
                "quality_gate": "Gate 4: 100% Inter-Pod Traffic Enforced via mTLS and Default-Deny Ingress Network Policies"
            },
            {
                "stage_id": 5,
                "stage_name": "Zero-Trust Security, Secret Storage & Vulnerability Scanning",
                "purpose": "Inject secrets dynamically without disk persistence, audit container vulnerabilities in CI and runtime, and enforce admission controller policies.",
                "recommended_repositories": [
                    fetch_repo_meta("hashicorp/vault", "Tool for secrets management, encryption as a service, and privileged access management"),
                    fetch_repo_meta("aquasecurity/trivy", "Comprehensive vulnerability and misconfiguration scanner for containers, Kubernetes, and code")
                ],
                "input_handoff": {
                    "source_stage": "Stage 4: Service Mesh, Ingress & eBPF Networking",
                    "artifacts": ["Container Images", "Secret Ingestion Declarations", "Pod Security Admission Profiles"],
                    "format": "OCI Images / ExternalSecret CRDs"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Full-Stack Observability, Tracing & APM Telemetry",
                    "artifacts": ["In-Memory Ephemeral Secret Mounts", "Trivy Security Audit Reports", "Admission Control Approval Tokens"],
                    "format": "Audit JSON / Attestation Signatures"
                },
                "dependencies": ["HashiCorp Vault or Cloud KMS (KMS/Secrets Manager)", "External Secrets Operator", "Kubernetes Admission Webhooks"],
                "alternatives": [
                    {"name": "kyverno/kyverno", "tradeoff": "Kubernetes native policy engine without requiring Rego (unlike OPA/Gatekeeper)"},
                    {"name": "falcosecurity/falco", "tradeoff": "Runtime eBPF threat detection engine alerting on unexpected kernel syscalls"}
                ],
                "quality_gate": "Gate 5: Zero Critical/High CVEs in Runtime Containers and 100% In-Flight Secret Injection"
            },
            {
                "stage_id": 6,
                "stage_name": "Full-Stack Observability, Tracing & APM Telemetry",
                "purpose": "Ingest high-cardinality metrics, aggregate distributed traces across microservices, and render unified operational dashboards with alerting rules.",
                "recommended_repositories": [
                    fetch_repo_meta("prometheus/prometheus", "Cloud-native systems monitoring and alerting toolkit with dimensional data model and PromQL"),
                    fetch_repo_meta("grafana/grafana", "Leading open-source observability visualization and interactive analytics platform")
                ],
                "input_handoff": {
                    "source_stage": "Stage 5: Zero-Trust Security, Secret Storage",
                    "artifacts": ["Service Metrics Scrape Endpoints (/metrics)", "OpenTelemetry Trace Exporters", "Log Stream Sinks"],
                    "format": "Prometheus Exposition Format / OTLP"
                },
                "output_handoff": {
                    "next_stage": "Stage 7: Reliability Verification & Auto-Healing Cluster Operations",
                    "artifacts": ["Grafana Executive Dashboards", "Alertmanager PagerDuty/Slack Routes", "SLO / SLA Error Budget Trackers"],
                    "format": "Prometheus Rules / Grafana JSON Dashboards"
                },
                "dependencies": ["Prometheus Operator (kube-prometheus-stack)", "OpenTelemetry Collector DaemonSet", "Persistent Volumes for TSDB"],
                "alternatives": [
                    {"name": "VictoriaMetrics/VictoriaMetrics", "tradeoff": "Cost-effective drop-in replacement for Prometheus with significantly lower RAM/disk usage"},
                    {"name": "grafana/loki", "tradeoff": "Log aggregation system inspired by Prometheus, indexes only labels rather than full text"}
                ],
                "quality_gate": "Gate 6: Golden Signals Monitored (Latency, Traffic, Errors, Saturation) with Sub-30s Alert Trigger Threshold"
            },
            {
                "stage_id": 7,
                "stage_name": "Reliability Verification & Auto-Healing Cluster Operations",
                "purpose": "Implement horizontal pod autoscaling (HPA / KEDA), automated node provisioning, and continuous chaos resilience verification.",
                "recommended_repositories": [
                    fetch_repo_meta("argoproj/argo-cd", "Continuous rollback triggers and automated sync window management"),
                    fetch_repo_meta("prometheus/prometheus", "Telemetry-driven auto-scaling triggers via PromQL custom metrics")
                ],
                "input_handoff": {
                    "source_stage": "Stage 6: Full-Stack Observability, Tracing & APM Telemetry",
                    "artifacts": ["SLO Thresholds", "Autoscaling Policies (CPU/Memory/Queue Depth)", "Chaos Testing Plans"],
                    "format": "HPA / KEDA ScaledObject CRDs"
                },
                "output_handoff": {
                    "next_stage": "Production Operations & Platform Engineers",
                    "artifacts": ["Auto-Healing Infrastructure", "Chaos Resilience Certification", "Incident Runbooks"],
                    "format": "Production SLA Reports"
                },
                "dependencies": ["Kubernetes Metrics Server / KEDA", "Cluster Autoscaler / Karpenter"],
                "alternatives": [
                    {"name": "chaos-mesh/chaos-mesh", "tradeoff": "Cloud-native chaos engineering platform injecting network delays, pod kills, and I/O faults"},
                    {"name": "kubernetes-sigs/karpenter", "tradeoff": "High-velocity AWS node autoscaler bypassing ASGs, requires AWS EKS"}
                ],
                "quality_gate": "Gate 7: Automated Recovery from Single-Node Outage in under 60 Seconds with Zero User-Perceived Downtime"
            }
        ]
    },

    # --------------------------------------------------------------------------
    # 4. STARTUP FULL-STACK SAAS MVP WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-004",
        "name": "High-Velocity Full-Stack SaaS MVP Engineering Workflow",
        "domain": "Full-Stack Web Engineering & SaaS Product Acceleration",
        "description": "Rapid yet resilient architecture for building, validating, and scaling commercial SaaS platforms, covering responsive modern frontend interfaces, type-safe API microservices, distributed relational database and ORM layers, secure multi-tenant authentication, asynchronous distributed queues, and production product analytics.",
        "total_stages": 7,
        "governance": {
            "quality_gate_standard": "Full-Stack SaaS High-Conversion & Security Standard",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Frontend Experience & Design Token System",
                "purpose": "Build ultra-fast, responsive web interfaces with server-side rendering, semantic HTML, accessible UI components, and strict theme tokenization.",
                "recommended_repositories": [
                    fetch_repo_meta("vercel/next.js", "The React framework for the web with App Router, React Server Components (RSC), and edge rendering"),
                    fetch_repo_meta("tailwindlabs/tailwindcss", "A utility-first CSS framework for rapidly building custom user interfaces without context switching")
                ],
                "input_handoff": {
                    "source_stage": "Product Wireframes / User Journey Design",
                    "artifacts": ["Brand Styleguide", "UX Component Hierarchy", "Route Map"],
                    "format": "Figma / Markdown"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: Type-Safe Backend API & Business Services",
                    "artifacts": ["App Router Page Templates", "Reusable UI Component Tree", "Optimized Image Assets", "Global Theme Provider"],
                    "format": "React / Next.js TypeScript Code"
                },
                "dependencies": ["Node.js 20+ / pnpm", "Next.js 14/15 App Router", "Tailwind CSS v3/v4"],
                "alternatives": [
                    {"name": "sveltejs/kit", "tradeoff": "Compiler-driven reactive web framework with exceptional performance and simpler syntax than React"},
                    {"name": "remix-run/remix", "tradeoff": "Web standard-focused full-stack framework with nested routing and robust form actions"}
                ],
                "quality_gate": "Gate 1: Lighthouse Performance & Accessibility Score >= 95 with Zero Cumulative Layout Shift (CLS < 0.1)"
            },
            {
                "stage_id": 2,
                "stage_name": "Type-Safe Backend API & Business Services",
                "purpose": "Develop high-performance REST and RPC microservices with automatic OpenAPI generation, strict payload validation, and middleware pipelines.",
                "recommended_repositories": [
                    fetch_repo_meta("fastapi/fastapi", "High-performance Python web framework for building APIs with Pydantic type hints and Starlette"),
                    fetch_repo_meta("nestjs/nest", "Progressive TypeScript framework for building scalable enterprise-grade backend server architectures"),
                    fetch_repo_meta("honojs/hono", "Ultrafast, lightweight web framework built on Web Standards that runs on any JavaScript runtime (Cloudflare Workers, Node, Deno)")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Frontend Experience & Design Token System",
                    "artifacts": ["Frontend Data Contract Requirements", "Service Interface Specifications", "Business Validation Rules"],
                    "format": "TypeScript Types / OpenAPI Draft"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: Database Architecture & Relational Persistence",
                    "artifacts": ["Validated REST / GraphQL / RPC Endpoints", "Auto-Generated OpenAPI / Swagger Documentation", "Shared Type Contracts"],
                    "format": "OpenAPI v3 JSON / TypeScript SDK"
                },
                "dependencies": ["Python 3.11+ / Node.js 20+", "FastAPI / NestJS / Hono CLI", "Uvicorn / Node Runtime"],
                "alternatives": [
                    {"name": "trpc/trpc", "tradeoff": "End-to-end typesafe APIs without code generation for full-stack TypeScript teams"},
                    {"name": "gin-gonic/gin", "tradeoff": "Blazing fast Golang HTTP web framework, highest raw request throughput, more verbose boilerplate"}
                ],
                "quality_gate": "Gate 2: 100% Type-Safe API Contracts and Sub-15ms Core Endpoint Response Times"
            },
            {
                "stage_id": 3,
                "stage_name": "Database Architecture & Relational Persistence",
                "purpose": "Model relational schemas, manage automated SQL migrations, enforce foreign key integrity, and provide type-safe queries via modern ORM.",
                "recommended_repositories": [
                    fetch_repo_meta("supabase/supabase", "The open source Firebase alternative providing PostgreSQL with Row-Level Security, Auth, and Realtime"),
                    fetch_repo_meta("prisma/orm", "Next-generation Node.js and TypeScript ORM with declarative modeling and automated migrations"),
                    fetch_repo_meta("drizzle-team/drizzle-orm", "Lightweight TypeScript ORM with maximum type-safety, zero dependencies, and SQL-like syntax")
                ],
                "input_handoff": {
                    "source_stage": "Stage 2: Type-Safe Backend API & Business Services",
                    "artifacts": ["Domain Entity Relationship Diagrams", "Query Access Patterns", "Multi-Tenant Partition Keys"],
                    "format": "DBML / ERD"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Multi-Tenant Authentication & Session Security",
                    "artifacts": ["PostgreSQL Production Database", "Applied Migration Scripts", "Type-Safe Client DB Instances"],
                    "format": "SQL Schema / TypeScript Client"
                },
                "dependencies": ["PostgreSQL 15+ Instance (Local or Supabase / Neon)", "Prisma / Drizzle CLI", "PgBouncer Connection Pooler"],
                "alternatives": [
                    {"name": "sqlalchemy/sqlalchemy", "tradeoff": "Battle-tested Python SQL toolkit and Object Relational Mapper for FastAPI systems"},
                    {"name": "planetscale/vitess", "tradeoff": "Horizontally scalable distributed MySQL clustering for hyper-growth SaaS platforms"}
                ],
                "quality_gate": "Gate 3: Enforced Foreign Key Constraints, Clean Rollback-Capable Migration Files, and Index Optimization on All Filter Keys"
            },
            {
                "stage_id": 4,
                "stage_name": "Multi-Tenant Authentication & Session Security",
                "purpose": "Implement secure authentication, role-based access control (RBAC), OAuth social logins, session management, and multi-tenant organization tenancy.",
                "recommended_repositories": [
                    fetch_repo_meta("better-auth/better-auth", "The most advanced TypeScript authentication framework supporting 2FA, OAuth, Passkeys, and multi-tenant teams"),
                    fetch_repo_meta("appwrite/appwrite", "Self-hosted backend server for web and mobile developers providing auth, databases, functions, and security")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: Database Architecture & Relational Persistence",
                    "artifacts": ["User & Organization Schema Tables", "OAuth Provider Client Credentials", "Session TTL Policies"],
                    "format": "SQL Tables & Environment Secrets"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Billing, Subscription & Webhook Processing",
                    "artifacts": ["Protected API Route Middleware", "Auth Session Tokens (JWT / Encrypted Cookies)", "Tenant Context Resolvers"],
                    "format": "HTTP Headers / Cookies"
                },
                "dependencies": ["Redis or PostgreSQL for Session Storage", "OAuth 2.0 Provider Applications (Google, GitHub)", "Web Crypto API"],
                "alternatives": [
                    {"name": "nextauthjs/next-auth", "tradeoff": "Ubiquitous Auth.js library for Next.js, evolving v5 upgrade path"},
                    {"name": "clerk/javascript", "tradeoff": "Fully managed enterprise authentication SaaS, fastest UI drop-in, monthly per-MAU fee"}
                ],
                "quality_gate": "Gate 4: OWASP Top 10 Auth Protection: HttpOnly Secure SameSite Cookies, CSRF Prevention, and Timing-Attack Safe Verification"
            },
            {
                "stage_id": 5,
                "stage_name": "Billing, Subscription & Webhook Processing",
                "purpose": "Monetize the SaaS platform with tiered subscriptions, usage-based metering, self-service customer portals, and idempotent webhook processors.",
                "recommended_repositories": [
                    fetch_repo_meta("better-auth/better-auth", "Built-in subscription and organization billing integration plugins"),
                    fetch_repo_meta("supabase/supabase", "PostgreSQL database storing customer IDs, active entitlements, and webhook event logs")
                ],
                "input_handoff": {
                    "source_stage": "Stage 4: Multi-Tenant Authentication & Session Security",
                    "artifacts": ["Pricing Tier Definitions", "Feature Flag Matrices", "Payment Gateway API Keys"],
                    "format": "JSON Config"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Asynchronous Queues & Background Job Processing",
                    "artifacts": ["Idempotent Webhook Handler Endpoints", "Customer Subscription Entitlement Cache", "Payment Audit Trail"],
                    "format": "Event Handlers / Database Records"
                },
                "dependencies": ["Stripe / Lemon Squeezy Merchant Account", "Stripe CLI for local webhook forwarding", "Cryptographic Webhook Secret"],
                "alternatives": [
                    {"name": "polar-sh/polar", "tradeoff": "Open-source developer monetization platform with native Next.js and GitHub sponsorship tiers"},
                    {"name": "autumn-api/autumn", "tradeoff": "Modern pricing and usage billing engine with flexible pay-as-you-go architecture"}
                ],
                "quality_gate": "Gate 5: Cryptographic Webhook Signature Verification and Idempotency Handling Preventing Double-Billing"
            },
            {
                "stage_id": 6,
                "stage_name": "Asynchronous Queues & Background Job Processing",
                "purpose": "Offload long-running tasks (email notifications, PDF rendering, AI generation, data exports) to distributed background workers.",
                "recommended_repositories": [
                    fetch_repo_meta("taskforcesh/bullmq", "Fast, robust, Redis-based distributed message queue and batch job processing engine for Node.js / TypeScript"),
                    fetch_repo_meta("celery/celery", "Distributed task queue system focused on real-time processing and task scheduling in Python"),
                    fetch_repo_meta("temporalio/temporal", "Durable execution platform executing resilient, stateful, and fault-tolerant distributed workflows")
                ],
                "input_handoff": {
                    "source_stage": "Stage 5: Billing, Subscription & Webhook Processing",
                    "artifacts": ["Async Task Payloads", "Cron Schedule Definitions", "Retry & Dead-Letter Queue (DLQ) Rules"],
                    "format": "JSON Message Payloads"
                },
                "output_handoff": {
                    "next_stage": "Stage 7: Production Observability, Product Analytics & Edge Hosting",
                    "artifacts": ["Processed Job Receipts", "Background Worker Fleet", "Dead Letter Queue Dashboard"],
                    "format": "Redis / RabbitMQ Stream Messages"
                },
                "dependencies": ["Redis 7.x (Upstash / Redis Cloud / Self-hosted)", "Worker Compute Runtimes", "Sentry Integration for Failed Tasks"],
                "alternatives": [
                    {"name": "inngest/inngest", "tradeoff": "Event-driven serverless background jobs without managing Redis instances"},
                    {"name": "triggerdotdev/trigger.dev", "tradeoff": "Open-source background jobs framework with full TypeScript support and live monitoring UI"}
                ],
                "quality_gate": "Gate 6: Exponential Backoff Retries with Tiered DLQ Isolation and Zero Lost Task Guarantees"
            },
            {
                "stage_id": 7,
                "stage_name": "Production Observability, Product Analytics & Edge Hosting",
                "purpose": "Deploy full-stack application to edge infrastructure, track user conversion funnels, capture session replays, and monitor uptime.",
                "recommended_repositories": [
                    fetch_repo_meta("PostHog/posthog", "Open-source product analytics, session recording, feature flags, A/B testing, and user feedback platform"),
                    fetch_repo_meta("appwrite/appwrite", "Self-hosted scalable microservice infrastructure alternative for private cloud deployments")
                ],
                "input_handoff": {
                    "source_stage": "Stage 6: Asynchronous Queues & Background Job Processing",
                    "artifacts": ["Production Build Artifacts", "Telemetry Tracking Plan", "Domain SSL Certificates"],
                    "format": "Deploy Packages / Git Tag"
                },
                "output_handoff": {
                    "next_stage": "Active SaaS Customers & Growth Marketers",
                    "artifacts": ["Live Global HTTPS Production Web Application", "Conversion Funnel Dashboards", "Session Replay Explorer"],
                    "format": "Web Portal / Analytics BI"
                },
                "dependencies": ["Vercel / Coolify / Dokku / Cloudflare Host", "DNS Nameservers", "PostHog Analytics API Keys"],
                "alternatives": [
                    {"name": "coolify-io/coolify", "tradeoff": "Self-hosted, open-source Heroku/Netlify/Vercel alternative on your own VPS with zero vendor lock-in"},
                    {"name": "dokku/dokku", "tradeoff": "Lightweight, Docker-powered mini-Heroku on a single Linux server"}
                ],
                "quality_gate": "Gate 7: Automated Zero-Downtime Deployment, 99.9% Uptime SLA, and Full Funnel Analytics Event Ingestion"
            }
        ]
    },

    # --------------------------------------------------------------------------
    # 5. CYBERSECURITY & PENETRATION TESTING LAB WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-005",
        "name": "Cybersecurity, Penetration Testing & Vulnerability Research Lab Workflow",
        "domain": "Cybersecurity, Red Teaming & Offensive Security Engineering",
        "description": "Rigorous 6-stage red teaming and binary analysis workflow spanning external reconnaissance and OSINT, automated vulnerability probing, weaponized exploitation and C2 orchestration, deep binary reverse engineering and decompilation, privilege escalation with Active Directory attack graph mapping, and structured vulnerability reporting.",
        "total_stages": 6,
        "governance": {
            "quality_gate_standard": "Authorized Red Team Rules of Engagement & Zero-Collateral Standard",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Attack Surface Reconnaissance & OSINT Asset Discovery",
                "purpose": "Discover external target perimeters, enumerate subdomains, map ASN infrastructure, query DNS histories, and correlate exposed HTTP endpoints.",
                "recommended_repositories": [
                    fetch_repo_meta("owasp-amass/amass", "In-depth attack surface mapping and external asset discovery using active and passive OSINT techniques"),
                    fetch_repo_meta("projectdiscovery/subfinder", "Fast and passive subdomain discovery tool built in Go using curated passive data sources")
                ],
                "input_handoff": {
                    "source_stage": "Engagement Scope Document / Authorized Root Domains",
                    "artifacts": ["Target Domain Names", "CIDR IP Ranges", "Rules of Engagement (RoE) Contracts"],
                    "format": "Text / Scope Document"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: Automated Vulnerability Scanning & Dynamic Probing",
                    "artifacts": ["Discovered Subdomain Hostnames", "Resolved IP Addresses", "Active Web Port & HTTP Status Map"],
                    "format": "JSON Lines / Text Lists"
                },
                "dependencies": ["Go 1.22+ / Amass CLI", "Security API Keys (Shodan, Censys, SecurityTrails, VirusTotal)", "Permitted Network Egress"],
                "alternatives": [
                    {"name": "projectdiscovery/httpx", "tradeoff": "Fast multi-purpose HTTP toolkit for probing live web servers and extracting titles/technologies"},
                    {"name": "projectdiscovery/naabu", "tradeoff": "Ultra-fast port scanner written in Go focused on speed and minimal SYN packet overhead"}
                ],
                "quality_gate": "Gate 1: Strict Scope Confinement: Verification that 100% of Discovered Assets Belong Exclusively to Authorized Scope"
            },
            {
                "stage_id": 2,
                "stage_name": "Automated Vulnerability Scanning & Dynamic Probing",
                "purpose": "Execute fast, template-driven vulnerability scans across identified HTTP endpoints, protocols, and network services to detect known CVEs and misconfigurations.",
                "recommended_repositories": [
                    fetch_repo_meta("projectdiscovery/nuclei", "Fast and customizable vulnerability scanner based on simple YAML-based DSL templates"),
                    fetch_repo_meta("projectdiscovery/nuclei-templates", "Community-curated repository of thousands of vulnerability templates covering zero-days and CVEs")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Attack Surface Reconnaissance & OSINT Asset Discovery",
                    "artifacts": ["Live URL Targets", "Open Ports List", "Service Banner Headers"],
                    "format": "URLs / JSON"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: Exploitation & Post-Exploitation Red Teaming",
                    "artifacts": ["Confirmed Vulnerability Findings", "HTTP Request/Response Proof-of-Concepts (PoCs)", "CVSS Severity Scores"],
                    "format": "SARIF / JSON / Markdown"
                },
                "dependencies": ["Nuclei Engine v3.x", "Updated Nuclei Template Database", "Bandwidth-limited Rate Throttling"],
                "alternatives": [
                    {"name": "sullo/nikto", "tradeoff": "Classic web server vulnerability scanner, comprehensive on older legacy systems, slower and noisier than Nuclei"},
                    {"name": "greenbone/openvas-scanner", "tradeoff": "Full enterprise vulnerability management scanner, heavy multi-container footprint"}
                ],
                "quality_gate": "Gate 2: Zero False Positive Verification on Critical/High Findings via Manual Request Replay"
            },
            {
                "stage_id": 3,
                "stage_name": "Exploitation & Post-Exploitation Red Teaming",
                "purpose": "Verify exploitability via controlled payloads, automate SQL injection extraction, test network authentication protocols, and deploy resilient C2 agents.",
                "recommended_repositories": [
                    fetch_repo_meta("rapid7/metasploit-framework", "World's most used penetration testing framework providing automated exploit verification and payloads"),
                    fetch_repo_meta("sqlmapproject/sqlmap", "Automatic SQL injection and database takeover tool detecting and exploiting SQL flaws"),
                    fetch_repo_meta("fortra/impacket", "Collection of Python classes for working with network protocols (SMB, MSRPC, NTLM, Kerberos)"),
                    fetch_repo_meta("BishopFox/sliver", "Adversary emulation and red team command and control (C2) framework supporting mTLS, WireGuard, and DNS")
                ],
                "input_handoff": {
                    "source_stage": "Stage 2: Automated Vulnerability Scanning & Dynamic Probing",
                    "artifacts": ["Validated Vulnerable Endpoints", "Vulnerability Parameter Names", "Authentication Credentials"],
                    "format": "Target Specifications"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Reverse Engineering, Decompilation & Binary Triage",
                    "artifacts": ["Simulated Access Sessions", "Database Dumps (Redacted)", "Dropped Payloads & Command Logs"],
                    "format": "Session Logs / Pcap Traffic Captures"
                },
                "dependencies": ["Kali Linux / Docker Security Suite", "Metasploit Console", "Sliver Server / Client", "Python 3"],
                "alternatives": [
                    {"name": "commixproject/commix", "tradeoff": "Automated command injection exploitation tool, specialized strictly on command execution sinks"},
                    {"name": "praetorian-inc/mythic", "tradeoff": "Modern modular web-based C2 framework with multi-agent orchestration, complex Docker setup"}
                ],
                "quality_gate": "Gate 3: Explicit Operation Logging: Every Executed Command, Payload Hash, and Timestamp Recorded in Tamper-Proof Audit Log"
            },
            {
                "stage_id": 4,
                "stage_name": "Reverse Engineering, Decompilation & Binary Triage",
                "purpose": "Disassemble native binaries, decompile executables into clean C/C++ pseudocode, analyze malware samples, and trace control flow graphs.",
                "recommended_repositories": [
                    fetch_repo_meta("NationalSecurityAgency/ghidra", "Software reverse engineering (SRE) suite developed by NSA for analyzing compiled code on Windows, macOS, Linux"),
                    fetch_repo_meta("radareorg/radare2", "Unix-like reverse engineering framework and command-line toolset for disassembly, debugging, and patching"),
                    fetch_repo_meta("rizinorg/cutter", "Free and open-source GUI for Rizin reverse engineering engine focusing on usability and decompilation")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3 (or External Malware / Firmware Artifacts)",
                    "artifacts": ["Target Executables (.exe / .elf / .dylib)", "Firmware Blobs", "Memory Dumps"],
                    "format": "Raw Binary / PE / ELF / Mach-O"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Privilege Escalation & Lateral Movement Graphing",
                    "artifacts": ["Decompiled C Code", "Identified Vulnerable Sinks (buffer overflows, format strings)", "Function Call Graphs"],
                    "format": "Ghidra Project Archive (.gpr) / JSON AST"
                },
                "dependencies": ["Java 17+ (for Ghidra)", "Radare2 / Rizin native toolchains", "Isolated Sandbox VM / Container"],
                "alternatives": [
                    {"name": "angr/angr", "tradeoff": "Symbolic execution and program analysis framework in Python, mathematically rigorous but resource heavy"},
                    {"name": "Hex-Rays/IDA-Free", "tradeoff": "Freeware tier of industry standard IDA Pro, restricted commercial licensing and feature limits"}
                ],
                "quality_gate": "Gate 4: 100% Function Disassembly Resolution and Memory Safety Vulnerability (CWE-120/122/416) Pinpointing"
            },
            {
                "stage_id": 5,
                "stage_name": "Privilege Escalation & Lateral Movement Graphing",
                "purpose": "Enumerate local privilege escalation vectors on Linux/Windows hosts, map Active Directory identity attack paths, and simulate lateral movement.",
                "recommended_repositories": [
                    fetch_repo_meta("peass-ng/PEASS-ng", "Privilege Escalation Awesome Scripts Suite (LinPEAS / WinPEAS) searching for local misconfigurations"),
                    fetch_repo_meta("SpecterOps/BloodHound-Legacy", "Graph theory-based attack path mapping tool revealing hidden relationships in Active Directory"),
                    fetch_repo_meta("Pennyw0rth/NetExec", "The network execution tool for automating security assessment of large Active Directory networks")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: Exploitation & Post-Exploitation Red Teaming",
                    "artifacts": ["Low-Privilege Shell Sessions", "Domain User Credentials", "Host Environment Variables"],
                    "format": "Interactive Shell / LDAP Access"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Remediation Tracking, Centralized Triage & Compliance Auditing",
                    "artifacts": ["Shortest Path to Domain Admin Graph", "Root Privilege Escalation PoCs", "NTLM / Kerberos Hash Captures"],
                    "format": "BloodHound JSON / LinPEAS Output Text"
                },
                "dependencies": ["BloodHound GUI / Neo4j Graph Database", "SharpHound / BloodHound.py data collector", "NetExec CLI"],
                "alternatives": [
                    {"name": "gentilkiwi/mimikatz", "tradeoff": "Famous credential extraction tool, heavily flagged by every modern EDR/antivirus"},
                    {"name": "GhostPack/Seatbelt", "tradeoff": "C# security triage tool for Windows post-exploitation situational awareness"}
                ],
                "quality_gate": "Gate 5: Non-Destructive Proof Validation (Proof-of-Access through Token Extraction without Modifying Domain Admin Passwords)"
            },
            {
                "stage_id": 6,
                "stage_name": "Remediation Tracking, Centralized Triage & Compliance Auditing",
                "purpose": "Consolidate all discovered vulnerabilities into an actionable vulnerability management system, calculate CVSS v3.1 scores, and provide defensive remediation patches.",
                "recommended_repositories": [
                    fetch_repo_meta("projectdiscovery/nuclei", "Automated re-test validation scripts verifying patch effectiveness post-remediation")
                ],
                "input_handoff": {
                    "source_stage": "All Stages (Recon, Scanning, Exploitation, RE, PrivEsc)",
                    "artifacts": ["Finding Dossiers", "Reproduction Steps", "Network Evidence Logs", "Severity Ratings"],
                    "format": "JSON / Markdown / PCAP"
                },
                "output_handoff": {
                    "next_stage": "CISO / Security Engineering & Development Teams",
                    "artifacts": ["Executive Pentest Summary Report", "Technical Remediation Guidance (Diffs)", "DefectDojo Jira Tickets"],
                    "format": "PDF / Jira Tickets / SARIF"
                },
                "dependencies": ["DefectDojo / Markdown Engine (Pandas / WeasyPrint)", "Jira / GitHub Issues API"],
                "alternatives": [
                    {"name": "DefectDojo/django-DefectDojo", "tradeoff": "Industry standard open-source vulnerability management and correlation platform"},
                    {"name": "dradis/dradis-ce", "tradeoff": "Collaboration and reporting platform for penetration testers, simplified collaboration"}
                ],
                "quality_gate": "Gate 6: 100% Remediation Actionability: Every Discovered Flaw Paired with Concrete Code/Configuration Fix and Retest Script"
            }
        ]
    },

    # --------------------------------------------------------------------------
    # 6. AUTONOMOUS SEO & GROWTH AGENT WORKFLOW
    # --------------------------------------------------------------------------
    {
        "workflow_id": "WORKFLOW-006",
        "name": "Autonomous Search Intelligence, GEO/AEO & Organic Growth Workflow",
        "domain": "Search Engine Optimization, Generative Engine Optimization & Growth Automation",
        "description": "Comprehensive 6-stage algorithmic growth workflow combining headless crawling and DOM extraction, search intent mining and keyword clustering, LLM citability optimization and schema structuring, programmatic content compilation, real-time search engine submission, and privacy-first conversion analytics.",
        "total_stages": 6,
        "governance": {
            "quality_gate_standard": "OmniSearch Growth Dual-Optimization (Traditional SEO + GEO + AEO)",
            "audit_status": "PRODUCTION_READY"
        },
        "stages": [
            {
                "stage_id": 1,
                "stage_name": "Deep Web Crawling, DOM Extraction & Technical SEO Audit",
                "purpose": "Crawl entire website architectures, execute client-side JavaScript, extract clean Markdown and structured metadata, and detect indexing blockers (4xx/5xx, canonical conflicts, robots.txt exclusions).",
                "recommended_repositories": [
                    fetch_repo_meta("firecrawl/firecrawl", "Turn entire websites into clean LLM-ready markdown or structured data with intelligent web crawling"),
                    fetch_repo_meta("scrapy/scrapy", "High-level fast web crawling and screen scraping framework for asynchronous data extraction"),
                    fetch_repo_meta("apify/crawlee", "Web scraping and browser automation library for Node.js with headless Chrome, anti-fingerprinting and proxy rotation")
                ],
                "input_handoff": {
                    "source_stage": "Target Domain URL / Sitemaps",
                    "artifacts": ["Root Domain URL", "XML Sitemap URLs", "Crawl Depth & Rate Limits"],
                    "format": "URL / Robots.txt"
                },
                "output_handoff": {
                    "next_stage": "Stage 2: Search Intent Mining & Keyword Research",
                    "artifacts": ["Clean Markdown DOM Dumps", "Crawl Graph & Internal Link Map", "Technical Error Inventory (broken links, redirect chains)"],
                    "format": "JSON Lines / Markdown"
                },
                "dependencies": ["Node.js 20+ / Python 3.11+", "Headless Chromium / Playwright", "Firecrawl API or Self-Hosted Docker Container"],
                "alternatives": [
                    {"name": "colly/colly", "tradeoff": "Fast and elegant scraping framework for Golang, extreme memory efficiency, requires custom JS rendering integration"},
                    {"name": "gocolly/colly", "tradeoff": "Lightweight scraping without headless browser rendering"}
                ],
                "quality_gate": "Gate 1: 100% Crawl Completion without Rate-Limit Bans, Sub-200ms DOM Parse Speed, and Complete Link Graph Extraction"
            },
            {
                "stage_id": 2,
                "stage_name": "Search Intent Mining & Keyword Research",
                "purpose": "Extract high-opportunity search queries, classify query intent (informational, commercial, navigational, transactional), compute SERP overlap, and cluster keywords into topic hubs.",
                "recommended_repositories": [
                    fetch_repo_meta("coreyhaines31/marketingskills", "Full-stack marketing skills suite covering conversion copywriting, positioning, SEO, and growth loops"),
                    fetch_repo_meta("AgriciDaniel/claude-seo", "Claude-optimized prompt engineering and workflows for autonomous SEO analysis and search clustering")
                ],
                "input_handoff": {
                    "source_stage": "Stage 1: Deep Web Crawling, DOM Extraction & Technical SEO Audit",
                    "artifacts": ["Domain Topic Seed Words", "Competitor Landing Page URLs", "Existing Page Inventory"],
                    "format": "JSON / CSV"
                },
                "output_handoff": {
                    "next_stage": "Stage 3: Semantic Optimization, AEO & LLM Citability Engineering",
                    "artifacts": ["Clustered Topic Architecture (Hub-and-Spoke)", "Target Keyword-to-URL Mapping", "Content Gap Priority Matrix"],
                    "format": "CSV / JSON"
                },
                "dependencies": ["Google Search Console API / Bing Webmaster API", "Python Pandas for TF-IDF / Embeddings Clustering"],
                "alternatives": [
                    {"name": "eliasdabbas/advertools", "tradeoff": "Comprehensive online marketing productivity and analysis Python package with SERP tracking"},
                    {"name": "GeneralMills/pytrends", "tradeoff": "Unofficial API for Google Trends for historical search interest tracking"}
                ],
                "quality_gate": "Gate 2: Topic Clusters Exceed 75% SERP Overlap Threshold and Target Keywords Align 1:1 with Single Search Intent"
            },
            {
                "stage_id": 3,
                "stage_name": "Semantic Optimization, AEO & LLM Citability Engineering",
                "purpose": "Structure content for direct Answer Engine Optimization (AEO - 40-60 word definitive summaries), generate rich Schema.org JSON-LD entities, and produce standardized llms.txt files for AI engine discovery.",
                "recommended_repositories": [
                    fetch_repo_meta("coreyhaines31/marketingskills", "High-converting editorial copy frameworks, value proposition positioning, and headline optimization"),
                    fetch_repo_meta("AgriciDaniel/claude-seo", "Automated E-E-A-T scoring, citability passages, and AI overview optimization prompt chains"),
                    fetch_repo_meta("every-app/open-seo", "Open-source SEO tooling and automated metadata optimization framework")
                ],
                "input_handoff": {
                    "source_stage": "Stage 2: Search Intent Mining & Keyword Research",
                    "artifacts": ["Target Keyword Cluster", "Competitor Outlines", "Primary Domain Entity Attributes"],
                    "format": "JSON Specification"
                },
                "output_handoff": {
                    "next_stage": "Stage 4: Programmatic Content Engine & Rich Asset Generation",
                    "artifacts": ["Validated Schema.org JSON-LD Markup", "40-60 Word Direct Answer Snippets", "llms.txt Specification File", "Optimized Heading Hierarchy (H1-H3)"],
                    "format": "JSON-LD / Markdown"
                },
                "dependencies": ["JSON-LD Validator / Schema.org Vocabulary", "Python / TypeScript Markdown Processors"],
                "alternatives": [
                    {"name": "schema-org/schemaorg", "tradeoff": "Authoritative schema.org repository, reference schema schemas rather than automated code generator"},
                    {"name": "ahrefs/seo-toolbar", "tradeoff": "Browser extension for on-page audit, manual workflow rather than autonomous programmatic execution"}
                ],
                "quality_gate": "Gate 3: 100% Schema.org Rich Result Validation Without Errors and Verified AI Citability Score >= 85/100"
            },
            {
                "stage_id": 4,
                "stage_name": "Programmatic Content Engine & Rich Asset Generation",
                "purpose": "Generate authoritative, non-templated, answer-first articles, comparison tables, and interactive widgets with verified statistics and internal cross-linking.",
                "recommended_repositories": [
                    fetch_repo_meta("coreyhaines31/marketingskills", "Editorial tone calibration, conversion-focused copywriting, and humanized readability guidelines"),
                    fetch_repo_meta("AgriciDaniel/claude-seo", "Structured content generation pipelines adhering strictly to dual search engine optimization standards")
                ],
                "input_handoff": {
                    "source_stage": "Stage 3: Semantic Optimization, AEO & LLM Citability Engineering",
                    "artifacts": ["Content Briefs", "Schema Metadata", "Direct Answers", "Internal Link Target Graph"],
                    "format": "JSON Content Brief"
                },
                "output_handoff": {
                    "next_stage": "Stage 5: Real-Time Indexation, Sitemaps & Search Engine Ingestion",
                    "artifacts": ["Production Markdown / MDX Articles", "Optimized WebP Image Variants", "Structured Data Embeds", "Static HTML Builds"],
                    "format": "Markdown / MDX / HTML"
                },
                "dependencies": ["Markdown Engine (markdown-it / remark)", "Image Optimization Pipeline (Sharp / Libvips)", "Git Commit Pipeline"],
                "alternatives": [
                    {"name": "gohugoio/hugo", "tradeoff": "Fastest static site generator written in Go, compiles thousands of pages in milliseconds"},
                    {"name": "astro-build/astro", "tradeoff": "Component islands web framework, zero client JS by default, excellent for content-driven SEO sites"}
                ],
                "quality_gate": "Gate 4: Flesch-Kincaid Readability Grade 8-10, Zero AI Watermarks, and 100% Valid Internal Anchor Link Graph"
            },
            {
                "stage_id": 5,
                "stage_name": "Real-Time Indexation, Sitemaps & Search Engine Ingestion",
                "purpose": "Generate dynamic XML sitemaps, notify search engines instantaneously via IndexNow protocol, and monitor indexation status via Google Search Console API.",
                "recommended_repositories": [
                    fetch_repo_meta("every-app/open-seo", "Sitemap generator and automated search engine pinging and indexation engine")
                ],
                "input_handoff": {
                    "source_stage": "Stage 4: Programmatic Content Engine & Rich Asset Generation",
                    "artifacts": ["Published URL Slugs", "Last-Modified Timestamps", "Change Frequency Tags"],
                    "format": "URL List / Git Diff"
                },
                "output_handoff": {
                    "next_stage": "Stage 6: Growth Telemetry, Rank Tracking & Conversion Attribution",
                    "artifacts": ["Validated sitemap.xml", "IndexNow Submission Receipts", "Google Search Console Inspection Logs"],
                    "format": "XML / HTTP 200 Confirmation"
                },
                "dependencies": ["IndexNow API Key hosted at domain root", "Google Cloud Service Account with GSC API access", "Automated Cron / Webhook"],
                "alternatives": [
                    {"name": "ekalinin/sitemap.js", "tradeoff": "High-level sitemap-generating library for Node.js, fast streaming for million-URL catalogs"},
                    {"name": "alexp-ssn/indexnow-action", "tradeoff": "GitHub Action for pushing changed URLs to IndexNow on git commit"}
                ],
                "quality_gate": "Gate 5: Automated IndexNow HTTP 200/202 Response and Verification of Valid Sitemaps in GSC without Parse Errors"
            },
            {
                "stage_id": 6,
                "stage_name": "Growth Telemetry, Rank Tracking & Conversion Attribution",
                "purpose": "Analyze organic search traffic trends, track SERP keyword position movements, evaluate AI Overview citation share-of-voice, and attribute conversions to content.",
                "recommended_repositories": [
                    fetch_repo_meta("matomo-org/matomo", "Google Analytics alternative that protects user privacy, provides full data ownership and search keyword insights"),
                    fetch_repo_meta("umami-software/umami", "Simple, fast, privacy-focused open-source alternative to Google Analytics with lightweight script"),
                    fetch_repo_meta("plausible/analytics", "Simple, open-source, lightweight (< 1 KB) and privacy-friendly web analytics alternative to Google Analytics")
                ],
                "input_handoff": {
                    "source_stage": "Stage 5: Real-Time Indexation, Sitemaps & Search Engine Ingestion",
                    "artifacts": ["Target Keyword Baseline Rankings", "Live Webhook Traffic Events", "Goal Funnel Definitions"],
                    "format": "Analytics Tracking Events"
                },
                "output_handoff": {
                    "next_stage": "Chief Growth Officer / Marketing Executive Feedback Loop",
                    "artifacts": ["Organic Revenue Attribution Reports", "Keyword Ranking Movement Dashboard", "Content Decay Alerts"],
                    "format": "Executive BI Reports / CSV"
                },
                "dependencies": ["Self-hosted or Cloud Analytics Instance", "PostgreSQL / ClickHouse storage", "Zero-Cookie Privacy Compliance (GDPR/CCPA)"],
                "alternatives": [
                    {"name": "PostHog/posthog", "tradeoff": "Full product analytics suite with session recording, heavier payload than Plausible/Umami"},
                    {"name": "pirsch-analytics/pirsch", "tradeoff": "Server-side privacy-first web analytics with low overhead"}
                ],
                "quality_gate": "Gate 6: Zero-Cookie GDPR Compliance, Sub-10ms Analytics Script Load Time, and Verified Organic Conversion Attribution"
            }
        ]
    }
]

print(f"Generating {len(workflows_data)} production workflow schemas...")

index_manifest = {
    "title": "Github Ultimate Repos - Workflow Intelligence Catalog",
    "version": "1.0.0",
    "total_workflows": len(workflows_data),
    "workflows": []
}

for wf in workflows_data:
    wfid = wf["workflow_id"]
    slug = wf["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "_").replace(",", "").replace("-", "_")
    base_filename = f"{wfid.lower()}_{slug}"
    json_path = os.path.join(WORKFLOWS_DIR, f"{base_filename}.json")
    yaml_path = os.path.join(WORKFLOWS_DIR, f"{base_filename}.yaml")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(wf, f, sort_keys=False, allow_unicode=True)

    print(f"  -> Generated: {base_filename}.json & .yaml ({wf['total_stages']} stages)")

    index_manifest["workflows"].append({
        "workflow_id": wf["workflow_id"],
        "name": wf["name"],
        "domain": wf["domain"],
        "total_stages": wf["total_stages"],
        "json_file": os.path.basename(json_path),
        "yaml_file": os.path.basename(yaml_path),
        "governance": wf["governance"]
    })

index_path = os.path.join(WORKFLOWS_DIR, "workflow_index.json")
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index_manifest, f, indent=2)

print(f"\nSuccessfully generated all schemas and index: {index_path}")
conn.close()
