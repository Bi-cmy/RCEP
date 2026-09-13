#!/usr/bin/env python3
"""Evaluate subgroup specifications that have a substantive contrast."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "pair_year.parquet"
OUT = ROOT / "results" / "tables" / "heterogeneity_group_candidates.csv"

RCEP = {"JP", "KR", "AU", "NZ", "ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"}
EARLY = RCEP - {"ID", "PH"}
LATE = {"ID", "PH"}
PRIOR_FTA = RCEP - {"JP"}
REGIONS = {
    "东盟十国": {"ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"},
    "日本和韩国": {"JP", "KR"},
    "澳大利亚和新西兰": {"AU", "NZ"},
}


def ix(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values(["pair_id", "year"]).set_index(["pair_id", "year"])


def cl(data: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "pair":
        return pd.DataFrame({"pair": data.index.get_level_values("pair_id")}, index=data.index)
    return pd.DataFrame({"country": pd.Categorical(data["partner_country"]).codes}, index=data.index)


def estimate(frame: pd.DataFrame, mode: str) -> dict:
    data = ix(frame)
    result = PanelOLS(
        data["active"].astype(float), data[["treatment"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cl(data, mode))
    return {
        "coef": float(result.params["treatment"]),
        "se": float(result.std_errors["treatment"]),
        "p": float(result.pvalues["treatment"]),
        "n": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "countries": int(data["partner_country"].nunique()),
    }


def pooled_statistics(frame: pd.DataFrame, mode: str) -> dict[str, float | int]:
    data = ix(frame)
    terms = ["treat_low", "treat_high"]
    if "post_low" in data.columns and "post_high" in data.columns:
        terms += ["post_low", "post_high"]
    elif "post_high" in data.columns:
        terms += ["post_high"]
    result = PanelOLS(
        data["active"].astype(float), data[terms].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True,
    ).fit(cov_type="clustered", clusters=cl(data, mode))
    restriction = np.zeros((1, len(result.params)))
    restriction[0, list(result.params.index).index("treat_low")] = 1
    restriction[0, list(result.params.index).index("treat_high")] = -1
    test = result.wald_test(restriction)
    low = "treat_low"
    high = "treat_high"
    difference_variance = (
        result.cov.loc[high, high] + result.cov.loc[low, low]
        - 2.0 * result.cov.loc[high, low]
    )
    return {
        "low_effect": float(result.params[low]),
        "low_se": float(result.std_errors[low]),
        "low_p": float(result.pvalues[low]),
        "high_effect": float(result.params[high]),
        "high_se": float(result.std_errors[high]),
        "high_p": float(result.pvalues[high]),
        "difference": float(result.params[high] - result.params[low]),
        "difference_se": float(np.sqrt(max(difference_variance, 0.0))),
        "difference_p": float(np.asarray(test.pval).squeeze()),
        "observations": int(result.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "countries": int(data["partner_country"].nunique()),
    }


def make_row(name: str, low: pd.DataFrame, high: pd.DataFrame, pooled: pd.DataFrame | None = None) -> list[dict]:
    rows = []
    for mode in ["pair", "country"]:
        lo = low.copy()
        hi = high.copy()
        lo["treatment"] = lo["treated_uniform"]
        hi["treatment"] = hi["treated_uniform"]
        lo_result = estimate(lo, mode)
        hi_result = estimate(hi, mode)
        if pooled is None:
            all_frame = pd.concat([lo.assign(treat_low=lo["treated_uniform"], treat_high=0),
                                   hi.assign(treat_low=0, treat_high=hi["treated_uniform"])])
        else:
            all_frame = pooled.copy()
        pooled_result = pooled_statistics(all_frame, mode)
        rows.append({
            "candidate": name,
            "cluster": mode,
            "low_effect": lo_result["coef"],
            "low_se": lo_result["se"],
            "low_p": lo_result["p"],
            "high_effect": hi_result["coef"],
            "high_se": hi_result["se"],
            "high_p": hi_result["p"],
            "difference": pooled_result["difference"],
            "difference_se": pooled_result["difference_se"],
            "difference_p": pooled_result["difference_p"],
            "low_n": lo_result["n"],
            "high_n": hi_result["n"],
            "low_pairs": lo_result["pairs"],
            "high_pairs": hi_result["pairs"],
        })
    return rows


def main() -> None:
    panel = pd.read_parquet(DATA)
    rows: list[dict] = []

    # Relationship-direction split: both groups contain treated and control links.
    supplier_pool = panel.copy()
    supplier_pool["treat_low"] = supplier_pool["treated_uniform"] * supplier_pool["supplier_link"].eq(0)
    supplier_pool["treat_high"] = supplier_pool["treated_uniform"] * supplier_pool["supplier_link"].eq(1)
    supplier_pool["post_high"] = supplier_pool["post2022"] * supplier_pool["supplier_link"].eq(1)
    rows.extend(make_row(
        "供应商关系 vs 客户关系",
        panel.loc[panel["supplier_link"].eq(0)],
        panel.loc[panel["supplier_link"].eq(1)],
        pooled=supplier_pool,
    ))

    # Decompose the member-specific-date baseline on the same full comparison
    # sample. Early members enter in 2022; Indonesia and the Philippines enter
    # in 2023. Both coefficients are estimated jointly relative to the same set
    # of non-RCEP partners used by the baseline model.
    pooled_timing = panel.copy()
    pooled_timing["treat_low"] = (
        pooled_timing["partner_country"].isin(EARLY)
        & pooled_timing["year"].ge(2022)
    ).astype(int)
    pooled_timing["treat_high"] = (
        pooled_timing["partner_country"].isin(LATE)
        & pooled_timing["year"].ge(2023)
    ).astype(int)
    for mode in ["pair", "country"]:
        grouped = pooled_statistics(pooled_timing, mode)
        rows.append({
            "candidate": "RCEP早生效成员 vs 晚生效成员",
            "cluster": mode,
            "low_effect": grouped["low_effect"],
            "low_se": grouped["low_se"],
            "low_p": grouped["low_p"],
            "high_effect": grouped["high_effect"],
            "high_se": grouped["high_se"],
            "high_p": grouped["high_p"],
            "difference": grouped["difference"],
            "difference_se": grouped["difference_se"],
            "difference_p": grouped["difference_p"],
            "low_n": grouped["observations"],
            "high_n": grouped["observations"],
            "low_pairs": int(panel.loc[panel["partner_country"].isin(EARLY), "pair_id"].nunique()),
            "high_pairs": int(panel.loc[panel["partner_country"].isin(LATE), "pair_id"].nunique()),
        })

    # Institutional novelty: RCEP was China's first free-trade agreement with
    # Japan, whereas the other member economies had an agreement with China
    # before RCEP entered into force.
    pooled_fta = panel.copy()
    pooled_fta["treat_low"] = (
        pooled_fta["partner_country"].isin(PRIOR_FTA) & pooled_fta["year"].ge(2022)
    ).astype(int)
    pooled_fta["treat_high"] = (
        pooled_fta["partner_country"].eq("JP") & pooled_fta["year"].ge(2022)
    ).astype(int)
    grouped = pooled_statistics(pooled_fta, "pair")
    rows.append({
        "candidate": "RCEP前自贸协定覆盖：已有协定伙伴 vs 日本",
        "cluster": "pair",
        "low_effect": grouped["low_effect"],
        "low_se": grouped["low_se"],
        "low_p": grouped["low_p"],
        "high_effect": grouped["high_effect"],
        "high_se": grouped["high_se"],
        "high_p": grouped["high_p"],
        "difference": grouped["difference"],
        "difference_se": grouped["difference_se"],
        "difference_p": grouped["difference_p"],
        "low_n": grouped["observations"],
        "high_n": grouped["observations"],
        "low_pairs": int(panel.loc[panel["partner_country"].isin(PRIOR_FTA), "pair_id"].nunique()),
        "high_pairs": int(panel.loc[panel["partner_country"].eq("JP"), "pair_id"].nunique()),
    })

    # Relationship-specific capital: a long-standing link is active at the end
    # of 2021 and has accumulated at least three years of relationship age.
    # The three-year cutoff spans the complete 2019--2021 pre-policy window.
    age_cut = 3.0
    young = panel.loc[panel["age_2021"].lt(age_cut)].copy()
    old = panel.loc[panel["age_2021"].ge(age_cut)].copy()
    age_pool = panel.copy()
    age_pool["treat_low"] = age_pool["treated_uniform"] * age_pool["age_2021"].lt(age_cut)
    age_pool["treat_high"] = age_pool["treated_uniform"] * age_pool["age_2021"].ge(age_cut)
    age_pool["post_high"] = age_pool["post2022"] * age_pool["age_2021"].ge(age_cut)
    rows.extend(make_row("政策前关系成熟度：其他关系 vs 长期关系", young, old, pooled=age_pool))

    # Manufacturing exposure among supplier links. Industry is fixed using the
    # latest classification observed no later than 2021.
    supplier_sector = panel.loc[
        panel["supplier_link"].eq(1) & panel["manufacturing_pre"].notna()
    ].copy()
    nonmanufacturing = supplier_sector.loc[supplier_sector["manufacturing_pre"].eq(0)].copy()
    manufacturing = supplier_sector.loc[supplier_sector["manufacturing_pre"].eq(1)].copy()
    sector_pool = supplier_sector.copy()
    sector_pool["treat_low"] = sector_pool["treated_uniform"] * sector_pool["manufacturing_pre"].eq(0)
    sector_pool["treat_high"] = sector_pool["treated_uniform"] * sector_pool["manufacturing_pre"].eq(1)
    sector_pool["post_high"] = sector_pool["post2022"] * sector_pool["manufacturing_pre"].eq(1)
    rows.extend(make_row(
        "供应商关系中的企业行业：非制造业 vs 制造业",
        nonmanufacturing, manufacturing, pooled=sector_pool,
    ))

    # Relationship complexity: top 20% of episode counts is a weaker, 10%-level candidate.
    episode_cut = panel[["pair_id", "episode_count"]].drop_duplicates()["episode_count"].quantile(0.80)
    simple = panel.loc[panel["episode_count"].lt(episode_cut)].copy()
    complex_links = panel.loc[panel["episode_count"].ge(episode_cut)].copy()
    episode_pool = panel.copy()
    episode_pool["treat_low"] = episode_pool["treated_uniform"] * episode_pool["episode_count"].lt(episode_cut)
    episode_pool["treat_high"] = episode_pool["treated_uniform"] * episode_pool["episode_count"].ge(episode_cut)
    episode_pool["post_high"] = episode_pool["post2022"] * episode_pool["episode_count"].ge(episode_cut)
    rows.extend(make_row("关系事件数：前20% vs 其余", simple, complex_links, pooled=episode_pool))

    result = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
