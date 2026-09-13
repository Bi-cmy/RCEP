# RCEP supply-chain empirical experiments

This tree is separate from the current paper and its verified results. Each
empirical direction receives an immutable numbered folder before any new
outcome estimate is inspected.

## Workflow

1. Register the direction in `registry/directions.csv`.
2. Create a numbered experiment folder and freeze its PAP.
3. Record the data contract and planned sample-construction steps.
4. Build and validate the analysis panel, recording every exclusion count.
5. Run identification diagnostics before headline regressions.
6. Preserve all code, logs, tables, figures, and machine-readable results.
7. Mark the direction `PASSED`, `FAILED`, or `INCONCLUSIVE` using the
   pre-specified gates. Null and failed runs are never deleted.

## Integrity rules

- No observation may be removed because it changes significance.
- No estimator, outcome definition, random seed, or subgroup may be selected
  after results are viewed.
- All planned outcomes are reported together, with multiple-testing control.
- Separate subgroup stars are not evidence of heterogeneity; an interaction or
  formal cross-group equality test is required.
- A regional sourcing breadth measure is a `regional cumulation readiness
  proxy`, not observed use of RCEP certificates or rules of origin.
- The existing average country-membership DID is not re-labeled as successful.

See `registry/archive_policy.md` for status definitions and required artifacts.
