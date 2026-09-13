#!/usr/bin/env python3
"""Expanded placebo battery for the RCEP pair-year DiD.

The headline specification is clustered by directed firm-partner relationship
(``pair_id``). Country-level assignment is retained in the data, while the
placebo battery reports country-label, pair-level, timing, mixed, and event-
study diagnostics with reproducible draws.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
RCEP = {"JP", "KR", "AU", "NZ", "ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"}
POLICY_DATE = pd.Timestamp("2022-01-01")
SEED = 20260904
DRAWS = 499

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9, "axes.labelsize": 10, "xtick.labelsize": 8,
    "ytick.labelsize": 8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.unicode_minus": False, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.dpi": 300,
})


def indexed(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def cluster_frame(data: pd.DataFrame, cluster: str) -> pd.DataFrame:
    if cluster == "pair":
        values = data.index.get_level_values("pair_id")
    elif cluster == "country":
        values = pd.Categorical(data["partner_country"]).codes
    else:
        raise ValueError(f"Unknown cluster: {cluster}")
    return pd.DataFrame({cluster: values}, index=data.index)


def fit_twfe(frame: pd.DataFrame, terms: list[str], cluster: str = "pair"):
    data = indexed(frame.dropna(subset=["active"] + terms).copy())
    model = PanelOLS(
        data["active"].astype(float), data[terms].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=True,
    )
    result = model.fit(cov_type="clustered", clusters=cluster_frame(data, cluster))
    return result, data


def result_row(name: str, result, term: str, data: pd.DataFrame, cluster: str) -> dict:
    return {
        "specification": name,
        "term": term,
        "coefficient": float(result.params[term]),
        "std_error": float(result.std_errors[term]),
        "t_stat": float(result.tstats[term]),
        "p_value": float(result.pvalues[term]),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "partner_countries": int(data["partner_country"].nunique()),
        "cluster": cluster,
        "pair_fe": True,
        "year_fe": True,
    }


def two_way_beta(active: np.ndarray, group: np.ndarray, post: np.ndarray) -> float:
    """Within-within coefficient for a balanced pair-by-year matrix."""
    group = np.asarray(group, dtype=float)
    post = np.asarray(post, dtype=float)
    treatment = group[:, None] * post[None, :]
    d_tilde = treatment - treatment.mean(1, keepdims=True) - treatment.mean(0, keepdims=True) + treatment.mean()
    y_tilde = active - active.mean(1, keepdims=True) - active.mean(0, keepdims=True) + active.mean()
    denominator = float(np.sum(d_tilde * d_tilde))
    if denominator <= 1e-12:
        return np.nan
    return float(np.sum(d_tilde * y_tilde) / denominator)


def rank_p(observed: float, distribution: np.ndarray) -> float:
    distribution = np.asarray(distribution, dtype=float)
    return float((1 + np.sum(np.abs(distribution) >= abs(observed))) / (len(distribution) + 1))


def save_figure(fig, stem: str) -> None:
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES / f"{stem}.{ext}", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def annual_post(years: np.ndarray, false_date: pd.Timestamp) -> np.ndarray:
    year_end = pd.to_datetime(years.astype(str) + "-12-31")
    return (year_end >= false_date).astype(float)


def false_date_from_lead(lead_years: float) -> tuple[pd.Timestamp, int]:
    # Use a calendar-year offset for the one-year lead.  Fractional leads are
    # day-based because the annual panel cannot distinguish their intra-year
    # timing.
    if np.isclose(lead_years, 1.0):
        false_date = POLICY_DATE - pd.DateOffset(years=1)
    else:
        false_date = POLICY_DATE - pd.to_timedelta(lead_years * 365.25, unit="D")
    return false_date, int(false_date.year)


def event_study_pretrend(panel: pd.DataFrame, cluster: str = "pair") -> tuple[pd.DataFrame, dict]:
    """Estimate event studies with multiple pre-treatment lead windows."""
    rows, details = [], {}
    for lead_window in [1, 2, 3, 4, 5]:
        rel_map = {k: f"event_{'m' if k < 0 else 'p'}{abs(k)}" for k in range(-lead_window, 3) if k != -1}
        work = panel.copy()
        for k, term in rel_map.items():
            work[term] = (work["rcep"].eq(1) & work["year"].sub(2022).eq(k)).astype("int8")
        terms = list(rel_map.values())
        result, data = fit_twfe(work, terms, cluster=cluster)
        pre_terms = [term for k, term in rel_map.items() if k < 0]
        restriction = np.zeros((len(pre_terms), len(result.params)))
        for i, term in enumerate(pre_terms):
            restriction[i, list(result.params.index).index(term)] = 1
        wald = result.wald_test(restriction) if pre_terms else None
        rows.append({
            "lead_window_years": lead_window,
            "pre_terms": len(pre_terms),
            "wald_stat": float(np.asarray(wald.stat).squeeze()) if wald is not None else np.nan,
            "wald_p_value": float(np.asarray(wald.pval).squeeze()) if wald is not None else np.nan,
            "cluster": cluster, "observations": int(result.nobs),
            "pairs": int(data.index.get_level_values("pair_id").nunique()),
        })
        details[str(lead_window)] = {
            "coefficient": {term: float(result.params[term]) for term in terms},
            "std_error": {term: float(result.std_errors[term]) for term in terms},
            "p_value": {term: float(result.pvalues[term]) for term in terms},
        }
    return pd.DataFrame(rows), details


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(DATA / "pair_year.parquet")
    matrix = panel.pivot(index="pair_id", columns="year", values="active").sort_index()
    info = panel[["pair_id", "partner_country"]].drop_duplicates("pair_id").set_index("pair_id").loc[matrix.index]
    countries = np.array(sorted(info["partner_country"].unique()))
    pair_country = info["partner_country"].to_numpy()
    years = matrix.columns.to_numpy()
    active = matrix.to_numpy(dtype=float)
    pre_mask = years <= 2021
    pre_years = years[pre_mask]
    active_pre = active[:, pre_mask]
    post_2022 = annual_post(years, POLICY_DATE)
    real_group = np.isin(pair_country, list(RCEP)).astype(float)
    real_beta = two_way_beta(active, real_group, post_2022)
    treated_pair_count = int(real_group.sum())
    print(f"REAL RCEP beta (pair/year FE; pair-cluster main): {real_beta:.5f}")
    print(f"Treated pair-role units: {treated_pair_count:,}; countries: {len(RCEP)}")

    rng = np.random.default_rng(SEED)
    summary: dict = {
        "seed": SEED, "draws_per_permutation": DRAWS, "main_cluster": "pair",
        "policy_date": str(POLICY_DATE.date()), "real_beta": real_beta,
        "treated_pair_units": treated_pair_count,
    }

    # A. Country-label spatial placebo with varied treatment-group sizes.
    spatial_rows, spatial_draw_rows = [], []
    for k in [5, 8, 10, 12, 14, 16, 18, 21, 25, 30, 40]:
        values = []
        for draw in range(DRAWS):
            fake = rng.choice(countries, size=k, replace=False)
            beta = two_way_beta(active, np.isin(pair_country, fake), post_2022)
            values.append(beta)
            spatial_draw_rows.append({"k_countries": k, "draw": draw + 1, "coefficient": beta})
        values = np.asarray(values)
        spatial_rows.append({
            "placebo_type": "country_label", "k_countries": k, "draws": DRAWS,
            "real_beta": real_beta, "dist_mean": float(values.mean()),
            "dist_sd": float(values.std()), "dist_min": float(values.min()),
            "dist_max": float(values.max()), "rank_p_vs_real": rank_p(real_beta, values),
            "two_sided_p_vs_zero": float(np.mean(np.abs(values) >= abs(real_beta))),
            "frac_positive": float(np.mean(values > 0)),
        })
    df_spatial = pd.DataFrame(spatial_rows)
    df_spatial.to_csv(TABLES / "placebo_spatial_varied_k.csv", index=False)
    pd.DataFrame(spatial_draw_rows).to_csv(TABLES / "placebo_spatial_draws.csv", index=False)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(df_spatial["k_countries"], df_spatial["rank_p_vs_real"], marker="o", color="#0072B2")
    ax.axhline(0.05, color="#D55E00", linestyle="--", linewidth=1)
    ax.set_xlabel("Number of placebo-treated countries (k)")
    ax.set_ylabel("Rank p-value of observed estimate")
    save_figure(fig, "placebo_spatial_k")
    # Match the manuscript's country-label histogram to the expanded k=14
    # draw set rather than leaving the older independent permutation figure.
    k14 = df_spatial.loc[df_spatial["k_countries"].eq(14)].iloc[0]
    k14_values = np.asarray([r["coefficient"] for r in spatial_draw_rows if r["k_countries"] == 14])
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.hist(k14_values, bins=28, color="#BDBDBD", edgecolor="white", linewidth=0.5)
    ax.axvline(real_beta, color="#D55E00", linestyle="--", linewidth=1.5,
               label=f"Observed = {real_beta:.3f}")
    ax.set_xlabel("Placebo treatment coefficient (k=14 countries)")
    ax.set_ylabel("Frequency")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#E0E0E0", linewidth=0.5)
    save_figure(fig, "placebo_country_permutation")
    summary["spatial_country"] = df_spatial.to_dict("records")

    # B. Exploratory pair-level spatial placebo; this does not preserve the
    # country-level assignment and is therefore not a causal randomization test.
    pair_rows, values = [], []
    for draw in range(DRAWS):
        selected = rng.choice(len(pair_country), size=treated_pair_count, replace=False)
        fake_group = np.zeros(len(pair_country), dtype=float)
        fake_group[selected] = 1.0
        beta = two_way_beta(active, fake_group, post_2022)
        values.append(beta)
        pair_rows.append({"draw": draw + 1, "treated_pair_units": treated_pair_count, "coefficient": beta})
    values = np.asarray(values)
    summary["spatial_pair_random"] = {
        "placebo_type": "pair_level_random", "draws": DRAWS, "real_beta": real_beta,
        "dist_mean": float(values.mean()), "dist_sd": float(values.std()),
        "rank_p_vs_real": rank_p(real_beta, values),
        "two_sided_p_vs_zero": float(np.mean(np.abs(values) >= abs(real_beta))),
    }
    pd.DataFrame(pair_rows).to_csv(TABLES / "placebo_pair_random.csv", index=False)

    # C. Fixed RCEP group, integer false policy years, using only pre-2022 data.
    temporal_rows = []
    pre_panel = panel[panel["year"].le(2021)].copy()
    for fake_year in [2018, 2019, 2020, 2021]:
        term = f"fake_{fake_year}"
        pre_panel[term] = (pre_panel["rcep"].eq(1) & pre_panel["year"].ge(fake_year)).astype("int8")
        result, data = fit_twfe(pre_panel, [term], cluster="pair")
        temporal_rows.append(result_row(f"False policy year {fake_year}", result, term, data, "pair"))
    pd.DataFrame(temporal_rows).to_csv(TABLES / "placebo_temporal_false_year.csv", index=False)
    summary["temporal_fixed_year"] = temporal_rows

    # D. Fixed leads. With annual year-end outcomes, fractional leads within
    # 2021 necessarily map to the same annual cutoff; this limitation is shown.
    lead_rows = []
    for lead in [1.0, 2 / 3, 0.5, 1 / 3]:
        false_date, annual_cutoff = false_date_from_lead(lead)
        beta = two_way_beta(active_pre, real_group, annual_post(pre_years, false_date))
        lead_rows.append({
            "lead_years": lead, "false_date": str(false_date.date()),
            "annual_cutoff_year": annual_cutoff, "coefficient": beta,
            "identifiable_at_annual_resolution": False if lead < 1 else True,
            "resolution_note": "Fractional leads within 2021 use the 2021 year-end observation.",
        })
    pd.DataFrame(lead_rows).to_csv(TABLES / "placebo_temporal_fixed_leads.csv", index=False)
    summary["temporal_fixed_leads"] = lead_rows

    # E. Random false policy dates, fixed RCEP group; 999 draws are retained.
    start_date, end_date = pd.Timestamp("2018-01-01"), pd.Timestamp("2021-12-31")
    day_span = int((end_date - start_date).days) + 1
    random_date_rows, random_betas = [], []
    for draw in range(999):
        false_date = start_date + pd.to_timedelta(int(rng.integers(0, day_span)), unit="D")
        beta = two_way_beta(active_pre, real_group, annual_post(pre_years, false_date))
        random_betas.append(beta)
        random_date_rows.append({"draw": draw + 1, "false_date": str(false_date.date()),
                                 "annual_cutoff_year": int(false_date.year), "coefficient": beta})
    random_betas = np.asarray(random_betas)
    pd.DataFrame(random_date_rows).to_csv(TABLES / "placebo_temporal_random_dates.csv", index=False)
    summary["temporal_random_dates"] = {
        "draws": len(random_betas), "dist_mean": float(random_betas.mean()),
        "dist_sd": float(random_betas.std()), "rank_p_vs_real": rank_p(real_beta, random_betas),
        "two_sided_p_vs_zero": float(np.mean(np.abs(random_betas) >= abs(real_beta))),
    }

    # F. Mixed country-group and false-date placebo.
    mixed_rows, mixed_draw_rows = [], []
    for k in [10, 14, 18, 21]:
        values = []
        for draw in range(DRAWS):
            fake = rng.choice(countries, size=k, replace=False)
            false_date = start_date + pd.to_timedelta(int(rng.integers(0, day_span)), unit="D")
            beta = two_way_beta(active_pre, np.isin(pair_country, fake), annual_post(pre_years, false_date))
            values.append(beta)
            mixed_draw_rows.append({"k_countries": k, "draw": draw + 1,
                                    "false_date": str(false_date.date()), "coefficient": beta})
        values = np.asarray(values)
        mixed_rows.append({
            "placebo_type": "country_and_date", "k_countries": k, "draws": DRAWS,
            "real_beta": real_beta, "dist_mean": float(values.mean()),
            "dist_sd": float(values.std()), "rank_p_vs_real": rank_p(real_beta, values),
            "two_sided_p_vs_zero": float(np.mean(np.abs(values) >= abs(real_beta))),
        })
    pd.DataFrame(mixed_rows).to_csv(TABLES / "placebo_mixed.csv", index=False)
    pd.DataFrame(mixed_draw_rows).to_csv(TABLES / "placebo_mixed_draws.csv", index=False)
    summary["mixed"] = mixed_rows

    # G. Event-study pre-trend tests with pair-clustered inference.
    pretrend, event_details = event_study_pretrend(panel, cluster="pair")
    pretrend.to_csv(TABLES / "placebo_event_study_lead_windows.csv", index=False)
    summary["event_study_lead_windows"] = pretrend.to_dict("records")
    summary["event_study_coefficients"] = event_details

    (TABLES / "placebo_battery_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # Keep the compact diagnostics artifact aligned with the expanded k=14
    # placebo used in the manuscript.
    diagnostics_path = TABLES / "diagnostics.json"
    if diagnostics_path.exists():
        diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))
        diagnostics["main_cluster"] = "pair"
        diagnostics["country_permutation_p_value"] = float(
            df_spatial.loc[df_spatial["k_countries"].eq(14), "rank_p_vs_real"].iloc[0]
        )
        diagnostics["country_permutation_draws"] = DRAWS
        diagnostics_path.write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    print("\n=== SUMMARY ===")
    print(df_spatial[["k_countries", "rank_p_vs_real", "dist_mean", "dist_sd"]].to_string(index=False))
    print("\nFixed-year timing placebos (pair-clustered):")
    print(pd.DataFrame(temporal_rows)[["specification", "coefficient", "std_error", "p_value"]].to_string(index=False))
    print("\nFixed leads:")
    print(pd.DataFrame(lead_rows)[["lead_years", "false_date", "annual_cutoff_year", "coefficient"]].to_string(index=False))
    print("\nEvent-study joint pre-trend p-values:")
    print(pretrend[["lead_window_years", "wald_p_value", "cluster"]].to_string(index=False))
    print(f"\nOutputs written to {TABLES} and {FIGURES}")


if __name__ == "__main__":
    main()
