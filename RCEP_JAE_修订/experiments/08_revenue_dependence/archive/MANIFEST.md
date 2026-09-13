# Archive manifest

- `pap/`: frozen PAP version 1.0.0 and amendment log.
- `code/01_build_quantified_panel.py`: raw-event reconstruction and support gate.
- `code/02_pretrend_gate.py`: dynamic moderation identification gate.
- `data/quantified_relationship_year.parquet`: balanced quantified panel.
- `data/revenue_percent_summary.csv`: group-specific measurement summary.
- `data/support_gate.json`: passed support decision.
- `data/event_study_gate.csv` and `data/cohort_event_terms.csv`: failed dynamic diagnostics.
- `logs/`: panel-build and pretrend machine-readable records.
- `tables/`: support and event-study tables in XLSX, DOCX, and LaTeX.
- `figures/`: raw dependence-gap and event-study plots in PDF and 300-DPI PNG.
- `archive/decision.md`: final stopping rationale.

Static and downstream outputs are absent because the frozen identification gate
stopped the experiment.
