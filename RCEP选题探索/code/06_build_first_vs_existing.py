#!/usr/bin/env python3
"""
Build the merged panel for the "First-FTA (JP+KR) vs Existing-FTA (ASEAN+AU/NZ)"
causal design. Falls back to policy-panel exposures for JP/KR (high baseline)
and constructs a first-vs-existing treatment contrast.

This is the data-preparation step (no estimation). It outputs a parquet that
the estimation module consumes.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

POL = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_tariffs")
TD = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/data")
OUT.mkdir(parents=True, exist_ok=True)

# First-FTA partners (no prior China FTA => high baseline): Japan, Korea
FIRST = {"JPN", "KOR"}
# Existing-FTA partners (ACFTA / China-Australia FTA / China-NZ FTA => near-zero): ASEAN10 + AUS/NZL
EXISTING = {"AUS", "NZL", "IDN", "MYS", "PHL", "SGP", "THA", "VNM", "BRN", "KHM", "LAO", "MMR"}
RCEP = FIRST | EXISTING


def main():
    pol = pd.read_csv(POL / "china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    pol["year"] = pol["calendar_year"].astype("int64")

    # Per (partner x hs6): pre-policy baseline, first/ultimate incremental cut, post
    feats = pol.groupby(["partner_iso3", "hs6"], as_index=False).agg(
        baseline=("pre_rcep_baseline_pct", "first"),
        cut=("first_year_incremental_cut_pct", "first"),
    )
    # Pivot baseline and cut by partner
    base_piv = feats.pivot(index="hs6", columns="partner_iso3", values="baseline").fillna(0)
    cut_piv = feats.pivot(index="hs6", columns="partner_iso3", values="cut").fillna(0)
    for c in FIRST | EXISTING:
        if c not in base_piv.columns:
            base_piv[c] = 0.0
            cut_piv[c] = 0.0
    base_piv = base_piv.rename_axis(None, axis=1).reset_index()
    cut_piv = cut_piv.rename_axis(None, axis=1).reset_index()

    # First-FTA exposure = max/mean of JPN+KOR baseline (the real treatment)
    base_piv["first_base"] = base_piv[["JPN", "KOR"]].mean(axis=1)
    base_piv["existing_base"] = base_piv[list(EXISTING)].mean(axis=1)
    cut_piv["first_cut"] = cut_piv[["JPN", "KOR"]].mean(axis=1)
    cut_piv["existing_cut"] = cut_piv[list(EXISTING)].mean(axis=1)

    exp = base_piv[["hs6", "first_base", "existing_base"]].merge(
        cut_piv[["hs6", "first_cut", "existing_cut"]], on="hs6", how="left")

    print(f"Exposure (hs6): {exp.shape}")
    print(f"  first_base nonzero share: {(exp['first_base']>0).mean():.3f}, mean={exp['first_base'].mean():.3f}")
    print(f"  existing_base nonzero share: {(exp['existing_base']>0).mean():.3f}, mean={exp['existing_base'].mean():.3f}")
    print(f"  first_cut nonzero nonzero share: {(exp['first_cut']>0).mean():.3f}")
    print(f"  existing_cut nonzero share: {(exp['existing_cut']>0).mean():.3f}")

    # Supply-chain outcome panel (hs6 x year) for source structure
    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]
    panel = sc.merge(exp, on="hs6", how="left")
    panel["post"] = (panel["year"] >= 2022).astype(float)
    panel["post_x_first"] = panel["post"] * panel["first_base"].fillna(0)
    panel["post_x_existing"] = panel["post"] * panel["existing_base"].fillna(0)
    panel["post_x_first_cut"] = panel["post"] * panel["first_cut"].fillna(0)
    panel["post_x_existing_cut"] = panel["post"] * panel["existing_cut"].fillna(0)
    # BEC intermediate
    if "bec5_intermediate_strict" in panel.columns:
        panel["intm"] = panel["bec5_intermediate_strict"].fillna(0).astype(float)
    print(f"\nMerged panel: {panel.shape}, hs6={panel['hs6'].nunique()}")
    print(f"post_x_first nonzero share: {(panel['post_x_first']!=0).mean():.3f}")
    print(f"post_x_existing nonzero share: {(panel['post_x_existing']!=0).mean():.3f}")

    panel.to_parquet(OUT / "first_vs_existing_panel.parquet", index=False)
    print("Saved data/first_vs_existing_panel.parquet")


if __name__ == "__main__":
    main()
