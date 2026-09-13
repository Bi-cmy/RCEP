#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAlex search helper with polite-pool + retry/backoff."""
import json, time, sys, urllib.request, urllib.parse

MAILTO = "test@example.com"
BASE = "https://api.openalex.org/works"

def get(url, tries=6, wait=3.0):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"research/1.0 (mailto:{MAILTO})"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = wait * 1.8
                time.sleep(wait)
                continue
            return {"error": f"HTTP {e.code}", "url": url}
        except Exception as e:
            time.sleep(2)
            return {"error": str(e), "url": url}
    return {"error": "too many retries", "url": url}

def search(query, per_page=25, extra=""):
    q = urllib.parse.quote(query)
    url = f"{BASE}?search={q}&per_page={per_page}&mailto={MAILTO}&sort=cited_by_count:desc{extra}"
    return get(url)

def titlecase(t):
    if not t: return ""
    # title_display if present
    return t

def summarize(works):
    out = []
    for w in works:
        out.append({
            "id": w.get("id"),
            "doi": w.get("doi"),
            "title": w.get("title") or w.get("display_name"),
            "year": w.get("publication_year"),
            "type": w.get("type"),
            "cited": w.get("cited_by_count"),
            "host": (w.get("primary_location") or {}).get("source", {}).get("display_name") if (w.get("primary_location") or {}).get("source") else None,
            "authors": [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")][:6],
        })
    return out

if __name__ == "__main__":
    qs = [
        "supply chain network diversification",
        "supply chain structure geographic concentration customers",
        "supplier network foreign direct investment regional integration",
        "customer supplier relationships international trade network",
    ]
    for q in qs:
        print(f"\n### QUERY: {q}")
        res = search(q, per_page=10)
        if "results" not in res:
            print("ERROR:", res.get("error"), res.get("url"))
            continue
        print("count:", res["meta"]["count"])
        for item in summarize(res["results"]):
            print(f"  - [{item['year']}] ({item['cited']}c) {item['title']}")
            print(f"      DOI={item['doi']} | {item['host']} | {item['type']}")
        time.sleep(1.2)
