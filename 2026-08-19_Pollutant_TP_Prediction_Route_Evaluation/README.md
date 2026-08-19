# Pollutant transformation-product prediction route evaluation package

Date: 2026-08-19  
Scope: pollutant transformation-product prediction / lookup route evaluation only.

This folder is a teacher-facing evidence package for the recent pollutant-transformation route exploration.

Read first:

```text
00_READ_FIRST/POLLUTANT_TP_PREDICTION_ROUTE_STAGE_REPORT_2026-08-19.md
00_READ_FIRST/TEST_SET_CONSTRUCTION_NOTE_2026-08-19.md
00_READ_FIRST/EVIDENCE_INDEX_2026-08-19.md
00_READ_FIRST/PACKAGE_LOCAL_AUDIT_2026-08-19.md
```

Directly browsable detailed tables:

```text
06_Detailed_Result_Tables/README_DETAILED_RESULT_TABLES_2026-08-19.md
```

Main conclusion:

```text
For known parent/pathway records, use enviPath local known-pathway lookup first.
For unknown parents requiring blind prediction, BioTransformer ENVMICRO remains the strongest current baseline.
BBD-finetuned ECLIPSE PREDEC improves over ECLIPSE NoEC, but is currently better treated as a complementary candidate generator rather than a BioTransformer replacement.
```

Important boundary:

```text
enviPath Soil/Sludge 100% recovery is database lookup / known-pathway retrieval, not blind prediction accuracy.
```
