#!/usr/bin/env python3
"""Build the grouped heterogeneity table used in the Chinese manuscript."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "pair_year.parquet"
CANDIDATES = ROOT / "results" / "tables" / "heterogeneity_group_candidates.csv"
SUBREGIONS = ROOT / "results" / "tables" / "heterogeneity_subregions_formal.csv"
OUT = ROOT / "legacy" / "table5_heterogeneity.tex"
OUT_ENGLISH = ROOT / "paper" / "paper_v2" / "tables" / "table3_heterogeneity.tex"

REGIONS = {
    "东盟十国": {"ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"},
    "日本和韩国": {"JP", "KR"},
    "澳大利亚和新西兰": {"AU", "NZ"},
}


def indexed(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def cluster(data: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "pair":
        return pd.DataFrame({"pair": data.index.get_level_values("pair_id")}, index=data.index)
    return pd.DataFrame({"country": pd.Categorical(data["partner_country"]).codes}, index=data.index)


def region_contrast(panel: pd.DataFrame) -> dict[str, float]:
    region_countries = REGIONS["东盟十国"] | REGIONS["日本和韩国"]
    work = panel.loc[
        panel["partner_country"].isin(region_countries) | panel["asia_control"].eq(1)
    ].copy()
    work["treat_asean"] = work["partner_country"].isin(REGIONS["东盟十国"]).astype(int) * work["post2022"]
    work["treat_jk"] = work["partner_country"].isin(REGIONS["日本和韩国"]).astype(int) * work["post2022"]
    data = indexed(work)
    result = PanelOLS(
        data["active"].astype(float), data[["treat_asean", "treat_jk"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster(data, "country"))
    restriction = np.array([[1, -1]])
    test = result.wald_test(restriction)
    return {
        "low_effect": float(result.params["treat_asean"]),
        "low_p": float(result.pvalues["treat_asean"]),
        "high_effect": float(result.params["treat_jk"]),
        "high_p": float(result.pvalues["treat_jk"]),
        "difference": float(result.params["treat_jk"] - result.params["treat_asean"]),
        "difference_p": float(np.asarray(test.pval).squeeze()),
    }


def pformat(value: float) -> str:
    return "<0.001" if float(value) < 0.001 else f"{float(value):.3f}"


def main() -> None:
    candidates = pd.read_csv(CANDIDATES)
    rows = []
    for candidate, cluster_name in [
        ("供应商关系 vs 客户关系", "pair"),
        ("政策前关系成熟度：其他关系 vs 长期关系", "pair"),
        ("RCEP前自贸协定覆盖：已有协定伙伴 vs 日本", "pair"),
        ("供应商关系中的企业行业：非制造业 vs 制造业", "pair"),
    ]:
        row = candidates.loc[
            candidates["candidate"].eq(candidate) & candidates["cluster"].eq(cluster_name)
        ].iloc[0]
        labels = {
            "供应商关系 vs 客户关系": ("客户关系", "供应商关系"),
            "政策前关系成熟度：其他关系 vs 长期关系": ("其他关系", "长期关系"),
            "RCEP前自贸协定覆盖：已有协定伙伴 vs 日本": ("已有协定伙伴", "日本"),
            "供应商关系中的企业行业：非制造业 vs 制造业": ("非制造业", "制造业"),
        }
        low_label, high_label = labels[candidate]
        rows.append({
            "candidate": candidate,
            "low_label": low_label,
            "high_label": high_label,
            "low_effect": row["low_effect"], "low_se": row["low_se"], "low_p": row["low_p"],
            "high_effect": row["high_effect"], "high_se": row["high_se"], "high_p": row["high_p"],
            "difference": row["difference"], "difference_se": row["difference_se"],
            "difference_p": row["difference_p"],
            "cluster": "关系对" if cluster_name == "pair" else "伙伴国",
        })
    result = pd.DataFrame(rows)
    lines = [
        r"\begin{table}[htbp]", r"\centering",
        r"\caption{分组异质性检验：显著组与不显著组的对比}",
        r"\label{tab:heterogeneity}", r"\small",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lccccc}", r"\toprule",
        r"分组方案 & 低组效应（$p$） & 高组效应（$p$） & 组间差异 & 差异$p$值 & 聚类层级 \\",
        r"\midrule",
    ]
    for _, row in result.iterrows():
        lines.append(
            f"{row['candidate']} & {row['low_effect']:.4f} ({pformat(row['low_p'])}) "
            f"& {row['high_effect']:.4f} ({pformat(row['high_p'])}) "
            f"& {row['difference']:.4f} & {pformat(row['difference_p'])} "
            f"& {row['cluster']} \\\\"
        )
    lines += [
        r"\bottomrule", r"\end{tabular}}",
        r"\begin{tablenotes}",
        r"\footnotesize 注：括号内为组内处理效应的$p$值；组间差异来自同一回归中的线性限制检验。长期关系是指截至2021年末关系年龄至少为三年的关系。企业行业分组仅使用供应商关系及政策前行业信息可匹配的企业。所有模型均含关系对和年份固定效应，标准误按关系对聚类。",
        r"\end{tablenotes}", r"\end{table}",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    pair_rows = result.loc[result["cluster"].eq("关系对")].copy()

    def stars(value: float) -> str:
        if float(value) < 0.01:
            return "***"
        if float(value) < 0.05:
            return "**"
        if float(value) < 0.10:
            return "*"
        return ""

    direction = pair_rows.loc[pair_rows["candidate"].eq("供应商关系 vs 客户关系")].iloc[0]
    maturity = pair_rows.loc[pair_rows["candidate"].str.contains("成熟度")].iloc[0]
    agreement = pair_rows.loc[pair_rows["candidate"].str.contains("自贸协定覆盖")].iloc[0]
    sector = pair_rows.loc[pair_rows["candidate"].str.contains("企业行业")].iloc[0]
    english_lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Heterogeneity analysis}",
        r"\label{tab:heterogeneity}",
        r"\small",
        r"\begin{minipage}{\textwidth}",
        r"\centering",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"Partition & Group 1 & Group 2 & Difference (Group 2 $-$ Group 1) \\",
        r"\midrule",
        (
            f"Relationship direction & Customer: {direction['low_effect']:.4f}{stars(direction['low_p'])} "
            f"& Supplier: {direction['high_effect']:.4f}{stars(direction['high_p'])} "
            f"& {direction['difference']:.4f}{stars(direction['difference_p'])} \\\\"
        ),
        (
            f" & ({direction['low_se']:.4f}) & ({direction['high_se']:.4f}) "
            f"& ({direction['difference_se']:.4f}) \\\\"
        ),
        (
            f"Pre-policy relationship maturity & Other: {maturity['low_effect']:.4f}{stars(maturity['low_p'])} "
            f"& Long-standing: {maturity['high_effect']:.4f}{stars(maturity['high_p'])} "
            f"& {maturity['difference']:.4f}{stars(maturity['difference_p'])} \\\\"
        ),
        (
            f" & ({maturity['low_se']:.4f}) & ({maturity['high_se']:.4f}) "
            f"& ({maturity['difference_se']:.4f}) \\\\"
        ),
        (
            f"Pre-RCEP FTA coverage & Existing FTA: {agreement['low_effect']:.4f}{stars(agreement['low_p'])} "
            f"& Japan: {agreement['high_effect']:.4f}{stars(agreement['high_p'])} "
            f"& {agreement['difference']:.4f}{stars(agreement['difference_p'])} \\\\"
        ),
        (
            f" & ({agreement['low_se']:.4f}) & ({agreement['high_se']:.4f}) "
            f"& ({agreement['difference_se']:.4f}) \\\\"
        ),
        (
            f"Firm sector, supplier links & Non-manufacturing: {sector['low_effect']:.4f}{stars(sector['low_p'])} "
            f"& Manufacturing: {sector['high_effect']:.4f}{stars(sector['high_p'])} "
            f"& {sector['difference']:.4f}{stars(sector['difference_p'])} \\\\"
        ),
        (
            f" & ({sector['low_se']:.4f}) & ({sector['high_se']:.4f}) "
            f"& ({sector['difference_se']:.4f}) \\\\"
        ),
        r"\bottomrule",
        r"\end{tabular}",
        r"}",
        r"\vspace{2pt}",
        r"\parbox{\textwidth}{\footnotesize \textit{Notes}: Group coefficients are estimated jointly. A long-standing relationship is active at year-end 2021 and is at least three years old. The sector comparison is restricted to supplier links with pre-policy industry data. All models include relationship-pair and year fixed effects; relationship-pair clustered standard errors are in parentheses. The difference is Group 2 minus Group 1. * $p<0.10$, ** $p<0.05$, *** $p<0.01$.}",
        r"\end{minipage}",
        r"\end{table}",
    ]
    OUT_ENGLISH.write_text("\n".join(english_lines), encoding="utf-8")
    result.to_csv(ROOT / "results" / "tables" / "heterogeneity_grouped_main.csv", index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
