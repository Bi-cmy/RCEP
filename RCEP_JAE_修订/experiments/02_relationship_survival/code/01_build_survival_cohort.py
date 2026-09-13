#!/usr/bin/env python3
"""Build the fixed-2017 incumbent supplier-link survival cohort."""

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
STATUS_PATH = EXPERIMENT / "STATUS.json"
RCEP = {"JP", "KR", "AU", "NZ", "ID", "MY", "PH", "SG", "TH", "VN", "BN", "KH", "LA", "MM"}
LATE_2023 = {"ID", "PH"}
ASIA_CONTROLS = {"HK", "TW", "IN", "PK", "BD", "LK", "MN"}
COUNTRIES = RCEP | ASIA_CONTROLS
YEARS = list(range(2017, 2025))
FOLLOW_YEARS = list(range(2018, 2025))


def find_legacy_root() -> Path:
    for candidate in WORKSPACE.parent.iterdir():
        ddd = candidate / "data" / "cleaned" / "ddd_panel.parquet"
        if ddd.exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not locate the verified legacy data root.")


def normalize_ticker(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
    values = values.where(values.str.fullmatch(r"\d{1,6}"), pd.NA)
    return values.str.zfill(6)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    pair_path = REVISION / "data" / "derived" / "pair_year.parquet"
    firm_path = find_legacy_root() / "data" / "cleaned" / "ddd_panel.parquet"
    columns = [
        "cn_id", "partner_id", "partner_country", "supplier_link", "pair_id",
        "year", "active", "ticker_key",
    ]
    pair = pd.read_parquet(pair_path, columns=columns)
    firm = pd.read_parquet(firm_path, columns=["Stkcd", "year"])

    duplicate_pair_year = int(pair.duplicated(["pair_id", "year"]).sum())
    invalid_active = int((~pair["active"].isin([0, 1])).sum())
    invalid_year = int((~pair["year"].isin(YEARS)).sum())
    if duplicate_pair_year or invalid_active or invalid_year:
        raise ValueError(
            f"Source validation failed: duplicate={duplicate_pair_year}, "
            f"invalid_active={invalid_active}, invalid_year={invalid_year}"
        )

    pair["listed_ticker"] = normalize_ticker(pair["ticker_key"])
    firm["listed_ticker"] = normalize_ticker(firm["Stkcd"])
    listed_tickers = set(firm["listed_ticker"].dropna())
    source_rows = len(pair)
    invalid_or_zero_ticker_rows = int(
        (pair["listed_ticker"].isna() | pair["listed_ticker"].eq("000000")).sum()
    )
    nonlisted_ticker_rows = int(
        (
            pair["listed_ticker"].notna()
            & ~pair["listed_ticker"].eq("000000")
            & ~pair["listed_ticker"].isin(listed_tickers)
        ).sum()
    )

    eligible = pair.loc[
        pair["supplier_link"].eq(1)
        & pair["partner_country"].isin(COUNTRIES)
        & pair["listed_ticker"].isin(listed_tickers)
        & ~pair["listed_ticker"].eq("000000")
    ].copy()
    key = ["listed_ticker", "partner_id", "partner_country"]
    collapsed = (
        eligible.groupby(key + ["year"], as_index=False)
        .agg(current_active=("active", "max"), factset_cn_ids=("cn_id", "nunique"))
    )
    duplicate_collapsed = int(collapsed.duplicated(key + ["year"]).sum())
    if duplicate_collapsed:
        raise ValueError(f"Collapsed panel has {duplicate_collapsed} duplicate keys.")

    cohort_keys = collapsed.loc[
        collapsed["year"].eq(2017) & collapsed["current_active"].eq(1), key
    ].drop_duplicates()
    cohort = collapsed.merge(cohort_keys, on=key, how="inner", validate="many_to_one")
    counts_per_relation = cohort.groupby(key)["year"].nunique()
    incomplete_relations = int(counts_per_relation.ne(len(YEARS)).sum())
    if incomplete_relations:
        raise ValueError(f"Cohort has {incomplete_relations} incomplete 2017-2024 histories.")
    if not cohort.loc[cohort["year"].eq(2017), "current_active"].eq(1).all():
        raise ValueError("At least one frozen cohort relationship is not active in 2017.")

    cohort = cohort.sort_values(key + ["year"])
    cohort["survival"] = cohort.groupby(key)["current_active"].cummin().astype("int8")
    cohort["lag_survival"] = cohort.groupby(key)["survival"].shift(1).fillna(1).astype("int8")
    cohort["at_risk"] = cohort["lag_survival"]
    cohort["first_exit"] = (
        cohort["at_risk"].eq(1) & cohort["current_active"].eq(0)
    ).astype("int8")

    cohort["lag_current_active"] = (
        cohort.groupby(key)["current_active"].shift(1).fillna(1).astype("int8")
    )
    cohort["two_absent"] = (
        cohort["current_active"].eq(0) & cohort["lag_current_active"].eq(0)
    ).astype("int8")
    cohort["survival_two_year_grace"] = (
        1 - cohort.groupby(key)["two_absent"].cummax()
    ).astype("int8")

    cohort["rcep"] = cohort["partner_country"].isin(RCEP).astype("int8")
    cohort["entry_year"] = np.where(
        cohort["partner_country"].isin(LATE_2023),
        2023,
        np.where(cohort["rcep"].eq(1), 2022, 9999),
    ).astype("int16")
    cohort["treated_staged"] = (
        cohort["rcep"].eq(1) & cohort["year"].ge(cohort["entry_year"])
    ).astype("int8")
    cohort["treated_uniform"] = (
        cohort["rcep"].eq(1) & cohort["year"].ge(2022)
    ).astype("int8")
    cohort["event_time"] = np.where(
        cohort["rcep"].eq(1), cohort["year"] - cohort["entry_year"], np.nan
    )
    cohort["relationship_id"] = pd.factorize(
        pd.MultiIndex.from_frame(cohort[key]), sort=True
    )[0].astype("int64")
    cohort = cohort.loc[cohort["year"].isin(FOLLOW_YEARS)].copy()

    if cohort.duplicated(key + ["year"]).any():
        raise ValueError("Final survival cohort key is not unique.")
    if (cohort.groupby(key)["survival"].diff().fillna(0) > 0).any():
        raise ValueError("Absorbing survival changes from zero back to one.")

    country_support = (
        cohort.groupby(["partner_country", "rcep", "year"], as_index=False)
        .agg(
            relationships=("relationship_id", "nunique"),
            listed_firms=("listed_ticker", "nunique"),
            survivors=("survival", "sum"),
            at_risk=("at_risk", "sum"),
            first_exits=("first_exit", "sum"),
        )
    )
    group_support = (
        cohort.groupby(["rcep", "year"], as_index=False)
        .agg(
            countries=("partner_country", "nunique"),
            relationships=("relationship_id", "nunique"),
            listed_firms=("listed_ticker", "nunique"),
            survivors=("survival", "sum"),
            at_risk=("at_risk", "sum"),
            first_exits=("first_exit", "sum"),
        )
    )
    baseline_firm_groups = (
        cohort.loc[cohort["year"].eq(2018)]
        .groupby("listed_ticker")["rcep"]
        .agg(has_rcep="max", has_control="min")
        .reset_index()
    )
    baseline_firm_groups["has_control"] = 1 - baseline_firm_groups["has_control"]
    baseline_firm_groups["overlap_group"] = np.select(
        [
            baseline_firm_groups["has_rcep"].eq(1) & baseline_firm_groups["has_control"].eq(1),
            baseline_firm_groups["has_rcep"].eq(1),
        ],
        ["both", "rcep_only"],
        default="control_only",
    )
    overlap = (
        baseline_firm_groups.groupby("overlap_group", as_index=False)
        .agg(listed_firms=("listed_ticker", "nunique"))
    )

    observed_countries = set(cohort["partner_country"].unique())
    absent_rcep = sorted(RCEP - observed_countries)
    absent_controls = sorted(ASIA_CONTROLS - observed_countries)
    relationship_counts = cohort.loc[cohort["year"].eq(2018)].groupby("partner_country")[
        "relationship_id"
    ].nunique()

    DATA.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    cohort = cohort.sort_values(["relationship_id", "year"]).reset_index(drop=True)
    cohort.to_parquet(DATA / "survival_cohort.parquet", index=False)
    country_support.to_csv(DATA / "country_year_support.csv", index=False)
    group_support.to_csv(DATA / "group_year_support.csv", index=False)
    overlap.to_csv(DATA / "within_firm_overlap.csv", index=False)

    summary = {
        "experiment_id": "02_relationship_survival",
        "build_status": "PASSED",
        "python": platform.python_version(),
        "source_hashes": {
            "pair_year_sha256": sha256(pair_path),
            "firm_year_sha256": sha256(firm_path),
        },
        "source_pair_year_rows": int(source_rows),
        "invalid_or_zero_ticker_rows": invalid_or_zero_ticker_rows,
        "nonlisted_ticker_rows": nonlisted_ticker_rows,
        "eligible_asian_supplier_pair_year_rows": int(len(eligible)),
        "collapsed_ticker_partner_country_year_rows": int(len(collapsed)),
        "cohort_relationships": int(cohort["relationship_id"].nunique()),
        "cohort_listed_firms": int(cohort["listed_ticker"].nunique()),
        "follow_up_rows": int(len(cohort)),
        "observed_rcep_countries": sorted(RCEP & observed_countries),
        "observed_control_countries": sorted(ASIA_CONTROLS & observed_countries),
        "absent_rcep_countries": absent_rcep,
        "absent_control_countries": absent_controls,
        "country_relationship_count": {
            country: int(count) for country, count in relationship_counts.items()
        },
        "countries_with_fewer_than_10_relationships": sorted(
            relationship_counts.loc[relationship_counts.lt(10)].index.tolist()
        ),
        "within_firm_overlap": {
            row.overlap_group: int(row.listed_firms) for row in overlap.itertuples(index=False)
        },
        "outputs": [
            "data/survival_cohort.parquet",
            "data/country_year_support.csv",
            "data/group_year_support.csv",
            "data/within_firm_overlap.csv",
        ],
    }
    (DATA / "cohort_build_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (LOGS / "cohort_build.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    sample_path = DATA / "sample_construction.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    sample["status"] = "COMPLETED"
    sample["counts"] = summary
    sample["execution_log"] = "logs/cohort_build.json"
    sample_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    status["phase"] = "DATA_COHORT_BUILT"
    status["next_gate"] = "COUNTRY_SUPPORT_AND_PRETREND_DIAGNOSTICS"
    STATUS_PATH.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
