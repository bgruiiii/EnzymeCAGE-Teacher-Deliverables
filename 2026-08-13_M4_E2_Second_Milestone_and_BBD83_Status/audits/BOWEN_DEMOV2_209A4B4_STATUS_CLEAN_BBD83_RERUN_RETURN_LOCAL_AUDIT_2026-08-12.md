# Bowen demov2 209a4b4 status-clean BBD83 rerun return local audit

Date: 2026-08-12

## Audited return

Returned directory:

```text
03_HPC_Returned_Result_Summaries/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
```

Final status token:

```text
BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_COMPLETE
```

This audit is for the Bowen/Gong `demov2` degradation-route prediction track.
It is not a MetaTraits/microbe audit.

## Local verdict

```text
STATUS_MACHINE_FIX: PASS
SCIENTIFIC_COVERAGE: STILL_LOW
FORMAL_TRANSPORT_ACCEPTANCE: BLOCKED_BY_MISSING_ARCHIVE_AND_IDENTITY
FINAL_F6_ACCEPTANCE: NOT_CLAIMED
```

Plain reading: this rerun fixes the previous status pollution problem. It does
not yet solve the full 83-case BBD prediction objective.

## Transport and integrity

Expected formal return artifacts for a Chenyu/HPC return are:

```text
return directory
return .tar.gz
return .tar.gz.identity.txt
```

Local check found only the directory:

```text
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
```

No matching top-level `.tar.gz` or `.tar.gz.identity.txt` was present beside the
directory. Therefore the result can be reviewed as a directory preaudit, but it
is not yet a formally complete transport package.

Manifest check:

```text
file count under returned directory: 195
sha256sum -c MANIFEST.sha256: 194 files OK, MANIFEST.sha256 FAILED
```

The failure is consistent with a self-hash packaging issue: `MANIFEST.sha256`
contains an entry for `./MANIFEST.sha256`, so its own checksum changes when the
entry is written. All other listed files verified OK. Treat this as a packaging
defect, not as evidence that the result body drifted.

## Commit and environment evidence

Returned report states:

```text
HEAD = 209a4b4a5c02a7acee1e48fe1c108f5fab134743
remote demov2 = 209a4b4a5c02a7acee1e48fe1c108f5fab134743
remote main = ee55753630f3dfb7290ff5a37b07a8ad58279db1
tags = 0
branches = demov2 and main only
429ab00c2ec2ffe02f683bbee978539f1279eebf is ancestor of HEAD
working tree = clean
```

Snapshot:

```text
snapshot_id = snap_19caddc6b312
fx_fixture_snapshot_found = false
production_index_record_count = 7
conditional_eligible_count = 7
included_strict_count = 0
```

Forbidden package boundary:

```text
rxnmapper: not installed
rxn4chemistry: not installed
restricted answer files not read on HPC
```

## Status-clean result

HPC-reported distribution and local normalized-file recomputation agree:

```text
total blind cases:                83
normalized rows:                  85
candidate rows:                    9
unique candidate-producing cases:  7
completed_with_warnings cases:     7
typed_blocker_or_no_match cases:  76
runtime_failure:                   0
parse_failure:                     0
coverage:                       7/83 = 8.4%
```

Important nuance: the normalized JSONL has 85 rows because 7 cases produced 9
ranked candidate rows and 76 cases produced blocker rows. The file named
`BBD83_BOWEN_DEMOV2_209A4B4_CASE_RUN_SUMMARY.csv` also has 85 rows, so it is a
result-row summary, not a strict one-row-per-case summary.

The previous `429ab00` run had all 83 raw runs returning exit code 1, including
76 runtime failures caused by donor-level `TRANSFORM_EXTRACTION_ERROR`
polluting top-level status. In this `209a4b4` return:

```text
runtime_failure = 0
all 83 cases have typed terminal status
7 candidate-producing cases are completed_with_warnings
76 non-candidate cases are blocked / typed_blocker_or_no_match
```

Therefore the status-machine fix is locally accepted as working.

## Candidate evidence

Candidate-producing cases:

```text
SPD-BBD2-PARENT-c0018
SPD-BBD2-PARENT-c0153
SPD-BBD2-PARENT-c1013
SPD-BBD2-PARENT-c1043
SPD-BBD2-PARENT-c1066
SPD-BBD2-PARENT-c1549
SPD-BBD2-PARENT-c1586
```

All 9 candidate rows share:

```text
lane = strict
source_evidence_eligibilities = ["conditional_eligible"]
source_snapshot_lanes = ["production"]
warnings = ["implicit_h_e_policy"]
score = null
score_name = null
```

The 7 candidate-producing cases used only 2 of the 7 conditional donors:

```text
real_real_audit_case_001
real_real_audit_case_002
```

The other 5 conditional donors did not produce BBD83 candidates:

```text
real_real_audit_case_003
real_real_audit_case_011
real_real_audit_case_012
real_real_audit_case_013
real_real_audit_case_014
```

## Local restricted scoring

Local scoring used the restricted v0.2 answer key only after the HPC blind run
returned:

