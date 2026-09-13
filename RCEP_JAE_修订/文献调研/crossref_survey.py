#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crossref-based literature survey for the 'de-coupling vs re-engagement' +
   'US tariffs + RCEP dual-track' angle. Free API, no paywall."""
import json, time, sys, urllib.parse, re
import requests

BASE = "https://api.crossref.org/works"
MAILTO = "research.office.cn@gmail.com"
HEADERS = {"User-Agent": f"lit-survey/1.0 (mailto:{MAILTO})"}

def clean(s):
    if not s: return None
    # remove jats tags
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def strip_html(s):
    if not s: return None
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def crossref_search(q, rows=15, from_pub="2017-01-01", type_filter="journal-article"):
    params = {
        "query.bibliographic": q,
        "rows": rows,
        "mailto": MAILTO,
        "filter": f"from-pub-date:{from_pub},type:{type_filter}",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=50)
            if r.status_code == 429:
                time.sleep(2*(attempt+1)); continue
            r.raise_for_status()
            return r.json().get("message", {})
        except Exception as e:
            if attempt == 3:
                return {"error": str(e), "items": []}
            time.sleep(2*(attempt+1))
    return {"error": "exhausted", "items": []}

def item_to_dict(it):
    tit = (it.get("title") or ["?"])[0]
    auth = []
    for a in it.get("author", [])[:4]:
        nm = (a.get("given","") + " " + a.get("family","")).strip()
        if nm: auth.append(nm)
    yr = None
    for k in ("published-print","published-online","issued","created"):
        dp = it.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]: yr = dp[0][0]; break
    return {
        "title": tit,
        "year": yr,
        "authors": auth,
        "journal": (it.get("container-title") or [None])[0],
        "doi": it.get("DOI"),
        "cited": it.get("cited-by-count", 0),
        "type": it.get("type"),
        "subjects": it.get("subject") or [],
        "abstract": clean(it.get("abstract")),
    }

def run(queries, out_file, mode="a"):
    store = {}
    if mode == "a":
        try:
            with open(out_file, encoding="utf-8") as f:
                store = json.load(f)
        except Exception:
            store = {}
    for k, q in queries.items():
        msg = crossref_search(q)
        items = [item_to_dict(it) for it in msg.get("items", []) if it.get("title")]
        store[k] = {"query": q, "total": msg.get("total-results"), "error": msg.get("error"), "items": items}
        print(f"[{k}] total={msg.get('total-results')} err={msg.get('error','')} fetched={len(items)}")
        for it in items[:6]:
            print(f"   - {it['year']} | {it['title'][:92]}")
            print(f"      {it['journal'] if it['journal'] else 'N/A'} | cit={it['cited']}")
        time.sleep(1.2)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    return store

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "a"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "crossref_results.json"
    queries = {
        "decoupling": "US China decoupling supply chain reallocation",
        "derisking": "de-risking China supply chain decoupling global south",
        "friendshoring": "friend-shoring re-shoring near-shoring regionalization China supply chain",
        "deglobalization": "China supply chain restructuring deglobalization regionalisation",
        "tradewar_rcep": "US-China trade war RCEP tariff",
        "rcep_firm": "RCEP tariff reduction Chinese firm exports trade diversion",
        "tariff_301": "Section 301 tariffs China exporters firm level evidence",
        "resilience": "supply chain resilience Chinese firms tariff shock exports",
    }
    run(queries, out_file, mode)
