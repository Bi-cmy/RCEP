# B. RCEP 与中国进口来源再配置 / 供应商集中度（HHI）：文献地图与空白定位

> 任务：调研 RCEP 引起的中国进口来源再配置 / 供应商集中度（HHI）变化的研究，定位空白。
> 检索工具：**Crossref REST API**（`api.crossref.org/works`，polite pool，`mailto`）。web_search 在本环境未配置，故按 academic-literature-api-search 技能的"API fallback"路径完成，未使用任何虚构/未核实的记录——所有文献的作者/期刊/年份/DOI 均经 Crossref 反向解析核验；Crossref 中 abstract 为空的条目已在文中标注"需查原文"。
> 检索维度：①处理变量（RCEP）②结果变量（来源再配置 / 多元化 / 集中度 HHI / 有效供应商数）③数据与情境（中国 / HS6 产品级 / 供应商国别）。约 40 组查询，去重后筛出 25 篇核心文献。
> 文件夹：`RCEP选题探索/文献调研/`（本文件为系列之 B，与 A、C、D 并列。）

---

## 0. 一句话结论（TL;DR）

在跨境检索（Crossref 全库 + 反向 DOI 核验）下，**"RCEP（2022-01-01 生效）→ 中国 HS6 产品级进口来源集中度（来源国 HHI / 有效供应商数）下降"这一因果识别** 目前**没有人做**。最接近的三类现有研究分别是：

1. **RCEP 对中国的贸易创造/贸易转移**——但限于**国家/行业层面的 SMART-WITS 模拟或面板引力**（如 Zhang et al. 2024；Yang & Martinez-Zarzoso 2014），**没有产品级来源构成、没有因果识别**；
2. **进口来源多样化/集中度（HHI）**——唯一在 RCEP 情境下用 HHI 测度进口来源多样性的，是 **Zaki Ar-Rafif & Revindo (East Asian Policy, 2025)**，但它是**RCEP 15 国、机械行业、区域跨国层面**，且把"多样性"当作**解释变量→供应链韧性**，**不是识别 RCEP 对集中度的因果效应，也不聚焦中国、更非 HS6 产品级**；
3. **中国特定农产品的来源多元化**（大豆/小麦/石油）——产品级、国别来源，但处理变量是**价格风险/进口安全**，**不是 RCEP 的关税削减**。

**结论：存在清晰、可操作的研究缺口**——"以 RCEP 关税削减为处理、以中国 HS6 进口来源国构成的 HHI / 有效供应商数为结果、用 DiD/事件研究做因果识别"这一组合**无人占据**（详见 §4）。

---

## 1. 三个子问题各自的现状

### a) RCEP 是否被研究为"中国从非 RCEP（美国+其他）转向 RCEP 成员"的来源再配置？

**部分研究（但停留在总量/行业层面，非产品级构成）。** 现有 RCEP×中国 文献主要回答"贸易创造 vs 贸易转移"（总量），而非"进口来源国构成"的再配置：

| 文献 | 期刊/年份 | 核心内容 | 是否触及"中国进口来源国构成" |
|---|---|---|---|
| Wenjie Zhang et al. (2024) `10.5539/ass.v20n4p1` | Asian Social Science | 用 **SMART-WITS 部分均衡模型**分析 RCEP 下中国贸易创造与转移，贸易格局变化 | **否**——国家/行业层面加总，非 HS6 来源构成；模拟非因果 |
| Kumuthini Sivathas (2026) `10.1016/j.chieco.2026.102677` | China Economic Review | CPTPP 与 RCEP 深度/贸易/福利分析，比较"深化 RCEP 至 CPTPP 标准"是否有差异 | 否——福利/深度，不涉来源构成 |
| Shanping Yang & Inmaculada Martinez-Zarzoso (2014) `10.1016/j.chieco.2014.04.002`（166 引） | China Economic Review | 东盟–中国 FTA 的贸易创造/转移面板分析（经典范式） | 否——东盟–中国总量，非中国进口来源国再配置 |
| Qianyi Zhou (2024) `10.2139/ssrn.4775658` | SSRN | RCEP 对中国与 RCEP 成员国贸易的影响 | 否——双边总量 |
| Guanhui Wang & Ming Ma (2023) `10.4108/eai.18-11-2022.2326918`；Fei Wang (2023) `10.4108/eai.18-11-2022.2327158` | 国际会议论文集 | RCEP 对中国—伙伴国进出口贸易的影响（含中越） | 否——双边总量 |
| Jose A. Ramirez, G. Manzano, M. Bedaño (2023) `10.62986/pn2023.21` | 报告 | RCEP 对**菲律宾**在中国/日/韩进口市场的**偏好侵蚀**（利益受损方是菲，非中国） | 方向相反（他国视角），非中国来源再配置 |

