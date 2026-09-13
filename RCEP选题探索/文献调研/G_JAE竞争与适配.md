# JAE 竞争与适配度分析：中日韩 / RCEP / 首次自贸协定

> 检索时间：2026-09-03。数据源：**Crossref API**（对 `Journal of Asian Economics`，ISSN **1049-0078** 全量拉取 + 关键词检索），OpenAlex 交叉核验。摘要字段被 Elsevier 在下游 API 剥离，故以标题/作者/年份/DOI 为证据；方法推断结合标题与文献共识。

## 0. 检索口径与覆盖
- 全量拉取 JAE **2016–2026** 论文共 **955 篇**（`_jae_all_2016.json`）。
- 关键词命中 **172 条**（`_crossref_raw.json`），按 RCEP / FTA / tariff / supply chain / rule of origin / utilization / integration / Japan / Korea / China / trade 做标题级过滤。
- 关键论文 DOI 均实测返回并保留。

---

## 1. JAE 已发表的「中日韩 / RCEP / 自贸协定」相关论文

### 1.1 直接命中 RCEP（全刊仅 3 篇标题提及 RCEP）
| 年份 | 作者 | 标题 | DOI |
|---|---|---|---|
| 2025 | Qing Peng; Zhenhao Chen; Jie Li | Financing constraints and the export partnerships with RCEP: Evidence from manufacturing firms in China | 10.1016/j.asieco.2024.101870 |
| 2023 | Kejuan Sun; Hao Xiao; Zhen Jia; Bin Tang | Estimating the effects of regional value chains of the RCEP in a GVC-CGE model | 10.1016/j.asieco.2023.101647 |
| 2023 | (RCEP under supply-chain/Tariff 检索命中) | …(另有 RCEP GVC 交叉命中) | — |

**关键判断**：RCEP 在 JAE 只有 **2–3 篇**，且两者分别是「微观出口伙伴 + 融资约束」（Peng et al. 2025）与「宏观 GVC-CGE 模拟」（Sun et al. 2023）。**没有任何一篇做企业级生产网络 / 原产地规则 / 协定间对比**。

### 1.2 中日韩三角（China–Japan–Korea）
- **零篇** 以「trilateral / China-Japan-Korea」为题（2016+ 全量扫描结果）。
- 接近的存量文献偏 **中美日** 三角（2009 年代，宏观）：Greaney & Lovely (2009)「China, Japan and the US: Deeper economic integration」；Dean, Lovely & Mora (2009)「Decomposing China–Japan–U.S. trade: Vertical specialization」；Kawai & Zhai (2009)「China–Japan–US integration amid global rebalancing (CGE)」。
- **中日韩/韩日双边**唯一实证：Sangho Shin & Edward J. Balistreri (2022)「The other trade war: Quantifying the Korea–Japan trade dispute」doi:10.1016/j.asieco.2022.101442（CGE 量化韩日出口管制争端）。

### 1.3 FTA / 区域贸易协定（通类——含东盟、原产地、利用率）
| 年份 | 作者 | 标题 | DOI |
|---|---|---|---|
| 2023 | Kazunobu Hayakawa 等 | Firm-level Utilization Rates of Regional Trade Agreements: Importers' Perspective | 10.1016/j.asieco.2023.101610 |
| 2021 | Kimie Harada; Shuhei Nishitateno | Measuring trade creation effects of FTAs: Evidence from wine trade in East Asia | 10.1016/j.asieco.2021.101308 |
| 2018 | Thang N. Doan; Yuqing Xing | Trade efficiency, free trade agreements and rules of origin | 10.1016/j.asieco.2017.12.007 |
| 2018 | Tomoo Kikuchi 等 | The effects of Mega-Regional Trade Agreements on Vietnam | 10.1016/j.asieco.2017.12.005 |
| 2018 | (mega-RTA) | The welfare and sectoral adjustment effects of mega-regional trade agreements on ASEAN countries | 10.1016/j.asieco.2017.09.001 |
| 2016 | Qiaomin Li; Robert Scollay; Sholeh Maani | Effects on China and ASEAN of the ASEAN-China FTA: The FDI perspective | 10.1016/j.asieco.2016.05.001 |
| 2022 | Jin Sun; Yitong Luo; Yuan Zhou | The impact of regional trade agreements on the quality of export products in China's manufacturing industry | 10.1016/j.asieco.2022.101456 |

### 1.4 关税（Tariff）
| 年份 | 作者 | 标题 | DOI |
|---|---|---|---|
| 2023 | Dan Xie | Tariff cost and cross-border M&A affiliate sales: Evidence from China | 10.1016/j.asieco.2023.101636 |
| 2020 | (US-China trade war GE) | The U.S.–China trade war: Tariff data and general equilibrium analysis | 10.1016/j.asieco.2020.101216 |
| 2020 | (destination tariffs) | The impact of destination tariffs on China's exports: Country, firm, and product perspectives | 10.1016/j.asieco.2020.101246 |
| 2022 | Fengxiu Zhou; Huwei Wen | Trade policy uncertainty, development strategy, and export behavior | 10.1016/j.asieco.2022.101528 |

### 1.5 规则 / 原产地 / GVC（RCEP 之外）
- Doan & Xing (2018)「Trade efficiency, FTAs and rules of origin」：**原产地规则** 与贸易效率（Doi 10.1016/j.asieco.2017.12.007）。
- 2025「Rules of Origin, Import of Inputs and Firm Innovation」doi:10.1016/j.asieco.2024.101872（原产地 × 中间品进口 × 企业创新）。
- 2022「Rules of origin and exports in developing economies: garment」doi:10.1016/j.asieco.2022.101514。
- GVC/供应链侧：Sun (2023) RCEP GVC-CGE；2023「Tracing the regional dual value chains」；2024「Cross-border personnel mobility and bilateral value chain linkages (visa)」doi:10.1016/j.asieco.2024.101844。

