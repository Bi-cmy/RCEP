#!/usr/bin/env python3
"""
Standard placebo battery for the RCEP DiD, using pair-clustered inference
throughout. No country-label permutations. Consists of:
  (1) Fake-policy-year (timing) placebos: 2019 / 2020 / 2021.
  (2) Fake treatment timing via event-study pre-trend check (leads).
  (3) A false "treatment" placebo on a rotated set of non-RCEP countries
      as an additional timing-space check (reported, not the headline).
Reports full coefficient / SE / t / p / N / fixed effects per specification.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
TABLES = ROOT / "results" / "tables"
RCEP = {"JP","KR","AU","NZ","ID","MY","PH","SG","TH","VN","BN","KH","LA","MM"}


def indexed(frame):
    return frame.sort_values(["pair_id","year"]).set_index(["pair_id","year"])


def fit_twfe(work, term):
    data = indexed(work.dropna(subset=["active", term]).copy())
    model = PanelOLS(data["active"].astype(float), data[term].astype(float),
                     entity_effects=True, time_effects=True,
                     drop_absorbed=True, check_rank=True)
    res = model.fit(cov_type="clustered",
                    clusters=pd.DataFrame({"pair": data.index.get_level_values("pair_id")},
                                           index=data.index))
    return res, data


def row(name, res, term, data):
    return {
        "specification": name,
        "term": term,
        "coefficient": float(res.params[term]),
        "std_error": float(res.std_errors[term]),
        "t_stat": float(res.tstats[term]),
        "p_value": float(res.pvalues[term]),
        "observations": int(res.nobs),
        "pairs": int(data.index.get_level_values("pair_id").nunique()),
        "partner_countries": int(data["partner_country"].nunique()),
        "entity_fe": True,
        "time_fe": True,
        "cluster": "pair",
    }


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(DATA / "pair_year.parquet")

    # ------------- 1. Fake policy-year timing placebos -------------
    print("=== 1. Timing placebo: false policy years ===")
    rows = []
    # True policy year is 2022. Test false years using only pre-2022 data.
    pre = panel[panel["year"].le(2021)].copy()
    for fy in [2019, 2020, 2021]:
        pre[f"fake_{fy}"] = (pre["rcep"].eq(1) & pre["year"].ge(fy)).astype("int8")
        res, data = fit_twfe(pre, f"fake_{fy}")
        rows.append(row(f"False policy year {fy}", res, f"fake_{fy}", data))
        print(f"  false {fy}: coef={res.params[f'fake_{fy}']:+.5f} "
              f"se={res.std_errors[f'fake_{fy}']:.5f} "
              f"p={res.pvalues[f'fake_{fy}']:.3f} N={res.nobs:.0f}")

    # Real 2022 for reference (full sample, pre+post)
    panel["treat"] = panel["treated_uniform"].astype("int8")
    res, data = fit_twfe(panel, "treat")
    rows.append(row("True policy 2022 (reference, full sample)", res, "treat", data))
    print(f"  REAL 2022: coef={res.params['treat']:+.5f} se={res.std_errors['treat']:.5f} "
          f"p={res.pvalues['treat']:.3f} N={res.nobs:.0f}")
    pd.DataFrame(rows).to_csv(TABLES / "placebo_timing_standard.csv", index=False)

    # ------------- 2. Event-study pre-trend check -------------
    print("\n=== 2. Event-study pre-trend (joint leads = 0) ===")
    terms = {}
    rel_map = {-4:"m4",-3:"m3",-2:"m2",-1:"m1",0:"p0",1:"p1",2:"p2",3:"p3"}
    for k, nm in rel_map.items():
        panel[nm] = (panel["rcep"].eq(1) & panel["year"].sub(2022).eq(k)).astype("int8")
        terms[nm] = panel[nm]
    # Drop the base period (=m1, 2021) to avoid collinearity; keep one lead bin
    term_list = [nm for k, nm in rel_map.items() if k != -1]
    data = indexed(panel.dropna(subset=["active"]).copy())
    model = PanelOLS(data["active"].astype(float), data[term_list].astype(float),
                     entity_effects=True, time_effects=True,
                     drop_absorbed=True, check_rank=False)
    res = model.fit(cov_type="clustered",
                    clusters=pd.DataFrame({"pair": data.index.get_level_values("pair_id")},
                                           index=data.index))
    evt = []
    for k, nm in rel_map.items():
        if nm not in res.params.index:
            # omitted base period OR absorbed (e.g., beyond sample)
            evt.append({"rel_time": k, "term": nm,
                        "coef": 0.0, "se": 0.0, "p": np.nan,
                        "ci_lo": 0.0, "ci_hi": 0.0})
            continue
        evt.append({"rel_time": k, "term": nm,
                    "coef": float(res.params[nm]), "se": float(res.std_errors[nm]),
                    "p": float(res.pvalues[nm]),
                    "ci_lo": float(res.params[nm] - 1.96 * res.std_errors[nm]),
                    "ci_hi": float(res.params[nm] + 1.96 * res.std_errors[nm])})
    evt = pd.DataFrame(evt).sort_values("rel_time")
    evt.to_csv(TABLES / "event_study_pre_trend.csv", index=False)

    pre_terms = [nm for nm in ["m4","m3","m2"] if nm in term_list]
    restriction = np.zeros((len(pre_terms), len(res.params)))
    for i, t in enumerate(pre_terms):
        restriction[i, list(res.params.index).index(t)] = 1
    wald = res.wald_test(restriction)
    wald_p = float(np.asarray(wald.pval).squeeze())
    wald_stat = float(np.asarray(wald.stat).squeeze())
    print(f"  joint pre-trend Wald: stat={wald_stat:.3f} p={wald_p:.3f} (m1 omitted is 2022-1=2021 relative)")
    print("  event-study summary (coef, se, p):")
    for _, r in evt.iterrows():
        print(f"    rel={int(r['rel_time']):+d}  {r['coef']:+.5f} ({r['se']:.5f}) p={r['p']:.3f}")

    # ------------- 3. False non-RCEP treatment placebo (space check) -------------
    # Assign the fictitious "RCEP" label to a set of large non-RCEP trading
    # partners that are NOT members, then re-run the timing DiD. This is
    # standard as a mistaken-treatment (false-compound) placebo.
    print("\n=== 3. False non-RCEP treatment placebo ===")
    # Choose large non-RCEP partner economies that plausibly share an "Asian integration" shock
    false_group = {"HK","TW","IN","RU","GB","DE","FR","IT","BR"}
    rows2 = []
    for fy in [2019, 2020, 2021]:
        sub = panel[panel["year"].le(2021)].copy()
        sub["fake_treat"] = (sub["partner_country"].isin(false_group) & sub["year"].ge(fy)).astype("int8")
        res2, data2 = fit_twfe(sub, "fake_treat")
        rows2.append(row(f"False non-RCEP group, policy {fy}", res2, "fake_treat", data2))
        print(f"  false-nonRCEP group, policy {fy}: coef={res2.params['fake_treat']:+.5f} "
              f"p={res2.pvalues['fake_treat']:.3f}")
    pd.DataFrame(rows2).to_csv(TABLES / "placebo_false_group.csv", index=False)

    summary = {
        "timing_placebo": pd.DataFrame(rows).to_dict("records"),
        "event_study_pretrend_wald_p": wald_p,
        "event_study_pretrend_wald_stat": wald_stat,
        "false_group_placebo": pd.DataFrame(rows2).to_dict("records"),
        "note": ("All estimates use pair-clustered SE. Timing placebos "
                 "use pre-2022 data only. The event-study omitted period is 2021 "
                 "(rel_time=-1)."),
    }
    (TABLES / "placebo_diagnostics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nDone. Saved timing_standard / event_study_pre_trend / false_group / placebo_diagnostics.")


if __name__ == "__main__":
    main()
