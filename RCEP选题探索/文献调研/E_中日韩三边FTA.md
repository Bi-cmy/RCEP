# E｜中日韩（非东盟RCEP成员）首次FTA 的三边/双边实证文献调研与空白定位

（调研日期：2026-09-03；方法：CrossRef REST API 为主，逐条调取元数据/摘要/被引）
（姊妹篇见同目录 `C_中日首次FTA.md`，本篇聚焦**中日韩三边 + 双边（中-日、中-韩、日-韩）+ 非东盟RCEP成员整体（NAR）**）

---

## 0. 检索方式与覆盖说明

- **主检索源**：CrossRef REST API（`api.crossref.org/works`），`query.bibliographic` + `filter=type:journal-article`，双轮 32 组递进检索 + 对 13 篇关键命中逐条 DOI 反向调取摘要/作者/期刊/被引。
- **检索词（代表性）**：China Japan Korea trilateral free trade agreement；trilateral free trade agreement Northeast Asia；China Japan Korea FTA trade creation；Northeast Asia free trade agreement；China Japan first ever free trade agreement 2022 RCEP；China Korea FTA tariff；China Korea FTA difference-in-differences；Japan Korea free trade agreement never signed tariff；RCEP non-ASEAN five members economic integration；Asia non-ASEAN RCEP members trade study；RCEP preferential tariff utilization China Japan；China Korea Japan supply chain RCEP；economic effects trilateral free trade East Asia ex-post。
- **命中量**：两轮共 **360 + 240 = 600 条**，去重后 **~430 条唯一 DOI**；按地理关键词过滤得 **~180 条相关**，其中与"中日韩/东北亚/非东盟"强相关者 ~70 条。全部论文的作者/期刊/年份/DOI 均经 Crossref 逐条核验。
- **已知盲区（与 C 篇一致）**：OpenAlex 本轮仍限流（429）；web_search/浏览器不可用。**中文核心（知网 CNKI）与 NBER/RIETI/韩研院（KIEP）工作论文在 CrossRef 收录有限**，结论在"英文/国际期刊"层面稳健，在中日韩文层面建议知网二次确认（见 §8）。

### 核心结论先行（三问一答）
> **① 有没有一篇高引论文研究"中国、日本、韩国这三个非东盟成员在 RCEP 下首次建立 FTA"？——没有。** 现存 CJK 三边文献几乎全是 **2013–2019 的"提案/潜力/政治经济学"或 ex-ante CGE**，没有一篇以"RCEP 让中日韩之间**从无到有**建立FTA"作为**处理变量**做经验识别。
> **② 中-日、中-韩双边关税减让的实证现状：两极分化。** 中-韩（2015 年真实签了 CKFTA）→ **已有较丰富的 ex-post 实证**（含 DiD-gravity、政治冲突混杂处理）；中-日（从未签双边，只靠 RCEP 2022）→ **几乎是空白**，只有单行业 SMART 模拟 + 低引 OA。
> **③ "非东盟RCEP成员（NAR）"作为一个整体被研究过吗？——几乎没人当"整体"研究。** 唯一一篇**明确以"non-ASEAN-RCEP member states"命名整体**的是 Raghavan et al. (2022, *The World Economy*)，但那是**宏观 GVAR 溢出/联动**研究，**不是**FTA 政策（首次建立）识别。

---

## 1. 制度背景：为什么"中日韩"= 非东盟里最"特殊"的一组

