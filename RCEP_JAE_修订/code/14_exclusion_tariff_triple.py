#!/usr/bin/env python3
"""Exclusion/alternative-explanation test using US tariff exposure.

The test asks whether the RCEP effect is disproportionately large for firms
with higher pre-determined US trade-war tariff exposure.  The estimand is the
pair-level triple interaction Post x RCEP-partner x tariff exposure, with
Post x tariff exposure included to absorb general post-period responses.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "pair_year.parquet"
EXPOSURE = (ROOT.parent / "中美供应链STGNN" / "预处理数据_非供应链" /
            "04_模型输入" / "firm_tariff_exposure.parquet")
TABLES = ROOT / "results" / "tables"
OUT_TEX = ROOT / "legacy" / "table6_exclusion.tex"


def fit(frame: pd.DataFrame, variables: list[str], cluster: str):
    data = frame.set_index(["pair_id", "year"]).sort_index()
    cols = ["active", *variables, "partner_country"]
    data = data[cols].dropna()
    model = PanelOLS(
        data["active"].astype(float),
        data[variables].astype(float),
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
        check_rank=True,
    )
    if cluster == "pair":
        groups = pd.DataFrame(
            {"pair": data.index.get_level_values("pair_id")}, index=data.index
        )
    elif cluster == "country":
        groups = pd.DataFrame(
            {"country": pd.Categorical(data["partner_country"]).codes},
            index=data.index,
        )
    else:
        raise ValueError(cluster)
    result = model.fit(cov_type="clustered", clusters=groups)
    return result, data


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    pair = pd.read_parquet(DATA)
    exposure = pd.read_parquet(EXPOSURE)

    # Use the 2019 exposure, before RCEP's 2022 entry into force and after the
    # US tariff schedule had stabilized.  It is fixed within firm in the panel.
    exposure = exposure.loc[exposure["year"].eq(2019), [
        "ticker6", "us_trade_war_301_232_export_weighted"
    ]].drop_duplicates("ticker6")
    exposure = exposure.rename(columns={
        "ticker6": "ticker_key",
        "us_trade_war_301_232_export_weighted": "us_tariff_2019",
    })
    pair["ticker_key"] = pair["ticker_key"].astype(str).str.zfill(6)
    exposure["ticker_key"] = exposure["ticker_key"].astype(str).str.zfill(6)
    # Do not treat an unmatched firm as a zero-tariff firm.  The exposure
    # file covers firms with an observable US export-weighted tariff measure;
    # unmatched firms have unknown exposure and are excluded from this test.
    work = pair.merge(exposure, on="ticker_key", how="inner")
    work["post_rcep"] = work["post2022"] * work["rcep"]
    work["post_tariff"] = work["post2022"] * work["us_tariff_2019"]
    work["triple"] = work["post_rcep"] * work["us_tariff_2019"]

    specifications = {
        "baseline": ["post_rcep"],
        "post_tariff_control": ["post_rcep", "post_tariff"],
        "full_triple_interaction": ["post_rcep", "post_tariff", "triple"],
    }
    rows = []
    for spec, variables in specifications.items():
        result, data = fit(work, variables, "pair")
        for term in variables:
            rows.append({
                "specification": spec,
                "term": term,
                "coefficient": float(result.params[term]),
                "std_error": float(result.std_errors[term]),
                "p_value": float(result.pvalues[term]),
                "observations": int(result.nobs),
                "pairs": int(data.index.get_level_values("pair_id").nunique()),
                "partner_countries": int(data["partner_country"].nunique()),
                "cluster": "pair",
            })

    # Country-clustered inference is retained as a sensitivity check, not the
    # headline result, because the number of independent policy countries is small.
    result_c, data_c = fit(work, specifications["full_triple_interaction"], "country")
    country_sensitivity = {
        term: {"coefficient": float(result_c.params[term]),
               "std_error": float(result_c.std_errors[term]),
               "p_value": float(result_c.pvalues[term])}
        for term in specifications["full_triple_interaction"]
    }
    result_df = pd.DataFrame(rows)
    result_df.to_csv(TABLES / "exclusion_tariff_triple.csv", index=False)
    triple = result_df[(result_df.specification == "full_triple_interaction") &
                       (result_df.term == "triple")].iloc[0]
    diagnostics = {
        "exposure_source": str(EXPOSURE),
        "exposure_year": 2019,
        "matched_firm_share": float(work["ticker_key"].nunique() / pair["ticker_key"].nunique()),
        "matched_pair_share": float(work["pair_id"].nunique() / pair["pair_id"].nunique()),
        "matched_nonzero_share": float((work["us_tariff_2019"] > 0).mean()),
        "observations": int(triple["observations"]),
        "pairs": int(triple["pairs"]),
        "countries": int(triple["partner_countries"]),
        "pair_cluster": result_df.to_dict("records"),
        "country_cluster_sensitivity": country_sensitivity,
        "interpretation": "The triple interaction tests differential RCEP effects by predetermined US tariff exposure; failure to reject is evidence against, not proof of, a tariff-driven explanation.",
    }
    (TABLES / "exclusion_tariff_triple.json").write_text(
        json.dumps(diagnostics, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Compact paper table: headline RCEP coefficient with and without exposure
    # control, followed by the triple interaction that targets the alternative.
    lookup = {(r["specification"], r["term"]): r for r in rows}
    display = [
        ("基准：Post$\\times$RCEP", lookup[("baseline", "post_rcep")]),
        ("加入Post$\\times$关税暴露", lookup[("post_tariff_control", "post_rcep")]),
        ("三重交互：Post$\\times$RCEP$\\times$关税暴露", lookup[("full_triple_interaction", "triple")]),
    ]
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{关税暴露替代解释检验}",
        r"\label{tab:exclusion}",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        "设定 & 系数 & 标准误 & $p$值 & 观测值 " + r"\\\\",
        r"\midrule",
    ]
    for label, row in display:
        p = "<0.001" if row["p_value"] < 0.001 else f"{row['p_value']:.3f}"
        lines.append(f"{label} & {row['coefficient']:.4f} & {row['std_error']:.4f} & {p} & {int(row['observations']):,} " + r"\\")
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\begin{tablenotes}",
        r"\footnotesize 注：样本限定为能够匹配2019年美国关税暴露的企业—伙伴关系。所有模型包含企业—伙伴关系对固定效应和年份固定效应，标准误聚类于关系对。美国关税暴露为企业层面的出口加权301/232关税暴露；三重交互项用于检验高关税暴露企业是否具有额外的RCEP关系变化。",
        r"\end{tablenotes}",
        r"\end{table}",
    ]
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")
    print(result_df.to_string(index=False))
    print("Country-cluster sensitivity:", country_sensitivity)


if __name__ == "__main__":
    main()
