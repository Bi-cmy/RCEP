#!/usr/bin/env python3
"""Estimate the frozen static DDD and its two few-country inference procedures."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from docx import Document
from pyhdfe import create
from scipy import stats


EXPERIMENT = Path(__file__).resolve().parents[1]
DATA = EXPERIMENT / "data"
TABLES = EXPERIMENT / "tables"
LOGS = EXPERIMENT / "logs"
STATUS_PATH = EXPERIMENT / "STATUS.json"
SEED = 20260723
B = 9_999


def write_docx(frame: pd.DataFrame, path: Path, title: str) -> None:
    document = Document()
    document.add_heading(title, level=1)
    table = document.add_table(rows=1, cols=len(frame.columns))
    for cell, column in zip(table.rows[0].cells, frame.columns, strict=True):
        cell.text = str(column)
    for row in frame.itertuples(index=False, name=None):
        cells = table.add_row().cells
        for cell, value in zip(cells, row, strict=True):
            if isinstance(value, float):
                cell.text = "" if np.isnan(value) else f"{value:.6f}"
            else:
                cell.text = str(value)
    document.save(path)


def export_table(frame: pd.DataFrame, stem: str, title: str) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    frame.to_excel(TABLES / f"{stem}.xlsx", index=False)
    frame.to_latex(
        TABLES / f"{stem}.tex",
        index=False,
        float_format="%.6f",
        caption=title,
        label=f"tab:{stem}",
    )
    write_docx(frame, TABLES / f"{stem}.docx", title)


def fwl_fit(
    work: pd.DataFrame,
    outcome: str,
    treatment: str,
    algorithm,
    clusters: np.ndarray,
) -> tuple[dict[str, float], np.ndarray, np.ndarray]:
    values = work[[outcome, treatment]].to_numpy(dtype=float)
    residualized = algorithm.residualize(values)
    y_tilde, x_tilde = residualized[:, 0], residualized[:, 1]
    fit = sm.OLS(y_tilde, x_tilde[:, None], hasconst=False).fit(
        cov_type="cluster",
        cov_kwds={"groups": clusters, "use_correction": True},
        use_t=True,
    )
    cluster_count = int(np.unique(clusters).size)
    critical = float(stats.t.ppf(0.975, df=cluster_count - 1))
    beta = float(fit.params[0])
    se = float(fit.bse[0])
    result = {
        "estimate": beta,
        "std_error": se,
        "t_stat": beta / se,
        "p_value_t20": float(fit.pvalues[0]),
        "ci_low": beta - critical * se,
        "ci_high": beta + critical * se,
    }
    return result, y_tilde, x_tilde


def unique_assignments(
    countries: list[str], observed: tuple[int, ...], draws: int
) -> list[tuple[int, ...]]:
    rng = np.random.default_rng(SEED)
    template = np.array([2022] * 12 + [2023] * 2 + [0] * 7, dtype=np.int16)
    assignments: set[tuple[int, ...]] = set()
    while len(assignments) < draws:
        candidate = tuple(int(value) for value in rng.permutation(template))
        if candidate != observed:
            assignments.add(candidate)
    return sorted(assignments)


def main() -> None:
    panel = pd.read_parquet(DATA / "firm_country_role_year.parquet")
    key = ["listed_ticker", "partner_country", "supplier_role", "year"]
    if panel.duplicated(key).any():
        raise ValueError("Firm-country-role-year panel has duplicate keys.")
    pretrend = json.loads((LOGS / "pretrend_gate.json").read_text(encoding="utf-8"))
    if not pretrend["gate_pass"]:
        raise RuntimeError("The frozen pretrend gate did not pass.")

    work = panel.sort_values(key).reset_index(drop=True)
    fixed_effects = work[
        ["firm_country_role_id", "firm_year_role_id", "country_year_id"]
    ].to_numpy(dtype=np.int64)
    algorithm = create(fixed_effects, drop_singletons=False)
    clusters = pd.Categorical(work["partner_country"]).codes
    specifications = [
        ("Preferred staged timing", "asinh_active_links", "triple_staged"),
        ("Uniform 2022 timing", "asinh_active_links", "triple_uniform"),
        ("Any active relationship", "any_active_link", "triple_staged"),
    ]
    result_rows = []
    transformed: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for name, outcome, treatment in specifications:
        estimate, y_tilde, x_tilde = fwl_fit(
            work, outcome, treatment, algorithm, clusters
        )
        result_rows.append(
            {
                "specification": name,
                "outcome": outcome,
                "timing": treatment,
                **estimate,
                "observations": int(len(work)),
                "clusters": int(work["partner_country"].nunique()),
                "fixed_effects": "firm-country-role; firm-year-role; country-year",
            }
        )
        transformed[name] = (y_tilde, x_tilde)

    main_result = result_rows[0]
    y_tilde, x_tilde = transformed["Preferred staged timing"]
    country_codes = np.unique(clusters)
    denominator = float(x_tilde @ x_tilde)
    cluster_xy = np.array(
        [float(x_tilde[clusters == code] @ y_tilde[clusters == code]) for code in country_codes]
    )
    cluster_xx = np.array(
        [float(x_tilde[clusters == code] @ x_tilde[clusters == code]) for code in country_codes]
    )
    rng = np.random.default_rng(SEED)
    weights = rng.choice(np.array([-1.0, 1.0]), size=(B, len(country_codes)))
    bootstrap_beta = (weights @ cluster_xy) / denominator
    bootstrap_scores = weights * cluster_xy - bootstrap_beta[:, None] * cluster_xx
    n = len(work)
    rank = int(algorithm.degrees + 1)
    cluster_count = len(country_codes)
    correction = (cluster_count / (cluster_count - 1)) * ((n - 1) / (n - rank))
    bootstrap_se = np.sqrt(
        correction * np.square(bootstrap_scores).sum(axis=1) / denominator**2
    )
    bootstrap_t = np.divide(
        bootstrap_beta,
        bootstrap_se,
        out=np.full(B, np.nan),
        where=bootstrap_se > 0,
    )
    observed_t = float(main_result["t_stat"])
    valid_bootstrap = np.isfinite(bootstrap_t)
    wild_p = float(
        (1 + np.sum(np.abs(bootstrap_t[valid_bootstrap]) >= abs(observed_t)))
        / (1 + valid_bootstrap.sum())
    )
    bootstrap_draws = pd.DataFrame(
        {
            "draw": np.arange(1, B + 1),
            "beta": bootstrap_beta,
            "std_error": bootstrap_se,
            "t_stat": bootstrap_t,
        }
    )
    bootstrap_draws.to_parquet(DATA / "wild_cluster_bootstrap_draws.parquet", index=False)
    bootstrap_draws.to_csv(DATA / "wild_cluster_bootstrap_draws.csv", index=False)

    countries = sorted(work["partner_country"].unique())
    observed_map = (
        work[["partner_country", "entry_policy_year"]]
        .drop_duplicates()
        .set_index("partner_country")["entry_policy_year"]
        .to_dict()
    )
    observed_assignment = tuple(
        0 if observed_map[country] == 9999 else int(observed_map[country])
        for country in countries
    )
    assignments = unique_assignments(countries, observed_assignment, B)

    cell = (
        work.groupby(["partner_country", "year", "supplier_role"], as_index=False)
        .agg(y_tilde_sum=("asinh_active_links", "size"))
    )
    # Use the fully residualized outcome collapsed to country-year-role cells.
    collapsed_y = (
        pd.DataFrame(
            {
                "partner_country": work["partner_country"].to_numpy(),
                "year": work["year"].to_numpy(),
                "supplier_role": work["supplier_role"].to_numpy(),
                "y_tilde": y_tilde,
            }
        )
        .groupby(["partner_country", "year", "supplier_role"], as_index=False)[
            "y_tilde"
        ]
        .sum()
        .sort_values(["partner_country", "year", "supplier_role"])
        .reset_index(drop=True)
    )
    cell = cell.sort_values(["partner_country", "year", "supplier_role"]).reset_index(drop=True)
    if not cell[["partner_country", "year", "supplier_role"]].equals(
        collapsed_y[["partner_country", "year", "supplier_role"]]
    ):
        raise ValueError("Collapsed outcome cells are misaligned.")
    cell_fe = pd.DataFrame(
        {
            "country_role": pd.factorize(
                pd.MultiIndex.from_frame(cell[["partner_country", "supplier_role"]]),
                sort=True,
            )[0],
            "year_role": pd.factorize(
                pd.MultiIndex.from_frame(cell[["year", "supplier_role"]]), sort=True
            )[0],
            "country_year": pd.factorize(
                pd.MultiIndex.from_frame(cell[["partner_country", "year"]]), sort=True
            )[0],
        }
    ).to_numpy(dtype=np.int64)
    cell_algorithm = create(cell_fe, drop_singletons=False)
    country_position = {country: index for index, country in enumerate(countries)}
    country_index = cell["partner_country"].map(country_position).to_numpy(dtype=int)
    years = cell["year"].to_numpy(dtype=int)
    supplier = cell["supplier_role"].to_numpy(dtype=float)
    treatment_matrix = np.empty((len(cell), B), dtype=np.float64)
    for start in range(0, B, 500):
        stop = min(start + 500, B)
        assignment_block = np.asarray(assignments[start:stop], dtype=np.int16)
        assigned_year = assignment_block[:, country_index].T
        treatment_matrix[:, start:stop] = supplier[:, None] * (
            (assigned_year > 0) & (years[:, None] >= assigned_year)
        )
    treatment_tilde = cell_algorithm.residualize(treatment_matrix)
    firms = int(work["listed_ticker"].nunique())
    permutation_numerator = collapsed_y["y_tilde"].to_numpy() @ treatment_tilde
    permutation_denominator = firms * np.square(treatment_tilde).sum(axis=0)
    permutation_beta = permutation_numerator / permutation_denominator

    observed_cell_treatment = supplier * work[
        ["partner_country", "year", "supplier_role", "treated_staged"]
    ].drop_duplicates().sort_values(
        ["partner_country", "year", "supplier_role"]
    )["treated_staged"].to_numpy(dtype=float)
    observed_cell_tilde = cell_algorithm.residualize(observed_cell_treatment[:, None])[:, 0]
    expanded_observed = (
        pd.DataFrame(
            {
                "partner_country": cell["partner_country"],
                "year": cell["year"],
                "supplier_role": cell["supplier_role"],
                "x_cell_tilde": observed_cell_tilde,
            }
        )
        .merge(work[key], on=["partner_country", "year", "supplier_role"], how="right")
        .sort_values(key)["x_cell_tilde"]
        .to_numpy()
    )
    residualization_max_difference = float(np.max(np.abs(expanded_observed - x_tilde)))
    if residualization_max_difference > 1e-8:
        raise ValueError("Collapsed and full residualization are not equivalent.")

    assignment_strings = [
        ";".join(f"{country}:{year}" for country, year in zip(countries, assignment, strict=True))
        for assignment in assignments
    ]
    permutation_draws = pd.DataFrame(
        {
            "draw": np.arange(1, B + 1),
            "beta": permutation_beta,
            "assignment": assignment_strings,
        }
    )
    permutation_draws.to_parquet(DATA / "country_label_randomization_draws.parquet", index=False)
    permutation_draws.to_csv(DATA / "country_label_randomization_draws.csv", index=False)
    randomization_p = float(
        (1 + np.sum(np.abs(permutation_beta) >= abs(main_result["estimate"])))
        / (B + 1)
    )

    main_result["wild_cluster_bootstrap_p"] = wild_p
    main_result["country_label_randomization_p"] = randomization_p
    results = pd.DataFrame(result_rows)
    results.loc[0, "wild_cluster_bootstrap_p"] = wild_p
    results.loc[0, "country_label_randomization_p"] = randomization_p
    export_table(results, "table3_static_ddd", "Static Supplier-Customer Triple Difference")

    diagnostics = {
        "experiment_id": "05_supplier_customer_asymmetry",
        "gate": "STATIC_EFFECT_AND_RANDOMIZATION",
        "preferred_result": main_result,
        "wild_cluster_bootstrap": {
            "draws": B,
            "seed": SEED,
            "weights": "Rademacher",
            "method": "restricted bootstrap-t on the FWL-transformed regression",
            "p_value": wild_p,
            "draw_file": "data/wild_cluster_bootstrap_draws.parquet",
        },
        "country_label_randomization": {
            "draws": B,
            "seed": SEED,
            "assignment_counts": {"2022": 12, "2023": 2, "control": 7},
            "two_sided_p_value": randomization_p,
            "draw_file": "data/country_label_randomization_draws.parquet",
            "collapsed_full_residualization_max_difference": residualization_max_difference,
        },
        "positive_evidence_randomization_gate": randomization_p < 0.05,
    }
    (LOGS / "static_inference.json").write_text(
        json.dumps(diagnostics, indent=2), encoding="utf-8"
    )
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    status["phase"] = "STATIC_EFFECT_AND_RANDOMIZATION_RUN"
    status["static_inference_run"] = True
    status["randomization_gate_pass"] = randomization_p < 0.05
    status["next_gate"] = (
        "SECONDARY_OUTCOMES_AND_INFLUENCE"
        if randomization_p < 0.05
        else "ARCHIVE_INCONCLUSIVE"
    )
    STATUS_PATH.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(diagnostics, indent=2))


if __name__ == "__main__":
    main()
