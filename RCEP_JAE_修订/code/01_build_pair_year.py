#!/usr/bin/env python3
"""Build the real FactSet pair-year panel used by the revised RCEP paper."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived"
AUDIT = ROOT / "audit"
YEARS = np.arange(2017, 2025)
RCEP = {"JP", "KR", "AU", "NZ", "ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"}
LATE_2023 = {"ID", "PH"}
ASIA_NON_RCEP = {"HK", "TW", "IN", "PK", "BD", "LK", "MN"}
OFFSHORE = {"KY", "BM", "VG", "JE", "IM", "GG", "MH"}


def find_legacy_root() -> Path:
    configured = os.environ.get("RCEP_LEGACY_ROOT")
    if configured:
        return Path(configured).resolve()
    for candidate in ROOT.parent.parent.iterdir():
        if (candidate / "data" / "cleaned" / "cn_global_links.parquet").exists():
            return candidate
    raise FileNotFoundError("Set RCEP_LEGACY_ROOT to the earlier project directory.")


def chinese_side_fields(df: pd.DataFrame) -> pd.DataFrame:
    source_is_cn = df["cn_side"].eq("source")
    df["cn_id"] = np.where(source_is_cn, df["source_company_id"], df["target_company_id"])
    df["partner_id"] = np.where(source_is_cn, df["target_company_id"], df["source_company_id"])
    df["cn_ticker"] = np.where(source_is_cn, df["SOURCE_ticker"], df["TARGET_ticker"])

    # FactSet CUSTOMER means the source sells to the target. This indicator is
    # one when the foreign partner supplies the Chinese firm.
    df["supplier_link"] = (
        (source_is_cn & df["rel_type"].eq("SUPPLIER"))
        | (~source_is_cn & df["rel_type"].eq("CUSTOMER"))
    ).astype("int8")
    return df


def build_panel(links: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    links = links[
        links["rel_type"].isin(["CUSTOMER", "SUPPLIER"])
        & links["cn_side"].isin(["source", "target"])
    ].copy()
    links["partner_country"] = links["partner_country"].fillna("").astype(str).str.strip().str.upper()
    links = links[
        links["partner_country"].str.fullmatch(r"[A-Z]{2}")
        & ~links["partner_country"].isin(["CN", "XZ"])
    ].copy()
    links = chinese_side_fields(links)
    links["start_dt"] = pd.to_datetime(links["start_dt"], errors="coerce")
    links["end_dt"] = pd.to_datetime(links["end_dt"], errors="coerce")
    links = links.dropna(subset=["start_dt", "end_dt", "cn_id", "partner_id"])

    key = ["cn_id", "partner_id", "partner_country", "supplier_link"]
    pair_info = (
        links.groupby(key, as_index=False)
        .agg(
            first_start=("start_dt", "min"),
            last_end=("end_dt", "max"),
            cn_ticker=("cn_ticker", "first"),
            revenue_percent=("revenue_percent", "max"),
            episode_count=("start_dt", "size"),
        )
    )
    pair_info["pair_id"] = np.arange(len(pair_info), dtype="int64")
    links = links.merge(pair_info[key + ["pair_id"]], on=key, how="left", validate="many_to_one")

    expanded = links[["pair_id", "start_dt", "end_dt"]].merge(
        pd.DataFrame({"year": YEARS}), how="cross"
    )
    year_end = pd.to_datetime(expanded["year"].astype(str) + "-12-31")
    expanded["active"] = (
        expanded["start_dt"].le(year_end) & expanded["end_dt"].ge(year_end)
    ).astype("int8")
    active = expanded.groupby(["pair_id", "year"], as_index=False)["active"].max()

    panel = pair_info.merge(pd.DataFrame({"year": YEARS}), how="cross")
    panel = panel.merge(active, on=["pair_id", "year"], how="left", validate="one_to_one")
    panel["active"] = panel["active"].fillna(0).astype("int8")
    panel["rcep"] = panel["partner_country"].isin(RCEP).astype("int8")
    panel["post2022"] = panel["year"].ge(2022).astype("int8")
    panel["treated_uniform"] = (panel["rcep"] * panel["post2022"]).astype("int8")
    panel["entry_year"] = np.where(panel["partner_country"].isin(LATE_2023), 2023, 2022)
    panel["treated_staged"] = (panel["rcep"].eq(1) & panel["year"].ge(panel["entry_year"])).astype("int8")
    panel["asia_control"] = panel["partner_country"].isin(ASIA_NON_RCEP).astype("int8")
    panel["offshore"] = panel["partner_country"].isin(OFFSHORE).astype("int8")

    active_2021 = panel.loc[panel["year"].eq(2021), ["pair_id", "active"]].rename(
        columns={"active": "active_2021"}
    )
    pair_info = pair_info.merge(active_2021, on="pair_id", how="left")
    pair_info["age_2021"] = np.where(
        pair_info["active_2021"].eq(1),
        (pd.Timestamp("2021-12-31") - pair_info["first_start"]).dt.days / 365.25,
        0.0,
    )
    pair_info["age_2021"] = pair_info["age_2021"].clip(lower=0)

    sourcing_2021 = pair_info[
        pair_info["active_2021"].eq(1)
        & pair_info["supplier_link"].eq(1)
        & pair_info["partner_country"].isin(RCEP)
    ]
    breadth = sourcing_2021.groupby("cn_id")["partner_country"].nunique().rename("rcep_breadth_2021")
    pair_info = pair_info.merge(breadth, on="cn_id", how="left")
    pair_info["rcep_breadth_2021"] = pair_info["rcep_breadth_2021"].fillna(0).astype("int16")
    pair_info["multi_rcep_2021"] = pair_info["rcep_breadth_2021"].ge(2).astype("int8")

    panel = panel.drop(columns=["active_2021"], errors="ignore").merge(
        pair_info[["pair_id", "active_2021", "age_2021", "rcep_breadth_2021", "multi_rcep_2021"]],
        on="pair_id",
        how="left",
        validate="many_to_one",
    )
    return panel.sort_values(["pair_id", "year"]), links


def attach_pre_treatment_characteristics(panel: pd.DataFrame, legacy: Path) -> pd.DataFrame:
    ddd = pd.read_parquet(legacy / "data" / "cleaned" / "ddd_panel.parquet")
    ddd["ticker_key"] = ddd["Stkcd"].astype(str).str.strip().str.zfill(6)
    pre = ddd[ddd["year"].le(2021)].groupby("ticker_key", as_index=False).agg(size_pre=("Size", "mean"))
    pre_industry = (
        ddd.loc[ddd["year"].le(2021)]
        .sort_values(["ticker_key", "year"])
        .groupby("ticker_key", as_index=False)
        .tail(1)[["ticker_key", "Indcd1", "Indcd_combined"]]
    )
    industry_code = pre_industry["Indcd1"].fillna(pre_industry["Indcd_combined"])
    pre_industry["manufacturing_pre"] = np.where(
        industry_code.notna(), industry_code.astype(str).str.startswith("C"), np.nan
    )
    pre = pre.merge(
        pre_industry[["ticker_key", "manufacturing_pre"]],
        on="ticker_key", how="left", validate="one_to_one",
    )
    panel["ticker_key"] = panel["cn_ticker"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(6)
    panel = panel.merge(pre, on="ticker_key", how="left", validate="many_to_one")
    median_size = panel.loc[panel["size_pre"].notna(), ["pair_id", "size_pre"]].drop_duplicates()["size_pre"].median()
    panel["large_firm"] = np.where(panel["size_pre"].notna(), panel["size_pre"].ge(median_size), np.nan)
    return panel


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    legacy = find_legacy_root()
    source = legacy / "data" / "cleaned" / "cn_global_links.parquet"
    raw = pd.read_parquet(source)
    panel, episodes = build_panel(raw)
    panel = attach_pre_treatment_characteristics(panel, legacy)

    panel.to_parquet(OUT / "pair_year.parquet", index=False)
    validation = (
        panel.groupby(["year", "rcep"], as_index=False)
        .agg(active_links=("active", "sum"), pairs=("pair_id", "nunique"), firms=("cn_id", "nunique"))
    )
    validation.to_csv(OUT / "pair_year_validation.csv", index=False)

    summary = {
        "source": str(source),
        "raw_rows": int(len(raw)),
        "eligible_episode_rows": int(len(episodes)),
        "pair_roles": int(panel["pair_id"].nunique()),
        "panel_rows": int(len(panel)),
        "years": [int(YEARS.min()), int(YEARS.max())],
        "partner_countries": int(panel["partner_country"].nunique()),
        "rcep_pair_roles": int(panel.loc[panel["rcep"].eq(1), "pair_id"].nunique()),
        "multi_rcep_firms_2021": int(panel.loc[panel["multi_rcep_2021"].eq(1), "cn_id"].nunique()),
        "revenue_percent_nonmissing_pairs": int(
            panel[["pair_id", "revenue_percent"]].drop_duplicates()["revenue_percent"].notna().sum()
        ),
        "size_match_rate_pairs": float(
            panel[["pair_id", "size_pre"]].drop_duplicates()["size_pre"].notna().mean()
        ),
    }
    (AUDIT / "panel_build_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
