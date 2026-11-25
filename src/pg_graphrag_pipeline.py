#!/usr/bin/env python3
"""
pg_graphrag_pipeline.py - Microsoft GraphRAG Architecture Docked into PostgreSQL 16 (Port 5435)
Extracts Entities, Relationships, and Hierarchical Communities from Enterprise Artifacts,
persists them into PostgreSQL 16, and provides Global/Local Graph Search for Nod WhatsApp Mesh.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import psycopg2
from psycopg2.extras import execute_values, Json

DB_CONFIG = {
    "dbname": "agent_memory",
    "user": "agent_admin",
    "password": "central_secret",
    "host": "127.0.0.1",
    "port": 5435
}

LLM_ENDPOINT = "http://127.0.0.1:8801/v1/chat/completions"
LLM_MODEL = "google/gemini-3.8-flash"

def get_db():
    return psycopg2.connect(**DB_CONFIG)

def call_llm(prompt: str, system_prompt: str = "You are an expert GraphRAG Knowledge Engineer.") -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    req = urllib.request.Request(
        LLM_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] LLM request failed: {e}", file=sys.stderr)
        return ""

def load_knowledge_corpus():
    """Aggregates enterprise knowledge from PostgreSQL records and markdown blueprints."""
    corpus = []
    
    # 1. Lead intake and candidate data from PostgreSQL
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, company, role, source, metadata FROM inbound_leads;")
        leads = cur.fetchall()
        for lead in leads:
            corpus.append({
                "source": f"inbound_lead_{lead[0]}",
                "text": f"Client Lead: {lead[1]} at {lead[2]}, Role: {lead[3]}, Source: {lead[4]}, Details: {lead[5]}"
            })
        
        cur.execute("SELECT vendor, subject, amount, status FROM nod_subscriptions;")
        subs = cur.fetchall()
        sub_text = "Active FinOps Subscriptions: " + "; ".join([f"{s[0]} ({s[1]}): {s[2]} [{s[3]}]" for s in subs])
        corpus.append({"source": "finops_subscriptions", "text": sub_text})
    conn.close()

    # 2. Key blueprint files
    blueprints = [
        "/home/ubuntu/agy-argon-home/.gemini/antigravity-cli/brain/128467fe-19b4-42d8-97d0-3a10ad10bff8/enterprise_fde_lead_intake_blueprint.md",
        "/home/ubuntu/agy-argon-home/.gemini/antigravity-cli/brain/128467fe-19b4-42d8-97d0-3a10ad10bff8/nod_ai_agent_centralised_infra_blueprint.md"
    ]
    for bp in blueprints:
        if os.path.exists(bp):
            with open(bp, "r", encoding="utf-8") as f:
                content = f.read()
                corpus.append({"source": os.path.basename(bp), "text": content[:4000]})
                
    return corpus

def index_graph():
    print("[*] Starting GraphRAG Entity & Relationship Extraction...")
    corpus = load_knowledge_corpus()
    
    all_entities = []
    all_relationships = []

    for item in corpus:
        source = item["source"]
        text = item["text"]
        print(f"[*] Processing document: {source}")
        
        prompt = f"""Given the following text from source '{source}', extract key entities and relationships for an enterprise knowledge graph.
Return ONLY valid JSON with this exact schema:
{{
  "entities": [
    {{"name": "Entity Name", "type": "ORGANIZATION|TECHNOLOGY|PERSON|PROJECT|METRIC|ROLE", "description": "1 sentence description"}}
  ],
  "relationships": [
    {{"source": "Entity A", "target": "Entity B", "relationship": "USES|DEPLOYED_ON|LEADS|BUILT_WITH|PAYS_FOR|INTEGRATED_WITH", "weight": 1.0, "description": "Relationship summary"}}
  ]
}}

TEXT:
{text}
"""
        raw_res = call_llm(prompt)
        # Parse JSON
        try:
            cleaned = raw_res.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            parsed = json.loads(cleaned.strip())
            
            for ent in parsed.get("entities", []):
                all_entities.append((ent["name"], ent.get("type", "CONCEPT"), ent.get("description", ""), source))
            for rel in parsed.get("relationships", []):
                all_relationships.append((rel["source"], rel["target"], rel.get("relationship", "RELATED_TO"), float(rel.get("weight", 1.0)), rel.get("description", "")))
        except Exception as e:
            print(f"[!] Warning parsing JSON for {source}: {e}")

    # Hierarchical Community Clustering & Summarization
    print(f"[*] Extracted {len(all_entities)} entities, {len(all_relationships)} relationships. Clustering communities...")
    
    community_prompt = f"""Synthesize the overall knowledge graph represented by these entities and relationships into 3 distinct Enterprise Graph Communities:
1. Enterprise FDE & Client Operations
2. Infrastructure, WhatsApp Mesh & Autonomous Tooling
3. FinOps, Subscription Governance & Resource Optimization

