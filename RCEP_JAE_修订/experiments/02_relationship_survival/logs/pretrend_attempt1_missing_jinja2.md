# Pre-trend run attempt 1: technical failure

Date: 2026-07-23

The script stopped while exporting the pre-regression cohort-support table.
`pandas.DataFrame.to_latex` required Jinja2, which was not listed in the pinned
environment. No PanelOLS model had been instantiated and no coefficient was
estimated.

Resolution: add `Jinja2==3.1.4` to `requirements.txt` and rerun the unchanged
script. This is an environment correction, not a PAP amendment.
