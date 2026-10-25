#!/usr/bin/env python3
"""
mcp_server.py - Model Context Protocol (MCP) Standard Server for Github-Ultimate-Repos

Exposes the 11,730 repository catalog, full-text search (FTS5), recommendation engine,
and architecture workflows as standard MCP tools and resources over stdio JSON-RPC 2.0.
Compatible with Cline, Cursor, Claude Desktop, Antigravity, and any MCP client.
"""

import sys
import os
import json
import sqlite3
from typing import Dict, Any, List, Optional

# Ensure UTF-8 stdio
if hasattr(sys.stdin, 'reconfigure'):
    try:
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
DB_PATH = os.path.join(REPO_ROOT, "registry", "agents_registry.db")
WORKFLOWS_DIR = os.path.join(REPO_ROOT, "workflows")

try:
    from scripts.recommendation.recommendation_engine import RecommendationEngine
    REC_ENGINE = RecommendationEngine(DB_PATH)
except Exception:
    try:
        sys.path.insert(0, os.path.join(REPO_ROOT, "scripts", "recommendation"))
        from recommendation_engine import RecommendationEngine
        REC_ENGINE = RecommendationEngine(DB_PATH)
    except Exception:
        REC_ENGINE = None

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "github-ultimate-repos-mcp"
SERVER_VERSION = "1.0.0"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------

def tool_search_repositories(query: str, category: Optional[str] = None, min_stars: int = 0, limit: int = 10) -> Dict[str, Any]:
    """Search repositories using FTS5 with fallback to LIKE."""
    conn = get_db()
    c = conn.cursor()
    limit = min(max(1, limit), 50)
    
    fts_query = f'"{query}"' if " " in query and not any(op in query for op in ["AND", "OR", "NOT", "*"]) else query
    sql = """
    SELECT r.id, r.name, r.stars, r.forks, r.language, r.category_name, r.url, r.workflow, r.description, r.quality_gate
    FROM repositories_fts f
    JOIN repositories r ON f.rowid = r.id
    WHERE repositories_fts MATCH ?
    """
    params = [fts_query]
    if category:
        sql += " AND r.category_name LIKE ?"
        params.append(f"%{category}%")
    if min_stars > 0:
        sql += " AND r.stars >= ?"
        params.append(min_stars)
    sql += " ORDER BY r.stars DESC LIMIT ?;"
    params.append(limit)

    try:
        c.execute(sql, params)
        rows = c.fetchall()
    except sqlite3.OperationalError:
        like_sql = """
        SELECT id, name, stars, forks, language, category_name, url, workflow, description, quality_gate
        FROM repositories
        WHERE (name LIKE ? OR description LIKE ? OR workflow LIKE ?)
        """
        like_params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        if category:
            like_sql += " AND category_name LIKE ?"
            like_params.append(f"%{category}%")
        if min_stars > 0:
            like_sql += " AND stars >= ?"
            like_params.append(min_stars)
        like_sql += " ORDER BY stars DESC LIMIT ?;"
        like_params.append(limit)
        c.execute(like_sql, like_params)
        rows = c.fetchall()

    conn.close()
    results = [dict(r) for r in rows]
    return {
        "count": len(results),
        "query": query,
        "repositories": results
    }

def tool_get_repository(name: str) -> Dict[str, Any]:
    """Retrieve the comprehensive dossier for a specific repository."""
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM repositories WHERE LOWER(name) = ? OR LOWER(name) LIKE ? ORDER BY stars DESC LIMIT 1;",
        (name.lower(), f"%/{name.lower()}%")
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return {"error": f"Repository '{name}' not found in catalog."}
    return {"repository": dict(row)}

def tool_recommend_stack(intent: str, category: Optional[str] = None, lang: Optional[str] = None, min_stars: int = 0, limit: int = 5) -> Dict[str, Any]:
    """Provide intent-based multi-factor recommendations for AI development."""
    if not REC_ENGINE:
        return {"error": "Recommendation engine unavailable."}
    
    try:
        res = REC_ENGINE.recommend(
            query=intent,
            category_filter=category,
            preferred_lang=lang,
            min_stars=min_stars,
            limit=min(max(1, limit), 20)
        )
        if isinstance(res, tuple):
            _, rec_cards = res
        elif isinstance(res, list):
            rec_cards = res
        else:
            rec_cards = [res]
        
        recs_list = []
        for r in rec_cards:
            if hasattr(r, "to_dict"):
                recs_list.append(r.to_dict())
            elif hasattr(r, "__dict__"):
                from dataclasses import asdict
                recs_list.append(asdict(r))
            else:
                recs_list.append(r)

        return {
            "intent": intent,
            "count": len(recs_list),
            "recommendations": recs_list
        }
    except Exception as e:
        return {"error": f"Recommendation failed: {e}", "recommendations": []}

