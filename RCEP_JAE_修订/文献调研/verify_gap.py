#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final verification: search for Chinese firm-level dual (US tariff + RCEP) papers.
Uses both Crossref and Semantic Scholar (free)."""
import json, time, re, urllib.parse
import requests

CC = {"User-Agent": "lit-survey/1.0 (mailto:research.office.cn@gmail.com)"}
MAILTO = "research.office.cn@gmail.com"

def cs(q, rows=10):
    params={"query.bibliographic":q,"rows":rows,"mailto":MAILTO,
            "filter":"from-pub-date:2017-01-01,type:journal-article"}
    url="https://api.crossref.org/works?"+urllib.parse.urlencode(params)
    for _ in range(3):
        try:
            r=requests.get(url,headers=CC,timeout=50)
            if r.status_code==429: time.sleep(2); continue
            r.raise_for_status(); return r.json().get("message",{}).get("items",[])
        except Exception: time.sleep(2)
    return []

def ss(q, limit=10):
    """Semantic Scholar aad graph search. Free unauthenticated but rate-limited."""
    params={"query":q,"limit":limit,"fields":"title,year,venue,externalIds,abstract,authors"}
    url="https://api.semanticscholar.org/graph/v1/paper/search?"+urllib.parse.urlencode(params)
    try:
        r=requests.get(url,headers=CC,timeout=45)
        if r.status_code!=200: return ("HTTP",r.status_code)
        return r.json().get("data",[])
    except Exception as e:
        return ("ERR",str(e))

def show(it):
    y=it.get('year'); t=it.get('title','?')
    v=(it.get('journal') or it.get('venue') or 'N/A')
    aul=(it.get('authors') or [])
    a0=aul[0].get('name') if aul else ''
    print(f"   - {y} | {t[:88]} | {v} | {a0}")

# Verification queries targeting the EXACT desired design
CQ = [
 "RCEP China listed firms export tariff dual shock supply chain",
 "RCEP trade war Chinese exporters firm-level double shock tariff",
 "US tariff RCEP China firm supply chain reconfiguration evidence",
 "RCEP China firm supply chain shifting ASEAN trade war",
 "Chinese firms trade war RCEP exports margin reallocating",
]
print("="*70); print("CROSSREF verification:")
for q in CQ:
    items=cs(q)
    print(f"[CR] {q} -> {len(items)}")
    for it in items[:4]: show(it)
    time.sleep(1.0)

print("\n" + "="*70); print("SEMANTIC SCHOLAR verification:")
SQ = [
 "RCEP Chinese listed firms tariff exposure exports",
 "US China trade war RCEP trade diversion Chinese exporters",
 "RCEP trade war China supply chain reallocation firm",
 "RCEP tariff China firm exports origin rules",
]
for q in SQ:
    d=ss(q)
    if isinstance(d,tuple):
        print(f"[SS] {q} -> {d}"); time.sleep(2); continue
    print(f"[SS] {q} -> {len(d)}")
    for it in d[:5]: show(it)
    time.sleep(2)
