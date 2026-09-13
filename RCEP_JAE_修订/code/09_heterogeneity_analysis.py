#!/usr/bin/env python3
"""Formal heterogeneity tests for the Chinese RCEP manuscript."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "pair_year.parquet"
RESULTS = ROOT / "results" / "tables"
LEGACY = ROOT / "legacy"

REGIONS = {
    "东盟十国": {"ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"},
    "日本和韩国": {"JP", "KR"},
    "澳大利亚和新西兰": {"AU", "NZ"},
}


def indexed(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def cluster(frame: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "pair":
        values = frame.index.get_level_values("pair_id")
        return pd.DataFrame({"pair": values}, index=frame.index)
    if mode == "country":
        values = pd.Categorical(frame["partner_country"]).codes
        return pd.DataFrame({"country": values}, index=frame.index)
    raise ValueError(mode)


def interaction(panel: pd.DataFrame, moderator: str, label: str, mode: str) -> dict[str, float | int | str]:
    work = panel.dropna(subset=[moderator]).copy()
    work[moderator] = work[moderator].astype(float)
    work["post_mod"] = work["post2022"] * work[moderator]
    work["treat_mod"] = work["treated_uniform"] * work[moderator]
    data = indexed(work)
    result = PanelOLS(
        data["active"].astype(float),
        data[["treated_uniform", "post_mod", "treat_mod"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster(data, mode))
    base = float(result.params["treated_uniform"])
    diff = float(result.params["treat_mod"])
    high_variance = (
        result.cov.loc["treated_uniform", "treated_uniform"]
        + result.cov.loc["treat_mod", "treat_mod"]
        + 2 * result.cov.loc["treated_uniform", "treat_mod"]
    )
    return {
        "dimension": label,
        "moderator": moderator,
        "cluster": mode,
        "base_effect": base,
        "base_se": float(result.std_errors["treated_uniform"]),
        "base_p": float(result.pvalues["treated_uniform"]),
        "high_effect": base + diff,
        "high_se_delta": float(np.sqrt(max(high_variance, 0))),
        "difference": diff,
        "difference_se": float(result.std_errors["treat_mod"]),
        "difference_p": float(result.pvalues["treat_mod"]),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "countries": int(data["partner_country"].nunique()),
    }


def regions(panel: pd.DataFrame, mode: str) -> tuple[pd.DataFrame, dict[str, float | int]]:
    work = panel.copy()
    terms = []
    for label, countries in REGIONS.items():
        term = f"region_{len(terms)}"
        work[term] = work["partner_country"].isin(countries).astype(float) * work["post2022"]
        terms.append(term)
    data = indexed(work)
    result = PanelOLS(
        data["active"].astype(float), data[terms].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cluster(data, mode))
    rows = []
    for label, term in zip(REGIONS, terms):
        rows.append({
            "region": label,
            "cluster": mode,
            "coefficient": float(result.params[term]),
            "std_error": float(result.std_errors[term]),
            "p_value": float(result.pvalues[term]),
            "observations": int(result.nobs),
            "pairs": int(data.index.get_level_values("pair_id").nunique()),
        })
    restrictions = []
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            row = np.zeros((1, len(result.params)))
            row[0, list(result.params.index).index(terms[i])] = 1
            row[0, list(result.params.index).index(terms[j])] = -1
            restrictions.append(float(np.asarray(result.wald_test(row).pval).squeeze()))
    return pd.DataFrame(rows), {
        "cluster": mode,
        "pairwise_equality_p_min": min(restrictions),
        "pairwise_equality_p_max": max(restrictions),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
    }


def write_latex(interactions: pd.DataFrame, subregions: pd.DataFrame) -> None:
    pair_inter = interactions.loc[interactions["cluster"].eq("pair")]
    pair_regions = subregions.loc[subregions["cluster"].eq("pair")]
    lines = [
        r"\begin{table}[htbp]", r"\centering", r"\caption{异质性检验：预先确定的组间交互}",
        r"\label{tab:heterogeneity}", r"\small", r"\begin{tabular}{lrrrr}", r"\toprule",
        r"面板A：分组变量 & 低组效应 & 高组效应 & 组间差异 & 差异$p$值 \\",
        r"\midrule",
    ]
    for _, row in pair_inter.iterrows():
        p_value = "<0.001" if row["difference_p"] < 0.001 else f"{row['difference_p']:.3f}"
        lines.append(
            f"{row['dimension']} & {row['base_effect']:.4f} & {row['high_effect']:.4f} "
            f"& {row['difference']:.4f} & {p_value} \\\\"
        )
    lines += [r"\midrule", r"面板B：成员区域 & 系数 & 标准误 & $p$值 &  \\ ", r"\midrule"]
    for _, row in pair_regions.iterrows():
        p_value = "<0.001" if row["p_value"] < 0.001 else f"{row['p_value']:.3f}"
        lines.append(
            f"{row['region']} & {row['coefficient']:.4f} & {row['std_error']:.4f} "
            f"& {p_value} & \\\\"
        )
    lines += [
        r"\bottomrule", r"\end{tabular}", r"\begin{tablenotes}",
        r"\footnotesize 注：面板A中的低组和高组效应来自同一模型，模型包含$Post\times H$和$RCEP\times Post\times H$，其中$H$均在2021年政策前确定；差异列为三重交互项，正式检验的是组间差异而非分别比较显著性。面板B为成员区域的探索性估计。所有模型含关系对和年份固定效应，表内标准误按关系对聚类。",
        r"\end{tablenotes}", r"\end{table}",
    ]
    (LEGACY / "table5_heterogeneity.tex").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(DATA)
    moderators = [
        ("供应商关系方向", "supplier_link"),
        ("政策前RCEP来源广度", "multi_rcep_2021"),
        ("政策前企业规模", "large_firm"),
    ]
    interaction_rows = []
    for label, moderator in moderators:
        interaction_rows.append(interaction(panel, moderator, label, "pair"))
        interaction_rows.append(interaction(panel, moderator, label, "country"))
    interactions = pd.DataFrame(interaction_rows)
    interactions.to_csv(RESULTS / "heterogeneity_interactions_formal.csv", index=False, encoding="utf-8-sig")
    region_pair, region_pair_diag = regions(panel, "pair")
    region_country, region_country_diag = regions(panel, "country")
    subregions = pd.concat([region_pair, region_country], ignore_index=True)
    subregions.to_csv(RESULTS / "heterogeneity_subregions_formal.csv", index=False, encoding="utf-8-sig")
    write_latex(interactions, subregions)
    print(interactions[["dimension", "cluster", "base_effect", "high_effect", "difference", "difference_p"]].to_string(index=False))
    print(subregions.to_string(index=False))
    print({"pair_region_diagnostics": region_pair_diag, "country_region_diagnostics": region_country_diag})


if __name__ == "__main__":
    main()
