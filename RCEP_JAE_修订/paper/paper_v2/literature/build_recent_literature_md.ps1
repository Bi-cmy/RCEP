$ErrorActionPreference = 'Stop'

$summaries = @{
    2 = '研究区域贸易协定如何影响中国制造业出口产品质量，重点对应贸易协定在企业出口升级和产品质量调整中的作用。该文可用于支持本文关于区域制度整合具有企业层面实际效应的论述。'
    3 = '从多部门视角考察标准对贸易的异质性影响，强调技术标准或制度要求的贸易效应会随行业和产品特征而变化。该研究适合用于说明非关税制度安排不会对所有供应链关系产生同质影响。'
    5 = '使用中国上市工业企业数据研究贸易政策不确定性、发展战略与出口行为之间的关系。该文可为本文的政策不确定性渠道、企业出口调整以及异质性分析提供直接的 JAE 文献依据。'
    6 = '考察贸易协定在印度尼西亚外商直接投资中的作用，关注协定安排与跨境投资决策之间的联系。该文适合用于扩展 RCEP 研究从贸易流量到企业跨境资源配置的文献背景。'
    8 = '利用中国企业层面证据考察互联网使用对海洋制造业出口的影响，体现数字基础设施如何降低信息和交易成本并促进国际市场参与。该研究可用于补充贸易便利化与企业国际联系的讨论。'
    9 = '构建区域双重价值链及生产位置的测度，并以中国为经验对象分析区域与全球价值链中的位置。该文可用于界定 RCEP 背景下区域生产网络和中间品联系的经济含义。'
    10 = '从进口商视角测量企业对区域贸易协定的实际利用率，强调签署协定并不意味着企业自动使用优惠安排。该文与本文关于无法直接观察企业优惠利用、原产地证书和报关行为的限定高度相关。'
    11 = '结合理论与中国证据研究高等教育扩张对出口国内增加值的影响，讨论人力资本如何改变企业嵌入价值链的能力。该文可作为价值链升级和企业能力异质性的补充文献。'
    12 = '研究关税成本与中国企业跨境并购附属机构销售之间的关系，关注贸易成本变化如何影响企业跨境组织形式及海外经营。该文可补充本文由关税变化到企业关系调整的理论链条。'
    13 = '采用全球价值链可计算一般均衡模型评估 RCEP 对区域价值链的影响，提供协议实施前后的宏观和产业层面反事实。该文是本文定位现有 RCEP 研究偏重模拟分析、缺少企业关系证据时的核心引用。'
    14 = '使用中国微观数据重新评估贸易带来的创新收益，讨论企业参与国际贸易与创新表现之间的关系。该文可用于连接贸易开放、企业能力提升与供应链关系稳定性。'
    15 = '研究外资撤出对中国企业全球价值链升级的影响，关注外部资本变化如何重塑企业的价值链位置。该文适合用于讨论供应链重构及企业对外部冲击的调整。'
    16 = '利用柬埔寨的自然实验识别贸易对正规与非正规部门就业的影响，强调贸易政策可能在不同制度部门产生差异化结果。该文可作为本文异质性分析和准自然实验写法的参考。'
    17 = '考察出口退税是否促进中国劳动密集型企业升级，研究政策性贸易成本调整与企业生产升级之间的联系。该文可用于支持关税和税费优惠影响企业行为的机制论述。'
    18 = '分析全球价值链重构对中国与欧洲出口产品结构的影响，关注外部生产网络变化所引致的产品组合调整。该文可用于说明供应链重构不仅影响贸易总量，也影响关系和产品结构。'
    19 = '研究加工出口对中国企业社会保障缴费的影响，并突出供应链压力的作用。该文展示了供应链位置和出口模式可能向企业内部成本与决策传导。'
    20 = '从出口密度和出口国内增加值率两个角度研究出口贸易能否推动中国企业绿色转型。该文可作为企业出口参与具有多维结果、且效果取决于价值链嵌入方式的证据。'
    21 = '研究金融发展如何影响全球价值链位置，并从研发强度角度分析其作用差异。该文可支持融资能力与企业参与复杂跨境生产网络之间的联系。'
    22 = '利用中国数据考察数据政策限制对跨境电子商务的影响，反映数字规则和数据制度如何改变跨境交易成本。该文适合补充 RCEP 数字贸易和贸易便利化条款的讨论。'
    23 = '以签证便利化为切入点研究跨境人员流动与双边价值链联系，说明人员往来成本下降可以加强生产网络连接。该文与本文关系层级结果及贸易便利化机制直接相关。'
    24 = '从五通框架考察一项区域合作倡议与中国食品进口来源多元化之间的关系。该文可用于支持制度合作可能扩大来源范围并降低单一来源依赖的机制。'
    25 = '研究融资约束如何影响中国制造企业与 RCEP 市场建立或维持出口伙伴关系。该文与本文的研究对象最为接近，可直接用于说明 RCEP、融资能力和企业伙伴关系之间的联系。'
    26 = '考察原产地规则、投入品进口与企业创新之间的关系，突出原产地制度通过中间投入选择影响企业表现。该文是本文区域累积规则和中间品机制的重要 JAE 依据。'
    27 = '研究进口需求、数字赋能与企业创新之间的联系，关注进口端市场需求和数字能力的协同作用。该文可补充中间品进口、企业能力与供应链关系调整的讨论。'
    28 = '研究知识产权保护如何影响出口企业的产品结构及出口来源，强调制度环境会改变企业产品组合与市场配置。该文可用于支持 RCEP 非关税制度条款的企业层面意义。'
    29 = '考察工业机器人应用如何影响企业在一般出口和加工出口之间的模式选择。该文说明技术条件会改变企业嵌入国际生产网络的方式，可用于异质性和价值链组织讨论。'
    30 = '分析贸易政策不确定性对世界农产品价格波动的直接与间接影响，明确区分传导渠道。该文既可用于外部冲击讨论，也可参考其机制分解的叙述方式。'
    31 = '研究优惠贸易协定中的环境条款如何影响中国企业出口产品质量，展示协定条款不仅影响关税，也能通过制度约束改变企业表现。该文可用于扩展 RCEP 综合规则的理论背景。'
    32 = '利用中国证据研究区域市场一体化的就业效应，考察区域内部市场壁垒下降所带来的劳动力市场调整。该文可作为区域一体化产生微观经济后果的近期 JAE 证据。'
    33 = '研究制度治理和能源安全如何影响亚洲经济体参与全球价值链，强调治理质量在跨境生产网络中的作用。该文可用于说明价值链参与取决于制度条件而不仅是关税水平。'
    34 = '考察多维风险与中国—东盟清洁生产导向型贸易转型之间的关系，关注风险环境下区域贸易结构的调整。该文可为区域供应链韧性和外部风险讨论提供最新 JAE 证据。'
    35 = '使用双重去偏机器学习识别跨境电子商务综合试验区对城市创业活动的影响。该文与本文采用双重机器学习作稳健性检验的方法部分直接相关，也可参考其对交叉拟合和因果估计的表述。'
    36 = '研究区域贸易协定中的数字贸易规则如何影响全球创新网络，关注协定规则对跨境知识联系和网络结构的作用。该文适合扩展 RCEP 制度内容及网络效应的理论讨论。'
    37 = '利用中国上市公司数据研究数字金融、供应链溢出与企业创新，明确从上下游网络识别企业间传导。该文可为本文采用关系型供应链数据和讨论网络外溢提供近期 JAE 依据。'
    38 = '研究数字经济发展如何改变经济体在全球中间品贸易网络中的位置，重点关注中间品网络和结构重定位。该文可用于支持本文中间品采购及区域生产网络机制。'
    39 = '分析多个优惠制度并存时原产地规则的设计与使用问题，强调制度重叠会影响企业选择优惠安排及其合规成本。该文有助于解释 RCEP 与既有双边协定并存的制度背景。'
    40 = '从企业层面研究区域贸易协定对第三国的影响，关注协定是否引致贸易转移和企业市场重新配置。该文是本文比较 RCEP 与非成员伙伴、讨论替代解释时的重要方法和理论依据。'
    42 = '研究贸易政策不确定性如何改变企业投入品选择，直接连接政策预期、供应商配置和进口投入调整。该文可用于强化本文从政策环境到供应链关系变化的理论机制。'
    44 = '构建区域贸易政策不确定性指标并研究其地区经济后果，强调全国性关税波动会因地区产业与进口结构不同而产生异质影响。该文可为本文的外部政策冲击和异质性控制提供测度思路。'
    45 = '研究进口、供应链联系与企业生产率之间的关系，关注进口投入如何通过供应网络影响企业表现。该文可为本文中间品进口份额机制及供应链关系的经济价值提供证据。'
}

