#!/usr/bin/env python3
"""
Diagnose + estimate partner-specific RCEP tariff-cut exposure.

Key fix over 11b: exposure is China's RCEP import tariff cut toward the SPECIFIC
partner country j (not a 14-country mean). Treatment varies across BOTH firm
(industry -> HS products) AND partner country -> far more variation.

Steps:
  1. firm industry (gb4) -> HS products -> China's RCEP cut toward partner j
     for those products -> firm x partner exposure (pre-policy, exogenous).
  2. Diagnostic: exposure quartiles vs entry/break rate (monotonicity check).
  3. Two-way FE (firm x partner FE + year FE) with Post x exposure.
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
AUDIT = ROOT / "RCEP选题探索/audit/选题7伙伴国精确暴露"
AUDIT.mkdir(parents=True, exist_ok=True)

ISO = {"JPN":"JP","KOR":"KR","AUS":"AU","NZL":"NZ","IDN":"ID","MYS":"MY","PHL":"PH",
       "SGP":"SG","THA":"TH","VNM":"VN","BRN":"BN","KHM":"KH","LAO":"LA","MMR":"MM"}


def main():
    # --- firm industry -> HS products (gb4) ---
    ind = pd.read_excel(IND)
    ind = ind[["证券代码","所属国民经济行业代码\n[交易日期] 最新收盘日\n[行业级别] 四级行业"]].copy()
    ind.columns = ["ticker","gb4"]
    ind["ticker6"] = ind["ticker"].astype(str).str.split(".").str[0]
    ind["gb4_d"] = ind["gb4"].astype(str).str.strip().str.replace(r"[A-Za-z]","",regex=True).str.zfill(4)

    m = pd.read_excel(MAP)
    m["gb4"] = m["gb2017"].astype(str).str.strip().str.zfill(4)
    m["hs6"] = m["hs2017"].astype(str).str.strip().str[:6]

    pol = pd.read_csv(POL, low_memory=False)
    pol["hs6"] = pol["hs6"].astype(str).str.zfill(6)
    pol["iso2"] = pol["partner_iso3"].map(ISO)
    # China's RCEP import tariff cut toward partner j, per hs6 (pre-policy baseline)
    cut = pol[["hs6","iso2","pre_rcep_baseline_pct"]].rename(columns={"pre_rcep_baseline_pct":"cut_pct"})
    cut = cut.dropna(subset=["iso2"])

    # firm industry -> hs6
    firm_hs = ind[["ticker6","gb4_d"]].merge(m[["gb4","hs6"]].rename(columns={"gb4":"gb4_d"}), on="gb4_d", how="inner")
    # firm x partner exposure = mean cut over the firm's industry HS products, toward partner j
    firm_partner = firm_hs.merge(cut, on="hs6", how="inner")
    fexp = firm_partner.groupby(["ticker6","iso2"])["cut_pct"].mean().reset_index()
    fexp.columns = ["ticker6","partner","exposure"]
    print(f"firm x partner exposure: {len(fexp)} rows, firms={fexp['ticker6'].nunique()}, partners={fexp['partner'].nunique()}")
    print(f"  exposure: mean={fexp['exposure'].mean():.3f}, sd={fexp['exposure'].std():.3f}, nonzero={(fexp['exposure']>0).mean():.3f}, unique={fexp['exposure'].nunique()}")

    # --- attach to pair_year (RCEP links) ---
    df = pd.read_parquet(DATA)
    df["ticker_key_s"] = df["ticker_key"].astype(str).str.strip()
    df["partner"] = df["partner_country"].astype(str).str.strip()
    df = df[df["rcep"]==1].copy()
    df = df.merge(fexp.rename(columns={"ticker6":"ticker_key_s"}), on=["ticker_key_s","partner"], how="left")
    df["exposure"] = df["exposure"].fillna(0)
    print(f"  merged RCEP rows={len(df)}, nonzero exposure share={(df['exposure']>0).mean():.3f}")

    # outcomes
    df = df.sort_values(["pair_id","year"])
    df["active_next"] = df.groupby("pair_id")["active"].shift(-1)
    df["active_prev"] = df.groupby("pair_id")["active"].shift(1)
    df["break"] = ((df["active"]==1)&(df["active_next"]==0)).astype(int)
    df["entry"] = ((df["active"]==1)&(df["active_prev"]!=1)).astype(int)
    df["post"] = (df["year"]>=2022).astype(int)
    df["post_x_exp"] = df["post"]*df["exposure"]

    # --- Diagnostic: exposure quartiles vs entry rate ---
    print("\n=== 诊断: 暴露度分位数 vs 增链率 (仅匹配企业) ===")
    m2 = df[df["exposure"]>0].copy()
    m2["exp_bin"] = pd.qcut(m2["exposure"], 4, labels=["Q1低","Q2","Q3","Q4高"], duplicates="drop")
    g = m2.groupby("exp_bin", observed=True).agg(entry_rate=("entry","mean"), break_rate=("break","mean"), n=("entry","count"))
    g["entry_rate"]=(g["entry_rate"]*100).round(2); g["break_rate"]=(g["break_rate"]*100).round(2)
    print(g.to_string())

    # --- Two-way FE: firm x partner FE + year FE ---
    df["firm_partner_fe"] = df["cn_id"].astype(str)+"_"+df["partner"]
    df["year_d"] = df["year"].astype(str)
    df["firm_fe"] = df["cn_id"].astype(str)
    print("\n=== 双重固定效应: firm×partner FE + year FE ===")
    results=[]
    for outcome in ["break","entry"]:
        for cluster,ctag in [("firm_partner_fe","fp-cluster"),("partner","partner-cluster")]:
            fml=f"{outcome} ~ post_x_exp | firm_partner_fe + year_d"
            try:
                mm=pf.feols(fml,data=df,vcov={"CRV1":cluster},fixef_rm="none",lean=True)
                t=mm.tidy(); row=t[t.index=="post_x_exp"]
                if len(row):
                    print(f"  {outcome:6}[{ctag:16}] coef={row['Estimate'].iloc[0]:+.6f} se={row['Std. Error'].iloc[0]:.6f} p={row['Pr(>|t|)'].iloc[0]:.4f} N={mm._N}")
                    results.append({"outcome":outcome,"cluster":ctag,"coef":float(row['Estimate'].iloc[0]),"se":float(row['Std. Error'].iloc[0]),"p":float(row['Pr(>|t|)'].iloc[0]),"n":int(mm._N)})
                else:
                    print(f"  {outcome:6}[{ctag:16}] 被吸收")
            except Exception as e:
                print(f"  {outcome:6}[{ctag:16}] ERR {str(e)[:90]}")

    pd.DataFrame(results).to_csv(OUT/"topic7_partner_exposure_did.csv",index=False)
    (AUDIT/"partner_exposure_did.json").write_text(json.dumps(results,indent=2,default=float))
    print("\nSaved topic7_partner_exposure_did.csv")


if __name__ == "__main__":
    main()