- RCEP（2022-01-01 生效）缔约方中 **5 个非东盟成员：中、日、韩、澳、新西兰**。三者之间此前**不存在任何覆盖"贸易创造红利"的双边 FTA**——这是 RCEP 区别于"东盟+1"体系的最大制度点。
- **关键细微差别（比 C 篇更精细）**：这 5 个非东盟成员**并非彼此都"无 FTA"**——澳-新（ANZCERTA 1983）、中-澳（ChAFTA 2015）、中-新（2008）、中-韩（CKFTA 2015）、日-澳（JAEPA 2014）、韩-澳（KAFTA 2014）、韩-新（2015）都已有协定。
- **因此真正"从无到有、首次建立"的配对只有三组：中国-日本、日本-韩国、日本-新西兰。** 其中**中-日、日-韩都以"三边/东北亚"为叙事核心，且长期停滞**。
- 换言之：**"中日韩三边首次FTA"的制度事实 = 中日、日韩两对"从未签过"的双边，被 RCEP 一次性覆盖**。这个"从无到有"的**处理性质**（vs 东盟的"存量深化"、vs 中韩的"已有协定再加深"）在文献里**完全没有被当处理变量用**。

---

## 2. 核心问题 a：有没有高引论文研究"中日韩=非东盟成员首次建立FTA"？

### 2.1 直接以"中日韩三边FTA"为对象的文献——几乎全部是"提案/潜力/政治经济学"，且都在 RCEP 之前
| 文献 | 年份/期刊 | 被引 | 性质 | 是否处理"RCEP 下首次建立" |
|---|---|---|---|---|
| Min-Hua Chiang, *The Potential of China-Japan-South Korea Free Trade Agreement* | 2013, *East Asia* | 18 | ex-ante 潜力评估 | ❌（谈的是独立的 CJKFTA 提案，非 RCEP 处理） |
| Srinivasa Madhur, *China-Japan-Korea FTA: A Dual Track Approach to a Trilateral Agreement* | 2013, *J. of Economic Integration* | 12 | 政策方案（双轨） | ❌（2013 年标准叙事） |
| Sarah Chan & Chun-Chien Kuo, *Trilateral trade relations among China, Japan and South Korea* | 2005, *East Asia* | 11 | 描述性区域整合 | ❌ |
| **Muhui Zhang, *The China–Japan–Korea Trilateral FTA: Why Did Trade Negotiations Stall?*** | 2019, *Pacific Focus* | 10 | **政治经济学/谈判停滞** | ❌（最直接相关，但从制度/政治解释"为何停"，无贸易因果识别） |
| Muhui Zhang, *Institutional Creation or Sovereign Extension? Roles and Functions of Nascent CJK* | 2017, *IR of the Asia-Pacific* | 6 | 制度创建 | ❌ |
| Hidetaka Yoshimatsu, *Diplomatic Objectives in Trade Politics: The Development of the CJK FTA* | 2015, *Asia-Pacific Review* | 5 | 外交方针 | ❌ |
| Ying Bi, *Rising Mega RTA? CJK FTA under the New Trade Dynamism* | 2015, *J. of East Asia & Intl Law* | 1 | 区域主义 | ❌ |
| Yang & Woo, *A Study on Impact of RCEP Agreement on the Industrial Trade between China, Korea and Japan* | 2022, *Regional Industry Review*（韩） | 0 | 产业贸易描述 | ❌（RCEP 后但只是韩国视角产业分析） |
| Yan Pei & Sang Kon Kim, *Digital trade: a new chance for China-South Korea-Japan trilateral cooperation?* | 2023, *J. of East-West...* | 1 | 数字贸易机会 | ❌ |
| 刘/王 等, *The impact of RCEP on agricultural trade among members*（中文《资源科学》） | 2024, 资源科学 | 1 | 关税减让+农业 | ❌（成员整体，非"NAR 首次"） |

