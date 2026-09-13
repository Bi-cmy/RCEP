# RCEP 累积原产地规则对中国·日本·韩国中间品/供应链布局的影响：因果实证文献调研与空白定位

> 调研范围：以 **Crossref API** 为主，覆盖 `rules of origin / cumulative rules / RCEP / China Japan Korea rules of origin / regional value content / cumulation / intermediate goods / supply chain reconfiguration` 等检索词，分两批共 **40 组查询**，去重后 **428 条唯一学术记录**（219 + 209）。
> 结论先行：**针对"RCEP 区域累积原产地规则（RVC40 + 区域/对角累积）"对"中日韩（非东盟）中间品采购与供应链布局"的因果识别，目前在公开文献中基本空白。** 现有研究高度集中于法律/制度评估、宏观 CGE/GTAP 模拟、以及描述性指数分析。

---

## 0. 核心结论（一句话版）

把检索命中的文献按方法学分类后，呈现出清晰的"分层空档"：

| 研究视角 | 代表性文献 | 是否回答"中日韩非东盟中间品/供应链 + 累积规则" | 是否因果识别 |
|---|---|---|---|
| 法律/制度评估（legal review） | Dinh 2021；Hasegawa 2022；ADB 2023；Tresnawati 2024；Kim 2023 | 部分（多止于制度对比） | 否 |
| 宏观模拟（GTAP / CGE / gravity trade cost） | Chung–Park–Park 2022；Ling & Qian 2023；Chen & He 2026 | 否 / 非常间接 | 否（贸易成本方程+均衡模拟，非准实验） |
| 描述性指数（index / 描述性） | YoungHo Kim 2025；Yang & Woo 2022 | 题目最贴近，但无识别 | 否（指数与相关性） |
| 理论+结构模型（微观） | Bombarda & Gamberoni 2013 / 2019 | 方法是标杆，但未用于 RCEP 中日韩 | 理论结构（非实证 DiD） |

**即：没有一个研究把"区域累积原产地规则"作为外生冲击，在企业/产品层面识别其对中日韩中间品互供与供应链重构的影响。**

---

## 1. 检索说明与局限

- **数据源**：Crossref REST API `https://api.crossref.org/works`，`query` / `query.author` 两种模式，按相关性排序，每查询取 12–15 条；限流（429）自动重试 + 节流，全部命中。
- **原始数据**：已保存 `_crossref_raw.json`（219 条）、`_crossref_raw2.json`（209 条）。
- **局限（重要）**：
  1. Crossref 对**中文期刊（CNKI 系）**与部分日文文献覆盖差，本轮环境未配置 web search / 网络爬虫（`FIRECRAWL_API_KEY` 未设），故**中文核心期刊（《国际贸易问题》《财经研究》等）与 CNKI 论文未能直接检索**——这本身只是一个需要补验的覆盖盲区，而非"不存在"的证据。
  2. 韩文期刊（Korea Trade Review、Journal of Korea Trade、Korea International Trade Research、The International Commerce & Law Review 等）摘要常缺失，需人工补全文。
  3. 本次主要是"标题/摘要级"判断；个别文献的识别方法需全文复核。

---

## 2. 文献版图（按方法学分层）

### A. 法律 / 制度评估（Legal & Institutional Review）——数量最多
- **Duy K. Dinh (2021)**，*Global Trade and Customs Journal*，「Rules of Origin in RCEP Agreement: Advancement and Convergence」，DOI: `10.54648/gtcj2021028`。分析 RCEP 原产地规则相较 ATIGA 的"先进性/趋同"。
- **Jitsuya Hasegawa (2022)**，*J. Econ. & Admin. Sciences*，「Evolution of RCEP rules of origin (comparison with ASEAN plus FTAs and recent mega-FTAs/EPAs)」，DOI: `10.1108/jeas-02-2022-0037`。**明确点出**：RCEP 首次把"日本—中国""日本—韩国"这些此前**无任何 EPA/FTA 的安排**纳入同一原产地框——这是 b) 问"首次 FTA"的直接制度背景，但该文只做制度比较，无效应量化。
- **Asian Development Bank (2023)**，「An Assessment of Rules of Origin in RCEP and ASEAN+1 Free Trade Agreements」，DOI: `10.22617/tcs230396-2`。比较 RCEP 与 ASEAN+1 的产品特定规则（PSRO）宽松度，属制度/便利化评估。
- **Tresnawati et al. (2024)**，*Journal of Politics and Law*，「Rules of Origin Within ASEAN and RCEP: Has It Been Resolved?」，DOI: `10.5539/jpl.v18n1p1`。制度信任与自我认证、贸易转移规避。
- **Eun-Bin Kim (2023)**，*Korea International Trade Research*，「The Characteristics and Application of RCEP Rules of Origin」，DOI: `10.16980/jitc.19.2.202304.247`。
- **刘紫松 (2026)**、**李庆林 (2026)** 等中文新媒体期刊：RCEP 原产地规则适用困境、de minimis 条款争议等，均为制度评估。
- **Yap & Medalla (2008)**，「Rules of Origin: Regimes in East Asia and Recommendations for Best Practice」，DOI: `10.62986/dp2008.19`。

