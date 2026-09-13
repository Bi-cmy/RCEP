# Environment audit

Date: 2026-07-23

## Initial check

The system-default `python` could not read Parquet because user-site NumPy
2.4.6 was combined with extensions compiled against NumPy 1.x. Import errors
were raised by pyarrow, numexpr, and bottleneck.

The bundled workspace Python runs in isolated mode but does not currently
include pyarrow. No source data or existing result was modified during this
check.

## Reproducibility decision

The experiment will use a dedicated, pinned environment invoked from its own
run script. Package versions and the full command will be appended here before
panel construction. The broken system environment will not be repaired in
place because doing so could affect unrelated projects.

## Executed environment

The isolated run resolved Python 3.12.7 with NumPy 1.26.4, pandas 2.2.3, and
pyarrow 18.1.0 from `requirements.txt`.

The first panel-build invocation included `uv --no-project`. The Python script
completed, wrote a `build_status: PASSED` JSON, and passed every data assertion,
but PowerShell returned status 1 because it converted uv's harmless
`--no-project` warning on stderr into a native-command error. This wrapper event
is retained in `logs/panel_build_stdout.log`; it is not an empirical failure.

The mapping-cardinality audit was then run without `--no-project` and exited 0.