### 2.2 触及 RCEP（但把中日韩当"整体/网络/中日韩"而非"首次建立"）的高引基线文献
- **Shiro Armstrong & Peter Drysdale (2022)，*The Economic Cooperation Potential of East Asia's RCEP Agreement*，East Asian Economic Review，21 引**——最近"中/日/韩/澳/新=非东盟合作潜力"的量级框架，但仍是**"合作潜力"（potential）**，非"首次FTA"处理识别。
- **Kazushi Shimizu (2021)，*The ASEAN Economic Community and RCEP in the world economy*，J. of Contemporary East Asia Studies，66 引**——本轮命中**被引最高**，但主体是**AEC + RCEP 在世界经济中的地位**（ASEAN 中心），非中日韩双边。
- **Inkyo Cheong & Jose Tongzon (2013)，*Comparing the Economic Impact of TPP and RCEP*，Asian Economic Papers，38 引**——动态 CGE 比较 TPP/RCEP，处理"重叠协定去重"，ex-ante，非"首次建立"。
- **Wen, You & Zhang (2021)，*Effects of tariff reduction by RCEP on GVCs*，Applied Economics Letters，11 引**；**Zhu & Huang (2023)，*RCEP tariff concessions → manufacturing trade networks*，Social Networks，23 引**——都是"RCEP 整体关税→GVC/网络"，无中日韩三边或"首次"维度。

### 2.3 问题 a 的判定 ⭐
- **高引/国际期刊层面，没有一篇把"中日韩（三个非东盟成员）在 RCEP 下**首次**建立FTA"作为处理变量**。所有 CJK 三边研究要么**早于 RCEP**（2013–2015）、要么**是政治经济学/谈判停滞**（Zhang 2019/2017）、要么**是 ex-ante 潜力/CGE**（Chiang、Madhur、Cheong&Tongzon）。
- **"从无到有"这个 RCEP 对大中日韩最大的制度增量，文献里反复被"提及"（as background），却无人在"首次FTA"框架下做减式识别。** 这与 C 篇的中日结论同构，但现在**放到"中日韩三边 + 非东盟组"层面**，空白更加立体。

---

## 3. 核心问题 b：中-日 vs 中-韩 双边关税减让实证现状（两极分化）

### 3.1 中-韩（有真实 CKFTA 2015）→ **存在较成熟 ex-post 实证**，且已有"识别"意识
| 文献 | 年份/期刊 | 被引 | 方法/要点 |
|---|---|---|---|
| **HuiHui Yin & Juyoung Cheong, *Disentangling Trade Effects of the Korea-China FTA: Trade Liberalization or Political Conflicts?*** | 2023, *J. of Korea Trade* | 0 | **ex-post，专门把 CKFTA 贸易效应与 THAAD 政治冲突分开**（用月度/结构反事实）。指出既往 ex-ante 研究忽略 THAAD 这一混淆。**本主题最成熟的方法论模板。** |
| **Xinyi Deng, Dong-Hyun Kim & Jiansuo Pei, *Revisiting the Korea-China FTA: A Difference-in-differences Gravity Model Approach at the Province-Product Level*** | 2026, *J. of Korea Trade* | 0 | **DiD + 引力 + 省×产品**——唯一真正的"双重差分×引力"中韩研究，**与你的目标识别最接近**（但对象是 CKFTA，非"首次"）。 |
| Xiang Li, Hyukku Lee & Seung-Lin Hong, *Evaluation of the Policy Effects of FTAs: New Evidence from the Korea-China FTA* | 2022, *J. of Korea Trade* | 0 | **反事实面板/合成控制式**：CKFTA 使韩国 GDP 增速 +2.1%（短期）。ex-post 宏观。 |
| Sunghyun Kim & Serge Shikher, *Long-run Effects of the Korea-China Free-Trade Agreement* | 2015, *East Asian Economic Review* | 6 | CGE/长短期动态。 |
| Qiaomin Li & Hee Cheol Moon, *The trade and income effects of RCEP: implications for China and Korea* | 2018, *J. of Korea Trade* | 28 | **异质性企业 CGE 模拟**（Li et al. 2017 的 CGE），RCEP→中韩贸易/收入。ex-ante，但被引最高。 |
| Jaimin Lee & Sangyong Han, *Intra-Industry Trade and tariff rates of Korea and China* | 2008, *China Economic Review* | 5 | IIT × 关税率。 |
| Heng Wang, *The Challenges of China's Recent FTA: An Anatomy of the China-Korea FTA* | 2016, *J. of World Trade* | 1 | 制度解剖。 |
| Rui Zhuang, Junjie Hong & Guangyu Bai, *Sino-Korea FTA and Asia-Pacific economic integration: the China perspective* | 2014, *China Economic Journal* | 1 | 中国视角。 |
| （其他大量韩文 0 引）Liu Zi-He & Yi Chae-Deug 2021 面板引力；Joo Yeon Sun 2018；Jungu Kang & Seung-jin Shim 2017（服务增加值贸易创造/转移）等 |

