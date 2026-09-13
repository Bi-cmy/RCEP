# Data and result lineage audit

## Verified source files

| Item | Location in legacy project | Verified facts | Permitted use |
|---|---|---|---|
| FactSet relationship DTA | `关税+供应链（数据）/全球供应链关系数据Factset/factset_data_dta/factset_revere_relationship/ocmdbmiq9ac1fufn.dta` | 5,245,665 rows; 33 fields; customer/supplier direction, start/end dates, and occasionally `revenue_percent` | Read-only raw source |
| FactSet company DTA | same tree, `factset_revere_company/rhpatvcatg2efdjb.dta` | 3.08 GB company file | Read-only identifier and country source |
| China-related cleaned links | `data/cleaned/cn_global_links.parquet` | 578,142 rows; 364,975 customer/supplier records; 159,026 unique directed company pairs | Primary relationship source, subject to reconstruction checks |
| Firm-year panel | `data/cleaned/ddd_panel.parquet` | 35,978 firm-year rows; 5,689 firms; 2017-2024; 3,143 firms observed in all eight years | Firm-level controls and aggregate link outcomes |
| CSMAR panel | `data/cleaned/csmar_firm_panel.parquet` | 35,978 firm-year rows | Firm-level controls |

## Field limitations

- `revenue_percent` is nonmissing for 51,586 of 578,142 cleaned records (8.9%). FactSet states that approximately 10% of customer-supplier relationships are quantified.
- The DTA does not contain transaction-level trade value or contract amount.
- `end_dt` uses year 4000 as an open-ended relationship marker.
- The cleaned customer/supplier file has multiple records per directed pair (mean 2.30; maximum 173) and 73,131 duplicate pair-start-year records. Pair-year construction must collapse overlapping episodes before estimation.
- `ExposureFentanyl` is missing whenever the industry tariff match is missing; 28.1% of firm-year observations are unmatched. It is not required for the core RCEP design and should not be presented as a stand-alone RCEP mechanism.

## Legacy outputs that are quarantined

| Legacy result | Status | Reason |
|---|---|---|
| Simulated placebo distribution in `code/gen_en_figures.py` | Rejected | Generated with `np.random.normal`; not an empirical permutation test |
| Country-placebo placeholders in `code/robustness_checks.py` | Rejected | Code explicitly writes placeholder zeros and does not retain partner country in the constructed rows |
| Relationship-age mediation, 91.3%, Sobel z=11.48 | Unverified/rejected pending reproduction | Legacy code and manuscript do not establish a valid causal mediation design linking age to RCEP policy exposure |
| Gelbach 52% maintenance / 48% expansion | Unverified/rejected pending reproduction | Must be reproduced from collapsed real relationship episodes and a documented decomposition estimand |
| Headline 2.0 pp baseline effect | Unverified pending reproduction | A value appears in legacy tables, but the complete estimand, risk set, treatment timing, and clustering must be re-estimated |
| Existing event-study figure | Rejected | It plots counts or group means rather than event-time regression coefficients with confidence intervals |
| Existing heterogeneity stars | Unverified | Separate subgroup significance does not test equality across groups |

## Mechanism analysis admitted for the Chinese draft

| Result | Source and construction | Estimand and inference | Limitation |
|---|---|---|---|
| Three policy-linked mechanism paths | `REPC/08_rcep_analysis/01_data_build/processed_trade/china_import_source_hs12_model_panel_2015_2024.parquet`; constructed by `code/08_mechanism_analysis.py` into `results/tables/mechanism_partner_year_metrics.csv` | Three-step fixed-effects path: mechanism on `treated_uniform` ($a$), active relationship on treatment and mechanism ($b$, $c'$), and $ab$ Delta-method product; pair and year fixed effects; relationship-clustered inference | Mechanism variables are partner-country/year aggregates merged to the FactSet relationship panel; they do not observe firm-level preference utilization, origin certificates, or customs time. Country-clustered sensitivity leaves only the source-diversification path significant. |
| Formal heterogeneity | `code/09_heterogeneity_analysis.py` using `data/derived/pair_year.parquet`; outputs `results/tables/heterogeneity_interactions_formal.csv` and `heterogeneity_subregions_formal.csv` | Common interaction models with pair/year FE; moderators (supplier direction, pre-policy RCEP breadth, firm size) are fixed before 2022; member-region coefficients are reported as exploratory | Pair-clustered group differences are precise for supplier direction and pre-policy breadth, but partner-country clustering attenuates both; regional estimates use few treated countries and are not confirmatory. |
| Tariff-exposure alternative-explanation test | `code/14_exclusion_tariff_triple.py`; exposure source `中美供应链STGNN/预处理数据_非供应链/04_模型输入/firm_tariff_exposure.parquet`; outputs `results/tables/exclusion_tariff_triple.csv` and `.json` | Relationship-pair panel with pair and year fixed effects; estimates `Post×RCEP`, `Post×TariffExposure`, and `Post×RCEP×TariffExposure`; exposure fixed at 2019 and sample restricted to firms successfully matched to the exposure file; pair-clustered inference with partner-country sensitivity | The triple interaction is an alternative-explanation test, not a proof of an exclusion restriction. Matching covers only part of the relationship panel, and a null interaction weakens but cannot rule out tariff-driven mechanisms. |

## Admission rule for the revised manuscript

Every numeric claim must have: (1) a source dataset, (2) an executable script in `code/`, (3) a machine-readable output in `results/`, (4) a stated sample and estimand, and (5) a note describing fixed effects and inference. Until all five are present, the claim stays out of `paper/main.tex`.
