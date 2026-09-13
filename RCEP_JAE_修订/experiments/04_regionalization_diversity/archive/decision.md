# Decision: FAILED at pre-trend gate

Closed: 2026-07-23

## Data support

The balanced panel contains 623 listed firms, 21 Asian candidate countries,
13,083 firm-country fixed effects, and 91,581 observations for 2018-2024. All
frozen support gates pass:

- Active links in control-pre, RCEP-pre, control-post, and RCEP-post cells are
  575, 1,436, 617, and 1,386.
- Five control countries and ten RCEP countries have positive links in both
  periods.
- 86 pre-policy and 87 post-policy firms have positive links in both groups.

## Identification result

The cohort-by-event model absorbs firm-country and firm-year fixed effects and
clusters at partner country. The frozen joint pre-trend gate fails:

- Wald statistic: 47.5384
- Degrees of freedom: 7
- p-value: 4.382e-08
- Maximum absolute aggregated lead: 0.003365
- Frozen economic threshold: 0.05

The aggregated leads are economically small and individually imprecise, but the
PAP requires both the joint statistical criterion and the economic criterion.
The statistical criterion rejects, so the experiment cannot be promoted to a
confirmatory result.

## Stopping decision

No static post coefficient, country-label randomization inference, wild-cluster
bootstrap, robustness battery, mechanism, or heterogeneity estimate was run.
Post-event coefficients included in the mandatory event-study table are not
interpreted.

This is the closest current-data design to passing on economic magnitude. A
future equivalence or HonestDiD design would require a new PAP and cannot be
retroactively substituted for this failed gate.
