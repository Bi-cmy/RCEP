#!/usr/bin/env python3
"""Document FactSet ID to listed-ticker mapping cardinality."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


EXPERIMENT = Path(__file__).resolve().parents[1]
REVISION = EXPERIMENT.parents[1]
WORKSPACE = REVISION.parent


def find_legacy_root() -> Path:
    for candidate in WORKSPACE.parent.iterdir():
        path = candidate / "data" / "cleaned" / "ddd_panel.parquet"
        if path.exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not locate the verified legacy data root.")


def normalize_ticker(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
    values = values.where(values.str.fullmatch(r"\d{1,6}"), pd.NA)
    return values.str.zfill(6)


def main() -> None:
    pair = pd.read_parquet(
        REVISION / "data" / "derived" / "pair_year.parquet",
        columns=["cn_id", "ticker_key"],
    ).drop_duplicates()
    firm = pd.read_parquet(
        find_legacy_root() / "data" / "cleaned" / "ddd_panel.parquet",
        columns=["Stkcd"],
    )
    pair["ticker"] = normalize_ticker(pair["ticker_key"])
    firm["ticker"] = normalize_ticker(firm["Stkcd"])
    valid = pair.dropna(subset=["cn_id", "ticker"])[["cn_id", "ticker"]].drop_duplicates()
    cn_degree = valid.groupby("cn_id")["ticker"].nunique()
    ticker_degree = valid.groupby("ticker")["cn_id"].nunique().sort_values(ascending=False)
    firm_tickers = set(firm["ticker"].dropna())

    top = ticker_degree.head(100).rename("factset_cn_ids").reset_index()
    top["in_firm_panel"] = top["ticker"].isin(firm_tickers)
    top.to_csv(EXPERIMENT / "data" / "mapping_many_to_one_top.csv", index=False)

    quantiles = ticker_degree.quantile([0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1.0])
    audit = {
        "valid_cn_id_ticker_pairs": int(len(valid)),
        "unique_cn_ids": int(valid["cn_id"].nunique()),
        "unique_tickers": int(valid["ticker"].nunique()),
        "cn_ids_linked_to_one_ticker": int(cn_degree.eq(1).sum()),
        "cn_ids_linked_to_multiple_tickers": int(cn_degree.gt(1).sum()),
        "tickers_linked_to_one_cn_id": int(ticker_degree.eq(1).sum()),
        "tickers_linked_to_multiple_cn_ids": int(ticker_degree.gt(1).sum()),
        "valid_tickers_found_in_firm_panel": int(pd.Index(valid["ticker"].unique()).isin(firm_tickers).sum()),
        "cn_ids_per_ticker_quantiles": {str(index): float(value) for index, value in quantiles.items()},
        "interpretation": "Multiple FactSet cn_ids sharing one listed ticker can be aggregated at ticker level; cn_ids linked to multiple listed tickers are genuinely ambiguous for this design.",
    }
    path = EXPERIMENT / "logs" / "mapping_cardinality.json"
    path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
