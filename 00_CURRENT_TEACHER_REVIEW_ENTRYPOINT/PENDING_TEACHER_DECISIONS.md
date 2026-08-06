# 仍需老师后续裁定的问题（EnzymeCAGE 侧）

日期：2026-08-06  
说明：本文件只列“尚未正式裁定”的事项，避免把建议写成已经批准。

## 1. 已有老师裁定但仍需执行闭环

| 项 | 老师已裁定 | 当前状态 |
|---|---|---|
| Paraoxon S1 Stage A | 授权只对 `P0A434` / `Q97VT7` 做 D4 构造可行性检查 | 已完成；technical PASS；见 [`../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/`](../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/) |
| Paraoxon 案例文件化 S2 | S1 通过后写正式案例草案 | 已完成草案；尚未执行模型评分 |
| Carbaryl | 暂不晋级；Q8GRB9 可保留为 Tier-2 literature-positive | 后续另写证据链补强方案 |
| Route-B pool 规则 | `reviewed-only + release-pinned` | 作为后续 pool 规则边界保留 |
| EC-null agent-assisted discovery | 暂缓 | 等 reaction fallback 引擎选型闭环后再议 |

## 2. 老师尚未正式裁定的问题

| 问题 | 当前只可写成 | 不能写成 |
|---|---|---|
| OnDemand D4 是否通用工具化 | 已有小试证据，可作为 M4 前置讨论 | 老师已批准正式接入智能体 |
| 少量域外 UID 是否可现场补 staged assets 后临时评分 | Paraoxon S1 是特定授权；通用规则待 M4 合同 | 任意域外 UID 都可自动补后评分 |
| 是否做 full-coverage D4 全量补资产/重整理 | 已提出为后续 M4 方案选项 | 已批准全量补资产 |
| M4 是否使用更宽 Rhea/EC 酶域或全量数据重新训练 | 只是待讨论建议 | 已批准全量重训或更换训练域 |
| AutoDock 是否进入默认排序 | 建议仅作为 Top-K 后辅助证据或后续 benchmark | 已替代 EnzymeCAGE 主分数或成为 hard filter |
| Paraoxon 是否进入正式模型运行 | S1/S2 已完成，但模型执行合同尚未冻结 | 已经跑出 Paraoxon EnzymeCAGE 分数或排名 |

## 3. 后续汇报建议口径

```text
本轮已完成老师授权的 Paraoxon S1 staged feasibility，并完成 S2 formal case draft。
OnDemand D4 通用工具化、full-coverage D4 资产补齐/重整理，以及 M4 是否采用更宽 Rhea/EC 酶域或全量重新训练，目前尚未获老师正式裁定。
Paraoxon 后续如需正式模型评分，应另行冻结 C pool / prediction fallback execution contract。
```
