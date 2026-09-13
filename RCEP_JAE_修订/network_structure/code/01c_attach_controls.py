#!/usr/bin/env python3
"""
01c — Attach COMPLETE CSMAR firm controls to the network panel.

The naive firm_year_network.parquet only had a sparse `size_pre` (38.4%).
This script merges the full CSMAR controls via the ticker_key <-> Stkcd bridge.
Controls added: Size, Lev, ROA, Growth, Indcd (industry), Indnme.

Output: data/derived/firm_network_controls.parquet  (firm-year)
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived"
TOP = ROOT.parent.parent   # 项目根 (学习/论文、项目)
OUT.mkdir(parents=True, exist_ok=True)

# CSMAR ddd_panel from the legacy project
DDD = "C:/Users/97328/Desktop/学习/论文、项目/关税冲击对供应链的影响/data/cleaned/ddd_panel.parquet"


def index_controls(ddd: pd.DataFrame) -> pd.DataFrame:
    c = ddd[["Stkcd", "year", "Size", "Lev", "ROA", "Growth", "Indcd", "Indnme",
             "Indcd1", "Indnme1"]].copy()
    c["Stkcd"] = c["Stkcd"].astype(str).str.strip().str.zfill(6)
    c["year"] = c["year"].astype("int64")
    return c


def main():
    net = pd.read_parquet(OUT / "firm_year_network.parquet")
    ddd = pd.read_parquet(DDD)
    ctrl = index_controls(ddd)

    # Bridge: net.ticker_key (6-digit) -> Stkcd
    net["Stkcd"] = net["ticker_key"].astype(str).str.strip().str.zfill(6)
    net["year"] = net["year"].astype("int64")

    # Merge controls on (Stkcd, year)
    merged = net.merge(ctrl, on=["Stkcd", "year"], how="left", validate="many_to_one")
    print(f"After merge: {len(merged)} rows")
    for c in ["Size", "Lev", "ROA", "Growth", "Indcd"]:
        print(f"  {c}: non-null {merged[c].notna().mean():.3f}")

    # Firm-level industry (from Indcd, forward-fill per firm in case of year gaps)
    merged["Indcd"] = merged["Indcd"].astype(str)
    merged["Indcd"] = merged["Indcd"].where(merged["Indcd"].ne("nan") & merged["Indcd"].ne("None"), None)
    # Manufacturing indicator
    merged["manufacturing"] = merged["Indcd"].str.startswith("C").astype(float)
    # Industry code (2-digit for FE)
    merged["gb大类"] = merged["Indcd"].str.extract(r"(\d{1,2})").astype("float")

    # Derive firm-level (time-invariant) values for year-BASED panel where controls constant
    merged = merged.sort_values(["cn_id", "year"])
    for c in ["Size", "Lev", "ROA", "Indcd", "Indnme", "manufacturing", "gb大类"]:
        merged[c] = merged.groupby("cn_id")[c].ffill()

    merged.to_parquet(OUT / "firm_network_controls.parquet", index=False)
    print(f"\nSaved: {OUT / 'firm_network_controls.parquet'}")
    print(f"Shape: {merged.shape}, firms: {merged['cn_id'].nunique()}")

    summary = {
        "rows": int(len(merged)),
        "firms": int(merged["cn_id"].nunique()),
        "size_nonnull": float(merged["Size"].notna().mean()),
        "lev_nonnull": float(merged["Lev"].notna().mean()),
        "roa_nonnull": float(merged["ROA"].notna().mean()),
        "indcd_nonnull": float(merged["Indcd"].notna().mean()),
        "manufacturing_share": float(merged["manufacturing"].mean()),
    }
    (OUT / "1c_controls_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
