# Local audit: M4 Phase 1 acceptance teacher submission package

Date: 2026-08-11

Audited submission directory:

```text
01_Path_Contract_Objective/
M4_Phase1_Acceptance_Execution_2026-08-11/
M4_Phase1_Acceptance_Teacher_Submission_2026-08-11/
```

Authority:

```text
00_Authority_Teacher_Plan/
TEACHER_REPLY_M4_PHASE1_CONDITIONAL_APPROVAL_2026-08-11.md
```

## 1. Verdict

Verdict:

```text
LOCAL_AUDIT_PASS_TEACHER_SUBMISSION_PACKAGE_READY_FOR_USER_REVIEW_BEFORE_UPLOAD
```

The folder is organized as a teacher-facing Phase 1 acceptance candidate
submission package. It includes:

```text
main teacher-facing result summary;
file index and README;
corrected Chenyu return archive and external identity;
final return local audit;
F3 reproduction audit;
UID freeze audit;
P2Rank isolated tool directory audit;
corrective rerun prompt and prompt audit;
folder-level SHA256 manifest.
```

This audit does not upload the package and does not claim teacher approval.

## 2. Required teacher-condition coverage

Teacher condition / requirement coverage:

| Requirement | Evidence in package | Result |
|---|---|---|
| F3 numeric reproduction path included | final return archive includes F3 path; F3 local audit copied | PASS |
| F3 rerun on Chenyu | summary and final audit report `f3_reproduction_pass=true` | PASS |
| frozen >=100 UID subset | 100 UID freeze audit copied; summary reports 100 unique UID | PASS |
| 35/25/40 strata | UID freeze audit and summary both report expected strata | PASS |
| AFDB-only + P2Rank predicted-pocket route | return archive and final audit copied | PASS |
| staged outputs only | summary and final audit report staged-only assets | PASS |
| formal/production mutation false | identity, summary, final audit copied | PASS |
| P2Rank version/SHA/command | P2Rank audit and final identity copied | PASS |
| honest blocker counts | summary reports 41 PASS / 44 P2Rank no-pocket / 15 AFDB fetch failed / 0 parse failed | PASS |
| no full 4,681 backfill claim | summary/README state not full backfill | PASS |
| no production merge claim | summary/README state no production merge | PASS |

P2Rank commit caveat:

```text
The package does not overclaim local git proof for commit 255a05e. It states
that release tarball identity is proven by SHA256/version/command contract, and
that the official commit field is retained as an expected identity field
because the release tarball has no .git metadata.
```

## 3. File coverage

Top-level package files:

```text
README.md
M4_PHASE1_ACCEPTANCE_RESULT_SUMMARY_TO_HUANG_2026-08-11.md
EVIDENCE_FILE_INDEX_2026-08-11.md
MANIFEST.sha256
```

Evidence copies:

```text
HPC_ENZYMECAGE_M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_CLEAN_100UID_RERUN_EXECUTOR_ONLY_PROMPT_2026-08-11.md
M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_CLEAN_100UID_RERUN_PROMPT_LOCAL_AUDIT_2026-08-11.md
M4_PHASE1_ACCEPTANCE_CIF_PARSER_FIX_RERUN_RETURN_LOCAL_AUDIT_2026-08-11.md
M4_PHASE1_ACCEPTANCE_TEACHER_SUBMISSION_PACKAGE_LOCAL_AUDIT_2026-08-11.md
M4_PHASE1_ACCEPTANCE_UID_FREEZE_LOCAL_AUDIT_2026-08-11.md
M4_PHASE1_F3_NUMERIC_REPRODUCTION_PATH_LOCAL_AUDIT_2026-08-11.md
M4_PHASE1_P2RANK_ISOLATED_TOOL_DIR_ESTABLISHMENT_RETURN_LOCAL_AUDIT_2026-08-11.md
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz
enzymecage_m4_phase1_acceptance_100uid_afdb_p2rank_cif_parser_fix_rerun1_20260811.tar.gz.identity.txt
```

Archive identity copied into the package:

```text
archive_sha256=4dcbfb5387812c284dd00aade46ec3fb1a5c923ab8e751376a423ada7d8d1afa
archive_bytes=24334733
n_input_uids=100
n_unique_input_uids=100
n_pass_afdb_p2rank_predicted_pocket_d4_loader=41
n_blocked_total=59
n_afdb_structure_parse_failed=0
n_p2rank_no_pocket=44
n_esm2_3b_cache_hit=41
n_esm2_3b_cache_miss=0
formal_assets_mutated=false
production_pool_mutated=false
```

The copied archive SHA256 matches the original archive in
`03_HPC_Returned_Result_Summaries/`.

## 4. Manifest and wording checks

Folder manifest check:

```text
sha256sum -c MANIFEST.sha256: all listed files OK
```

Wording checks:

```text
No claim that teacher has approved/passed this package.
No claim that full 4,681 UID backfill is done.
No claim that production D4/pool was written.
No claim that P2Rank no-pocket means download failure.
No strict AlphaFill full-loader success label used in the teacher-facing text.
```

Expected residual matches from text scan:

```text
The phrase "teacher-approved stratum" appears only inside copied UID-freeze
audit evidence, where it refers to the teacher-authorized sampling strata from
the M4 conditional approval, not approval of this returned package.
```

## 5. Final local interpretation

The submission folder is ready for user review before upload. The next step
should be:

```text
Confirm target upload location and remote directory convention;
upload the submission folder exactly as organized;
verify remote file list and SHA256 after upload;
then send the short message draft to Huang with the uploaded path.
```
