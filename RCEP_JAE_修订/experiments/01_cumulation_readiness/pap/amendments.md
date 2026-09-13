# PAP amendments

Version 1.0.0 was frozen on 2026-07-23 before new outcome estimates were
inspected.

## Amendment 1: schema-resolved field definitions

Time: 2026-07-23, before panel construction or outcome estimation.

The schema audit found 18 broad `Indcat` groups and 77 detailed industry
groups. `Indcat` is frozen as the industry field for industry-by-year effects
and stratified permutations because the broad grouping provides materially
better within-stratum support. A firm's pre-policy industry is its modal
2017-2019 `Indcat`, with lexicographic tie-breaking.

Permutation strata are pre-policy `Indcat` crossed with global pre-policy mean
asset-size terciles. Missing industry and size form explicit `UNKNOWN` strata;
singleton strata remain fixed and their share is reported.

Transition outcomes cannot be identified in 2017 because 2016 activity is not
in the registered panel. Exit rate, first link entry, first country entry, and
net link growth are therefore missing in 2017. Entropy and HHI retain 2017.