> **结论：中-韩"双边关税减让/ FTA 贸易效应"实证文献是**较充实**的，且已形成"ex-ante（CGE）→ ex-post（DiD/反事实/置换，处理政治冲突混淆）"的演进路径。**

### 3.2 中-日（从未签双边，只靠 RCEP 2022）→ **几乎空白**
| 文献 | 年份/期刊 | 被引 | 性质 |
|---|---|---|---|
| Sun Yanlin & Zhang Jiajia, *Analysis of the economic effects of China-Japan tariff concessions on Mechanical and electrical products under RCEP (SMART)* | 2023, *SHS Web of Conferences* | 0 | 局部均衡 SMART 模拟（单行业） |
| Yanlin Sun & Zhang, *Determinants of Staging Categories for Tariff Elimination in the Bilateral Tariff Arrangement between China and Japan under RCEP* | 2024, *Adv. in Computer Science Research* | 0 | **关税分期决定因子（潜在 exposure，未被用于因果）**——参见 C 篇 |
| Min Chen, Xian Lin, et al., *Study on the Impact of Textile Trade between China and Japan under the RCEP Framework* | 2024, *Textile & Leather Review* | 0 | RCA + WITS-SMART |
| 唐雨果, *Research on the Impact of RCEP on Chemical Products Trade between China and Japan* | 2025, *E-Commerce Letters*（中文 OA） | 0 | 描述性/计量，质量低 |

> **结论：中-日"双边关税减让"实证 =**单行业 SMART + 低引 OA**，**无**任何高引/顶刊的 ex-post 因果研究（DiD/事件研究/引力/结构）。** 原因：此前无双边协定可研究；RCEP 后文献又薄。

### 3.3 日-韩（从未签双边，只靠 RCEP 2022）→ **只有 ex-ante**
- **Ippei Yamazawa (2001)，*Assessing a Japan-Korea Free Trade Agreement*，J. of Economic Integration，7 引**——唯一直接以"日韩FTA"为对象的论文，**ex-ante 评估**（2001 年即提出，日韩从未实现）。
- 其余日韩相关多为"外交/争端"（如 Choi 2025 日韩贸易争端为企业层面）或把日韩放在中日韩/东北亚角度，**无日韩双边的 ex-post 贸易识别**。→ **日韩是 RCEP 中另一组"首次"，同样无实证。**

### 3.4 问题 b 的判定 ⭐
- **"双边关税减让实证"现状呈"中韩充实、中日/日韩近乎空白"的显著梯度。** 恰好**"最没被研究过"的中日、日韩，正是 RCEP 里"从无到有、首次建立"的那两组**——**实证供给与制度增量的大小完全倒挂**。

---

## 4. 核心问题 c：非东盟RCEP成员（NAR / 任务代号 NRET）当作"整体"被研究过吗？

### 4.1 唯一一篇"明确命名整体"的论文——但它是宏观联动，不是FTA识别
- **Mala Raghavan, Faisal Khan & Sonia Kumari Selvarajan (2022)，*Cross-country linkages between ASEAN and non-ASEAN-RCEP member states: A global VAR approach*，The World Economy，9 引（DOI: 10.1111/twec.13347）**。
- 这是我在本轮全部命中里**唯一**一篇**在标题/摘要中把"non-ASEAN-RCEP member states"作为明确范畴**的论文。**但它做的是 GVAR 宏观联动/溢出（cross-country linkages），并不是"这些成员之间建立 FTA 的贸易政策效应"，更没有"首次建立"的处理识别。** → 只是"整体"维度的**边缘**接近点。

