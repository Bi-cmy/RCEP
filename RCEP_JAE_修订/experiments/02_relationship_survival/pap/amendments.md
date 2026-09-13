# PAP amendments

Version 1.0.0 was frozen on 2026-07-23 before cohort support or effect estimates
were inspected.

## Amendment 1: economic pre-trend threshold

Time: 2026-07-23, after cohort support counts but before any event-study or
treatment-effect estimate.

The phrase `economically large pre-differences` is operationalized as any
interaction-weighted pre-treatment event coefficient with absolute magnitude
greater than 0.10 on the survival-probability scale. The identification gate
passes only if the joint pre-trend p-value is at least 0.10 and this maximum
absolute pre-coefficient is at most 0.10.
