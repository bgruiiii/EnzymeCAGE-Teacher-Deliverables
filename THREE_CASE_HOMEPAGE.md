# EnzymeCAGE M3 Frozen Case Configs

Date: 2026-07-21

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_P1_UNLOCK_CASE1_REBOUND_AND_METATRAITS_M4A_ADJUDICATION_2026-07-21.md

00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE1_RHEA11880_FAIRNESS_AND_KNOWN_POSITIVE_EVIDENCE_2026-07-22.md
```

Status: M3-P1 is teacher-side unlocked. The teacher replaced old Case 1
RHEA:40543 with RHEA:46976 on 2026-07-21 and clarified the RHEA:11880
fair-retrieval boundary on 2026-07-22. The replacement config, per-UID direct
known-positive evidence and registry have passed local audits and remain
pending final teacher delivery. No Agent, three-case inference, candidate-pool
mutation or fourth active case is created here.

## Active Files

```text
case_1_rhea_46976.json
case_2_rhea_11532.json
case_3_rhea_24292.json
```

`M3_CASE_REGISTRY.json` is the machine-readable active/deprecated index. The
old `case_1_rhea_40543.json` is retained byte-for-byte as deprecated evidence:

```text
deprecated: true
reason: business_direction_mismatch
superseded_by: RHEA:46976
```

The retained old JSON is not a fourth active case.

## Three System Roles

```text
Case 1 (RHEA:46976, 尼古丁降解): C-fallback 成功分支演示
Case 2 (RHEA:11532, EC 1.4.3.19): B-primary 排序统计意义
Case 3 (RHEA:24292, EC 2.3.1.1): 上游召回失败 fail-closed

组合覆盖 M3 三种系统行为：B 空 → C 成功 / B-primary 排序 / B 空 → C
召回失败 → fail-closed。
组合不覆盖 "EnzymeCAGE 效果全景评估"——后者不在 M3 契约范围内。
```

Every active file contains the teacher-required identity, reaction, route,
role, independent B/C pools, complete known-positive UID list, complete
historical D4 rank map, mechanism self-review and fixed A1A/B1/Rhea 140
provenance.

## Frozen Pool Summary

| Case | Role | B pool / recalled | C pool / recalled | Runtime decision |
|---|---|---:|---:|---|
| 1 | nicotine degradation; C-fallback success | 0 / 0 | 15 / 2 | B empty; use C; call wrapper |
| 2 | ranking measurement | 10 / 3 | 17 / 3 | use B; call wrapper |
| 3 | upstream recall failure | 0 / 0 | 79 / 0 | inspect C, then fail closed before wrapper |

All B and C pools independently satisfy the teacher's `<=100` gate. The known
positive UIDs are evaluation-only evidence and were not used to choose the
route or alter pool membership.

## Fixed Boundaries

- M3 uses B-primary and C-fallback. It never uses a B+C union.
- M3 uses only the frozen D4-computable UID domain and does not complete assets.
- Case 1 has JSON `ec: null`. EC 1.5.3.5 belongs to related overall
  RHEA:11880 and must not be inherited by exact query RHEA:46976.
- Case 1 is `SUPPORTED_PLAUSIBLE_REQUIRES_REVIEW` for wastewater/environment
  context. It is not a wastewater-engineering validation or evidence of
  treatment efficiency, removal, detoxification or mineralization.
- RHEA:11880 may contribute candidate enzymes when it naturally appears in the
  fair Top-K similarity search and must not be manually removed. It cannot
  replace the RHEA:46976 query identity, supply its EC or establish a UID's
  known-positive identity. Both strict Case 1 known positives instead have
  direct reviewed UniProt RHEA:46976 and experimental-literature evidence.
- Case 2 is `NOT_ESTABLISHED` for wastewater context.
- Case 3 has role exactly
  `UPSTREAM_RECALL_FAILURE_FAIL_CLOSED_DEMO`; its historical rank must not be
  used to discuss a model limit because no known positive enters its runtime
  candidate pool.
- Historical D4 ranks are provenance, not results from a new model run.
- Case 1 is part of the formal test set and its historical ranks were already
  inspected; it is a disclosed branch demo, not an unbiased performance test.
