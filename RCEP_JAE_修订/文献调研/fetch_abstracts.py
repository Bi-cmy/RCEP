#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch full abstracts for shortlisted candidates from Crossref by DOI."""
import json, time, re, urllib.parse
import requests

H = {"User-Agent": "lit-survey/1.0 (mailto:research.office.cn@gmail.com)"}
MAILTO = "research.office.cn@gmail.com"

def clean(s):
    if not s: return None
    s = re.sub(r"<[^>]+>", "", s); s = re.sub(r"&(?:amp|lt|gt|quot|#39);"," ",s)
    return re.sub(r"\s+"," ",s).strip()

# Gather all items from saved JSON files
items = {}
for fn in ("dual_track.json","crossref_results.json","anchor_papers.json"):
    try:
        with open(fn,encoding="utf-8") as f:
            store = json.load(f)
    except Exception as e:
        print("skip",fn,e); continue
    for k,v in store.items():
        for it in v.get("items",[]):
            if it.get("doi"):
                items[it["doi"]] = it

# shortlist by relevance keywords
KEYS = ["rcep","regional comprehensive","trade war","trade tension","decoupling","reallocation",
        "re-engage","reshor","friend-shor","near-shor","trade diversion","regionalis","regionalization",
        "asean","vietnam","push","pull","tariff reduction","supply chain"]
short = {d:i for d,i in items.items()
         if any(k in (i["title"] or "").lower() or k in (i.get("abstract") or "").lower() for k in KEYS)}
# Rank: penalize clearly-off-topic (grain/green) lightly, but keep for context
print(f"shortlisted {len(short)} items\n")

def fetch(doi):
    try:
        r = requests.get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}",
                         headers=H, timeout=50)
        if r.status_code==429: time.sleep(2); return None
        r.raise_for_status(); return r.json().get("message",{})
    except Exception as e:
        return None

# Manual dedupe by (title,year), limit to ~22 for readability
seen=set(); out=[]
for doi,it in short.items():
    key=(it["title"],it["year"])
    if key in seen: continue
    seen.add(key); out.append((doi,it))

for doi,it in out:
    rec = fetch(doi)
    full_abs = clean(rec.get("abstract")) if rec else it.get("abstract")
    print("="*70)
    print(f"DOI: {doi}\nTITLE: {it['title']}\nYEAR: {it['year']} | {it['journal']}")
    print(f"AUTHORS: {', '.join(it['authors'])}")
    print(f"ABS: {(full_abs or 'NO ABSTRACT')[:600]}")
    time.sleep(0.8)
