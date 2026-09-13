# C｜中日首次FTA在RCEP中的特殊性及相关实证研究 —— 文献调研与空白定位

（调研日期：2026-09-03；方法：CrossRef REST API 为主，全文逐条调取摘要）

---

## 0. 检索方式与覆盖说明

- **主检索源**：CrossRef REST API（`api.crossref.org/works`）。以"query + query.title"双通道、跨 8 组递进检索 + 对 15+ 条命中逐条解析 DOI 元数据（摘要/作者/期刊/被引）。
- **检索词（代表性）**：RCEP China Japan trade；RCEP Japan tariff elimination；RCEP China Japan first free trade agreement；RCEP trade creation trade diversion；RCEP tariff reduction structure heterogeneous；RCEP supply chain / intermediate goods / GVC；China Japan-Korea FTA；ASEAN preferential trade agreements trade creation；SMART/Gravity/CGE。
- **未能覆盖**：① OpenAlex API 全程 429（限流）——本报告不依赖其结果；② Web 搜索（Firecrawl）未配置、浏览器环境 pydantic 冲突——未能补足。→ **中文文献（CNKI 体系）与部分 NBER/RiETI 工作论文在 CrossRef 里收录有限**，是本调研的已知盲区，建议后续用知网/百度学术单独补一轮（见 §8）。
- **核心结论先行**：**"中日首次FTA"作为 RCEP 最大增量这一制度事实，文献里"反复被'提及'、却几乎无人'实证'它"**。现有中日专项研究几乎全是**单个行业的局部均衡（SMART）模拟**或**低被引的会议/OA 期刊**，没有一篇以"中日双边"为对象的严谨减式因果识别；而把"首次FTA效应"与"已有东盟FTA增量"作为处理对比的**零**。

---

## 1. 制度背景：中日首次FTA的特殊性（先厘清"为什么这是空白"）

- RCEP 15 国中，**6 个非东盟成员（中、日、韩、澳、新西兰）彼此之间此前没有任何双边/区域性 FTA**。这是 RCEP 区别于"东盟+1"体系的最大制度特征。
- **中国与日本尤其特殊**：中日长期存在政治与经济博弈，**从未签订任何双边自由贸易协定**；RCEP（2022-01-01 生效）是**中日之间的"首次 FTA"**——这本应是 RCEP 全部关税增量中最大的一块（中日互为对方最大的贸易伙伴之一，且相互关税此前基本未被减免）。
- 文献中对该制度事实最清晰的表述来自 **Wardani & Cooray (2019)**："the other six ASEAN trading partners within RCEP have no free trade agreements yet among them"、"The impact of RCEP will be insignificant without China and Japan"。**但作者只做了 ex-ante 的"节省潜力"估算，并未对"首次FTA"做成因分析。**
- 与此相对，**东盟系成员（中-东盟、日-东盟、韩-东盟）都已签过"A+1"协定**，RCEP 对它们是**"存量优惠的深化/整合"**，而非"从无到有"。

> 一句话概括特殊性：**同一份 RCEP，对中日是"从无到有的首次关税减让"，对东盟是"已有优惠的边际加深"。前者无直接可比照的"增量大小"，后者有**。这个对比本身就是天然的处理强度/处理性质差异，然而文献没有用起来。

---

## 2. 角度 a〕RCEP 对中日进口/供应链的影响研究现状

