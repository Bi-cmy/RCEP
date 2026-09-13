# Archive manifest

The experiment is self-contained under this directory.

- `pap/`: frozen version 1.0.0 and amendment log.
- `code/01_build_role_panel.py`: balanced-panel construction and support gate.
- `code/02_pretrend_gate.py`: frozen cohort-specific event-study gate.
- `code/03_static_inference.py`: static DDD, wild bootstrap, and country-label randomization.
- `data/firm_country_role_year.parquet`: analysis panel.
- `data/support_gate.json`: frozen data-support decision.
- `data/event_study_gate.csv`: aggregated event-study estimates.
- `data/cohort_event_terms.csv`: underlying cohort-event estimates.
- `data/wild_cluster_bootstrap_draws.*`: all 9,999 bootstrap draws.
- `data/country_label_randomization_draws.*`: all 9,999 unique label assignments and estimates.
- `logs/`: panel, pretrend, and static-inference machine-readable logs.
- `tables/`: all tables in XLSX, DOCX, and LaTeX formats.
- `figures/`: raw role-gap trends and event study in PDF and 300-DPI PNG.
- `archive/decision.md`: final gate results and stopping rationale.

The frozen PAP did not require later-stage robustness, mechanism, or
heterogeneity outputs after the positive-evidence randomization condition
failed; their omission is therefore explicit rather than silent.