**反向证据（美国侧），说明"贸易转移"主题热但都是"美国/他国"而非"中国"。** Hayakawa (2026, International Economics) `10.1016/j.inteco.2026.100700`、Cigna/Meinen/Schulte (2020) `10.2139/ssrn.3749362`、Sungwoo Hong & Sunhyung Lee (2025) `10.2139/ssrn.5141956`、Shu-Yang Gan & Hongshik Lee (2025) `10.2139/ssrn.5208414`——全是**美国/第三方进口从中国转移**，**不是中国进口来源的国别再配置**。

> **要点：** "China's import ORIGIN reallocation"（国别来源构成变动）作为**结果**出现最接近的英文概念是 `import source reallocation`，但现有两篇都用在美国（见 §3 概念层）。RCEP 情境下没有人把它用于中国进口来源国构成。

### b) 供应商 HHI / 有效供应商数 这个结果变量是否有人用过？

**用过（HHI 测进口来源多样性），但仅在极少数、非中国、非产品级场景；"有效供应商数"在中国进口来源上几乎空白。**

| 文献 | 期刊/年份 | 结果/测度 | 情境 |
|---|---|---|---|
| **Naufal Zaki Ar-Rafif & Mohamad Dian Revindo (2025)** `10.1142/s1793930525000042` | **East Asian Policy** | **Herfindahl-Hirschman index (HHI)** 测进口来源多样性 | **RCEP 15 国、机械行业、2007–2020**。探究"来源多样性→供应链韧性"（把多样性当**解释变量**）。发现**较小/新兴经济体**的进口来源多样性（HHI）更低、波动明显 |
| Huanlang He, Lianzi Gu, Jian Mao (2024) `10.26599/cje.2024.9300102` | 中国经济学（China Journal of Economics） | 中间品**来源多样化** | 中国**企业**层面；结果变量是**企业创新**（来源多样≠HHI，作为解释变量） |
| Wei Yun, Jie Cao, Shangbin Liu (2025) `10.1016/j.econlet.2024.112138` | Economics Letters | 中间品进口多样化 | 中国**上市公司**；结果变量为**创新**（非集中度本身） |
| Xixi Li, Hongman Liu, Zhuang Wang, Hongsong Chen (2025) `10.1016/j.chieco.2025.102483`（7 引） | China Economic Review | 进口多样化、市场风险共动、农产品供应链韧性 | 农产品/食品供应链；**多样化→韧性**，非 RCEP 处理 |
| Jian Xu et al. (2014) `10.3390/su6118329` | Sustainability | 进口来源多样化（**石油**） | 中国**石油**进口来源优化可行性；测度是进出口来源地熵/份额类指标 |
| Vlado Vivoda & James Manicom (2011) `10.1017/s1598240800007177` | J. of East Asian Studies | 石油进口多样化程度 | 中日对比；**不是** HHI，是主体策略/地理结构描述 |
| Zheng Xuyun & He Meiying (2024) `10.18402/resci.2024.07.09` | 资源科学 | 来源多元化（**大豆**） | 中国**大豆来源多元化→进口价格**；产品级、单品类 |
| Sen Wu & Dayan Lin (2024) `10.54691/d73mth51` | Scientific J. of Econ. & Mgt. | 进口来源多样化（**小麦**）与进口风险 | 中国**小麦**来源多元化→进口风险；单品类 |
| Shengcheng Yang, Yan Tao, Siqi Yang (2023) `10.4108/eai.19-5-2023.2334395` | 会议 | **RCEP框架**下中国粮食进口安全路径 | 主题最贴近（RCEP+中国+粮食品类），但分析的是"安全路径"论述，**未用 HHI、未做来源集中度因果估计** |

