#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second targeted Crossref + arXiv pass for canonical trade/econ + firm-network causal papers."""
import json, time, requests, os, re

UA = {"User-Agent": "research/1.0 (mailto:research.agent@nousresearch.com)"}
DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "cr_raw2.json")

TARGET = [
    "Barrot Sauvagnat input specificity propagation production networks",
    "Carvalho Nirei Saito Tahbaz supply chain disruptions Great East Japan earthquake",
    "Acemoglu Carvalho Ozdaglar Tahbaz-Salehi network origins of aggregate fluctuations",
    "Antras Chor on the measurement of upstreamness downstreamness",
    "Fally production networks geographic fragmentation",
    "Bernard Moxnes networks and trade",
    "Eaton Kortum Kramarz firm to firm trade imports exports labor market",
    "Antras global value chains conceptual aspects",
    "trade war supply chain firm network China tariff",
    "import variable cost trade war customer supplier China",
    "supply chain exposure tariff shock firm China",
    "firm supply chain network tariff shock resilience",
    "regional trade agreement firm import network formation",
    "trade liberalization supplier relationship new partner formation",
    "input output network trade policy downstream upstream tariff",
    "domestic supply chain trade war exports China Japan",
]

def cr(txt, rows=8):
    for a in range(4):
        try:
            r = requests.get("https://api.crossref.org/works",
                             params={"query.bibliographic": txt, "rows": rows},
                             headers=UA, timeout=60)
            if r.status_code == 200:
                return r.json()["message"]["items"]
            if 429:
                time.sleep(5 * (a + 1)); continue
        except Exception:
            time.sleep(3)
    return []

def arx(txt, n=6):
    try:
        q = 'all:"%s"' % txt
        r = requests.get("http://export.arxiv.org/api/query",
                         params={"search_query": q, "start": 0, "max_results": n}, timeout=60)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            ns = {"a": "http://www.w3.org/2005/Atom"}
            root = ET.fromstring(r.text)
            out = []
            for e in root.findall("a:entry", ns):
                t = e.find("a:title", ns).text.strip().replace("\n", " ")
                # id
                iid = e.find("a:id", ns).text
                out.append({"title": t, "arxiv": iid})
            return out
    except Exception:
        pass
    return []

def fmt(it):
    a = it.get("author", []) or []
    auth = [f"{x.get('given','')} {x.get('family','')}".strip() for x in a][:6]
    dp = it.get("published", {}).get("date-parts", [[None]])[0]
    return {
        "title": (it.get("title") or [""])[0],
        "year": dp[0] if dp else None,
        "authors": auth,
        "venue": (it.get("container-title") or [""])[0] if it.get("container-title") else None,
        "doi": it.get("DOI"), "type": it.get("type"),
        "cited": it.get("is-referenced-by-count"),
    }

res = {}
for q in TARGET:
    res[q] = {"crossref": [fmt(x) for x in cr(q)], "arxiv": arx(q)}
    time.sleep(0.8)
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
print("DONE", len(TARGET))
for q in TARGET:
    print("\n### ", q)
    for x in res[q]["crossref"]:
        print(f"   [CR] ({x['year']}) ({x['cited']}c) {x['title']} | {x['venue']} | {x['doi']}")
    for x in res[q]["arxiv"][:4]:
        print(f"   [AX] {x['title']} | {x['arxiv']}")