```text
03_HPC_Returned_Result_Summaries/
enzymecage_m3_p1_2_1_bbd_known_pathway_benchmark_v0_2_local_build_20260805/
restricted/KNOWN_PATHWAY_POLLUTANT_RESTRICTED_ANSWER_KEY_V0_2.jsonl
```

Strict RDKit-canonicalized product scoring:

```text
Hit@1  = 1/83 = 0.012048
Hit@3  = 1/83 = 0.012048
Hit@5  = 1/83 = 0.012048
Hit@10 = 1/83 = 0.012048
MRR@10 = 0.012048
accepted products recovered @10 = 1/148
hit case = SPD-BBD2-PARENT-c1013, product Citronellal
```

Loose non-isomeric / first InChIKey-block scoring:

```text
Hit@1  = 3/83 = 0.036145
Hit@3  = 3/83 = 0.036145
Hit@5  = 3/83 = 0.036145
Hit@10 = 3/83 = 0.036145
MRR@10 = 0.036145
accepted products recovered @10 = 3/148
hit cases = c1013 Citronellal, c1043 Geranial, c1066 Menthone
```

This is effectively unchanged from the previous low-coverage `429ab00`
candidate set. The scientific result has not caught up with BioTransformer or
enviPath BBD Rules on the exploratory BBD83 benchmark.

## What is still missing

1. Formal return package:

```text
.tar.gz is missing locally
.tar.gz.identity.txt is missing locally
MANIFEST.sha256 self-check fails because it hashes itself
```

Ask Chenyu to provide the missing archive and identity sidecar if they were
generated, or rerun packaging with a manifest that excludes itself or uses a
two-pass manifest convention.

2. Full BBD83 coverage:

```text
current candidate coverage = 7/83 = 8.4%
current production donor evidence = 7 conditional donors
strict eligible donors = 0
```

The limiting factor is not the 83 input list. The run did try all 83 parents.
The model/kernel only had about 7 conditional production donor reactions to
generalize from, and only 2 of those donors actually produced any candidates.
So most BBD83 molecules had no applicable donor transformation in the current
production index.

3. Mapper and evidence expansion:

```text
rxnmapper/rxn4chemistry intentionally not used
learned mapper A1 is not connected
donor/reaction evidence remains too sparse for full BBD83 evaluability
```

For the next Bowen/Gong request, state plainly that the goal is not another
7-case demo. The goal is full 83-case evaluability. To get there, they need to
add enough donor/reaction evidence and mapper capability so most or all BBD83
parents can receive ranked candidate products.

4. P4 numeric score:

```text
score = null for all 9 candidate rows
score_name = null for all 9 candidate rows
```

This is expected for this round, but it remains missing for ranking-comparable
evaluation.

5. Blocker semantics:

```text
76/76 blocker rows report:
blocker_code = TRANSFORM_EXTRACTION_FAILED
blocker_reason = donor reaction real_real_audit_case_012 could not be processed
```

This is better than runtime failure, but still not a useful per-case scientific
explanation. The blocked cases should distinguish "no applicable donor/site"
from "a specific donor transform failed while scanning donors". Donor
`real_real_audit_case_012` should not dominate the blocker reason for every
non-candidate case.

6. Inventory fields:

```text
mapping_status = fully_mapped for all 7 donors
fully_mapped = true for all 7 donors
validator_status = not_present
support_tier = not_present
```

The returned inventory fills `mapping_status` and derived `fully_mapped`, but
`validator_status` and `support_tier` are placeholders rather than real computed
evidence fields.

7. Batch runner portability:

```text
scripts/run_bbd83_batch.py required VENV_PYTHON patch
reason: hardcoded macOS path in runner
```

Chenyu worked around this successfully, but the runner should use
`sys.executable` or a CLI/env override by default.

8. Minor documentation inconsistency:

`ENVIRONMENT_INFO.txt` says:

```text
blocked + typed system blocker (CAPABILITY_UNAVAILABLE) -> exit 1
```

The report says all 83 cases returned exit code 0 typed terminal, including the
76 blocked/no-match cases. This should be clarified in the code/report truth
table so future audits know which blocked statuses are expected to exit 0.

## Recommendation

For Chenyu:

```text
Please provide or regenerate the deterministic .tar.gz and .tar.gz.identity.txt
for bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812. Also fix the
manifest convention so MANIFEST.sha256 does not fail by hashing itself.
```

For Bowen/Gong:

```text
209a4b4 fixed the status-clean problem: runtime_failure is now 0, and the 83
BBD parents all terminate in typed statuses. However, the scientific prediction
coverage remains 7/83 with strict local Hit@10 1/83 and loose Hit@10 3/83.

Next work should target full BBD83 evaluability: expand donor/reaction evidence,
connect the learned mapper A1 or another permitted mapper path, add P4 numeric
scores, produce more informative per-case no-match/blocker reasons, and make
the batch runner portable without hardcoded local paths.
```

Do not present this return as final F6 acceptance. It is a successful
status-layer repair and a valid diagnostic rerun, with scientific coverage and
formal packaging still incomplete.