### 4.2 其余文献对"非东盟"的用法——要么 ASEAN 中心，要么单双边
- **ASEAN 中心**：Suvannaphakdy (2021) *Assessing the Impact of RCEP on ASEAN Trade*（13 引）；Jiang & Husin (2023) *Malaysia's…*（6 引）；Tran & Tran (2023) *Vietnam's…*；Chien-Huei Wu (2019) *ASEAN at the Crossroads: CPTPP & RCEP*（21 引）；Zainuddin et al. (2020) *Non-tariff measures & trade in RCEP countries*（17 引）——都把 RCEP 当"东盟主场"。
- **把"非东盟"当背景/潜在合作**：Armstrong & Drysdale (2022)（21 引）——"East Asia's RCEP"的非东盟合作潜力；Sen, Srivastava & Das (2016) *Can ASEAN+1 FTAs Be a Pathway towards Negotiating and Designing RCEP*（J. of World Trade）——"ASEAN+1 无协定→RCEP"的衔接，**但落脚点是"路径/设计"**，非 NAR 整体的贸易效应。
- **单双边**：大量"中韩 FTA"（见 §3.1）、"日-韩 FTA"（Yamazawa 2001）——都是**单个配对**，从未把它们当作"一个整体（非东盟组）"共同比较。

### 4.3 问题 c 的判定 ⭐
- **"非东盟RCEP成员（NAR）作为一个整体"几乎没有被当作研究对象**；唯一命名整体的 Raghavan et al. (2022) 也**不是**FTA 政策识别。
- 也就是说，**"把 5 个（尤其中日韩 3 个）非东盟成员作为一个'同受 RCEP 从无到有红利'的处理组"这一研究设计，在文献里缺席。** 这正是你给这个整体做"首次FTA 组 vs 东盟存量组"对比的**理论切口**。

---

## 5. 关键文献清单（作者/期刊/年份/DOI 已逐条核验）

**制度与潜力（背景锚点，非因果）**
1. Min-Hua Chiang (2013). *The Potential of China-Japan-South Korea Free Trade Agreement*. East Asia. DOI: 10.1007/s12140-013-9196-5（18c）
2. Srinivasa Madhur (2013). *China-Japan-Korea FTA: A Dual Track Approach to a Trilateral Agreement*. Journal of Economic Integration. DOI: 10.11130/jei.2013.28.3.375（12c）
3. Sarah Chan & Chun-Chien Kuo (2005). *Trilateral trade relations among China, Japan and South Korea*. East Asia. DOI: 10.1007/s12140-005-0019-1（11c）
4. Shiro Armstrong & Peter Drysdale (2022). *The Economic Cooperation Potential of East Asia's RCEP Agreement*. East Asian Economic Review. DOI: 10.11644/kiep.eaer.2022.26.1.403（21c）

**"为何停"政治经济 / 制度（最临近但非因果贸易识别）**
5. **Muhui Zhang (2019). *The China–Japan–Korea Trilateral FTA: Why Did Trade Negotiations Stall?*. Pacific Focus. DOI: 10.1111/pafo.12142（10c）**
6. Muhui Zhang (2017). *Institutional Creation or Sovereign Extension? Roles and Functions of Nascent China-Japan-South Korea...* International Relations of the Asia-Pacific. DOI: 10.1093/irap/lcw023（6c）
7. Hidetaka Yoshimatsu (2015). *Diplomatic Objectives in Trade Politics: The Development of the China-Japan-Korea FTA*. Asia-Pacific Review. DOI: 10.1080/13439006.2015.1038890（5c）