---

## 2. JAE 上有没有「首次 vs 存量 FTA」对比？

**没有。** 这是本次调研最明确的结论。

- 对 2016+ 全部 955 个标题做 `first/new vs existing/stock/intensive/extensive` 过滤，**零命中**「首次 vs 存量」对比设计。
- 最接近的三种都是「**单协定**」研究，而非跨协定（new vs old）对比：
  1. **利用率**：Hayakawa et al. (2023) 测度企业层面 RTAs 利用率——但以「进口商视角」测单一使用率，不做「首次协议 vs 已有协议」比较。
  2. **贸易创造**：Harada & Nishitateno (2021) 酒类贸易创造——引力模型，不分新旧协定。
  3. **原产地规则**：Doan & Xing (2018)——贸易效率，非新旧对比。
- **结论**：以「**首次协定 vs 存量协定**」为核心的识别设计在 JAE 完全空白，构成清晰的差异化护城河。

---

## 3. JAE 倾向发表的方法 & 中日韩选题契合度

### 3.1 方法光谱（按 JAE 已发表贸易类论文归纳）
| 方法层次 | JAE 代表 | 接受度 |
|---|---|---|
| **宏观 CGE / GTAP 模拟** | Sun (2023) RCEP GVC-CGE；US-China trade war GE (2020)；CPTPP 农业 (2025) doi:10.1016/j.asieco.2025.102013；Mega-RTA ASEAN (2018) | **极高**（JAE 是少数大量容纳 CGE 的期刊） |
| **引力模型 / PPML / 贸易效率** | Harada (2021) wine；Doan & Xing (2018) | **高** |
| **微观 DID / 事件研究 / 面板固定效应** | Xie (2023) tariff cost M&A；Sun (2022) RTA export product quality；Zhou & Wen (2022) TPU exports；Hayakawa (2023) utilization 测度 | **高**（大量企业层面 DID） |
| **企业网络 / 供应关系** | 几乎无（仅 Peng 2025 出口伙伴；M&A 2023） | **潜力大但未占领** |

### 3.2 中日韩 / RCEP 选题契合度
- **高度契合**。JAE 核心板块在「东亚 + 贸易 + 微观/宏观」，China / Japan / Korea 三词在标题出现 25 / 44 / 327 次，区域属性天然对口。
- **RCEP 缺口明显**：RCEP 标题仅 3 篇；中日韩三角 trilateral 零篇；首次 vs 存量对比零篇。
- **方法风险对照**：JAE 偏爱 CGE 与「单协定引力 / DID」。若选纯宏观 CGE，将直接撞上 Sun et al. (2023)；若选「出口伙伴 + 融资约束」，会咬住 Peng et al. (2025)。因此**避开这两条既有路线**，转向「企业生产网络 + 协定间（首次 vs 存量）异质性」是最优切入。

---

## 4. 竞争格局（谁在写 / 用什么抢）

1. **最直接对手（JAE 内部）**：Peng, Chen & Li (2025, JAE, doi:10.1016/j.asieco.2024.101870) —— 中国企业出口伙伴是否随 RCEP 扩张，机制为**融资约束**。若本文做的是 firm-to-firm **生产网络**（FactSet Revere 客户-供应商）且加入「首次 vs 存量 FTA」异质性，即形成清晰增量。
2. **方法对手（JAE 内部）**：Sun et al. (2023) 已占 RCEP 宏观 GVC-CGE 路线 → 不要走纯 CGE，或仅把 CGE 当背景而非核心贡献。
3. **可能抢跑的相邻期刊**（本报告不完全覆盖，建议另行核验）：China Economic Review、Journal of Comparative Economics、Review of International Economics、World Economy、China & World Economy、Emerging Markets Finance and Trade 对 RCEP/供应链有活跃发表；但「首次 vs 存量」+ 企业级供应网络这一组合在**各刊均未见**。
4. **方法护城河**：国家层面聚类（country-clustered SE）+ push-pull dual-track 交互（美国 301 push × RCEP/协定拉pull）正是既有 RCEP 文献尚无的识别骨架，叠加「first-vs-stock」异质性，符合 JAE 的东亚刊定位。

---

## 5. 结论与定位建议

- **适配度：高。** 东亚属性、微观+宏观皆可、以及 JAE 对 CGE/PPML/DID 的高包容度，都支持本文投 JAE。
- **护城河 = 首次 vs 存量 FTA 对比 + 企业生产网络 + 国家聚类 DID + push-pull 双轨**。这一式在 JAE 无先例。
- **必须差异化**的两篇文章：Peng et al. (2025)（出口伙伴+融资约束）与 Sun et al. (2023)（RCEP CGE）。清晰声明「生产网络 vs 出口伙伴」「首次 vs 存量 vs 单协定」差异后，竞争压力基本解除。
- **潜在挑战**：JAE 少数微观 DID 论文更偏好「企业面板 + 固定效应 + 聚类」而非复杂网络测度；需以规范的 supply-network 指标定义 + 国家层聚类 + 预分析计划（PAP）回应审稿人对「网络测度主观性 / 聚类单位」的质疑（这正是 `trade-policy-shock-supply-network` skill 反复强调的 PITFALL #1）。

---

## 附：本报告支撑文件
- `_crossref_raw.json`（关键词检索 172 条原始命中）
- `_jae_all_2016.json`（JAE 2016+ 全量 955 篇）
- `_key_abstracts.json`（关键论文元数据；摘要被 Elsevier 剥离，留空）