Return ONLY valid JSON matching this schema:
{{
  "communities": [
    {{
      "community_id": "COMM_1",
      "level": 0,
      "title": "Enterprise FDE & Client Operations",
      "summary": "Comprehensive executive summary of enterprise intake, clients, and technical blueprints...",
      "findings": ["Finding 1", "Finding 2"]
    }},
    {{
      "community_id": "COMM_2",
      "level": 0,
      "title": "Infrastructure & WhatsApp Mesh Autonomous Tooling",
      "summary": "Summary of Baileys WhatsApp transport, browser-use visual computer use, and centralized AI Gateway...",
      "findings": ["Finding 1", "Finding 2"]
    }},
    {{
      "community_id": "COMM_3",
      "level": 0,
      "title": "FinOps & Subscription Leak Governance",
      "summary": "Audit summary of SaaS subscriptions, cost leaks, and Nod approval tripwires...",
      "findings": ["Finding 1", "Finding 2"]
    }}
  ]
}}

SAMPLE ENTITIES:
{json.dumps([e[0] for e in all_entities[:25]])}
SAMPLE RELATIONSHIPS:
{json.dumps([f"{r[0]} -> {r[2]} -> {r[1]}" for r in all_relationships[:25]])}
"""
    raw_comm = call_llm(community_prompt)
    communities = []
    try:
        cleaned_c = raw_comm.strip()
        if cleaned_c.startswith("```json"):
            cleaned_c = cleaned_c[7:]
        if cleaned_c.startswith("```"):
            cleaned_c = cleaned_c[3:]
        if cleaned_c.endswith("```"):
            cleaned_c = cleaned_c[:-3]
        comm_parsed = json.loads(cleaned_c.strip())
        for c in comm_parsed.get("communities", []):
            communities.append((c["community_id"], c.get("level", 0), c["title"], c["summary"], json.dumps(c.get("findings", []))))
    except Exception as e:
        print(f"[!] Warning parsing community JSON: {e}")

    # Persist to PostgreSQL 16
    print("[*] Persisting GraphRAG nodes, edges, and communities to PostgreSQL 16...")
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE graphrag_entities, graphrag_relationships, graphrag_communities RESTART IDENTITY;")
        if all_entities:
            cur.executemany("INSERT INTO graphrag_entities (entity_name, entity_type, description, source_doc) VALUES (%s, %s, %s, %s);", all_entities)
        if all_relationships:
            cur.executemany("INSERT INTO graphrag_relationships (source_entity, target_entity, relationship, weight, description) VALUES (%s, %s, %s, %s, %s);", all_relationships)
        if communities:
            cur.executemany("INSERT INTO graphrag_communities (community_id, level, title, summary, findings) VALUES (%s, %s, %s, %s, %s);", communities)
    conn.commit()
    conn.close()
    print(f"[+] Indexing Complete! Stored {len(all_entities)} entities, {len(all_relationships)} relationships, {len(communities)} communities in PostgreSQL 16.")

def query_graph(query_str: str, mode: str = "global") -> str:
    conn = get_db()
    with conn.cursor() as cur:
        if mode == "global":
            cur.execute("SELECT title, summary, findings FROM graphrag_communities;")
            comms = cur.fetchall()
            context = "\n\n".join([f"### Community: {c[0]}\nSummary: {c[1]}\nKey Findings: {c[2]}" for c in comms])
        else: # local search
            cur.execute("SELECT entity_name, entity_type, description FROM graphrag_entities WHERE entity_name ILIKE %s LIMIT 10;", (f"%{query_str}%",))
            ents = cur.fetchall()
            cur.execute("SELECT source_entity, relationship, target_entity, description FROM graphrag_relationships WHERE source_entity ILIKE %s OR target_entity ILIKE %s LIMIT 15;", (f"%{query_str}%", f"%{query_str}%"))
            rels = cur.fetchall()
            context = f"Entities:\n" + "\n".join([f"- {e[0]} ({e[1]}): {e[2]}" for e in ents])
            context += f"\nRelationships:\n" + "\n".join([f"- {r[0]} --[{r[1]}]--> {r[2]}: {r[3]}" for r in rels])
    conn.close()

    answer_prompt = f"""You are an executive GraphRAG knowledge agent. Use the following structured knowledge graph context from PostgreSQL 16 to answer the user query concisely and authoritatively.

CONTEXT:
{context}

USER QUERY:
{query_str}
"""
    return call_llm(answer_prompt, system_prompt="You are an enterprise knowledge assistant answering questions using a graph-indexed corporate database.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--index":
        index_graph()
    elif len(sys.argv) > 1 and sys.argv[1] == "--query":
        q = sys.argv[2] if len(sys.argv) > 2 else "What are our active infrastructure components and subscriptions?"
        mode = sys.argv[3] if len(sys.argv) > 3 else "global"
        print(f"[*] Querying GraphRAG ({mode} mode): '{q}'\n")
        res = query_graph(q, mode=mode)
        print(res)
    else:
        print("Usage:\n  python3 pg_graphrag_pipeline.py --index\n  python3 pg_graphrag_pipeline.py --query '<query_text>' [global|local]")
