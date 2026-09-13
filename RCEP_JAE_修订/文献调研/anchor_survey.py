#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anchor canonical papers via Crossref title + author search."""
import json, time, sys, urllib.parse, re
import requests

BASE = "https://api.crossref.org/works"
MAILTO = "research.office.cn@gmail.com"
H = {"User-Agent": f"lit-survey/1.0 (mailto:{MAILTO})"}

def clean(s):
    if not s: return None
    s = re.sub(r"<[^>]+>", "", s); return re.sub(r"\s+"," ",s).strip()

def cs(params, rows=8):
    params.update({"rows": rows, "mailto": MAILTO,
                   "filter": "from-pub-date:2016-01-01,type:journal-article"})
    url = BASE + "?" + urllib.parse.urlencode(params)
    for _ in range(4):
        try:
            r = requests.get(url, headers=H, timeout=50)
            if r.status_code == 429: time.sleep(2); continue
            r.raise_for_status(); return r.json().get("message", {})
        except Exception: time.sleep(2)
    return {"items": []}

def d(it):
    tit = (it.get("title") or ["?"])[0]
    auth = [ (a.get("given","")+" "+a.get("family","")).strip() for a in it.get("author",[])[:5] if (a.get("given","")+" "+a.get("family","")).strip() ]
    yr=None
    for k in ("published-print","published-online","issued","created"):
        dp=it.get(k,{}).get("date-parts",[[None]])
        if dp and dp[0] and dp[0][0]: yr=dp[0][0]; break
    return {"title":tit,"year":yr,"authors":auth,"journal":(it.get("container-title") or [None])[0],
            "doi":it.get("DOI"),"cited":it.get("cited-by-count",0),"abstract":clean(it.get("abstract"))}

# Anchor papers (title phrase searches)
anchors = {
    "fajgelbaum": "Trade War and Global Reallocations",
    "cavallo": "Tariff Pass-Through and Substitution Barcode-Level Evidence US-China Trade War",
    "amiti": "The Impact of the 2018 Tariffs on Prices and Welfare",
    "flaaen": "The Cost of the 2018 Tariffs on US Consumers",
    "handley": "Trade War and trade wars tariff uncertainty",
    "rcep_anchor": "Regional Comprehensive Economic Partnership China trade",
    "china_tradewar_firm": "US-China trade war Chinese firms export evidence",
    "trade_diversion_anch": "trade diversion United States tariffs Chinese exporters third-country",
    "china_shock_global": "The China Shock Learning from Labor Market Adjustment",
}
store={}
for k,q in anchors.items():
    m = cs({"query.title": q})
    items=[d(it) for it in m.get("items",[]) if it.get("title")]
    store[k]={"query":q,"items":items}
    print(f"[{k}] {len(items)}")
    for it in items[:4]:
        print(f"   - {it['year']} | {it['title'][:85]} | {it['journal'] if it['journal'] else 'N/A'} | cit={it['cited']} | {it['authors'][0] if it['authors'] else ''}")
    time.sleep(1.0)
with open("anchor_papers.json","w",encoding="utf-8") as f:
    json.dump(store,f,ensure_ascii=False,indent=2)
print("saved anchor_papers.json")
