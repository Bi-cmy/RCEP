#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Precision dual-track Crossref batch: US tariff + RCEP in same frame."""
import json, time, sys, urllib.parse, re
import requests

BASE = "https://api.crossref.org/works"
MAILTO = "research.office.cn@gmail.com"
HEADERS = {"User-Agent": f"lit-survey/1.0 (mailto:{MAILTO})"}

def clean(s):
    if not s: return None
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def cs(q, rows=12, from_pub="2017-01-01", type_filter="journal-article"):
    params = {
        "query.bibliographic": q,
        "rows": rows,
        "mailto": MAILTO,
        "filter": f"from-pub-date:{from_pub},type:{type_filter}",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    for _ in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=50)
            if r.status_code == 429:
                time.sleep(2); continue
            r.raise_for_status()
            return r.json().get("message", {})
        except Exception as e:
            time.sleep(2)
    return {"items": []}

def d(it):
    tit = (it.get("title") or ["?"])[0]
    auth = [ (a.get("given","")+" "+a.get("family","")).strip() for a in it.get("author",[])[:4] if (a.get("given","")+" "+a.get("family","")).strip() ]
    yr = None
    for k in ("published-print","published-online","issued","created"):
        dp = it.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]: yr = dp[0][0]; break
    return {"title": tit, "year": yr, "authors": auth,
            "journal": (it.get("container-title") or [None])[0],
            "doi": it.get("DOI"), "cited": it.get("cited-by-count",0),
            "abstract": clean(it.get("abstract"))}

def run(queries, out_file):
    store = {}
    try:
        with open(out_file, encoding="utf-8") as f: store = json.load(f)
    except Exception: store = {}
    for k, q in queries.items():
        m = cs(q)
        items = [d(it) for it in m.get("items", []) if it.get("title")]
        store[k] = {"query": q, "items": items}
        print(f"[{k}] fetched={len(items)}")
        for it in items[:8]:
            print(f"   - {it['year']} | {it['title'][:90]}")
            ab = (it['abstract'] or '')[:130]
            print(f"      {it['journal'] if it['journal'] else 'N/A'} | cit={it['cited']} | ABS: {ab}")
        time.sleep(1.0)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    return store

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "dual_track.json"
    # Query configs: split into two runs for safety (avoid timeout). Pass set via env? Just hardcode 5 queries.
    queries = {
        "rcep_us_tradewar_title": "RCEP US-China trade war tariff",
        "rcep_trade_diversion": "RCEP trade diversion US China tariff evasion",
        "rcep_firm_export": "RCEP tariff cut Chinese firm exports effect",
        "us_tariff_rcep_pull": "US tariff shock RCEP regional trade agreement China firms",
        "tariff_ea_evidence": "US-China tariff war export reallocation firm evidence emerging Asia",
    }
    run(queries, out)
