# Staged revision and pre-analysis plan

## Research question

Does RCEP's entry into force change the probability that Chinese listed firms maintain or establish supply-chain relationships with Asian member-country firms, and are any changes consistent with regional cumulation and trade-facilitation channels?

## Primary estimand

The main sample is a directed company-pair by year panel covering 2017-2024. The outcome equals one when at least one customer or supplier episode for the pair is active at year-end. The principal specification compares foreign RCEP partners with non-RCEP partners, includes pair and year fixed effects, and clusters at the directed pair level. Partner-country clustering is retained as a sensitivity check because policy treatment is assigned at that level. The 2021 event-time coefficient is omitted.

Country-specific entry dates will be used in the preferred treatment variable. A uniform 2022 date is a robustness specification. Indonesia and the Philippines enter the annual treatment indicator in 2023; other foreign RCEP members enter in 2022.

## Gating diagnostics

1. Reconstruct overlapping relationship episodes and publish validation counts.
2. Estimate the event study and conduct a joint Wald test that all pre-treatment coefficients equal zero.
3. Run genuine country-label, pair-level, treatment-time, mixed, and fixed-lead placebo tests with reproducible random seeds.
4. Inspect support and country-level cluster counts before interpreting inference or DML results.

If pre-trends fail materially, the paper will narrow or change its causal claim rather than proceed as though the design passed.

## Mechanism-consistent interaction tests

1. **Regional sourcing breadth:** interact treatment with the Chinese firm's pre-2022 number of distinct RCEP source countries. This is the closest available proxy for whether a firm was positioned to use regional cumulation, but it does not measure certificate utilization.
2. **Input-sourcing direction:** interact treatment with a supplier-relationship indicator. Regional cumulation should be more directly relevant to imported intermediate inputs than to customer links.
3. **Pre-existing relationship tenure (secondary):** interact treatment with pre-2022 relationship age. This tests whether established links respond differently; it will not be labeled mediation.

Each table will report subgroup marginal effects and the triple-interaction difference test. Null results remain in the specification log.

## Heterogeneity

- Firm ownership: private versus state-owned, if ownership data lineage can be verified.
- Firm size: pre-treatment asset size, defined before outcomes are examined.
- RCEP subregion: ASEAN, Japan/Korea, Australia/New Zealand.
- Supplier versus customer relationships.
- Pre-treatment regional breadth.

No split will be selected because it produces the desired pattern of significance.

## Robustness battery

1. Country-specific versus uniform treatment timing.
2. Exclude 2020-2021.
3. Restrict to 2019-2024.
4. Asian non-RCEP control group only.
5. Exclude US partner relationships from the control group.
6. Alternative outcomes: exit among active links and entry among inactive links.
7. Partner-country clustering and two-way clustering where supported.
8. Balanced firm panel / stable relationship-universe checks.
9. Cross-fitted partially linear DML on an aggregated firm-country-year sample, reported only if overlap and nuisance-model diagnostics are acceptable.

## Writing revision

- Lead with RCEP and Asian regional production networks.
- Remove claims that the US trade war creates the paper's core natural experiment.
- Describe rules of origin, customs procedures, SPS measures, and tariff schedules separately and accurately.
- Replace causal-mechanism language with mechanism-consistent evidence unless the mechanism itself is identified.
- Report limitations of FactSet coverage, public-company selection, relationship intensity, and the short post-treatment window.
