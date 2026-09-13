#!/usr/bin/env python3
"""
Modern staggered DiD (Callaway-Sant'Anna) for RCEP link entry/breakage.

Treatment cohort = partner's actual RCEP implementation year (2022 or 2023).
Never-treated controls = non-RCEP Asian partners. Estimates group-time ATTs,
aggregated to overall ATT and dynamic (event-study) effects with honest
pre-trends.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from csdid.att_gt import ATTgt

DATA = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP_JAE_修订/data/derived/pair_year.parquet")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题9现代DID")
AUDIT.mkdir(parents=True, exist_ok=True)

IMPL_YEAR = {
    "JP": 2022, "KR": 2022, "AU": 2022, "NZ": 2022, "SG": 2022, "TH": 2022,
    "VN": 2022, "MY": 2022, "KH": 2022, "LA": 2022, "MM": 2022, "BN": 2022,
    "ID": 2023, "PH": 2023,
}


def main():
    df = pd.read_parquet(DATA)
    df = df.sort_values(["pair_id", "year"]).copy()
    df["active_prev"] = df.groupby("pair_id")["active"].shift(1)
    df["active_next"] = df.groupby("pair_id")["active"].shift(-1)
    df["entry"] = ((df["active"] == 1) & (df["active_prev"] != 1)).astype(int)
    df["break"] = ((df["active"] == 1) & (df["active_next"] == 0)).astype(int)

    df["partner"] = df["partner_country"].astype(str).str.strip()
    df["rcep"] = df["rcep"].astype(int)
    df["g"] = np.where(df["rcep"] == 1, df["partner"].map(IMPL_YEAR).fillna(0).astype(int), 0)
    df["id"] = df["pair_id"].astype(int).astype(str)
    df["t"] = df["year"].astype(int)

    # RCEP treated + non-RCEP Asian never-treated controls
    asia_ctl = df["asia_control"].eq(1) if "asia_control" in df.columns else df["rcep"].eq(0)
    d = df[(df["rcep"] == 1) | (asia_ctl)].copy()
    # id must be numeric for csdid
    d["idn"] = pd.factorize(d["id"])[0] + 1
    print(f"Sample: {len(d)} rows, pairs={d['idn'].nunique()}, cohorts g: {sorted(d['g'].unique())}")
    print(f"entry={d['entry'].sum()}, break={d['break'].sum()}")

    out_rows = []
    for outcome in ["entry", "break"]:
        print(f"\n=== Callaway-Sant'Anna: {outcome} ===")
        try:
            sub = d[["idn", "t", "g", outcome]].dropna().copy()
            sub = sub.astype({outcome: float})
            att = ATTgt(
                yname=outcome, tname="t", idname="idn", gname="g", data=sub,
                control_group="nevertreated", est_method="dr",
                allow_unbalanced_panel=True, panel=True, print_details=False,
            )
            att.fit()
            # overall simple ATT
            agg = att.aggte("simple")
            print(f"  overall ATT = {agg[0]:+.5f} (se={agg[1]:.5f})")
            # dynamic (event study)
            dyn = att.aggte("dynamic")
            print("  dynamic ATT (相对期):")
            print(dyn.round(4).to_string())
            out_rows.append({"outcome": outcome, "overall_att": float(agg[0]), "se": float(agg[1])})
        except Exception as e:
            import traceback
            print(f"  ERR: {str(e)[:200]}")
            traceback.print_exc()

    (AUDIT / "cs_modern_did.json").write_text(json.dumps(out_rows, indent=2, default=float))
    print("\nDone.")


if __name__ == "__main__":
    main()
