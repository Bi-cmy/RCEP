$ErrorActionPreference = 'Continue'

$workspace = 'C:\Users\97328\Desktop\学习\论文、项目\供应链冲击'
$outputRoot = Join-Path $workspace '文献下载'
$sourceFiles = Get-ChildItem -LiteralPath $workspace -Recurse -File -Filter '*.md' -Force | Where-Object {
    $_.FullName -match '\\RCEP_JAE_修订\\|\\RCEP选题探索\\' -and $_.FullName -match '\\文献调研\\|\\literature\\'
}
$doiPattern = '(?i)10\.\d{4,9}/[-._;()/:A-Z0-9]+'
$categoryMap = [ordered]@{
    'recent_literature_2022_2026.md' = '00_近期文献'
    '01_RCEP_实证文献空白.md' = '01_RCEP实证'
    '02_网络结构_结果变量文献.md' = '02_网络结构'
    '03_双轨推拉_文献.md' = '03_双轨推拉'
    '04_原产地累积规则_制度特性.md' = '04_原产地累积'
    'A_中间品累积规则.md' = '05A_中间品累积'
    'B_来源再配置HHI.md' = '05B_来源再配置'
    'C_中日首次FTA.md' = '05C_中日首次FTA'
    'D_便利化调节效应.md' = '05D_贸易便利化'
    'E_中日韩三边FTA.md' = '05E_中日韩FTA'
    'F_累积规则与中日韩.md' = '05F_累积规则与中日韩'
    'G_JAE竞争与适配.md' = '05G_JAE与期刊'
}

New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
foreach ($category in $categoryMap.Values) {
    New-Item -ItemType Directory -Path (Join-Path $outputRoot $category) -Force | Out-Null
}

$records = @{}
foreach ($source in $sourceFiles) {
    $category = $categoryMap[$source.Name]
    if (-not $category) { continue }
    $content = Get-Content -LiteralPath $source.FullName -Raw
    $dois = [regex]::Matches($content, $doiPattern) | ForEach-Object {
        $_.Value.TrimEnd(').,;`').ToLowerInvariant()
    } | Sort-Object -Unique
    foreach ($doi in $dois) {
        if (-not $records.ContainsKey($doi)) {
            $records[$doi] = [ordered]@{ doi = $doi; categories = [System.Collections.Generic.List[string]]::new(); source_files = [System.Collections.Generic.List[string]]::new() }
        }
        if (-not $records[$doi].categories.Contains($category)) { [void]$records[$doi].categories.Add($category) }
        if (-not $records[$doi].source_files.Contains($source.FullName)) { [void]$records[$doi].source_files.Add($source.FullName) }
    }
}

$manifest = [System.Collections.Generic.List[object]]::new()
$index = 0
foreach ($doi in ($records.Keys | Sort-Object)) {
    $index++
    $record = $records[$doi]
    $title = ''
    $year = ''
    $pdfUrl = ''
    $isOa = $false
    $status = 'not_checked'
    $errorText = ''
    try {
        $encoded = [uri]::EscapeDataString("https://doi.org/$doi")
        $work = Invoke-RestMethod -Uri "https://api.openalex.org/works/$encoded" -Headers @{ 'User-Agent' = 'RCEP-literature-download/1.0' } -TimeoutSec 30
        $title = [string]$work.title
        $year = [string]$work.publication_year
        $isOa = [bool]$work.open_access.is_oa
        $locations = @($work.best_oa_location) + @($work.locations)
        foreach ($location in $locations) {
            if ($location -and $location.pdf_url) { $pdfUrl = [string]$location.pdf_url; break }
        }
        if (-not $pdfUrl -and $isOa -and $work.primary_location.landing_page_url) { $pdfUrl = [string]$work.primary_location.landing_page_url }
        if ($pdfUrl) {
            $safeTitle = if ($title) { $title } else { $doi }
            $safeTitle = $safeTitle -replace '[<>:"/\\|?*\x00-\x1F]', ' '
            $safeTitle = ($safeTitle -replace '\s+', ' ').Trim()
            if ($safeTitle.Length -gt 150) { $safeTitle = $safeTitle.Substring(0,150).Trim() }
            $fileName = "{0} - {1} [{2}].pdf" -f $year, $safeTitle, ($doi -replace '[^a-z0-9]+','_')
            $category = $record.categories[0]
            $destination = Join-Path (Join-Path $outputRoot $category) $fileName
            if (Test-Path -LiteralPath $destination) {
                $status = 'already_present'
            } else {
                $temp = Join-Path $env:TEMP ('rcep-paper-' + [guid]::NewGuid().ToString('N') + '.bin')
                try {
                    Invoke-WebRequest -Uri $pdfUrl -OutFile $temp -Headers @{ 'User-Agent' = 'Mozilla/5.0 RCEP-literature-download/1.0' } -TimeoutSec 90
                    $bytes = [IO.File]::ReadAllBytes($temp)
                    $isPdf = $bytes.Length -ge 4 -and $bytes[0] -eq 37 -and $bytes[1] -eq 80 -and $bytes[2] -eq 68 -and $bytes[3] -eq 70
                    if ($isPdf) {
                        Move-Item -LiteralPath $temp -Destination $destination -Force
                        $status = 'downloaded'
                    } else {
                        $status = 'oa_link_not_pdf'
                    }
                } catch { $status = 'download_failed'; $errorText = $_.Exception.Message }
                finally { if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue } }
            }
        } elseif ($isOa) { $status = 'oa_no_pdf_url' } else { $status = 'no_free_pdf_found' }
    } catch { $status = 'metadata_failed'; $errorText = $_.Exception.Message }
    $manifest.Add([pscustomobject]@{
        doi = $doi
        title = $title
        year = $year
        categories = ($record.categories -join '; ')
        source_files = ($record.source_files -join '; ')
        openalex_is_oa = $isOa
        pdf_url = $pdfUrl
        status = $status
        error = $errorText
    })
    if (($index % 10) -eq 0) { Write-Output "PROGRESS: $index / $($records.Count)" }
    Start-Sleep -Milliseconds 150
}

$manifest | Export-Csv -LiteralPath (Join-Path $outputRoot '文献下载清单.csv') -NoTypeInformation -Encoding UTF8
$summary = $manifest | Group-Object status | Sort-Object Name | ForEach-Object { "- $($_.Name): $($_.Count)" }
$readme = @(
    '# 免费文献下载目录',
    '',
    '本目录只保存通过公开链接实际下载到的 PDF。未找到免费 PDF、链接不是 PDF 或下载失败的文献，记录在 `文献下载清单.csv` 中。',
    '',
    '每个 DOI 只下载一份，重复出现的主题记录在清单的 `categories` 字段中。',
    '',
    '## 下载结果',
    '',
    $summary,
    '',
    '来源 Markdown 文件位于工作区的 `RCEP_JAE_修订/文献调研`、`RCEP_JAE_修订/paper/paper_v2/literature` 和 `RCEP选题探索/文献调研`。'
)
$readme | Set-Content -LiteralPath (Join-Path $outputRoot 'README.md') -Encoding UTF8
Write-Output "TOTAL_DOI: $($records.Count)"
$manifest | Group-Object status | Sort-Object Name | ForEach-Object { Write-Output "$($_.Name): $($_.Count)" }
