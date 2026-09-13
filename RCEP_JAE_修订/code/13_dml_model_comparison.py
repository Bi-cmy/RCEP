#!/usr/bin/env python3
"""Compare principled DML nuisance-model choices before reporting one.

The estimand is the pair-level change in active status. Treatment is binary
RCEP membership; folds are grouped by partner country to prevent leakage.
"""

from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "pair_year.parquet"
OUT = ROOT / "results" / "tables" / "dml_model_comparison.csv"


def fit_dml(pair: pd.DataFrame, features: list[str], propensity_model_factory, seed: int = 20260723):
    x = pair[features].astype(float).to_numpy()
    d = pair["rcep"].astype(int).to_numpy()
    y = pair["delta_active"].astype(float).to_numpy()
    groups = pair["partner_country"].astype(str).to_numpy()
    m0 = np.full(len(pair), np.nan)
    p = np.full(len(pair), np.nan)
    for fold, (train, test) in enumerate(GroupKFold(n_splits=5).split(x, d, groups), start=1):
        outcome = HistGradientBoostingRegressor(
            learning_rate=0.05, max_iter=160, max_depth=3,
            min_samples_leaf=80, l2_regularization=1.0,
            random_state=seed + fold,
        )
        propensity = propensity_model_factory(seed + fold)
        outcome.fit(x[train], y[train])
        propensity.fit(x[train], d[train])
        m0[test] = outcome.predict(x[test])
        p[test] = propensity.predict_proba(x[test])[:, 1]
    p = np.clip(p, 0.01, 0.99)
    ry = y - m0
    rd = d - p
    theta = float(np.sum(ry * rd) / np.sum(rd * rd))

    rng = np.random.default_rng(seed)
    boot = {"pair": [], "country": []}
    pair_ids = pair["pair_id"].to_numpy()
    countries = np.unique(groups)
    for _ in range(999):
        sampled_pairs = rng.choice(np.unique(pair_ids), size=len(np.unique(pair_ids)), replace=True)
        pair_counts = pd.Series(sampled_pairs).value_counts()
        w_pair = pd.Series(pair_ids).map(pair_counts).fillna(0).to_numpy(float)
        sampled_countries = rng.choice(countries, size=len(countries), replace=True)
        country_counts = pd.Series(sampled_countries).value_counts()
        w_country = pd.Series(groups).map(country_counts).fillna(0).to_numpy(float)
        for key, weights in [("pair", w_pair), ("country", w_country)]:
            num = np.sum(weights * ry * rd)
            den = np.sum(weights * rd * rd)
            if den > 1e-12:
                boot[key].append(num / den)
    out = {}
    for key, values in boot.items():
        values = np.asarray(values)
        ci = np.quantile(values, [0.025, 0.975])
        out[f"{key}_se"] = float(values.std(ddof=1))
        out[f"{key}_ci_low"] = float(ci[0])
        out[f"{key}_ci_high"] = float(ci[1])
        out[f"{key}_p"] = float(2 * min(np.mean(values <= 0), np.mean(values >= 0)))
    return theta, out


def main() -> None:
    ns = runpy.run_path(str(ROOT / "code" / "06_dml_authentic.py"))
    panel = pd.read_parquet(DATA)
    pair, features = ns["make_pair_data"](panel)
    factories = {
        "Logit propensity + HGB outcome": lambda seed: make_pipeline(
            StandardScaler(), LogisticRegression(C=1.0, max_iter=1000, random_state=seed)
        ),
        "HGB classifier propensity + HGB outcome": lambda seed: HistGradientBoostingClassifier(
            learning_rate=0.05, max_iter=160, max_depth=3, min_samples_leaf=80,
            l2_regularization=1.0, random_state=seed,
        ),
        "Random forest propensity + HGB outcome": lambda seed: RandomForestClassifier(
            n_estimators=300, max_depth=8, min_samples_leaf=40, max_features="sqrt",
            n_jobs=-1, random_state=seed,
        ),
    }
    rows = []
    for name, factory in factories.items():
        theta, stats = fit_dml(pair, features, factory)
        rows.append({"model": name, "theta": theta, **stats})
    result = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
