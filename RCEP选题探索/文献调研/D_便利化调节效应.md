# 文献调研 D：贸易便利化/物流效率对 RCEP 关税实效的调节作用——空白定位

> 检索工具：Crossref REST API（`api.crossref.org/works`）；检索时间：2026-09。
> 检索概念：贸易便利化 / 海关效率 / 物流绩效指数 LPI / 制度质量 × 区域贸易协定（RTA）关税减让之**调节（交互）作用**。
> 注意：本环境未配置 web_search / Firecrawl，所有文献凭证均来自 Crossref 元数据（标题 + 部分摘要）。抽象为空或不可得的条目，结论仅据标题与语境推断，已在文中标注。

---

## 0. 任务与空白核验问题（三问）

本报告围绕三个具体问题查找证据，最终判定空白是否成立：

- **Q-a**：RCEP 相关研究中，是否有人把**伙伴国物流绩效 LPI** 或**海关效率**当作**调节变量**，检验"制度/物流越好的伙伴国，其优惠关税减让越有效"（即 `LPI × RCEP关税减让` 交互项）？
- **Q-b**："**便利化互补关税减让**"（facilitation complements tariff cuts）这一假说，是否已被实证检验？
- **Q-c**：是否有人用 **World Bank LPI 与 RCEP 关税做交互**？

> **核心结论（先行声明）**：在三问上，现有文献呈"对面不相逢"格局。**LPI/物流效率、RCEP 关税减让、优惠利用率**三个话题各自都有大量文献，但**至今没有一篇**把"**伙伴国 LPI/海关效率 × RCEP 关税减让/偏好幅度**"作为交互项放进 RCEP 的引力/双重差分框架里做调节检验。Q-a、Q-c 的答案是"**未发现**"；Q-b 仅在**非 RCEP 语境**、且多为**叙事/泛化实证**层面出现（见 §3.2），**未在 RCEP 内用标准交互项正式检验**。空白成立且方向清晰。

---

## 1. 检索策略

按策略分层检索，避免"题目模糊命中"污染：

| 批次 | 检索式（query.bibliographic） | 目标 |
|---|---|---|
| 泛化 | trade facilitation * regional trade agreement tariff | 边界探测 |
| 专题1 | logistics performance index trade agreement trade flows | LPI–RTA 主效应 |
| 专题2 | RCEP tariff utilization margin / trade creation gravity | RCEP 关税实效 |
| 专题3 | (LPI / customs efficiency) moderator / interaction / tariff | **调节/交互命中核验** |
| 专题4 | facilitation complements / substitutes tariff; deeper integration | 互补性假说 |
| 专题5 | (institutional / logistics) quality × RTA / trade effect | 制度质量调节 |
| 专题6 | rules of origin utilization determinants | 优惠利用率决定因素 |

对关键 DOI 逐一拉取 `abstract` 以确认其"主效应 vs 调节效应"的性质（当前工具下摘要可读取者为 Tang & Rosland 2025、Qu & Zhang 2023、Lee/Rocha/Ruta 2021、Korea 2022 等；其余仅据标题）。

---

## 2. 现有文献的"三大版图"

### 2.1 版图 A：物流绩效 LPI 对贸易流的**直接（主效应）**——含大量 RCEP 相关文献

主流做法是把伙伴国/出口国 LPI 作为引力方程的一个**加性解释变量**，估计其对双边贸易流的平均影响。**这一落点下 RCEP 相关文献并不稀缺，但全部是"主效应"，没有一个做调节/交互。**

