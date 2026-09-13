# Archive manifest

- `pap/`: frozen PAP version 1.0.0 and amendment log.
- `data/institutional_architecture_mapping.csv`: frozen country-to-architecture mapping.
- `code/01_build_architecture_panel.py`: mapping, panel construction, and support gate.
- `data/architecture_firm_year.parquet`: five-year analysis candidate panel.
- `data/exposure_distribution.csv`: frozen exposure support.
- `data/year_outcome_support.csv`: annual primary-outcome support.
- `data/support_gate.json`: machine-readable failed decision.
- `data/panel_build_summary.json` and `logs/panel_build.json`: hashes and execution record.
- `tables/table1_support_gate.*`: XLSX, DOCX, and LaTeX support table.
- `archive/decision.md`: final stopping rationale.

Figures and coefficient tables are absent because the frozen support gate
stopped estimation.
