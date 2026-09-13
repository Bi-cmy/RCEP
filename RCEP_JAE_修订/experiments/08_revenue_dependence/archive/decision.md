# Decision: FAILED at moderation pretrend gate

Closed: 2026-07-23

## Data support

The pre-policy quantified panel contains 958 pair-roles and 7,664 annual
observations. It covers 512 RCEP and 446 Asian-control pair-roles across 19
countries. Ninety-six listed firms have quantified relationships in both
groups. Active-status variation and revenue-percentage support pass every
frozen requirement.

The raw-event reconstruction uses only valid percentages from episodes begun
by 2021-12-31. It recodes 7,103 year-4000 open-end markers, retains 2,165
qualifying pre-policy quantified episode rows, and does not use the existing
full-period maximum percentage.

## Identification result

The dynamic model retains both cohort-event main effects and their interaction
with revenue percentage per ten points. It absorbs pair-role and firm-year
fixed effects and clusters by 19 partner countries. The interaction leads fail
both frozen conditions:

- Joint Wald statistic: 247.3308
- Degrees of freedom: 9
- Joint p-value: 3.651e-48
- Maximum absolute aggregated lead: 0.268467
- Frozen economic threshold: 0.02

The result shows that high- and low-percentage quantified relationships had
materially different dynamics well before RCEP. The moderation coefficient
would therefore not have a credible parallel-trends interpretation.

## Decision

No static moderation estimate, bootstrap, country-label randomization,
transition decomposition, robustness check, mechanism, or heterogeneity result
was run. The revenue cutoff, role composition, country set, or sample was not
changed to repair the failed pretrend.