### 2.1 直接以"中日双边"为对象的文献（全部列出）
| 文献 | 年份/期刊 | 方法 | 要点 | 被引 |
|---|---|---|---|---|
| Sun Yanlin & Zhang Jiajia, *Analysis of the economic effects of China-Japan tariff concessions on Mechanical and electrical products under RCEP (SMART)* | 2023, SHS Web of Conferences | 局部均衡 SMART 模拟 | 中日机电产品：RCEP 生效前 91.3% 日对华出口机电已零关税；生效后中国对日本机电"渐进减税+过渡期"，日本得利更大一方是中国，中国设置过渡期维持基准税率 | 0 |
| Sun Yanlin & Zhang Xinyue, *Determinants of Staging Categories for Tariff Elimination in the Bilateral Tariff Arrangement between China and Japan under RCEP* | 2024, Adv. in Computer Science Research | 关税分期（staging）决定因子（实证/计量） | 专门解析**中日条约里哪些产品被安排到分期/延迟减税**——构成潜在的处理强度变异，但**未被用于因果识别** | 0 |
| Chen, Lin et al., *Study on the Impact of Textile Trade between China and Japan under the RCEP Framework* | 2024, Textile & Leather Review | 显示性比较优势 + WITS-SMART 模拟 | 中日纺织品（HS61-63）：短期中国得利更多（日本减税），长期双方均受益 | 0 |
| 唐雨果, *Research on the Impact of RCEP on Chemical Products Trade between China and Japan* | 2025, E-Commerce Letters（中文OA） | 描述性/计量 | 化工品双边贸易，质量较低 | 0 |
| Wardani & Cooray, *Saving Potential of RCEP: Implication for China and Japan* | 2019, Journal of Economic Info | ex-ante FTA 节省潜力 + 政治经济 | **该角度最权威**：明确点出"六非成员彼此无FTA"、"无中/日则RCEP意义不大" | 9 |
| Yang & Woo, *A Study on Impact of RCEP Agreement on the Industrial Trade between China, Korea and Japan* | 2022, Regional Industry Review（韩） | 产业贸易分析 | 中日韩产业贸易，韩国视角为主 | 0 |

### 2.2 高被引但"非中日专项"的 RCEP 关税/GVC 文献（可作基线方法参照）
- **Wen, You & Zhang (2021)，*Effects of tariff reduction by RCEP on global value chains based on simulation*，Applied Economics Letters，引 11**：RCEP 关税削减对全球价值链的影响（模拟）。**处理的是"RCEP 整体关税"，未落到中日双边。**
- **Zhu & Huang (2023)，*Impact of the tariff concessions of RCEP on the structure and evolution mechanism of manufacturing trade networks*，Social Networks，引 23（本项目命中里被引最高）**：RCEP 关税减让对制造业贸易**网络**结构的影响。网络层面，非中日双边。
- **Li & Moon (2018)，*The trade and income effects of RCEP: implications for China and Korea*，Journal of Korea Trade，引 28**：CGE（异质性企业）模拟贸易与收入效应，**聚焦中国与韩国**，未落到中日。
- Zhao & Mun (2023)，*RCEP on Intra-Industry Trade: Panel VAR*，Journal of Korea Trade，引 9。

### 2.3 角度 a 的空白判定 ⭐
- **没有**一篇高被引/顶刊、以"RCEP 对中日双边进口（或日本自华进口）"为**核心被解释对象**的严谨经验研究。
- 现存的中日专项**几乎全是**：① 单行业（机电/纺织/化工）的**局部均衡 SMART 模拟**；② 低被引会议/中文OA；③ 以**模拟**而非减式识别为主。
- 高水平文献（Wen 2021、Zhu 2023、Li&Moon 2018）处理的是 **"RCEP 整体关税→GVC/网络/中日韩"**，**均未把"中日首次FTA"单独抽出来作为处理变量**。
- **即：中日是 RCEP 最大的增量双边，却是实证上被研究得最薄的双边之一。**

---

## 3. 角度 b〕"日本进口份额 / 日本关税减让幅度"作为处理强度的异质性研究

### 3.1 现状：**未发现任何以"处理强度"为核心的连续异质性识别**
- 检索"Japan import share / tariff reduction magnitude / heterogeneous treatment / exposure"等，**没有**命中把**"日本（或出口方）在 RCEP 前对该产品的 MFN 税率"、"日本进口份额"、或"减让幅度"**作为**连续处理强度**纳入 **DiD / 事件研究 / 合成控制**的文献。
- 现有"异质性"研究多为**产品/行业层面的模拟区分**，而非计量上的处理强度异质性：
  - Sun & Zhang (2023)：用 SMART 区分"中日谁获益更多"，但**无**按减让幅度/进口份额分层的异质性回归；
  - Wen et al. (2021)、Zhu & Huang (2023)：RCEP 关税模拟，**无**处理强度异质性；
  - "Determinants of Staging Categories..."（Sun & Zhang 2024）研究了"哪些产品被安排分期减税"，**本质上刻画了关税调整的截面差异（潜在 exposure），但被用在"解释分期决定"，而非"当作处理强度做因果识别"**——这是一个**几乎未被利用的设计素材**。
