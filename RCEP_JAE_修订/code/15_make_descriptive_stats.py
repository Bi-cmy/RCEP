#!/usr/bin/env python3
"""Create JAE-style summary statistics and an informative descriptive figure."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / "data" / "derived" / "pair_year.parquet"
MECH = ROOT / "results" / "tables" / "mechanism_partner_year_metrics.csv"
FIRM = ROOT.parent.parent / "关税冲击对供应链的影响" / "data" / "cleaned" / "ddd_panel.parquet"
OUT_TABLE = ROOT / "paper" / "paper_v2" / "tables" / "table1_summary_statistics.tex"
OUT_FIG = ROOT / "paper" / "paper_v2" / "figures"


def fmt(x: float, digits: int = 3) -> str:
    if pd.isna(x):
        return "--"
    return f"{x:,.{digits}f}"


def stats_row(label: str, values: pd.Series, scale: float = 1.0, digits: int = 3,
              binary: bool = False) -> str:
    x = pd.to_numeric(values, errors="coerce").dropna() * scale
    q = x.quantile([.50])
    tail = ("-- & -- & --" if binary else
            f"{fmt(x.min(), digits)} & {fmt(q.loc[.50], digits)} & {fmt(x.max(), digits)}")
    return f"{label} & {len(x):,} & {fmt(x.mean(), digits)} & {fmt(x.std(), digits)} & {tail} \\\\"


def write_table(pair: pd.DataFrame, mech: pd.DataFrame, firm: pd.DataFrame | None) -> None:
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Summary statistics}",
        r"\label{tab:summary}",
        r"\small",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Variable & Observations & Mean & S.D. & Min. & Median & Max. \\" ,
        r"\midrule",
        r"\multicolumn{7}{l}{\textit{Relationship--year variables}} \\",
        stats_row("Active relationship", pair["active"], binary=True),
        stats_row("RCEP partner", pair["rcep"], binary=True),
        stats_row("Post-2022 indicator", pair["post2022"], binary=True),
        stats_row(r"RCEP $\times$ Post-2022", pair["treated_uniform"], binary=True),
        stats_row("Foreign supplier relationship", pair["supplier_link"], binary=True),
        stats_row("Relationship age in 2021 (years)", pair["age_2021"]),
        stats_row("Pre-policy RCEP sourcing breadth", pair["rcep_breadth_2021"]),
        stats_row("Large-firm indicator", pair["large_firm"], binary=True),
        r"\midrule",
        r"\multicolumn{7}{l}{\textit{Partner-country--year indicators}} \\",
        stats_row("Incremental tariff relief (percentage points)", mech["tariff_relief"], scale=100),
        stats_row("Intermediate-goods share of bilateral imports (percent)", mech["intermediate_share"], scale=100),
        stats_row("Partner-country share of China's imports (percent)", mech["source_share"], scale=100),
    ]
    if firm is not None:
        lines += [
            r"\midrule",
            r"\multicolumn{7}{l}{\textit{Firm-year covariates}} \\",
            stats_row("Log total assets", firm["Size"]),
            stats_row("Leverage", firm["Lev"]),
            stats_row("Return on assets", firm["ROA"]),
            stats_row("Revenue growth", firm["Growth"]),
            stats_row("Inventory intensity", firm["InvDensity"]),
        ]
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\begin{minipage}{0.85\textwidth}",
        r"\footnotesize \textit{Notes}: Statistics cover 2017--2024 and use all available observations; counts vary with missing values. Binary variables report the mean and S.D. only, with -- indicating omitted distribution statistics. Percentage measures use the units shown in the variable labels.",
        r"\end{minipage}",
        r"\end{table}",
    ]
    OUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    OUT_TABLE.write_text("\n".join(lines), encoding="utf-8")


def write_figure(pair: pd.DataFrame) -> None:
    annual = (
        pair.groupby(["year", "rcep"], as_index=False)
        .agg(active_rate=("active", "mean"), n_pairs=("pair_id", "nunique"))
    )
    wide = annual.pivot(index="year", columns="rcep", values="active_rate").sort_index()
    gap = (wide[1] - wide[0]) * 100

    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8,
        "ytick.labelsize": 8, "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "white", "axes.facecolor": "white",
    })
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.9), sharex=True)
    ax = axes[0]
    ax.plot(wide.index, wide[1] * 100, marker="o", linewidth=1.4, markersize=3.5,
            color="#0072B2", label="RCEP partners")
    ax.plot(wide.index, wide[0] * 100, marker="s", linewidth=1.2, markersize=3.2,
            linestyle="--", color="#555555", label="Other partners")
    ax.axvline(2021.5, color="#D55E00", linestyle="--", linewidth=1)
    ax.set_title("Active relationship rate", fontsize=9)
    ax.set_ylabel("Percent")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)

    ax = axes[1]
    ax.plot(gap.index, gap, marker="o", linewidth=1.4, markersize=3.5, color="#009E73")
    ax.axhline(0, color="black", linewidth=0.7)
    ax.axvline(2021.5, color="#D55E00", linestyle="--", linewidth=1)
    ax.set_title("RCEP minus other partners", fontsize=9)
    ax.set_ylabel("Percentage points")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)
    for axis in axes:
        axis.set_xlabel("Year")
        axis.set_xticks(range(2017, 2025, 2))
    fig.tight_layout(w_pad=1.4)
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT_FIG / f"descriptive_active_links.{ext}", dpi=300,
                    bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def main() -> None:
    pair = pd.read_parquet(PAIR)
    mech = pd.read_csv(MECH)
    firm = None
    if FIRM.exists():
        firm = pd.read_parquet(FIRM)
        firm = firm.loc[firm["year"].between(2017, 2024)].copy()
    write_table(pair, mech, firm)
    write_figure(pair)
    print(f"Wrote {OUT_TABLE}")


if __name__ == "__main__":
    main()
