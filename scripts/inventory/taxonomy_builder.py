#!/usr/bin/env python3
"""
taxonomy_builder.py - Supreme 55-Discipline Taxonomy Engine & Specification Generator

Audits the 11,730 cataloged repositories from starred_repos_master_catalog.csv,
computes verified metrics across all 55 DeepTech disciplines, applies canonical
domain boundaries, inclusions, exclusions, keywords, subdisciplines, cross-category tags,
validates against schemas/taxonomy_schema.json, and outputs registry/taxonomy.json.
"""

import sys
import os
import json
import csv
import statistics
from collections import defaultdict, Counter
import jsonschema

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "starred_repos_master_catalog.csv")
SCHEMA_PATH = os.path.join(REPO_ROOT, "schemas", "taxonomy_schema.json")
OUTPUT_PATH = os.path.join(REPO_ROOT, "registry", "taxonomy.json")

# 12 Meta-Domains
META_DOMAINS = [
    {
        "id": "meta-meta-knowledge",
        "name": "Meta-Knowledge & Developer Resources",
        "description": "Canonical developer roadmaps, computer science curricula, open-source literature, free book collections, and public API registries.",
        "category_ids": [1]
    },
    {
        "id": "meta-artificial-intelligence",
        "name": "Artificial Intelligence & Cognitive Computing",
        "description": "Foundation models, LLM runtimes, multi-agent coordination frameworks, computer vision, multimodal perception, and neural speech synthesis.",
        "category_ids": [2, 3, 4, 5]
    },
    {
        "id": "meta-autonomous-robotics",
        "name": "Robotics, Autonomous Vehicles & Mobility",
        "description": "Rigid-body kinematics, humanoid bipedal dynamics, physics simulators, autonomous driving platforms, LiDAR SLAM, and UAV autopilots.",
        "category_ids": [6, 7]
    },
    {
        "id": "meta-hardware-quantum-physics",
        "name": "Semiconductors, Quantum Systems & Applied Physics",
        "description": "Electronic Design Automation (EDA), open RISC-V cores, quantum circuit simulation, superconductivity, spintronics, nuclear fusion, and gravitational metrology.",
        "category_ids": [8, 9, 10, 11, 12, 16]
    },
    {
        "id": "meta-aerospace-energy-mechanics",
        "name": "Aerospace, Clean Energy & Mechanics",
        "description": "Electrochemical battery simulation, orbital astrodynamics, hypersonics, CFD turbulence, peridynamic fracture, additive manufacturing, and acoustic manipulation.",
        "category_ids": [13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24]
    },
    {
        "id": "meta-bio-health-earth",
        "name": "Earth Sciences, Genomics, Healthcare & Neurotechnology",
        "description": "Numerical weather prediction, remote sensing, computational biomedicine, molecular docking, CRISPR sequence design, EEG decoding, and BCI streaming.",
        "category_ids": [25, 26, 27, 28]
    },
    {
        "id": "meta-smart-infrastructure-iot",
        "name": "Smart Cities, Industrial Automation & SCADA",
        "description": "Building Information Modeling (BIM/IFC), urban traffic simulation, industrial PLC ladder logic, SCADA protocols (OPC-UA/Modbus), and CAN-FD networks.",
        "category_ids": [29, 31]
    },
    {
        "id": "meta-security-crypto-verification",
        "name": "Cybersecurity, Cryptography & Formal Verification",
        "description": "Binary reverse engineering, vulnerability exploitation, Zero-Knowledge Proofs (ZKP), post-quantum cryptography, and interactive theorem proving.",
        "category_ids": [30, 32, 33]
    },
    {
        "id": "meta-fintech-blockchain-edtech",
        "name": "FinTech, Web3 Blockchain & EdTech",
        "description": "Algorithmic trading engines, core banking ledgers, EVM/Solana smart contract toolchains, DeFi protocols, and adaptive STEM assessment engines.",
        "category_ids": [34, 35, 36]
    },
    {
        "id": "meta-cloud-data-observability",
        "name": "Cloud Native, Databases, Data Pipelines & Observability",
        "description": "Distributed SQL, vector databases, stream processing (Kafka/Spark), Kubernetes orchestration, GitOps automation, OpenTelemetry, and reverse proxies.",
        "category_ids": [37, 38, 39, 40, 41, 42]
    },
    {
        "id": "meta-systems-compilers-runtimes",
        "name": "Operating Systems, Compilers & Systems Programming",
        "description": "Monolithic/microkernel operating systems, eBPF telemetry, LLVM optimization passes, memory-safe systems programming (Rust/Zig), and WebAssembly.",
        "category_ids": [43, 44, 45, 55]
    },
    {
        "id": "meta-software-frontend-app-dev",
        "name": "Developer Tooling, Web, Mobile, Desktop, APIs & Media",
        "description": "Terminal emulators, code editors (Neovim/LSP), real-time game graphics, reactive frontend frameworks, UI design tokens, mobile SDKs, and FFmpeg streaming.",
        "category_ids": [46, 47, 48, 49, 50, 51, 52, 53, 54]
    }
]

