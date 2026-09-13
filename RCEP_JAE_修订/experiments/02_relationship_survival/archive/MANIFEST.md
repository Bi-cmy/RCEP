# Failure archive manifest

- `../pap/pap.json`: frozen cohort and estimator design.
- `../pap/amendments.md`: frozen economic pre-trend threshold.
- `../code/01_build_survival_cohort.py`: cohort builder.
- `../code/02_pretrend_gate.py`: exact identification-gate estimator.
- `../data/survival_cohort.parquet`: fixed 2017 relationship cohort.
- `../data/cohort_build_summary.json`: cohort support and source hashes.
- `../data/country_year_support.csv`: country-level support.
- `../data/group_year_support.csv`: RCEP/control survival support.
- `../data/within_firm_overlap.csv`: listed-firm overlap counts.
- `../data/event_study_gate.csv`: all aggregated event-time estimates.
- `../tables/table1_cohort_support.{xlsx,docx,tex}`: support table.
- `../tables/table2_event_study_gate.{xlsx,docx,tex}`: identification table.
- `../figures/fig1_survival_trends.{pdf,png}`: fixed-cohort raw trends.
- `../figures/fig2_event_study_gate.{pdf,png}`: event-study gate.
- `../logs/cohort_build.json`: build log.
- `../logs/pretrend_gate.json`: machine-readable gate result.
- `../logs/pretrend_attempt1_missing_jinja2.md`: preserved technical failure.
