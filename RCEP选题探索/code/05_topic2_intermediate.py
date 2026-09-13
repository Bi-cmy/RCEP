#!/usr/bin/env python3
"""
Topic 2 — RCEP cumulative rules of origin: intermediate vs final goods
difference in import-source diversification.

Rationale (Bombarda & Gamberoni 2013): regional cumulation lowers the cost of
sourcing intermediates across member countries. If RCEP's cumulation rule
works, the effect on import sourcing should be STRONGER for intermediate goods
(BEC) than final goods, because intermediates are what can be cumulated.

Design (aer-identification):
  - Outcome: supplier_hhi, supplier_effective_number, rcep_import_share,
             japan_import_share, rcep_supplier_count
  - Treatment: Post2022 x (Japan/global policy-predetermined exposure) x BEC-intermediate
    => triple interaction identifying the incremental effect on intermediates.
  - Product FE + year FE; HS2-chapter clustered SEs.
  - Event study joint pre-trend Wald for the intermediate interaction.

This uses product-attribute heterogeneity (BEC) as the identification axis,
which is the cleanest way around the Japan-dominance problem.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

POL = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_tariffs")
TD = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题2中间品累积")
AUDIT.mkdir(parents=True, exist_ok=True)


def indexed(df):
    return df.sort_values(["hs6", "year"]).set_index(["hs6", "year"])


def build_exposure() -> pd.DataFrame:
    pol = pd.read_csv(POL / "china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    base = pol.groupby(["partner_iso3", "hs6"])["pre_rcep_baseline_pct"].first().reset_index()
    pk = base.pivot(index="hs6", columns="partner_iso3", values="pre_rcep_baseline_pct").fillna(0)
    pk = pk.rename_axis(None, axis=1).reset_index()
    for c in ["JPN", "KOR"]:
        if c not in pk.columns:
            pk[c] = 0.0
    pk["jpn_exp"] = pk["JPN"]
    pk["kor_exp"] = pk["KOR"]
    return pk[["hs6", "jpn_exp", "kor_exp"]]


def main():
    exp = build_exposure()
    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]

    df = sc.merge(exp, on="hs6", how="left")
    df["post"] = (df["year"] >= 2022).astype(float)
    df["intm"] = df["bec5_intermediate_strict"].fillna(0).astype(float)
    df["jpn_exp"] = df["jpn_exp"].fillna(0)
    df["kor_exp"] = df["kor_exp"].fillna(0)

    # Triple interaction: Post x Japan-exposure x BEC-intermediate
    df["post_x_jpn"] = df["post"] * df["jpn_exp"]
    df["post_x_jpn_x_intm"] = df["post"] * df["jpn_exp"] * df["intm"]
    df["post_x_intm"] = df["post"] * df["intm"]
    df["jpn_x_intm"] = df["jpn_exp"] * df["intm"]

    print(f"Merged: {df.shape}, hs6={df['hs6'].nunique()}, intermediate share={df['intm'].mean():.3f}")
    print(f"jpn_exp nonzero: {(df['jpn_exp']>0).mean():.3f}")

    outcomes = ["supplier_hhi", "supplier_effective_number", "rcep_import_share",
                "japan_import_share", "rcep_supplier_count"]
    print("\n=== Triple interaction: Post x Japan-exposure x BEC-intermediate ===")
    results = []
    for outcome in outcomes:
        work = df[["hs6", "year", "hs2", outcome, "post_x_jpn", "post_x_jpn_x_intm"]].copy()
        data = indexed(work.dropna(subset=[outcome]).copy())
        model = PanelOLS(data[outcome].astype(float), data[["post_x_jpn", "post_x_jpn_x_intm"]].astype(float),
                         entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
        cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
        res = model.fit(cov_type="clustered", clusters=cl)
        r = {"outcome": outcome,
             "post_x_jpn": float(res.params["post_x_jpn"]), "se_jpn": float(res.std_errors["post_x_jpn"]), "p_jpn": float(res.pvalues["post_x_jpn"]),
             "triple": float(res.params["post_x_jpn_x_intm"]), "se_triple": float(res.std_errors["post_x_jpn_x_intm"]), "p_triple": float(res.pvalues["post_x_jpn_x_intm"]),
             "n": int(res.nobs)}
        results.append(r)
        print(f"{outcome:>28}: base={r['post_x_jpn']:+.5f}(p={r['p_jpn']:.3f})  "
              f"x_intm={r['triple']:+.5f}(p={r['p_triple']:.3f})  N={r['n']}")
    pd.DataFrame(results).to_csv(OUT / "topic2_intermediate_triple.csv", index=False)
    (AUDIT / "topic2_intermediate_triple.json").write_text(json.dumps(results, indent=2, default=float))

    # Event study on the triple for the primary outcome japan_import_share
    print("\n=== Event study: japan_import_share, triple interaction (base=2021) ===")
    work = df.copy(); work["y"] = work["japan_import_share"].astype(float)
    rel_map = {-4: "tm4", -3: "tm3", -2: "tm2", 0: "tp0", 1: "tp1", 2: "tp2"}
    for rel, name in rel_map.items():
        work[name] = work["jpn_exp"] * work["intm"] * work["year"].sub(2022).eq(rel).astype(float)
    terms = list(rel_map.values())
    data = indexed(work.dropna(subset=["y"]).copy())
    model = PanelOLS(data["y"].astype(float), data[terms].astype(float),
                     entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    pre = [t for t in ["tm4", "tm3", "tm2"] if t in res.params.index]
    restriction = np.zeros((len(pre), len(res.params)))
    for i, t in enumerate(pre):
        restriction[i, list(res.params.index).index(t)] = 1
    wald = res.wald_test(restriction)
    coefs = {t: (float(res.params[t]), float(res.pvalues[t])) for t in terms if t in res.params.index}
    evt = {"outcome": "japan_import_share", "joint_pre_p": float(np.asarray(wald.pval).squeeze()), "coefs": coefs}
    (AUDIT / "topic2_event_triple.json").write_text(json.dumps(evt, indent=2, default=float))
    print(f"  joint pre-trend p={evt['joint_pre_p']:.3f}")
    for t in ["tm3", "tm2", "tp0", "tp1"]:
        if t in coefs:
            print(f"    {t}: {coefs[t][0]:+.5f} (p={coefs[t][1]:.3f})")

    print("\nSaved topic2 tables + audit")


if __name__ == "__main__":
    main()
