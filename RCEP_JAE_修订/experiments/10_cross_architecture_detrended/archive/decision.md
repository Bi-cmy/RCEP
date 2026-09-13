# Decision: FAILED trend sensitivity

Closed: 2026-07-23

The exact Experiment 09 panel was cloned without mutation; source and output
SHA-256 hashes are identical. The frozen model allows architecture count to
interact with a linear time trend and estimates an additional post-2022 level
break.

- Exposure-specific linear trend: -0.013193 (SE 0.011841)
- Detrended post break: -0.021191 (SE 0.029286)
- Firm-clustered p-value: 0.4694
- 999-draw stratified-randomization p-value: 0.247

The post break remains negative but is less than half the Experiment 09 static
estimate and is statistically ordinary under both inference procedures. It
fails the frozen survival rule. Experiment 09 therefore cannot be described as
robust to continuation of its only observable pre-policy differential trend.

The first execution attempt stopped before estimation because `pyhdfe` was not
listed in the isolated environment. That failure is retained in
`logs/attempt1_missing_pyhdfe.md`; the dependency was pinned and the unchanged
analysis rerun.