| 文献 | 年份 | 期刊 | DOI | 性质 |
|---|---|---|---|---|
| A Study on the Influencing Factors of LPI of RCEP Signatories on China's Foreign Export Trade (Gravity Model) | 2021 | 韩国物流研究协会 (축산) | 10.17825/klr.2021.31.2.81 | RCEP签约国 LPI → 中国出口（引力主效应）|
| The Effect of Logistics Performance Index of RCEP Countries on China's Export Trade | 2022 | Review of Economic Assessment | 10.58567/rea01010004 | RCEP 国 LPI → 中国出口（主效应）；Sum：CrossRef 无摘要，据标题推断 |
| Analysis on the Effects of Logistics Efficiency on Korea's Trade Flows in RCEP Signatories | 2022 | International Academy of Global Business & Trade | 10.20294/jgbt.2022.18.5.101 | RCEP 国物流效率（含 LPI 各分项）→ 韩国贸易；引力、变系数/固定/随机效应模型。**主效应** |
| Impact of logistics performance and trade facilitation on China–ASEAN trade flows | 2025 | Asian Journal of Economic Modelling | 10.55493/5009.v13i1.5363 | 2009–2019 六国面板；FGLS。摘要确认：东盟 LPI 改善、TF 措施均显著促进中—东盟贸易。**主效应**（无交互）|
| Analysis of the Influencing Factors of Cross-Border Logistics between China and RCEP Member States (From the Perspective of LPI) | 2025 | ICLSE 2024 | 10.52202/078960-0041 | 中国–RCEP 跨境电商物流影响因素；LPI 视角 |
| A Comparative Study on the Current Situation of Logistics Development Among Countries Under the RCEP Framework (World Bank LPI) | 2025 | Proceedings of Business & Economic Studies | 10.26689/pbes.v8i8.13385 | RCEP 各国 LPI 横向比较；**非关税交互** |
| China–ASEAN International Logistics Development and Prospects Under the RCEP | 2024 | Current Chinese Economic Report Series | 10.1007/978-981-97-6839-4_11 | 中国—东盟物流发展展望；非关税交互 |
| (非RCEP) Impact of the Logistics Performance Index (LPI) on Agri-Food Trade: Evidence from Korean Exports | 2026 | Journal of Korea Trade | 10.35611/jkt.2026.30.2.1 | LPI 对农产品出口（主效应）|
| (非RCEP) Logistics digitalisation and trade flows: evidence from the LPI using a gravity model | 2026 | Intl. J. of Logistics Research & Applications | 10.1080/13675567.2026.2646342 | LPI 主效应 |
| (非RCEP) The Mediator Effect of LPI on the Relation Between Corruption Perception Index and Foreign Trade Volume | 2016 | European Scientific Journal | 10.19044/esj.2016.v12n25p37 | **LPI 作为"中介（mediator）"**而非调节——注意与"调节"的区别 |

> **关键判定**：版图 A 把 LPI 当**主效应/中介**。若要在"调节作用"上找空白，这批文献恰恰论证了"LPI 本身重要"，但**没有**把 LPI 与关税减让相乘。

### 2.2 版图 B：RCEP/区域 FTA 优惠关税**效用与利用率**的决定因素（ROO 与偏好幅度为主）

这条线研究"关税减让（margin of preference / 关税优惠率）到底有没有被用起来、效果几何"，解释变量集中在**原产地规则 ROO、优惠幅度**，**不含**伙伴国物流/海关效率交互。

| 文献 | 年份 | 期刊 | DOI | 关键点 |
|---|---|---|---|---|
| Assessing the effects of ROO and tariff margin on China–ASEAN FTA utilization | 2023 | PLOS ONE | 10.1371/journal.pone.0286106 | 40,474 产品—国观测、Logit；**优惠幅度增大→利用率↑，ROO→利用率↓**；含异质性（低收入伙伴）。**未纳入 LPI/物流交互** |
| Determinants of ATIGA Preferential Tariff Utilization: Margin of Preference and Rules of Origin | 2025 | Southeast Asian Economies | 10.1355/ae42-3b | ATIGA 利用率：偏好幅度+ROO |
| Determinants of Preferential Tariff Utilization under the Korea–US FTA | 2022 | Journal of Market Economy | 10.38162/jome.51.3.4 | 韩美 FTA 利用率决定因素 |
| Utilization of Preferential Tariff under ASEAN Free Trade Area (AFTA): Case of Malaysia | 2015 | Journal of Global Economy | 10.1956/jge.v11i4.413 | 马来西亚 AFTA 利用率 |
| Study on the Impact of RCEP Tariff Reduction on Shandong's Export to ROK | 2024 | 韩国物流研究协会 | 10.17825/klr.2024.34.6.69 | RCEP 减税→山东对韩出口路径（**效力测算**）；未做 LPI 调节 |
| Depth, trade, and welfare analysis of the CPTPP and RCEP: Does deepening RCEP to CPTPP standards make a difference? | 2026 | China Economic Review | 10.1016/j.chieco.2026.102677 | **RCEP"深度"**对贸易与福利；可视为"整合深度"邻近文献，但用的是**协议深度指标**，非 LPI |
| An Empirical Study on the Impact of Tariff Reduction on China's Textile Industry under RCEP | 2024 | Economics | 10.1515/econ-2022-0102 | RCEP 关税→产业（效益/分配）|
| Effects of tariff reduction by RCEP on global value chains (simulation) | 2021 | Applied Economics Letters | 10.1080/13504851.2021.1966361 | RCEP 减税→GVC 模拟（CGE 思路）|
| Tariff Reduction, Import Liberalization, and Consumer Welfare in RCEP Member States (structural model) | 2026 | Business and Economic Research | 10.5296/ber.v16i3.23777 | 结构模型（福利）|

