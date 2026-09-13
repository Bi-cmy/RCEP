#!/usr/bin/env python3
"""
11b — Firm-level RCEP tariff-cut EXPOSURE (continuous), CORRECTED.

Fixes from 11:
  - Use ticker_key (standard 6-digit) not cn_ticker (mixed formats).
  - Use FOUR-level GB industry (gb4, e.g. C2721 -> 2721) for finer firm variation,
    matched to GB->HS at the finest available digit.
  - Exposure = mean China-RCEP import tariff cut (pre-policy baseline) over the
    firm's industry HS products. Policy-predetermined, exogenous.

Two-way FE (firm + year) with the continuous exposure x Post. Note: since exposure
is time-invariant per firm, we interact Post x exposure; firm FE absorbs level.
Outcome: break / entry on RCEP-partner links.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyfixest as pf

ROOT = Path("C:/Users/97328/Desktop/学习/论文、项目/供应链冲击")
DATA = ROOT / "RCEP_JAE_修订/data/derived/pair_year.parquet"
POL = ROOT / "REPC/08_rcep_analysis/01_data_build/processed_tariffs/china_import_rcep_policy_incremental_hs12_2015_2024.csv"
IND = ROOT / "关税+供应链（数据）/上市公司国民经济行业分类.xlsx"
MAP = ROOT / "关税+供应链（数据）/所有行业和 hs2017 匹配（GB2017）/国民经济行业分类（GB2017）所有行业和hs2017匹配结果.xlsx"
OUT = ROOT / "RCEP选题探索/results/tables"
OUT.mkdir(parents=True, exist_ok=True)
AUDIT = ROOT / "RCEP选题探索/audit/选题6企业级暴露度"
AUDIT.mkdir(parents=True, exist_ok=True)


def build_firm_exposure():
    ind = pd.read_excel(IND)
    ind = ind[["证券代码", "所属国民经济行业代码\n[交易日期] 最新收盘日\n[行业级别] 四级行业",
               "所属国民经济行业代码\n[交易日期] 最新收盘日\n[行业级别] 三级行业",
               "所属国民经济行业代码\n[交易日期] 最新收盘日\n[行业级别] 二级行业"]].copy()
    ind.columns = ["ticker", "gb4", "gb3", "gb2"]
    ind["ticker6"] = ind["ticker"].astype(str).str.split(".").str[0]
    for c in ["gb4", "gb3", "gb2"]:
        ind[c + "_d"] = ind[c].astype(str).str.strip().str.replace(r"[A-Za-z]", "", regex=True)

    m = pd.read_excel(MAP)
    m["gb_full"] = m["gb2017"].astype(str).str.strip()
    m["gb4"] = m["gb_full"].str.zfill(4)  # 4-digit small-class
    m["gb2"] = m["gb_full"].str[:2]

    pol = pd.read_csv(POL, low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    hs = pol.groupby("hs6")["pre_rcep_baseline_pct"].mean().reset_index()
    hs.columns = ["hs6", "rcep_cut"]
    m["hs6"] = m["hs2017"].astype(str).str.strip().str[:6]
    m = m.merge(hs, on="hs6", how="left")
    m["rcep_cut"] = m["rcep_cut"].fillna(0)

    # Match at 4-digit small class first; fallback to 2-digit
    m4 = m[["gb4", "hs6", "rcep_cut"]].drop_duplicates("hs6").rename(columns={"gb4": "gb4_d"})
    firm = ind.merge(m4, on="gb4_d", how="inner")
    # coverage check: if too few, fall back to gb2
    if firm["ticker6"].nunique() < 2000:
        m2 = m[["gb2", "hs6", "rcep_cut"]].drop_duplicates("hs6").rename(columns={"gb2": "gb2_d"})
        firm = ind.merge(m2, on="gb2_d", how="inner")
        key = "gb2_d"
    else:
        key = "gb4_d"
    firm_exp = firm.groupby("ticker6")["rcep_cut"].mean().reset_index()
    firm_exp.columns = ["ticker6", "firm_rcep_exposure"]
    return firm_exp, key


def main():
    fexp, key = build_firm_exposure()
    print(f"Firm exposure via {key}: {len(fexp)} firms")
    print(f"  mean={fexp['firm_rcep_exposure'].mean():.3f}, sd={fexp['firm_rcep_exposure'].std():.3f}, "
          f"nonzero={(fexp['firm_rcep_exposure']>0).mean():.3f}, unique={fexp['firm_rcep_exposure'].nunique()}")

    df = pd.read_parquet(DATA)
    df["ticker_key_s"] = df["ticker_key"].astype(str).str.strip()
    df = df.merge(fexp, left_on="ticker_key_s", right_on="ticker6", how="left")
    df["firm_rcep_exposure"] = df["firm_rcep_exposure"].fillna(0)
    print(f"  matched in pair_year: nonzero exposure share={(df['firm_rcep_exposure']>0).mean():.3f}")

    df = df.sort_values(["pair_id", "year"])
    df["active_next"] = df.groupby("pair_id")["active"].shift(-1)
    df["active_prev"] = df.groupby("pair_id")["active"].shift(1)
    df["break"] = ((df["active"] == 1) & (df["active_next"] == 0)).astype(int)
    df["entry"] = ((df["active"] == 1) & (df["active_prev"] != 1)).astype(int)
    df["post"] = (df["year"] >= 2022).astype(int)
    df["post_x_exp"] = df["post"] * df["firm_rcep_exposure"]

    # Restrict to RCEP-partner links (exposure applies to RCEP sourcing)
    df_r = df[df["rcep"] == 1].copy()
    df_r["firm_fe"] = df_r["cn_id"].astype(str)
    df_r["year_d"] = df_r["year"].astype(str)
    df_r["country"] = df_r["partner_country"].astype(str)
    print(f"\nRCEP-partner rows: {len(df_r)}; break={df_r['break'].sum()}, entry={df_r['entry'].sum()}")
    print(f"post_x_exp nonzero share: {(df_r['post_x_exp']>0).mean():.3f}")

    results = []
    print("\n=== 双重固定效应: firm FE + year FE ===")
    for outcome in ["break", "entry"]:
        for cluster, ctag in [("firm_fe", "firm-cluster"), ("country", "country-cluster")]:
            fml = f"{outcome} ~ post_x_exp | firm_fe + year_d"
            try:
                m = pf.feols(fml, data=df_r, vcov={"CRV1": cluster}, fixef_rm="none", lean=True)
                t = m.tidy(); row = t[t.index == "post_x_exp"]
                if len(row):
                    print(f"  {outcome:6} [{ctag:16}] coef={row['Estimate'].iloc[0]:+.6f} se={row['Std. Error'].iloc[0]:.6f} p={row['Pr(>|t|)'].iloc[0]:.4f} N={m._N}")
                    results.append({"outcome":outcome,"cluster":ctag,"coef":float(row['Estimate'].iloc[0]),"se":float(row['Std. Error'].iloc[0]),"p":float(row['Pr(>|t|)'].iloc[0]),"n":int(m._N)})
                else:
                    print(f"  {outcome:6} [{ctag:16}] 被吸收")
            except Exception as e:
                print(f"  {outcome:6} [{ctag:16}] ERR {str(e)[:90]}")

    pd.DataFrame(results).to_csv(OUT / "topic6_firm_exposure_did.csv", index=False)
    (AUDIT / "firm_exposure_did.json").write_text(json.dumps(results, indent=2, default=float))
    print("\nSaved topic6_firm_exposure_did.csv")


if __name__ == "__main__":
    main()