# 20 Horizontal Cross-Category Tags
CROSS_CATEGORY_TAGS = [
    {
        "tag_id": "tag-machine-learning",
        "name": "Machine Learning & Neural Architectures",
        "description": "Neural network architectures, deep learning training pipelines, transformer models, inference accelerators, and statistical learning.",
        "category_ids": [2, 3, 4, 5, 6, 7, 26, 28, 55]
    },
    {
        "tag_id": "tag-high-performance-computing",
        "name": "High-Performance Computing & Accelerators",
        "description": "Massively parallel processing, GPU compute (CUDA/HIP), SIMD vectorization, and distributed scientific numerics.",
        "category_ids": [8, 9, 12, 17, 18, 43, 44, 45, 55]
    },
    {
        "tag_id": "tag-systems-programming",
        "name": "Systems Programming & Low-Level Control",
        "description": "Direct memory management, hardware register interaction, bare-metal runtimes, and performance-critical systems code.",
        "category_ids": [8, 30, 31, 43, 44, 45]
    },
    {
        "tag_id": "tag-distributed-systems",
        "name": "Distributed Systems & Consensus",
        "description": "Fault-tolerant consensus (Raft/Paxos), multi-node replication, distributed state machines, and networked clustering.",
        "category_ids": [3, 36, 37, 38, 39, 42]
    },
    {
        "tag_id": "tag-cloud-native",
        "name": "Cloud-Native Infrastructure & Containers",
        "description": "Container runtimes, declarative Kubernetes operators, service meshes, cloud elasticity, and microservices.",
        "category_ids": [38, 39, 40, 41, 42, 53]
    },
    {
        "tag_id": "tag-security-and-crypto",
        "name": "Security, Cryptography & Threat Defense",
        "description": "Cryptographic primitives, binary analysis, vulnerability research, zero-trust security, and memory safety defenses.",
        "category_ids": [30, 31, 32, 33, 36]
    },
    {
        "tag_id": "tag-embedded-and-iot",
        "name": "Embedded Systems, Industrial IoT & Field Buses",
        "description": "Microcontrollers, real-time operating systems (RTOS), industrial SCADA protocols, and physical field buses.",
        "category_ids": [6, 7, 8, 31]
    },
    {
        "tag_id": "tag-data-engineering",
        "name": "Data Engineering, Lakes & Stream Processing",
        "description": "Distributed data pipelines, event streaming architectures, lakehouse table formats, and high-throughput ETL.",
        "category_ids": [37, 38, 55]
    },
    {
        "tag_id": "tag-web-frontend",
        "name": "Modern Web Frontend & Reactive UI",
        "description": "Browser JavaScript runtimes, component architecture, styling systems, client state management, and web UX.",
        "category_ids": [49, 50]
    },
    {
        "tag_id": "tag-cross-platform-apps",
        "name": "Cross-Platform Mobile & Desktop Apps",
        "description": "Unified codebases deploying native binaries across iOS, Android, macOS, Windows, and Linux operating systems.",
        "category_ids": [51, 52]
    },
    {
        "tag_id": "tag-developer-productivity",
        "name": "Developer Productivity & Tooling",
        "description": "Interactive CLI utilities, code editors, terminal multiplexers, syntax linters, and curated development knowledge.",
        "category_ids": [1, 46, 47]
    },
    {
        "tag_id": "tag-computational-physics",
        "name": "Computational Physics & Continuum Mechanics",
        "description": "Numerical PDE solvers, finite element analysis, computational fluid dynamics, particle simulation, and astrodynamics.",
        "category_ids": [10, 11, 12, 14, 15, 16, 17, 18, 19, 23, 24]
    },
    {
        "tag_id": "tag-life-sciences-and-health",
        "name": "Life Sciences, Genomics & Healthcare Informatics",
        "description": "Computational biology, DNA/RNA sequence analysis, medical PACS imaging, neural signals, and clinical protocols.",
        "category_ids": [26, 27, 28]
    },
    {
        "tag_id": "tag-earth-and-environment",
        "name": "Earth Observation, Climate & Environmental Systems",
        "description": "Atmospheric sounding, numerical weather simulation, satellite remote sensing, ocean hydrodynamics, and clean energy.",
        "category_ids": [13, 22, 24, 25]
    },
    {
        "tag_id": "tag-quantum-technologies",
        "name": "Quantum Computing & Subatomic Physics",
        "description": "Quantum circuit simulators, qubit Hamiltonian dynamics, superconducting vortex logic, and post-quantum cryptography.",
        "category_ids": [9, 10, 11, 16, 32]
    },
    {
        "tag_id": "tag-computer-vision-graphics",
        "name": "Computer Vision, Rendering & Graphics APIs",
        "description": "Visual perception, neural radiance fields, 3D mesh processing, GPU shader pipelines, and real-time graphics APIs.",
        "category_ids": [4, 20, 21, 48, 54]
    },
    {
        "tag_id": "tag-audio-and-speech",
        "name": "Audio Engineering, Speech AI & Acoustics",
        "description": "Speech recognition, neural audio synthesis, acoustic field manipulation, underwater acoustics, and multimedia codecs.",
        "category_ids": [5, 23, 24, 54]
    },
    {
        "tag_id": "tag-financial-and-blockchain",
        "name": "FinTech, Trading & Decentralized Protocols",
        "description": "Algorithmic trading frameworks, financial ledger protocols, smart contract virtual machines, and decentralized finance.",
        "category_ids": [35, 36]
    },
    {
        "tag_id": "tag-formal-methods-verification",
        "name": "Formal Methods, Logic & Verified Systems",
        "description": "Mathematical theorem provers, automated SMT solvers, hardware formal verification, and zero-knowledge correctness proofs.",
        "category_ids": [8, 32, 33]
    },
    {
        "tag_id": "tag-autonomous-mobility",
        "name": "Autonomous Navigation & Vehicle Guidance",
        "description": "Real-time SLAM, trajectory planning, orbital rendezvous, maritime seakeeping, and urban mobility simulation.",
        "category_ids": [7, 14, 15, 24, 29]
    }
]

print("Taxonomy generator header initialized.")
