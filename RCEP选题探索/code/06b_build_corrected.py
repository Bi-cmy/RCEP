#!/usr/bin/env python3
"""
06b — Rebuild panel with CORRECTED group split (per E-report institutional facts):

  First-FTA group (from-nowhere, high baseline): JAPAN only.
    Japan has NO prior FTA with China, Korea, Australia, NZ. Its RCEP baseline
    tariff rate is the highest (7.5%).
  Existing/deepening group (low baseline): KOREA + ASEAN + AUS/NZL.
    KOREA signed China-Korea FTA (CKFTA) in 2015 → RCEP is a marginal deepening.
    ASEAN signed ACFTA; AUS/NZL / others too.

The previous build wrongly pooled JPN+KOR as 'first'. This corrects it:
  japan_base   = pre-policy baseline rate of Japan (first-FTA intensity)
  kor_base     = baseline rate of Korea (existing-FTA, control)
  existing_base= baseline of ASEAN+AUS+NZL (existing-FTA, control)

Outputs a corrected parquet.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

POL = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_tariffs")
TD = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/data")
OUT.mkdir(parents=True, exist_ok=True)

FIRST = {"JPN"}                                  # truly from-nowhere
KOREA = {"KOR"}                                  # CKFTA 2015 (existing, control)
EXISTING = {"AUS","NZL","IDN","MYS","PHL","SGP","THA","VNM","BRN","KHM","LAO","MMR"}


def main():
    pol = pd.read_csv(POL / "china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    feats = pol.groupby(["partner_iso3", "hs6"], as_index=False).agg(
        baseline=("pre_rcep_baseline_pct", "first"),
        cut=("first_year_incremental_cut_pct", "first"),
    )
    piv = feats.pivot(index="hs6", columns="partner_iso3", values=["baseline", "cut"]).fillna(0)
    piv.columns = [f"{v}_{p}" for v, p in piv.columns]

    for group, names in [("first", FIRST), ("kor", KOREA), ("existing", EXISTING)]:
        bs = [f"baseline_{p}" for p in names if f"baseline_{p}" in piv.columns] or [0.0]
        cuts = [f"cut_{p}" for p in names if f"cut_{p}" in piv.columns] or [0.0]
        piv[f"{group}_base"] = piv[bs].mean(axis=1)
        piv[f"{group}_cut"] = piv[cuts].mean(axis=1)
    exp = piv.reset_index()[["hs6", "first_base", "first_cut", "kor_base", "kor_cut", "existing_base", "existing_cut"]]

    # status check
    print(f"first_base (Japan): nonzero {(exp['first_base']>0).mean():.3f}, mean={exp['first_base'].mean():.3f}")
    print(f"kor_base:            nonzero {(exp['kor_base']>0).mean():.3f}, mean={exp['kor_base'].mean():.3f}")
    print(f"existing_base:       nonzero {(exp['existing_base']>0).mean():.3f}, mean={exp['existing_base'].mean():.3f}")

    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]
    panel = sc.merge(exp, on="hs6", how="left")
    panel["post"] = (panel["year"] >= 2022).astype(float)
    # Interaction terms (intensity is continuous; standalone intensity absorbed by FE)
    panel["post_x_first"] = panel["post"] * panel["first_base"].fillna(0)
    panel["post_x_kor"] = panel["post"] * panel["kor_base"].fillna(0)
    panel["post_x_existing"] = panel["post"] * panel["existing_base"].fillna(0)
    panel["post_x_first_cut"] = panel["post"] * panel["first_cut"].fillna(0)
    panel["post_x_kor_cut"] = panel["post"] * panel["kor_cut"].fillna(0)
    panel["intm"] = panel["bec5_intermediate_strict"].fillna(0).astype(float)
    panel["post_x_first_x_intm"] = panel["post"] * panel["first_base"].fillna(0) * panel["intm"]
    panel["post_x_kor_x_intm"] = panel["post"] * panel["kor_base"].fillna(0) * panel["intm"]

    print(f"\nMerged panel: {panel.shape}")
    print(f"post_x_first nonzero: {(panel['post_x_first']!=0).mean():.3f}")
    print(f"post_x_kor nonzero:   {(panel['post_x_kor']!=0).mean():.3f}")
    print(f"post_x_existing nonzero: {(panel['post_x_existing']!=0).mean():.3f}")

    panel.to_parquet(OUT / "first_vs_existing_corrected.parquet", index=False)
    print("Saved data/first_vs_existing_corrected.parquet")


if __name__ == "__main__":
    main()
