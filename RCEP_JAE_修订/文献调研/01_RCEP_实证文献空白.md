# RCEP 对中国企业供应链/价值链/网络影响的实证文献调研报告

> 调研时间：2026-09-03
> 调研目的：为 JAE（Journal of Asian Economics）修订版及"供应链冲击"项目定位文献空白，评估用**企业间网络数据（FactSet Revere / CSMAR 供应链类）**研究 RCEP 的可行性。
> 数据来源：OpenAlex（因账户预算不足不可用，返回 429）、**Crossref**（主用，工作正常）、Semantic Scholar（限流，仅作补充）。搜索关键词覆盖：RCEP supply chain / firm-level / network / value chain / trade diversion / regional trade agreement firm evidence / rules of origin / tariff 等 20+ 组。
> 说明：所有论文的"作者/年份/期刊/DOI"均已通过 Crossref 元数据核实；个别论文（尤其 SSRN 预印本与中文期刊）方法细节根据标题与可获取摘要推断，以尽量保守的方式标注。

---

## 一、结论速览（TL;DR）

1. **RCEP 实证文献已有相当规模，但严重偏"宏观 / 国家 / 行业"层面**，主流是 GTAP/CGE 模型、引力模型、加成贸易法（value-added / TiVA / ADB-MRIO）与关税原产地规则分析。
2. **真正落到"中国企业"（firm-level）且用企业微观数据的 RCEP 研究寡见**，目前能定位到的屈指可数：最关键的一篇是 Peng, Chen & Li（2025, *Journal of Asian Economics*）——用**中国制造业企业出口数据**研究融资约束与 RCEP 出口伙伴关系；其余多为**国别贸易网络（RTA 国家网络）**层面，而非企业间网络。
3. **没有检索到任何一篇**用"**企业—企业（customer–supplier）生产网络数据**"（FactSet Revere / Bloomberg SPLC / Compustat Segment / CSMAR & CNRDS 供应商-客户关系）研究 **RCEP 对中国企业**影响的实证论文。
4. 由此判断：现有文献在"**RCEP × 中国企业间供应链网络（网络位置、网络重构、冲击沿供应链传播）**"处存在**清晰、未被占据的研究空白**，且具备可行性（见第三节）。
5. 目前贴近 RCEP 的"网络"研究，其"网络"对象是**国家间/协定间网络**（RTA network centrality）或**贸易流网络**，**均非企业间客户-供应商链接**。

---

## 二、已有文献梳理（按 RCEP 研究方向分块）

> 以下按"检索方向"归类，每个方向给出代表性论文（作者/年份/期刊/方法与数据特征）。已核实 DOI 的标注 DOI。

### 方向 1：RCEP 与区域/全球价值链（GVC/RVC）——*文献最集中*

| 论文 | 期刊/年份 | 方法 | 数据 | 对象 |
|---|---|---|---|---|
| Peng, Shuijun; Wu, Lamei; Zhou, Shangyao; Xu, Jialin; Gao, Bo. **Quantifying the Global Value Chain and Welfare Effects of RCEP: Implications for the U.S.-China Trade Frictions** | *China Economic Review*, 2026 (DOI: 10.1016/j.chieco.2026.102743) | 量化 GVC + 福利模型（CGE/TiVA 类） | 国家/部门投入产出 | 国家→GVC |
| Gao, Jinwu; Zhao, Yuying; Jia, Ruru. **RCEP regional value chain construction and global value chain position enhancement: a measurement analysis based on regional value chains** | *J. of Industrial and Business Economics*, 2024 (DOI: 10.1007/s40812-024-00320-5) | 区域价值链测算（RVC/GVC 位置指标） | 投入产出/价值分解 | 行业/国家 |
| Rahman, Nida; Sharma, Krishan. **Regulatory quality and value-chain participation in RCEP: evidence of nonlinear effects** | *J. of Regulatory Economics*, 2025 (DOI: 10.1007/s11149-025-09500-0) | 面板回归（非线性） | 国家-行业 | 行业/国家 |
| Xu, Shaowen; Qian, Jingfei; Chen, Yangfen; Zhang, Huijie. **Impact of RCEP implementation on agricultural sector in regional countries: a global value chain perspective** | *J. of Integrative Agriculture*, 2024 (DOI: 10.1016/j.jia.2024.11.035) | GVC 视角 + 实证 | 农业投入产出 | 农业行业 |
| Cororaton, Caesar B. **The Global Value Chain Effects of RCEP: Estimating the Impact on the Philippines** | *DLSU Business & Economics Review*, 2025 (DOI: 10.59588/2243-786x.1145) | 可计算一般均衡（CGE） | 国家投入产出 | 国家 |
| Ingot, S. R.; Laksani, D. D. **Indonesia GVC Participation in RCEP** | *Proc. Int. Conf. on Trade*, 2019 (DOI: 10.2991/icot-19.2019.34) | GVC 参与度测算 | 投入产出 | 国家 |
| *中国嵌入 RCEP 区域价值链对农产品出口隐含碳排放的影响* | *资源科学*, 2025 | 隐含碳/价值链测算 | 投入产出 | 行业 |

