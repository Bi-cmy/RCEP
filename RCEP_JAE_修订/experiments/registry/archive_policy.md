# Experiment status and archive policy

## Status definitions

- `QUEUED`: registered but no experiment folder has been opened.
- `PLANNED`: folder exists and the PAP is frozen; no confirmatory estimate has
  been inspected.
- `RUNNING`: panel construction or a pre-specified diagnostic is running.
- `PASSED`: identification and evidence gates in the frozen PAP are satisfied.
- `INCONCLUSIVE`: the design is usable but the frozen evidence gate is not met,
  or the available data cannot distinguish a substantively relevant effect.
- `FAILED`: a frozen identification, support, data-quality, or reproducibility
  gate fails.

`FAILED` does not mean the files are disposable. It is an empirical result.

## Required contents of every opened experiment

- `README.md`
- `STATUS.json`
- `pap/pap.json`
- `data/data_contract.json`
- `data/sample_construction.json`
- `code/` with the exact scripts used
- `logs/` with environment and run logs
- `tables/` with XLSX, DOCX, and TEX outputs when estimates are run
- `figures/` with PDF and 300-DPI PNG outputs when figures are run
- `archive/decision.md` when the final status is not `PASSED`

If a planned output is not applicable or cannot be generated, the run log and
decision file must state the reason explicitly.

## Prohibited practices

- Outcome-driven trimming, sample deletion, or country exclusion.
- Choosing a random seed after inspecting a placebo distribution.
- Replacing the stated clustering level because another level produces stars.
- Reporting only the successful outcome from a pre-specified outcome family.
- Interpreting a non-rejection of pre-trends as proof of parallel trends.
