import sqlite3
import json

conn = sqlite3.connect('C:/Users/Aryan/Github-Ultimate-Repos/registry/agents_registry.db')
c = conn.cursor()

def get_repo(name_or_suffix):
    c.execute("SELECT name, stars, category_name, url, workflow FROM repositories WHERE name = ? OR name LIKE ? ORDER BY stars DESC LIMIT 1",
              (name_or_suffix, f"%/{name_or_suffix}"))
    row = c.fetchone()
    if not row:
        c.execute("SELECT name, stars, category_name, url, workflow FROM repositories WHERE name LIKE ? ORDER BY stars DESC LIMIT 1",
                  (f"%{name_or_suffix}%",))
        row = c.fetchone()
    if row:
        return {
            "name": row[0],
            "stars": row[1],
            "category": row[2],
            "url": row[3],
            "workflow_pipeline": row[4]
        }
    return None

test_repos = [
    "stanfordnlp/dspy", "promptfoo/promptfoo", "567-labs/instructor",
    "vllm-project/vllm", "ollama/ollama", "ggml-org/llama.cpp", "BerriAI/litellm",
    "docling-project/docling", "datalab-to/marker", "google/langextract",
    "qdrant/qdrant", "milvus-io/milvus", "facebookresearch/faiss",
    "FoundationAgents/MetaGPT", "microsoft/autogen", "crewAIInc/crewAI", "langchain-ai/langgraph",
    "langfuse/langfuse", "vibrantlabsai/ragas", "Portkey-AI/gateway",
    "bentoml/BentoML", "open-webui/open-webui",
    
    "flutter/flutter", "react/react-native", "expo/expo",
    "pmndrs/zustand", "reduxjs/redux",
    "tursodatabase/turso", "typeorm/typeorm",
    "mobile-dev-inc/Maestro", "appium/appium",
    "fastlane/fastlane",
    
    "hashicorp/terraform", "opentofu/manifesto", "gruntwork-io/terragrunt",
    "helm/helm", "helm/charts",
    "argoproj/argo-cd",
    "cilium/cilium", "istio/istio", "linkerd/linkerd2",
    "hashicorp/vault", "aquasecurity/trivy",
    "prometheus/prometheus", "grafana/grafana",
    
    "vercel/next.js", "tailwindlabs/tailwindcss",
    "fastapi/fastapi", "nestjs/nest", "honojs/hono",
    "supabase/supabase", "prisma/orm", "drizzle-team/drizzle-orm",
    "better-auth/better-auth", "appwrite/appwrite",
    "taskforcesh/bullmq", "celery/celery", "temporalio/temporal",
    "PostHog/posthog",
    
    "owasp-amass/amass", "projectdiscovery/subfinder",
    "projectdiscovery/nuclei", "projectdiscovery/nuclei-templates",
    "rapid7/metasploit-framework", "sqlmapproject/sqlmap", "fortra/impacket", "BishopFox/sliver",
    "NationalSecurityAgency/ghidra", "radareorg/radare2", "rizinorg/cutter",
    "peass-ng/PEASS-ng", "SpecterOps/BloodHound-Legacy", "Pennyw0rth/NetExec",
    
    "firecrawl/firecrawl", "scrapy/scrapy", "apify/crawlee",
    "coreyhaines31/marketingskills", "AgriciDaniel/claude-seo", "every-app/open-seo",
    "matomo-org/matomo", "umami-software/umami", "plausible/analytics"
]

verified = {}
for r in test_repos:
    res = get_repo(r)
    if res:
        verified[r] = res
    else:
        print(f"FAILED TO FIND: {r}")

with open('C:/Users/Aryan/Github-Ultimate-Repos/scripts/verified_repos.json', 'w', encoding='utf-8') as f:
    json.dump(verified, f, indent=2)

print(f"Dumped {len(verified)} verified repos to verified_repos.json")
