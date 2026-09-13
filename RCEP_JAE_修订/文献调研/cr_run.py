#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crossref-based literature search for supply chain network structure as outcome variable.
Saves results incrementally to cr_raw.json. Retries on 429 with backoff."""
import json, time, requests, os, urllib.parse

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cr_raw.json")
UA = {"User-Agent": "research/1.0 (mailto:research.agent@nousresearch.com)"}

# (query, rows) — targeted to outcome=network structure, treatment=trade policy/FTA
QUERIES = [
    # Outcome = network diversification/breadth
    ("supply chain network diversification", 15),
    ("supply network diversification trade liberalization firm", 15),
    ("customer supplier network diversification", 15),
    ("import partner diversification liberalization", 15),
    ("supplier base diversification resilience", 12),
    # Outcome = geographic concentration / near-shoring / regionalization / HHI
    ("geographic concentration supply chain customers suppliers", 15),
    ("supply chain regionalization nearshoring trade", 12),
    ("onshore outsourcing regional production network", 12),
    ("customer geographical concentration supplier", 12),
    ("production network regionalization free trade agreement", 12),
    # Outcome = centrality / network position
    ("supply chain network centrality firm", 12),
    ("network centrality global value chain firms", 12),
    ("production network centrality shock propagation", 12),
    ("firm centrality buyer supplier network exports", 12),
    # Outcome = number of partner countries / sourcing breadth
    ("number of supplier countries firm imports", 12),
    ("international sourcing breadth country count", 12),
    ("import supplier countries diversification tariff", 12),
    # Treatment = FTA / regional integration on network
    ("free trade agreement supply chain network", 15),
    ("regional trade agreement production networks firms", 15),
    ("RCEP supply chains firms", 12),
    ("trade agreement trade network exports", 12),
    ("tariff reduction production network firm", 12),
    # Firm-to-firm data / FactSet Revere / Compustat customer-supplier
    ("compustat customer supplier data production network", 12),
    ("factset revere customer supplier connections", 10),
    ("firm to firm trade network exporter", 12),
    ("customer-supplier network China listed firms", 12),
    ("customers suppliers top five public firms China", 12),
    # Resilience / robustness of network structure
    ("production network resilience trade war", 12),
    ("supply chain robustness tariff shock", 12),
    ("network structure trade costs reallocation", 12),
]

def query_cr(txt, rows):
    p = {"query.bibliographic": txt, "rows": rows, "select": "title,author,published,container-title,DOI,is-referenced-by-count,abstract,type"}
    # increase select via many fields
    p = {"query.bibliographic": txt, "rows": rows}
    for attempt in range(4):
        try:
            r = requests.get("https://api.crossref.org/works", params=p, headers=UA, timeout=60)
            if r.status_code == 200:
                return r.json()["message"]["items"]
            if r.status_code == 429:
                time.sleep(6 * (attempt + 1)); continue
            return None
        except Exception as e:
            time.sleep(4); 
    return None

def fmt(it):
    a = it.get("author", []) or []
    auth = [f"{x.get('given','')} {x.get('family','')}".strip() for x in a][:6]
    dateparts = it.get("published", {}).get("date-parts", [[None]])[0]
    year = dateparts[0] if dateparts else None
    return {
        "title": (it.get("title") or [""])[0],
        "year": year,
        "authors": auth,
        "venue": (it.get("container-title") or [""])[0] if it.get("container-title") else None,
        "doi": it.get("DOI"),
        "type": it.get("type"),
        "cited": it.get("is-referenced-by-count"),
        "abstract": it.get("abstract"),
    }

def main():
    seen = {}
    if os.path.exists(OUT):
        seen = json.load(open(OUT, encoding="utf-8"))
    done = seen.get("_done", [])
    for q, rows in QUERIES:
        if q in done:
            print("skip:", q, flush=True); continue
        items = query_cr(q, rows)
        if items is None:
            print("ERR:", q, flush=True); time.sleep(3); continue
        seen.setdefault(q, {"runs": []})["runs"].append([fmt(x) for x in items])
        seen.setdefault("_done", []).append(q)
        json.dump(seen, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"OK {q}: {len(items)} items", flush=True)
        time.sleep(1.0)
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    main()
