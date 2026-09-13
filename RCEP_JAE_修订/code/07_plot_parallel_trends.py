#!/usr/bin/env python3
"""Publication-style event-study figure for the Chinese manuscript."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Noto Serif SC", "SimSun", "Times New Roman", "DejaVu Serif"],
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 300,
})


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(TABLES / "event_study.csv").sort_values("event_time")
    base = data.loc[data["event_time"].eq(-1)].copy()
    plotted = data.loc[data["event_time"].ne(-1)].copy()
    pre = plotted.loc[plotted["event_time"] < -1]
    post = plotted.loc[plotted["event_time"] >= 0]

    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    for frame, color, label in [
        (pre, "#4C78A8", "政策前"),
        (post, "#D55E00", "政策后"),
    ]:
        ax.errorbar(
            frame["event_time"], frame["coefficient"],
            yerr=1.96 * frame["std_error"], fmt="o", linestyle="-",
            color=color, ecolor=color, elinewidth=1.1, capsize=3,
            markersize=4.5, linewidth=1.2, label=label, zorder=3,
        )

    ax.scatter(base["event_time"], base["coefficient"], s=36,
               facecolors="white", edgecolors="#333333", zorder=4,
               label="省略期（2021）")
    ax.axhline(0, color="#333333", linewidth=0.8)
    ax.axvline(-0.5, color="#666666", linestyle="--", linewidth=0.9)
    ax.set_xlim(-5.45, 2.45)
    ax.set_xticks(range(-5, 3))
    ax.set_xticklabels(["-5", "-4", "-3", "-2", "-1（基期）", "0", "1", "2"])
    ax.set_xlabel("相对于RCEP生效年份的相对年份")
    ax.set_ylabel("对关系活跃概率的估计效应")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)
    ax.legend(loc="upper left", frameon=False, ncol=3, handlelength=1.5)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"parallel_trends_standard.{ext}",
                    bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"Saved standard parallel-trends figure to {FIGURES}")


if __name__ == "__main__":
    main()