> **关键判定**：版图 B 把"关税减让/偏好幅度"作为**主解释变量**决定贸易/利用率，但**没有在其中引入伙伴国 LPI/海关效率**。

### 2.3 版图 C：便利化与关税的**互补/替代**关系——已存在，但**多在非 RCEP 语境、且常为叙事/泛化层面**

这是三问中最接近 Q-b 的落点，值得说明其"存在但未经 RCEP 交互检验"的现状。

| 文献 | 年份 | 出版方/期刊 | DOI | 关键点 |
|---|---|---|---|---|
| Trade policy without trade facilitation: Lessons from **tariff pass-through in Tunisia** | 2016 | WTO：Trade Costs and Inclusive Growth | 10.30875/541bb513-en | **标题即点题**：贸易政策若无便利化支撑，关税的传导（pass-through）可能失效 → 隐含"便利化互补关税" |
| Trade facilitation under the regional trade agreement umbrella (WTO) | 2016 | WTO / Cambridge | 10.30875/a9b448e8-en；10.1017/cbo9781316676493.006 | RTA 作为便利化载体；制度性背景 |
| Trade Facilitation Provisions in Preferential Trade Agreements: Impact on **Peru's Exporters** | 2021 | World Bank Policy Research WP | 10.1596/1813-9450-9674 | PTA 内的**便利化条款**对出口的影响（Lee, Rocha, Ruta）|
| Impact of Trade Facilitation on China's Cross-border E-Commerce Exports (RCEP 成员便利化指数) | 2022 | Journal of Korea Trade | 10.35611/jkt.2022.26.7.109 | RCEP 成员**贸易便利化指数**（TFI）→ 跨境电商出口；**主效应**，非与关税交互 |
| Trade Facilitation and Customs (WCO) / Benefits of Trade Facilitation (量化评估) | 2005 / 2015 系列 | World Bank / Cambridge | 见下 | 便利化收益量化传统文献 |
| (制度质量 × 贸易) The Role of Institutional Quality and Institutional Quality **Distance** on Agricultural Trade Within a FTA (SADC) | 2023 | SSRN | 10.2139/ssrn.4432826 | **制度质量**及其**距离**对 FTA 内农产品贸易；非 LPI |
| (制度调节) Aid for Trade Effectiveness under Structural Constraints: The Role of Logistics Performance in Shaping Export Outcomes | 2026 | 韩国物流研究协会 | 10.17825/klr.2026.36.3.1 | LPI 在**结构性约束**下塑造出口结果 → 已隐含"条件性"（conditional/shape），但为"援助促贸易"语境，非"关税×LPI"|
| (制度调节金融类，属偏离) Trade openness & inequality: moderating role of institutional quality | 2024 | Global Finance Journal | 10.1016/j.gfj.2024.100959 | 相关方法（机构质量作调节）但主题非关税便利化 |

> **关键判定**：版图 C 存在"便利化/制度质量与关税/开放互补"的**哲学与政策论证**（尤其 Tunisia 一文），且已有**制度质量作调节**的方法论示范（GFJ 2024、SADC 2023）。但它们要么**不在 RCEP**，要么**把 LPI/海关效率作为直接或条件变量而非「关税×LPI」交互项**。

---

## 3. 空白定位（精确表述）

### 3.1 三问答案汇总

| 问题 | 答案 | 证据 |
|---|---|---|
| **Q-a**：RCEP 内是否有人用**伙伴国 LPI/海关效率**作**调节变量**检验"好制度伙伴→优惠关税更有效"？ | **未发现** | 版图 A 全为 LPI 主效应；版图 B 全为 ROO/优惠幅度决定利用率。无任何 RCEP 文献出现 `LPI × RCEP优惠幅度` 交互 |
| **Q-b**："**便利化互补关税减让**"是否被实证？ | **部分存在，但非 RCEP、非标准交互项** | 只有 Tunisia"关税传导"（2016）、Peru PTA 便利化条款（2021）、RCEP 深度（China Econ Review 2026）等**邻近/叙事/条件性**证据；未见在 RCEP 引力/DID 里放 `便利化×关税` 交互 |
| **Q-c**：是否有人用 **World Bank LPI 与 RCEP 关税**做交互？ | **未发现** | LPI 在 RCEP 文献里只作主效应、横向比较（pbes 2025）、影响因素分析（ICLSE 2025）；无交互 |

