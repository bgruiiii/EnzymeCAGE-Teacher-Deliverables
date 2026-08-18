# M4 E2 accession ambiguity clarification: P18173 / P80550

Date: 2026-08-18

Authority: teacher 2026-08-17 ruling, section "学生下一步" item 2.

## What this package answers

This is a record-only clarification package for the two uncertain candidate rows from the 1,650 fetch-failed accession secondary review:

- `P18173`: why prior table selected `Q8SXV0` rather than `U3PT72`, and whether either candidate is sequence-consistent with the original 625aa sequence.
- `P80550`: where the original 38aa sequence came from.

## Main files

| File | Purpose |
|---|---|
| [`reports/P18173_P80550_ACCESSION_CLARIFICATION_REPORT.md`](reports/P18173_P80550_ACCESSION_CLARIFICATION_REPORT.md) | Teacher-facing explanation. |
| [`tables/ACCESSION_AMBIGUITY_CLARIFICATION_TABLE.csv`](tables/ACCESSION_AMBIGUITY_CLARIFICATION_TABLE.csv) | Two-row machine-readable clarification table. |
| [`reports/NO_MUTATION_CHECK.json`](reports/NO_MUTATION_CHECK.json) | Confirms no UID replacement, no asset generation and no formal/production mutation. |
| [`audits/ACCESSION_AMBIGUITY_CLARIFICATION_P18173_P80550_TABLE_ONLY_LOCAL_AUDIT_2026-08-18.md`](audits/ACCESSION_AMBIGUITY_CLARIFICATION_P18173_P80550_TABLE_ONLY_LOCAL_AUDIT_2026-08-18.md) | Local audit. |
| [`reports/FINAL_STATUS.txt`](reports/FINAL_STATUS.txt) | Final status statement. |
| [`MANIFEST.sha256`](MANIFEST.sha256) | GitHub package hash manifest. |

## Core result

```text
P18173:
  Q8SXV0 was selected because the 1,650 review probed primary accession first,
  then UniProt secondary accessions in returned order, and recorded the first
  AFDB v6 HTTP 200 candidate.
  This is a deterministic table rule, not a biological preference.
  Original 625aa is not sequence-identical to current UniProt canonical 612aa
  or either AFDB candidate structure sequence.

P80550:
  The 38aa sequence is already present in the frozen 2026-01-21 processed
  Rhea/UniProt enzyme snapshot and downstream backfill manifests.
  It is not introduced by the accession review script.
  Current UniProt P80550 canonical is 704aa, and AFDB F1RSB4 is not
  sequence-identical to the original 38aa source sequence.
```

## Boundary

This package keeps both teacher-flagged cases unresolved:

```text
replacement_performed=false
asset_generation_started=false
formal_assets_mutated=false
production_pool_mutated=false
production_d4_mutated=false
candidate_closure_started=false
```

No candidate-based closure is claimed for `P18173` or `P80550`.
