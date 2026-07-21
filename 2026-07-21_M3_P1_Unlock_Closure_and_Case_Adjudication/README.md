# EnzymeCAGE M3 Frozen Case Configs

Date: 2026-07-21

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M3_CASE_FREEZE_AND_WRAPPER_MODE_ADJUDICATION_2026-07-20(3).md
```

Status: the teacher accepted and froze all three cases. These files implement
teacher action 6.1 only. They do not start M3-P1, alter candidate pools, merge
B and C, run EnzymeCAGE, or add another case.

## Frozen Files

```text
case_1_rhea_40543.json
case_2_rhea_11532.json
case_3_rhea_24292.json
```

Every file contains the teacher-required identity, reaction, route, role,
independent B/C pools, complete known-positive UID list, complete historical
D4 rank map, original student mechanism self-review and fixed A1A/B1/Rhea 140
provenance.

## Three System Roles

```text
Case 1：B-primary + strong pool=1 → pipeline 走通验证 + 污水占位（非排序验证）
Case 2：B-primary + medium 3/8 recall → EnzymeCAGE 排序能力测量（唯一）
Case 3：B 空 → C-fallback → pool ∩ positive = 0 → fail-closed 分支验证

组合覆盖 M3 三种系统行为：B 走通 / B 走通 / B 空 → C → fail-closed。
组合不覆盖 "EnzymeCAGE 效果全景评估"——后者不在 M3 契约范围内。
```

The combination covers three M3 system behaviors: B-primary pipeline passage,
B-primary ranking, and B-empty to C-fallback to fail-closed. It does not cover
a comprehensive EnzymeCAGE performance evaluation, which is outside M3.

## Frozen Pool Summary

| Case | Role | B pool / recalled | C pool / recalled | Runtime decision |
|---|---|---:|---:|---|
| 1 | pipeline + wastewater placeholder | 1 / 1 | 5 / 1 | use B; call wrapper |
| 2 | ranking measurement | 10 / 3 | 17 / 3 | use B; call wrapper |
| 3 | upstream recall failure | 0 / 0 | 79 / 0 | inspect C, then fail closed before wrapper |

All B and C pools independently satisfy the teacher's `<=100` gate. The known
positive UIDs are evaluation-only evidence and were not used to choose the
route or alter pool membership.

## Fixed Boundaries

- M3 uses B-primary and C-fallback. It never uses a B+C union.
- M3 uses only the frozen D4-computable UID domain and does not complete assets.
- Case 1 is only `SUPPORTED_PLAUSIBLE_REQUIRES_REVIEW` for wastewater context;
  it is not established wastewater degradation evidence.
- Case 2 is `NOT_ESTABLISHED` for wastewater context.
- Case 3 has role exactly
  `UPSTREAM_RECALL_FAILURE_FAIL_CLOSED_DEMO`; its historical rank must not be
  used to discuss a model limit because no known positive enters its runtime
  candidate pool.
- Historical D4 ranks are provenance, not results from a new model run.
