#!/usr/bin/env python3
"""
02 — Reproduce REPC's verified PPML result as a quality anchor.

Uses the same data + three-way FE (partner_hs6 + hs6_year + partner_year) +
partner_hs6 clustering + pyfixest fepois/feols. Goal: confirm this environment
reproduces REPC's PPML coefficient (0.0855, p=0.116) and OLS (-0.0024, p=0.903).
If reproduced, the pipeline and estimand are correct; any new topic uses the
same verified machinery rather than a home-grown approximation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyfixest as pf

ROOT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results")
OUT.mkdir(parents=True, exist_ok=True)
DATA_FILE = ROOT / "china_import_rcep_atlas_hs12_incremental_policy_2015_2024.csv"
POS_TOL = 1e-10


def prepare(data: pd.DataFrame) -> pd.DataFrame:
    required = {"partner_iso3", "hs6", "calendar_year", "trade_value",
                "ln_trade_value", "treatment_intensity", "incremental_tariff_cut_pct",
                "post", "strict_primary_usable"}
    work = data.copy()
    work["hs6"] = work["hs6"].astype("string").str.replace(r"\.0$", "", regex=True).str.zfill(6)
    work["calendar_year"] = pd.to_numeric(work["calendar_year"], errors="coerce")
    for c in ["trade_value", "ln_trade_value", "treatment_intensity",
              "incremental_tariff_cut_pct", "post"]:
        work[c] = pd.to_numeric(work[c], errors="coerce")
    key_valid = work[["partner_iso3", "hs6", "calendar_year"]].notna().all(axis=1)
    dup = work.duplicated(["partner_iso3", "hs6", "calendar_year"], keep=False) & key_valid
    strict = work["strict_primary_usable"].eq(1)
    finite = work[["trade_value", "ln_trade_value", "treatment_intensity"]].notna().all(axis=1)
    nneg_trade = work["trade_value"].ge(0)
    nneg_treat = work["treatment_intensity"].ge(-POS_TOL)
    post_valid = work["post"].isin([0, 1])
    inc_match = (work["incremental_tariff_cut_pct"].notna()
                 & work["treatment_intensity"].sub(work["incremental_tariff_cut_pct"]).abs().le(POS_TOL))
    expected = work["incremental_tariff_cut_pct"] * work["post"]
    exp_match = (post_valid & expected.notna()
                 & work["treatment_intensity"].sub(expected).abs().le(POS_TOL))
    cand = strict & key_valid & ~dup & finite & nneg_trade & nneg_treat & post_valid & exp_match
    frame = work.loc[cand].copy()
    frame["calendar_year"] = frame["calendar_year"].astype(int)
    frame["partner_iso3"] = frame["partner_iso3"].astype(str)
    year = frame["calendar_year"].astype(str)
    frame["partner_hs6"] = frame["partner_iso3"] + "_" + frame["hs6"]
    frame["hs6_year"] = frame["hs6"] + "_" + year
    frame["partner_year"] = frame["partner_iso3"] + "_" + year
    return frame.reset_index(drop=True)


def main():
    print(f"Data: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE, low_memory=False)
    print(f"  raw rows: {len(df)}")
    frame = prepare(df)
    print(f"  strict estimation rows: {len(frame)}")

    # Robustness: PPML might drop all-zero FE separated groups; run as-is.
    ppml = pf.fepois(
        "trade_value ~ treatment_intensity | partner_hs6 + hs6_year + partner_year",
        data=frame, vcov={"CRV1": "partner_hs6"},
        separation_check=["fe", "ir"], fixef_rm="none",
        iwls_tol=1e-8, iwls_maxiter=100, lean=False, copy_data=True,
    )
    ols = pf.feols(
        "ln_trade_value ~ treatment_intensity | partner_hs6 + hs6_year + partner_year",
        data=frame, vcov={"CRV1": "partner_hs6"}, fixef_rm="none",
        lean=True,
    )
    def tidy(m, model):
        t = m.tidy().loc["treatment_intensity"]
        return {"model": model, "coef": float(t["Estimate"]),
                "se": float(t["Std. Error"]), "p": float(t["Pr(>|t|)"]),
                "n": int(m._N)}
    rows = [tidy(ppml, "PPML"), tidy(ols, "OLS_strict")]

    # Also linear-support diagnostic on the strict frame (reproduce REPC)
    print("\nPPML result:", rows[0])
    print("OLS result:", rows[1])
    print("Reference (REPC): PPML 0.0855 (p=0.116), OLS_full -0.0024 (p=0.903)")

    (OUT / "02_reproduce_anchor.json").write_text(json.dumps(rows, indent=2, default=float))
    print("\nSaved 02_reproduce_anchor.json")


if __name__ == "__main__":
    main()
