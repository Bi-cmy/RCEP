#!/usr/bin/env python3
"""Estimate policy-linked mechanism paths for the Chinese manuscript.

The FactSet panel has no firm-level customs transactions.  This script therefore
merges pre-specified partner-country/year indicators from the RCEP trade project
onto the relationship panel.  The indicators are used as mechanism-consistent
outcomes, not as observed preference claims or certificates of origin.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS


ROOT = Path(__file__).resolve().parents[1]
PAIR_PATH = ROOT / "data" / "derived" / "pair_year.parquet"
TRADE_PATH = (
    ROOT.parent / "REPC" / "08_rcep_analysis" / "01_data_build" / "processed_trade"
    / "china_import_source_hs12_model_panel_2015_2024.parquet"
)
RESULTS = ROOT / "results" / "tables"
LEGACY = ROOT / "legacy"
PAPER_TABLE = ROOT / "paper" / "paper_v2" / "tables" / "table2_mechanisms.tex"

BOOTSTRAP_REPS = 2000
BOOTSTRAP_SEED = 20260904

RCEP_ISO3 = {
    "AUS", "BRN", "KHM", "IDN", "JPN", "KOR", "LAO", "MYS",
    "MMR", "NZL", "PHL", "SGP", "THA", "VNM",
}


def alpha3_to_alpha2() -> dict[str, str]:
    """Use ISO data when available; retain a local fallback for the RCEP set."""
    fallback = {
        "AUS": "AU", "BRN": "BN", "KHM": "KH", "IDN": "ID", "JPN": "JP",
        "KOR": "KR", "LAO": "LA", "MYS": "MY", "MMR": "MM", "NZL": "NZ",
        "PHL": "PH", "SGP": "SG", "THA": "TH", "VNM": "VN",
    }
    try:
        import pycountry  # type: ignore

        return {
            country.alpha_3: country.alpha_2
            for country in pycountry.countries
            if getattr(country, "alpha_2", None) and getattr(country, "alpha_3", None)
        } | fallback
    except ImportError:
        return fallback


def build_partner_year_metrics() -> pd.DataFrame:
    trade = pd.read_parquet(TRADE_PATH)
    trade = trade.loc[trade["calendar_year"].between(2017, 2024)].copy()
    trade["value"] = trade["trade_value"].astype(float)
    trade["intermediate_value"] = trade["value"] * trade["bec5_intermediate_strict"]
    trade["positive_product"] = trade["value"].gt(0).astype("int8")
    trade["tariff_cut"] = np.where(
        trade["is_japan_source"],
        trade["japan_tariff_cut_pct"],
        trade["other_rcep_tariff_cut_pct"],
    )

    # Fixed 2017--2019 import weights avoid using post-treatment trade weights
    # to construct the tariff-relief mechanism indicator.
    baseline = (
        trade.loc[trade["calendar_year"].between(2017, 2019)]
        .groupby(["partner_iso3", "hs6"], as_index=False)["value"]
        .sum()
        .rename(columns={"value": "baseline_value"})
    )
    trade = trade.merge(baseline, on=["partner_iso3", "hs6"], how="left", validate="many_to_one")
    trade["weighted_cut"] = trade["baseline_value"] * trade["tariff_cut"].fillna(0.0)

    metrics = (
        trade.groupby(["partner_iso3", "calendar_year"], as_index=False)
        .agg(
            total_import=("value", "sum"),
            intermediate_import=("intermediate_value", "sum"),
            positive_products=("positive_product", "sum"),
            weighted_cut=("weighted_cut", "sum"),
            baseline_value=("baseline_value", "sum"),
        )
    )

    # Product-composition HHI is computed separately for each source country.
    source_product = (
        trade.groupby(["partner_iso3", "calendar_year", "hs6"], as_index=False)["value"]
        .sum()
    )
    source_product["source_total"] = source_product.groupby(
        ["partner_iso3", "calendar_year"]
    )["value"].transform("sum")
    source_product["product_share"] = np.where(
        source_product["source_total"].gt(0),
        source_product["value"] / source_product["source_total"],
        0.0,
    )
    hhi = (
        source_product.groupby(["partner_iso3", "calendar_year"])["product_share"]
        .apply(lambda x: float(np.square(x).sum()))
        .rename("product_hhi")
        .reset_index()
    )
    metrics = metrics.merge(hhi, on=["partner_iso3", "calendar_year"], validate="one_to_one")
    metrics["tariff_relief"] = np.where(
        metrics["baseline_value"].gt(0),
        metrics["weighted_cut"] / metrics["baseline_value"],
        np.nan,
    )
    metrics["intermediate_share"] = np.where(
        metrics["total_import"].gt(0),
        metrics["intermediate_import"] / metrics["total_import"],
        np.nan,
    )
    metrics["source_share"] = metrics["total_import"] / metrics.groupby(
        "calendar_year"
    )["total_import"].transform("sum")
    # A lower single-partner share is the source-diversification mechanism.
    metrics = metrics.rename(columns={"calendar_year": "year"})
    metrics["partner_country"] = metrics["partner_iso3"].map(alpha3_to_alpha2())
    return metrics[
        [
            "partner_country", "year", "tariff_relief", "intermediate_share",
            "source_share", "partner_iso3",
        ]
    ]


def indexed(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def clustered(frame: pd.DataFrame, mode: str = "pair") -> pd.DataFrame:
    if mode == "pair":
        values = frame.index.get_level_values("pair_id")
        return pd.DataFrame({"pair": values}, index=frame.index)
    if mode == "country":
        values = pd.Categorical(frame["partner_country"]).codes
        return pd.DataFrame({"country": values}, index=frame.index)
    raise ValueError(mode)


def _prepare_bootstrap_arrays(data: pd.DataFrame, variable: str) -> dict[str, object]:
    """Prepare sufficient statistics for a relationship-pair cluster bootstrap."""
    sample = data.dropna(subset=["active", "treated_uniform", variable]).copy()
    sample = sample.sort_values(["pair_id", "year"]).reset_index(drop=True)
    _, pair_idx = np.unique(sample["pair_id"].to_numpy(), return_inverse=True)
    _, year_idx = np.unique(sample["year"].to_numpy(), return_inverse=True)
    z = sample[["treated_uniform", variable, "active"]].astype(float).to_numpy()
    n_pairs = int(pair_idx.max() + 1)
    n_years = int(year_idx.max() + 1)
    pair_obs = np.bincount(pair_idx, minlength=n_pairs).astype(float)
    pair_sum = np.zeros((n_pairs, z.shape[1]), dtype=float)
    np.add.at(pair_sum, pair_idx, z)
    pair_mean = pair_sum / pair_obs[:, None]
    demeaned_pair = z - pair_mean[pair_idx]

    # One pair-year cell is normally present, but summing also handles any
    # repeated or irregular cells without changing the fixed-effects design.
    pair_year_residual_sum = np.zeros((n_pairs * n_years, z.shape[1]), dtype=float)
    flat_idx = pair_idx * n_years + year_idx
    np.add.at(pair_year_residual_sum, flat_idx, demeaned_pair)
    pair_year_residual_sum = pair_year_residual_sum.reshape(n_pairs, n_years, z.shape[1])
    incidence = np.zeros((n_pairs, n_years), dtype=float)
    np.add.at(incidence, (pair_idx, year_idx), 1.0)
    return {
        "z": z,
        "pair_idx": pair_idx,
        "year_idx": year_idx,
        "pair_obs": pair_obs,
        "pair_mean": pair_mean,
        "pair_year_residual_sum": pair_year_residual_sum,
        "incidence": incidence,
        "n_pairs": n_pairs,
        "n_years": n_years,
        "observations": int(len(sample)),
    }


def _weighted_two_way_residuals(prepared: dict[str, object], weights: np.ndarray) -> np.ndarray:
    """Residualize columns on pair and year fixed effects under pair weights."""
    incidence = prepared["incidence"]
    pair_obs = prepared["pair_obs"]
    pair_year_residual_sum = prepared["pair_year_residual_sum"]
    n_years = int(prepared["n_years"])
    year_weight = weights @ incidence
    if np.any(year_weight <= 0):
        raise np.linalg.LinAlgError("A bootstrap draw has an empty year cell")

    # Solve the two-way FE normal equations in the small year dimension.
    weighted_incidence = incidence * (weights / pair_obs)[:, None]
    q = incidence.T @ weighted_incidence
    q = q / year_weight[:, None]
    rhs = weights @ pair_year_residual_sum.reshape(len(weights), -1)
    rhs = rhs.reshape(n_years, -1) / year_weight[:, None]
    system = np.eye(n_years) - q
    # Year effects are identified only up to a constant; normalize the first
    # year effect to zero without changing the residualized variables.
    system[0, :] = 0.0
    system[0, 0] = 1.0
    rhs[0, :] = 0.0
    year_effect = np.linalg.solve(system, rhs)
    pair_year_mean = (incidence @ year_effect) / pair_obs[:, None]

    pair_idx = prepared["pair_idx"]
    year_idx = prepared["year_idx"]
    z = prepared["z"]
    pair_mean = prepared["pair_mean"]
    return z - pair_mean[pair_idx] + pair_year_mean[pair_idx] - year_effect[year_idx]


def _weighted_ols(y: np.ndarray, x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    sqrt_w = np.sqrt(weights)
    return np.linalg.lstsq(x * sqrt_w[:, None], y * sqrt_w, rcond=None)[0]


def bootstrap_indirect_effect(
    data: pd.DataFrame,
    variable: str,
    reps: int = BOOTSTRAP_REPS,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[pd.DataFrame, dict[str, float | int | str]]:
    """Resample relationship pairs and re-estimate a, b, and a*b each draw."""
    prepared = _prepare_bootstrap_arrays(data, variable)
    n_pairs = int(prepared["n_pairs"])
    n_obs = int(prepared["observations"])
    rng = np.random.default_rng(seed)
    draws = np.full((reps, 3), np.nan, dtype=float)
    failures = 0

    for iteration in range(reps):
        sampled_pairs = rng.integers(0, n_pairs, size=n_pairs)
        weights = np.bincount(sampled_pairs, minlength=n_pairs).astype(float)
        try:
            residuals = _weighted_two_way_residuals(prepared, weights)
            x = residuals[:, 0]
            m = residuals[:, 1]
            y = residuals[:, 2]
            row_weights = weights[prepared["pair_idx"]]
            a = float(_weighted_ols(m, x[:, None], row_weights)[0])
            b = float(_weighted_ols(y, np.column_stack([x, m]), row_weights)[1])
            draws[iteration] = (a, b, a * b)
        except (FloatingPointError, np.linalg.LinAlgError, ValueError):
            failures += 1

    valid = np.isfinite(draws[:, 2])
    if valid.sum() == 0:
        raise RuntimeError(f"All {reps} bootstrap draws failed for {variable}")
    ab = draws[valid, 2]
    ci90_low, ci90_high = np.percentile(ab, [5.0, 95.0])
    ci95_low, ci95_high = np.percentile(ab, [2.5, 97.5])
    ci99_low, ci99_high = np.percentile(ab, [0.5, 99.5])
    summary = {
        "bootstrap_reps": int(reps),
        "bootstrap_valid_reps": int(valid.sum()),
        "bootstrap_failures": int(failures),
        "bootstrap_failure_rate": float(failures / reps),
        "bootstrap_ci90_low": float(ci90_low),
        "bootstrap_ci90_high": float(ci90_high),
        "bootstrap_ci_low": float(ci95_low),
        "bootstrap_ci_high": float(ci95_high),
        "bootstrap_ci99_low": float(ci99_low),
        "bootstrap_ci99_high": float(ci99_high),
        "bootstrap_method": "percentile",
        "bootstrap_cluster_unit": "relationship pair",
        "bootstrap_observations": n_obs,
        "bootstrap_pairs": n_pairs,
    }
    draws_frame = pd.DataFrame(
        draws, columns=["a_boot", "b_boot", "ab_boot"]
    )
    draws_frame.insert(0, "replicate", np.arange(1, reps + 1))
    return draws_frame, summary


def fit_mechanism(
    data: pd.DataFrame,
    variable: str,
    label: str,
    cluster_mode: str = "pair",
) -> dict[str, float | int | str]:
    sample = indexed(data.dropna(subset=["active", "treated_uniform", variable]).copy())
    cluster = clustered(sample, cluster_mode)

    # Step 1: total treatment effect, retained for a common reference.
    total = PanelOLS(
        sample["active"].astype(float), sample[["treated_uniform"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster)
    # Step 2: treatment -> mechanism indicator.
    first = PanelOLS(
        sample[variable].astype(float), sample[["treated_uniform"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster)
    # Step 3: outcome equation with the mechanism indicator.
    second = PanelOLS(
        sample["active"].astype(float), sample[["treated_uniform", variable]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster)

    a = float(first.params["treated_uniform"])
    a_se = float(first.std_errors["treated_uniform"])
    b = float(second.params[variable])
    b_se = float(second.std_errors[variable])
    return {
        "mechanism": label,
        "variable": variable,
        "a_treatment_to_mechanism": a,
        "a_se": a_se,
        "a_p_value": float(first.pvalues["treated_uniform"]),
        "b_mechanism_to_active": b,
        "b_se": b_se,
        "b_p_value": float(second.pvalues[variable]),
        "total_effect_c": float(total.params["treated_uniform"]),
        "total_effect_se": float(total.std_errors["treated_uniform"]),
        "total_effect_p": float(total.pvalues["treated_uniform"]),
        "direct_effect_c_prime": float(second.params["treated_uniform"]),
        "direct_effect_se": float(second.std_errors["treated_uniform"]),
        "direct_effect_p": float(second.pvalues["treated_uniform"]),
        "indirect_effect_ab": a * b,
        "observations": int(second.nobs),
        "pairs": int(sample.index.get_level_values("pair_id").nunique()),
        "partner_countries": int(sample["partner_country"].nunique()),
        "inference": f"{cluster_mode}-clustered",
    }


def bootstrap_stars(row: pd.Series) -> str:
    """Assign stars from percentile bootstrap CIs, strongest level first."""
    ci_excludes_zero = lambda low, high: float(low) > 0.0 or float(high) < 0.0
    if ci_excludes_zero(row["bootstrap_ci99_low"], row["bootstrap_ci99_high"]):
        return "***"
    if ci_excludes_zero(row["bootstrap_ci_low"], row["bootstrap_ci_high"]):
        return "**"
    if ci_excludes_zero(row["bootstrap_ci90_low"], row["bootstrap_ci90_high"]):
        return "*"
    return ""


def write_latex(results: pd.DataFrame) -> None:
    """Write the English paper table with bootstrap inference for the indirect effect."""
    def f(value: float, digits: int = 4) -> str:
        return f"{float(value):.{digits}f}"

    def stars(value: float) -> str:
        value = float(value)
        if value < 0.01:
            return "***"
        if value < 0.05:
            return "**"
        if value < 0.10:
            return "*"
        return ""

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Policy-linked mechanism evidence}",
        r"\label{tab:mechanisms}",
        r"\small",
        r"\begin{minipage}{\textwidth}",
        r"\centering",
        r"\smallskip",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Mechanism measure & $a$ & $b$ & $c$ & $c'$ & \shortstack{Indirect\\effect ($ab$)} & \shortstack{Bootstrap\\95\% CI} \\",
        r"\midrule",
    ]
    for _, row in results.iterrows():
        lines.append(
            f"{row['mechanism_label']} & {f(row['a_treatment_to_mechanism'])}{stars(row['a_p_value'])} "
            f"& {f(row['b_mechanism_to_active'])}{stars(row['b_p_value'])} "
            f"& {f(row['total_effect_c'])}{stars(row['total_effect_p'])} "
            f"& {f(row['direct_effect_c_prime'])}{stars(row['direct_effect_p'])} "
            f"& {f(row['indirect_effect_ab'])}{bootstrap_stars(row)} "
            f"& [{f(row['bootstrap_ci_low'])}, {f(row['bootstrap_ci_high'])}] \\\\")
        lines.append(
            f" & ({f(row['a_se'])}) & ({f(row['b_se'])}) & ({f(row['total_effect_se'])}) "
            f"& ({f(row['direct_effect_se'])}) & & \\\\")
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\vspace{2pt}",
        r"\parbox[t]{\textwidth}{%",
        r"\footnotesize \textit{Notes}: Each row uses its mechanism-specific complete-case sample. The percentile interval for $ab$ is based on 2,000 relationship-pair bootstrap draws. All models include pair and year fixed effects; standard errors in parentheses are clustered by pair. *, **, and *** denote 10\%, 5\%, and 1\% significance, using the corresponding bootstrap intervals for $ab$. All mechanism measures vary at the partner-country--year level.}",
        r"\end{minipage}",
        r"\end{table}",
    ]
    content = "\n".join(lines)
    PAPER_TABLE.parent.mkdir(parents=True, exist_ok=True)
    PAPER_TABLE.write_text(content, encoding="utf-8")
    (LEGACY / "table5_mechanisms.tex").write_text(content, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(PAIR_PATH)
    metrics = build_partner_year_metrics()
    data = panel.merge(metrics, on=["partner_country", "year"], how="left", validate="many_to_one")
    candidates = [
        ("增量关税优惠幅度", "Incremental tariff relief", "tariff_relief"),
        ("中间品进口份额", "Intermediate-goods import share", "intermediate_share"),
        ("单一伙伴来源份额（来源集中度）", "Partner-country import share", "source_share"),
    ]
    rows = []
    bootstrap_draws = []
    for index, (label, english_label, variable) in enumerate(candidates):
        print(f"Estimating {english_label} ({BOOTSTRAP_REPS} relationship-pair bootstrap draws)...")
        row = fit_mechanism(data, variable, label)
        row["mechanism_label"] = english_label
        draws, bootstrap_summary = bootstrap_indirect_effect(
            data,
            variable,
            reps=BOOTSTRAP_REPS,
            seed=BOOTSTRAP_SEED + index,
        )
        draws.insert(0, "mechanism", label)
        draws.insert(1, "variable", variable)
        bootstrap_draws.append(draws)
        row.update(bootstrap_summary)
        rows.append(row)
        print(
            f"  valid={bootstrap_summary['bootstrap_valid_reps']}, "
            f"failures={bootstrap_summary['bootstrap_failures']}, "
            f"CI=[{bootstrap_summary['bootstrap_ci_low']:.6f}, "
            f"{bootstrap_summary['bootstrap_ci_high']:.6f}]"
        )

    result = pd.DataFrame(rows)
    result["consistency_difference"] = (
        result["total_effect_c"]
        - result["direct_effect_c_prime"]
        - result["indirect_effect_ab"]
    )
    result["indirect_effect_significant"] = (
        (result["bootstrap_ci_low"] > 0) | (result["bootstrap_ci_high"] < 0)
    )
    result["indirect_effect_stars"] = result.apply(bootstrap_stars, axis=1)
    result["direct_effect_significant_5pct"] = result["direct_effect_p"] < 0.05
    result["mechanism_interpretation"] = np.where(
        result["indirect_effect_significant"] & result["direct_effect_significant_5pct"],
        "significant indirect effect with a statistically significant direct effect",
        np.where(
            result["indirect_effect_significant"],
            "significant indirect effect with a statistically insignificant direct effect",
            "indirect effect not supported",
        ),
    )
    result.to_csv(RESULTS / "mechanism_analysis.csv", index=False, encoding="utf-8-sig")
    pd.concat(bootstrap_draws, ignore_index=True).to_csv(
        RESULTS / "mechanism_bootstrap_draws.csv", index=False, encoding="utf-8-sig"
    )
    write_latex(result)
    data[["partner_country", "year", "tariff_relief", "intermediate_share", "source_share"]].drop_duplicates().to_csv(
        RESULTS / "mechanism_partner_year_metrics.csv", index=False, encoding="utf-8-sig"
    )
    report = {
        "policy_basis": [
            "RCEP第2章的产品—成员梯度降税和有效优惠税率",
            "第3.4条区域累积对中间品原产价值的影响",
            "第3章原产地累积与第4章便利化降低跨成员采购摩擦，影响来源集中度",
        ],
        "mechanism_pass_rule": "The indirect effect is supported when its percentile 95% bootstrap confidence interval excludes zero; a and b are reported with pair-clustered standard errors.",
        "bootstrap": {
            "repetitions": BOOTSTRAP_REPS,
            "method": "percentile",
            "cluster_unit": "relationship pair",
            "seed": BOOTSTRAP_SEED,
        },
        "source_share_definition": "source_share is a partner country's share of China's total imports in a calendar year; a larger value indicates greater source concentration, while a lower value indicates diversification.",
        "mechanisms": result.to_dict(orient="records"),
        "data_warning": "All three indicators are partner-country/year aggregates merged to the relationship panel; they are mechanism-consistent proxies, not firm-level preference-utilization records.",
    }
    (RESULTS / "mechanism_analysis.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        result[
            [
                "mechanism", "a_treatment_to_mechanism", "a_p_value",
                "b_mechanism_to_active", "b_p_value", "indirect_effect_ab",
                "bootstrap_ci_low", "bootstrap_ci_high", "bootstrap_failures",
                "observations",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
