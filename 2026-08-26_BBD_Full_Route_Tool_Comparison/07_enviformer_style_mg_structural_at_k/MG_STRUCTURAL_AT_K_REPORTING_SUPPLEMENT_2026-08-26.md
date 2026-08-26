# MG-Structural@K reporting supplement — all-92 inclusive summary

日期：2026-08-26
协议：`ENVIFORMER_MG_STRUCTURAL_AT_K_ADAPTED_BBD_FULL_ROUTE`

---

## 1. 为什么需要这个补充

Codex review 发现：原 `MG_STRUCTURAL_AT_K_TOOL_SUMMARY_2026-08-26.csv` 只在 `SCORED` case 上做 macro/micro 平均，这对有 `NO_PREDICTION` case 的工具偏乐观：

```text
biotransformer_envmicro: 84 SCORED / 8 NO_PREDICTION
envipath_prediction:     87 SCORED / 5 NO_PREDICTION
eclipse_predec:          92 SCORED / 0 NO_PREDICTION
eclipse_noec optional:   92 SCORED / 0 NO_PREDICTION
```

跨工具 teacher-facing 比较需要更严格的汇总：92 个 evaluable case 全入分母，NO_PREDICTION 按 0 分保留。

## 2. 新增文件

- **`MG_STRUCTURAL_AT_K_TOOL_SUMMARY_ALL92_2026-08-26.csv`** — all-92 inclusive macro/micro 主表（推荐 teacher-facing 主表）

## 3. 计算方法

从 `MG_STRUCTURAL_AT_K_CASE_LEVEL_SCORES_2026-08-26.csv` 读取全部 1472 行（92 × 4 tools × 4 K），按 `tool_id × k` 分组：

- all-92 macro = mean(指标 over 全部 92 行，含 NO_PREDICTION 的 0 分行)
- all-92 micro = sum(tp/fp/fn over 全部 92 行) 再算指标

NO_PREDICTION 行已确认全为零分（tp=fp=precision=recall=jaccard=0, fn>0），保留在分母中。

## 4. all-92 macro 结果（与 prompt 期望值交叉验证一致）

| tool | K | all-92 macro P | all-92 macro R | all-92 macro J |
|---|---:|---:|---:|---:|
| biotransformer_envmicro | 1 | 0.329 | 0.242 | **0.197** |
| biotransformer_envmicro | 3 | 0.203 | 0.396 | **0.154** |
| biotransformer_envmicro | 5 | 0.195 | 0.467 | **0.152** |
| biotransformer_envmicro | 10 | 0.191 | 0.474 | 0.149 |
| envipath_prediction | 1 | 0.257 | 0.133 | 0.116 |
| envipath_prediction | 3 | 0.208 | 0.327 | 0.136 |
| envipath_prediction | 5 | 0.197 | 0.384 | 0.140 |
| envipath_prediction | 10 | 0.184 | 0.398 | 0.133 |
| eclipse_predec | 1 | 0.315 | 0.220 | 0.178 |
| eclipse_predec | 3 | 0.122 | 0.510 | 0.106 |
| eclipse_predec | 5 | 0.074 | 0.645 | 0.070 |
| eclipse_predec | 10 | 0.050 | 0.706 | 0.049 |
| eclipse_noec *(optional)* | 1 | 0.278 | 0.188 | 0.155 |
| eclipse_noec *(optional)* | 3 | 0.115 | 0.429 | 0.100 |
| eclipse_noec *(optional)* | 5 | 0.069 | 0.512 | 0.065 |
| eclipse_noec *(optional)* | 10 | 0.051 | 0.548 | 0.049 |

所有值与 prompt §5 期望值精确匹配（3 位小数）。

## 5. 与 scored-only 的差异

以 biotransformer K=1 为例：

- scored-only macro J = 0.216（84 case 平均）
- all-92 macro J = 0.197（92 case 平均，8 个 NO_PREDICTION 按 0 拉低）

差异说明：BioTransformer 有 8 个 NO_PREDICTION case，这些在 scored-only 中被排除（不拉低均值），在 all-92 中按 0 分保留（拉低均值）。ECLIPSE PREDEC 无 NO_PREDICTION，两表数值相同。

## 6. 结论稳定性

all-92 下科学结论不变：
- BioTransformer 在 K=1/3/5 的 Jaccard 仍最高。
- ECLIPSE PREDEC recall 仍最高，precision 仍最低。
- 分支变宽（K↑）recall↑、precision↓ 仍成立。

主结论从"scored-only 偏乐观视角"改为"all-92 公平视角"后更稳健。

## 7. 脚本修复

`scripts/score_mg_structural_at_k.py` 已修复 stale tmp extraction 问题：
- 原：复用 `/tmp/mg_struct_extract`（可能残留旧解压）
- 现：每次运行用 `tempfile.mkdtemp(prefix='mg_struct_extract_')` 全新解压

脚本现同时生成 scored-only 与 all-92 两套汇总。
