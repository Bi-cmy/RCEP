#!/usr/bin/env python3
"""
Topic 3 — First-FTA vs existing-FTA: did RCEP's first China-Japan FTA shift
China's import sourcing?

Identification (per aer-identification):
  - Japan is the only RCEP partner with a real pre-policy MFN/legacy baseline
    (no prior China-Japan FTA) => the genuine "first FTA" treatment arm.
  - ASEAN partners already had ACFTA (zero base) => weak/absent treatment arm
    (useful contrast, not treated effectively).
  - Continuous treatment exposure = pre-policy baseline rate (JPN high, ASEAN ~0),
    interacted with Post2022. Product FE + year FE; HS2-chapter clustered SEs.
  - Outcomes: japan_import_share (direct first-FTA effect) + supplier_hhi /
    supplier_effective_number / rcep_import_share (sourcing reconfiguration).

Also runs first-vs-existing contrast via partner-group interaction and an
event study with joint pre-trend Wald test. Results archived regardless.
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
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题3中日首次FTA")
AUDIT.mkdir(parents=True, exist_ok=True)

# Japan as the true treatment (first FTA); ASEAN's legacy FTA baseline weak
JAPAN = "JPN"
ASEAN = {"IDN","MYS","PHL","SGP","THA","VNM","BRN","KHM","LAO","MMR"}


def indexed(df):
    return df.sort_values(["hs6", "year"]).set_index(["hs6", "year"])


def build_primary_exposure() -> pd.DataFrame:
    pol = pd.read_csv(POL / "china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    # For each partner x hs6, the policy-predetermined baseline (Japan's is high)
    base = pol.groupby(["partner_iso3", "hs6"])["pre_rcep_baseline_pct"].first().reset_index()
    pk = base.pivot(index="hs6", columns="partner_iso3", values="pre_rcep_baseline_pct")
    pk = pk.rename_axis(None, axis=1).reset_index()
    for c in ["JPN","KOR"] + sorted(ASEAN):
        if c not in pk.columns:
            pk[c] = 0.0
    pk = pk.fillna(0)
    # Japan exposure (first FTA baseline)
    pk["jpn_exp"] = pk["JPN"]
    # ASEAN exposure (mostly ~0)
    pk["asean_exp"] = pk[list(ASEAN)].mean(axis=1)
    # Korea exposure
    pk["kor_exp"] = pk["KOR"]
    return pk[["hs6", "jpn_exp", "asean_exp", "kor_exp"]]


def main():
    exp = build_primary_exposure()
    print(f"Exposure panel: {exp.shape}")
    print(f"jpn_exp nonzero share: {(exp['jpn_exp']>0).mean():.3f}, mean={exp['jpn_exp'].mean():.3f}")
    print(f"asean_exp nonzero share: {(exp['asean_exp']>0).mean():.3f}, mean={exp['asean_exp'].mean():.3f}")

    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]
    df = sc.merge(exp, on="hs6", how="left")
    df["post"] = (df["year"] >= 2022).astype(float)
    df["post_x_jpn"] = df["post"] * df["jpn_exp"].fillna(0)
    df["post_x_asean"] = df["post"] * df["asean_exp"].fillna(0)

    print(f"\nMerged: {df.shape}, hs6={df['hs6'].nunique()}")

    # Baseline: Japan first-FTA effect on Japan import share
    print("\n=== Japan first-FTA DiD (product FE + year FE, HS2 cluster) ===")
    outcomes = ["japan_import_share", "supplier_hhi", "supplier_effective_number", "rcep_import_share"]
    results = []
    for outcome in outcomes:
        work = df[["hs6", "year", "hs2", outcome, "post_x_jpn", "post_x_asean"]].copy()
        data = indexed(work.dropna(subset=[outcome]).copy())
        model = PanelOLS(data[outcome].astype(float), data[["post_x_jpn", "post_x_asean"]].astype(float),
                         entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
        cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
        res = model.fit(cov_type="clustered", clusters=cl)
        j = float(res.params["post_x_jpn"]); a = float(res.params["post_x_asean"])
        results.append({"outcome": outcome,
                        "jpn_coef": j, "jpn_se": float(res.std_errors["post_x_jpn"]), "jpn_p": float(res.pvalues["post_x_jpn"]),
                        "asean_coef": a, "asean_se": float(res.std_errors["post_x_asean"]), "asean_p": float(res.pvalues["post_x_asean"]),
                        "n": int(res.nobs), "hs6": int(data.index.get_level_values("hs6").nunique())})
        print(f"{outcome:>28}: JPN={j:+.5f}(p={results[-1]['jpn_p']:.3f}) ASEAN={a:+.5f}(p={results[-1]['asean_p']:.3f}) N={results[-1]['n']}")
    pd.DataFrame(results).to_csv(OUT / "topic3_japan_firstFTA.csv", index=False)
    (AUDIT / "topic3_japan_firstFTA.json").write_text(json.dumps(results, indent=2, default=float))

    # --- Event study for japan_import_share: joint pre-trend Wald ---
    print("\n=== Event study: japan_import_share (base=2021) ===")
    work = df.copy()
    work["y"] = work["japan_import_share"].astype(float)
    rel_map = {-4: "m4", -3: "m3", -2: "m2", 0: "p0", 1: "p1", 2: "p2"}
    for rel, name in rel_map.items():
        work[name] = work["jpn_exp"].fillna(0) * work["year"].sub(2022).eq(rel).astype(float)
    terms = list(rel_map.values())
    data = indexed(work.dropna(subset=["y"]).copy())
    model = PanelOLS(data["y"].astype(float), data[terms].astype(float),
                     entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    pre = [t for t in ["m4", "m3", "m2"] if t in res.params.index]
    restriction = np.zeros((len(pre), len(res.params)))
    for i, t in enumerate(pre):
        restriction[i, list(res.params.index).index(t)] = 1
    wald = res.wald_test(restriction)
    coefs = {t: (float(res.params[t]), float(res.pvalues[t])) for t in terms if t in res.params.index}
    evt = {"outcome": "japan_import_share", "joint_pre_p": float(np.asarray(wald.pval).squeeze()), "coefs": coefs}
    pd.Series({k: v[0] for k, v in coefs.items()}).to_csv(OUT / "topic3_event_jpnshare.csv")
    (AUDIT / "topic3_event_jpnshare.json").write_text(json.dumps(evt, indent=2, default=float))
    print(f"  joint pre-trend p={evt['joint_pre_p']:.3f}")
    for t in ["m3", "m2", "p0", "p1"]:
        if t in coefs:
            print(f"    {t}: {coefs[t][0]:+.5f} (p={coefs[t][1]:.3f})")

    print("\nSaved topic3 tables + audit")


if __name__ == "__main__":
    main()
