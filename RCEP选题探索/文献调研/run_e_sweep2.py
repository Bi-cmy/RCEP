#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second targeted sweep + abstract pulls for most-relevant CJK / NAR papers."""
import json, os, time, requests

UA = {"User-Agent": "research/1.0 (mailto:research.agent@nousresearch.com)"}
WORKDIR = "C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/文献调研"
os.chdir(WORKDIR)
OUT = "cr_raw_e2.json"

QUERIES = [
    "China Japan Korea RCEP trilateral first free trade agreement",
    "RCEP non-ASEAN five members economic integration",
    "Asia non-ASEAN RCEP members trade study",
    "China Japan Korea RCEP trade diversion trilateral",
    "China Japan Korea FTA empirical analysis panel",
    "Japan Korea free trade agreement never signed tariff",
    "China Japan first ever free trade agreement 2022 RCEP",
    "RCEP preferential tariff utilization China Japan",
    "Northeast Asia regional economic integration RCEP empirical",
    "China Korea Japan supply chain resilience RCEP",
    "East Asia trade agreement network non-ASEAN",
    "economic effects trilateral free trade East Asia ex-post",
]

def cr_search(text, rows=20):
    for a in range(4):
        try:
            r = requests.get("https://api.crossref.org/works",
                             params={"query.bibliographic": text, "rows": rows,
                                     "filter": "type:journal-article", "select": "DOI,title,author,container-title,published,is-referenced-by-count,abstract,type"},
                             headers=UA, timeout=60)
            if r.status_code == 200:
                return r.json()["message"]["items"]
            if r.status_code == 429:
                time.sleep(5*(a+1)); continue
            return []
        except Exception:
            time.sleep(3)
    return []

def cr_doi(doi):
    try:
        r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=45)
        if r.status_code == 200:
            return r.json()["message"]
    except Exception:
        pass
    return None

# --- sweep 2 ---
raw = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
done = set(raw.keys())
for q in QUERIES:
    if q in done: continue
    items = cr_search(q)
    raw[q] = [{"doi": it.get("DOI"), "title": (it.get("title") or [""])[0],
               "journal": (it.get("container-title") or [""])[0],
               "year": (it.get("published", {}).get("date-parts", [[None]])[0][0]),
               "cites": it.get("is-referenced-by-count"),
               "authors": [f"{a.get('given','')} {a.get('family','')}".strip() for a in (it.get("author") or [])[:8]],
               "abstract": it.get("abstract","")} for it in items]
    json.dump(raw, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK({len(items)}): {q}", flush=True)
    time.sleep(1.2)

# --- abstract pulls for key DOIs ---
KEY_DOIS = {
 "10.1007/s12140-013-9196-5": "Chiang CJK FTA potential",
 "10.11130/jei.2013.28.3.375": "Madhur dual track trilateral",
 "10.1111/pafo.12142": "Zhang CJK FTA why negotiations stalled",
 "10.11644/kiep.eaer.2022.26.1.403": "Armstrong Drysdale RCEP cooperation potential",
 "10.1108/jkt-03-2018-0020": "Li Moon RCEP China Korea",
 "10.11644/kiep.jeai.2015.19.2.293": "Kim Shikher Korea-China FTA long run",
 "10.35611/jkt.2023.27.3.21": "Yin Cheong Korea-China FTA disentangle",
 "10.35611/jkt.2026.30.3.1": "Deng Kim Korea-China DiD gravity",
 "10.35611/jkt.2022.26.6.41": "Li Lee Korea-China policy effects",
 "10.1007/s12140-005-0019-1": "Chan Kuo trilateral trade relations",
 "10.1080/24761028.2021.1907881": "Shimizu AEC and RCEP",
 "10.1162/asep_a_00218": "Cheong Tongzon TPP vs RCEP",
 "10.1016/j.jce.2026.03.006": "Lin et al input tariff gender China",
}
KEY_OUT = {}
for doi, tag in KEY_DOIS.items():
    m = cr_doi(doi)
    if m:
        KEY_OUT[doi] = {"tag": tag, "title": (m.get("title") or [""])[0],
                        "journal": (m.get("container-title") or [""])[0],
                        "year": (m.get("published",{}).get("date-parts",[[None]])[0][0]),
                        "cites": m.get("is-referenced-by-count"),
                        "authors": [f"{a.get('given','')} {a.get('family','')}".strip() for a in (m.get("author") or [])[:8]],
                        "abstract": m.get("abstract","")}
    print(f"DOI OK: {tag} | {doi}", flush=True)
    time.sleep(0.8)
json.dump(KEY_OUT, open("cr_key_abstracts.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("Saved KEY abstracts:", len(KEY_OUT))
print("Sweep2 total items:", sum(len(v) for v in raw.values()))