### B. 宏观模拟 / 均衡模型（GTAP / CGE / gravity trade cost）——最接近"量化"但非识别
- **★ Chung, Innwon Park & Soonchan Park (2022)**，*Asian Economic Papers*，「Estimating the Impact of Cumulative Rules of Origin on Trade Costs: An Application to Mega-regional FTAs in the Asia-Pacific Region」，DOI: `10.1162/asep_a_00846`。
  **这是最接近"累积原产地规则→贸易成本"的量化研究**：用 gravity 回归估计各类累积性 ROO（bilateral / diagonal / multilateral）对贸易成本的影响，并嵌入 static + capital accumulation CGE，比较 RCEP / CPTPP / FTAAP。**但**：作用于**总体双边贸易流**，未聚焦中间品，未聚焦中日韩（非东盟），且是"贸易成本估计 + 均衡模拟"而非准实验式（DiD/RDD）因果识别。
- **Dan Ling & Kun Qian (2023)**，*SHS Web of Conferences*，「Research on the impact of RCEP rules of origin on China's manufacturing industry」，DOI: `10.1051/shsconf/202316901010`。GTAP 模拟、行业层面。
- **Zhixiang Chen & Junlin He (2026)**，*The Chinese Economy*，「A Study on the Impact of RCEP Rules of Origin on Industrial Relocation in China's Manufacturing Sector」，DOI: `10.1080/10971475.2026.2657735`。产业转移（中国视角）。
- **Peter A. Petri & Michael G. Plummer (2020)**，「Trade War, RCEP and CPTPP: Will East Asia Decouple from the United States?」，DOI: `10.2139/ssrn.3630294`；**Petri (2018)**，「The case for RCEP as Asia's next trade agreement」，DOI: `10.59425/eabc.1541541658`。
- **Armstrong & Drysdale (2022)**，*East Asian Economic Review*，「The Economic Cooperation Potential of East Asia's RCEP Agreement」，DOI: `10.11644/kiep.eaer.2022.26.1.403`。

### C. 描述性 / 指标体系经验研究（Descriptive Empirical）——"中日韩"题目最贴近但无识别
- **★ YoungHo Kim (2025)**，*The Northeast Asia Economic Association of Korea*，「An Empirical Analysis of Industry-Level Supply Chain Structural Changes between Korea and China: Implications for the Reconfiguration of East Asian Regional Value Chains (RVCs)」，DOI: `10.52819/jnes.2025.37.2.1`。
  **题目几乎正中靶心**（韩—中 + 东亚洲区价值链重构 + 非东盟），但方法仅是 CS / CC / TCD / GL 指数等**描述性结构指标**，无回归、无准实验识别、未把"累积规则"作为处理变量。
- **Zhenhua Yang & Kwang-Myung Woo (2022)**，*Regional Industry Review*，「A Study on Impact of the RCEP Agreement on the Industrial Trade between China, Korea and Japan」，DOI: `10.33932/rir.45.4.5`。
- **Dong-hyun Kim & Sang-hoon Lee (2025)**，*Korean-Chinese Social Science Studies*，「A Study on Industrial and Supply Chain Cooperation between Korea and China Using RCEP」，DOI: `10.36527/kcsss.23.1.5`。
- **李健、Dho、Hong (2025)**，*Journal of Korea Trade*，「Optimization of Trade Supply Chain Cooperation between Korean and Chinese Enterprises under the RCEP」；**张林、刘娟 (2023)**，*Modern Economics & Management Forum*「中日韩三边合作路径」。
- **China's Climb of Regional Value Chain under the Framework of RCEP (2023)**，DOI: `10.25236/ajbm.2023.050802`。

### D. 理论 + 微观结构模型（"累积规则"研究的方法论标杆，但未用于 RCEP 中日韩）
- **★ Pamela Bombarda & Elisa Gamberoni (2013)**，*International Economic Review*，「Firm Heterogeneity, Rules of Origin, and Rules of Cumulation」，DOI: `10.1111/j.1468-2354.2012.00734.x`。
  异质性企业 + 国内/国外中间投入采购的模型，证明"双边累积→对角累积"如何放宽 ROO 限制、并排挤最弱生产率出口商。**这是"累积规则 × sourcing"的最强结构框架**，应用于特惠体系一般性，**未落到 RCEP/中日韩**。
