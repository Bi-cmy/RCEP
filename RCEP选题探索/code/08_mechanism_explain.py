#!/usr/bin/env python3
"""
Mechanism tests to explain the "counter-intuitive" sign (Japan first-FTA ->
China's Japan import SHARE falls), distinguishing:

  H_denominator  : share fell because China's TOTAL imports grew (not a real
                   fall in Japan-supplied imports) - mechanical.
  H_diversify    : first-FTA tariff cut lowered switching costs, so China
                   diversified import sources AWAY from single reliance on Japan
                   (import-source diversification / reallocation).
  H_transfer     : China reallocated sourcing from Japan toward OTHER RCEP
                   members (Korea / ASEAN) - trade diversion / source reallocation.

Tests (two-way FE, hs6 FE + year FE, hs2 cluster), on the source-level
(partner x hs6 x year) panel:
  1. ln(japan_import_value) vs ln(total) - is the Japan-denominated-import share
     fall driven by a numerator (Japan) or denominator (total) effect?
  2. Japan share vs Korea share vs other-RCEP share - did the reallocation go to
     Korea/other RCEP (trade diversion)?
  3. supplier_hhi / supplier_effective_number - overall diversification (source
     diversification mechanism).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

TD = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/机制检验_反直觉解释")
AUDIT.mkdir(parents=True, exist_ok=True)

FIRST = {"JPN"}
KOREA = {"KOR"}
OTHER_RCEP = {"AUS","NZL","IDN","MYS","PHL","SGP","THA","VNM","BRN","KHM","LAO","MMR"}


def indexed(df):
    return df.sort_values(["entity", "year"]).set_index(["entity", "year"])


def twfe(df, outcome, treat):
    work = df[["entity", "year", "hs2", outcome, treat]].copy()
    data = indexed(work.dropna(subset=[outcome]).copy())
    model = PanelOLS(data[outcome].astype(float), data[[treat]].astype(float),
                     entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    return float(res.params[treat]), float(res.pvalues[treat]), int(res.nobs)


def main():
    # Use the partner x hs6 x year source panel for per-partner values
    src = pd.read_parquet(TD / "china_import_source_hs12_model_panel_2015_2024.parquet")
    src["hs6"] = src["hs6"].astype(str).str.zfill(6)
    src["year"] = src["calendar_year"].astype("int64")
    src["hs2"] = src["hs6"].astype(str).str[:2]

    # Build a product x year panel with Japan / Korea / other-RCEP / total import values
    # Use trade_value from the source panel (China's imports by partner x hs6 x year)
    # Note: trade_value here = partner-reported export to China (mirror) per README.
    # Aggregate within groups.
    src["grp"] = np.select(
        [src["partner_iso3"].isin(FIRST), src["partner_iso3"].isin(KOREA),
         src["partner_iso3"].isin(OTHER_RCEP), src["source_group"].eq("rest_world"),
         src["source_group"].eq("non_rcep_asia")],
        ["japan", "kor", "other_rcep", "rest_world", "non_rcep_asia"],
        default="other",
    )
    grp_val = src.groupby(["hs6", "year", "grp"])["trade_value"].sum().unstack(["grp"]).fillna(0).reset_index()
    grp_val["hs2"] = grp_val["hs6"].astype(str).str[:2]
    # total
    grp_val["total"] = grp_val[["japan", "kor", "other_rcep", "rest_world", "non_rcep_asia"]].sum(axis=1)
    grp_val["japan_share"] = grp_val["japan"] / grp_val["total"].replace(0, np.nan)
    grp_val["kor_share"] = grp_val["kor"] / grp_val["total"].replace(0, np.nan)
    grp_val["other_rcep_share"] = grp_val["other_rcep"] / grp_val["total"].replace(0, np.nan)
    grp_val["non_rcep_share"] = (grp_val["non_rcep_asia"] + grp_val["rest_world"]) / grp_val["total"].replace(0, np.nan)

    # Japan-specific first-FTA exposure (pre-policy baseline of Japan)
    # Load from corrected panel exposure by hs6 (Japan baseline fixed per hs6)
    pol = pd.read_csv("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_tariffs/china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    jpn_base = pol[pol["partner_iso3"].eq("JPN")].groupby("hs6")["pre_rcep_baseline_pct"].first().reset_index()
    jpn_base.columns = ["hs6", "jpn_base"]
    grp_val = grp_val.merge(jpn_base, on="hs6", how="left")
    grp_val["jpn_base"] = grp_val["jpn_base"].fillna(0)
    grp_val["post"] = (grp_val["year"] >= 2022).astype(float)
    grp_val["post_x_jpnbase"] = grp_val["post"] * grp_val["jpn_base"]
    grp_val["entity"] = grp_val["hs6"]

    print(f"Source panel: {grp_val.shape}, hs6={grp_val['hs6'].nunique()}")
    print(f"jpn_base nonzero: {(grp_val['jpn_base']>0).mean():.3f}")

    results = {}

    # TEST 1: Denominator effect — Japan absolute import vs total vs share
    print("\n=== TEST 1: is the Japan-share fall driven by numerator or denominator? ===")
    grp_val["japan_abs"] = np.log1p(grp_val["japan"].fillna(0))
    grp_val["total_abs"] = np.log1p(grp_val["total"].fillna(0))
    grp_val["jshare"] = grp_val["japan_share"].fillna(0)
    tests = [
        ("japan_abs", "ln(1+Japan imports)", "post_x_jpnbase"),
        ("total_abs", "ln(1+Total imports)", "post_x_jpnbase"),
        ("jshare", "Japan share (level)", "post_x_jpnbase"),
    ]
    for base, label, treat in tests:
        coef, p, n = twfe(grp_val, base, treat)
        results[label] = {"coef": coef, "p": p, "n": n}
        print(f"  {label:>25}: {coef:+.5f} (p={p:.3f})")

    # TEST 2: Trade diversion — did reallocation go to Korea / other RCEP?
    print("\n=== TEST 2: source reallocation toward Korea / other RCEP? ===")
    for base, label in [("kor_share", "Korea share"), ("other_rcep_share", "Other-RCEP share")]:
        grp_val["o"] = grp_val[base].fillna(0)
        coef, p, n = twfe(grp_val, "o", "post_x_jpnbase")
        results[label] = {"coef": coef, "p": p, "n": n}
        print(f"  {label:>25}: ({coef:+.5f}) p={p:.3f}")

    # TEST 3: overall import-source diversification (supplier HHI / eff number)
    print("\n=== TEST 3: overall import-source diversification ===")
    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]
    sc = sc.merge(jpn_base, on="hs6", how="left")
    sc["jpn_base"] = sc["jpn_base"].fillna(0)
    sc["post"] = (sc["year"] >= 2022).astype(float)
    sc["post_x_jpnbase"] = sc["post"] * sc["jpn_base"]
    sc["entity"] = sc["hs6"]
    for out in ["supplier_hhi", "supplier_effective_number", "supplier_count_positive"]:
        coef, p, n = twfe(sc, out, "post_x_jpnbase")
        results[out] = {"coef": coef, "p": p, "n": n}
        print(f"  {out:>25}: {coef:+.5f} (p={p:.3f})")

    (AUDIT / "mechanism_tests.json").write_text(json.dumps(results, indent=2, default=float))
    print("\nSaved audit/机制检验_反直觉解释/mechanism_tests.json")


if __name__ == "__main__":
    main()