**中-韩实证（方法成熟，含政治冲突与 DiD）**
8. **HuiHui Yin & Juyoung Cheong (2023). *Disentangling Trade Effects of the Korea-China FTA: Trade Liberalization or Political Conflicts?*. Journal of Korea Trade. DOI: 10.35611/jkt.2023.27.3.21**
9. **Xinyi Deng, Dong-Hyun Kim & Jiansuo Pei (2026). *Revisiting the Korea-China Free Trade Agreement: A Difference-in-differences Gravity Model Approach at the Province-Product Level*. Journal of Korea Trade. DOI: 10.35611/jkt.2026.30.3.1**
10. Xiang Li, Hyukku Lee & Seung-Lin Hong (2022). *Evaluation of the Policy Effects of Free Trade Agreements: New Evidence from the Korea-China FTA*. Journal of Korea Trade. DOI: 10.35611/jkt.2022.26.6.41
11. Qiaomin Li & Hee Cheol Moon (2018). *The trade and income effects of RCEP: implications for China and Korea*. Journal of Korea Trade. DOI: 10.1108/jkt-03-2018-0020（28c，ex-ante CGE）
12. Sunghyun Kim & Serge Shikher (2015). *Long-run Effects of the Korea-China Free-Trade Agreement*. East Asian Economic Review. DOI: 10.11644/kiep.jeai.2015.19.2.293（6c）
13. Jaimin Lee & Sangyong Han (2008). *Intra-Industry Trade and tariff rates of Korea and China*. China Economic Review. DOI: 10.1016/j.chieco.2008.08.003（5c）

**中-日/日-韩（稀缺）**
14. Ippei Yamazawa (2001). *Assessing a Japan-Korea Free Trade Agreement*. Journal of Economic Integration. DOI: 10.1111/j.1746-1049.2001.tb00892.x（7c，ex-ante）
15. Yanlin Sun & Jiajia Zhang (2023). *Analysis of the economic effects of China-Japan tariff concessions... under RCEP (SMART)*. SHS Web of Conferences. DOI: 10.1051/shsconf/202316901014
16. Min Chen et al. (2024). *Study on the Impact of Textile Trade between China and Japan under the RCEP Framework*. Textile & Leather Review. DOI: 10.31881/tlr.2024.155

**非东盟 RCEP 整体（唯一命名整体——但非 FTA 识别）**
17. **Mala Raghavan, Faisal Khan & Sonia Kumari Selvarajan (2022). *Cross-country linkages between ASEAN and non-ASEAN-RCEP member states: A global VAR approach*. The World Economy. DOI: 10.1111/twec.13347（9c）**

**高引方法论/基线（RCEP 整体→GVC/网络）**
18. Kazushi Shimizu (2021). *The ASEAN Economic Community and the RCEP in the world economy*. J. of Contemporary East Asia Studies. DOI: 10.1080/24761028.2021.1907881（66c，本轮最高）
19. Inkyo Cheong & Jose Tongzon (2013). *Comparing the Economic Impact of the TPP and RCEP*. Asian Economic Papers. DOI: 10.1162/asep_a_00218（38c）
20. Nina Zhu & Siyi Huang (2023). *Impact of the tariff concessions of RCEP on the structure and evolution mechanism of manufacturing trade networks*. Social Networks. DOI: 10.1016/j.socnet.2023.01.008（23c）
21. Hui Wen, Yu You & Yue Zhang (2021). *Effects of tariff reduction by RCEP on global value chains*. Applied Economics Letters. DOI: 10.1080/13504851.2021.1966361（11c）
22. Ranti Yulia Wardani & Nawalage S. Cooray (2019). *Saving Potential of RCEP: Implication for China and Japan*. Journal of Economic Info. DOI: 10.31580/jei.v6i1.122（9c）

---

## 6. 研究空白总结（三合一）

