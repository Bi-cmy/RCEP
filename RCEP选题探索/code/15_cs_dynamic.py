#!/usr/bin/env python3
"""Extract Callaway-Sant'Anna group-time ATT + dynamic + pre-trend (W) test."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from csdid.att_gt import ATTgt

DATA = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP_JAE_修订/data/derived/pair_year.parquet")
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题9现代DID")
AUDIT.mkdir(parents=True, exist_ok=True)

IMPL_YEAR = {"JP":2022,"KR":2022,"AU":2022,"NZ":2022,"SG":2022,"TH":2022,"VN":2022,"MY":2022,"KH":2022,"LA":2022,"MM":2022,"BN":2022,"ID":2023,"PH":2023}


def main():
    df = pd.read_parquet(DATA).sort_values(["pair_id","year"])
    df["active_prev"] = df.groupby("pair_id")["active"].shift(1)
    df["active_next"] = df.groupby("pair_id")["active"].shift(-1)
    df["entry"] = ((df["active"]==1)&(df["active_prev"]!=1)).astype(int)
    df["break"] = ((df["active"]==1)&(df["active_next"]==0)).astype(int)
    df["g"] = np.where(df["rcep"]==1, df["partner_country"].map(IMPL_YEAR).fillna(0).astype(int), 0)
    df["idn"] = pd.factorize(df["pair_id"].astype(str))[0]+1
    df["t"] = df["year"].astype(int)
    asia = df["asia_control"].eq(1) if "asia_control" in df.columns else df["rcep"].eq(0)
    d = df[(df["rcep"]==1)|(asia)].copy()

    all_out = {}
    for outcome in ["entry","break"]:
        sub = d[["idn","t","g",outcome]].dropna().astype({outcome:float})
        att = ATTgt(yname=outcome,tname="t",idname="idn",gname="g",data=sub,
                    control_group="nevertreated",est_method="dr",
                    allow_unbalanced_panel=True,panel=True,print_details=False,
                    compute_inffunc=True)
        att.fit()
        mp = att.MP
        g = np.asarray(mp["group"]); atts = np.asarray(mp["att"]); ts = np.asarray(mp["t"])
        print(f"\n{'='*60}\n{outcome} — group-time ATT\n{'='*60}")
        for gi, ti, ai in zip(g, ts, atts):
            print(f"  cohort g={gi}, period t={ti}: ATT={ai:+.5f}")
        print(f"\n  Pre-trend Wald W = {mp['W']:.3f}, p-value = {mp['Wpval']:.4f}")

        # dynamic aggregation
        att.aggte(typec="dynamic")
        atte = att.atte
        # atte has .att and .se arrays keyed by event time e
        print(f"\n  --- dynamic ATT (event time e) ---")
        if hasattr(atte, 'att'):
            try:
                dyn_att = np.asarray(atte.att)
                dyn_se = np.asarray(atte.se) if hasattr(atte,'se') else np.full_like(dyn_att, np.nan)
                # e values
                egt = atte.egt if hasattr(atte,'egt') else None
                # att_gt object for dynamic stores: atte.att is a list; inspect
                print("  atte.att type:", type(atte.att), "len:", len(atte.att))
                print("  atte.att =", atte.att)
                if hasattr(atte,'se'):
                    print("  atte.se =", atte.se)
            except Exception as e:
                print("  dyn extract err:", e)
        all_out[outcome] = {"W": float(mp["W"]), "Wpval": float(mp["Wpval"]),
                            "gt_att": [[float(gi), float(ti), float(ai)] for gi,ti,ai in zip(g,ts,atts)]}

    (AUDIT/"cs_dynamic_results.json").write_text(json.dumps(all_out, indent=2, default=float))
    print("\nSaved cs_dynamic_results.json")


if __name__ == "__main__":
    main()
