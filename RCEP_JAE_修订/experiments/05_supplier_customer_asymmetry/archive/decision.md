# Decision: INCONCLUSIVE after passing identification gates

Closed: 2026-07-23

## Data support

The frozen balanced panel contains 1,141 listed firms, 21 Asian partner
countries, two relationship roles, and 335,454 observations for 2018-2024.
Every frozen support requirement passed. The weakest country-support cell was
the supplier-role Asian-control pre-period cell, with five positive countries;
210 firms had both supplier and customer links in the pre period and 232 did so
in the post period.

## Identification result

The cohort-specific role event study absorbs firm-country-role,
firm-year-role, and country-year fixed effects and clusters at partner country.
Both frozen pretrend requirements passed:

- Joint lead Wald statistic: 11.1259
- Degrees of freedom: 7
- Joint p-value: 0.1332
- Maximum absolute aggregated lead: 0.005572
- Frozen economic threshold: 0.05

## Static evidence

The preferred staged-timing triple difference is 0.006008 on the asinh-link
scale. Its country-clustered standard error is 0.004012 and its conventional
p-value is 0.1499. The 9,999-draw wild-cluster bootstrap-t p-value is 0.0971.

The decisive frozen evidence check is the country-label randomization test.
Across 9,999 unique assignments preserving 12 countries assigned to 2022,
two assigned to 2023, and seven controls, the two-sided p-value is 0.0976.
The PAP required a value below 0.05 for positive evidence.

The uniform-2022 specification has the same positive sign (0.005995), as does
the any-active-link outcome (0.004995). These sign checks do not override the
failed randomization threshold.

## Decision

This route is identified under its pre-registered diagnostics but does not
provide sufficiently unusual assignment-level evidence to serve as the main
paper design. It is archived as inconclusive, not relabeled as a positive
result. No seed, threshold, sample, country set, or subgroup was changed after
inspection. Because the decisive evidence gate failed, no PPML secondary
outcome, leave-one-country-out selection, mechanism, or heterogeneity search
was used to rescue the result.