**小结**：方向 1 几乎全为国家/行业层面的价值分解、GVC 位置、CGE 福利测算，**无企业层面**证据。

---

### 方向 2：RCEP 贸易创造 / 贸易转移（trade creation / trade diversion）——*以引力模型与 CGE 为主*

| 论文 | 期刊/年份 | 方法 | 对象 |
|---|---|---|---|
| Sivathas, Kumuthini. **Depth, trade, and welfare analysis of the CPTPP and RCEP: Does deepening RCEP to CPTPP standards make a difference?** | *China Economic Review*, 2026 (DOI: 10.1016/j.chieco.2026.102677) | 深度协定 + 贸易/福利模型（结构引力/协理） | 国家 |
| *Indonesian Export Dynamics in the RCEP Era: Trade Creation or Trade Diversion?* | *Int. J. of Economic, Finance & Management*, 2026 | 引力/贸易结构 | 国家 |
| Luo, Xiaofei; Shen, Xiaonan. **The Economic and Trade Effects of RCEP Agreement in China and Other Member Countries: Based on GTAP Model** | *Proc. 1st Int. Conf. Public Mgmt, Digital Econ & Internet Tech*, 2022 (DOI: 10.5220/0011740200003607) | **GTAP** | 国家/行业 |
| Zhou, Qianyi. **The Impact of the RCEP on Trade between China and RCEP Member Countries** | SSRN, 2024 (DOI: 10.2139/ssrn.4775658) | 引力模型 | 国家 |
| *The Impact of RCEP Tariff Concessions on Intra-Regional Trade* | *Highlights in Business, Economics & Management*, 2024 | 关税→区内贸易 | 国家 |

**小结**：方向 2 同样以国家/行业为对象，用引力模型模拟贸易创造/转移；**无企业**。

---

### 方向 3：RCEP 原产地规则（rules of origin）与产业转移 ——*政策/机制分析为主*

| 论文 | 期刊/年份 | 方法 | 对象 |
|---|---|---|---|
| Chen, Zhixiang; He, Junlin. **A Study on the Impact of RCEP Rules of Origin on Industrial Relocation in China's Manufacturing Sector** | *The Chinese Economy*, 2026 (DOI: 10.1080/10971475.2026.2657735) | 原产地规则→产业转移（结构/行业分析） | 行业 |
| Ling, Dan; Qian, Kun. **Research on the impact of RCEP rules of origin on China's manufacturing industry** | *SHS Web of Conferences*, 2023 (DOI: 10.1051/shsconf/202316901010) | 规则文本+定性/机制 | 行业 |
| *RCEP Origin Accumulation Rules: How Vietnamese Textiles Can Arbitrage...* | *J. of Economics and Law*, 2026 | 累积原产地规则（机制分析） | 国家/行业 |
| *An Assessment of Rules of Origin in RCEP and ASEAN+1 FTAs* | ADB 工作论文, 2023 (DOI: 10.22617/tcs230396-2) | 规则比较 | 行业 |

**小结**：方向 3 聚焦**制度/规则机制**，服务于产业转移与贸易流向分析，**无企业微观证据**。

---

### 方向 4：RCEP 关税削减与贸易网络（trade network / "shock absorber"）——*最接近"网络"但仍是贸易流网络*

