# RCEP and supply-chain empirical route assessment

Date: 2026-07-23

## Bottom line

No design supported by the current FactSet annual relationship panel passes
all of the frozen data, identification, assignment-inference, and trend-
sensitivity requirements for a positive causal headline.

The best formal current-data design is Experiment 05's supplier-customer
triple difference. It passes support and pretrend gates, but the preferred
estimate is small (0.00601) and the country-label randomization p-value is
0.0976 rather than below 0.05. It is credible as a null or weak-evidence result,
not as proof that RCEP changed supply chains.

Experiment 09 is the strongest mechanism-linked concept. Its non-overlapping
architecture exposure maps directly to RCEP's unification of rules-of-origin
frameworks, and its frozen static result is negative and unusual under
stratified assignments. However, Experiment 10 shows that the estimate does
not survive an exposure-specific linear trend. It can motivate a supply-chain
consolidation hypothesis but cannot carry the paper's causal claim.

## Why the current data reach a limit

1. Treatment varies across only 21 registered Asian partner countries, while
   RCEP membership is structurally non-random.
2. Annual relationship presence is coarse and provides only 2022-2024 post
   observations.
3. New-entry and within-firm designs have thin control-country or overlap
   support.
4. `revenue_percent` covers a selected subset and exhibits severe differential
   pretrends.
5. FactSet records relationships, not tariff-line exposure, certificate use,
   origin cumulation, shipment value, or customs processing time.

## Recommended paper choices

### Current data only

Reframe the manuscript as an identification-conscious null/limited-evidence
study. Lead with Experiment 05, disclose its randomization p=0.0976, and use
Experiment 09 only as a fragile exploratory consolidation pattern together
with the failed detrended sensitivity. This is honest but may not satisfy a
journal strategy that requires a strong positive causal contribution.

### Stronger positive-design route

Acquire product-country-year or firm-product-country customs data and merge
official RCEP tariff schedules and rules-of-origin eligibility. Freeze
pre-2022 import weights, construct tariff-preference or cumulation exposure at
HS6 level, and estimate post-2022 changes with firm-product, country-year, and
industry-year fixed effects. This directly identifies policy intensity and
provides many product-level shocks instead of relying on 14 country labels.

Priority outcomes are import-source diversification, intermediate-input value,
supplier-country entry, concentration, and value-chain position. A second-best
public-data route is country-sector analysis using OECD ICIO/TiVA or ADB MRIO,
with RCEP tariff commitments matched by sector; its firm-level contribution is
weaker but its policy measurement is substantially better than annual FactSet
relationship presence.

## Integrity decision

No country, firm, industry, relationship, seed, threshold, or subgroup was
changed because it altered significance. Every failed and inconclusive route
remains in its numbered folder with its PAP, code, data, logs, tables, figures,
and stopping reason.