- **Bombarda & Gamberoni (2019)**，World Bank RP，「Diagonal Cumulation and Sourcing Decisions」，DOI: `10.1596/1813-9450-8884`；及（同题 WP 另一副本）。
- **Dzmitry Kniahin & Marcelo Olarreaga (2023)**，「Rules of Origin and Exporters' Value-Added」，DOI: `10.2139/ssrn.4340626` / `10.2139/ssrn.4507804`。
- **Soonchan Park (2025)**，「Regime-Wide Rules of Origin and Global Value Chains Trade」，DOI: `10.2139/ssrn.5255514` / `10.2139/ssrn.5255516`。

### E. 其他相关但非直接
- **Ikuo Kuroiwa (2008)**，「Rules of Origin, Local Content and Cumulative Local Content in East Asia: Application of an International Input-Output Analysis」，DOI: `10.1057/9780230227309_4`。I-O 法评估累积本地含量。
- **Honggue Lee (2016)**，*International Economic Journal*，「Do Preferential Rules of Origin Reverse Trade Creation and Trade Diversion?」，DOI: `10.1080/10168737.2016.1204344`。
- **Hansung Daniel Kim & Mee Cho (2014)**，「Impact of Rules of Origin on FTA Utilization in Korean FTAs」，DOI: `10.2139/ssrn.2489806`。韩国 FTA 利用率（偏好利用率侧）。
- **Soo-Chul Kang (2024)**，*Korea Trade Review*，「An Empirical Study on the Economic Effects of Multilateral Cumulation in RCEP」，DOI: `10.22659/ktra.2024.49.2.21`。多边累积经济效益（RCEP 语境，但需全文核实方法与范围）。
- **Yanrong Wang (2026)**，*Journal of Economics and Law*，「RCEP Origin Accumulation Rules: How Vietnamese Textiles Can Arbitrage in the Sino-US Tariff War」，DOI: `10.62517/jel.202614311`。累积规则 × 越南纺织产业链，是"累积规则→供应链整合"少见的**案例式**研究，但聚焦越南+纺织，非中日韩。
- **Athukorala (2015)**，「Global Production Sharing and Asian Trade Patterns: Implications for RCEP」，DOI: `10.1007/978-81-322-2698-7_14`；**Wignaraja (2018)**，「RCEP and Asian economic integration」，DOI: `10.4324/9781351046954-33`；**Innwon Park (2019)**，*Development Policy Review*，「Regional Trade Agreements in East Asia: Past and Future」，DOI: `10.1111/dpr.12418`；**Gong & Lai (2025)**，「Supply Chain Trade Creation and Diversion Effects of Free Trade Agreements」，DOI: `10.2139/ssrn.5849275`。

---

## 3. 三个核心问题的直接回答

### a) 有没有"区域累积原产地规则（RVC40 + regional cumulation）"对"中日韩（非东盟）中间品/供应链"影响的因果识别？
→ **没有（明确空白）。**
- 最接近者 Chung–Park–Park (2022) 以 gravity 估计累积性 ROO 对**贸易成本**的影响，但作用于**总体双边贸易**，不聚焦中间品、不聚焦中日韩非东盟三角，且为贸易成本方程 + CGE 模拟，**非准实验识别**。
- Bombarda & Gamberoni (2013/2019) 提供唯一的"累积规则 × 企业 sourcing"结构模型，但未应用到 RCEP 或中日韩。
- YoungHo Kim (2025) 题目最贴合，但为描述性指数。
**结论：这是"因果识别 × 中日韩非东盟 × 中间品/供应链"的三重空白。**

### b) "首次 FTA + 累积规则"对中日韩中间品互供的影响？
→ **同样缺失。** Hasegawa (2022) 明确说明 RCEP 首次将"中—日""日—韩"纳入同一原产地框架（此前无 EPA/FTA），ADB (2023) 亦确认这一制度断裂，但二者都只做**制度对比**；未见把"首次 FTA + 累积规则"作为处理变量、检验其对中日韩**中间品互供/采购结构**的因果证据。这构成一个识别上极有吸引力的**制度断点（institutional discontinuity）**。

### c) 现有 ROO 文献是否只停留在"制度评估或宏观模拟"？
→ **大体如此。** 428 条记录的分布显示：法律/贸易法类期刊（Global Trade & Customs Journal、J. Politics & Law、Dispute Settlement、E-Commerce Letters、大量韩国国际通商法刊）占据主导，均为制度/合规/政策评估；经济学侧以 GTAP/CGE/gravity 模拟与指数描述为主；**真正的微观因果识别（企业/产品层面 DiD 或事件研究）几乎为空**。Bombarda–Gamberoni 一脉是唯一靠近"识别"的结构/经验工作，但未与中国韩制度细节结合。

