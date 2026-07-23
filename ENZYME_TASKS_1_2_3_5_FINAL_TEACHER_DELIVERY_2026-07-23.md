# 酶侧 Tasks 1、2、3、5 最终交付与裁定请求

日期：2026-07-23

状态：`SUBMITTED_FOR_TEACHER_REVIEW_NOT_YET_TEACHER_ACCEPTED`

权威依据：

```text
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md
SHA256 57699b8a92ba6b555c96c0216c3961af0e80299d150b21979cb4fa7a19a18d57
```

Case 1 的 RHEA:11880 公平检索边界另按 2026-07-22 老师澄清执行。

## 1. 老师从哪里开始看

本次将老师当前要求的主要文件直接放在仓库根目录，避免文件已存在但
未在主入口显式列出：

| 老师任务 | 根目录交付文件 | 当前状态 |
|---|---|---|
| Task 1：重发新 Case 1 JSON | `case_1_rhea_46976.json` | 本地审计通过，提交老师复核 |
| Task 2：三案例首页统一措辞 | `THREE_CASE_HOMEPAGE.md` | 本地审计通过，提交老师复核 |
| Task 3：旧 Case 1 弃用登记 | `M3_CASE_REGISTRY.json`、`case_1_rhea_40543.json` | 本地审计通过，旧文件未删除 |
| Task 5：M3-EXT 候选清单 | `M3_EXT_CANDIDATE_SHORTLIST_v0.md` | 候选筛选完成，等待老师二次裁定 |

`case_2_rhea_11532.json` 和 `case_3_rhea_24292.json` 也放在根目录，
使 `M3_CASE_REGISTRY.json` 的相对文件引用完整且可独立核验。

逐任务审计及提交前总审计位于：

```text
2026-07-23_Enzyme_Tasks_1_2_3_5_Submission/audits/
```

## 2. Task 1：RHEA:46976 Case 1

机器可读文件：`case_1_rhea_46976.json`

重新核验后的核心状态：

```text
rhea_master_id = 46976
ec = null
route = C-fallback
B pool / recalled = 0 / 0
C pool / recalled = 15 / 2
known positives = Q93NH4, A0A075BSX9
```

两个 known-positive UID 都有独立的 reviewed UniProt RHEA:46976
直接催化反应记录和实验文献证据，因此不是从 RHEA:11880 自动继承
known-positive 身份。

RHEA:11880 在公平 Top-K 相似检索中自然命中时允许像其他邻居一样
贡献候选，不得人为剔除；但它不替代 RHEA:46976 查询身份，不向
RHEA:46976 继承 EC 1.5.3.5，也不作为 known-positive 身份证据。

## 3. Task 2：三案例首页统一措辞

首页文件：`THREE_CASE_HOMEPAGE.md`

其中包含老师要求的三行原文：

```text
Case 1 (RHEA:46976, 尼古丁降解): C-fallback 成功分支演示
Case 2 (RHEA:11532, EC 1.4.3.19): B-primary 排序统计意义
Case 3 (RHEA:24292, EC 2.3.1.1): 上游召回失败 fail-closed
```

活动案例仍严格为三个，没有新增第四案例。

## 4. Task 3：旧 Case 1 弃用留痕

`M3_CASE_REGISTRY.json` 对旧 RHEA:40543 的记录为：

```text
deprecated = true
reason = business_direction_mismatch
superseded_by = RHEA:46976
evidence_retention = RETAIN_DO_NOT_DELETE
```

旧文件 `case_1_rhea_40543.json` 保留且哈希与 registry 一致，不是
第四个活动案例。

## 5. Task 5：M3-EXT 候选筛选及建议

候选清单：`M3_EXT_CANDIDATE_SHORTLIST_v0.md`

本轮保留两个候选：

| 优先级 | 候选 | Rhea EC 状态 | 初步 B/C |
|---:|---|---|---:|
| 1 | Paraoxon hydrolysis，RHEA:18053 | Rhea 140 EC 3.1.8.1 | 0 / 13 |
| 2 | Carbaryl hydrolysis，RHEA:62380 | `rhea_ec=null`；外部候选 EC 3.5.1.137 | 0 / 72 |

已排除 Nitrobenzene RHEA:46508：虽然精确反应和证据 UID 没有命中
正式切分，但 nitrobenzene 分子本身出现在 52 条训练行中，不满足
老师要求的 molecule 排除门。

清单中已经写入以下建议，供老师裁定：

1. Paraoxon 作为第一优先候选。
2. 若老师授权，可先对 P0A434、Q97VT7 做仅限 D4 可构建性的 Stage A
   验证；不得改正式池、报告召回或调用模型。
3. 真正测试前，由老师选择并冻结 reviewed-only 或全部 accession
   等客观全池规则，再完成完整池 D4 和公平 Route B 重建；不能只补
   known positives。
4. Carbaryl 保留 `rhea_ec=null`，外部 EC 3.5.1.137 只作为带来源的
   `external_ec_candidate`，不得覆写冻结 Rhea 140。
5. 对 EC-null 反应，可试验由联网智能体按 IUBMB/ExPASy、Rhea、
   BRENDA、UniProt 和原始论文的证据层级辅助搜证；不同模型的可靠性
   当前未知，必须保留可复现来源、冲突/未解决终态和人工裁定。

## 6. 请老师裁定的 Task 5 问题

1. Paraoxon 和/或 Carbaryl 是否晋级官方挑战案例冻结流程？
2. 是否先授权两个 Paraoxon 直接证据 UID 的 Stage-A D4 可构建性
   检查，并保持“不改池、不报召回、不跑模型”？
3. 若 Carbaryl 晋级，是否接受保留 `rhea_ec=null` 的外部 EC 候选
   桥接；Q8GRB9 是否可保持为缺少官方 UID-level EC 的文献正例？
4. 后续完整候选池采用 reviewed-only、全部 accession，还是老师
   指定的其他可复现规则？
5. 是否确认完整池、D4 和重建 Route B 通过独立审计前不调用模型？
6. 是否授权 EC-null 联网智能体搜证小试；采用单智能体复现还是不同
   智能体/基础模型的受控对比？

## 7. 明确未做

本次没有补 D4 或其他数据资产，没有修改冻结 Rhea 140、Route B 或
Route C，没有改变当前三个案例，没有调用 EnzymeCAGE wrapper、
checkpoint、GPU 或晨羽资源，也没有把 Task 5 候选表述为系统已验证
案例。

