#!/usr/bin/env python3
"""Audit source schemas without estimating or inspecting outcome effects."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


EXPERIMENT = Path(__file__).resolve().parents[1]
REVISION = EXPERIMENT.parents[1]
WORKSPACE = REVISION.parent
OUT = EXPERIMENT / "logs" / "schema_audit.json"


def find_legacy_root() -> Path:
    for candidate in WORKSPACE.parent.iterdir():
        required = candidate / "data" / "cleaned" / "ddd_panel.parquet"
        links = candidate / "data" / "cleaned" / "cn_global_links.parquet"
        if required.exists() and links.exists():
            return candidate.resolve()
    raise FileNotFoundError("Could not locate the verified legacy data root.")


def parquet_metadata(path: Path) -> dict[str, object]:
    parquet = pq.ParquetFile(path)
    arrow_schema = parquet.schema_arrow
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "rows": parquet.metadata.num_rows,
        "row_groups": parquet.metadata.num_row_groups,
        "columns": [
            {"name": field.name, "type": str(field.type), "nullable": field.nullable}
            for field in arrow_schema
        ],
    }


def main() -> None:
    legacy = find_legacy_root()
    sources = {
        "pair_year": REVISION / "data" / "derived" / "pair_year.parquet",
        "firm_year": legacy / "data" / "cleaned" / "ddd_panel.parquet",
        "relationship_links": legacy / "data" / "cleaned" / "cn_global_links.parquet",
    }
    missing = [str(path) for path in sources.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing registered source files: {missing}")

    industry_fields = ["Indcd", "Indcd1", "Indcd_combined", "Indcat", "gb\u5927\u7c7b"]
    firm_schema = set(pq.ParquetFile(sources["firm_year"]).schema_arrow.names)
    available_industry_fields = [field for field in industry_fields if field in firm_schema]
    firm_fields = pd.read_parquet(
        sources["firm_year"], columns=["Stkcd", "year", *available_industry_fields]
    )
    pre_firm_fields = firm_fields.loc[firm_fields["year"].between(2017, 2019)]
    industry_candidates = {}
    for field in available_industry_fields:
        values = pre_firm_fields[field].dropna().astype(str).str.strip()
        values = values.loc[values.ne("")]
        industry_candidates[field] = {
            "nonmissing_rows_2017_2019": int(len(values)),
            "unique_values_2017_2019": int(values.nunique()),
            "examples": sorted(values.unique().tolist())[:20],
        }

    audit = {
        "audit_type": "schema_only_no_effect_estimates",
        "python": platform.python_version(),
        "packages": {
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "pyarrow": pa.__version__,
        },
        "industry_candidates": industry_candidates,
        "sources": {name: parquet_metadata(path) for name, path in sources.items()},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