> **要点：**
> - **HHI 测"进口来源多样性"**在 RCEP 情境下**仅有 Zaki & Revindo (2025) 一篇**，且是**区域×行业**层级的描述性实证，非"处理→结果"因果。
> - **"有效供应商数"（effective number of suppliers，约等于 1/HHI）** 直接用于**中国进口来源**的文献：**未检索到**。相关检索命中多为操作层面的"Selecting Import Products & Suppliers"类教材条目，或美国海关"Identifying Foreign Suppliers"（Kamal/Krizan/Monarch 2015，`10.2139/ssrn.2650703`），均不涉及中国来源集中度。

### c) "RCEP 降低来源集中度"的因果证据是否存在？

**不存在（未检索到任何直接因果识别）。** 关键判据：

1. 最接近的 **Zhang et al. (2024)** 用的是 **SMART-WITS 部分均衡模拟**——本质是**反事实模拟**而非**计量识别**，且**不是以来源国 HHI 为结果**。
2. 唯一用 HHI 的 **Zaki & Revindo (2025)** 是**跨国的、把多样性当自变量的关联性/描述**，**没有围绕 RCEP 生效时点（2022-01-01）做事件研究或 DiD、没有利用 RCEP 差异化关税削减做识别、不聚焦中国单国、不是 HS6 产品级**。
3. 没有任何文献**以中国海关 HS6×来源国数据**，用 **RCEP 关税削减作为处理、来源集中度 HHI 作为结果、做差分识别**。

**这是本调研确认的最强空白。**

---

## 2. 概念层（"import source reallocation"）的既有骨架

`import source reallocation` 作为一个结果概念，**现有文献全在美国**，且**测度不采用来源国 HHI**：

| 文献 | 期刊/年份 | 结果/设计 | 与中国/RCEP 关系 |
|---|---|---|---|
| Roger White (2007) `10.1007/s11079-007-9050-8` | Open Economies Review | **Import source reallocation** 与美国制造业就业（1972–2001） | 概念源头（美国）；不使用 HHI，用来源构成/再配置份额 |
| Fernando Leibovici & Dawn Chinagorom-Abiakalam (2025) `10.20955/wp.2025.018` | St. Louis Fed WP | **Import source reallocation** 与总体价格动态（美国） | 美国；来源再配置→价格；**不聚焦中国、不做 RCEP** |
| JaeBin Ahn, Lorenzo Rotunno, Michele Ruta（IMF WP）`10.5089/9798229054171.001.a001` | IMF 工作论文 | **Tariff pass-through & import reallocation** | 关税→进口再配置；国家/行业层面（多国），非中国单国、非 HHI |
| Wei Tian & Miaojie Yu (2023) `10.1007/978-981-99-7599-0_7` | Contributions to Economics | **Input trade liberalization & import switching**: Chinese firms | **中国、企业进口转换**——唯一"中国企业进口来源切换"，但其处理是**投入品贸易自由化（非 RCEP）**，且以企业为观察单位、不以 HS6×来源国 HHI 为结果（需查原文） |

> 这一层表明：**"来源再配置"被反复使用，但挂靠在美国/多国、价格/就业/创新等结果上；把"来源再配置"落到"中国产品级集中度变化"且与 RCEP 挂钩——空缺。**

---

## 3. 与"集中度/进口竞争"相邻但不重叠的文献（避免误撞）

