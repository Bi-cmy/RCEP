#!/usr/bin/env python3
"""Cross-fitted doubly robust DID diagnostic at the pair-role level.

The estimator uses pre-treatment relationship histories and fixed pair
attributes to estimate the RCEP-group propensity and the untreated outcome
regression. Folds are defined by partner country to avoid country leakage.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"


def make_pair_data(panel: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    wide = panel.pivot(index="pair_id", columns="year", values="active")
    info = panel.drop_duplicates("pair_id").set_index("pair_id")
    pair = info[[
        "partner_country", "rcep", "supplier_link", "age_2021",
        "rcep_breadth_2021", "size_pre", "revenue_percent", "episode_count",
    ]].join(wide.add_prefix("active_"))
    pair["delta_active"] = pair[["active_2022", "active_2023", "active_2024"]].mean(axis=1) - pair[
        ["active_2017", "active_2018", "active_2019", "active_2020", "active_2021"]
    ].mean(axis=1)
    pair["pre_active_mean"] = pair[[f"active_{y}" for y in range(2017, 2022)]].mean(axis=1)
    pair["pre_active_slope"] = (
        pair["active_2021"] - pair["active_2017"]
    ) / 4.0
    pair["size_missing"] = pair["size_pre"].isna().astype(float)
    pair["size_pre"] = pair["size_pre"].fillna(pair["size_pre"].median())
    pair["revenue_observed"] = pair["revenue_percent"].notna().astype(float)
    pair["log_revenue_percent"] = np.log1p(pair["revenue_percent"].fillna(0).clip(lower=0))
    pair["log_episode_count"] = np.log1p(pair["episode_count"].clip(lower=0))
    features = [
        "supplier_link", "age_2021", "rcep_breadth_2021", "size_pre", "size_missing",
        "revenue_observed", "log_revenue_percent", "log_episode_count",
        "pre_active_mean", "pre_active_slope",
        "active_2017", "active_2018", "active_2019", "active_2020", "active_2021",
    ]
    return pair.reset_index(), features


def dr_att(y: np.ndarray, d: np.ndarray, propensity: np.ndarray, m0: np.ndarray, weights=None) -> float:
    weights = np.ones_like(y, dtype=float) if weights is None else np.asarray(weights, dtype=float)
    weights = weights / weights.mean()
    d_mean = np.average(d, weights=weights)
    w1 = d / d_mean
    raw0 = (1 - d) * propensity / (1 - propensity)
    w0 = raw0 / np.average(raw0, weights=weights)
    return float(np.average((w1 - w0) * (y - m0), weights=weights))


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(DATA / "pair_year.parquet")
    pair, features = make_pair_data(panel)
    x = pair[features].astype(float).to_numpy()
    d = pair["rcep"].astype(int).to_numpy()
    y = pair["delta_active"].astype(float).to_numpy()
    groups = pair["partner_country"].astype(str).to_numpy()

    propensity = np.full(len(pair), np.nan)
    m0 = np.full(len(pair), np.nan)
    folds = GroupKFold(n_splits=5)
    fold_rows = []
    for fold, (train, test) in enumerate(folds.split(x, d, groups), start=1):
        propensity_model = HistGradientBoostingClassifier(
            learning_rate=0.05, max_iter=160, max_depth=3, min_samples_leaf=80,
            l2_regularization=1.0, random_state=20260723 + fold,
        )
        outcome_model = HistGradientBoostingRegressor(
            learning_rate=0.05, max_iter=160, max_depth=3, min_samples_leaf=80,
            l2_regularization=1.0, random_state=20260723 + fold,
        )
        propensity_model.fit(x[train], d[train])
        controls = train[d[train] == 0]
        outcome_model.fit(x[controls], y[controls])
        propensity[test] = propensity_model.predict_proba(x[test])[:, 1]
        m0[test] = outcome_model.predict(x[test])
        fold_rows.append({
            "fold": fold,
            "test_rows": int(len(test)),
            "test_countries": int(pd.Series(groups[test]).nunique()),
            "treated_share": float(d[test].mean()),
        })

    propensity = np.clip(propensity, 0.01, 0.99)
    estimate = dr_att(y, d, propensity, m0)
    raw0 = (1 - d) * propensity / (1 - propensity)
    control_ess = float(raw0.sum() ** 2 / np.square(raw0).sum())

    rng = np.random.default_rng(20260723)
    countries = np.unique(groups)
    bootstrap = []
    for draw in range(999):
        sampled = rng.choice(countries, size=len(countries), replace=True)
        counts = pd.Series(sampled).value_counts()
        obs_weights = pd.Series(groups).map(counts).fillna(0).to_numpy(dtype=float)
        bootstrap.append(dr_att(y, d, propensity, m0, obs_weights))
    bootstrap = np.asarray(bootstrap)
    se = float(bootstrap.std(ddof=1))
    ci = np.quantile(bootstrap, [0.025, 0.975])
    p_value = float(2 * min(np.mean(bootstrap <= 0), np.mean(bootstrap >= 0)))

    diagnostics = {
        "estimator": "cross-fitted doubly robust panel DID ATT",
        "estimate": estimate,
        "cluster_bootstrap_se": se,
        "cluster_bootstrap_ci_low": float(ci[0]),
        "cluster_bootstrap_ci_high": float(ci[1]),
        "cluster_bootstrap_p_value": p_value,
        "bootstrap_draws": int(len(bootstrap)),
        "observations": int(len(pair)),
        "treated_pairs": int(d.sum()),
        "partner_countries": int(len(countries)),
        "propensity_min": float(propensity.min()),
        "propensity_p01": float(np.quantile(propensity, 0.01)),
        "propensity_median": float(np.median(propensity)),
        "propensity_p99": float(np.quantile(propensity, 0.99)),
        "propensity_max": float(propensity.max()),
        "control_effective_sample_size": control_ess,
        "features": features,
        "folding": "five folds grouped by partner country",
        "status": "diagnostic only because the main event-study/permutation gates did not pass",
    }
    pd.DataFrame(fold_rows).to_csv(TABLES / "dml_fold_diagnostics.csv", index=False)
    pd.DataFrame({"estimate": bootstrap}).to_csv(TABLES / "dml_cluster_bootstrap.csv", index=False)
    (TABLES / "dml_dr_did.json").write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
