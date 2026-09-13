#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OpenAlex searches for network-structure-as-outcome literature, batch-save to JSON."""
import json, time, urllib.request, urllib.parse, os, sys

MAILTO = "test@example.com"
BASE = "https://api.openalex.org/works"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oa_raw.json")
SEEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oa_seen.json")

ALL_QUERIES = [
    # A) outcome = network diversification / breadth
    "supply chain network diversification",
    "supply network diversification firm",
    "supplier diversification trade policy",
    "customer base diversification firm performance",
    "supplier concentration international trade",
    # B) outcome = geographic concentration / regionalization / HHI
    "supply chain geographic concentration",
    "geographic concentration supply chain firms",
    "supply chain regionalization nearshoring",
    "regional production network concentration",
    "customer geographic concentration supplier HHI",
    # C) outcome = centrality / network position
    "supply chain network centrality",
    "firm centrality supply network",
    "intermediary centrality trade network",
    "network position global value chain firm",
    # D) outcome = partner country count / number of countries
    "number of supplier countries firm",
    "international sourcing breadth firm",
    "import partner diversification liberalization",
    # E) treatment = FTA / regional integration
    "free trade agreement supply chain",
    "regional trade agreement production network",
    "RCEP supply chain",
    "trade liberalization global value chain firm",
]

def get(url, tries=4, wait=4.0):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"research/1.0 (mailto:{MAILTO})"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = wait * 1.8
                time.sleep(wait)
                continue
            return {"error": f"HTTP {e.code}"}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "too many retries"}

def search(query, per_page=20):
    u = f"{BASE}?search={urllib.parse.quote(query)}&per_page={per_page}&mailto={MAILTO}&sort=cited_by_count:desc"
    return get(u)

def main():
    # load existing
    if os.path.exists(SEEN):
        seen = json.load(open(SEEN, encoding="utf-8"))
    else:
        seen = {}
    for q in ALL_QUERIES:
        if seen.get("_done", []) and q in seen["_done"]:
            print("skip (done):", q, flush=True)
            continue
        print("QUERY:", q, flush=True)
        res = search(q)
        if "results" not in res:
            print("  ERR:", res.get("error"), flush=True)
            time.sleep(3)
            continue
        key = q
        seen.setdefault(key, {"count": res["meta"]["count"], "runs": []})
        seen[key]["runs"].append({
            "query": q, "count": res["meta"]["count"],
            "works": [{
                "id": w.get("id"), "doi": w.get("doi"), "title": w.get("title"),
                "year": w.get("publication_year"), "type": w.get("type"),
                "cited": w.get("cited_by_count"),
                "host": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "authors": [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")][:6],
                "abstract_inverted": w.get("abstract_inverted_index"),
            } for w in res["results"]]
        })
        seen.setdefault("_done", []).append(q)
        json.dump(seen, open(SEEN, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"  count={res['meta']['count']}, saved {len(res['results'])} works", flush=True)
        time.sleep(1.5)
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    main()
