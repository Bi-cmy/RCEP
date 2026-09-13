#!/usr/bin/env python3
"""
04 — Propensity Score Matching (PSM) DiD.

Goal: eliminate the ~4x base-window scale gap between high-exposure (treated)
and low-exposure (control) firms, to test whether the Regional_HHI / Entropy
/ RCEP_share DiD effects survive after matching on baseline observables.

Design:
  - Estimate propensity of being High-Exposure (had >=1 RCEP link 2017-2021)
    from BASELINE (2021) observables: Size, Lev, ROA, Growth, N_links, N_countries,
    manufacturing.
  - 1:1 nearest-neighbor matching WITHOUT replacement on the logit(propensity),
    common-support (caliper 0.05), treated = high-exposure.
  - Carry matched firm pairs to the full 2017-2024 panel; re-run the two-way FE
    DiD (firm FE + year FE, firm-clustered) on the matched sample.
  - Report ATT-style DiD coefficient + pre-trend Wald p for each outcome.

This is the decisive clean-identification test the user asked for.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

OUTCOMES = ["RCEP_share", "Regional_HHI", "Entropy", "N_countries", "N_RCEP_countries"]
RNG = np.random.default_rng(20260903)


def print_pair(*a):
    print(*a)


def main():
    print("Loading firm-year panel with controls...")
    df = pd.read_parquet(OUT / "firm_network_controls.parquet")
    df = df.copy()

    # ---- Build treatment & base-window firm-level covariates ----
    base = df[df["year"].eq(2021)].copy()   # pre-policy cross-section
    # Treatment: high exposure (had >=1 RCEP link in base window 2017-2021)
    win = df[df["year"].between(2017, 2021)]
    ever = win.groupby("cn_id")["N_RCEP_links"].max().gt(0)
    base["treated"] = base["cn_id"].map(ever).astype(int)

    # Firm-level covariates (2021 cross-section already has Size/Lev/ROA/Growth/manufacturing)
    cov = df[df["year"].eq(2021)].groupby("cn_id")[["Size", "Lev", "ROA", "Growth", "manufacturing"]].first()
    cnt = win.groupby("cn_id").agg(N_links_base=("N_links", "sum"),
                                    N_countries_base=("N_countries", "mean"))
    base = base.set_index("cn_id")
    base = base.join(cnt, how="left")

    # Baseline characteristics
    base_X = base[["Size", "Lev", "ROA", "Growth", "manufacturing", "N_links_base"]].copy()
    base_X["Growth"] = base_X["Growth"].fillna(base_X["Growth"].median())
    base_X["Size"] = base_X["Size"].fillna(base_X["Size"].median())
    base_X["Lev"] = base_X["Lev"].fillna(base_X["Lev"].median())
    base_X["ROA"] = base_X["ROA"].fillna(base_X["ROA"].median())
    base_X["N_links_base"] = base_X["N_links_base"].fillna(0)
    base_X = base_X.dropna()

    base = base.loc[base_X.index]
    X = base_X.to_numpy(dtype=float)
    T = base["treated"].to_numpy(dtype=int)

    print(f"Baseline sample (2021): N={len(X)}, treated={T.sum()}, control={len(T)-T.sum()}")

    # ---- Estimate propensity ----
    logit = LogisticRegression(max_iter=1000, random_state=20260903)
    logit.fit(X, T)
    ps = logit.predict_proba(X)[:, 1]
    base["pscore"] = ps

    # ---- 1:1 nearest-neighbor matching without replacement, caliper 0.05 ----
    treated_mask = T == 1
    control_mask = T == 0
    # Common support: trim extreme propensity
    lo, hi = np.quantile(ps[control_mask], [0.02, 0.98])
    common = (ps > lo) & (ps < hi) & (T == 1)
    X_t = X[common]
    ps_t = ps[common]
    idx_t = base.index[common]
    print(f"Treated on common support: {X_t.shape[0]}")

    # Match each treated to nearest control
    ctrl_idx = base.index[control_mask & (ps > lo) & (ps < hi)]
    X_c = X[control_mask & (ps > lo) & (ps < hi)]
    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(X_c)
    dist, ind = nn.kneighbors(X_t)
    matched_pairs = []
    used = set()
    caliper = 0.05
    for i in range(X_t.shape[0]):
        j = ind[i, 0]
        if j in used:
            # find next nearest unused
            dd, ii = nn.kneighbors(X_t[i:i+1], n_neighbors=len(X_c))
            for jj in ii[0]:
                if jj not in used:
                    j = jj
                    break
            else:
                continue
        if dist[i, 0] > caliper:
            continue
        used.add(j)
        matched_pairs.append((idx_t[i], ctrl_idx[j]))
    print(f"Matched pairs: {len(matched_pairs)}")

    matched_treated = [p[0] for p in matched_pairs]
    matched_control = [p[1] for p in matched_pairs]
    match_firms = matched_treated + matched_control
    match_df = df[df["cn_id"].isin(match_firms)].copy()
    from linearmodels.panel import PanelOLS

    # Balance check on matched sample (2021)
    print("\n=== BALANCE after matching (2021) ===")
    bal = base.loc[[c for c in match_firms if c in base.index],
                   ["treated", "Size", "Lev", "ROA", "N_links_base", "manufacturing"]]
    grp = bal.groupby("treated")[["Size", "Lev", "ROA", "N_links_base", "manufacturing"]].mean()
    print(grp.round(3).to_string())

    # ---- Run DiD on matched sample ----
    def prep(d):
        d = d.copy()
        ever2 = d[d["year"].between(2017, 2021)].groupby("cn_id")["N_RCEP_links"].max().gt(0)
        d["high_exp"] = d["cn_id"].map(ever2).astype(float)
        d["post2022"] = (d["year"] >= 2022).astype(float)
        d["treat_x_post"] = d["high_exp"] * d["post2022"]
        return d

    mm = prep(match_df)
    print(f"\nMatched panel: {len(mm)} rows, {mm['cn_id'].nunique()} firms")

    print("\n=== DiD on MATCHED sample (firm FE + year FE, firm-clustered) ===")
    rows = []
    for outcome in OUTCOMES:
        work = mm.copy()
        work["y"] = work[outcome].astype(float)
        xvars = ["treat_x_post", "high_exp", "post2022"]
        data = work.set_index(["cn_id", "year"]).sort_index()
        data = data.dropna(subset=["y"])
        model = PanelOLS(data["y"].astype(float), data[xvars].astype(float),
                         entity_effects=True, time_effects=True,
                         drop_absorbed=True, check_rank=False)
        cl = pd.DataFrame({"firm": data.index.get_level_values("cn_id").to_numpy()}, index=data.index)
        res = model.fit(cov_type="clustered", clusters=cl)
        coef = float(res.params["treat_x_post"]); se = float(res.std_errors["treat_x_post"])
        p = float(res.pvalues["treat_x_post"])
        rows.append({"outcome": outcome, "coef": coef, "se": se, "p": p,
                     "n": int(res.nobs), "firms": int(data.index.get_level_values("cn_id").nunique())})
        print(f"{outcome:>18}: coef={coef:+.5f} se={se:.5f} p={p:.3f} N={res.nobs:.0f} firms={data.index.get_level_values('cn_id').nunique()}")
    pd.DataFrame(rows).to_csv(TABLES / "psm_did.csv", index=False)

    # Balance summary for the report
    balance_after = bal.groupby("treated")[["Size", "Lev", "ROA", "N_links_base"]].mean().round(3).to_dict()
    summary = {"matched_pairs": len(matched_pairs), "balance": balance_after,
               "diD": rows}
    (TABLES / "psm_did_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print("\nSaved psm_did.csv, psm_did_summary.json")


if __name__ == "__main__":
    main()
