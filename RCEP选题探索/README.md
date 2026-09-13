# RCEP 选题探索 — 工作区说明

> 定位：基于 REPC（RCEP 官方资料库 + 产品级数据管道）已建成的基础，
> 探索 4~6 个有价值的 RCEP 选题，逐一跑双固定效应主回归 + 预趋势，
> 确定其可实现性。**成功/失败的尝试均如实归档。**

工作区：`C:\Users\97328\Desktop\学习\论文、项目\供应链冲击\RCEP选题探索`

---

## 目标

在**亚洲内部**（不使用美国作为核心处理）的前提下，找到：
1. 文献空白干净、有价值
2. 用现有 REPC 数据**可实现**（有产品级关税暴露度 + 供应链结果变量）
3. 跑出**双固定效应主回归 + 预趋势**，确定因果识别是否成立

---

## 已确认的关键数据资产（来自 REPC/08_rcep_analysis）

### 处理变量（RCEP 增量关税暴露度，产品级）
- `china_import_rcep_policy_incremental_hs12_2015_2024.csv` — HS6×伙伴×年份 RCEP 增量降税
- `china_import_rcep_policy_hs12_2015_2024.csv` — 政策税率
- `china_hs6_mfn_applied_hs12_2015_2024.csv` — MFN 基线
- `china_legacy_fta_counterfactual_hs12_2022_2024.csv` — 无RCEP反事实（旧FTA）
- `Global share weighted incremental cut pct` — 连续暴露度（已有）

### 供应链结果变量（HS6×年份，5192个HS6，50948行）
| 变量 | 含义 |
|------|------|
| `china_total_import_value` | 中国该HS6总进口 |
| `rcep_import_value` / `rcep_import_share` | RCEP来源进口额/份额 |
| `japan_import_value` / `japan_import_share` | 日本来源份额 |
| `supplier_hhi` / `supplier_hhi_excluding_micro` | 供应商集中度 HH |
| `supplier_count_positive` / `supplier_effective_number` | 供应商数/有效数 |
| `supplier_count_excluding_micro` | 排除小微后的供应商数 |
| `largest_supplier_share` | 最大供应商份额 |
| `non_rcep_import_share` | 非RCEP份额 |
| `bec5_intermediate_strict` | BEC中间品(严格) |
| `bec4_intermediate_share` | BEC中间品份额 |

### 控制变量
- World Bank 宏观（GDP、FDI）+ LPI（海关、物流、基础设施）— 已下载
- BEC 中间品分类 — 已构造（5205个HS6映射）

### REPC 已跑的基准（诚实记录，供对比）
- 严格 M6 对数TWFE：-0.0024（p=0.903）
- PPML：0.0855（p=0.116）
- **识别问题**：日本贡献 91.5% 处理变异 → 目前只能定位"中日首次FTA"效应

---

## 探索方法（按 plan 模式，每步独立归档）

1. **文献调研**（进行中）：4个方向 → 找空白
2. **选题设计**：选 4-6 个候选，每个明确 RQ + 识别 + 结果变量
3. **数据管线**：确认每个选题所需变量都存在
4. **双固定效应主回归 + 预趋势**：逐一跑，判断可实现性
5. **归档**：每个选题一个 `audit/` 文件夹，成功/失败都保留 code + results + 结论

---

## 进度状态

- [x] 建立工作区
- [x] 确认 REPC 数据资产
- [ ] 文献调研（待4 Agent返回）
- [ ] 选题设计
- [ ] 双固定效应主回归 + 预趋势（逐选题）
- [ ] 归档