$useOriginalAbstract = @(1, 4, 7, 41, 43, 46, 47, 48)
$metadataPath = Join-Path $PSScriptRoot 'recent_references_metadata.json'
$outputPath = Join-Path $PSScriptRoot 'recent_literature_2022_2026.md'
$records = Get-Content -Raw $metadataPath | ConvertFrom-Json

function Format-Citation($record) {
    $authors = $record.authors -join '; '
    $volumeIssue = ''
    if ($record.volume -and $record.issue) { $volumeIssue = ", $($record.volume)($($record.issue))" }
    elseif ($record.volume) { $volumeIssue = ", $($record.volume)" }
    $locator = if ($record.locator) { ", $($record.locator)" } else { '' }
    return "$authors ($($record.year)). $($record.title). *$($record.journal)*$volumeIssue$locator. https://doi.org/$($record.doi)"
}

function Format-InText($record) {
    $families = @($record.authors | ForEach-Object { ($_ -split ',', 2)[0] })
    if ($families.Count -eq 1) { return "($($families[0]), $($record.year))" }
    if ($families.Count -eq 2) { return "($($families[0]) and $($families[1]), $($record.year))" }
    return "($($families[0]) et al., $($record.year))"
}

$builder = [System.Text.StringBuilder]::new()
[void]$builder.AppendLine('# Recent literature for the RCEP supply-chain paper (2022–2026)')
[void]$builder.AppendLine()
[void]$builder.AppendLine('整理日期：2026-09-04。共 48 篇，其中 38 篇来自 *Journal of Asian Economics*（JAE），10 篇来自其他经济学期刊。出版信息和 DOI 均由 Crossref 核验。引用格式采用与 `elsarticle-harv` 相容的 author–year/Elsevier Harvard 形式。')
[void]$builder.AppendLine()
[void]$builder.AppendLine('摘要说明：开放数据库能够提供完整原始摘要的条目保留英文摘要，并标注来源；其余条目提供基于题名和出版元数据的中文内容概述，不将其表述为出版社原始摘要。2026 年条目均已有 Crossref 正式 DOI 和出版元数据，但在投稿时仍建议再次确认卷期状态。')
[void]$builder.AppendLine()
[void]$builder.AppendLine('## Priority map for the current manuscript')
[void]$builder.AppendLine()
[void]$builder.AppendLine('- Literature review：2、4、5、10、13、25、26、39、40、42、43、47、48。')
[void]$builder.AppendLine('- Hypothesis development：3、12、17、23、24、26、31、39、42、43、45、47、48。')
[void]$builder.AppendLine('- Mechanism analysis：10、23、24、25、26、27、37、38、42、43、45。')
[void]$builder.AppendLine('- Heterogeneity and further analysis：3、5、15、16、30、32、34、40、44。')
[void]$builder.AppendLine('- Double machine learning：35。')
[void]$builder.AppendLine()

