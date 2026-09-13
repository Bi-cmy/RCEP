#!/usr/bin/env python3
"""Convert machine-readable estimates into LaTeX tables."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "results" / "tables"
OUT = ROOT / "paper" / "tables"


def esc(text: str) -> str:
    return str(text).replace("&", r"\&").replace("_", r"\_")


def fnum(value: float, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    robust = pd.read_csv(SRC / "robustness_specs.csv")
    lines = [
        r"\begin{tabular}{lrrrr}", r"\toprule",
        r"Specification & Estimate & S.E. & $p$-value & Observations \\", r"\midrule",
    ]
    for _, r in robust.iterrows():
        lines.append(
            f"{esc(r['specification'])} & {fnum(r['coefficient'])} & {fnum(r['std_error'])} & "
            f"{fnum(r['p_value'])} & {int(r['observations']):,} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "robustness.tex").write_text("\n".join(lines), encoding="utf-8")

    interactions = pd.read_csv(SRC / "interaction_mechanisms_heterogeneity.csv")
    lines = [
        r"\begin{tabular}{lrrrrr}", r"\toprule",
        r"Moderator & Base effect & Moderated effect & Difference & S.E. & $p$-value \\", r"\midrule",
    ]
    for _, r in interactions.iterrows():
        lines.append(
            f"{esc(r['dimension'])} & {fnum(r['base_effect'])} & {fnum(r['moderated_effect'])} & "
            f"{fnum(r['difference'])} & {fnum(r['difference_se'])} & {fnum(r['difference_p'])} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "interactions.tex").write_text("\n".join(lines), encoding="utf-8")

    sub = pd.read_csv(SRC / "heterogeneity_subregions.csv")
    lines = [
        r"\begin{tabular}{lrrrr}", r"\toprule",
        r"RCEP subregion & Estimate & S.E. & $t$ statistic & $p$-value \\", r"\midrule",
    ]
    for _, r in sub.iterrows():
        label = str(r["subregion"]).replace("Japan_Korea", "Japan/Korea").replace("Australia_NZ", "Australia/New Zealand")
        lines.append(
            f"{esc(label)} & {fnum(r['coefficient'])} & {fnum(r['std_error'])} & "
            f"{fnum(r['t_stat'])} & {fnum(r['p_value'])} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "subregions.tex").write_text("\n".join(lines), encoding="utf-8")

    dml = json.loads((SRC / "dml_dr_did.json").read_text(encoding="utf-8"))
    lines = [
        r"\begin{tabular}{lrrrrr}", r"\toprule",
        r"Estimator & Estimate & Cluster S.E. & 95\% CI & $p$-value & Pairs \\", r"\midrule",
        (
            f"Cross-fitted DR-DID & {fnum(dml['estimate'])} & {fnum(dml['cluster_bootstrap_se'])} & "
            f"[{fnum(dml['cluster_bootstrap_ci_low'])}, {fnum(dml['cluster_bootstrap_ci_high'])}] & "
            f"{fnum(dml['cluster_bootstrap_p_value'])} & {int(dml['observations']):,} \\\\"
        ),
        r"\bottomrule", r"\end{tabular}",
    ]
    (OUT / "dml.tex").write_text("\n".join(lines), encoding="utf-8")

    # Compact placebo overview.  The underlying CSV files retain every draw;
    # this table only presents the pre-specified summaries used in the text.
    spatial = pd.read_csv(SRC / "placebo_spatial_varied_k.csv")
    temporal = pd.read_csv(SRC / "placebo_temporal_false_year.csv")
    leads = pd.read_csv(SRC / "placebo_temporal_fixed_leads.csv")
    mixed = pd.read_csv(SRC / "placebo_mixed.csv")
    placebo_json = json.loads((SRC / "placebo_battery_summary.json").read_text(encoding="utf-8"))
    placebo_lines = [
        r"\begin{tabular}{lrrrr}", r"\toprule",
        "Placebo & Setting & Estimate/mean & S.D./S.E. & Reference $p$ \\\\", r"\midrule",
    ]
    for _, r in spatial.iterrows():
        placebo_lines.append(
            f"Country-label & $k={int(r['k_countries'])}$ & {fnum(r['dist_mean'])} & "
            f"{fnum(r['dist_sd'])} & {fnum(r['rank_p_vs_real'])} \\\\"
        )
    pair_random = placebo_json["spatial_pair_random"]
    placebo_lines.append(
        f"Pair-level random & {int(placebo_json['treated_pair_units']):,} pairs & "
        f"{fnum(pair_random['dist_mean'])} & {fnum(pair_random['dist_sd'])} & "
        f"{fnum(pair_random['rank_p_vs_real'])} " + r"\\"
    )
    for _, r in temporal.iterrows():
        year = str(r["specification"]).split()[-1]
        placebo_lines.append(
            f"Fixed group/date & {year} & {fnum(r['coefficient'])} & {fnum(r['std_error'])} & "
            f"{fnum(r['p_value'])} \\\\"
        )
    for _, r in leads.iterrows():
        placebo_lines.append(
            f"Fixed lead & {float(r['lead_years']):.2f} years & {fnum(r['coefficient'])} & -- & -- \\\\"
        )
    random_dates = placebo_json["temporal_random_dates"]
    placebo_lines.append(
        f"Random false date & 999 draws & {fnum(random_dates['dist_mean'])} & "
        f"{fnum(random_dates['dist_sd'])} & {fnum(random_dates['rank_p_vs_real'])} " + r"\\"
    )
    for _, r in mixed.iterrows():
        placebo_lines.append(
            f"Mixed group/date & $k={int(r['k_countries'])}$ & {fnum(r['dist_mean'])} & "
            f"{fnum(r['dist_sd'])} & {fnum(r['rank_p_vs_real'])} \\\\"
        )
    placebo_lines += [r"\bottomrule", r"\end{tabular}"]
    (OUT / "placebo_summary.tex").write_text("\n".join(placebo_lines), encoding="utf-8")
    print(f"Wrote four tables to {OUT}")


if __name__ == "__main__":
    main()
