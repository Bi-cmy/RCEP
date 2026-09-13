# RCEP paper revision for Journal of Asian Economics

This directory is the only working location for the revised paper. The earlier project is preserved unchanged.

## Status

- The annotated PDF and reference figure are archived in `source_materials/`.
- Earlier manuscripts are archived in `legacy/` and explicitly marked `UNVERIFIED`.
- No coefficient from a legacy table may enter `paper/main.tex` until its source is recorded in `audit/data_lineage.md` and reproduced by code in this directory.
- The revision emphasizes Asian regional integration. US tariff material is retained only where it is a necessary competing explanation or control.

## Directory map

- `paper/`: submission manuscript and bibliography.
- `code/`: reproducible analysis and figure scripts.
- `data/derived/`: analysis-ready data generated from the original read-only data.
- `results/tables/`: machine-generated regression tables and specification logs.
- `results/figures/`: publication figures in PDF and PNG formats.
- `audit/`: PDF comments, pre-analysis plan, and data lineage.
- `legacy/`: previous drafts for reference only.
- `source_materials/`: annotated PDF and visual reference supplied by the author.

The current main specification uses pair-clustered standard errors. The
partner-country-clustered estimate remains in the specification table as a
sensitivity check. `code/05_comprehensive_placebo.py` generates the expanded
country-label, pair-level, fixed-date, fractional-lead, random-date, mixed,
and event-study lead-window placebo outputs under `results/tables/`.

## Integrity rule

Sample exclusions must be substantively justified, pre-specified, and disclosed. Observations will not be removed because their removal changes statistical significance. Heterogeneity is evaluated with formal interaction or cross-group difference tests, not by comparing stars across separately estimated regressions.