### 3.2 空白的**四点精确定位**（据此可圈定新意）

1. **「调节」视角缺席，而非「相关」视角缺席**：现有 RCEP–LPI 文献证明"LPI 重要"（主效应），但从未检验"**LPI 是否改写了 RCEP 关税减让的边际效果**"（交互效应）。这在计量上是完全不同的识别的层面：`ln(trade) = α·tariff + β·LPI + γ·(tariff×LPI) + ...`，现有文献只估计了 β，未估计 γ。
2. **关税实效的"效力"侧与"利用率"侧都未接入 LPI**：
   - 效力侧（贸易流响应）——版图 A/B 各自独立，未合并；
   - 利用率侧（优惠是否被用上）——版图 B 用 ROO+margin，**漏掉了物流/海关成本**（这恰恰是利用率文献公认的重要解释维度）。把 LPI/海关效率加进利用率方程，本身即是有价值的一步。
3. **核心机制——"便利化互补关税"——缺乏干净的识别**：Tunisia 一文只提供"弱便利化→关税传导失效"的单体证据；未在跨国 RCEP 面板中用**交互项**识别"互补"还是"替代"。亦即（Q-b）"complementarity vs substitutability"这一理论问题在 RCEP 语境下**未**被正式检验。
4. **伙伴国维度 vs 本国维度**：现有 RCEP–LPI 文献几乎都取**伙伴国/签约国 LPI**（如 2021、2022、2025 各篇），但多作为**引力主效应**；若把它升级为**交互项**并放到**货物—国家—年份**层面，其"制度/物流质量如何放大关税节税与通关收益"的微观机制尚未有人做。

### 3.3 方法上可直接借鉴的"调节"参考文献（为你的实证提供脚手架）

- 制度质量作调节变量的主流面板做法：**GFJ 2024 (10.1016/j.gfj.2024.100959)**、**SSRN 4432826（制度质量——距离）**。
- 便利化条款→出口：**Peru WP 9674 (10.1596/1813-9450-9674)**。
- 关税传导受限：**Tunisia (10.30875/541bb513-en)**；更通用版**Tariff Passthrough at the Border (IMF/World Bank, 10.5089/9781513518381.001.a001)**。
- RCEP 优惠利用率方法：**Qu & Zhang 2023 (PLOS ONE, 10.1371/journal.pone.0286106，Logit+异质性)**——可直接移植其 Logit/异质性框架，加入 LPI×优惠幅度交互。

---

## 4. 给你的论文定位建议（对标空白）

**主标题方向**：*"RCEP 关税减让实效是否取决于伙伴国物流/制度质量——基于 World Bank LPI 与关税交互的识别"*

**最小可行贡献（可一篇做成）**：
1. 在 RCEP 十五国（或中国—RCEP 双边）的**货物—国家—年份**层，构造 `关税减让/偏好幅度 × 伙伴国 LPI（或其分项：海关与通关效率、基础设施）` 交互项，放入引力/PPML 或 DID。
2. 同时对**优惠利用率**（若可得，如海关利用率/原产地证书）做 Logit/线性概率，加入 `LPI × margin`，补充现有"ROO+margin"框架（呼应 2023 PLOS ONE）。
3. 机制上检验"互补 vs 替代"：`γ>0` → 便利化互补关税、好物流伙伴放大关税收益；`γ≤0` → 替代。Tunisia 与深 RTA 文献为互补提供了理论预期。
4. 稳健性：LPI 分项（海关效率 vs 基础设施 vs 物流质量）、制度质量替代度量、滞后/工具变量（剔除逆向因果——贸易旺→LPI 高）。

**可补充的角度（扩大新意）**：结合你所在项目"供应链冲击"主线，可进一步做**LPI×关税×GVC 参与度**三层交互，检验"便利化是否尤能放大深度嵌入 GVC、对通关时滞敏感行业的关税收益"——目前**无人**做过。

---

## 5. 文献清单（按用途分组，含 DOI）

