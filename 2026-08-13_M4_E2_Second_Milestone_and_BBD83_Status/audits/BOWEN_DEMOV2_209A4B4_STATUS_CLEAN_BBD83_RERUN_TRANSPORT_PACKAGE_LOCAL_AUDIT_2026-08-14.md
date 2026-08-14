# Bowen demov2 209a4b4 status-clean BBD83 transport package local audit

Date: 2026-08-14

## Audited artifacts

Local returned-result artifacts:

```text
03_HPC_Returned_Result_Summaries/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz
bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz.identity.txt
```

This audit only closes the previously missing Chenyu transport sidecar for the
2026-08-12 `bowen_demov2_209a4b4_status_clean_bbd83_rerun` result. It does not
change the scientific coverage verdict from the earlier 2026-08-12 / 2026-08-13
local audits.

## Local verdict

```text
FORMAL_TRANSPORT_PACKAGE: PASS_WITH_MANIFEST_SELF_HASH_CAVEAT
ARCHIVE_IDENTITY_MATCH: PASS
ARCHIVE_ROOT_MATCH: PASS
ARCHIVE_BODY_MATCHES_EXISTING_RETURN_DIRECTORY: PASS
STATUS_CLEAN_VERDICT_UNCHANGED: PASS
FINAL_SCIENTIFIC_BBD83_CLOSURE: NOT_CLAIMED
```

Plain-language conclusion:

```text
The missing `.tar.gz` and `.tar.gz.identity.txt` sidecar files have now been
returned locally. The archive SHA256 matches the identity sidecar, extracts to
the expected single root directory, and is byte-identical to the existing local
returned directory. The only remaining package caveat is the known
MANIFEST.sha256 self-hash convention, already recorded in the 2026-08-12 audit.
```

## Identity check

Identity sidecar reports:

```text
archive=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz
archive_sha256=6f8276fe1bcfdbca5cd7d1b1cffa2a8c70a16d66c8fa08bb167395ab82fc95b2
archive_bytes=96158
identity_file=/root/projects/EnzymeCAGE-master/HPC_Returned_Result_Summaries/bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812.tar.gz.identity.txt
single_root=bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812
manifest_sha256=dadded3417b98078b83e1c63e7210e68c49675f11f3633a18b5165c64fc38ad2
manifest_file_count=195
final_status=BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_COMPLETE
repo_commit=209a4b4a5c02a7acee1e48fe1c108f5fab134743
snapshot_id=snap_19caddc6b312
blind_input_sha256=6f811d4b40cfa8ee8c82af40178d85c6770959698e29e6ae202bc7cda21c769a
restricted_answer_files_read=false
```

Local SHA256 recomputation:

```text
6f8276fe1bcfdbca5cd7d1b1cffa2a8c70a16d66c8fa08bb167395ab82fc95b2
```

This matches the identity sidecar.

## Archive body check

Archive extraction checks:

```text
single root: bowen_demov2_209a4b4_status_clean_bbd83_rerun_20260812/
FINAL_STATUS.txt: BOWEN_DEMOV2_209A4B4_STATUS_CLEAN_BBD83_COMPLETE
MANIFEST.sha256 lines: 195
file count under extracted root: 195
normalized JSONL rows: 85
case summary CSV rows: 86 including header
raw BBD83 result JSON files: 83
```

Comparison against the already-audited local returned directory:

```text
diff -qr existing_return_directory extracted_archive_root
```

Result: no differences were reported.

## MANIFEST.sha256 caveat

Raw manifest verification still reports one failing entry:

```text
./MANIFEST.sha256: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
```

This is the same self-hash issue recorded in the 2026-08-12 return audit:
`MANIFEST.sha256` contains an entry for itself, so its digest changes after the
entry is written. Because the archive body is byte-identical to the previously
audited returned directory, this remains a packaging-convention caveat and is
not treated as evidence of result-body drift.

## Status-clean facts retained from the returned body

Local recomputation from the normalized JSONL:

```text
normalized rows: 85
unique case_id values: 83
status=blocked rows: 76
status=completed_with_warnings rows: 9
score null rows: 85
score_name null rows: 85
```

The earlier scientific boundary remains unchanged:

```text
candidate-producing cases: 7/83
strict Hit@10: 1/83
loose non-isomeric Hit@10: 3/83
P4 numeric score fields: null
```

## Teacher-facing wording boundary

Allowed wording:

```text
The previously missing formal Chenyu transport sidecar for the 2026-08-12
`bowen_demov2_209a4b4_status_clean_bbd83_rerun` result has been recovered and
locally audited. Archive SHA256 matches identity, the archive extracts to the
expected single root, and the extracted body matches the existing local return
directory.
```

Required caveat:

```text
This does not convert the 209a4b4 result into BBD83 full scientific closure.
It remains status-clean only: runtime failure pollution was fixed, but
candidate coverage remains low, score fields remain null, and final F6 /
reaction-predictor acceptance is not claimed.
```

