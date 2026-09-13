# REPC 现状与正确做法（供选题设计参考）

> 来源：`REPC/08_rcep_analysis/output/rcep_first_publishability_gate_2026-08-30.md` + `02_models/run_main_ppml.py`
> 目的：避免在选题设计中重蹈"日本主导变异"和"FE不完整"两个坑。

---

## 一、REPC 已完成的规范主回归（诚实记录）

**设计**（符合 AER 标准）：
- 样本：`partner × HS6 × year`，14 个 RCEP 伙伴，2015–2024，严格样本 679,420 行
- **三向固定效应**：`partner_hs6 + hs6_year + partner_year`（全部吸收，`fixef_rm="none"`）
- **处理**：`treatment_intensity = incremental_tariff_cut_pct × post`（连续降税暴露）
- **结果**：`trade_value`（PPML）、`ln_trade_value`（OLS）
- **聚类**：`partner_hs6`（CRV1）
- 工具：`pyfixest`（fepois/feols）+ `pyhdfe`（残差化）

**结果**（REPC 已跑）：
| 模型 | 系数 | 标准误 | p值 | N |
|------|:---:|:---:|:---:|:---:|
| PPML | 0.0855 | 0.0544 | 0.1159 | 395,111 |
| OLS(同PPML样本) | −0.0155 | 0.0273 | 0.5698 | 395,111 |
| OLS(全严格样本) | −0.0024 | 0.0198 | 0.9034 | 679,420 |

→ **三项都不能拒绝零效应**。日本贡献 91.5% 处理变异。

## 二、关键识别问题（必须规避）

1. **日本主导**：日本占处理变异 91.55%（线性残差）/~84.8%（PPML样本）。→ 范围必须收窄为"中日首次FTA"，不能说成14国平均RCEP效应。
2. **伙伴×年份FE缺失时**（如我之前的双向FE），系数−0.096显著——但那是因为没吸收伙伴-年度冲击。**规范做法是必须加入 partner_year FE。**
3. **PPML分离**：零贸易、全零FE组会分离，需用 pyfixest separation_check 处理。

## 三、选题方向如何绕过"日本主导"

要摆脱日本单一驱动，选题应**改变识别维度**：
- 用**非日本伙伴的内在变异**，或
- 用**产品/规则层面的差异**（如 BEC 中间品 vs 最终品）作异质性，而不用"14国平均"
- 或聚焦**特定伙伴组**（东盟、日韩、澳新）而非14国平均

---

## 四、可选选题的候选角度（待文献调研确认）

| 角度 | 结果变量 | 处理 | 规避日本主导？ |
|------|---------|------|:---:|
| A. 中间品vs最终品累积规则差异 | 来源份额/HHI | 增量降税×BEC | ✅ 用产品差异 |
| B. 来源再配置（HHI/供应商数）| 供应商HHI | 增量降税 | ⚠️ 需交互 |
| C. 中日首次FTA | 日本份额 | 日本降税 | ✅ 明确日本 |
| D. 便利化调节（LPI交互）| 贸易额 | 降税×LPI | ✅ 用伙伴制度 |

---

## 五、工具链（Windows 已验证）

```bash
# pyfixest + pyhdfe 做三向FE PPML/OLS（REPC 已用）
pip install pyfixest pyhdfe
```

模型公式：
```
trade_value ~ treatment_intensity | partner_hs6 + hs6_year + partner_year
```

注意：
- 变量名避免 `-` 和 `.`（formulaic）
- PPML 需处理 FE 分离
- 三向 FE 必须 `fixef_rm="none"`（禁用自动吸收，保留全部FE）
