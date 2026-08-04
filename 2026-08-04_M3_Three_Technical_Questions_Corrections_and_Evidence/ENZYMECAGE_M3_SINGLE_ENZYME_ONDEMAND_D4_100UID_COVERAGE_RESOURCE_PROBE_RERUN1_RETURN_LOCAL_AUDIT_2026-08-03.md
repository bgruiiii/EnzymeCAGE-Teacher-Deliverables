# Local audit: 100-UID on-demand D4 coverage/resource probe rerun1 payload return

Date: 2026-08-03  
Audited package:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_100uid_alphafill_coverage_resource_probe_rerun1_payload_20260803.tar.gz
```

Identity file:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_single_enzyme_ondemand_d4_100uid_alphafill_coverage_resource_probe_rerun1_payload_20260803.tar.gz.identity.txt
```

## 1. Verdict

Verdict: ACCEPT AS COMPLETE 100-UID TECHNICAL COVERAGE/RESOURCE PROBE, with interpretation caveats.

This package supports:

```text
Under a deterministic stratified 100-UID sample from current strict 2026 missing-pocket/missing-D4 metadata, the strict on-demand AlphaFill-transplant EnzymeCAGE D4 staging route recovered 16 / 100 UIDs to isolated loader eligibility.
```

It does not support:

```text
production asset merge;
biological correctness of any UID for a target reaction;
global unbiased coverage across all enzymes;
claiming sequence absence for timeout rows;
teacher authorization for predicted/whole-protein/fixed-pocket fallback.
```

## 2. Package integrity

Local archive SHA256:

```text
89c83cc29e4b3320b2a27e2f38bece39a297e95e97ad5bae80040c08f309b4ab
```

Identity file reports the same archive SHA256:

```text
archive_sha256=89c83cc29e4b3320b2a27e2f38bece39a297e95e97ad5bae80040c08f309b4ab
```

Final status:

```text
M3_SINGLE_ENZYME_D4_100UID_PROBE_RERUN1_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

Identity summary:

```text
n_sampled=100
n_full_d4_loader_pass=16
payload_archive_sha256=f75b68d7f43cf994f1a3c31a86ab218764f17f2373292aabd480c75c810e61dc
```

Internal `MANIFEST.sha256`:

```text
all listed files: OK
```

## 3. Payload validation

The sampling-source payload was validated:

```text
expected_sha256=f75b68d7f43cf994f1a3c31a86ab218764f17f2373292aabd480c75c810e61dc
actual_sha256=f75b68d7f43cf994f1a3c31a86ab218764f17f2373292aabd480c75c810e61dc
sha256_verified=true
internal MANIFEST.sha256 check=PASS
```

All five source tables existed after payload extraction:

```text
FINAL_MISSING
ALPHAFILL_SUCCESS_NO_POCKET
OLD_POOL_WITH_POCKET
OLD_POOL_WITHOUT_POCKET
EXTERNAL_NEEDED
```

This fixes the previous blocked run's input-table problem.

## 4. Sampling audit

Sampling result:

```text
SAMPLED_UIDS.csv rows: 100
PER_UID_STATUS_TABLE.csv rows: 100
PER_UID_TIMING_RESOURCE_TABLE.csv rows: 100
unique sampled UIDs: 100
sample/status/timing UID sets: identical
excluded controls present: none
```

Excluded controls:

```text
P0A434
Q97VT7
Q8RR61
Q8GRB9
```

Stratified sample counts:

| Stratum | Sampled |
|---|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 35 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 40 |

No allocation deficits or fill-in substitutions were reported.

## 5. Main result counts

Overall final-status distribution:

| Final status | Count | Rate |
|---|---:|---:|
| `PASS_FULL_D4_LOADER` | 16 | 16% |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 43 | 43% |
| `BLOCKED_ALPHAFILL_404` | 20 | 20% |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 17 | 17% |
| `BLOCKED_SEQUENCE_MISSING` | 4 | 4% |

Important correction:

The 4 `BLOCKED_SEQUENCE_MISSING` rows are not confirmed missing sequences. Their per-UID reports show:

```text
URLError(TimeoutError('timed out'))
sequence_fetch_sec ≈ 45.046 sec
```

Therefore they should be described as:

```text
UniProt sequence fetch timeout / unresolved in this run
```

not as true sequence absence.

AlphaFill distribution:

| AlphaFill status | Count |
|---|---:|
| `PASS_ALPHAFILL_HAS_TRANSPLANTS` | 33 |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 43 |
| `BLOCKED_ALPHAFILL_404` | 20 |
| not attempted due to sequence timeout | 4 |

Downstream funnel:

```text
AlphaFill has transplants: 33
pocket extraction attempted: 33
pocket extraction PASS: 16
ESM-2 3B attempted: 16
GVP attempted: 16
loader attempted: 16
full D4 loader PASS: 16
```

## 6. Stratified interpretation

Final status by stratum:

| Stratum | PASS | Main blockers |
|---|---:|---|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 0 / 35 | 23 hits-null, 10 pocket extraction invalid, 2 sequence timeout |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 15 / 25 | 4 hits-null, 4 pocket extraction invalid, 2 AlphaFill 404 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 1 / 40 | 18 AlphaFill 404, 16 hits-null, 3 pocket extraction invalid, 2 sequence timeout |

Interpretation:

```text
The strict on-demand route is technically viable, but rescue success is highly enriched in the old-pool-with-pocket/recheck stratum.
```

This means the route can recover some missing-D4 candidates, especially where historical pocket evidence exists or can be effectively regenerated, but it is not a universal rescue for all AlphaFill-available proteins.

## 7. Full D4 PASS audit

PASS UIDs:

```text
A6S9T6
Q9CFB4
A1KHE9
Q12WF0
Q9SPB1
Q9I7X6
A5U2I9
Q81TU9
Q9SEH4
P12646
A6SAG8
A6RJA2
Q5HNA5
A6US00
Q24816
A0A1E3M8P2
```

For all 16 PASS UIDs, independent local checks found:

```text
LOADER_VALIDATION_REPORT.json/md present
load_geometric_dataset_called=true
dataset_len=1
dataset0_constructed=true
loader_validation_status=PASS
```

Spot-check examples:

| UID | Pocket residues | full-sequence ESM node feature | Loader |
|---|---:|---|---|
| `A6S9T6` | 31 | `[485,2560]` | PASS |
| `Q9CFB4` | 70 | `[316,2560]` | PASS |
| `A1KHE9` | 51 | `[320,2560]` | PASS |
| `A0A1E3M8P2` | 66 | `[288,2560]` | PASS |

Local audit note:

```text
The package contains pocket-node ESM and GVP torch assets for the PASS UIDs, and each PASS UID has an HPC LOADER_VALIDATION_REPORT showing dataset_len=1 and dataset0_constructed=true. The local audit environment did not have torch installed, so it did not directly deserialize the .torch.pt files to independently recheck pocket-node/GVP tensor shapes.
```

The PASS evidence is therefore credible as isolated staged D4 loader eligibility.

## 8. Timing and resource audit

Overall per-UID timing:

```text
mean total wall time: 14.37 sec
median total wall time: 3.45 sec
max total wall time: 69.37 sec
```

By final status:

| Final status | Mean total sec | n |
|---|---:|---:|
| `PASS_FULL_D4_LOADER` | 51.31 | 16 |
| `BLOCKED_ALPHAFILL_200_JSON_HITS_NULL_OR_EMPTY` | 5.50 | 43 |
| `BLOCKED_ALPHAFILL_404` | 4.14 | 20 |
| `BLOCKED_POCKET_EXTRACTION_EMPTY_OR_INVALID` | 6.85 | 17 |
| `BLOCKED_SEQUENCE_MISSING` / timeout | 45.05 | 4 |

Key stage timing:

```text
AlphaFill download median: 2.22 sec; p95: 29.65 sec
ESM-2 3B compute for PASS-like rows: about 29.5–36.9 sec
GVP max: 4.14 sec
loader validation max: 1.94 sec
```

Memory/resource interpretation:

```text
reported process max RSS max ≈ 18.39 GB
reported GPU peak allocated ≈ 11.0–11.24 GB during ESM-2 3B stages
```

Caveat:

`process_max_rss_mb` is process cumulative maximum, not clean per-UID cold-start memory. After the first ESM-2 3B load, subsequent rows inherit a high process max. Use it as an upper-bound process footprint estimate, not as independent per-enzyme memory.

## 9. Formal asset mutation check

Formal before/after snapshot comparison:

```text
mutated=false
mutation_diffs={}
```

No production EnzymeCAGE D4 assets were modified.

## 10. Executor / report weaknesses

These weaknesses do not invalidate the completed probe, but should be noted:

1. The script contains packaging logic that unlinks an existing `ARCHIVE` / `IDENTITY` if present. The run appears fresh and there is no evidence of overwriting an existing completed package, but future prompts should enforce fail-closed output-path existence before any unlink.
2. `BLOCKED_SEQUENCE_MISSING` is an over-broad status for the 4 timeout rows. Future runs should use a more precise token such as:

```text
BLOCKED_SEQUENCE_FETCH_TIMEOUT
```

3. The summary has minor typo keys:

```text
rate_pocket_extractiorate_attempted
rate_pocket_extractiorate_pass
```

The underlying counts are still clear.

4. The resource fields are useful for sizing but are not a perfect cold-start benchmark, because model load/process max effects persist across UIDs.

## 11. Teacher-facing conclusion

This rerun provides the first useful 100-UID estimate for strict on-demand EnzymeCAGE D4 backfill:

```text
16 / 100 sampled missing-pocket UIDs reached full isolated D4 loader eligibility.
The main blockers were AlphaFill 200 with no transplant metadata (43%), AlphaFill 404 (20%), and AlphaFill transplant present but original pocket extraction invalid/empty (17%).
Success was strongly concentrated in the old-pool-with-pocket/recheck stratum (15 / 25), while the AlphaFill-success-no-pocket stratum did not yield a PASS in this sample.
```

Practical implication:

```text
On-demand strict D4 backfill is worth keeping as an agent tool, but it should be framed as a conditional rescue route with explicit blocker reporting, not as a universal way to admit all EC/Rhea-derived candidate enzymes into geometric EnzymeCAGE ranking.
```