---

## 4. 可切入的研究空白（价值定位）

1. **识别设计（建议）**：以 **RCEP 2022-01-01 生效 + 累积原产地规则（RVC40 + 区域/对角累积）** 作为外生冲击，用**企业/行业面板 + 事件研究 / 双重差分**，识别其对**中国对日、对韩（及日韩之间）中间品进口与采购**的影响，或对**中日韩区域价值链参与度/位置（RVC 参与度、前向-后向链接）**的影响。
2. **差异化亮点**：RCEP 首次把"中—日—韩"三极纳入同一可累积原产地框，形成可识别的**制度断裂**；宏观 CGE/模拟与指数研究均无法捕捉企业在断点处的 **switch 采购（sourcing switching）**。Bombarda–Gamberoni 异质性企业模型可作为理论支撑与机制解释。
3. **数据可行性**：中国海关进出口（HS6/HS8 × 日本、韩国）逐月企业-贸易匹配、RCEP 原产地证书(CO)利用率、企业层面采购数据；结构上可用 **ADB MRIO / OECD TiVA / WIOD** 测度中日韩区域价值链参与度。
4. **稳健方法**：以 RVC40 门槛的"**刚好达标 vs 未达标**"构造边界样本（局部处理效应）、shift-share，或以"产品是否被列入区域累积/享受新增优惠"区分处理组。

---

## 5. 主要参考清单（按类别、含 DOI）

### 法律/制度
- Dinh (2021) — 10.54648/gtcj2021028
- Hasegawa (2022) — 10.1108/jeas-02-2022-0037
- ADB (2023) — 10.22617/tcs230396-2
- Tresnawati et al. (2024) — 10.5539/jpl.v18n1p1
- E.-B. Kim (2023) — 10.16980/jitc.19.2.202304.247
- Yap & Medalla (2008) — 10.62986/dp2008.19

### 宏观模拟/均衡
- Chung, Park & Park (2022) — 10.1162/asep_a_00846　**【最相关量化】**
- Ling & Qian (2023) — 10.1051/shsconf/202316901010
- Chen & He (2026) — 10.1080/10971475.2026.2657735
- Petri & Plummer (2020) — 10.2139/ssrn.3630294；Petri (2018) — 10.59425/eabc.1541541658
- Armstrong & Drysdale (2022) — 10.11644/kiep.eaer.2022.26.1.403

### 描述性/中日韩
- YoungHo Kim (2025) — 10.52819/jnes.2025.37.2.1　**【题目最贴近】**
- Yang & Woo (2022) — 10.33932/rir.45.4.5
- Kim & Lee (2025) — 10.36527/kcsss.23.1.5
- 中国区域价值链 (2023) — 10.25236/ajbm.2023.050802

### 理论/微观结构（方法标杆）
- Bombarda & Gamberoni (2013) — 10.1111/j.1468-2354.2012.00734.x　**【方法论标杆】**
- Bombarda & Gamberoni (2019) — 10.1596/1813-9450-8884
- Kniahin & Olarreaga (2023) — 10.2139/ssrn.4340626
- Soonchan Park (2025) — 10.2139/ssrn.5255514

### 相关
- Kuroiwa (2008) — 10.1057/9780230227309_4
- Honggue Lee (2016) — 10.1080/10168737.2016.1204344
- Kim & Cho (2014) — 10.2139/ssrn.2489806
- Kang (2024) — 10.22659/ktra.2024.49.2.21
- Yanrong Wang (2026) — 10.62517/jel.202614311
- Athukorala (2015) — 10.1007/978-81-322-2698-7_14
- Wignaraja (2018) — 10.4324/9781351046954-33
- Innwon Park (2019) — 10.1111/dpr.12418
- Gong & Lai (2025) — 10.2139/ssrn.5849275

---

## 6. 局限与后续建议
- **中文文献盲区**：本环境只能用 Crossref，CNKI/中文核心（《国际贸易问题》《世界经济研究》《财经研究》等）未覆盖，需人工/专门渠道检索中文学界对"RCEP 累积原产地 + 中日韩 + 中间品"的实证进展，以坐实"国内也空白"。
- **韩文摘要缺失**：Korea Trade Review / Journal of Korea Trade 等需 DB 补全文，确认其中是否存在更接近因果的韩文学本研究。
- 建议下一步：用 CNKI、KCI（韩国学术索引）、Web of Science 复检；并对 Chung–Park–Park (2022)、Kang (2024)、YoungHo Kim (2025)、Bombarda–Gamberoni (2013) 做全文精读，以最终坐实空白与选取识别策略。

---

*生成时间：2026-09-03 ｜ 数据源：Crossref API（40 组查询/428 唯一记录）*