foreach ($group in @('JAE', 'Broader')) {
    if ($group -eq 'JAE') {
        [void]$builder.AppendLine('## Journal of Asian Economics')
    } else {
        [void]$builder.AppendLine('## Other closely related journals')
    }
    [void]$builder.AppendLine()

    foreach ($record in ($records | Where-Object group -eq $group)) {
        [void]$builder.AppendLine("### $($record.order). $($record.title)")
        [void]$builder.AppendLine()
        [void]$builder.AppendLine("**Formatted reference:** $(Format-Citation $record)")
        [void]$builder.AppendLine()
        [void]$builder.AppendLine(('**In-text citation:** `{0}`' -f (Format-InText $record)))
        [void]$builder.AppendLine()
        if ($record.semantic_url) {
            [void]$builder.AppendLine(('**Links:** [DOI]({0}) | [Semantic Scholar]({1})' -f $record.doi_url, $record.semantic_url))
        } else {
            [void]$builder.AppendLine(('**Link:** [DOI]({0})' -f $record.doi_url))
        }
        [void]$builder.AppendLine()

        if (($record.order -in $useOriginalAbstract) -and $record.abstract) {
            [void]$builder.AppendLine("**Original abstract ($($record.abstract_source)):** $($record.abstract)")
        } else {
            [void]$builder.AppendLine("**内容摘要（中文整理）：** $($summaries[[int]$record.order])")
        }
        [void]$builder.AppendLine()
    }
}

[System.IO.File]::WriteAllText($outputPath, $builder.ToString(), [System.Text.UTF8Encoding]::new($false))
Write-Host "Saved Markdown to $outputPath"
Write-Host "Entries: $($records.Count); JAE: $(($records | Where-Object group -eq 'JAE').Count)"