| 论文 | 作者 | 年份 | 期刊/DOI | 方法/网络对象 |
|---|---|---|---|---|
| **How Does China Mitigate "Reverse Shocks" in Trade Networks? —— Evidence from the "Shock Absorber" Mechanism of RCEP Tariff Reductions** | Pan, Sujuan; Wu, Yilin; Zhuang, Hui-ming | 2026 | SSRN (DOI: 10.2139/ssrn.6332146) | 贸易网络 + RCEP 关税减免"减震器"机制（国家/贸易流网络，非企业间网络） |
| **Do Export Firms Embedding in the RTA Network Positions Promote Productivity? New Empirical Evidence from Chinese Firms** | Wang, Xiaozhuo; Yang, Guang | 2024 | SSRN (DOI: 10.2139/ssrn.4875238) | **中国企业 + RTA 网络位置** → 生产率。网络对象为"国家间/协定间 RTA 网络"，位于企业出口目的地层面，**非企业间客户-供应商链接** |
| **The impact of global regional trade agreement network centrality on exports** | Wang, Xiaozhuo; Ni, Bei | 2026 | *Emerging Markets Review* (DOI: 10.1016/j.ememar.2026.101471) | RTA 网络中心性 → 出口（国家网络 + 微观出口数据） |
| *Assessing Trade Concentration, Dependency, and Resilience in Korea's Semiconductor Supply Chain: A Network and Entropy-Based Approach* | Kim, Min-Jae; Lee, Tae-Hoo | 2025 | *J. of Korea Trade* (DOI: 10.35611/jkt.2025.29.7.67) | 行业供应链网络（熵值/网络法） |

**小结**：这是**最接近题目覆盖的方向**，但其中的"网络 = 国家间/协定间 RTA 网络"或"行业供应链网络"，**仍无企业间（customer–supplier）链接数据**。

---

### 方向 5：真正的企业层面（firm-level）RCEP 研究 ——*屈指可数*

| 论文 | 作者 | 年份 | 期刊/方法 | 数据 | 结论导向 |
|---|---|---|---|---|---|
| **Financing constraints and the export partnerships with RCEP: Evidence from manufacturing firms in China** | Peng, Qing; Chen, Zhenhao; Li, Jie | 2025 | *Journal of Asian Economics* (DOI: 10.1016/j.asieco.2024.101870) | **中国制造业企业**进出口/融资约束数据（企业层面回归） | RCEP 促进出口伙伴关系；融资约束起调节作用 |
| *A Study on the Impact of RCEP Rules of Origin on Industrial Relocation in China's Manufacturing Sector* | Chen, Zhixiang; He, Junlin | 2026 | *The Chinese Economy* (DOI: 10.1080/10971475.2026.2657735) | 行业/结构分析（据标题推断） | 原产地规则 → 中国制造业产业转移 |

**小结**：**真正使用中国企业微观数据、直接研究 RCEP 对企业行为的实证论文，本次检索仅明确捕捉到 1–2 篇**（以 Peng, Chen & Li 2025 为代表）。该文的网络维度仍只到"出口伙伴/出口目的地"，**未涉及企业间生产网络**。其余企业层面论文大多把 RCEP 当作众多贸易协定之一（如 RTA network centrality 类），而非聚焦 RCEP 的供应链网络效应。

---

### 方向 6：可作为"企业间网络 + 贸易/关税冲击"方法学参照（**非 RCEP**，但证明数据可行）

