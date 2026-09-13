$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$projects = Split-Path -Parent (Split-Path -Parent $root)
$legacy = Get-ChildItem -LiteralPath $projects -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName 'data\cleaned\cn_global_links.parquet')
} | Select-Object -First 1

if (-not $legacy) {
    throw 'Could not locate the legacy project containing data/cleaned/cn_global_links.parquet.'
}

$python = Join-Path $legacy.FullName '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw "Python environment not found: $python"
}

$env:RCEP_LEGACY_ROOT = $legacy.FullName
& $python (Join-Path $root 'code\01_build_pair_year.py')
& $python (Join-Path $root 'code\02_twfe_event_placebo.py')
& $python (Join-Path $root 'code\07_plot_parallel_trends.py')
& $python (Join-Path $root 'code\05_comprehensive_placebo.py')
& $python (Join-Path $root 'code\06_dml_authentic.py')
& $python (Join-Path $root 'code\08_mechanism_analysis.py')
& $python (Join-Path $root 'code\09_heterogeneity_analysis.py')
& $python (Join-Path $root 'code\10_group_heterogeneity_candidates.py')
& $python (Join-Path $root 'code\11_make_group_heterogeneity_table.py')
& $python (Join-Path $root 'code\12_make_robustness_table.py')
& $python (Join-Path $root 'code\14_exclusion_tariff_triple.py')
& $python (Join-Path $root 'code\03_dml_dr_did.py')
& $python (Join-Path $root 'code\04_make_latex_tables.py')

Push-Location (Join-Path $root 'paper')
try {
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
} finally {
    Pop-Location
}

Write-Host "Completed. Manuscript: $(Join-Path $root 'paper\main.pdf')"