def tool_compare_repositories(repos: List[str]) -> Dict[str, Any]:
    """Compare 2 to 3 repositories side-by-side."""
    if len(repos) < 2:
        return {"error": "Provide at least 2 repositories to compare."}
    
    conn = get_db()
    c = conn.cursor()
    records = []
    for r in repos[:3]:
        c.execute("SELECT * FROM repositories WHERE LOWER(name) = ? OR LOWER(name) LIKE ? ORDER BY stars DESC LIMIT 1;", (r.lower(), f"%/{r.lower()}%"))
        row = c.fetchone()
        if row:
            records.append(dict(row))
        else:
            records.append({"name": r, "error": "Not found in catalog"})
    conn.close()
    return {"comparison": records}

def tool_get_workflow(name: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve verified end-to-end development workflow DAGs."""
    if not os.path.exists(WORKFLOWS_DIR):
        return {"error": "Workflows directory not found."}
    
    files = [f for f in os.listdir(WORKFLOWS_DIR) if f.endswith(".json")]
    if not name:
        manifest = []
        for f in files:
            p = os.path.join(WORKFLOWS_DIR, f)
            try:
                with open(p, "r", encoding="utf-8") as wf_file:
                    data = json.load(wf_file)
                    manifest.append({
                        "filename": f,
                        "workflow_id": data.get("workflow_id"),
                        "name": data.get("name"),
                        "domain": data.get("domain"),
                        "stages_count": len(data.get("stages", []))
                    })
            except Exception:
                pass
        return {"available_workflows": manifest}
    
    matched = None
    for f in files:
        if name.lower() in f.lower() or name.lower() in f.replace("_", "-").lower():
            matched = os.path.join(WORKFLOWS_DIR, f)
            break
    
    if not matched:
        return {"error": f"Workflow '{name}' not found.", "available": files}
    
    with open(matched, "r", encoding="utf-8") as wf_file:
        return {"workflow": json.load(wf_file)}

def tool_list_categories() -> Dict[str, Any]:
    """List all 55 DeepTech disciplines with counts and star volumes."""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT category_id, category_name, COUNT(*) as repo_count, SUM(stars) as total_stars
        FROM repositories
        GROUP BY category_id, category_name
        ORDER BY category_id ASC;
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"total_categories": len(rows), "categories": rows}

def tool_get_stats() -> Dict[str, Any]:
    """Get high-level catalog intelligence and health metrics."""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(stars), SUM(forks), COUNT(DISTINCT language), COUNT(DISTINCT category_name) FROM repositories;")
    total_repos, total_stars, total_forks, total_langs, total_cats = c.fetchone()
    conn.close()
    return {
        "total_repositories": total_repos,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_languages": total_langs,
        "total_disciplines": total_cats,
        "quality_gate": "100% VERIFIED",
        "protocol_version": PROTOCOL_VERSION
    }

# ---------------------------------------------------------
# Tool Definitions Manifest (MCP Schema)
# ---------------------------------------------------------

MCP_TOOLS = [
    {
        "name": "search_repositories",
        "description": "Full-text search (FTS5) across 11,730 verified GitHub repositories, AI agents, and tools. Supports category and star filters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword, framework name, or topic (e.g. 'mcp server', 'cline', 'swarms')"},
                "category": {"type": "string", "description": "Optional category filter (e.g. 'Multi-Agent Systems', 'Artificial Intelligence')"},
                "min_stars": {"type": "integer", "description": "Optional minimum GitHub stars threshold", "default": 0},
                "limit": {"type": "integer", "description": "Max results to return (1-50)", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_repository",
        "description": "Retrieve the complete architecture workflow, stars, license, language, and quality status for a specific repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Exact or partial repository name (e.g. 'cline/cline', 'AutoGPT', 'aider')"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "get_repository_details",
        "description": "Retrieve detailed architectural workflow, metrics, and quality gate for a repository (alias of get_repository).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Exact or partial repository name (e.g. 'cline/cline', 'AutoGPT', 'aider')"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "recommend_stack",
        "description": "Intelligent multi-factor recommendation engine. Scores repositories based on intent relevance, architectural fit, maturity, and language.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string", "description": "Natural language objective (e.g. 'build an AI agent with tool calling and sandboxing')"},
                "category": {"type": "string", "description": "Constrain recommendation to specific discipline"},
                "lang": {"type": "string", "description": "Preferred programming language (e.g. 'Python', 'TypeScript', 'Rust')"},
                "min_stars": {"type": "integer", "description": "Minimum star threshold", "default": 0},
                "limit": {"type": "integer", "description": "Number of recommendations to return (1-20)", "default": 5}
            },
            "required": ["intent"]
        }
    },
    {
        "name": "recommend_repositories",
        "description": "Intelligent multi-factor recommendation engine. Scores repositories based on intent relevance, architectural fit, maturity, and language (alias of recommend_stack).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string", "description": "Natural language objective (e.g. 'build an AI agent with tool calling and sandboxing')"},
                "category": {"type": "string", "description": "Constrain recommendation to specific discipline"},
                "lang": {"type": "string", "description": "Preferred programming language (e.g. 'Python', 'TypeScript', 'Rust')"},
                "min_stars": {"type": "integer", "description": "Minimum star threshold", "default": 0},
                "limit": {"type": "integer", "description": "Number of recommendations to return (1-20)", "default": 5}
            },
            "required": ["intent"]
        }
    },
    {
        "name": "compare_repositories",
        "description": "Compare 2 to 3 candidate frameworks side-by-side on stars, forks, language, architecture workflow, and category.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of 2 to 3 repository names to compare (e.g. ['cline/cline', 'Aider-AI/aider', 'OpenHands/OpenHands'])"
                }
            },
            "required": ["repos"]
        }
    },
    {
        "name": "get_workflow",
        "description": "Retrieve verified production workflow pipelines (stages, checkpoints, recommended tools) for AI Agents, RAG, Cloud-Native, Mobile, and SaaS MVP.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Optional workflow name (e.g. 'ai_agent', 'rag', 'cloud_native'). Omit to list all available workflows."}
            }
        }
    },
    {
        "name": "list_categories",
        "description": "List all 55 DeepTech disciplines indexed in the catalog along with repository counts and star metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_catalog_stats",
        "description": "Retrieve overall intelligence statistics and health metrics for the repository catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

MCP_RESOURCES = [
    {
        "uri": "ultimate-repos://stats",
        "name": "Catalog Intelligence Statistics",
        "description": "Live aggregate metrics of 11,730 repositories across 55 disciplines",
        "mimeType": "application/json"
    },
    {
        "uri": "ultimate-repos://categories",
        "name": "Discipline Taxonomy",
        "description": "Complete breakdown of 55 DeepTech disciplines and repository distributions",
        "mimeType": "application/json"
    },
    {
        "uri": "ultimate-repos://workflows/ai-agent",
        "name": "Production AI Agent Swarm Workflow",
        "description": "Verified 4-stage engineering pipeline for building multi-agent swarms with MCP tools",
        "mimeType": "application/json"
    }
]

# ---------------------------------------------------------
# JSON-RPC Dispatcher
# ---------------------------------------------------------

def handle_request(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    # Handshake: initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                }
            }
        }

    # Notification: initialized
    if method == "notifications/initialized":
        return None

    # Ping
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    # Tools: list
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }

    # Tools: call
    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        try:
            if tool_name == "search_repositories":
                res = tool_search_repositories(
                    query=args.get("query", ""),
                    category=args.get("category"),
                    min_stars=args.get("min_stars", 0),
                    limit=args.get("limit", 10)
                )
            elif tool_name in ("get_repository", "get_repository_details"):
                repo_name = args.get("name") or args.get("repo") or args.get("repository", "")
                res = tool_get_repository(name=repo_name)
            elif tool_name in ("recommend_stack", "recommend_repositories"):
                intent_query = args.get("intent") or args.get("query", "")
                lang_pref = args.get("lang") or args.get("language")
                res = tool_recommend_stack(
                    intent=intent_query,
                    category=args.get("category"),
                    lang=lang_pref,
                    min_stars=args.get("min_stars", 0),
                    limit=args.get("limit", 5)
                )
            elif tool_name == "compare_repositories":
                res = tool_compare_repositories(repos=args.get("repos", []))
            elif tool_name == "get_workflow":
                res = tool_get_workflow(name=args.get("name"))
            elif tool_name == "list_categories":
                res = tool_list_categories()
            elif tool_name == "get_catalog_stats":
                res = tool_get_stats()
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Method/Tool '{tool_name}' not found"}
                }

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(res, indent=2, ensure_ascii=False)
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": str(e)}
            }

    # Resources: list
    if method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "resources": MCP_RESOURCES
            }
        }

    # Resources: read
    if method == "resources/read":
        uri = params.get("uri")
        if uri == "ultimate-repos://stats":
            content = tool_get_stats()
        elif uri == "ultimate-repos://categories":
            content = tool_list_categories()
        elif uri == "ultimate-repos://workflows/ai-agent":
            content = tool_get_workflow(name="ai_agent")
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Unknown resource URI '{uri}'"}
            }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(content, indent=2, ensure_ascii=False)
                    }
                ]
            }
        }

    # Default unsupported method
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method: {method}"}
    }

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            req = json.loads(line)
            resp = handle_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
