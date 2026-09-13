# Failure archive manifest

- `../pap/pap.json`: frozen design.
- `../pap/amendments.md`: schema-resolved definitions.
- `../code/00_schema_audit.py`: source and industry-field audit.
- `../code/00b_mapping_cardinality.py`: ID-to-ticker cardinality audit.
- `../code/01_build_firm_year.py`: exact failed-design panel builder.
- `../data/firm_year.parquet`: constructed panel retained for audit only.
- `../data/panel_build_summary.json`: build and support summary.
- `../data/exposure_distribution.csv`: exposure support.
- `../data/outcome_support_by_year_group.csv`: risk-set support.
- `../data/mapping_audit.csv`: conservative mapping counts.
- `../data/mapping_many_to_one_top.csv`: many-to-one mapping audit.
- `../logs/schema_audit.json`: schema and package record.
- `../logs/mapping_cardinality.json`: detailed cardinality record.
- `../logs/panel_build.json`: machine-readable build log.
- `../logs/panel_build_stdout.log`: complete first invocation output.