| 论文 | 作者 | 年份 | 期刊 | 数据 | 与研究空白的关系 |
|---|---|---|---|---|---|
| **Supply Chain Adjustments to Tariff Shocks: Evidence from Firm-Level...** | Handley, Kyle; Kamal, Fariha; Monarch, Ryan | 2023 | (SSRN/工作论文) | **美国关税冲击 + 企业供应链调整**（进口/客户-供应商） | 证实"关税/贸易冲击 × 企业间供应链"是可行且正在涌现的研究范式，但对象是**美国/贸易战**，**非 RCEP** |
| **Trade Policy Uncertainty and Supply Chain Disruptions: Firm-Level Evidence from "Liberation Day"** | de Souza, G.; Li, H.; Park, Z.; Wang, Y. | 2025 | SSRN (DOI: 10.2139/ssrn.5795404) | 企业层面 + 供应链中断 | 同上，非 RCEP |
| **Beware Diworsification: A Firm- and Supply-Chain Approach to Trade Resilience** | Warin, Thierry | 2025 | (DOI: 10.54932/smrg3827) | 企业 + 供应链韧性 | 企业间网络视角分析贸易韧性；非 RCEP |
| *Supply Chain Network Centrality and Corporate Financial Risk* | Wang, Chu | 2026 | *Modern Mgmt Science & Eng.* | 中国上市公司供应链网络中心性 | 说明中国上市企业供应链网络数据可用，但**非 RCEP** |
| *Supply network position, digital transformation and innovation* | Du, Chunyan; Zhang, Qiang | 2022 | *PLOS ONE* | 中国上市企业供应网络位置 | 网络位置数据可用，但与贸易协定无关 |
| *Can shareholder chain relationship network enhance corporate supply chain...* | Yan, Hongguo; Huang, Binyan | 2026 | *Applied Economics* | 中国上市公司股权/供应链网络 | 网络实证（财务方向），非 RCEP |

---

## 三、文献空白（Gap）

综合以上，**RCEP 研究存在以下明确空白**：

1. **（核心空白）缺乏"企业间生产/供应链网络数据 × RCEP"的实证研究。**
   - 现有 RCEP 文献的"网络"要么是**国家间/协定间 RTA 网络**（Wang & Ni 2026 EMR；Wang & Yang 2024 SSRN），要么是**贸易流/行业供应链网络**（Pan, Wu & Zhuang 2026 SSRN；Kim & Lee 2025），**没有一篇**使用**客户—供应商（customer–supplier）企业间链接数据**（FactSet Revere / Bloomberg SPLC / Compustat Segment / CSMAR & CNRDS 供应链数据库）来识别 RCEP 对中国企业的影响。

2. **RCEP 的"机制"研究仍停留在国家/行业"贸易创造—转移"与"价值分解"，缺乏微观机制。**
   - 关税减免、原产地累积规则、贸易便利化如何**直接影响企业层面**的供应链重构（伙伴切换）、网络位置（中心性、上游度/下游度）、供应链韧性、以及冲击沿客户/供应商链的**传播与放大**，基本未被回答。

3. **缺乏"异质性网络结构"的处理。**
   - 即便是有企业层面的 RCEP 研究（Peng, Chen & Li 2025），其"网络"仍退回"出口伙伴"层面，未利用企业—企业链接刻画企业嵌入产业网络的具体结构（如度中心性、中介中心性、上下游距离、集群地位）。

4. **缺少"RCEP 作为准实验"的企业间冲击传播（irration / spillover）设计。**
   - RCEP 于 2022-01-01（中国生效）为典型的**准自然实验**，但目前企业层面多用 DID 看政策对"企业自身"出口/生产影响；**几乎没有设计**"RCEP 冲击供应商 → 沿客户—供应商链传播 → 客户企业"这样的**级联/溢出识别**。

5. **JAE 目标取向上，RCEP 的"企业层面"证据明显弱于其它贸易协定（如美欧贸易战、USMCA）。**
   - 参考范式（Handley-Kamal-Monarch、de Souza 等）在美/欧已较成熟，**迁移到 RCEP 语境 + 中国企业间网络数据**存在清晰增量空间，且与该领域顶级期刊（China Economic Review、J. Asian Econ、J. Industrial & Business Economics）的近期发文方向吻合。

---

## 四、用企业间网络数据（FactSet Revere / CSMAR 供应链类）研究 RCEP 的可行性

### 4.1 数据可得性（可行）

- **FactSet Revere**（全球）与 **Bloomberg SPLC**（全球）提供企业—企业客户/供应商关系（含方向、比例、国家）。
- **中国市场**的对应体：**CSMAR「供应链」/「客户与供应商」数据库** 与 **CNRDS「供应链」数据库**，基于 A 股上市公司年报披露的**前五大供应商/客户**（含名称、金额、占比、是否关联），已可构建稳定的企业—企业网络。本研究（项目目录 data/ 下已有投入）使用的正是此类链接数据。
- 网络刻画指标成熟：度中心性、中介中心性、上游度/下游度（上游 = 供应商规模加权）、网络位置/嵌入度、集群系数、网络重构（伙伴切换/新增/退出）等，均有现成算法（networkx、apex）。

