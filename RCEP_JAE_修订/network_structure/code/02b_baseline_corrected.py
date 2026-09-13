#!/usr/bin/env python3
"""
02b — CORRECTED baseline design.

Fixes three problems in the naive continuous-exposure DID:
  (1) Baseline exposure missingness handled by ZERO-fill (firms with no pre-RCEP
      RCEP relationship are valid controls with exposure=0), not by dropping.
  (2) Uses a DISCRETE treatment: high-exposure firms (baseline RCEP_share above
      the pre-policy median) vs low-exposure firms, a cleaner 2x2 DID with the
      year FE absorbing the 'post' main effect.
  (3) Event-study uses smooth interactions (exposure × relative-year dummies),
      base period omitted = 2021.

Two-way fixed effects: firm FE + year FE. Clustered at firm level (treatment is
firm-level). All outcomes reported together; no cherry-picking.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

OUTCOMES = ["RCEP_share", "Regional_HHI", "Entropy", "N_countries", "N_RCEP_countries"]
REL = {-4: "m4", -3: "m3", -2: "m2", 0: "p0", 1: "p1", 2: "p2"}


def indexed(df):
    return df.sort_values(["cn_id", "year"]).set_index(["cn_id", "year"])


def prepare(df):
    """Zero-fill baseline exposure; define high/low discrete treatment."""
    df = df.copy()
    df["RCEP_Exp0"] = df["RCEP_Exposure_base"].fillna(0.0)          # zero-fill
    pre = df[df["year"].between(2017, 2021)]
    median = pre["RCEP_Exp0"].median()
    df["high_exp"] = (df["RCEP_Exp0"] > median).astype(float)
    df["post2022"] = (df["year"] >= 2022).astype(float)
    df["treat_x_post"] = df["high_exp"] * df["post2022"]
    return df, median


def fit(df, outcome, xvars, cluster="firm"):
    work = df.copy()
    work["y"] = work[outcome].astype(float)
    data = indexed(work.dropna(subset=["y"]).copy()).dropna()
    model = PanelOLS(
        data["y"].astype(float), data[xvars].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False,
    )
    cl = pd.DataFrame({"firm": data.index.get_level_values("cn_id").to_numpy()}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    return res, data


def main():
    df = pd.read_parquet(OUT / "firm_year_network.parquet")
    df, median = prepare(df)
    print(f"Median baseline exposure: {median:.4f}")

    # ---- Baseline discrete DID: y ~ high_exp × post2022, with main effects ----
    print("\n=== BASELINE DID (high vs low exposure, firm FE + year FE) ===")
    rows = []
    for outcome in OUTCOMES:
        xvars = ["treat_x_post", "high_exp", "post2022"]
        res, data = fit(df, outcome, xvars)
        rows.append({
            "outcome": outcome,
            "coef": float(res.params["treat_x_post"]),
            "se": float(res.std_errors["treat_x_post"]),
            "t": float(res.tstats["treat_x_post"]),
            "p": float(res.pvalues["treat_x_post"]),
            "n": int(res.nobs),
            "firms": int(data.index.get_level_values("cn_id").nunique()),
        })
        print(f"{outcome:>18}: coef={rows[-1]['coef']:+.5f} se={rows[-1]['se']:.5f} "
              f"p={rows[-1]['p']:.3f} N={rows[-1]['n']} firms={rows[-1]['firms']}")
    pd.DataFrame(rows).to_csv(TABLES / "baseline_did_v2.csv", index=False)

    # ---- Event study with smooth interactions ----
    print("\n=== EVENT STUDY (smooth exposure × relative-year, base=2021) ===")
    evt_rows = []
    for outcome in OUTCOMES:
        work = df.copy()
        work["y"] = work[outcome].astype(float)
        terms = []
        for rel, name in REL.items():
            work[name] = work["RCEP_Exp0"] * work["year"].sub(2022).eq(rel).astype(float)
            terms.append(name)
        xvars = terms + ["RCEP_Exp0"]
        res, data = fit(work, outcome, xvars)
        pre = [t for t in ["m4", "m3", "m2"] if t in res.params.index]
        restriction = np.zeros((len(pre), len(res.params)))
        for i, t in enumerate(pre):
            restriction[i, list(res.params.index).index(t)] = 1
        wald = res.wald_test(restriction)
        wald_p = float(np.asarray(wald.pval).squeeze())
        coefs = {t: (float(res.params[t]), float(res.pvalues[t])) for t in REL.values() if t in res.params.index}
        evt_rows.append({"outcome": outcome, "joint_pretrend_p": wald_p, "coefs": coefs})
        print(f"{outcome:>18}: joint pre-trend p={wald_p:.3f}")
    pd.DataFrame(evt_rows).to_csv(TABLES / "event_study_pretrend_v2.csv", index=False)

    # Summary of post-period smooth effects for the passing ones
    print("\n=== POST coefficients (smooth) for reading ===")
    for e in evt_rows:
        p0 = e["coefs"].get("p0")
        p1 = e["coefs"].get("p1")
        print(f"{e['outcome']:>18}: p0={p0[0] if p0 else None:+.4f}({p0[1] if p0 else None:.3f}) "
              f"p1={p1[0] if p1 else None:+.4f}({p1[1] if p1 else None:.3f})")

    print("\nSaved baseline_did_v2.csv, event_study_pretrend_v2.csv")


if __name__ == "__main__":
    main()
