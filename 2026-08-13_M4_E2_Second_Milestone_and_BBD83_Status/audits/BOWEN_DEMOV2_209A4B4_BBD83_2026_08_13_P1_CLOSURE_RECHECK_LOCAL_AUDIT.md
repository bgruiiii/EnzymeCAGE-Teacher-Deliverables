# BBD83 209a4b4 2026-08-13 P1 closure re-check local audit

Date: 2026-08-13

## 1. Authority

Teacher 2026-08-13 guidance lists this Chen Haoran-side P1 item:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_PROJECT_NEXT_STEPS_GUIDANCE_2026-08-13.md

P1: BBD83 blind workflow closure
Required: bowen_demov2_209a4b4_status_clean_bbd83_rerun output from 2026-08-12
should receive local audit + normalized return.
```

This re-check does not own Gong Sai-side later v4.2 reruns. It only checks
whether the existing 2026-08-12 `209a4b4` return satisfies the 2026-08-13 P1
request for the Chen Haoran-side package.

## 2. Re-checked artifacts

Returned result directory:

```text
03_HPC_Returned_Result_Summaries/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
```

Existing local audit:

```text
04_Local_Review_Audits/
BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_RERUN_RETURN_LOCAL_AUDIT_2026-08-12.md
```

Normalized return file:

```text
03_HPC_Returned_Result_Summaries/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
BBD83_BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_NORMALIZED.jsonl
```

Case/run summary:

```text
03_HPC_Returned_Result_Summaries/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
BBD83_BOWEN_DEMOV2_209A4B4_CASE_RUN_SUMMARY.csv
```

## 3. Re-check verdict

```text
P1_RECHECK_PARTIAL_PASS_WITH_TRANSPORT_AND_SCIENTIFIC_COVERAGE_CAVEATS
```

Plain-language conclusion:

```text
The existing 2026-08-12 return satisfies the auditability/status-clean part of
teacher's 2026-08-13 P1 request: the returned directory is present, normalized
JSONL is present, all 83 blind cases have typed terminal status, and the old
runtime-failure pollution is cleared.

It should not be reported as final BBD83 scientific closure or final F6
acceptance. Scientific coverage remains low, numeric score fields are absent,
and the formal Chenyu transport package is incomplete locally because the
matching .tar.gz and .tar.gz.identity.txt are not present.
```

## 4. Evidence checks

Local recomputation from the normalized JSONL:

```text
normalized rows:                         85
unique blind cases:                      83
ranked_prediction rows:                   9
candidate-producing cases:                7
typed_blocker_or_no_match rows:          76
runtime_failure count:                    0
parse_failure count:                      0
candidate rows with score = null:         9
```

Existing 2026-08-12 local audit reports:

```text
STATUS_MACHINE_FIX: PASS
SCIENTIFIC_COVERAGE: STILL_LOW
FORMAL_TRANSPORT_ACCEPTANCE: BLOCKED_BY_MISSING_ARCHIVE_AND_IDENTITY
FINAL_F6_ACCEPTANCE: NOT_CLAIMED
```

Existing final status token:

```text
BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_COMPLETE
```

Scoring facts from the existing local audit:

```text
strict Hit@10:              1/83
loose non-isomeric Hit@10:  3/83
accepted products @10:      strict 1/148, loose 3/148
```

Formal transport check:

```text
returned directory: present
matching top-level .tar.gz beside directory: not found locally
matching .tar.gz.identity.txt beside directory: not found locally
MANIFEST.sha256 body: all listed body files OK except self-hash convention
```

The self-hash issue is treated as a packaging defect, not as evidence that the
returned body files drifted.

## 5. What can be reported to teacher

Allowed wording:

```text
The 2026-08-12 bowen_demov2_209a4b4 status-clean BBD83 return has been re-checked
against the 2026-08-13 P1 request. Local audit and normalized JSONL are present.
The status-machine repair is accepted locally: runtime_failure=0 and all 83
BBD83 parents terminate with typed statuses.
```

Required caveat:

```text
This is not BBD83 final scientific closure. Candidate coverage remains 7/83,
strict Hit@10 remains 1/83, loose non-isomeric Hit@10 remains 3/83, and score
fields are null. The formal Chenyu archive/identity sidecar is still missing
locally, so formal transport acceptance is not claimed.
```

## 6. What should not be claimed

Do not claim:

```text
BBD83 full scientific closure;
F6 final reaction-predictor acceptance;
full 83-case evaluability solved;
P4 ranking solved;
formal Chenyu transport package complete;
teacher acceptance of the BBD83 scientific result.
```

## 7. Follow-up if teacher asks for more

If teacher wants this item made formally transport-complete, ask Chenyu to
provide or regenerate:

```text
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz.identity.txt
```

If teacher wants scientific closure rather than status-clean closure, this is a
Gong Sai/Bowen model-side task: expand donor/reaction evidence, connect the
permitted mapper path, add numeric P4 scores, and improve per-case no-match /
blocker semantics.
