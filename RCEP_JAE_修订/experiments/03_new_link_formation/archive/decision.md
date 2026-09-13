# Decision: FAILED at data-support gate

Closed: 2026-07-23

No event-study or post-treatment coefficient was estimated.

## Constructed risk set

- 623 listed firms were frozen using active foreign-supplier coverage in 2017.
- 13,083 firm-country dyads were created across 21 frozen Asian countries.
- 552 dyads with a supplier relationship starting by 2017 were excluded under
  the frozen clean-history rule.
- The final discrete-time risk set has 86,554 rows and 398 first-country entry
  events.

## Gate result

Event-count and within-firm-year overlap requirements pass:

- Asian controls: 84 pre-policy and 86 post-policy entry events.
- RCEP candidates: 129 pre-policy and 99 post-policy entry events.
- All years retain 623 firms with candidate dyads in both groups.

The country-support requirement fails. The PAP required at least five countries
with events in every group-period cell. Before RCEP, only Hong Kong, India,
Pakistan, and Taiwan record an Asian-control entry event. Bangladesh, Sri Lanka,
and Mongolia record none. Thus the pre-policy control cell has four event-
contributing country clusters rather than five.

Because treatment is assigned at country-year level, the large number of
firm-country zero observations cannot compensate for the missing country-level
event support. Lowering the threshold after observing the data would violate
the frozen PAP.

## Omitted outputs

The support table is retained in XLSX, DOCX, and TEX. Event-study, headline,
placebo, robustness, mechanism, and heterogeneity tables and figures were not
generated because the data gate failed before estimation.
