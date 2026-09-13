# RCEP 与中国企业供应链网络结构 — 独立研究工作区

> 方向：**RCEP 区域一体化 如何重塑中国上市公司的供应链网络结构（区域化 / 多样性 / 集中度）**
> 本工作区只研究**亚洲内部**格局，美国关税仅作为竞争性解释/控制，不作为核心处理。
> 独立于 `RCEP_JAE_修订` 主工作区，但与主工作区共享同一份已验证的 FactSet / CSMAR / 关税数据源。

---

## 一、研究问题

**RCEP（2022-01 生效）是否改变了中国上市公司供应链网络的形状？**

具体地，RCEP 作为**亚洲区域一体化政策**，可能：
1. **提高区域化**（regional concentration）：企业的供应链伙伴是否向 RCEP 成员国集中？
2. **改变多样性**（diversification）：企业的供应链伙伴国数量/国家多样性是否变化？
3. **重塑集中度**（supplier/customer HHI）：是否更依赖 RCEP 区域的几家核心伙伴？

---

## 二、核心结果变量（全部由 FactSet 网络数据构建，不需海关）

| 变量 | 定义 | 含义 |
|------|------|------|
| `RCEP_share` | 企业 i 在 t 年，与 RCEP 成员的供应链关系数 / 总关系数 | 区域化程度 |
| `Regional_HHI` | 企业 i 在 t 年，供应链伙伴国分布的赫芬达尔指数（区域集中度） | 是否向某些国家集中 |
| `Diversification_entropy` | 企业 i 在 t 年，供应链伙伴国数的香农熵（= −Σ p log p） | 国家多样性 |
| `N_countries` | 企业 i 在 t 年，供应链覆盖的国家数 | 网络广度 |
| `N_RCEP_countries` | 企业 i 在 t 年，涉足的 RCEP 成员国数 | RCEP 网络覆盖 |

---

## 三、处理变量

- `Post2022`：2022 及之后 = 1（RCEP 对多数成员生效）
- `RCEP_group`：伙伴国是否 RCEP 成员（JP, KR, AU, NZ 及东盟十国）
- （国家特定进入时间：印尼/菲律宾 2023，作为稳健性）

---

## 四、识别策略

**基准**：关系对层面 / 企业层面的 DID 与事件研究

```
Y_{it} = β × (Post2022_t × RCEP_Exposure_i) + γ X_{it} + μ_i + λ_t + ε_{it}
```

- `Y_{it}`：上述网络结构指标
- `RCEP_Exposure_i`：RCEP 生效前（基期）企业 i 对 RCEP 的暴露（如基期 RCEP_share）
- **聚类**：伙伴国层（主推断）；关系对层仅作敏感性
- **核心检验**：平行趋势（事件研究 leads）+ 时间安慰剂 + 排除亚洲非 RCEP 对照

**关键理念**："网络结构"作为结果变量，识别的是**区域化/再集中**，而非单纯的关系增减——这恰好检验"RCEP 是否让供应链向亚洲集中"这个对 JAE 而言最有故事的问题。

---

## 五、数据溯源（必须遵守）

- FactSet 供应链关系（已验证）：`（上级）data/derived/pair_year.parquet` 及原始 `cn_global_links.parquet`
- CSMAR 财务：`（上级）data/cleaned/csmar_firm_panel.parquet`
- RCEP 成员定义：JP, KR, AU, NZ + 东盟十国（BN, KH, ID, LA, MY, MM, PH, SG, TH, VN）

**禁止**：为获得显著性而删观测、改聚类、调样本。

---

## 六、目录结构

```
network_structure/
├── README.md            ← 本文件
├── pap/                 ← 预登记分析计划（PAP）
├── paper/               ← 最终论文（LaTeX）
├── code/                ← 可复现分析脚本
├── data/derived/        ← 生成的网络结构指标面板
├── results/tables/      ← 机器生成的回归表
├── results/figures/     ← 投稿级图
└── audit/               ← 数据溯源 + 审计
```

---

## 七、进度状态

- [x] 建立工作区
- [x] 确定研究方向（方向②：网络结构当结果变量）
- [ ] 编写 PAP（预登记分析计划）
- [ ] 构建企业级网络结构指标面板
- [ ] 基准回归 + 事件研究 + 平行趋势
- [ ] 时间/空间安慰剂
- [ ] 异质性（行业、规模、所有制）
- [ ] 稳健性（排除疫情、亚洲非RCEP对照、国家特定时间）
- [ ] 论文撰写（elsarticle, JAE 格式）
