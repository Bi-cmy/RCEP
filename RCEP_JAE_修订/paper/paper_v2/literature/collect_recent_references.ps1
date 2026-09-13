$ErrorActionPreference = 'Stop'

$selected = @'
JAE|10.1016/j.asieco.2021.101419
JAE|10.1016/j.asieco.2022.101456
JAE|10.1016/j.asieco.2022.101513
JAE|10.1016/j.asieco.2022.101514
JAE|10.1016/j.asieco.2022.101528
JAE|10.1016/j.asieco.2022.101532
JAE|10.1016/j.asieco.2021.101369
JAE|10.1016/j.asieco.2022.101572
JAE|10.1016/j.asieco.2023.101591
JAE|10.1016/j.asieco.2023.101610
JAE|10.1016/j.asieco.2023.101621
JAE|10.1016/j.asieco.2023.101636
JAE|10.1016/j.asieco.2023.101647
JAE|10.1016/j.asieco.2023.101664
JAE|10.1016/j.asieco.2023.101672
JAE|10.1016/j.asieco.2023.101676
JAE|10.1016/j.asieco.2023.101690
JAE|10.1016/j.asieco.2024.101708
JAE|10.1016/j.asieco.2024.101718
JAE|10.1016/j.asieco.2024.101737
JAE|10.1016/j.asieco.2024.101742
JAE|10.1016/j.asieco.2024.101826
JAE|10.1016/j.asieco.2024.101844
JAE|10.1016/j.asieco.2024.101849
JAE|10.1016/j.asieco.2024.101870
JAE|10.1016/j.asieco.2024.101872
JAE|10.1016/j.asieco.2025.101903
JAE|10.1016/j.asieco.2025.101980
JAE|10.1016/j.asieco.2025.102010
JAE|10.1016/j.asieco.2025.102014
JAE|10.1016/j.asieco.2025.102048
JAE|10.1016/j.asieco.2025.102053
JAE|10.1016/j.asieco.2025.102108
JAE|10.1016/j.asieco.2026.102128
JAE|10.1016/j.asieco.2026.102131
JAE|10.1016/j.asieco.2026.102144
JAE|10.1016/j.asieco.2026.102175
JAE|10.1016/j.asieco.2026.102218
Broader|10.1007/s10290-022-00479-w
Broader|10.1016/j.jinteco.2022.103688
Broader|10.1016/j.jinteco.2023.103793
Broader|10.1016/j.jinteco.2024.103909
Broader|10.1016/j.jinteco.2024.103911
Broader|10.1016/j.jinteco.2025.104078
Broader|10.1016/j.worlddev.2023.106371
Broader|10.1111/twec.13468
Broader|10.1111/twec.13557
Broader|10.1257/aer.20211519
'@ -split "\r?\n" | Where-Object { $_ }

function Remove-Markup([string]$text) {
    if (-not $text) { return $null }
    $clean = $text -replace '<[^>]+>', ' '
    $clean = [System.Net.WebUtility]::HtmlDecode($clean)
    return ($clean -replace '\s+', ' ').Trim()
}

function Get-Year($message) {
    if ($message.issued.'date-parts') {
        return [int]$message.issued.'date-parts'[0][0]
    }
    return [int]$message.published.'date-parts'[0][0]
}

function Invoke-JsonWithRetry([string]$uri) {
    for ($attempt = 1; $attempt -le 6; $attempt++) {
        try {
            return Invoke-RestMethod -Uri $uri -Headers @{
                'User-Agent' = 'CodexResearch/1.0'
            } -TimeoutSec 90
        } catch {
            if ($attempt -eq 6) { throw }
            Start-Sleep -Seconds (3 * $attempt)
        }
    }
}

$records = [System.Collections.Generic.List[object]]::new()
$index = 0
foreach ($line in $selected) {
    $index++
    $group, $doi = $line -split '\|', 2
    $encodedDoi = [uri]::EscapeDataString($doi)
    $crossrefUri = "https://api.crossref.org/works/$encodedDoi"
    $crossref = Invoke-JsonWithRetry $crossrefUri
    $message = $crossref.message

    $abstract = Remove-Markup $message.abstract
    $abstractSource = if ($abstract) { 'Crossref' } else { $null }
    $semanticUrl = $null

    if (-not $abstract) {
        $semanticApi = "https://api.semanticscholar.org/graph/v1/paper/DOI:${doi}?fields=title,authors,year,journal,abstract,externalIds,url"
        $jinaUri = "https://r.jina.ai/$semanticApi"
        try {
            $jina = Invoke-WebRequest -Uri $jinaUri -TimeoutSec 90
            $marker = 'Markdown Content:'
            $position = $jina.Content.IndexOf($marker)
            if ($position -ge 0) {
                $jsonText = $jina.Content.Substring($position + $marker.Length).Trim()
                $semantic = $jsonText | ConvertFrom-Json
                if ($semantic.abstract) {
                    $abstract = Remove-Markup $semantic.abstract
                    $abstractSource = 'Semantic Scholar'
                }
                $semanticUrl = $semantic.url
            }
        } catch {
            Write-Warning "Semantic Scholar lookup failed for $doi"
        }
    }

    $authors = @($message.author | ForEach-Object {
        if ($_.family -and $_.given) { "$($_.family), $($_.given)" }
        elseif ($_.family) { $_.family }
        else { $_.name }
    })
    $journal = if ($message.'container-title') { $message.'container-title'[0] } else { '' }
    $title = [System.Net.WebUtility]::HtmlDecode($message.title[0])
    $volume = if ($message.volume) { [string]$message.volume } else { '' }
    $issue = if ($message.issue) { [string]$message.issue } else { '' }
    $locator = if ($message.page) { [string]$message.page } elseif ($message.'article-number') { [string]$message.'article-number' } else { '' }

    $records.Add([pscustomobject]@{
        order = $index
        group = $group
        doi = $doi
        title = $title
        authors = $authors
        year = Get-Year $message
        journal = $journal
        volume = $volume
        issue = $issue
        locator = $locator
        doi_url = "https://doi.org/$doi"
        semantic_url = $semanticUrl
        abstract = $abstract
        abstract_source = $abstractSource
    })

    if (($index % 8) -eq 0) {
        Write-Host "Collected $index of $($selected.Count) records"
    }
    Start-Sleep -Milliseconds 900
}

$outputPath = Join-Path $PSScriptRoot 'recent_references_metadata.json'
$json = $records | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($outputPath, $json, [System.Text.UTF8Encoding]::new($false))
Write-Host "Saved $($records.Count) records to $outputPath"
Write-Host "Original abstracts found: $(($records | Where-Object abstract).Count)"