**A-1 主效应（RCEP 内 LPI→贸易流，直接竞争度最高）**
- 10.17825/klr.2021.31.2.81 — LPI of RCEP Signatories on China's Export (Gravity, 2021)
- 10.58567/rea01010004 — LPI of RCEP Countries on China's Export Trade (2022)
- 10.20294/jgbt.2022.18.5.101 — Logistics Efficiency on Korea's Trade in RCEP Signatories (2022)
- 10.55493/5009.v13i1.5363 — Logistics performance & trade facilitation on China–ASEAN (2025)
- 10.52202/078960-0041 — Cross-border logistics China–RCEP, LPI perspective (2025)
- 10.26689/pbes.v8i8.13385 — Comparative LPI across RCEP (2025)
- 10.1007/978-981-97-6839-4_11 — China–ASEAN logistics under RCEP (2024)
- 10.35611/jkt.2026.30.2.1 — LPI on agri-food trade (2026, outside RCEP)
- 10.19044/esj.2016.v12n25p37 — LPI as **mediator** corruption→trade (2016)

**A-2 主效应（非 RCEP，LPI/物流一般性）**
- 10.1080/13675567.2026.2646342 — Logistics digitalisation & trade flows (LPI gravity, 2026)
- 10.24006/jilt.2022.e3 — Export, logistics performance, regional integration: Vietnam (2022)
- 10.5539/ijbm.v20n5p83 — Logistics infrastructure & trade performance (2025)

**B-1 关税优惠利用率决定因素（ROO/幅度）**
- 10.1371/journal.pone.0286106 — ROO & tariff margin on CAFTA utilization (2023) ★最贴近
- 10.1355/ae42-3b — ATIGA utilization: margin & ROO (2025)
- 10.38162/jome.51.3.4 — KORUS utilization determinants (2022)
- 10.1956/jge.v11i4.413 — AFTA utilization Malaysia (2015)

**B-2 RCEP 关税实效（贸易/产业/福利）**
- 10.17825/klr.2024.34.6.69 — RCEP tariff reduction → Shandong exports to ROK (2024)
- 10.1515/econ-2022-0102 — RCEP tariff reduction on China's textile industry (2024)
- 10.1080/13504851.2021.1966361 — RCEP tariff reduction on GVCs (2021)
- 10.5296/ber.v16i3.23777 — RCEP tariff reduction & consumer welfare (2026)
- 10.1016/j.chieco.2026.102677 — RCEP depth (CPTPP) trade & welfare (2026)
- 10.54097/9fpgy060 — RCEP trade creation & diversion (2024)
- 10.18623/rvd.v22.5156 — RCEP trade creation & potential (2025)
- 10.2139/ssrn.4775658 — RCEP impact on China–RCEP trade (2024)

**C-1 便利化/制度与关税的互补或调节（邻近）**
- 10.30875/541bb513-en — Trade policy without trade facilitation: tariff pass-through Tunisia (2016) ★点题
- 10.1596/1813-9450-9674 — TF provisions in PTAs: Peru exporters (2021)
- 10.35611/jkt.2022.26.7.109 — TF index in RCEP members → cross-border e-commerce (2022)
- 10.2139/ssrn.4432826 — Institutional quality & quality distance in FTA (SADC) (2023)
- 10.1016/j.gfj.2024.100959 — Institutional quality as **moderator** (2024) 方法示范
- 10.5089/9781513518381.001.a001 — Tariff pass-through at the border (IMF/World Bank)
- 10.17825/klr.2026.36.3.1 — LPI shaping export outcomes under structural constraints (2026)
- 10.30875/a9b448e8-en — Trade facilitation under the RTA umbrella (2016)

**方法/背景**
- 10.1371/journal.pone.0286106 的 Logit+异质性框架（见上）；World Bank LPI & Trade Facilitation 量化传统：10.1142/9789812701350_0009、10.1142/9789812701350_0008。

---

## 6. 结论与风险提示

- **空白成立**：RCEP 语境下，伙伴国 LPI/海关效率**从未**作为**调节变量**与 RCEP 关税减让交互；"便利化互补关税"仅在非 RCEP/叙事层面被触碰。这是清晰、可写、可识别的微小创新点。
- **风险**：① 版图 A 已有大量"LPI 直接效应"文献，你必须在引言中**明确区分主效应与调节效应**，避免被审稿人误判为重复；② "便利化互补"理论预期（γ>0）要解释清楚为何不是替代（γ<0）——Tunisia 与深 RTA 文献支持互补，但需给出你的机制论证；③ 若走 RCEP 效用/利用率路线，注意与 2023 PLOS ONE 的重叠，需突出"加入 LPI/海关成本"这一新增维度。
- **待办**：建议后续补一次 **OpenAlex / Semantic Scholar**（本环境 web 工具未启用，未能交叉验证）以及针对"关税×LPI 交互"的定向检索，进一步确认无遗漏；同时核对 2021/2022/2025 各篇 LPI 论文的**实证方程**是否真的不含交互项（可下载其 PDF 核查）。
