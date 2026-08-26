# Local audit — BBD known-pathway full-route v0.3 v3.1 strict-blind fix

Date: 2026-08-21  
Audited package:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_1_strict_blind_fix_20260821
```

Archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_1_strict_blind_fix_20260821.tar.gz
```

## 1. Verdict

The v3.1 strict-blind fix passes local audit.

Recommended status:

```text
STRICT_BLIND_PASS_READY_FOR_CHENYU_TOOL_RUN
```

This package is intentionally compact. It does not duplicate restricted answers. It provides the corrected outward-facing strict blind input plus a pointer to the v3 restricted answer directory for local scoring.

## 2. Integrity

Manifest check:

```text
sha256sum -c MANIFEST.sha256
```

Result: all listed files passed.

Archive identity:

```text
archive_sha256=ea9bf0497592f686013c789d42259260c2c69ba00d8a073435d6408cf2e02d90
archive_bytes=14061
rdkit_version=2026.03.5
network_used=false
restricted_answer_key_created=false
blind_csv_created=true
final_status=VALIDATION_PASS_READY_FOR_CODEX_AUDIT
```

## 3. Strict blind audit

File:

```text
blind/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_1_BLIND_PARENT_INPUTS_FOR_PREDICTION_STRICT.csv
```

Rows:

```text
93
```

Columns:

```text
full_route_case_id
scope
pollutant_name
pollutant_category
parent_smiles
parent_canonical_smiles
input_note
```

Independent RDKit audit:

```text
parent_smiles RDKit-invalid = 0
parent_canonical_smiles mismatch = 0
```

Comparison to previous v3 strict blind:

```text
previous rows = 93
new rows = 93
missing case IDs = 0
parent_smiles_changed = 0
parent_canonical_smiles_changed = 50
parent_canonical_smiles_unchanged = 43
```

Diff table:

```text
curation/STRICT_BLIND_V3_TO_V3_1_DIFF.csv
rows = 93
changed=true = 50
changed=false = 43
rdkit_check_status=pass = 93
```

The previous bad strict blind was preserved:

```text
blind/BBD_KNOWN_PATHWAY_FULL_ROUTE_V0_3_V3_BLIND_PARENT_INPUTS_FOR_PREDICTION_STRICT_PREVIOUS_BAD.csv
```

## 4. Restricted answer handling

This v3.1 package does not contain restricted answers, which is correct for an outward-facing strict-blind fix.

Pointer file:

```text
restricted_pointer.txt
```

points local scoring to:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/21_BBD_Known_Pathway_Full_Route_Testset_2026-08-21/bbd_known_pathway_full_route_v0_3_candidate_v3_repair_20260821/restricted
```

Do not send the restricted answer directory to chenyu / Gong-shixiong.

## 5. Chenyu run scope note

The package includes:

```text
docs/CHENYU_TOOL_RUN_SCOPE_NOTE_2026-08-21.md
```

It correctly states:

```text
1. This strict blind CSV is the only outward input.
2. Do not provide restricted answer keys to chenyu.
3. First run BioTransformer ENVMICRO, enviPath prediction/lookup as appropriate, and ECLIPSE current best route.
4. Keep raw outputs and normalized product candidates.
5. Return packages must be under /root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries.
6. Scoring returns to local side.
```

## 6. Remaining scientific caveats inherited from v3

The strict blind is now clean, but the benchmark itself remains a candidate full-route benchmark with known route-confidence tiers:

```text
pathway_text_fallback edges = 522
high_confidence_reaction_page_verified edges = 184
legacy_v0_2_reaction_page_not_pathway_listed edges = 4
manual_review rows = 54
```

These are not blockers for sending blind inputs to chenyu, but final scoring/reporting must stratify by confidence tier and must not claim teacher/final benchmark acceptance before review.

## 7. Final conclusion

v3.1 fixes the v3 outward-facing blocker:

```text
strict blind parent canonical mismatch: 50 / 93 -> 0 / 93
```

The strict blind can now be used as the chenyu input for BioTransformer / enviPath / ECLIPSE tool runs, while restricted scoring remains local.

