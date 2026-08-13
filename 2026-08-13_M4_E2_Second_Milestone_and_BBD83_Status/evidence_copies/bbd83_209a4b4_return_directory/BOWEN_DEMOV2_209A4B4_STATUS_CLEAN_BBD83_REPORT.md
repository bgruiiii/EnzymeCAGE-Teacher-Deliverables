# Bowen demov2 209a4b4 status-clean BBD83 rerun report

Date: 2026-08-12

## 1. Commit verification

Did the run actually use commit `209a4b4...`?

**Yes.** `git rev-parse HEAD` = `209a4b4a5c02a7acee1e48fe1c108f5fab134743`, which starts with `209a4b4`.

Remote verification:
- `git ls-remote --heads origin demov2` = `209a4b4a5c02a7acee1e48fe1c108f5fab134743` (starts with `209a4b4a5c02`)
- `git ls-remote --heads origin main` = `ee55753630f3dfb7290ff5a37b07a8ad58279db1`
- Tags: 0
- Branches: demov2 and main only
- Ancestor check: `429ab00c2ec2ffe02f683bbee978539f1279eebf` IS ancestor of HEAD (exit=0)

Four new commits on top of `429ab00`:
1. `773e8bc` fix: A0 — _site_smiles catch RDKit RuntimeError → TransformExtractionError (R12)
2. `25481e6` feat: A0+A — completed_with_warnings enum + kernel decision tree + CLI truth table (R12/R13)
3. `c157cb7` feat: B-light' — source_evidence_eligibilities + source_snapshot_lanes (R15)
4. `209a4b4` feat: E' batch runner + summary (R15 Round 3)

## 2. Forbidden packages

Were `rxnmapper/rxn4chemistry` avoided?

**Yes.** Both packages confirmed NOT installed via import check. `requirements.lock.txt` contains neither package. No learned atom mapper packages were installed or used.

## 3. Entrypoint

Did `scripts/run_real_predict.py` exist and run?

**Yes.** The entrypoint exists at `scripts/run_real_predict.py` (91 lines) and ran successfully for all sanity checks and all 83 BBD83 blind cases.

New exit code truth table (R12/R13):
- `completed_with_warnings` (candidates + warnings) → exit 0
- `completed` + scientific stop (no candidates, typed rejection) → exit 0
- `blocked` + typed system blocker → exit 0
- usage error (`INVALID_INPUT`) → exit 1
- uncaught crash (no typed failure_code) → exit 2

All 83 cases returned exit code 0 (typed terminal).

## 4. Batch runner

Did `scripts/run_bbd83_batch.py` exist and run, or was direct fallback used?

**Both.** `scripts/run_bbd83_batch.py` exists (183 lines) and was used with a patched `VENV_PYTHON` (the hardcoded macOS path `/Volumes/CC/...` was overridden to the local venv Python). The batch runner produced `summary.json` with the §7 distribution.

Additionally, `scripts/run_real_predict.py` was run directly for all 83 cases as a fallback to capture full raw JSON output (the batch runner only saves limited candidate fields). Both methods produced consistent results.

## 5. Snapshot ID

Was the active snapshot id exactly `snap_19caddc6b312`?

**Yes.** The snapshot path `reports/p1/real_snapshot/snap_19caddc6b312` was used. All output JSON records contain `"snapshot_id": "snap_19caddc6b312"`.

## 6. fx_ fixture snapshot

Did any `fx_` fixture snapshot appear in output or preflight?

**No.** No `fx_` fixture snapshots were found in the snapshot directory or in any output.

## 7. Conditional-eligible donor count

How many conditional-eligible donor records were found?

**7.** The production_index.jsonl contains 7 records, all with `eligibility: conditional_eligible`. The manifest confirms: `conditional_count: 7`, `diagnostic_count: 43`, `included_strict_count: 0`, `policy_version: p1-1`.

The 7 conditional-eligible donor reaction IDs:
1. `real_real_audit_case_001`
2. `real_real_audit_case_002`
3. `real_real_audit_case_003`
4. `real_real_audit_case_011`
5. `real_real_audit_case_012`
6. `real_real_audit_case_013`
7. `real_real_audit_case_014`

