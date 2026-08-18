# 仍需老师后续裁定的问题（EnzymeCAGE 侧）

日期：2026-08-18

说明：本文件只列“尚未正式裁定”的事项，避免把建议写成已经批准。

## 0. 2026-08-18 当前仍需老师裁定

| 问题 | 当前只可写成 | 不能写成 |
|---|---|---|
| `P18173` 是否允许后续采用任一 accession candidate 进入收口路径 | 已补充说明：`Q8SXV0` 是按 accession probe order 记录的首个 AFDB v6 200；原始 625aa 与 current canonical / AFDB candidates 不完全一致；保持 unresolved | 已批准使用 `Q8SXV0` 或 `U3PT72` 补资产 |
| `P80550` 38aa legacy source 如何处理 | 已溯源到 frozen 2026-01-21 processed snapshot；与 current canonical 704aa / AFDB `F1RSB4` 不同序；保持 unresolved | 已批准用 `F1RSB4` 替换或补资产 |
| `P49823` / `P54835` 是否授权按 4,681 管线收口 | 老师 08-17 仅列为可收口候选，收口动作需另行授权 | 已授权执行 P2Rank + ESM2 3B + GVP + loader 收口 |

## 1. 2026-08-13/08-14 已推进事项的保留边界

| 问题 | 当前只可写成 | 不能写成 |
|---|---|---|
| M4 第二里程碑 E2 full 4,681 staged status table | 已按 08-14 裁定完成 staged status table；1,704 staged PASS、1,324 P2Rank no-pocket、1,650 AFDB fetch-failed、3 ESM-2 3B failed | production backfill 或 production merge |
| P2Rank no-pocket 约 44% 如何处理 | 当前命令合同下作为明确 blocker 记录，除非老师另行授权 pocket 定义/参数变化 | 静默改 P2Rank 参数、静默换 pocket 定义 |
| 1,650 accession 二次复核 | 08-17 老师已裁定 table-only 结案；candidate 仅记录 | 已允许 UID/accession 自动替换 |
| BBD83 209a4b4 下一步 | status-clean 通过但覆盖低，需扩 donor/reaction evidence、mapper、P4 score 和 blocker 语义 | BBD83 全量科学闭环或 F6 final acceptance |

## 2. 已有老师裁定但仍需执行闭环

| 项 | 老师已裁定 | 当前状态 |
|---|---|---|
| Paraoxon S1 Stage A | 授权只对 `P0A434` / `Q97VT7` 做 D4 构造可行性检查 | 已完成；technical PASS；见 [`../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/`](../2026-08-06_M3_EXT_Paraoxon_S1_StageA_and_S2_Formal_Case/) |
| Paraoxon 案例文件化 S2 | S1 通过后写正式案例草案 | 已完成草案；尚未执行模型评分 |
| Carbaryl | 暂不晋级；Q8GRB9 可保留为 Tier-2 literature-positive | 后续另写证据链补强方案 |
| Route-B pool 规则 | `reviewed-only + release-pinned` | 作为后续 pool 规则边界保留 |
| EC-null agent-assisted discovery | 暂缓 | 等 reaction fallback 引擎选型闭环后再议 |

## 3. 老师尚未正式裁定的问题

| 问题 | 当前只可写成 | 不能写成 |
|---|---|---|
| OnDemand D4 是否通用工具化 | 已有小试证据，可作为 M4 前置讨论 | 老师已批准正式接入智能体 |
| 少量域外 UID 是否可现场补 staged assets 后临时评分 | Paraoxon S1 是特定授权；通用规则待 M4 合同 | 任意域外 UID 都可自动补后评分 |
| 是否做 full-coverage D4 全量补资产/重整理 | 已提出为后续 M4 方案选项 | 已批准全量补资产 |
| M4 是否使用更宽 Rhea/EC 酶域或全量数据重新训练 | 只是待讨论建议 | 已批准全量重训或更换训练域 |
| AutoDock 是否进入默认排序 | 建议仅作为 Top-K 后辅助证据或后续 benchmark | 已替代 EnzymeCAGE 主分数或成为 hard filter |
| Paraoxon 是否进入正式模型运行 | S1/S2 已完成，但模型执行合同尚未冻结 | 已经跑出 Paraoxon EnzymeCAGE 分数或排名 |

## 4. 后续汇报建议口径

```text
本轮已完成老师 08-17 点名的 P18173/P80550 accession 存疑项 record-only 澄清；
两个 UID 仍不进入任何 candidate closure 路径。
P49823/P54835 虽已被老师列为可收口候选，但具体收口动作仍需另行授权。
OnDemand D4 通用工具化、full-coverage D4 资产补齐/重整理，以及 M4 是否采用
更宽 Rhea/EC 酶域或全量重新训练，目前尚未获老师正式裁定。
```