- 相关但角度不同的："*The welfare effects of partial tariff reduction in Japan*"(Asano & Sakane 2024)、"*Tariff Reduction, Import Liberalization, Consumer Welfare in RCEP (structural)*"(Zhou & Song 2026)——均为福利/结构估计，非中日双边处理强度异质性。

### 3.2 角度 b 的空白判定 ⭐
- **RCEP 关税清单/分期表天然提供了"产品×国别×减让幅度/减让时点"的连续变异**，又叠加了"中日首次 vs 东盟存量"的处理性质差异——但**尚无研究把这两者组合成"处理强度=日本（RCEP减让幅度/日本进口暴露份额）"的 DiD/esIV 识别**。
- **这是最值得切入、也最可行的一个空白**：数据（HS6 税率、分期、日本进口份额）可得性强，识别故事清晰。

---

## 4. 角度 c〕"首次FTA效应" vs "已有东盟FTA增量"的对比

### 4.1 现状：**零**（没有任何文献做这个实证对比）
- **没有**论文把"**首次建立FTA（中日、中韩）**"与"**已有优惠的边际深化（中-东盟、日-东盟）**"作为**同框架内的处理对比**来做因果估计。
- **最接近的是概念层面**：Wardani & Cooray (2019) 用文字点出"六非成员彼此无FTA"的特殊性，但**只做了 ex-ante 节省潜力**，未做"首次 vs 存量"的实证对比。
- **贸易创造/转移文献聚焦"重叠协定"而非"首次 vs 增量"**：
  - *Trade Creation and Diversion in Overlapping ASEAN+6 Agreements* (Narandu & Sriyanto 2026)；
  - *Trade Creation and Trade Diversion of ASEAN's Preferential Trade Agreements* (Sattayanuwat & Tangvitoontham 2018)；
  - *The Early Effects of Preferential Trade Agreements on Intra-Regional Trade within ASEAN+6* (Sen, Srivastava & Pacheco 2013，引7)。
  - 这些都是"ASEAN+6 重叠协议"或"东盟+1"视角，**没**落到"中国-日本首次FTA"这个具体对比。
- **制度/规则层面的对比（非因果）**：*An Assessment of Rules of Origin in RCEP and ASEAN+1 FTAs*（ADB 2023）、*Beyond trade creation: preferential trade agreements and trade disputes*（Li & Qiu 2019，引9）——政策评估类，非"首次 vs 增量"识别。

### 4.2 角度 c 的空白判定 ⭐
- **"首次FTA效应 vs 已有东盟FTA增量"作为一个明确、可操作、理论上有趣（贸易创造 vs 规则深化/伙伴国FTA库存差异）的对比设计，在文献中完全缺席。**
- 这一对比还能与 RCEP 的**原产地规则（累积richer、区域内累积标准放宽）**、**服务条款（中日首次开放）**叠加，构成"首次FTA 的制度红利"命题——同理无人做实证。

---

## 5. 关键文献清单（可直接引用）

**制度事实锚点**
1. Wardani, R.Y., & Cooray, N.S. (2019). *Saving Potential of RCEP: Implication for China and Japan*. Journal of Economic Info, 6(1). DOI: 10.31580/jei.v6i1.122（引9）——**"六非成员彼此无FTA、中日不可缺"的最权威表述。**

**中日专项（多为模拟/低被引，作为"存在但薄弱"的证据）**
2. Sun, Y., & Zhang, J. (2023). *Analysis of the economic effects of China-Japan tariff concessions on Mechanical and electrical products under RCEP (SMART)*. SHS Web Conf. DOI: 10.1051/shsconf/202316901014
3. Sun, Y., & Zhang, X. (2024). *Determinants of Staging Categories for Tariff Elimination in the Bilateral Tariff Arrangement between China and Japan under RCEP*. Adv. in Computer Science Research. DOI: 10.2991/978-94-6463-504-1_27
4. Chen, M., Lin, X., et al. (2024). *Study on the Impact of Textile Trade between China and Japan under the RCEP Framework*. Textile & Leather Review. DOI: 10.31881/tlr.2024.155

