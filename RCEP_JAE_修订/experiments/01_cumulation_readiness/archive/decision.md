# Decision: FAILED at identification-feasibility gate

Closed: 2026-07-23

No treatment-effect or event-study regression was run. The failure is a design
failure, not a null-result or significance decision.

## Frozen design problem

The primary readiness exposure counts distinct RCEP supplier countries active
during 2017-2019. The frozen event-study design also treats 2017-2020 as its
pre-period. This makes the exposure mechanically define several outcomes in
2017-2019:

- Firms with zero readiness must have zero active RCEP supplier countries and
  zero RCEP supplier-link entries throughout the exposure window.
- Their incumbent-link exit risk set and HHI are undefined in that window.
- Entropy and net link growth are mechanically constrained by the same links
  used to define readiness.

Consequently, a pre-period interaction or trend difference cannot be read as a
falsification test of the identifying assumption. Running the frozen event
study would produce a statistic but not a credible diagnostic.

## Recorded support problems

- 3,695 firms have zero readiness, 237 have one country, and only 59 have two
  or more countries.
- Across the constructed firm-year panel, exit rate is missing for 93.6% of
  rows because no incumbent RCEP supplier link is at risk.
- Conditional supplier-country HHI is missing for 92.1% of rows because no
  active RCEP supplier link is observed.
- The zero-readiness group has no incumbent exit risk set in 2017-2020 and no
  HHI observations in 2017-2019, exactly as implied by the exposure definition.

## Mapping audit

The initial conservative one-to-one rule retained 3,991 listed firms. The
cardinality audit found that ticker `000000` accounts for 12,113 FactSet IDs
and is absent from the listed-firm panel, so it is an invalid placeholder. Only
about 90 real tickers map to multiple FactSet IDs, usually two IDs per ticker.
A future ticker-level design may aggregate those IDs, but the additional firms
cannot repair the mechanical pre-period problem above.

## Preserved artifacts

- Frozen PAP and amendment log.
- Exact schema, mapping, and panel-build scripts.
- Pinned requirements file and environment logs.
- Derived firm-year panel and all support/mapping CSV and JSON outputs.
- The nonzero wrapper exit caused by uv's warning is retained in the stdout log.

## Omitted outputs

Regression tables in XLSX/DOCX/TEX and figures in PDF/PNG were not generated
because the identification-feasibility gate failed before estimation. Producing
publication graphics for a mechanically invalid pre-trend would be misleading.

## Possible future designs, not executed here

1. A new landmark design using readiness measured in 2017 and outcomes from
   2018 onward, with 2018-2021 held out for genuine pre-policy diagnostics.
2. A 2017-2019 readiness measure with analysis beginning in 2020, acknowledging
   that only one clean pre-policy change (2020 to 2021) remains before RCEP.

Either option requires a new numbered folder and a new PAP. Neither is a
post-hoc robustness result for this failed experiment.
