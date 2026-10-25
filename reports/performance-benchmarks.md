# Enterprise Scale & Query Performance Benchmark Report

- **Total Cataloged Records**: 11,730
- **SQLite FTS5 Storage Footprint**: 13.25 MB
- **CSV Storage Footprint**: 4.86 MB
- **Streaming Ingestion Throughput**: 251,260 records/sec
- **Benchmark Iterations**: 20 executions per query type

## FTS5 Search Latency Evaluation

| Query Pattern | Query String | Avg Latency (ms) | Min Latency (ms) | P95 Latency (ms) |
| :--- | :--- | :---: | :---: | :---: |
| Single Term (Unconstrained) | `langchain` | 0.04 ms | 0.02 ms | 0.38 ms |
| Multi-Term Conjunctive (AND) | `autonomous agent` | 0.06 ms | 0.05 ms | 0.25 ms |
| Disjunctive Expression (OR) | `transformers OR vllm OR ollama` | 0.03 ms | 0.02 ms | 0.20 ms |
| Prefix Wildcard | `robot*` | 0.04 ms | 0.03 ms | 0.18 ms |
| Category Filtered + Star Ordered | `category_name = "Robotics..." & stars >= 5000` | 0.71 ms | 0.61 ms | 2.22 ms |
| Deep Workflow Pipeline Query | `ROS2 OR MuJoCo OR Pinocchio` | 0.02 ms | 0.02 ms | 0.07 ms |

## Executive Summary & SLA Assessment

- **Sub-5ms SLA Target**: **PASSED (100%)**. All evaluated full-text, prefix, and boolean queries return within 1-3 milliseconds.
- **Memory Overhead**: Negligible (<25 MB resident set size during peak FTS evaluation).
- **Concurrency Scale**: SQLite WAL mode enabled, supporting simultaneous multi-agent reading without table locks.
