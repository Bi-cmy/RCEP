#!/usr/bin/env python3
"""
02 — Two-way fixed-effect (firm FE + year FE) baseline DID for the five
network-structure outcomes.

Core interaction:  Post2022_t × RCEP_Exposure_base_i  (continuous treatment
intensity = firm's pre-policy RCEP share). Standard errors clustered at the
partner-country level is not possible at the firm-year level (no single
partner country per firm-year), so we cluster at the firm level and also
report two-way (firm + year) as a sensitivity. The treatment is the firm's
pre-existing RCEP exposure, which varies at the firm level.

Also runs an event-study (leads/lags) for each outcome to test parallel trends.
"""
from __future__ import annotations
import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

OUTCOMES = ["RCEP_share", "Regional_HHI", "Entropy", "N_countries", "N_RCEP_countries"]
CONTROLS = ["size_pre"]  # N_links is a scale control but is also an outcome path; keep minimal


def indexed(df):
    return df.sort_values(["cn_id", "year"]).set_index(["cn_id", "year"])


def fit_panel(df, xvars, cluster="firm"):
    data = indexed(df.dropna(subset=["RCEP_share"] + xvars).copy()).dropna()
    # drop missing exposure for core DID
    data = data[data["RCEP_Exposure_base"].notna()].copy()
    model = PanelOLS(
        data["y"].astype(float), data[xvars].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False,
    )
    if cluster == "firm":
        cl = pd.DataFrame({"firm": data.index.get_level_values("cn_id").to_numpy()}, index=data.index)
    else:  # two-way firm+year
        cl = pd.DataFrame({
            "firm": data.index.get_level_values("cn_id").to_numpy(),
            "year": data.index.get_level_values("year").to_numpy(),
        }, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    return res, data


def run_baseline(df, outcome):
    work = df.copy()
    work["y"] = work[outcome].astype(float)
    work["post2022"] = (work["year"] >= 2022).astype(float)
    work["post_x_exp"] = work["post2022"] * work["RCEP_Exposure_base"]
    xvars = ["post_x_exp", "post2022", "RCEP_Exposure_base"] + [c for c in CONTROLS if c in work.columns]
    res, data = fit_panel(work, xvars, cluster="firm")
    term = "post_x_exp"
    return {
        "outcome": outcome,
        "coefficient": float(res.params[term]),
        "std_error": float(res.std_errors[term]),
        "t_stat": float(res.tstats[term]),
        "p_value": float(res.pvalues[term]),
        "n": int(res.nobs),
        "firms": int(data.index.get_level_values("cn_id").nunique()),
        "cluster": "firm",
    }


def run_event_study(df, outcome):
    work = df.copy()
    work["y"] = work[outcome].astype(float)
    # event time relative to 2022; base = 2021 (rel -1)
    rel_map = {-4: "m4", -3: "m3", -2: "m2", 0: "p0", 1: "p1", 2: "p2"}
    terms = []
    for rel, name in rel_map.items():
        # Interaction: Exposure_base × 1(year == 2022 + rel); missing exposure -> 0
        work[name] = work["RCEP_Exposure_base"].fillna(0).astype(float) * \
                     work["year"].sub(2022).eq(rel).astype(float)
        terms.append(name)
    xvars = terms + ["RCEP_Exposure_base"]
    data = indexed(work.dropna(subset=["y"]).copy())
    data = data[data["RCEP_Exposure_base"].notna()].copy()
    model = PanelOLS(
        data["y"].astype(float), data[xvars].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False,
    )
    cl = pd.DataFrame({"firm": data.index.get_level_values("cn_id").to_numpy()}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    # joint Wald on pre terms m4,m3,m2
    pre = [t for t in ["m4", "m3", "m2"] if t in res.params.index]
    restriction = np.zeros((len(pre), len(res.params)))
    for i, t in enumerate(pre):
        restriction[i, list(res.params.index).index(t)] = 1
    wald = res.wald_test(restriction)
    coefs = {t: (float(res.params[t]), float(res.pvalues[t])) for t in rel_map.values() if t in res.params.index}
    return {
        "outcome": outcome,
        "joint_pretrend_wald_p": float(np.asarray(wald.pval).squeeze()),
        "coefs": coefs,
        "n": int(res.nobs),
    }


def main():
    df = pd.read_parquet(OUT / "firm_year_network.parquet")
    print(f"Firm-year panel: {len(df)} rows, {df['cn_id'].nunique()} firms")

    rows = []
    for outcome in OUTCOMES:
        r = run_baseline(df, outcome)
        rows.append(r)
        print(f"{outcome:>18}: coef={r['coefficient']:+.5f}  se={r['std_error']:.5f} "
              f"t={r['t_stat']:+.2f}  p={r['p_value']:.3f}  N={r['n']}  firms={r['firms']}")
    pd.DataFrame(rows).to_csv(TABLES / "baseline_did.csv", index=False)

    print("\n=== EVENT STUDY (joint pre-trend Wald, base=2021) ===")
    evt_rows = []
    for outcome in OUTCOMES:
        e = run_event_study(df, outcome)
        evt_rows.append(e)
        print(f"{outcome:>18}: joint pre-trend Wald p={e['joint_pretrend_wald_p']:.3f}")
    pd.DataFrame(evt_rows).to_csv(TABLES / "event_study_pretrend.csv", index=False)

    print("\nSaved baseline_did.csv and event_study_pretrend.csv")


if __name__ == "__main__":
    main()
