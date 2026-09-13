# Decision: FAILED at pre-trend gate

Closed: 2026-07-23

## Result

The fixed 2017 incumbent supplier-link cohort contains 550 relationships, 272
listed Chinese firms, and 15 observed partner countries. The preferred staged-
timing interaction-weighted event study rejects the joint null that all seven
cohort-specific pre-treatment coefficients equal zero:

- Wald statistic: 76.0632
- Degrees of freedom: 7
- p-value: 8.726e-14
- Maximum absolute aggregated pre-coefficient: 0.0941
- Frozen economic threshold: 0.10

Although the maximum aggregated coefficient is just below the economic
threshold, the frozen gate requires both criteria. The statistical pre-trend
criterion fails decisively.

## Support limitations

- Four registered RCEP countries and two registered Asian controls have no
  fixed-2017 cohort relationships.
- Six of the 15 observed countries have fewer than ten relationships.
- Only 46 listed firms have both RCEP and Asian-control relationships.
- By 2021, only 102 of 387 RCEP relationships and 37 of 163 controls remain in
  the absorbing survival cohort.

These facts do not determine the failure by themselves, but they make
country-cluster inference and within-firm comparisons fragile.

## Stopping decision

The PAP requires stopping when the joint pre-trend test rejects at 10 percent.
Therefore the following were not run:

- Static post-RCEP survival-effect regression.
- 9,999-draw wild cluster bootstrap.
- Country-label randomization inference.
- Leave-one-country-out robustness.
- Mechanism or heterogeneity analysis.

Post-treatment event-time coefficients are present in the mandatory event-study
output but are not interpreted because the identification gate failed.

## Preserved technical failure

The first execution of the pre-trend script stopped before model estimation
because Jinja2 was missing when exporting the cohort-support LaTeX table. The
error and correction are retained in
`logs/pretrend_attempt1_missing_jinja2.md`. The unchanged script then ran in a
pinned environment and exited successfully.

## Output completeness

The cohort-support and event-study tables are retained in XLSX, DOCX, and TEX.
Raw survival and event-study figures are retained in PDF and 300-DPI PNG.
Tables for headline, robustness, mechanism, and heterogeneity estimates were
omitted because the pre-trend gate failed before those stages.
