# Annotated PDF revision matrix

Source: `source_materials/main0713_annotated.pdf` (20 pages, modified 2026-07-13).

| PDF page | Marked text or comment | Interpretation | Required revision |
|---:|---|---|---|
| 2 | Full paragraph framing RCEP as the pull force and the US trade war as the push force | US-centered framing is too prominent for the target journal | Remove the push-pull framing from the main contribution. Recast RCEP as an Asian regional-integration policy. Keep US tariffs only as a competing explanation or control. |
| 3 | Circles/checks around the five headline findings; highlight on relationship age | Several claims are too strong and the mechanism portfolio is too thin | Retain only reproduced findings. Replace the single dominant-mediator story with at least two policy-grounded interaction tests. |
| 4 | Underlines on the 20-year tariff schedule and short post-treatment window | The timing argument is useful | Distinguish immediate institutional provisions from phased tariff reductions, while avoiding the unsupported claim that all non-tariff provisions were fully uniform on day one. |
| 7 | Underlines on 2017 and 2024 counts; handwritten note about before/after 2022 | Descriptive changes need a clear pre/post comparison and should not be treated as causal | Add a transparent annual descriptive figure and separate it from the event-study estimates. |
| 9 | Handwritten question: whether the exit-rate interpretation has literature support | The conversion from a 2 pp estimate to an 8-13% decline needs a defensible denominator and citation | Recompute against the observed pre-treatment mean, report the exact denominator, and cite survival/relationship-duration literature or remove the conversion. |
| 10 | Underlines around maintenance/expansion interpretation | The Gelbach labels and policy interpretation are over-claimed | Re-estimate from real observations. Describe maintenance and entry outcomes directly; do not call a mechanical split a causal mechanism without identification. |
| 11 | Questions around the meaning of average relationship age and why it maps to cumulation rules | The causal bridge from duration to regional cumulation is not established | Remove the 91.3% mediation claim unless independently reproduced and identified. Treat pre-existing regional breadth and sourcing direction as mechanism-consistent moderators instead. |
| 12 | Handwritten: report t values and whether there is room to adjust | The null tariff, uncertainty, and diversion tests need full statistics and transparent specification choices | Report coefficient, standard error, t statistic, p value, sample, and fixed effects for every mechanism test. Show the full specification family, including nulls. Do not tune samples for significance. |
| 14 | Handwritten comment that the event-study/placebo drawings are not standard academic figures | Existing figures are descriptive or simulated rather than regression-based | Produce coefficient plots with 95% CIs, omitted base period, zero line, policy line, formal pre-trend test, and a real permutation distribution. |
| 18 | Handwritten: whether a DTA with trade volume is available | Relationship intensity may be measurable | The 20.3 GB relationship DTA exists and has 5,245,665 rows. It contains `revenue_percent`, not trade value or contract value. Only about 10% of customer-supplier relationships are quantified by FactSet, so this can be a limited-sample check, not the main outcome. |

## Additional verbal instructions incorporated

- Parallel trends and placebo tests are gating checks before interpreting downstream estimates.
- Run 5-8 defensible robustness checks and add a cross-fitted double-machine-learning robustness analysis if overlap is adequate.
- Use formal interactions for mechanisms when a two-step or three-step mediation design is unsupported.
- Heterogeneity must include a formal difference test. A pattern where one subgroup is significant and another is not is not itself evidence of a group difference.
- Do not delete observations solely to obtain significance.
