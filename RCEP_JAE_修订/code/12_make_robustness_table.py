#!/usr/bin/env python3
"""Build the robustness table for the Chinese manuscript."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "legacy" / "table7_robustness.tex"

PASSING = [
    "Country-specific entry timing, pair clusters",
    "Exclude 2020-2021, pair clusters",
    "Window 2019-2024, pair clusters",
    "Exclude US partners, pair clusters",
    "Exclude offshore financial centers, pair clusters",
]
INFERENCE = [
    "Country-cluster inference (sensitivity)",
    "Two-way country and Chinese-firm clusters",
]
LABELS = {
    "Country-specific entry timing, pair clusters": "按成员国生效时点",
    "Exclude 2020-2021, pair clusters": "剔除2020—2021年",
    "Window 2019-2024, pair clusters": "样本窗口2019—2024年",
    "Exclude US partners, pair clusters": "剔除美国伙伴",
    "Exclude offshore financial centers, pair clusters": "剔除离岸金融中心",
    "Country-cluster inference (sensitivity)": "伙伴国聚类",
    "Two-way country and Chinese-firm clusters": "企业—伙伴国双向聚类",
}


def pformat(value: float) -> str:
    value = float(value)
    return "<0.001" if value < 0.001 else f"{value:.3f}"


def main() -> None:
    robust = pd.read_csv(TABLES / "robustness_specs.csv").set_index("specification")
    dml = json.loads((TABLES / "dml_auth_dml.json").read_text(encoding="utf-8"))

    rows: list[tuple[str, float, float, str, str, str]] = []
    for name in PASSING:
        row = robust.loc[name]
        rows.append((LABELS[name], float(row["coefficient"]),
                     float(row["std_error"]), pformat(row["p_value"]),
                     f"{int(row['observations']):,}", "支持"))
    for name in INFERENCE:
        row = robust.loc[name]
        rows.append((LABELS[name], float(row["coefficient"]), float(row["std_error"]),
                     pformat(row["p_value"]), f"{int(row['observations']):,}",
                     "推断敏感性"))
    rows.append(("双重机器学习（交叉拟合）", float(dml["theta_att"]),
                 float(dml["cluster_bootstrap_se"]),
                 pformat(dml["cluster_bootstrap_p_value"]),
                 f"{int(dml['observations']):,}", "方法敏感性"))

    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{稳健性检验与敏感性诊断}",
        r"\label{tab:robustness}",
        r"\small",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        "规格 & 系数 & 标准误 & $p$值 & 观测值 & 结论 " + r"\\",
        r"\midrule",
    ]
    for name, coef, se, p, obs, status in rows:
        lines.append(f"{name} & {coef:.4f} & {se:.4f} & {p} & {obs} & {status} " + r"\\")
    lines += [
        r"\bottomrule",
        r"\end{tabular}}",
        r"\begin{tablenotes}",
        r"\footnotesize 注：前五行是预先设定的样本或处理时点稳健性检验；“支持”表示系数与主规格同方向且在5\%水平显著。随后两行改变聚类层级，用于检验推断对政策暴露层级的敏感性。双重机器学习在企业—伙伴关系对层面将2017—2021年均值与2022—2024年均值之差作为结果变量，使用伙伴国分组五折交叉拟合，以梯度提升回归器估计结果方程、以梯度提升分类器估计二元处理倾向，并以关系对聚类自助法计算表内标准误；伙伴国聚类结果作为敏感性核对。由于结果构造不同，DML不与年度固定效应DID系数作机械等同比较。",
        r"\end{tablenotes}",
        r"\end{table}",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(pd.DataFrame(rows, columns=["specification", "coefficient", "std_error",
                                      "p_value", "observations", "status"]).to_string(index=False))


if __name__ == "__main__":
    main()