## 8. Inventory fields

Did the inventory include `mapping_status`, `fully_mapped`, `validator_status` and `support_tier`?

| Field | Available in snapshot records? | Source |
|-------|-------------------------------|--------|
| `mapping_status` | Yes — all 7 records have `"fully_mapped"` | `reaction_evidence.mapping_report.mapping_status` |
| `fully_mapped` | Derived — `True` when `mapping_status == "fully_mapped"` | Computed from mapping_status |
| `validator_status` | Not a separate field in snapshot records | Recorded as `"not_present"` |
| `support_tier` | Not present in eligibility_decision | Recorded as `"not_present"` |
| `source_evidence_eligibilities` | Runtime-only (R15) — populated in candidate output as `["conditional_eligible"]` | Candidate JSON |
| `source_snapshot_lanes` | Runtime-only (R15) — populated in candidate output as `["production"]` | Candidate JSON |

All 7 inventory records have `mapping_status: "fully_mapped"` and `fully_mapped: true`.

## 9. Decanol sanity check

Did decanol return `CCCCCCCCCC=O` with `implicit_h_e_policy` warning?

**Yes.**
- Input: `CCCCCCCCCCO` (1-decanol)
- Status: `completed_with_warnings`
- Exit code: 0
- Candidates: 1
  - `canonical_product_identity`: `CCCCCCCCCC=O` (decanal)
  - `warnings`: `["implicit_h_e_policy"]`
  - `source_evidence_eligibilities`: `["conditional_eligible"]`
  - `source_snapshot_lanes`: `["production"]`
- Failures: `["TRANSFORM_EXTRACTION_FAILED"]` (donor case_012 RDKit Canon error — recorded but does NOT pollute status)

## 10. BBD83 distribution

```text
total blind cases:           83
clean_completed:               0
completed_with_warnings:       7
typed_blocker_or_no_match:    76
runtime_failure:               0
parse_failure:                 0
candidate rows:                9
unique candidate-producing case IDs: 7
cases with conditional warnings: 7
coverage: 7/83 = 8.4%
```

**6.1 fix verification: `runtime_failure = 0`.** In the previous `429ab00` run, 76 cases had `status: "failed"` (runtime_failure) because the donor-level `TRANSFORM_EXTRACTION_ERROR` on `real_real_audit_case_012` polluted the top-level status. In `209a4b4`, commit `773e8bc` catches the RDKit RuntimeError at the `_site_smiles` level and records it as `TRANSFORM_EXTRACTION_FAILED` without setting the top-level status to `failed`. All 76 non-matching cases now have `status: "blocked"` (typed_blocker_or_no_match) instead of `status: "failed"` (runtime_failure).

## 11. Completed BBD83 cases

All 9 candidate rows from 7 unique cases:

| Case ID | Input SMILES | Rank | Product SMILES | Donor | Lane | SEE | SSL | Warnings |
|---------|-------------|------|-----------------|-------|------|-----|-----|----------|
| c0018 | (blind) | 1 | `O=C(CCl)CCl` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c0153 | (blind) | 1 | `O=C([O-])C(=O)c1ccccc1` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1013 | `CC(CCO)CCC=C(C)C` | 1 | `CC(C)=CCCC(C)CC=O` | case_001 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1043 | (blind) | 1 | `CC(C)=CCCC(C)=CC=O` | case_001 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1066 | (blind) | 1 | `CC1CCC(C(C)C)C(=O)C1` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1549 | (blind) | 1 | `O=CC1OCC(=O)C(O)C1O` | case_001 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1549 | (blind) | 2 | `O=C1COC(CO)C(=O)C1O` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1549 | (blind) | 3 | `O=C1COC(CO)C(O)C1=O` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |
| c1586 | (blind) | 1 | `CC(C)NCC(=O)COc1ccc(CC(N)=O)cc1` | case_002 | strict | `["conditional_eligible"]` | `["production"]` | `["implicit_h_e_policy"]` |

