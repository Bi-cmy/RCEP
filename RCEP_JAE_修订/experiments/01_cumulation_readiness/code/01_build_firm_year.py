#!/usr/bin/env python3
"""Build the frozen firm-year panel for Experiment 01."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd


EXPERIMENT = Path(__file__).resolve().parents[1]
REVISION = EXPERIMENT.parents[1]
WORKSPACE = REVISION.parent
DATA = EXPERIMENT / "data"
LOGS = EXPERIMENT / "logs"
STATUS = EXPERIMENT / "STATUS.json"
YEARS = list(range(2017, 2025))
PRE_YEARS = [2017, 2018, 2019]


def find_legacy_root() -> Path:
    for candidate in WORKSPACE.parent.iterdir():
        ddd = candidate / "data" / "cleaned" / "ddd_panel.parquet"
        links = candidate / "data" / "cleaned" / "cn_global_links.parquet"
        if ddd.exists() and links.exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not locate the verified legacy data root.")


def normalize_ticker(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
    values = values.where(values.str.fullmatch(r"\d{1,6}"), pd.NA)
    return values.str.zfill(6)


def stable_mode(series: pd.Series) -> object:
    values = series.dropna().astype(str).str.strip()
    values = values.loc[values.ne("")]
    if values.empty:
        return pd.NA
    counts = values.value_counts()
    return sorted(counts.loc[counts.eq(counts.max())].index)[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_pair_year(pair: pd.DataFrame) -> dict[str, int]:
    required = {
        "cn_id", "partner_id", "partner_country", "supplier_link", "pair_id",
        "year", "active", "rcep", "ticker_key",
    }
    missing = sorted(required.difference(pair.columns))
    if missing:
        raise ValueError(f"pair_year is missing required fields: {missing}")
    duplicate_keys = int(pair.duplicated(["pair_id", "year"]).sum())
    invalid_years = int((~pair["year"].isin(YEARS)).sum())
    invalid_active = int((~pair["active"].isin([0, 1])).sum())
    invalid_supplier = int((~pair["supplier_link"].isin([0, 1])).sum())
    invalid_rcep = int((~pair["rcep"].isin([0, 1])).sum())
    invalid_country = int(
        (~pair["partner_country"].astype("string").str.fullmatch(r"[A-Z]{2}", na=False)).sum()
    )
    failures = {
        "duplicate_pair_year_keys": duplicate_keys,
        "invalid_year_rows": invalid_years,
        "invalid_active_rows": invalid_active,
        "invalid_supplier_rows": invalid_supplier,
        "invalid_rcep_rows": invalid_rcep,
        "invalid_partner_country_rows": invalid_country,
    }
    if any(failures.values()):
        raise ValueError(f"Pair-year validation failed: {failures}")
    return failures


def build_mapping(pair: pd.DataFrame, firm: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    pair_map = pair[["cn_id", "ticker_key"]].drop_duplicates().copy()
    pair_map["ticker"] = normalize_ticker(pair_map["ticker_key"])
    valid = pair_map.dropna(subset=["cn_id", "ticker"])[["cn_id", "ticker"]].drop_duplicates()
    cn_degree = valid.groupby("cn_id")["ticker"].nunique()
    ticker_degree = valid.groupby("ticker")["cn_id"].nunique()
    mapping = valid.loc[
        valid["cn_id"].map(cn_degree).eq(1) & valid["ticker"].map(ticker_degree).eq(1)
    ].drop_duplicates()

    firm = firm.copy()
    firm["ticker"] = normalize_ticker(firm["Stkcd"])
    bad_firm_ticker = int(firm["ticker"].isna().sum())
    duplicate_firm_year = int(firm.dropna(subset=["ticker"]).duplicated(["ticker", "year"]).sum())
    if duplicate_firm_year:
        raise ValueError(f"Firm-year source has {duplicate_firm_year} duplicate ticker-year keys.")
    firm = firm.dropna(subset=["ticker"])
    available_tickers = set(firm["ticker"])
    mapping["in_firm_panel"] = mapping["ticker"].isin(available_tickers)
    eligible = mapping.loc[mapping["in_firm_panel"], ["cn_id", "ticker"]].copy()

    audit = pd.DataFrame(
        [
            ("pair_year_unique_cn_ids", pair["cn_id"].nunique()),
            ("cn_ids_with_valid_six_digit_ticker", valid["cn_id"].nunique()),
            ("one_to_one_cn_id_ticker_mappings", mapping["cn_id"].nunique()),
            ("mappings_found_in_firm_panel", eligible["cn_id"].nunique()),
            ("invalid_firm_year_ticker_rows", bad_firm_ticker),
            ("duplicate_firm_year_keys", duplicate_firm_year),
        ],
        columns=["metric", "count"],
    )
    counts = {row.metric: int(row.count) for row in audit.itertuples(index=False)}
    return eligible, audit, counts


def construct_pre_characteristics(firm: pd.DataFrame, eligible: pd.DataFrame) -> pd.DataFrame:
    pre = firm.loc[firm["year"].isin(PRE_YEARS)].merge(
        eligible, on="ticker", how="inner", validate="many_to_one"
    )
    observed = (
        pre.groupby(["cn_id", "ticker"], as_index=False)
        .agg(
            industry_pre=("Indcat", stable_mode),
            size_pre=("Size", "mean"),
            pre_firm_years=("year", "nunique"),
        )
    )
    characteristics = eligible.merge(
        observed, on=["cn_id", "ticker"], how="left", validate="one_to_one"
    )
    characteristics["pre_firm_years"] = characteristics["pre_firm_years"].fillna(0).astype("int8")
    q1, q2 = characteristics["size_pre"].quantile([1 / 3, 2 / 3]).tolist()
    conditions = [
        characteristics["size_pre"].le(q1),
        characteristics["size_pre"].gt(q1) & characteristics["size_pre"].le(q2),
        characteristics["size_pre"].gt(q2),
    ]
    characteristics["size_tercile"] = np.select(
        conditions, ["LOW", "MID", "HIGH"], default="UNKNOWN"
    )
    characteristics["industry_pre"] = characteristics["industry_pre"].fillna("UNKNOWN")
    characteristics["permutation_stratum"] = (
        characteristics["industry_pre"].astype(str)
        + "__"
        + characteristics["size_tercile"].astype(str)
    )
    characteristics.attrs["size_tercile_cutoffs"] = [float(q1), float(q2)]
    return characteristics


def construct_outcomes(pair: pd.DataFrame, eligible_ids: set[str]) -> pd.DataFrame:
    supplier = pair.loc[
        pair["cn_id"].isin(eligible_ids)
        & pair["supplier_link"].eq(1)
        & pair["rcep"].eq(1)
    ].copy()
    supplier = supplier.sort_values(["pair_id", "year"])
    supplier["lag_active"] = supplier.groupby("pair_id")["active"].shift(1)
    supplier["exit_risk"] = supplier["lag_active"].eq(1).astype("int8")
    supplier["exit"] = (supplier["lag_active"].eq(1) & supplier["active"].eq(0)).astype("int8")

    first_link_year = (
        supplier.loc[supplier["active"].eq(1)]
        .groupby("pair_id")["year"]
        .min()
        .rename("first_link_active_year")
    )
    supplier = supplier.merge(first_link_year, on="pair_id", how="left", validate="many_to_one")
    supplier["first_link_entry"] = (
        supplier["active"].eq(1) & supplier["year"].eq(supplier["first_link_active_year"])
    ).astype("int8")

    link_year = (
        supplier.groupby(["cn_id", "year"], as_index=False)
        .agg(
            active_rcep_supplier_links=("active", "sum"),
            incumbent_link_risk_set=("exit_risk", "sum"),
            exited_incumbent_links=("exit", "sum"),
            first_rcep_supplier_link_entries=("first_link_entry", "sum"),
        )
    )

    country_year = (
        supplier.groupby(["cn_id", "partner_country", "year"], as_index=False)["active"]
        .max()
        .sort_values(["cn_id", "partner_country", "year"])
    )
    first_country_year = (
        country_year.loc[country_year["active"].eq(1)]
        .groupby(["cn_id", "partner_country"])["year"]
        .min()
        .rename("first_country_active_year")
    )
    country_year = country_year.merge(
        first_country_year,
        on=["cn_id", "partner_country"],
        how="left",
        validate="many_to_one",
    )
    country_year["first_country_entry"] = (
        country_year["active"].eq(1)
        & country_year["year"].eq(country_year["first_country_active_year"])
    ).astype("int8")
    country_entries = (
        country_year.groupby(["cn_id", "year"], as_index=False)["first_country_entry"]
        .sum()
        .rename(columns={"first_country_entry": "first_rcep_supplier_country_entries"})
    )

    active_by_country = (
        supplier.loc[supplier["active"].eq(1)]
        .groupby(["cn_id", "year", "partner_country"], as_index=False)
        .size()
        .rename(columns={"size": "country_link_count"})
    )
    active_by_country["link_total"] = active_by_country.groupby(
        ["cn_id", "year"]
    )["country_link_count"].transform("sum")
    active_by_country["share"] = (
        active_by_country["country_link_count"] / active_by_country["link_total"]
    )
    active_by_country["entropy_part"] = -active_by_country["share"] * np.log(
        active_by_country["share"]
    )
    active_by_country["hhi_part"] = active_by_country["share"].pow(2)
    diversity = (
        active_by_country.groupby(["cn_id", "year"], as_index=False)
        .agg(
            active_rcep_supplier_countries=("partner_country", "nunique"),
            supplier_country_entropy=("entropy_part", "sum"),
            supplier_country_hhi=("hhi_part", "sum"),
        )
    )
    return link_year.merge(country_entries, on=["cn_id", "year"], how="outer").merge(
        diversity, on=["cn_id", "year"], how="outer"
    )


def main() -> None:
    legacy = find_legacy_root()
    pair_path = REVISION / "data" / "derived" / "pair_year.parquet"
    firm_path = legacy / "data" / "cleaned" / "ddd_panel.parquet"
    pair = pd.read_parquet(pair_path)
    firm = pd.read_parquet(firm_path, columns=["Stkcd", "year", "Size", "Indcat"])

    validation = validate_pair_year(pair)
    eligible, mapping_audit, mapping_counts = build_mapping(pair, firm)
    if eligible.empty:
        raise ValueError("No one-to-one FactSet-to-firm-panel mappings passed the data gate.")

    firm["ticker"] = normalize_ticker(firm["Stkcd"])
    firm = firm.loc[firm["year"].isin(YEARS) & firm["ticker"].notna()].copy()
    pre_chars = construct_pre_characteristics(firm, eligible)
    size_tercile_cutoffs = pre_chars.attrs["size_tercile_cutoffs"]

    readiness = (
        pair.loc[
            pair["cn_id"].isin(set(eligible["cn_id"]))
            & pair["supplier_link"].eq(1)
            & pair["rcep"].eq(1)
            & pair["active"].eq(1)
            & pair["year"].isin(PRE_YEARS)
        ]
        .groupby("cn_id")["partner_country"]
        .nunique()
        .rename("readiness_countries")
    )
    pre_chars = pre_chars.merge(readiness, on="cn_id", how="left", validate="one_to_one")
    pre_chars["readiness_countries"] = pre_chars["readiness_countries"].fillna(0).astype("int16")
    pre_chars["readiness_2plus"] = pre_chars["readiness_countries"].ge(2).astype("int8")
    pre_chars["readiness_group"] = np.select(
        [pre_chars["readiness_countries"].eq(0), pre_chars["readiness_countries"].eq(1)],
        ["0", "1"],
        default="2plus",
    )

    base = firm.merge(eligible, on="ticker", how="inner", validate="many_to_one")
    base = base.merge(
        pre_chars.drop(columns=["ticker"]), on="cn_id", how="inner", validate="many_to_one"
    )
    outcomes = construct_outcomes(pair, set(pre_chars["cn_id"]))
    panel = base.merge(outcomes, on=["cn_id", "year"], how="left", validate="one_to_one")

    zero_columns = [
        "active_rcep_supplier_links",
        "incumbent_link_risk_set",
        "exited_incumbent_links",
        "first_rcep_supplier_link_entries",
        "first_rcep_supplier_country_entries",
        "active_rcep_supplier_countries",
        "supplier_country_entropy",
    ]
    panel[zero_columns] = panel[zero_columns].fillna(0)
    count_columns = [column for column in zero_columns if column != "supplier_country_entropy"]
    panel[count_columns] = panel[count_columns].astype("int32")
    panel["exit_rate"] = np.where(
        panel["incumbent_link_risk_set"].gt(0),
        panel["exited_incumbent_links"] / panel["incumbent_link_risk_set"],
        np.nan,
    )
    panel["net_rcep_supplier_link_growth"] = (
        panel["first_rcep_supplier_link_entries"] - panel["exited_incumbent_links"]
    ).astype("float64")
    transition_columns = [
        "exit_rate",
        "first_rcep_supplier_link_entries",
        "first_rcep_supplier_country_entries",
        "net_rcep_supplier_link_growth",
    ]
    panel.loc[panel["year"].eq(2017), transition_columns] = np.nan
    panel.loc[panel["active_rcep_supplier_links"].eq(0), "supplier_country_hhi"] = np.nan
    panel["post2022"] = panel["year"].ge(2022).astype("int8")

    duplicate_panel_keys = int(panel.duplicated(["cn_id", "year"]).sum())
    if duplicate_panel_keys:
        raise ValueError(f"Derived panel has {duplicate_panel_keys} duplicate firm-year keys.")
    if not panel.groupby("cn_id")["readiness_countries"].nunique().eq(1).all():
        raise ValueError("Frozen readiness exposure varies within firm.")

    stratum_sizes = pre_chars["permutation_stratum"].value_counts()
    exposure_distribution = (
        pre_chars.groupby(["readiness_countries", "readiness_group"], as_index=False)
        .agg(firms=("cn_id", "nunique"))
        .sort_values("readiness_countries")
    )
    support = (
        panel.groupby(["year", "readiness_group"], as_index=False)
        .agg(
            firms=("cn_id", "nunique"),
            exit_rate_nonmissing=("exit_rate", "count"),
            hhi_nonmissing=("supplier_country_hhi", "count"),
            incumbent_link_risk_set=("incumbent_link_risk_set", "sum"),
            active_rcep_supplier_links=("active_rcep_supplier_links", "sum"),
        )
    )

    DATA.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    panel = panel.sort_values(["cn_id", "year"]).reset_index(drop=True)
    panel.to_parquet(DATA / "firm_year.parquet", index=False)
    exposure_distribution.to_csv(DATA / "exposure_distribution.csv", index=False)
    support.to_csv(DATA / "outcome_support_by_year_group.csv", index=False)
    mapping_audit.to_csv(DATA / "mapping_audit.csv", index=False)

    summary = {
        "experiment_id": "01_cumulation_readiness",
        "build_status": "PASSED",
        "python": platform.python_version(),
        "source_hashes": {
            "pair_year_sha256": sha256(pair_path),
            "firm_year_sha256": sha256(firm_path),
        },
        "pair_year_rows": int(len(pair)),
        "pair_roles": int(pair["pair_id"].nunique()),
        "pair_year_validation": validation,
        "mapping": mapping_counts,
        "derived_rows": int(len(panel)),
        "derived_firms": int(panel["cn_id"].nunique()),
        "years": [int(panel["year"].min()), int(panel["year"].max())],
        "readiness": {
            "zero_firms": int(pre_chars["readiness_countries"].eq(0).sum()),
            "one_firms": int(pre_chars["readiness_countries"].eq(1).sum()),
            "two_plus_firms": int(pre_chars["readiness_countries"].ge(2).sum()),
            "maximum": int(pre_chars["readiness_countries"].max()),
        },
        "pre_policy_characteristics": {
            "industry_field": "Indcat",
            "industry_groups": int(pre_chars["industry_pre"].nunique()),
            "size_tercile_cutoffs": size_tercile_cutoffs,
            "permutation_strata": int(len(stratum_sizes)),
            "firms_in_singleton_strata": int(stratum_sizes.eq(1).sum()),
        },
        "missingness": {
            "exit_rate": float(panel["exit_rate"].isna().mean()),
            "supplier_country_hhi": float(panel["supplier_country_hhi"].isna().mean()),
        },
        "outputs": [
            "data/firm_year.parquet",
            "data/exposure_distribution.csv",
            "data/outcome_support_by_year_group.csv",
            "data/mapping_audit.csv",
        ],
    }
    (DATA / "panel_build_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (LOGS / "panel_build.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    sample_log_path = DATA / "sample_construction.json"
    sample_log = json.loads(sample_log_path.read_text(encoding="utf-8"))
    sample_log["status"] = "COMPLETED"
    sample_log["source_counts"] = {
        "pair_year_rows": int(len(pair)),
        "pair_year_firms": int(pair["cn_id"].nunique()),
        "firm_year_rows": int(len(firm)),
        "firm_year_firms": int(firm["ticker"].nunique()),
    }
    step_values = [
        (len(pair), len(pair), pair["cn_id"].nunique()),
        (len(pair), len(pair), pair["cn_id"].nunique()),
        (pair["cn_id"].nunique(), len(eligible), eligible["cn_id"].nunique()),
        (len(pre_chars), len(pre_chars), pre_chars["cn_id"].nunique()),
        (len(panel), len(panel), panel["cn_id"].nunique()),
        (len(base), len(panel), panel["cn_id"].nunique()),
        (len(panel), len(panel), panel["cn_id"].nunique()),
    ]
    for step, values in zip(sample_log["steps"], step_values, strict=True):
        step["rows_before"], step["rows_after"], step["firms_after"] = map(int, values)
    sample_log["execution_log"] = "logs/panel_build.json"
    sample_log_path.write_text(json.dumps(sample_log, indent=2), encoding="utf-8")

    status = json.loads(STATUS.read_text(encoding="utf-8"))
    status["phase"] = "DATA_PANEL_BUILT"
    status["results_inspected"] = False
    status["next_gate"] = "DESCRIPTIVES_OVERLAP_AND_EVENT_STUDY"
    STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