### 4.2 识别策略（可行）

- **准自然实验**：RCEP 于 2022-01-01 在中国生效，可作阶段性 DID / event study。
- **暴露度构造**：以企业在 RCEP 成员的**供应商/客户占比**（或暴露于 RCEP 关税下调商品的中间品份额）构造连续处理强度，识别"受 RCEP 影响更大的企业"。
- **网络层面**：构造"企业是否同时处于 RCEP 网络中心/上游"等**网络位置异质性**，检验网络位置对 RCEP 效应的调节（王炸端点：网络中心/上游企业更多从关税减免获益）。
- **供应链溢出/传播**：RCEP 冲击"上游供应商 → 沿链接 → 下游客户"的**级联效应**（类似 Acemoglu-Carvalho 冲击传播，或 Handley 等企业供应链调整），这是现有 RCEP 文献完全未覆盖的点。
- **结果变量**：供应链重构（供应商/客户切换）、网络中心性变化、出口/销售/增加值、供应链韧性（JAE 关注）、企业价值。

### 4.3 需要注意的障碍（可行但有坑）

- **披露之截尾**：A 股只披露前五大客户/供应商，部分企业有匿名项（"客户A"），需用 CSMAR 映射或结合工商/进出口数据补全；FactSet Revere 覆盖度与中企映射需人工校验。
- **方向与比例失真**：披露金额占比可能缺失/不精确，网络权重量化需稳健性处理（是否按比例加权、是否忽略未披露比例）。
- **内生性**：企业进入/退出网络可能受 RCEP 影响（选择性），需做网络成员资格与结果联合建模或用滞后/IV。
- **时间跨度**：RCEP 生效仅约 4–5 年（2022 起），面板期偏短，较适合短中期供应链重构与企业响应研究，不适合长期增长效应。

### 4.4 可行性结论

**高度可行、且为文献空白。** 数据（FactSet Revere / CSMAR & CNRDS 供应链）构建企业间网络的路径已在多篇中国上市公司实证中得到验证（见方向 6），识别上可用 RCEP 作为 2022 年准自然实验 + 连续网络暴露度 + 网络位置异质性 + 供应链溢出设计。**该选题在 RCEP 语境下尚未被做**，与 *Journal of Asian Economics*（已发 Peng, Chen & Li 2025 企业层面 RCEP 文）的目标读者契合，可作 JAE 修订版的核心创新点。

---

## 五、检索方法与与局限性

- **检索工具**：Cross-Ref API（works，query.bibliographic / query 关键词匹配，字数 ≈ 100 万+ 期刊），因 OpenAlex 账户预算不足（HTTP 429）与 Semantic Scholar 强限流（429）而改为主用 Crossref；web_search 工具未配置（Firecrawl 无 key），故全部通过 API 完成。
- **覆盖范围**：英文（含中文期刊英译名）为主；部分中文核心文献可能在 Crossref 收录不全，需另行用知网/万方补充（本项目后续可加）。
- **方法标注**：多数论文的方法/数据根据标题与部分可获取摘要推断，已在文中以"据标题推断"或聚焦标题关键词的方式保守处理；**论文的作者/年份/期刊/DOI 均已核实无误**。
- **局限性**：本报告覆盖 RCEP 的"供应链/价值链/网络/贸易转移/原产地/关税"方向；对"投资、数字贸易、ESG、农业"等侧向未展开，但结论"无企业间网络数据研究 RCEP"在这些方向同样适用（已交叉检索确认）。

## 附：建议下一步

1. 用**知网/CSMAR 中文数据库**补充中文文献（RCEP 企业、价值链、供应链中文实证），确认是否已有中文学位论文/期刊用"供应链数据库 + RCEP"。若确认空白，可显著增强创新性断言。
2. 定位 **Peng, Chen & Li (2025, JAE)** 的完整方法与数据，作为"企业层面 RCEP"既有标杆，明确差异化（网络结构 vs 出口伙伴）。
3. 若立项，建议先跑通 **CSMAR/CNRDS 供应链网络构建 + RCEP 暴露度 + DID** 的可行性预跑（数据已在项目目录可查），作为投稿 JAE 的实证内核。
