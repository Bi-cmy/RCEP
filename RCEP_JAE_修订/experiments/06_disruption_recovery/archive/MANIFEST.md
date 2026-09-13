# Archive manifest

- `pap/`: frozen PAP version 1.0.0 and amendment log.
- `code/01_build_2019_cohort.py`: source validation, cohort construction, and support gate.
- `data/prepandemic_relationship_cohort.parquet`: fixed 2019 cohort panel.
- `data/support_gate.json`: machine-readable failed gate.
- `data/country_cohort_support.csv`: country-level cohort support.
- `data/year_group_support.csv`: annual active, survival, and reactivation counts.
- `data/cohort_build_summary.json`: source hashes, exclusions, and counts.
- `logs/cohort_build.json`: execution record.
- `tables/table1_support_gate.*`: XLSX, DOCX, and LaTeX support table.
- `archive/decision.md`: stopping decision.

Figures and coefficient tables are absent because the frozen data gate stopped
the experiment before any estimation.
