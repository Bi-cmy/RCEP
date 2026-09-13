$ErrorActionPreference = 'Continue'
$workspace = 'C:\Users\97328\Desktop\学习\论文、项目\供应链冲击'
$outputRoot = Join-Path $workspace '文献下载'
$manifestPath = Join-Path $outputRoot '文献下载清单.csv'
$mdFiles = Get-ChildItem -LiteralPath $workspace -Recurse -File -Filter '*.md' -Force | Where-Object { $_.FullName -match '\\RCEP_JAE_修订\\|\\RCEP选题探索\\' -and $_.FullName -match '\\文献调研\\|\\literature\\' }
$doiPattern = '(?i)10\.\d{4,9}/[-._;()/:A-Z0-9]+'
$categoryByName = @{
    'recent_literature_2022_2026.md' = '00_近期文献'; '01_RCEP_实证文献空白.md' = '01_RCEP实证'; '02_网络结构_结果变量文献.md' = '02_网络结构'; '03_双轨推拉_文献.md' = '03_双轨推拉'; '04_原产地累积规则_制度特性.md' = '04_原产地累积'; 'A_中间品累积规则.md' = '05A_中间品累积'; 'B_来源再配置HHI.md' = '05B_来源再配置'; 'C_中日首次FTA.md' = '05C_中日首次FTA'; 'D_便利化调节效应.md' = '05D_贸易便利化'; 'E_中日韩三边FTA.md' = '05E_中日韩FTA'; 'F_累积规则与中日韩.md' = '05F_累积规则与中日韩'; 'G_JAE竞争与适配.md' = '05G_JAE与期刊'
}
$doiCategory = @{}
foreach ($f in $mdFiles) {
    $cat = $categoryByName[$f.Name]
    if (-not $cat) { continue }
    foreach ($doi in ([regex]::Matches((Get-Content -LiteralPath $f.FullName -Raw),$doiPattern) | ForEach-Object { $_.Value.TrimEnd(').,;`').ToLowerInvariant() } | Sort-Object -Unique)) {
        if (-not $doiCategory.ContainsKey($doi)) { $doiCategory[$doi] = $cat }
    }
}
$manifest = @(Import-Csv -LiteralPath $manifestPath)
$manifestByDoi = @{}
foreach ($row in $manifest) { $manifestByDoi[$row.doi] = $row }
$s2Urls = @()
foreach ($f in $mdFiles) { $s2Urls += [regex]::Matches((Get-Content -LiteralPath $f.FullName -Raw),'https?://www\.semanticscholar\.org/paper/[0-9a-f]{40}') | ForEach-Object Value }
$ids = $s2Urls | ForEach-Object { $_.Split('/')[-1] } | Sort-Object -Unique
$added = 0
$checked = 0
foreach ($id in $ids) {
    $checked++
    try {
        $paper = Invoke-RestMethod -Uri "https://api.semanticscholar.org/graph/v1/paper/$id?fields=title,year,openAccessPdf,externalIds" -Headers @{ 'User-Agent' = 'RCEP-literature-download/1.0' } -TimeoutSec 30
        $doi = [string]$paper.externalIds.DOI
        if (-not $doi) { continue }
        $doi = $doi.ToLowerInvariant()
        $oa = [string]$paper.openAccessPdf.url
        if (-not $oa -or -not $manifestByDoi.ContainsKey($doi)) { continue }
        $row = $manifestByDoi[$doi]
        $safeTitle = if ($row.title) { $row.title } else { $paper.title }
        $safeTitle = (($safeTitle -replace '[<>:"/\\|?*\x00-\x1F]', ' ') -replace '\s+', ' ').Trim()
        if ($safeTitle.Length -gt 150) { $safeTitle = $safeTitle.Substring(0,150).Trim() }
        $fileName = "{0} - {1} [{2}].pdf" -f $row.year, $safeTitle, ($doi -replace '[^a-z0-9]+','_')
        $destination = Join-Path (Join-Path $outputRoot $doiCategory[$doi]) $fileName
        if (Test-Path -LiteralPath $destination) { continue }
        $temp = Join-Path $env:TEMP ('rcep-s2-' + [guid]::NewGuid().ToString('N') + '.bin')
        try {
            Invoke-WebRequest -Uri $oa -OutFile $temp -Headers @{ 'User-Agent' = 'Mozilla/5.0 RCEP-literature-download/1.0' } -TimeoutSec 90
            $bytes = [IO.File]::ReadAllBytes($temp)
            if ($bytes.Length -ge 4 -and $bytes[0] -eq 37 -and $bytes[1] -eq 80 -and $bytes[2] -eq 68 -and $bytes[3] -eq 70) {
                Move-Item -LiteralPath $temp -Destination $destination -Force
                $row.status = 'downloaded'
                $row.pdf_url = $oa
                $added++
            }
        } catch {} finally { if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue } }
    } catch {}
    Start-Sleep -Milliseconds 300
}
$manifest | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8
$downloaded = (Get-ChildItem -LiteralPath $outputRoot -Recurse -File -Filter '*.pdf' -Force | Measure-Object).Count
Write-Output "SEMANTIC_SCHOLAR_CHECKED: $checked"
Write-Output "NEWLY_DOWNLOADED: $added"
Write-Output "TOTAL_PDF_FILES: $downloaded"