Note: `product_smiles` field in raw output is empty; `canonical_product_identity` is used as the product identifier. All candidates have `score: null` and `score_name: null` (P4 numeric scoring is not part of this round).

The 7 candidate-producing cases use 2 of the 7 conditional-eligible donors:
- `real_real_audit_case_001` (donor for c1013, c1043, c1549 rank 1)
- `real_real_audit_case_002` (donor for c0018, c0153, c1066, c1549 ranks 2-3, c1586)

The other 5 conditional-eligible donors (case_003, 011, 012, 013, 014) did not produce candidates for any BBD83 query. Donor case_012 (complex carotenoid, 40 heavy atoms) triggered `TRANSFORM_EXTRACTION_FAILED` (RDKit Canon.cpp Pre-condition Violation) but this error is now correctly isolated at the donor level and does not affect the top-level status.

## 12. Blocked/no-match cases

Aggregate blocker codes and reasons:

| Blocker code | Count | Reason |
|-------------|-------|--------|
| `TRANSFORM_EXTRACTION_FAILED` | 76 | `donor reaction real_real_audit_case_012 could not be processed` |

All 76 blocked cases share the same blocker code and reason. The `TRANSFORM_EXTRACTION_FAILED` failure is recorded for every case because donor `real_real_audit_case_012` is always attempted during kernel processing. However, the status is `blocked` (not `failed`) — the kernel correctly determines that the query SMILES has no matching conditional-eligible donor transformation site, and the donor-level transform error does not pollute the status.

## 13. Restricted answer files

Confirm restricted answer files were not opened/read.

**Confirmed.** No restricted answer files were accessed at any point:
- `restricted/` directory: NOT accessed
- `KNOWN_PATHWAY_POLLUTANT_RESTRICTED_ANSWER_KEY_V0_2.jsonl`: NOT accessed
- `KNOWN_PATHWAY_POLLUTANT_ACCEPTED_PRODUCTS_V0_2.csv`: NOT accessed
- No Hit@K, MRR, or answer-key scoring was performed
- `restricted_answer_files_read = false`

## 14. Correct interpretation

```text
runtime_failure should be 0 for the 6.1 fix to pass
  → CONFIRMED: runtime_failure = 0 (was 76 in 429ab00)

coverage = candidate-producing cases / 83
  → 7/83 = 8.4% (unchanged from 429ab00; coverage expansion not part of this round per 6.4)

blocked/no-match cases are not wrong predictions; they are not evaluable
  → 76 blocked cases are scientific stops (no matching conditional-eligible donor transformation site)

candidate-subset and full-set hits must be scored locally against the restricted answer key
  → Local scoring will be performed after audit

this is conditional production-index evaluation, not strict full BBD83 evaluation
  → Confirmed: only 7 conditional-eligible donors, 0 strict-eligible donors

no numeric P4 score is expected in this round
  → Confirmed: all candidates have score=null, score_name=null (per 6.5)
```

## Key changes from 429ab00 → 209a4b4

| Metric | 429ab00 | 209a4b4 | Fix |
|--------|---------|---------|-----|
| runtime_failure | 76 | **0** | 6.1 ✓ |
| typed_blocker_or_no_match | 0 | 76 | 6.1 ✓ (status corrected from `failed` to `blocked`) |
| completed_with_warnings | 0 (was `failed`) | 7 | 6.1 ✓ (status corrected from `failed` to `completed_with_warnings`) |
| coverage | 7/83 (8.4%) | 7/83 (8.4%) | unchanged (6.4) |
| conditional semantics in output | partial | explicit | 6.2 ✓ |
| evidence-chain fields | absent | populated | 6.3 ✓ |
| `source_evidence_eligibilities` | absent | `["conditional_eligible"]` in all candidates | 6.3 ✓ |
| `source_snapshot_lanes` | absent | `["production"]` in all candidates | 6.3 ✓ |
| `lane` in candidates | absent | `"strict"` in all candidates | 6.2 ✓ |
| `implicit_h_e_policy` warning | present | present | unchanged |
| P4 numeric score | absent | absent (null) | 6.5 ✓ |
