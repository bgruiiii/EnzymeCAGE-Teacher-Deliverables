# Local audit — pollutant TP prediction route evidence package

Date: 2026-08-19  
Package folder:

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/20_Pollutant_TP_Prediction_Route_Evaluation_2026-08-19
```

## Verdict

```text
PACKAGE_READY_FOR_REVIEW
```

The package contains:

1. a teacher-readable final stage report;
2. a test-set construction note for BBD83 and Soil/Sludge;
3. a read-first evidence index;
4. compact comparison tables;
5. directly browsable detailed result tables extracted from returned archives;
6. final cleaned Soil/Sludge transfer v2 package;
7. enviPath known-pathway lookup package;
8. BBD83 route-comparison and ECLIPSE evidence packages;
9. local audits, prompt files and identity sidecars.

## Scope check

Included:

```text
pollutant transformation product prediction / lookup route evaluation
BioTransformer
enviPath prediction and known-pathway lookup
Chem-ECLIPSE NoEC / PREDEC
current available enviFormer checkpoint as historical negative comparator
```

Excluded:

```text
MetaTraits / BacDive microbe-side trait package
enzyme-side M4 acceptance package
production D4 writing
new model training
new prediction runs
```

## Package manifest

The package includes:

```text
PACKAGE_FILE_MANIFEST.tsv
PACKAGE_SHA256SUMS.txt
```

`PACKAGE_SHA256SUMS.txt` covers all non-manifest files in this folder. The package-level manifest files themselves are excluded from package-level checksum coverage.

Local verification after generation:

```text
sha256sum -c PACKAGE_SHA256SUMS.txt
all listed files OK
```

At generation time:

```text
non-manifest files covered: 46
PACKAGE_FILE_MANIFEST.tsv rows: 46 data rows + header
PACKAGE_SHA256SUMS.txt rows: 46
```

## Read-first files

```text
README.md
00_READ_FIRST/POLLUTANT_TP_PREDICTION_ROUTE_STAGE_REPORT_2026-08-19.md
00_READ_FIRST/TEST_SET_CONSTRUCTION_NOTE_2026-08-19.md
00_READ_FIRST/EVIDENCE_INDEX_2026-08-19.md
01_Key_Tables/tool_capability_comparison_2026-08-19.md
01_Key_Tables/route_metric_summary_2026-08-19.csv
06_Detailed_Result_Tables/README_DETAILED_RESULT_TABLES_2026-08-19.md
```

## Final interpretation preserved

The package preserves the following safe conclusion:

```text
For known parent/pathway records, use enviPath local known-pathway lookup first.
For unknown parents requiring blind prediction, BioTransformer ENVMICRO remains the strongest current baseline.
BBD-finetuned ECLIPSE PREDEC improves over ECLIPSE NoEC, but is currently better treated as a complementary candidate generator rather than a BioTransformer replacement.
```

The package also preserves the key caveat:

```text
enviPath Soil/Sludge 100% recovery is database lookup / known-pathway retrieval, not blind prediction accuracy.
```

## Answer self-product check

Local RDKit-canonical checks confirmed:

```text
BBD83 accepted-products table:
148 rows; parent == accepted product rows = 0

Soil/Sludge unique-parent answer key:
2924 rows; parent == accepted product rows = 0

Soil/Sludge parent-product dedup table:
2924 rows; parent == product rows = 0
```

Therefore the reported ECLIPSE/BioTransformer/enviPath scores are not inflated by answer labels that are simply the unchanged parent.
