#!/usr/bin/env python3
"""
01 (v2) — Feasibility-check TWFE via linearmodels (no dummy-variable blowup).

Uses PanelOLS with within-transformed entity and time effects on the REPC
product-partner-year panel. Treatment = Japan-led incremental tariff cut
(Japan drives 91.5% of variation). Outcomes on log trade. For the feasibility
gate we run a two-way FE (partner x HS6 entity FE + year FE) on RCEP-source rows.
Partner x HS2 clustering for the 14-partner inference note.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

DATA = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results")
OUT.mkdir(parents=True, exist_ok=True)


def main():
    print("Loading source model panel...")
    df = pd.read_parquet(DATA / "china_import_source_hs12_model_panel_2015_2024.parquet")
    print(f"  shape={df.shape}")

    rcep = df[df["source_group"].isin(["japan", "other_rcep"])].copy()
    rcep["ln_trade"] = np.log1p(rcep["trade_value"].fillna(0))
    rcep["post"] = (rcep["calendar_year"].ge(2022)).astype(float)
    rcep["japan_cut"] = rcep["japan_tariff_cut_pct"].fillna(0)
    rcep["other_cut"] = rcep["other_rcep_tariff_cut_pct"].fillna(0)
    rcep["cut"] = np.where(rcep["source_group"].eq("japan"), rcep["japan_cut"], rcep["other_cut"])
    rcep["post_x_cut"] = rcep["post"] * rcep["cut"]

    # Entity = partner x hs6; time = year
    rcep["entity"] = rcep["partner_iso3"].astype(str) + "_" + rcep["hs6"].astype(str)
    rcep["year"] = rcep["calendar_year"].astype("int64")

    # Two-way FE: entity (partner x hs6) + year
    d = rcep.set_index(["entity", "year"]).sort_index()
    d = d.dropna(subset=["ln_trade"])
    print(f"  Estimation rows: {len(d)}")

    model = PanelOLS(
        d["ln_trade"].astype(float),
        d[["post_x_cut", "cut"]].astype(float),
        entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False,
    )
    res = model.fit(cov_type="clustered", cluster_entity=True)
    for t in ["post_x_cut", "cut"]:
        if t in res.params:
            print(f"  {t}: coef={res.params[t]:+.6f}  se={res.std_errors[t]:.6f}  p={res.pvalues[t]:.4f}")

    res_dict = {
        "feasibility": "DATA_PIPELINE_OK",
        "rows": int(res.nobs),
        "post_x_cut": float(res.params.get("post_x_cut", np.nan)),
        "post_x_cut_se": float(res.std_errors.get("post_x_cut", np.nan)),
        "post_x_cut_p": float(res.pvalues.get("post_x_cut", np.nan)),
        "cut": float(res.params.get("cut", np.nan)),
        "cut_p": float(res.pvalues.get("cut", np.nan)),
        "note": "Feasibility gate: two-way FE (partner x hs6 entity + year) on Japan-led cut. Check Japan dominance.",
    }
    (OUT / "01_feasibility_twfe.json").write_text(json.dumps(res_dict, indent=2, default=float))
    print("\n" + json.dumps(res_dict, indent=2))


if __name__ == "__main__":
    main()
