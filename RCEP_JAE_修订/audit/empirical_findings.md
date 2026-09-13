# Empirical gate report

Run date: 2026-07-23. All results below are generated from `data/derived/pair_year.parquet` by scripts in `code/`.

## Gate decisions

| Gate | Result | Decision |
|---|---:|---|
| Baseline TWFE, pair clusters (new main specification) | 0.0136 (SE 0.0040), p=0.001 | Positive and statistically precise under relationship-level inference |
| Baseline TWFE, partner-country clusters (sensitivity) | 0.0136 (SE 0.0203), p=0.503 | Country-level inference remains imprecise |
| Country-specific entry timing | 0.0144 (SE 0.0202), p=0.477 | Same conclusion |
| Joint pre-treatment event coefficients, pair clusters | Wald p=0.078 | Does not reject at 5%, but remains marginal at 10% |
| False treatment years 2019/2020/2021 | p=0.475/0.752/0.655 | These timing placebos do not reject |
| 499 country-label permutations, k=14 | Rank p=0.774 | Fails: the observed RCEP estimate is ordinary relative to randomly selected 14-country groups |
| Fixed-group timing placebo, false 2019 | p=0.039 | Significant false-year result indicates temporal sensitivity |
| Fixed leads 1, 2/3, 1/2, 1/3 years | coefficient 0.0051 in all cases | Fractional leads collapse to 2021 in annual data |
| Pair-level random spatial placebo | rank p=0.002 | Exploratory result is unusually large relative to pair-shuffled assignments |
| Random false dates (999 draws) | mean 0.0056, rank p=0.001 | Temporal distribution is not a clean null because annual cutoffs are coarse |
| Cross-fitted doubly robust DID | 0.0065 (cluster bootstrap SE 0.0088), p=0.446 | Does not support the old headline effect |

The paper therefore does not pass the author's rule that parallel trends and placebo tests must validate the design before mechanisms and heterogeneity are interpreted.

## Why both cluster levels are reported

Clustering at the relationship-pair level produces 0.0136 (SE 0.0040), p=0.0008 and is now the requested main specification. RCEP treatment is assigned by partner country and year, so relationships sharing a partner country can face common shocks. Partner-country clustering therefore remains a required sensitivity check and produces SE 0.0203 and p=0.503. The two results answer different sampling questions and should not be conflated.

## Exploratory interactions

| Moderator | Difference in treatment effects | p-value | Interpretation |
|---|---:|---:|---|
| Foreign supplier vs customer | 0.0327 | 0.328 | No formal supplier/customer difference |
| Pre-policy regional sourcing breadth (2+ countries) | 0.0480 | 0.107 | Suggestive, but not conventionally significant |
| Older pre-policy relationship | 0.0027 | 0.863 | No tenure difference; does not support the old relationship-age mechanism |
| Large pre-policy firm | 0.0121 | 0.749 | No formal size difference |

Subregion coefficients differ sharply (Japan/Korea positive, ASEAN negative and imprecise, Australia/New Zealand negative), and the asymptotic equality test rejects. These estimates are exploratory because each treated subregion contains very few country clusters and the aggregate identification gates fail. They require small-cluster procedures and an independently justified design before substantive interpretation.

## Manuscript consequences

- Delete the 2.0 percentage-point significant causal effect.
- Delete the 52/48 Gelbach causal-mechanism claim.
- Delete the 91.3% relationship-age mediation claim and Sobel statistic.
- Do not describe a mechanism as proven. Report the regional-breadth and supplier interactions as mechanism-consistent tests with null formal differences.
- Do not select or delete observations to obtain significance.
- Reframe the current document as an identification-conscious working paper. It is not submission-ready as a positive causal-effect paper.
