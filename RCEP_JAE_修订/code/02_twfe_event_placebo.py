#!/usr/bin/env python3
"""Estimate TWFE, event-study, placebo, robustness, and interaction models."""

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
MAIN_CLUSTER = "pair"
SUBREGIONS = {
    "ASEAN": {"ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"},
    "Japan_Korea": {"JP", "KR"},
    "Australia_NZ": {"AU", "NZ"},
}


plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 300,
})


def indexed(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def cluster_frame(frame: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "country":
        return pd.DataFrame({"country": pd.Categorical(frame["partner_country"]).codes}, index=frame.index)
    if mode == "pair":
        return pd.DataFrame({"pair": frame.index.get_level_values("pair_id")}, index=frame.index)
    if mode == "country_firm":
        return pd.DataFrame({
            "country": pd.Categorical(frame["partner_country"]).codes,
            "firm": pd.Categorical(frame["cn_id"]).codes,
        }, index=frame.index)
    raise ValueError(mode)


def fit(frame: pd.DataFrame, xvars: list[str], cluster: str = "country"):
    data = indexed(frame.dropna(subset=["active"] + xvars).copy())
    model = PanelOLS(
        data["active"].astype(float),
        data[xvars].astype(float),
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
        check_rank=True,
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


def save_descriptive(panel: pd.DataFrame) -> None:
    annual = panel.groupby(["year", "rcep"], as_index=False)["active"].sum()
    piv = annual.pivot(index="year", columns="rcep", values="active").fillna(0)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.plot(piv.index, piv.get(1, 0), marker="o", linewidth=1.4, color="#0072B2", label="RCEP partners")
    ax.plot(piv.index, piv.get(0, 0), marker="s", linewidth=1.2, linestyle="--", color="#666666", label="Other partners")
    ax.axvline(2021.5, color="#D55E00", linestyle="--", linewidth=1)
    ax.set_xlabel("Year")
    ax.set_ylabel("Active pair-role relationships")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES / f"descriptive_active_links.{ext}", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def event_study(panel: pd.DataFrame, cluster: str = MAIN_CLUSTER) -> tuple[pd.DataFrame, dict]:
    event_terms = []
    labels = {-5: "event_m5", -4: "event_m4", -3: "event_m3", -2: "event_m2", 0: "event_0", 1: "event_p1", 2: "event_p2"}
    work = panel.copy()
    for rel_time, name in labels.items():
        work[name] = (work["rcep"].eq(1) & work["year"].sub(2022).eq(rel_time)).astype("int8")
        event_terms.append(name)
    result, data = fit(work, event_terms, cluster=cluster)

    rows = []
    for rel_time, name in labels.items():
        rows.append({
            "event_time": rel_time,
            "term": name,
            "coefficient": float(result.params[name]),
            "std_error": float(result.std_errors[name]),
            "ci_low": float(result.params[name] - 1.96 * result.std_errors[name]),
            "ci_high": float(result.params[name] + 1.96 * result.std_errors[name]),
            "p_value": float(result.pvalues[name]),
        })
    rows.append({"event_time": -1, "term": "omitted", "coefficient": 0.0, "std_error": 0.0, "ci_low": 0.0, "ci_high": 0.0, "p_value": np.nan})
    out = pd.DataFrame(rows).sort_values("event_time")

    pre = ["event_m5", "event_m4", "event_m3", "event_m2"]
    restriction = np.zeros((len(pre), len(result.params)))
    for i, term in enumerate(pre):
        restriction[i, list(result.params.index).index(term)] = 1
    wald = result.wald_test(restriction)
    diagnostics = {
        "pretrend_wald_stat": float(np.asarray(wald.stat).squeeze()),
        "pretrend_df": int(np.asarray(wald.df).squeeze()),
        "pretrend_p_value": float(np.asarray(wald.pval).squeeze()),
        "omitted_period": -1,
        "cluster": cluster,
        "observations": int(result.nobs),
    }

    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    plot = out[out["event_time"].ne(-1)]
    ax.errorbar(
        plot["event_time"], plot["coefficient"],
        yerr=1.96 * plot["std_error"], fmt="o-", color="#0072B2",
        ecolor="#555555", elinewidth=1, capsize=3, markersize=4, linewidth=1,
    )
    ax.scatter([-1], [0], marker="o", facecolors="white", edgecolors="#0072B2", s=28, zorder=3)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(-0.5, color="#D55E00", linestyle="--", linewidth=1)
    ax.set_xticks(range(-5, 3))
    ax.set_xlabel("Years relative to RCEP entry into force")
    ax.set_ylabel("Estimated effect on active relationship")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES / f"event_study.{ext}", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return out, diagnostics


def two_way_beta(active: np.ndarray, group: np.ndarray, post: np.ndarray) -> float:
    treatment = group[:, None] * post[None, :]
    d_tilde = treatment - treatment.mean(1, keepdims=True) - treatment.mean(0, keepdims=True) + treatment.mean()
    y_tilde = active - active.mean(1, keepdims=True) - active.mean(0, keepdims=True) + active.mean()
    return float(np.sum(d_tilde * y_tilde) / np.sum(d_tilde * d_tilde))


def permutation_placebo(panel: pd.DataFrame, draws: int = 499, seed: int = 20260723) -> tuple[pd.DataFrame, float]:
    matrix = panel.pivot(index="pair_id", columns="year", values="active").sort_index()
    info = panel[["pair_id", "partner_country"]].drop_duplicates("pair_id").set_index("pair_id").loc[matrix.index]
    countries = np.array(sorted(info["partner_country"].unique()))
    pair_country = info["partner_country"].to_numpy()
    post = (matrix.columns.to_numpy() >= 2022).astype(float)
    active = matrix.to_numpy(dtype=float)
    real_group = np.isin(pair_country, list(RCEP)).astype(float)
    real_beta = two_way_beta(active, real_group, post)

    rng = np.random.default_rng(seed)
    values = []
    for draw in range(draws):
        fake = rng.choice(countries, size=len(RCEP), replace=False)
        group = np.isin(pair_country, fake).astype(float)
        values.append({"draw": draw + 1, "coefficient": two_way_beta(active, group, post)})
    out = pd.DataFrame(values)
    p_value = float((1 + (out["coefficient"].abs() >= abs(real_beta)).sum()) / (draws + 1))

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.hist(out["coefficient"], bins=28, color="#BDBDBD", edgecolor="white", linewidth=0.5)
    ax.axvline(real_beta, color="#D55E00", linestyle="--", linewidth=1.5, label=f"Observed = {real_beta:.3f}")
    ax.set_xlabel("Placebo treatment coefficient")
    ax.set_ylabel("Frequency")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#E0E0E0", linewidth=0.5)
    fig.tight_layout()
    for ext in ["pdf", "png"]:
        fig.savefig(FIGURES / f"placebo_country_permutation.{ext}", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return out, p_value


def marginal(result, base: str, interaction: str) -> tuple[float, float, float]:
    estimate = float(result.params[base] + result.params[interaction])
    cov = result.cov
    variance = float(cov.loc[base, base] + cov.loc[interaction, interaction] + 2 * cov.loc[base, interaction])
    se = np.sqrt(max(variance, 0))
    t = estimate / se if se else np.nan
    return estimate, se, t


def interaction_test(panel: pd.DataFrame, moderator: str, label: str, sample=None, cluster: str = MAIN_CLUSTER) -> dict:
    work = panel.copy() if sample is None else panel.loc[sample(panel)].copy()
    work = work.dropna(subset=[moderator])
    work[moderator] = work[moderator].astype(float)
    post_mod = f"post_x_{moderator}"
    triple = f"treat_x_{moderator}"
    work[post_mod] = work["post2022"] * work[moderator]
    work[triple] = work["treated_uniform"] * work[moderator]
    result, data = fit(work, ["treated_uniform", post_mod, triple], cluster=cluster)
    high, high_se, high_t = marginal(result, "treated_uniform", triple)
    return {
        "dimension": label,
        "moderator": moderator,
        "base_effect": float(result.params["treated_uniform"]),
        "base_se": float(result.std_errors["treated_uniform"]),
        "moderated_effect": high,
        "moderated_se": high_se,
        "moderated_t": high_t,
        "difference": float(result.params[triple]),
        "difference_se": float(result.std_errors[triple]),
        "difference_t": float(result.tstats[triple]),
        "difference_p": float(result.pvalues[triple]),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "countries": int(data["partner_country"].nunique()),
        "cluster": cluster,
    }


def subregion_test(panel: pd.DataFrame, cluster: str = MAIN_CLUSTER) -> tuple[pd.DataFrame, dict]:
    work = panel.copy()
    terms = []
    for label, countries in SUBREGIONS.items():
        term = f"treat_{label.lower()}"
        work[term] = (work["partner_country"].isin(countries) & work["post2022"].eq(1)).astype("int8")
        terms.append(term)
    result, data = fit(work, terms, cluster=cluster)
    rows = pd.DataFrame([{
        "subregion": label,
        "coefficient": float(result.params[term]),
        "std_error": float(result.std_errors[term]),
        "t_stat": float(result.tstats[term]),
        "p_value": float(result.pvalues[term]),
    } for label, term in zip(SUBREGIONS, terms)])
    restriction = np.zeros((2, len(result.params)))
    restriction[0, list(result.params.index).index(terms[0])] = 1
    restriction[0, list(result.params.index).index(terms[1])] = -1
    restriction[1, list(result.params.index).index(terms[0])] = 1
    restriction[1, list(result.params.index).index(terms[2])] = -1
    wald = result.wald_test(restriction)
    test = {
        "joint_equality_wald": float(np.asarray(wald.stat).squeeze()),
        "joint_equality_p": float(np.asarray(wald.pval).squeeze()),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
    }
    return rows, test


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(DATA / "pair_year.parquet")
    save_descriptive(panel)

    specifications = [
        ("Preferred: uniform 2022, pair clusters", panel, "treated_uniform", MAIN_CLUSTER),
        ("Country-specific entry timing, pair clusters", panel, "treated_staged", MAIN_CLUSTER),
        ("Country-cluster inference (sensitivity)", panel, "treated_uniform", "country"),
        ("Two-way country and Chinese-firm clusters", panel, "treated_uniform", "country_firm"),
        ("Exclude 2020-2021, pair clusters", panel[~panel["year"].isin([2020, 2021])], "treated_uniform", MAIN_CLUSTER),
        ("Window 2019-2024, pair clusters", panel[panel["year"].ge(2019)], "treated_uniform", MAIN_CLUSTER),
        ("Exclude US partners, pair clusters", panel[panel["partner_country"].ne("US")], "treated_uniform", MAIN_CLUSTER),
        ("RCEP versus Asian non-members, pair clusters", panel[panel["rcep"].eq(1) | panel["asia_control"].eq(1)], "treated_uniform", MAIN_CLUSTER),
        ("Exclude offshore financial centers, pair clusters", panel[panel["offshore"].eq(0)], "treated_uniform", MAIN_CLUSTER),
        ("Incumbent relationships active in 2021, pair clusters", panel[panel["active_2021"].eq(1)], "treated_uniform", MAIN_CLUSTER),
        ("Supplier links only, pair clusters", panel[panel["supplier_link"].eq(1)], "treated_uniform", MAIN_CLUSTER),
    ]
    robust_rows = []
    for name, frame, term, cluster in specifications:
        result, data = fit(frame, [term], cluster=cluster)
        robust_rows.append(result_row(name, result, term, data, cluster))
    pd.DataFrame(robust_rows).to_csv(TABLES / "robustness_specs.csv", index=False)

    event, event_diag = event_study(panel, cluster=MAIN_CLUSTER)
    event.to_csv(TABLES / "event_study.csv", index=False)

    fake_rows = []
    pre_policy = panel[panel["year"].le(2021)].copy()
    for fake_year in [2019, 2020, 2021]:
        term = f"fake_{fake_year}"
        pre_policy[term] = (pre_policy["rcep"].eq(1) & pre_policy["year"].ge(fake_year)).astype("int8")
        result, data = fit(pre_policy, [term], cluster=MAIN_CLUSTER)
        fake_rows.append(result_row(f"Fake policy year {fake_year}", result, term, data, "country"))
    pd.DataFrame(fake_rows).to_csv(TABLES / "placebo_timing.csv", index=False)

    permutations, permutation_p = permutation_placebo(panel)
    permutations.to_csv(TABLES / "placebo_country_permutations.csv", index=False)

    incumbent_pairs = panel["active_2021"].eq(1)
    age_cut = panel.loc[incumbent_pairs, ["pair_id", "age_2021"]].drop_duplicates()["age_2021"].median()
    panel["older_relation"] = (panel["age_2021"] >= age_cut).astype(float)
    interactions = [
        interaction_test(panel, "supplier_link", "Foreign supplier versus customer"),
        interaction_test(panel, "multi_rcep_2021", "Pre-policy regional sourcing breadth"),
        interaction_test(panel, "older_relation", "Pre-policy relationship tenure", sample=lambda x: x["active_2021"].eq(1)),
        interaction_test(panel, "large_firm", "Pre-policy firm size"),
    ]
    pd.DataFrame(interactions).to_csv(TABLES / "interaction_mechanisms_heterogeneity.csv", index=False)

    subregions, subregion_diag = subregion_test(panel)
    subregions.to_csv(TABLES / "heterogeneity_subregions.csv", index=False)
    diagnostics = {
        "event_study": event_diag,
        "country_permutation_p_value": permutation_p,
        "country_permutation_draws": int(len(permutations)),
        "subregion_equality_test": subregion_diag,
        "relationship_age_median_2021": float(age_cut),
    }
    (TABLES / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
    print(json.dumps(diagnostics, indent=2))
    print(pd.DataFrame(robust_rows)[["specification", "coefficient", "std_error", "p_value"]].to_string(index=False))
    print(pd.DataFrame(interactions)[["dimension", "base_effect", "moderated_effect", "difference", "difference_p"]].to_string(index=False))


if __name__ == "__main__":
    main()
