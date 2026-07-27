# M3-P1-2.1 A-first 三工具评测生物学决定本地审计

审计日期：2026-07-27（Asia/Shanghai）  
审计对象：

`M3_P1_2_1_REACTION_PREDICTOR_A_FIRST_THREE_TOOL_BENCHMARK_BIOLOGICAL_DECISION_RECORD_2026-07-27.md`

对象 SHA256：

```text
2622fc6fd955f3395d72a80746b55ceec13ec4e70120f899e647c1208b524e0e
```

结论：**PASS / A-FIRST STRATEGY ACCURATELY RECORDED / NO TOOL WINNER OR PRODUCTION CLAIM**

## 1. 会议决定映射

会议结论包含：

1. 比较弓师兄模型、BioTransformer 3.0–ENVMICRO 和 enviFormer；
2. 在项目测试集上比较；
3. 增加模型未见数据；
4. 比较后再选工具；
5. 三者均不满足时再考虑 C 路线自建数据库。

对象逐项覆盖，且准确映射到黄老师 07-24 §2.1 的 A 专业工具路线。对象没有把条件后备 C
写成当前已选择/已实施的 C，也没有继续把旧 B 建议写成生物学会议选择。

结果：`MEETING_DECISION_COVERAGE = PASS`。

## 2. 三工具状态诚实性

对象分别写为：

```text
internal model:
  waiting handoff / not benchmarked

BioTransformer:
  prior product-only pilot
  old unified contract incompatible

enviFormer:
  paper identity verified
  tool validation in progress
  no project benchmark result
```

未发现：

- 把 BioTransformer 写成最佳工具；
- 把 enviFormer 写成项目验证通过；
- 把弓师兄模型写成已经取得；
- 把三工具比较写成已经完成；
- 把论文结果当项目结果。

结果：`TOOL_STATUS_HONESTY = PASS`。

## 3. enviFormer 论文身份核对

2026-07-27 只读查询 Crossref：

```text
request:
  https://api.crossref.org/works/10.1186/s13321-025-00969-7

HTTP:
  200

title:
  Predictive modeling of biodegradation pathways using transformer architectures

journal:
  Journal of Cheminformatics

published:
  2025-02-17

volume / article:
  17 / 21

DOI:
  10.1186/s13321-025-00969-7

software reference:
  EnviFormer v1.0.1
  Zenodo 10.5281/zenodo.13858575
```

结果：`PAPER_IDENTITY = PASS`。该检查不等于工具安装或项目 benchmark 通过。

## 4. “模型未见数据”口径

对象没有笼统承诺“找新文献就一定未见”，而是按每个工具独立分类：

```text
CONFIRMED_UNSEEN
LIKELY_UNSEEN
EXPOSURE_UNKNOWN
```

只有 `CONFIRMED_UNSEEN` 可无保留地称为未见数据。现有 6 例已经解锁，只能用于回归和
兼容性测试，不得再次称作新 blind set。

结果：`LEAKAGE_AND_EXPOSURE_DISCLOSURE = PASS`。

## 5. EnzymeCAGE 接口边界

对象明确：

- product-only 能否用于 EnzymeCAGE 仍需 FULL_FORMAL vs MAJOR_PAIR 消融支持；
- 三工具必须统一报告 RDKit、Top-K、失败模式、版本和 provenance；
- 自报 confidence 未校准时不可跨工具比较；
- production `reaction_prediction_node` 未授权修改；
- A 未失败前不自动启动 C 资产建设。

结果：`DOWNSTREAM_COMPATIBILITY_BOUNDARY = PASS`。

## 6. 最终判断

该决定记录可以作为下一阶段 A-first 三工具比较的生物学策略输入。正式 benchmark 仍需
冻结合同、工具身份、测试集和黄老师范围确认，当前不能声称最终工具已选择。

