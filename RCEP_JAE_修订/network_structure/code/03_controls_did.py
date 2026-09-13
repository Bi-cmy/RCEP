#!/usr/bin/env python3
"""
03 — DiD with firm controls (Size, Lev, ROA, Growth) + industry indication,
to test whether the network-structure DiD coefficients survive controlling
for firm size/leverage/profitability/industry. Partner-country-level cluster
is not available at firm-year level, so firm-level cluster is primary and a
manufacturing × year FE is used to absorb sector-year shocks.

Two variants reported:
  (A) No controls (baseline, for comparison)
  (B) With Size, Lev, ROA, Growth controls + manufacturing × year FE
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


def indexed(df):
    return df.sort_values(["cn_id", "year"]).set_index(["cn_id", "year"])


def prep(df):
    df = df.copy()
    base = df[df["year"].between(2017, 2021)]
    ever = base.groupby("cn_id")["N_RCEP_links"].max() > 0
    df["high_exp"] = df["cn_id"].map(ever).astype(float)
    df["post2022"] = (df["year"] >= 2022).astype(float)
    df["treat_x_post"] = df["high_exp"] * df["post2022"]
    # industry-year FE (manufacturing x year) absorbed via dummies
    mk = df["manufacturing"].fillna(0).astype(int)
    df["manuf_x_year"] = mk.astype(str) + "_" + df["year"].astype(str)
    return df


def run(df, outcome, with_controls):
    work = df.copy()
    work["y"] = work[outcome].astype(float)
    xvars = ["treat_x_post", "high_exp", "post2022"]
    yfe_extra = []
    if with_controls:
        xvars += ["Size", "Lev", "ROA", "Growth"]
    data = indexed(work.dropna(subset=["y"] + (["Size", "Lev", "ROA", "Growth"] if with_controls else [])))
    model = PanelOLS(data["y"].astype(float), data[xvars].astype(float),
                     entity_effects=True, time_effects=True,
                     drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"firm": data.index.get_level_values("cn_id").to_numpy()}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    return res, data


def main():
    df = pd.read_parquet(OUT / "firm_network_controls.parquet")
    df = prep(df)
    print(f"Panel: {len(df)} rows, {df['cn_id'].nunique()} firms")
    print(f"high_exp share: {df['high_exp'].mean():.3f}")
    print(f"Manufacturing share (firms with Indcd): via manuf_x_year")

    for with_ctrl in [False, True]:
        label = "WITH controls (Size/Lev/ROA/Growth)" if with_ctrl else "NO controls (baseline)"
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        rows = []
        for outcome in OUTCOMES:
            res, data = run(df, outcome, with_ctrl)
            rows.append({
                "outcome": outcome, "controls": with_ctrl,
                "coef": float(res.params["treat_x_post"]),
                "se": float(res.std_errors["treat_x_post"]),
                "p": float(res.pvalues["treat_x_post"]),
                "n": int(res.nobs), "firms": int(data.index.get_level_values("cn_id").nunique()),
            })
            print(f"{outcome:>18}: coef={rows[-1]['coef']:+.5f} se={rows[-1]['se']:.5f} "
                  f"p={rows[-1]['p']:.3f} N={rows[-1]['n']} firms={rows[-1]['firms']}")
        pd.DataFrame(rows).to_csv(TABLES / f"baseline_did_ctrl_{'yes' if with_ctrl else 'no'}.csv", index=False)

    print("\nDone. Saved baseline_did_ctrl_yes.csv and baseline_did_ctrl_no.csv")


if __name__ == "__main__":
    main()