**高被引方法论/基线参照**
5. Wen, H., You, Y., & Zhang, Y. (2021). *Effects of tariff reduction by RCEP on global value chains based on simulation*. Applied Economics Letters. DOI: 10.1080/13504851.2021.1966361（引11）
6. Zhu, N., & Huang, S. (2023). *Impact of the tariff concessions of RCEP on the structure and evolution mechanism of manufacturing trade networks*. Social Networks. DOI: 10.1016/j.socnet.2023.01.008（引23）
7. Li, Q., & Moon, H.C. (2018). *The trade and income effects of RCEP: implications for China and Korea*. Journal of Korea Trade. DOI: 10.1108/jkt-03-2018-0020（引28）

**贸易创造/转移（"首次 vs 增量"的最邻近、但未落到中日）**
8. Sen, R., Srivastava, S., & Pacheco, G. (2013). *The Early Effects of PTAs on Intra-Regional Trade within ASEAN+6*. Southeast Asian Economies. DOI: 10.1355/ae30-3a（引7）
9. Narandu & Sriyanto (2026). *Trade Creation and Diversion in Overlapping ASEAN+6 Agreements*. ETIKONOMI. DOI: 10.15408/etk.v25i1.49615
10. Li & Qiu (2019). *Beyond trade creation: preferential trade agreements and trade disputes*. Pacific Economic Review. DOI: 10.1111/1468-0106.12314（引9）

---

## 6. 研究空白总结（三合一）

| 角度 | 现状 | 空白等级 |
|---|---|---|
| **a) RCEP×中日进口/供应链** | 只有单行业 SMART 模拟 + 低被引会议/OA；高水平研究都落"RCEP整体→GVC/网络/中日韩"，**无**中日双边减式识别 | **大空白** ⭐ |
| **b) 日本关税减让幅度/进口份额=处理强度的异质性** | **完全无**；最大可用的"分期表+税率+进口份额"连续变异未被当处理强度用 | **最大空白** ⭐ |
| **c) 首次FTA效应 vs 已有东盟FTA增量** | **零**；仅有概念性"六非成员无FTA"表述（Wardani 2019）和"重叠FTA贸易创造"文献 | **完全空白** ⭐ |

---

## 7. 建议切入方向（可操作性排序）

1. **【首选】双重视角异质性 DiD**：以 HS6 产品×中日为对象，处理强度 = **RCEP 生效前日本对华 MFN 税率 / 减让幅度 × 日本进口份额（或中国出口暴露）**，DID/事件研究，利用"首次 vs 东盟存量"做安慰剂或分组。数据（协定税率表、分期、MFN、贸易流）可得性极强。→ 同时覆盖 a+b，并引出 c。
2. **【次选】"首次FTA"vs"存量深化"对照**：同一 RCEP、同一年生效，中日（首次）vs 中-东盟/日-东盟（存量）作为处理性质差异，比较贸易创造规模/方向（可用引力 + 双差分、或 synthetic control）。→ 直接回答 c。
3. **【理论/被引成本低】原产地规则累积 + 首次FTA**：RCEP 放宽的区域内累积标准对"中日首次建立原产地链接"的红利量化（中、日零部件互供）。文献里 RCEP 原产地规则只有制度评估（ADB 2023），无因果。
4. **利用被忽视的"分期表"数据**：Sun & Zhang (2024) 已说明"哪些产品被安排分期减税"是**内生的（行业保护/谈判力）**，可做**关税分期作为 exposure** 的识别，也可讨论处理强度内生性问题（这是该主题能发好刊的加分点）。→ 补强 b 的可识别性论证。

---

## 8. 本调研的局限与下一步

- **只覆盖 CrossRef 收录**（英文+部分韩/中期刊）。中文核心（知网 CNKI）与 **NBER / RIETI / 日本经济产业省**工作论文收录极少——**建议单独补一轮 CNKI 检索**（关键词：RCEP、中日自贸协定、关税减让、进口份额、双重差分）以及 RIETI/NBER 工作论文检索。
- OpenAlex 全程限流（429）、web 搜索与浏览器工具在本次环境不可用，故本文基于 CrossRef 单源，结论的"空白"判断在英文/国际期刊层面是稳健的，在中日文文献层面**待知网二次确认**。
- 建议后续（若需要）用 OpenAlex（错峰/加 mailto 重试）或 Semantic Scholar 补一轮，交叉验证"中日专项"是否确有更多中/日文成果。
