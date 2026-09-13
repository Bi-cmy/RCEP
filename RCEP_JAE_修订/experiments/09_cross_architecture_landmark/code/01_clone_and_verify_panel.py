#!/usr/bin/env python3
"""Clone Experiment 07's candidate panel and reproduce known support exactly."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


EXPERIMENT = Path(__file__).resolve().parents[1]
SOURCE = EXPERIMENT.parent / "07_fta_novelty" / "data" / "architecture_firm_year.parquet"
DATA = EXPERIMENT / "data"
LOGS = EXPERIMENT / "logs"
STATUS = EXPERIMENT / "STATUS.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    panel = pd.read_parquet(SOURCE)
    required = {
        "listed_ticker", "year", "architecture_count", "multi_architecture",
        "asinh_active_rcep_supplier_links", "asinh_active_rcep_supplier_countries",
        "rcep_asian_supplier_share", "pre_industry", "size_tercile",
        "permutation_stratum", "firm_id", "industry_year_id",
    }
    if required - set(panel.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(panel.columns))}")
    if panel.duplicated(["listed_ticker", "year"]).any():
        raise ValueError("Candidate panel key is not unique.")
    firms = int(panel["listed_ticker"].nunique())
    rows = int(len(panel))
    exposed = int(panel.drop_duplicates("listed_ticker")["architecture_count"].ge(1).sum())
    multi = int(panel.drop_duplicates("listed_ticker")["multi_architecture"].sum())
    minimum_positive = int(
        panel.groupby("year")["asinh_active_rcep_supplier_links"].apply(lambda x: x.gt(0).sum()).min()
    )
    exact_replication = firms == 2556 and rows == 12780 and exposed == 261 and multi == 52
    support_pass = exact_replication and firms >= 2000 and exposed >= 250 and multi >= 40 and minimum_positive >= 100
    if not exact_replication:
        raise ValueError("Known Experiment 07 support counts were not reproduced exactly.")
    DATA.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    output = DATA / "architecture_landmark_panel.parquet"
    panel.to_parquet(output, index=False)
    result = {
        "experiment_id": "09_cross_architecture_landmark",
        "gate": "SUPPORT_REPLICATION",
        "gate_pass": bool(support_pass),
        "source_sha256": sha256(SOURCE),
        "output_sha256": sha256(output),
        "rows": rows,
        "firms": firms,
        "firms_with_one_or_more_architectures": exposed,
        "firms_with_two_or_more_architectures": multi,
        "minimum_annual_positive_primary_outcome": minimum_positive,
        "exact_known_count_replication": exact_replication,
    }
    (DATA / "support_replication.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (LOGS / "support_replication.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    sample_path = DATA / "sample_construction.json"
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    sample["status"] = "COMPLETED"
    sample["counts"] = result
    sample_path.write_text(json.dumps(sample, indent=2), encoding="utf-8")
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    status["phase"] = "SUPPORT_REPLICATION_RUN"
    status["support_replication_pass"] = bool(support_pass)
    status["next_gate"] = "PRETREND" if support_pass else "ARCHIVE_FAILURE"
    STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
