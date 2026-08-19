# Local audit — enviPath Soil/Sludge known-pathway lookup supplement return

Date: 2026-08-19  
Return archive:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz
```

Identity file:

```text
/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/envipath_soil_sludge_known_pathway_lookup_supplement_20260819.tar.gz.identity.txt
```

## 1. Verdict

The local snapshot lookup result is valid and useful.

The package shows that the 1788 Soil/Sludge parent compounds used in the transfer evaluation are all exactly retrievable from the local enviPath Soil/Sludge snapshot, and all 2924 accepted product labels are recovered.

This supports the following conclusion:

```text
enviPath local snapshot lookup is a complete known-pathway retrieval layer for this Soil/Sludge-derived evaluation set.
```

It must not be described as blind prediction accuracy, because the evaluated cases were built from the same Soil/Sludge enviPath source.

## 2. Package integrity

Archive identity:

```text
archive_sha256=ad17f6377f2f5d8f97d226469eda7e149dfb8527928c350bcf0e80ab40068886
archive_bytes=103164
final_status=ENVIPATH_SOIL_SLUDGE_LOOKUP_SUPPLEMENT_COMPLETE
restricted_answer_key_read=true
```

Manifest check:

```text
sha256sum -c MANIFEST.sha256
```

All listed files passed. Unlike the prior Soil/Sludge transfer evaluation package, this manifest correctly excludes `MANIFEST.sha256` itself.

## 3. Local snapshot lookup result

Input:

```text
prior Soil/Sludge transfer eval set:
1788 unique parent compounds
2924 accepted parent-product labels
```

Local snapshot lookup source:

```text
/root/projects/EnzymeCAGE-master/data/envipath.csv
Soil rows: 2584
Sludge rows: 497
Soil+Sludge rows: 3081
```

Main metrics:

| Label | Parents | Parent found | Found rate | Parents with all accepted products recovered | Accepted product labels recovered | Product recall | Extra products |
|---|---:|---:|---:|---:|---:|---:|---:|
| combined | 1788 | 1788 | 100.0% | 1788/1788 | 2924/2924 | 100.0% | 0 |
| soil | 1521 | 1521 | 100.0% | 1521/1521 | 2454/2454 | 100.0% | 0 |
| sludge | 276 | 276 | 100.0% | 276/276 | 501/501 | 100.0% | 0 |
| bbd_parent_excluded | 1731 | 1731 | 100.0% | 1731/1731 | 2834/2834 | 100.0% | 0 |
| bbd_parent_overlap_only | 57 | 57 | 100.0% | 57/57 | 90/90 | 100.0% | 0 |

The local tables are internally consistent:

```text
local_snapshot_parent_lookup_results.csv rows: 1788
local_snapshot_product_recall_by_parent.csv rows: 1788
local_snapshot_unmatched_parents.csv rows: 0
local_snapshot_product_mismatch_details.csv rows: 0
```

Independent recalculation confirmed:

```text
lookup_status=found_exact_parent: 1788/1788
all_accepted_products_recovered=True: 1788/1788
accepted total: 2924
recovered total: 2924
lookup products total: 2924
lookup extra products: 0
```

## 4. Official API bounded sample

The optional API check was attempted and appears to have succeeded for the sampled parents.

Reported in `official_api_request_audit.json`:

```text
login_status=success
request_count=80
success_count=80
error_count=0
sample_size=80
http_status_distribution={"200": 80}
```

`logs/official_api_lookup.log` also says:

```text
Login OK
Stratified sample: 80 parents
```

However, there are two documentation defects:

1. `official_api_lookup_summary.md` says “Stratified sample of 100 parents,” but the actual result is 80 parents.
2. `official_api_blocker_or_skip_reason.md` contains:

```text
Reason: name 'source' is not defined
```

This conflicts with the completed API audit JSON and summary.

Interpretation:

- Treat the official API result as a bounded 80-parent sanity check, not a full 1788-parent API audit.
- The local snapshot lookup remains the authoritative full audit.
- The stale blocker file should be removed or corrected in any cleaned supplement package.

## 5. Comparison with prediction routes

The package correctly separates lookup/oracle retrieval from prediction.

Headline comparison from the returned summary:

| Route | Type | Count / rate |
|---|---|---:|
| enviPath local lookup | known-pathway retrieval / oracle | 1788/1788 parents found; 1788/1788 all products recovered |
| ECLIPSE NoEC | prediction Hit@10 | 414/1788 = 23.2% |
| ECLIPSE PREDEC | prediction Hit@10 | 474/1788 = 26.5% |
| BioTransformer ENVMICRO | prediction Hit@10 | 553/1788 = 30.9% |

This comparison is acceptable only because it labels enviPath lookup as oracle/known-pathway retrieval.

Safe interpretation:

```text
If a Soil/Sludge parent already exists in the enviPath package, local enviPath lookup can recover its known transformation products completely.
This supports an enviPath-first known-pathway retrieval layer.
For unknown parents, BioTransformer/ECLIPSE-style predictive routes are still needed.
```

Unsafe interpretation:

```text
enviPath has 100% prediction accuracy on Soil/Sludge.
```

Do not use that wording.

## 6. What this means for the current exploration

Together with the prior Soil/Sludge transfer evaluation, the current state is:

1. BBD-only ECLIPSE PREDEC transfers better than ECLIPSE NoEC.
2. BioTransformer ENVMICRO remains stronger than ECLIPSE on blind Soil/Sludge prediction metrics.
3. enviPath local snapshot lookup gives complete known-pathway recovery for Soil/Sludge-derived cases.
4. Therefore the practical route is likely:

```text
known parent/pathway exists in enviPath -> use enviPath lookup first
otherwise -> use BioTransformer ENVMICRO as current strongest prediction baseline
ECLIPSE PREDEC -> complementary candidate generator / future improvement target
```

## 7. Remaining cleanup before final report

The lookup supplement itself is good enough for reporting with the API sample-size caveat.

But the prior Soil/Sludge transfer evaluation package still needs a small cleanup supplement if we want a clean final evidence package:

1. Regenerate its `MANIFEST.sha256` excluding itself.
2. Correct BioTransformer coverage from reported `1788/1788` to valid non-empty `1679/1788`.
3. Add BioTransformer rows to `per_parent_scoring_table.csv`.
4. Remove or clearly mark skipped `eclipse_oracle_ec` zero rows.
5. Optionally remove / fix stale official API blocker text in this lookup supplement if repackaging both together.

After that, the exploration is close enough to write a final report.