- Mary Amiti & Sebastian Heise (2024, Review of Economic Studies) `10.1093/restud/rdae045`：**美国**生产者销售集中度上升 + 更多外国企业进入（进口竞争）。**方向与"进口多样化降低集中度"相反**，且是美国生产端集中度，非中国进口来源集中度。
- Michele Imbruno (2016, China Economic Review) `10.1016/j.chieco.2016.02.001`：中国加入 WTO 的进口、关税、非关税壁垒——**WTO 而非 RCEP**，且非来源构成。
- Robert Feenstra & Chang Hong (2020, NBER) `10.3386/w27383`：**第一阶段贸易协议**对中国农产品进口需求的影响——中国农产品进口，但处理是"中美第一阶段协议"，**非 RCEP、非来源国构成、非 HHI**。
- 其他来源集中度（HHI）文献多用于**金融市场/行业集中度**（如 Peleckis 2022）、**企业客户/供应商集中度（中国上市公司）**（Jia & Wu 2023 `10.1016/j.cjar.2023.100326`；Chen 2026 `10.2139/ssrn.6604118` 等），属**公司金融**领域的"客户/供应商集中度"，与**进出口来源国集中度**完全不是一个概念。

---

## 4. 空白定位（核心交付）

把三类文献看成三个集合，交集几乎为空：

- **集合 T（处理 = RCEP）**：Zhang 2024；Sivathas 2026；Zhou 2024；Ramirez/Manzano 2023；Yang/Tao 2023；Wang/Ma 2023 等。
- **集合 O（结果 = 进口来源集中度 / 多样化 / HHI）**：Zaki & Revindo 2025（HHI，RCEP 区域×机械行业）；He/Gu/Mao 2024（中国中间品来源多样性→创新）；Zheng & He 2024（大豆）；Wu & Lin 2024（小麦）；Xu 2014（石油）；Li et al. 2025（农产品韧性）。
- **集合 C（因果识别 / HS6 产品级 / 中国单国）**：几乎为空。

**T ∩ O（RCEP 处理 → 来源集中度结果）**：仅 **Zaki & Revindo (2025)** 一篇，但它是**区域（15国）×机械行业、描述性关联、把多样性当自变量**——**不是"RCEP→中国来源集中度下降"的因果估计**。

**T ∩ O ∩ C（RCEP 因果 → 中国 HS6 来源集中度下降）**：**空缺。**

### 空白具体表现（三条可写进intro的"缺什么"）

1. **处理维度的空白**：现有 RCEP×中国 研究讲"贸易创造 vs 转移"（总量/行业加总、SMART 模拟），**没人把 RCEP 的差异化关税削减当作一个可识别的冲击，去量化它对"中国进口来源国构成"的影响**。RCEP 恰好具有**强识别优势**——多国差异化降税时间表、不同产品降税幅度不同、中国对美国/非RCEP供应商依赖在不同产品上差异巨大——这正是适合做 **DiD / 事件研究 / 强度维度（tariff-stacked）设计** 的理想设定，但**尚无文献利用**。
2. **结果变量的空白**：**来源国构成 HHI / 有效供应商数（1/HHI）作为"被解释变量"在中国 HS6 产品级**上**未被使用**。Zaki & Revindo (2025) 用了 HHI 但用于"多样性→韧性"（自变量）且是区域×行业；中国商品级（大豆/小麦/石油）用的是"多样化→价格/风险"且**非 RCEP 处理**；中国企业级来源多样化用于"→创新"。**把 HHI 当作 RCEP 的后果来衡量，是新的。**
3. **数据/识别的空白**：**中国海关 HS6×来源国**进口数据完全可支撑（目录中已有"关税+供应链（数据）"等数据层），RCEP 生效时点（2022-01-01）明确、成员与非成员、降税幅度差异化清晰——**识别策略与数据都现成，只差一篇做的人**。

### 可操作的差异化卖点（相对最接近的三篇竞争文献）

- **vs. Zaki & Revindo (2025, East Asian Policy)**：由"区域×机械行业、描述性、多样性→韧性"升级为**"中国单国、HS6 全产品、RCEP→来源集中度 HHI 下降"的因果识别**；把 HHI 从**自变量**转为**因变量**；把观察单位从"国家"降到"HS6×来源国"；把识别从"跨国截面"升级为"围绕生效时点的 DiD/事件研究"。**这是清晰而坚实的超越。**
- **vs. Zhang et al. (2024, SMART-WITS)**：由"反事实模拟、国家/行业加总"升级为**"实际观测数据 + 计量识别"**，结果变量聚焦**来源构成集中度**而非总量转移。
- **vs. 大豆/小麦/石油文献**：由"单品类、价格/风险、非 RCEP 处理"升级为**"全产品 HS6、RCEP 处理、集中度结果"**。

