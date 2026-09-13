# Firm-level mechanism screening (2026-09-04)

## Policy basis and observation level

RCEP Chapter 4 links customs cooperation to predictable and expedited release,
advance processing, electronic documentation, and risk management. Chapter 3
allows regional cumulation, and Chapter 12 supports paperless trade. These
provisions motivate firm-level outcomes related to working-capital use,
inventory adjustment, and supplier-network organization.

The existing `intermediate_share` measure is not firm-level. It is China's
strict-BEC5 intermediate imports from partner country `j`, divided by China's
total imports from that partner, in year `t`. The value therefore varies only
at the partner-country--year level and must not be interpreted as firm `i`'s
intermediate-input purchasing.

## Firm-level design used for screening

- Unit: Chinese listed firm-year, 2017--2024.
- Predetermined continuous exposure: active RCEP supplier relationship-years
  divided by all active foreign supplier relationship-years during 2017--2021.
- Predetermined binary exposure: one if the firm had any active RCEP supplier
  relationship during 2017--2021.
- Estimator: firm and year fixed effects.
- Inference: standard errors clustered by firm.
- Financial outcomes: winsorized at the 1st and 99th percentiles.
- Event study: 2021 is the reference year; the reported pre-trend diagnostic is
  a joint Wald test of the 2017--2020 exposure interactions.

The exposure sample contains 1,654 firms, of which 533 have positive
pre-policy RCEP supplier exposure. The matched nonfinancial panel contains up
to 10,730 firm-year observations. The manufacturing subsample contains 1,010
firms and approximately 7,050 observations.

## Main diagnostics

| Outcome and sample | Exposure definition | Post coefficient | Clustered SE | p-value | Joint pre-trend p-value |
|---|---:|---:|---:|---:|---:|
| Net working capital / assets, all firms | Continuous share | -0.0090 | 0.0119 | 0.452 | 0.919 |
| Inventory / assets, all firms | Continuous share | 0.0055 | 0.0055 | 0.318 | 0.312 |
| Log(1 + inventory turnover), all firms | Continuous share | 0.0107 | 0.0409 | 0.794 | 0.651 |
| Operating margin, all firms | Continuous share | 0.0043 | 0.0163 | 0.791 | 0.314 |
| Capital expenditure / assets, all firms | Continuous share | -0.0017 | 0.0030 | 0.556 | 0.772 |
| Inventory / assets, manufacturing | Continuous share | 0.0057 | 0.0048 | 0.239 | 0.216 |
| Inventory / assets, manufacturing | Any pre-policy RCEP supplier | 0.0070 | 0.0031 | 0.026 | 0.841 |
| Log(1 + inventory turnover), manufacturing | Continuous share | -0.0114 | 0.0275 | 0.679 | 0.231 |
| Log(1 + inventory turnover), manufacturing | Any pre-policy RCEP supplier | -0.0466 | 0.0197 | 0.018 | 0.716 |

The binary manufacturing results are consistent with inventory-buffer
accumulation, not faster inventory turnover. They do not survive replacement
of the binary access indicator with continuous pre-policy supplier exposure.
They should therefore be treated as auxiliary and definition-sensitive rather
than as a confirmed mechanism.

## Indirect-effect check

For the manufacturing binary-exposure specification, the firm-level outcome
was the share of the firm's disclosed supplier pairs active in a year. The
treatment-to-inventory coefficient was 0.0068 (`p = 0.028`), but inventory was
not associated with the active-pair share conditional on treatment
(`b = -0.0016`, `p = 0.992`). A 2,000-draw firm-cluster percentile Bootstrap
produced an indirect-effect interval of `[-0.0021, 0.0022]`, with no failed
draws. The interval includes zero. Inventory adjustment therefore does not
pass the requested indirect-effect criterion and should not replace
`intermediate_share` in the current mediation-style table.

## Network outcomes

Firm-level supplier-country breadth, supplier-link counts, equal-weighted
supplier-country HHI, and one-year relationship retention were also examined.
The continuous-exposure estimates were statistically insignificant when their
joint pre-trend tests were satisfactory. Revenue-weighted concentration was
available for only 64 firms because `revenue_percent` is sparsely disclosed,
so it is not a usable main mechanism measure.

## Recommendation

The preferred replacement is a firm-year intermediate-input sourcing measure
constructed from firm-level customs transactions:

`RCEP intermediate-input imports / the firm's total intermediate-input imports`.

This regional sourcing share matches the policy mechanism, varies at the
firm-year level, and can be combined with the relationship outcome without
assigning a national trade composition measure to individual firms. The share
of intermediate goods within a firm's RCEP imports can be reported as a
secondary definition. Both measures require firm--HS--origin--year customs
records and a BEC5 concordance; these records are not present in the current
workspace.

If customs data cannot be obtained, the defensible current-data option is to
drop the intermediate-input indirect-effect claim and report the manufacturing
inventory result only as explicitly auxiliary channel evidence. A pre-policy
annual-report digitalization index can instead be used as heterogeneity in
search capacity, but it is not an outcome caused by RCEP and should not be
presented as a mediator.
