#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bulk Crossref sweep for China-Japan-Korea trilateral / bilateral FTA empirics.
Saves raw JSON incrementally to cr_raw_e.json, dedupes by DOI, ranks by citations.
"""
import sys, os, json, time, re, argparse

UA = {"User-Agent": "research/1.0 (mailto:research.agent@nousresearch.com)"}
OUT = "cr_raw_e.json"
DONE = "cr_done_e.json"
WORKDIR = "C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/文献调研"
os.chdir(WORKDIR)

QUERIES = [
    # Trilateral / CJK bloc
    "China Japan Korea trilateral free trade agreement",
    "China Japan Korea free trade agreement Northeast Asia",
    "trilateral free trade agreement China Japan Korea economic effect",
    "China Japan Korea economic integration trade agreement",
    "China Japan Korea FTA trade creation",
    "Northeast Asia free trade agreement China Japan Korea",
    "trilateral cooperation East Asia China Japan Korea",
    # Bilateral first-time pairs
    "China Japan free trade agreement RCEP tariff",
    "China Korea free trade agreement FTA tariff",
    "Japan Korea free trade agreement tariff",
    "China Japan bilateral tariff reduction RCEP",
    "China Korea bilateral tariff concessions",
    "China Japan Korea tariff reduction",
    # Non-ASEAN RCEP as a group / RCEP core
    "Regional Comprehensive Economic Partnership non-ASEAN members",
    "RCEP trade creation trade diversion East Asia",
    "RCEP China Japan Korea tariff liberalization",
    "RCEP North East Asia export supply chain",
    "ASEAN plus six free trade agreement trade",
    # methodology / related
    "China Japan Korea trade gravity model tariff",
    "China Japan Korea common market economic integration",
]

def cr_search(text, rows=18):
    for a in range(4):
        try:
            r = requests.get("https://api.crossref.org/works",
                             params={"query.bibliographic": text, "rows": rows,
                                     "filter": "type:journal-article", "select": "DOI,title,author,container-title,published,is-referenced-by-count,abstract,type"},
                             headers=UA, timeout=60)
            if r.status_code == 200:
                return r.json()["message"]["items"]
            if r.status_code == 429:
                time.sleep(5 * (a + 1)); continue
            return []
        except Exception:
            time.sleep(3)
    return []

def main():
    done = json.load(open(DONE, encoding="utf-8")) if os.path.exists(DONE) else []
    raw = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    for q in QUERIES:
        if q in done:
            print("SKIP:", q); continue
        items = cr_search(q)
        raw[q] = [{"doi": it.get("DOI"), "title": (it.get("title") or [""])[0],
                   "container-title": (it.get("container-title") or [""])[0],
                   "journal": (it.get("container-title") or [""])[0],
                   "year": (it.get("published", {}).get("date-parts", [[None]])[0][0]),
                   "cites": it.get("is-referenced-by-count"),
                   "authors": [f"{a.get('given','')} {a.get('family','')}".strip() for a in (it.get("author") or [])[:8]],
                   "abstract": it.get("abstract", "")} for it in items]
        done.append(q)
        json.dump(raw, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump(done, open(DONE, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"OK({len(items)}): {q}", flush=True)
        time.sleep(1.2)
    print("DONE total raw items:", sum(len(v) for v in raw.values()))
    # dedupe by DOI
    bydoi = {}
    for q, items in raw.items():
        for it in items:
            d = it.get("doi")
            if d and d not in bydoi:
                bydoi[d] = it
    print("UNIQUE DOIs:", len(bydoi))
    ranked = sorted(bydoi.values(), key=lambda x: x.get("cites") or 0, reverse=True)
    # top 25 by citations, print compact
    print("\n==== TOP 25 BY CITATIONS ====")
    for it in ranked[:25]:
        yr = it.get("year")
        print(f"[{yr}] ({it.get('cites')}c) {', '.join(it['authors'][:3])} | {it['title'][:110]} | {it.get('journal')} | {it.get('doi')}")

if __name__ == "__main__":
    import requests
    main()