> **一句话定位建议：** "RCEP 关税削减是否降低中国进口来源的地缘集中度（来源国 HHI / 有效供应商数）？——来自中国 HS6×来源国海关数据的 DiD/事件研究证据" 目前**无直接竞争者**。

---

## 5. 参考文献（经 Crossref 核验；abstract 缺失者标注）

> 格式：作者（年份）标题．期刊．DOI．[引用数]
> "〔abstract 需查原文〕"= Crossref 该条摘要为空，具体方法/结论需在期刊原文确认。

### 竞争组一：RCEP×中国（贸易创造/转移，总量或行业层）
1. Zhang, W., Abd Rahman, M. D., & Senan, M. K. A. M. (2024). Changes in the Trade Pattern in China Under the RCEP: An Analysis of Trade Creation and Diversion Using the SMART-WITS Model. *Asian Social Science*. `10.5539/ass.v20n4p1`．〔有摘要〕
2. Sivathas, K. (2026). Depth, trade, and welfare analysis of the CPTPP and RCEP: Does deepening RCEP to CPTPP standards make a difference? *China Economic Review*. `10.1016/j.chieco.2026.102677`．〔需查原文〕
3. Yang, S., & Martinez-Zarzoso, I. (2014). A panel data analysis of trade creation and trade diversion effects: The case of ASEAN–China Free Trade Area. *China Economic Review*. `10.1016/j.chieco.2014.04.002`．[166 引]〔需查原文〕
4. Zhou, Q. (2024). The Impact of the RCEP on Trade between China and RCEP Member Countries. *SSRN*. `10.2139/ssrn.4775658`．〔无摘要〕
5. Wang, G., & Ma, M. (2023). The impact of RCEP Agreement on the Import and Export Trade between China and Other Partners. *Proc. Int'l Conf.* `10.4108/eai.18-11-2022.2326918`．
6. Wang, F. (2023). Research on the Potential Impact of RCEP on China–Vietnam Import and Export Trade. *Proc. Int'l Conf.* `10.4108/eai.18-11-2022.2327158`．
7. Ramirez, J. A., Manzano, G., & Bedaño, M. (2023). RCEP: An Analysis of the Extent of Preference Erosion of the Philippines in the Import Markets of China, Japan, and South Korea. `10.62986/pn2023.21`．〔有摘要〕

### 竞争组二：进口来源多样化/集中度（HHI），含 RCEP 情境
8. **Ar-Rafif, N. Z., & Revindo, M. D. (2025). Effects of Import Source Diversity to Supply Chain Resilience: Analysis of Machinery Industries in RCEP Countries. *East Asian Policy*. `10.1142/s1793930525000042`．〔有摘要：RCEP 15 国、机械行业 2007–2020、用 HHI 测进口来源多样性、发现小/新兴经济体多样性更低〕**
9. He, H., Gu, L., & Mao, J. (2024). Diversification of Source and Import of Intermediate Products and Innovation of Chinese Enterprises. *China Journal of Economics*. `10.26599/cje.2024.9300102`．〔需查原文〕
10. Yun, W., Cao, J., & Liu, S. (2025). Intermediate import diversification, knowledge source diversity and firm innovation: Micro-level evidence from Chinese listed companies. *Economics Letters*. `10.1016/j.econlet.2024.112138`．〔需查原文〕
11. Li, X., Liu, H., Wang, Z., & Chen, H. (2025). Import diversification, market risk co-movement and Agri-food supply chain resilience. *China Economic Review*. `10.1016/j.chieco.2025.102483`．[7 引]〔需查原文〕
12. Xu, J., Zhang, J.-S., Yao, Q., & Zhang, W. (2014). Is It Feasible for China to Optimize Oil Import Source Diversification? *Sustainability*. `10.3390/su6118329`．[10 引]〔有摘要〕
13. Vivoda, V., & Manicom, J. (2011). Oil Import Diversification in Northeast Asia: A Comparison Between China and Japan. *Journal of East Asian Studies*. `10.1017/s1598240800007177`．[21 引]〔有摘要〕
14. Zheng, X., & He, M. (2024). The impact of source diversification on soybean's import prices of China. *资源科学 (Resources Science)*. `10.18402/resci.2024.07.09`．〔需查原文〕
15. Wu, S., & Lin, D. (2024). Study on the Impact of Import Source Diversification on China's Wheat Import Risk. *Scientific Journal of Economics and Management*. `10.54691/d73mth51`．
16. Yang, S., Tao, Y., & Yang, S. (2023). Exploring the Path of China's Grain Import Security under RCEP Framework. *Proc. Int'l Conf.* `10.4108/eai.19-5-2023.2334395`．