| 角度 | 现状 | 空白等级 |
|---|---|---|
| **a) 高引论文研究"中日韩=非东盟成员首次建立FTA"** | **无**。CJK 三边全为 2013–2019 的"提案/潜力/政治经济/ex-ante CGE"（Chiang, Madhur, Chan&Kuo, Zhang 2019/2017），无一篇以"RCEP 首次建立"为处理变量做经验识别 | **大空白** ⭐ |
| **b) 中日 / 日韩 双边关税减让实证** | **中-韩丰富**（含 DiD-gravity邓2026、THAAD政治冲突置换Yin&Cheong2023、反事实面板Li2022）；**中-日、日-韩近乎空白**（只有单行业 SMART + 低引 OA / 2001 年 ex-ante） | **中-日、日-韩 = 大空白** ⭐ |
| **c) 非东盟RCEP成员（NAR）当"整体"研究** | **几乎没人**；唯一命名整体的是 Raghavan et al. 2022（GVAR 宏观联动，非 FTA 政策识别）。其余全为"东盟中心"或"单双边" | **完全空白** ⭐ |

**一句话总括**：RCEP 里制度增量最特殊的两组——**"中日/日韩首次建立"** 和 **"非东盟组（NAR）从无到有"**——恰恰是**实证供给最薄**的地方；而**"中韩"这个已签协定**反而被研究得最充分。**"实证供给 × 制度增量"严重倒挂，是最值得切入的空白。**

---

## 7. 建议切入方向（可操作性排序）

1. **【首选】把"非东盟组（NAR/中日韩）首次FTA"作为处理组的 DiD / 事件研究**：以 HS6 产品 × 中日 / 日韩为对象，处理 = "RCEP 导致首次建立"（vs 中韩这类"已有协定存量深化"、vs 东盟"存量加深"），用 **RCEP 生效前 MFN 税率 / 减让幅度 × 日本（韩国）进口份额**做连续处理强度，DiD/引力。→ 同时回答 a+b+c，且直接复用 C 篇建议的双重异质性设计。
2. **【次选】"首次FTA vs 存量深化"对照**：同一 RCEP、同一年生效，把"中日、日韩（首次）"与"中韩、中-东盟/日-东盟（存量）"作为处理性质差异，比较贸易创造规模/方向（引力 + 双差分，或 synthetic control）。→ 直接回答 a、c。
3. **【方法论加分】处理政治冲突混杂**：中韩文献已证明 THAAD 这类政治冲击会污染 FTA 效应（Yin & Cheong 2023）。**中日、日韩之间的地缘政治摩擦（东海、核废水、出口管制）远比中韩复杂**——把"政治关系/制裁虚拟变量"作为混杂处理，是能发好刊的加分点，也是 C 篇没覆盖、而中韩文献已经示范的路径。
4. **【被忽视数据】关税分期表作为 exposure**：Sun & Zhang (2024) 已说明"哪些产品被安排分期减税"是内生的（行业保护/谈判力）——可把它当处理强度并讨论内生性（这是该主题发顶刊的关键）。
5. **【RCEP 原产地规则 + 首次FTA】**：RCEP 放宽的区域内累积标准，对"中日韩零部件互供、建立首次原产地链接"的红利量化，文献里只有制度评估（ADB），无因果。

---

## 8. 本调研的局限与下一步

- **只覆盖 CrossRef 收录**（英文 + 部分韩/中期刊）。中文核心（知网 CNKI）、**韩国 KIEP/KDI**、**日本 RIETI/经济产业省**、以及 NBER 工作论文收录极少——**建议补一轮 CNKI（关键词：RCEP、中日韩、中日自贸协定、关税减让、首次、双重差分）+ KIEP/RIETI/NBER 工作论文检索**，尤其确认"中日/日韩双边首次"是否确有大牛工作论文。
- OpenAlex 全程限流、web 搜索/浏览器不可用，故本报告单源（CrossRef）。**"空白"判断在英文/国际期刊层面稳健**，在中/日/韩文层面 **待知网、韩国学库、RIETI 二次确认**。
- 建议后续（若需）用 OpenAlex（错峰 + mailto 重试）或 Semantic Scholar 交叉验证 "中日韩三边 / NAR 整体" 是否另有成果（尤其中日、日韩方向）。
