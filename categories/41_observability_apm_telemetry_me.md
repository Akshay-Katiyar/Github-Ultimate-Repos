# [41] OBSERVABILITY, APM TELEMETRY, METRICS, DISTRIBUTED TRACING & LOGGING

**Total Repositories**: 52 | **Combined Stars**: 777,470★  

[⬅️ Back to Master Directory](../README.md)

---

```text
1. prometheus/prometheus                                   | ⭐  66,746★ | 🍴 10,916 forks | 💻 Go          
         🔗 URL      : https://github.com/prometheus/prometheus
         📝 DESC     : The Prometheus monitoring system and time series database.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       2. PostHog/posthog                                         | ⭐  40,423★ | 🍴  3,552 forks | 💻 Python      
         🔗 URL      : https://github.com/PostHog/posthog
         📝 DESC     : :hedgehog: PostHog is the leading platform for building self-driving products. Our developer tools – AI observability, analytics, session replay, flags, experiments, error tracking, logs, and more – capture all the context agents need to diagnose problems, uncover opportunities, and ship fixes. Steer it all from Slack, web, desktop, or the MCP.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       3. grafana/k6                                              | ⭐  32,033★ | 🍴  1,697 forks | 💻 Go          
         🔗 URL      : https://github.com/grafana/k6
         📝 DESC     : A modern load testing tool, using Go and JavaScript
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       4. influxdata/influxdb                                     | ⭐  31,783★ | 🍴  3,738 forks | 💻 Rust        
         🔗 URL      : https://github.com/influxdata/influxdb
         📝 DESC     : Scalable datastore for metrics, events, and real-time analytics
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       5. GoogleChrome/lighthouse                                 | ⭐  30,942★ | 🍴  9,776 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/GoogleChrome/lighthouse
         📝 DESC     : Automated auditing, performance metrics, and best practices for the web.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       6. ossrs/srs                                               | ⭐  29,366★ | 🍴  5,704 forks | 💻 C++         
         🔗 URL      : https://github.com/ossrs/srs
         📝 DESC     : SRS is a simple, high-performance, AI-driven real-time media server supporting RTMP, WebRTC, HLS, HTTP-FLV, HTTP-TS, SRT, MPEG-DASH, and GB28181, with codec support for H.264, H.265, AV1, VP9, AAC, Opus, and G.711.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       7. grafana/loki                                            | ⭐  29,055★ | 🍴  4,156 forks | 💻 Go          
         🔗 URL      : https://github.com/grafana/loki
         📝 DESC     : Like Prometheus, but for logs.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       8. hagezi/dns-blocklists                                   | ⭐  27,758★ | 🍴    842 forks | 💻 Text        
         🔗 URL      : https://github.com/hagezi/dns-blocklists
         📝 DESC     : DNS-Blocklists: For a better internet - keep the internet clean!
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

       9. apache/skywalking                                       | ⭐  24,975★ | 🍴  6,634 forks | 💻 Java        
         🔗 URL      : https://github.com/apache/skywalking
         📝 DESC     : APM, Application Performance Monitoring System
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      10. PrefectHQ/prefect                                       | ⭐  24,073★ | 🍴  2,618 forks | 💻 Python      
         🔗 URL      : https://github.com/PrefectHQ/prefect
         📝 DESC     : Prefect is a workflow orchestration framework for building resilient data pipelines in Python.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      11. jaegertracing/jaeger                                    | ⭐  23,337★ | 🍴  3,196 forks | 💻 Go          
         🔗 URL      : https://github.com/jaegertracing/jaeger
         📝 DESC     : CNCF Jaeger, a Distributed Tracing Platform
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      12. gofr-dev/gofr                                           | ⭐  20,840★ | 🍴  1,785 forks | 💻 Go          
         🔗 URL      : https://github.com/gofr-dev/gofr
         📝 DESC     : An opinionated GoLang framework for accelerated microservice development. Built in support for databases and observability.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      13. dianping/cat                                            | ⭐  18,937★ | 🍴  5,384 forks | 💻 Java        
         🔗 URL      : https://github.com/dianping/cat
         📝 DESC     : CAT 作为服务端项目基础组件，提供了 Java, C/C++, Node.js, Python, Go 等多语言客户端，已经在美团点评的基础架构中间件框架（MVC框架，RPC框架，数据库框架，缓存框架等，消息队列，配置系统等）深度集成，为美团点评各业务线提供系统丰富的性能指标、健康状况、实时告警等。
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      14. statsd/statsd                                           | ⭐  18,077★ | 🍴  1,938 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/statsd/statsd
         📝 DESC     : Daemon for easy but powerful stats aggregation
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      15. openzipkin/zipkin                                       | ⭐  17,471★ | 🍴  3,094 forks | 💻 Java        
         🔗 URL      : https://github.com/openzipkin/zipkin
         📝 DESC     : Zipkin is a distributed tracing system
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      16. Effect-TS/effect                                        | ⭐  17,383★ | 🍴    875 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/Effect-TS/effect
         📝 DESC     : Build production-ready applications in TypeScript
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      17. thedaviddias/Front-End-Performance-Checklist            | ⭐  17,380★ | 🍴  1,254 forks | 💻 Other       
         🔗 URL      : https://github.com/thedaviddias/Front-End-Performance-Checklist
         📝 DESC     : 🎮 The only Front-End Performance Checklist that runs faster than the others
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      18. lowlighter/metrics                                      | ⭐  17,328★ | 🍴  2,296 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/lowlighter/metrics
         📝 DESC     : 📊 An infographics generator with 30+ plugins and 300+ options to display stats about your GitHub account and render them as SVG, Markdown, PDF or JSON!
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      19. open-metadata/OpenMetadata                              | ⭐  15,574★ | 🍴  2,481 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/open-metadata/OpenMetadata
         📝 DESC     : The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building trusted data context and business semantics for humans, AI assistants, and agents.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      20. elastic/logstash                                        | ⭐  14,967★ | 🍴  3,499 forks | 💻 Java        
         🔗 URL      : https://github.com/elastic/logstash
         📝 DESC     : Logstash - transport and process your logs, events, or other data
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      21. thanos-io/thanos                                        | ⭐  14,253★ | 🍴  2,395 forks | 💻 Go          
         🔗 URL      : https://github.com/thanos-io/thanos
         📝 DESC     : Highly available Prometheus setup with long term storage capabilities. A CNCF Incubating project.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      22. prometheus/node_exporter                                | ⭐  13,878★ | 🍴  2,732 forks | 💻 Go          
         🔗 URL      : https://github.com/prometheus/node_exporter
         📝 DESC     : Exporter for machine metrics
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      23. fluent/fluentd                                          | ⭐  13,611★ | 🍴  1,405 forks | 💻 Ruby        
         🔗 URL      : https://github.com/fluent/fluentd
         📝 DESC     : Fluentd: Unified Logging Layer (project under CNCF)
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      24. datahub-project/datahub                                 | ⭐  12,886★ | 🍴  3,733 forks | 💻 Python      
         🔗 URL      : https://github.com/datahub-project/datahub
         📝 DESC     : The Context Platform for your Data and AI Stack
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      25. Tracer-Cloud/opensre                                    | ⭐  12,466★ | 🍴  1,826 forks | 💻 Python      
         🔗 URL      : https://github.com/Tracer-Cloud/opensre
         📝 DESC     : Build your own AI SRE agents. The open source toolkit for the AI era.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      26. grafana/pyroscope                                       | ⭐  11,703★ | 🍴    828 forks | 💻 Go          
         🔗 URL      : https://github.com/grafana/pyroscope
         📝 DESC     : Continuous Profiling Platform. Debug performance issues down to a single line of code
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      27. getagentseal/codeburn                                   | ⭐  11,575★ | 🍴    892 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/getagentseal/codeburn
         📝 DESC     : Free, local tool to track AI coding token usage and cost across 37 tools and agents (Claude Code, Cursor, Codex, Gemini and more), by model, project, and task. npx codeburn
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      28. resilience4j/resilience4j                               | ⭐  10,795★ | 🍴  1,533 forks | 💻 Java        
         🔗 URL      : https://github.com/resilience4j/resilience4j
         📝 DESC     : Resilience4j is a fault tolerance library designed for Java8 and functional programming
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      29. upgundecha/howtheysre                                   | ⭐   9,833★ | 🍴    900 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/upgundecha/howtheysre
         📝 DESC     : A curated collection of publicly available resources on how technology and tech-savvy organizations around the world practice Site Reliability Engineering (SRE)
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      30. aws-amplify/amplify-js                                  | ⭐   9,553★ | 🍴  2,175 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/aws-amplify/amplify-js
         📝 DESC     : A declarative JavaScript library for application development using cloud services.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      31. highlight/highlight                                     | ⭐   9,384★ | 🍴    690 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/highlight/highlight
         📝 DESC     : highlight.io: The open source, full-stack monitoring platform. Error monitoring, session replay, logging, distributed tracing, and more.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      32. coroot/coroot                                           | ⭐   7,985★ | 🍴    411 forks | 💻 Go          
         🔗 URL      : https://github.com/coroot/coroot
         📝 DESC     : Coroot is an open-source observability and APM tool with AI-powered Root Cause Analysis. It combines metrics, logs, traces, continuous profiling, and SLO-based alerting with predefined dashboards and inspections.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      33. dropwizard/metrics                                      | ⭐   7,848★ | 🍴  1,792 forks | 💻 Java        
         🔗 URL      : https://github.com/dropwizard/metrics
         📝 DESC     : :chart_with_upwards_trend: Capturing JVM- and application-level metrics. So you know what's going on.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      34. OneUptime/oneuptime                                     | ⭐   7,757★ | 🍴    479 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/OneUptime/oneuptime
         📝 DESC     : Complete open-source monitoring and observability platform.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      35. open-telemetry/opentelemetry-collector                  | ⭐   7,693★ | 🍴  2,316 forks | 💻 Go          
         🔗 URL      : https://github.com/open-telemetry/opentelemetry-collector
         📝 DESC     : OpenTelemetry Collector
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      36. aceberg/WatchYourLAN                                    | ⭐   7,646★ | 🍴    284 forks | 💻 Go          
         🔗 URL      : https://github.com/aceberg/WatchYourLAN
         📝 DESC     : Lightweight network IP scanner written in Go. With notifications, history, export to Grafana
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      37. metricsgraphics/metrics-graphics                        | ⭐   7,392★ | 🍴    460 forks | 💻 TypeScript  
         🔗 URL      : https://github.com/metricsgraphics/metrics-graphics
         📝 DESC     : A library optimized for concise and principled data graphics and layouts.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      38. XuehaiPan/nvitop                                        | ⭐   7,225★ | 🍴    253 forks | 💻 Python      
         🔗 URL      : https://github.com/XuehaiPan/nvitop
         📝 DESC     : An interactive NVIDIA-GPU process viewer and beyond, the one-stop solution for GPU process management.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      39. open-falcon/falcon-plus                                 | ⭐   7,224★ | 🍴  1,506 forks | 💻 Go          
         🔗 URL      : https://github.com/open-falcon/falcon-plus
         📝 DESC     : An open-source and enterprise-level monitoring system.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      40. tigerless-labs/cost-xray                                | ⭐   6,321★ | 🍴    384 forks | 💻 Python      
         🔗 URL      : https://github.com/tigerless-labs/cost-xray
         📝 DESC     : See what Claude Code and Codex actually send to the API — and what each part costs.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      41. graphite-project/graphite-web                           | ⭐   6,132★ | 🍴  1,254 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/graphite-project/graphite-web
         📝 DESC     : A highly scalable real-time graphing system
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      42. prometheus/client_golang                                | ⭐   6,043★ | 🍴  1,341 forks | 💻 Go          
         🔗 URL      : https://github.com/prometheus/client_golang
         📝 DESC     : Prometheus instrumentation library for Go applications
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      43. btraceio/btrace                                         | ⭐   5,997★ | 🍴    953 forks | 💻 Java        
         🔗 URL      : https://github.com/btraceio/btrace
         📝 DESC     : Production-safe dynamic tracing and diagnostics for Java applications—attach to live JVMs with no restart or recompilation.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      44. xinliangnote/go-gin-api                                 | ⭐   5,973★ | 🍴  1,121 forks | 💻 Go          
         🔗 URL      : https://github.com/xinliangnote/go-gin-api
         📝 DESC     : 基于 Gin 进行模块化设计的 API 框架，封装了常用功能，使用简单，致力于进行快速的业务研发。比如，支持 cors 跨域、jwt 签名验证、zap 日志收集、panic 异常捕获、trace 链路追踪、prometheus 监控指标、swagger 文档生成、viper 配置文件解析、gorm 数据库组件、gormgen 代码生成工具、graphql 查询语言、errno 统一定义错误码、gRPC 的使用、cron 定时任务 等等。
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      45. prometheus/blackbox_exporter                            | ⭐   5,915★ | 🍴  1,241 forks | 💻 Go          
         🔗 URL      : https://github.com/prometheus/blackbox_exporter
         📝 DESC     : Blackbox prober exporter
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      46. ossf/scorecard                                          | ⭐   5,791★ | 🍴    753 forks | 💻 Go          
         🔗 URL      : https://github.com/ossf/scorecard
         📝 DESC     : OpenSSF Scorecard - Security health metrics for Open Source
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      47. grafana/tempo                                           | ⭐   5,545★ | 🍴    776 forks | 💻 Go          
         🔗 URL      : https://github.com/grafana/tempo
         📝 DESC     : Grafana Tempo is a high volume, minimal dependency distributed tracing backend.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      48. oshi/oshi                                               | ⭐   5,272★ | 🍴    912 forks | 💻 Java        
         🔗 URL      : https://github.com/oshi/oshi
         📝 DESC     : Native Operating System and Hardware Information
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      49. grafana/mimir                                           | ⭐   5,261★ | 🍴    856 forks | 💻 Go          
         🔗 URL      : https://github.com/grafana/mimir
         📝 DESC     : Grafana Mimir provides horizontally scalable, highly available, multi-tenant, long-term storage for Prometheus.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      50. sitespeedio/sitespeed.io                                | ⭐   5,045★ | 🍴    628 forks | 💻 JavaScript  
         🔗 URL      : https://github.com/sitespeedio/sitespeed.io
         📝 DESC     : sitespeed.io is an open-source tool for comprehensive web performance analysis, enabling you to test, monitor, and optimize your website’s speed using real browsers in various environments.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      51. open-telemetry/opentelemetry-collector-contrib          | ⭐   5,018★ | 🍴  4,053 forks | 💻 Go          
         🔗 URL      : https://github.com/open-telemetry/opentelemetry-collector-contrib
         📝 DESC     : Contrib repository for the OpenTelemetry Collector
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.

      52. OllieOR/FBPIC-Baseline-Simulation                       | ⭐       2★ | 🍴      0 forks | 💻 Python      
         🔗 URL      : https://github.com/OllieOR/FBPIC-Baseline-Simulation
         📝 DESC     : Baseline FBPIC laser wakefield acceleration simulation with openPMD diagnostics, field and particle analysis, weighted bunch metrics, and initial robustness checks.
         ⚙️ WORKFLOW : Push/pull metric ingestion -> Gorilla double-delta timestamp & XOR float compression -> in-memory Head chunking -> immutable TSDB block compaction & PromQL evaluation.
```