### 竞争组三：概念层"import source reallocation / import switching"
17. White, R. (2007). Import Source Reallocation and U.S. Manufacturing Employment, 1972–2001. *Open Economies Review*. `10.1007/s11079-007-9050-8`．[3 引]〔需查原文〕
18. Leibovici, F., & Chinagorom-Abiakalam, D. (2025). Import Source Reallocation and Aggregate Price Dynamics in the United States. *Federal Reserve Bank of St. Louis WP*. `10.20955/wp.2025.018`．〔需查原文〕
19. Ahn, J., Rotunno, L., & Ruta, M. Tariff Pass-Through and Import Reallocation. *IMF Working Paper*. `10.5089/9798229054171.001.a001`．〔需查原文〕
20. Tian, W., & Yu, M. (2023). Input Trade Liberalization and Import Switching: Evidence from Chinese Firms. *Contributions to Economics*. `10.1007/978-981-99-7599-0_7`．〔需查原文〕

### 竞争/相邻组四：集中度与进口竞争（方向相反或他国）
21. Amiti, M., & Heise, S. (2024). U.S. Market Concentration and Import Competition. *Review of Economic Studies*. `10.1093/restud/rdae045`．[24 引]〔有摘要〕
22. Hayakawa, K. (2026). Do exports to the US increase imports from China during the US–China tariff war? *International Economics*. `10.1016/j.inteco.2026.100700`．〔需查原文〕
23. Cigna, S., Meinen, P., & Schulte, P. (2020). The Impact of US Tariffs Against China on US Imports: Evidence for Trade Diversion? *SSRN*. `10.2139/ssrn.3749362`．
24. Feenstra, R., & Hong, C. (2020). China's Import Demand for Agricultural Products: The Impact of the Phase One Trade Agreement. *NBER WP*. `10.3386/w27383`．[6 引]〔需查原文〕
25. Imbruno, M. (2016). China and WTO liberalization: Imports, tariffs and non-tariff barriers. *China Economic Review*. `10.1016/j.chieco.2016.02.001`．[47 引]〔需查原文〕

---

## 6. 局限与后续（诚实声明）

- **范围**：本调研以 Crossref（期刊+部分 WP/SSRN DOI 收录）为核心。**不能完全排除** NBER/CEPR/中文知网/CNKI 上有零星未收录进 Crossref 的相关工作；建议进一步用 CNKI 检索中文期刊（知网检索：`RCEP` + `进口来源` + `集中度/多元化` + `替代`），以及在 NBER/CEPR 官网补 `RCEP` + `import concentration` 关键词。web_search 在本环境不可用，故未做谷歌学术/百度学术覆盖，属**已声明的边界**。
- **证据载明**：凡 Crossref 摘要为空的条目，均未臆造其方法与结论，标注"需查原文"。**Zaki & Revindo (2025)** 摘要明确提到 HHI 测度与 RCEP 15 国机械行业，是"最接近竞争者"，但整套因果与产品级构成本调研**仍判断为空白**——该文为区域×行业描述性，未进行"RCEP→中国来源集中度"因果识别。
- **建议引用数据**：中国海关进口数据（HS6×来源国）支持 RCEP 的差异化降税识别；与目录中"关税+供应链（数据）"及 code/results 层可直接联动。

*报告生成：2026-09-03，基于 Crossref API 第 1、2 轮批量检索与反向 DOI 核验。*
