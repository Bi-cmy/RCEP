#!/usr/bin/env python3
"""Create the English event-study figure used in the Elsevier manuscript.

The figure reports the standard joint Wald test that all pre-treatment event
coefficients equal zero. The statistic is read from the estimation diagnostics
so that the plotted annotation and the regression output remain synchronized.
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "tables" / "event_study.csv"
DIAGNOSTICS = ROOT / "results" / "tables" / "diagnostics.json"
OUT = ROOT / "paper" / "paper_v2" / "figures"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 300,
})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA).sort_values("event_time")
    diagnostics = json.loads(DIAGNOSTICS.read_text(encoding="utf-8"))["event_study"]
    base = data.loc[data["event_time"].eq(-1)]
    plotted = data.loc[data["event_time"].ne(-1)]

    fig, ax = plt.subplots(figsize=(6.6, 3.75))
    ax.plot(
        data["event_time"], data["coefficient"],
        color="#8C8C8C", linewidth=0.9, zorder=1,
    )
    ax.errorbar(
        plotted["event_time"], plotted["coefficient"],
        yerr=1.96 * plotted["std_error"], fmt="o", linestyle="none",
        color="#0072B2", ecolor="#0072B2", elinewidth=1.1, capsize=3,
        markersize=4.8, label="Coefficient (95% CI)", zorder=3,
    )

    ax.scatter(base["event_time"], base["coefficient"], s=36,
               marker="D", facecolors="white", edgecolors="#333333", zorder=4,
               label="Omitted period")
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.axvline(-0.5, color="#D55E00", linestyle="--", linewidth=0.9,
               label="RCEP entry")
    ax.set_xlim(-5.45, 2.45)
    ax.set_xticks(range(-5, 3))
    ax.set_xticklabels(["-5", "-4", "-3", "-2", "-1", "0", "1", "2"])
    ax.set_xlabel("Event time (2021 = omitted reference year)")
    ax.set_ylabel("Estimated effect on active relationship probability")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5, alpha=0.65)
    handles, labels = ax.get_legend_handles_labels()
    order = [
        labels.index("Coefficient (95% CI)"),
        labels.index("Omitted period"),
        labels.index("RCEP entry"),
    ]
    ax.legend(
        [handles[index] for index in order], [labels[index] for index in order],
        loc="upper left", frameon=False, ncol=3, handlelength=1.4,
    )
    ax.text(
        0.98, 0.045,
        "Joint pre-trend test: "
        rf"Wald $\chi^2$({diagnostics['pretrend_df']}) = "
        rf"{diagnostics['pretrend_wald_stat']:.2f}, "
        rf"$p$ = {diagnostics['pretrend_p_value']:.3f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
        color="#333333",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5},
    )
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"parallel_trends_standard_en.{ext}",
                    bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


if __name__ == "__main__":
    main()
