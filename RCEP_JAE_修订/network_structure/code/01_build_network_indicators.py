#!/usr/bin/env python3
"""
01 — Build firm-year supply-chain NETWORK STRUCTURE indicators from the
verified pair_year panel. Produces a firm-year panel with:

  RCEP_share        share of active links with RCEP members
  Regional_HHI      Herfindahl of partner-country shares (regional concentration)
  Entropy           Shannon entropy of partner-country shares (diversification)
  N_countries       number of partner countries
  N_RCEP_countries  number of RCEP member countries
  N_links           total active links (scale control)
  + baseline (2017-2021) mean exposure for continuous treatment.

All indicators are built from ACTIVE links only (active == 1) at each firm-year.
Uses the verified ../data/derived/pair_year.parquet as source.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]                    # network_structure/
TOP = ROOT.parent                                             # RCEP_JAE_修订/
OUT = ROOT / "data" / "derived"
OUT.mkdir(parents=True, exist_ok=True)

RCEP = {"JP","KR","AU","NZ","BN","KH","ID","LA","MY","MM","PH","SG","TH","VN"}
YEARS = np.arange(2017, 2025)


def build_firm_year(panel: pd.DataFrame) -> pd.DataFrame:
    # Keep active links only
    act = panel[panel["active"].eq(1)].copy()

    # Firm-year totals by partner country
    cy = act.groupby(["cn_id", "year", "partner_country"], as_index=False).agg(n=("pair_id", "count"))
    fy = cy.groupby(["cn_id", "year"], as_index=False).agg(N_links=("n", "sum"))

    # RCEP share of links
    cy["is_rcep"] = cy["partner_country"].isin(RCEP).astype(int)
    rcep_share = cy.groupby(["cn_id", "year"], as_index=False)["is_rcep"].sum()
    rcep_share = rcep_share.rename(columns={"is_rcep": "N_RCEP_links"})
    fy = fy.merge(rcep_share, on=["cn_id", "year"], how="left")
    fy["N_RCEP_links"] = fy["N_RCEP_links"].fillna(0)
    fy["RCEP_share"] = fy["N_RCEP_links"] / fy["N_links"].where(fy["N_links"] > 0, np.nan)

    # Country shares for HHI / entropy
    cy["share"] = cy["n"] / cy.groupby(["cn_id", "year"])["n"].transform("sum")
    cy["share_sq"] = cy["share"] ** 2
    cy["log_share"] = cy["share"] * np.log(cy["share"])   # entropy term; 0*log0 treated as 0
    cy["log_share"] = cy["log_share"].where(cy["share"] > 0, 0.0)

    hhi = cy.groupby(["cn_id", "year"], as_index=False)["share_sq"].sum().rename(columns={"share_sq": "Regional_HHI"})
    entropy = cy.groupby(["cn_id", "year"], as_index=False)["log_share"].sum().rename(columns={"log_share": "Entropy_neg"})
    entropy["Entropy"] = -entropy["Entropy_neg"]
    n_countries = cy.groupby(["cn_id", "year"], as_index=False).agg(
        N_countries=("partner_country", "nunique"),
        N_RCEP_countries=("partner_country", lambda x: x[x.isin(RCEP)].nunique()),
    )

    fy = fy.merge(hhi, on=["cn_id", "year"], how="left")
    fy = fy.merge(entropy[["cn_id", "year", "Entropy"]], on=["cn_id", "year"], how="left")
    fy = fy.merge(n_countries, on=["cn_id", "year"], how="left")

    # Fill zeros for firms with no active links that year (still in panel)
    # We keep firm-years present in the panel; missing indicators -> set to sentinel then decide
    return fy


def attach_baseline(panel: pd.DataFrame, fy: pd.DataFrame) -> pd.DataFrame:
    # Baseline exposure from 2017-2021 mean RCEP_share (continuous treatment intensity)
    base = fy[fy["year"].between(2017, 2021)].groupby("cn_id", as_index=False)["RCEP_share"].mean()
    base = base.rename(columns={"RCEP_share": "RCEP_Exposure_base"})
    fy = fy.merge(base, on="cn_id", how="left")
    return fy


def attach_firm_controls(panel: pd.DataFrame, fy: pd.DataFrame) -> pd.DataFrame:
    # Firm-level controls from CSMAR (size_pre available in pair_year via ticker_key)
    pre = panel.drop_duplicates(["cn_id", "ticker_key"])[["cn_id", "ticker_key", "size_pre", "large_firm"]]
    fy = fy.merge(pre, on="cn_id", how="left")
    return fy


def main() -> None:
    print("Loading verified pair_year panel...")
    panel = pd.read_parquet(TOP / "data" / "derived" / "pair_year.parquet")
    print(f"  panel rows={len(panel)}, firms={panel['cn_id'].nunique()}, years={panel['year'].nunique()}")

    fy = build_firm_year(panel)
    print(f"  firm-year rows (active links only): {len(fy)}")

    fy = attach_baseline(panel, fy)
    fy = attach_firm_controls(panel, fy)

    # Save raw network indicators (firm-year), preserving missing for diagnostics
    fy.to_parquet(OUT / "firm_year_network.parquet", index=False)
    print(f"Saved: {OUT / 'firm_year_network.parquet'}")

    # Quick diagnostics
    print("\n=== DESCRIPTIVE (firm-level mean by year, among firms with active links) ===")
    desc = fy.groupby("year")[["RCEP_share", "Regional_HHI", "Entropy", "N_countries", "N_RCEP_countries", "N_links"]].mean()
    print(desc.round(3).to_string())

    print("\n=== Missingness ===")
    print(fy[["RCEP_share", "Regional_HHI", "Entropy", "N_countries"]].isna().mean().round(3).to_string())

    # Validation counts
    summary = {
        "firm_year_rows": int(len(fy)),
        "unique_firms": int(fy["cn_id"].nunique()),
        "firms_with_active_links": int(fy["N_links"].gt(0).sum()),
        "firm_year_with_links": int(fy["N_links"].gt(0).sum()),
        "RCEP_members": len(RCEP),
        "year_range": [int(YEARS.min()), int(YEARS.max())],
    }
    import json
    (OUT / "1_network_indicators_summary.json").write_text(json.dumps(summary, indent=2))
    print("\nSummary:", summary)


if __name__ == "__main__":
    main()
