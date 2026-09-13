#!/usr/bin/env python3
"""
RCEP version of Ding-Haoyuan (2024) design: link-breakage / link-entry DID.

Mirrors Ding et al. (China Industrial Economics, 2024):
  - Outcome: Break (active t -> inactive t+1) and Entry (inactive/absent t-1 -> active t)
  - Treatment: RCEP partner (Post2022 x RCEP_ij), relationship-pair level
  - FE: pair FE (phi_ij) + time FE (year) + firm x year FE (cn_id x year) +
        industry x year (via cn_id-year already absorbing firm-time shocks)
  - Clustered SE at partner country (Ding clusters at relationship; but treatment
    varies at country level -> cluster at partner country to be honest)
  - Baseline characteristics x Post interaction (Greenland et al. 2020)

Uses pyfixest for high-dimensional FE (relationship-pair FE = 78k groups).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyfixest as pf

DATA = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP_JAE_修订/data/derived/pair_year.parquet")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题5增链断链")
AUDIT.mkdir(parents=True, exist_ok=True)


def build(df: pd.DataFrame) -> pd.DataFrame:
    d = df.sort_values(["pair_id", "year"]).copy()
    d["active_next"] = d.groupby("pair_id")["active"].shift(-1)
    d["active_prev"] = d.groupby("pair_id")["active"].shift(1)
    d["break"] = ((d["active"] == 1) & (d["active_next"] == 0)).astype(int)
    d["entry"] = ((d["active"] == 1) & (d["active_prev"] != 1)).astype(int)
    d["post"] = (d["year"] >= 2022).astype(int)
    d["rcep"] = d["rcep"].astype(int)
    d["post_x_rcep"] = d["post"] * d["rcep"]
    # baseline characteristics (2017, first value per pair) for x Post interactions
    for c in ["supplier_link", "offshore", "asia_control", "age_2021"]:
        if c in d.columns:
            base = d.groupby("pair_id")[c].transform("first")
            d[f"{c}_x_post"] = base * d["post"]
    d["pair_fe"] = d["pair_id"].astype(str)
    d["firm_year_fe"] = d["cn_id"].astype(str) + "_" + d["year"].astype(str)
    d["country"] = d["partner_country"].astype(str)
    return d


def run(d, outcome):
    # Ding-style: pair FE + year FE + firm-year FE, cluster by partner country
    fml = f"{outcome} ~ post_x_rcep + supplier_link_x_post + offshore_x_post + asia_control_x_post + age_2021_x_post | pair_fe + year + firm_year_fe"
    try:
        m = pf.feols(
            fml, data=d, vcov={"CRV1": "country"},
            fixef_rm="none", lean=True,
        )
        t = m.tidy()
        return {
            "outcome": outcome,
            "coef": float(t.loc["post_x_rcep", "Estimate"]),
            "se": float(t.loc["post_x_rcep", "Std. Error"]),
            "p": float(t.loc["post_x_rcep", "Pr(>|t|)"]),
            "n": int(m._N),
            "n_clusters": int(d["country"].nunique()),
        }
    except Exception as e:
        return {"outcome": outcome, "error": str(e), "n": len(d)}


def main():
    df = pd.read_parquet(DATA)
    d = build(df)
    print(f"Panel: {len(d)} rows, {d['pair_id'].nunique()} pairs, {d['country'].nunique()} countries")
    print(f"break events={d['break'].sum()}, entry events={d['entry'].sum()}")

    results = []
    for outcome in ["break", "entry"]:
        r = run(d, outcome)
        results.append(r)
        if "error" in r:
            print(f"{outcome}: ERROR {r['error']}")
        else:
            print(f"{outcome}: coef={r['coef']:+.5f} se={r['se']:.5f} p={r['p']:.4f} N={r['n']} clusters={r['n_clusters']}")

    # Robustness: logit-style LPM already; also run without firm-year FE (common trend check)
    print("\n=== 无企业×年份FE版(看共同趋势是否被吸收) ===")
    for outcome in ["break", "entry"]:
        fml = f"{outcome} ~ post_x_rcep | pair_fe + year"
        m = pf.feols(fml, data=d, vcov={"CRV1": "country"}, fixef_rm="none", lean=True)
        t = m.tidy()
        print(f"{outcome}: coef={t.loc['post_x_rcep','Estimate']:+.5f} p={t.loc['post_x_rcep','Pr(>|t|)']:.4f}")

    (AUDIT / "ding_style_results.json").write_text(json.dumps(results, indent=2, default=float))
    pd.DataFrame(results).to_csv(OUT / "topic5_break_entry_did.csv", index=False)
    print("\nSaved topic5_break_entry_did.csv + audit")


if __name__ == "__main__":
    main()
