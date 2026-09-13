#!/usr/bin/env python3
"""
Topic 3 (v2, corrected) — First-FTA (Japan) vs Existing-FTA (Korea + ASEAN/AU/NZ)
causal identification, strictly using TWO-WAY FIXED EFFECTS.

Design per aer-identification + did-analysis skills:
  - Two-way FE: hs6 entity effects + year time effects (PanelOLS, entity+time).
  - Cluster SE at hs2 chapter (treatment varies at product level; cluster at
    the policy-relevant level to avoid understated SEs).
  - Continuous treatment intensity (Japan's pre-policy baseline tariff, the
    first-FTA exposure). Standalone intensity term is ABSORBED by entity FE;
    we include only the interaction terms per the continuous-intensity skill
    (drop standalone to avoid collinearity when controls' intensity ~ 0).
  - Triple interaction: Japan-first-FTA intensity x post x intermediate (BEC)
    to test the cumulative-RoO mechanism.
  - Event study with leads/lags (base = 2021) and a joint pre-trend Wald test.

Outcomes (supply-chain outcomes panel): japan_import_share, rcep_import_share,
supplier_hhi, supplier_effective_number, largest_supplier_share.

Estimates archived regardless of sign/significance.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

DATA = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/data/first_vs_existing_corrected.parquet")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题3中日首次FTA")
AUDIT.mkdir(parents=True, exist_ok=True)

OUTCOMES = ["japan_import_share", "rcep_import_share", "supplier_hhi",
            "supplier_effective_number", "largest_supplier_share"]


def indexed(df):
    return df.sort_values(["hs6", "year"]).set_index(["hs6", "year"])


def bid_fe(df, outcome, xcols):
    """Two-way FE (entity hs6 + time year) with hs2-clustered SEs."""
    work = df[["hs6", "year", "hs2", outcome] + xcols].copy()
    data = indexed(work.dropna(subset=[outcome]).copy())
    model = PanelOLS(data[outcome].astype(float), data[xcols].astype(float),
                     entity_effects=True, time_effects=True,
                     drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    return res, data


def main():
    df = pd.read_parquet(DATA)
    print(f"Panel: {df.shape}, hs6={df['hs6'].nunique()}")
    df["post"] = (df["year"] >= 2022).astype(float)
    df["year"] = df["year"].astype("int64")
    # fill treatment intensities (continuous exposure; standalone absorbed by FE)
    for c in ["first_base", "kor_base", "existing_base"]:
        df[c] = df[c].fillna(0)
    df["post_x_first"] = df["post"] * df["first_base"]
    df["post_x_kor"] = df["post"] * df["kor_base"]
    df["post_x_existing"] = df["post"] * df["existing_base"]
    df["post_x_first_cut"] = df["post"] * df["first_cut"].fillna(0)
    df["intm"] = df["intm"].fillna(0)
    df["post_x_first_x_intm"] = df["post"] * df["first_base"] * df["intm"]

    print("\n=== BASELINE TWO-WAY FE DiD (hs6 FE + year FE, hs2 cluster) ===")
    results = []
    for outcome in OUTCOMES:
        res, data = bid_fe(df, outcome, ["post_x_first", "post_x_kor", "post_x_existing"])
        results.append({
            "outcome": outcome,
            "post_x_first": float(res.params["post_x_first"]), "se_first": float(res.std_errors["post_x_first"]), "p_first": float(res.pvalues["post_x_first"]),
            "post_x_kor": float(res.params["post_x_kor"]), "se_kor": float(res.std_errors["post_x_kor"]), "p_kor": float(res.pvalues["post_x_kor"]),
            "post_x_existing": float(res.params["post_x_existing"]), "p_existing": float(res.pvalues["post_x_existing"]),
            "n": int(res.nobs), "hs6": int(data.index.get_level_values("hs6").nunique()),
        })
        r = results[-1]
        print(f"{outcome:>26}: JP_f={r['post_x_first']:+.5f}(p={r['p_first']:.3f})  "
              f"KR={r['post_x_kor']:+.5f}(p={r['p_kor']:.3f})  "
              f"EX={r['post_x_existing']:+.5f}(p={r['p_existing']:.3f})  N={r['n']}")
    pd.DataFrame(results).to_csv(OUT / "topic3_v2_baseline_twfe.csv", index=False)

    print("\n=== TRIPLE: Japan first-FTA x post x intermediate (cumulative RoO) ===")
    tri = []
    for outcome in OUTCOMES:
        res, data = bid_fe(df, outcome, ["post_x_first", "post_x_first_x_intm", "post_x_kor"])
        if "post_x_first_x_intm" not in res.params:
            continue
        tri.append({"outcome": outcome,
                    "post_x_first": float(res.params["post_x_first"]), "p_first": float(res.pvalues["post_x_first"]),
                    "triple": float(res.params["post_x_first_x_intm"]), "p_triple": float(res.pvalues["post_x_first_x_intm"]),
                    "n": int(res.nobs)})
        t = tri[-1]
        print(f"{outcome:>26}: JP_f={t['post_x_first']:+.5f}(p={t['p_first']:.3f})  "
              f"x_intm={t['triple']:+.5f}(p={t['p_triple']:.3f})")
    pd.DataFrame(tri).to_csv(OUT / "topic3_v2_triple_intermediate.csv", index=False)

    print("\n=== EVENT STUDY + pre-trend Wald: japan_import_share (base=2021) ===")
    work = df.copy(); work["y"] = work["japan_import_share"].astype(float)
    rel_map = {-4: "m4", -3: "m3", -2: "m2", 0: "p0", 1: "p1", 2: "p2"}
    for rel, name in rel_map.items():
        work[name] = work["first_base"] * work["year"].sub(2022).eq(rel).astype(float)
    terms = list(rel_map.values())
    data = indexed(work.dropna(subset=["y"]).copy())
    model = PanelOLS(data["y"].astype(float), data[terms].astype(float),
                     entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
    cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
    res = model.fit(cov_type="clustered", clusters=cl)
    pre = [t for t in ["m4", "m3", "m2"] if t in res.params.index]
    restriction = np.zeros((len(pre), len(res.params)))
    for i, t in enumerate(pre):
        restriction[i, list(res.params.index).index(t)] = 1
    wald = res.wald_test(restriction)
    coefs = {t: (float(res.params[t]), float(res.pvalues[t])) for t in terms if t in res.params.index}
    evt = {"outcome": "japan_import_share", "joint_pre_p": float(np.asarray(wald.pval).squeeze()), "coefs": coefs}
    print(f"  joint pre-trend p={evt['joint_pre_p']:.3f}")
    for t in ["m4", "m3", "m2", "p0", "p1", "p2"]:
        if t in coefs:
            print(f"    {t}: {coefs[t][0]:+.5f} (p={coefs[t][1]:.3f})")
    (AUDIT / "topic3_v2_event_japan.json").write_text(json.dumps(evt, indent=2, default=float))

    print("\n=== Diagnostics: treatment intensity balance across groups ===")
    for c in ["first_base", "kor_base", "existing_base"]:
        post_x = "post_x_" + c.replace("_base", "")
        nz_postx = (df[post_x].gt(0)).mean() if post_x in df.columns else np.nan
        print(f"  {c}: nonzero={(df[c]>0).mean():.3f}, mean={df[c].mean():.3f}, "
              f"post_x nonzero={nz_postx:.3f}")

    # Save all
    (AUDIT / "topic3_v2_appendix.json").write_text(json.dumps(
        {"baseline": results, "triple": tri, "event": evt}, indent=2, default=float))
    print("\nSaved topic3_v2 tables + audit")


if __name__ == "__main__":
    main()
