#!/usr/bin/env python3
"""
Topic 1 (v2) — Does RCEP reduce geographic concentration of China's import sources?

CORRECTED exposure design (fixes collinearity from v1):
  Exposure = policy-PREDETERMINED baseline tariff rate (pre_rcep_baseline_pct)
             aggregated from the partner x HS6 x year policy panel to HS6 x year.
             It is fixed at the policy date (time-invariant per hs6), varies in
             the cross-section, and is plausibly exogenous (China's MFN/legacy-
             FTA rate before RCEP). This avoids the Post x exp collinearity.
  Treatment = Post2022 x Exposure (continuous DiD), product FE + year FE.
  Outcome   = supplier_hhi / supplier_effective_number / largest_supplier_share
              / rcep_import_share / rcep_supplier_count  (from SC outcomes panel).
  Inference: HS2-chapter clustered SE. Event study with joint pre-trend Wald.

We construct the HS6 x year exposure ourselves from the policy panel, and
aggregate using RCEP-source import weights (pre-policy) so the weight is fixed.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

POL = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_tariffs")
TD = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/REPC/08_rcep_analysis/01_data_build/processed_trade")
OUT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/results/tables")
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击/RCEP选题探索/audit/选题1来源集中度")
AUDIT.mkdir(parents=True, exist_ok=True)

OUTCOMES = ["supplier_hhi", "supplier_effective_number", "largest_supplier_share",
            "rcep_import_share", "rcep_supplier_count"]


def build_policy_exposure() -> pd.DataFrame:
    """Aggregate partner x hs6 policy baseline to hs6 x year, weighted by RCEP
    source import share fixed at 2018-2019 (pre-policy). Returns hs6 x year."""
    pol = pd.read_csv(POL / "china_import_rcep_policy_incremental_hs12_2015_2024.csv", low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    pol["year"] = pol["calendar_year"].astype("int64")

    # Pre-policy baseline rate (time-invariant per partner x hs6)
    base = pol.groupby(["partner_iso3", "hs6"])["pre_rcep_baseline_pct"].first().reset_index()
    # Also take the ultimate/first-year incremental cut as an alternative intensity
    cut = pol.groupby(["partner_iso3", "hs6"])["first_year_incremental_cut_pct"].first().reset_index()
    pol_feat = base.merge(cut, on=["partner_iso3", "hs6"], how="left")

    # RCEP source import weights (pre-policy, 2018-2019) from Atlas imports global
    imp = pd.read_csv(TD / "atlas_hs12_china_imports_global_2015_2024.csv", low_memory=False)
    imp["hs6"] = imp["product_hs12_code"].astype(str).str.zfill(6)
    imp["year"] = imp["year"].astype("int64")
    imp = imp.rename(columns={"partner_iso3_code": "partner_iso3"})
    w = imp[imp["year"].between(2018, 2019)]
    w = w.groupby(["partner_iso3", "hs6"]).agg(import_value=("import_value", "sum")).reset_index()
    # restrict to RCEP members
    RCEP = {"JPN","KOR","AUS","NZL","IDN","MYS","PHL","SGP","THA","VNM","BRN","KHM","LAO","MMR"}
    w = w[w["partner_iso3"].isin(RCEP)]
    # weights per hs6
    w["hs6"] = w["hs6"].astype(str).str.zfill(6)
    w["w"] = w["import_value"] / w.groupby("hs6")["import_value"].transform("sum")
    pol_feat = pol_feat.merge(w[["partner_iso3", "hs6", "w"]], on=["partner_iso3", "hs6"], how="left")
    pol_feat["w"] = pol_feat["w"].fillna(0)

    # Weighted-by-RCEP-source baseline exposure per hs6 (fixed over time)
    def safe_weighted_avg(values, weights):
        values = np.asarray(values, dtype=float)
        weights = np.asarray(weights, dtype=float)
        mask = weights > 0
        if mask.sum() == 0:
            return 0.0
        return float(np.average(values[mask], weights=weights[mask]))

    exp = pol_feat.groupby("hs6").apply(
        lambda g: pd.Series({"exp_base": safe_weighted_avg(g["pre_rcep_baseline_pct"], g["w"]),
                             "exp_cut": safe_weighted_avg(g["first_year_incremental_cut_pct"], g["w"]),
                             "n_partners": int((g["w"] > 0).sum())}),
        include_groups=False,
    ).reset_index()
    # The apply gave hs6 -> series; tidy
    return exp


def main():
    print("Building policy-predetermined exposure (weighted by pre-policy RCEP source share)...")
    exp = build_policy_exposure()
    print(f"  exposure hs6 rows: {len(exp)}")
    print("  exp_base stats:", exp["exp_base"].describe().round(3).to_dict())
    print("  nonzero exp_base share:", (exp["exp_base"].fillna(0) != 0).mean().round(3))

    sc = pd.read_csv(TD / "china_import_hs12_supply_chain_outcomes_2015_2024.csv", low_memory=False)
    sc["hs6"] = sc["hs6"].astype(str).str.zfill(6)
    sc["year"] = sc["calendar_year"].astype("int64")
    sc["hs2"] = sc["hs6"].astype(str).str[:2]

    # Merge exposure (fixed per hs6)
    df = sc.merge(exp, on="hs6", how="left")
    df["post"] = (df["year"] >= 2022).astype(float)
    df["post_x_base"] = df["post"] * df["exp_base"].fillna(0)
    df["post_x_cut"] = df["post"] * df["exp_cut"].fillna(0)
    df["primary_exp"] = df["exp_base"].fillna(0)
    print(f"\nMerged panel: {df.shape}, hs6={df['hs6'].nunique()}")
    print(f"post_x_base nonzero share: {(df['post_x_base']!=0).mean():.3f}")

    # Baseline DiD
    def indexed(x):
        return x.sort_values(["hs6", "year"]).set_index(["hs6", "year"])

    print("\n=== Baseline DiD (product FE + year FE) ===")
    results = []
    for treatment in ["post_x_base", "post_x_cut"]:
        print(f"\n--- Treatment: {treatment} ---")
        for outcome in OUTCOMES:
            work = df[["hs6", "year", "hs2", outcome, treatment, "primary_exp"]].copy()
            data = indexed(work.dropna(subset=[outcome]).copy())
            model = PanelOLS(data[outcome].astype(float), data[[treatment]].astype(float),
                             entity_effects=True, time_effects=True, drop_absorbed=True, check_rank=False)
            cl = pd.DataFrame({"hs2": pd.Categorical(data["hs2"]).codes}, index=data.index)
            res = model.fit(cov_type="clustered", clusters=cl)
            results.append({"treatment": treatment, "outcome": outcome,
                            "coef": float(res.params[treatment]), "se": float(res.std_errors[treatment]),
                            "p": float(res.pvalues[treatment]), "n": int(res.nobs),
                            "hs6": int(data.index.get_level_values("hs6").nunique())})
            print(f"  {outcome:>30}: coef={results[-1]['coef']:+.5f} se={results[-1]['se']:.5f} "
                  f"p={results[-1]['p']:.3f} N={results[-1]['n']} hs6={results[-1]['hs6']}")
    pd.DataFrame(results).to_csv(OUT / "topic1_baseline_v2.csv", index=False)
    (AUDIT / "topic1_baseline_v2.json").write_text(json.dumps(results, indent=2, default=float))

    print("\nSaved topic1_baseline_v2.csv")


if __name__ == "__main__":
    main()
