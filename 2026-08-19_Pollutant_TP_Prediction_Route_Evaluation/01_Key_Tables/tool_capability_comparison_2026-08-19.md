# Tool capability comparison — pollutant TP route evaluation

Date: 2026-08-19

## Overall conclusion

| Tool / route | Best use | Current strength | Main limitation | Recommendation |
|---|---|---|---|---|
| BioTransformer ENVMICRO | Unknown-parent blind prediction | Best current Hit@3/5/10 on BBD83 and Soil/Sludge transfer | Some empty/error parents; rule coverage limits | Use as main blind-prediction baseline |
| enviPath local lookup | Known-pathway retrieval | 1788/1788 Soil/Sludge parents and 2924/2924 products recovered | Not blind prediction; only works when parent/pathway exists in database | Use first when parent/pathway exists |
| enviPath BBD Rules prediction | Rule-based one-step prediction | BBD83 Hit@10 43/83; has complementary cases | Below BioTransformer overall | Use as secondary/corroborating evidence |
| BBD-finetuned ECLIPSE PREDEC | Complementary candidate generation | Better than ECLIPSE NoEC; BBD83 all-fold strong | Conservative OOF and Soil/Sludge transfer still below BioTransformer; parent-copy behavior | Keep as supplement / future improvement target |
| ECLIPSE NoEC | No-EC baseline for ECLIPSE | Useful ablation baseline | Weaker than PREDEC | Do not use as main route |
| enviFormer latest-current | External model tested earlier | Technically runs | BBD83 score very low under available checkpoint | Do not use as current main route |

## Key prediction metrics

### BBD83 known-pathway v0.2

| Route | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 | Product labels@10 |
|---|---:|---:|---:|---:|---:|---:|
| BioTransformer ENVMICRO | 28/83 | 40/83 | 50/83 | 50/83 | 0.428 | 60/148 |
| enviPath BBD Rules prediction | 20/83 | 35/83 | 42/83 | 43/83 | 0.343 | 60/148 |
| enviFormer latest-current | 1/83 | 1/83 | 2/83 | 3/83 | 0.016 | 4/148 |
| BBD-finetuned ECLIPSE PREDEC OOF parent-filtered | 26/81 | 38/81 | 38/81 | 38/81 | 0.389 | 45/145 |
| BBD-finetuned ECLIPSE PREDEC all-fold parent-filtered | 37/83 | 60/83 | 66/83 | 66/83 | 0.589 | 87/148 |

Interpretation:

```text
All-fold ECLIPSE PREDEC is strong but optimistic; conservative OOF remains below BioTransformer.
```

### Soil/Sludge transfer, combined all-valid parent-filtered

| Route | Valid non-empty coverage | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR@10 |
|---|---:|---:|---:|---:|---:|---:|
| ECLIPSE NoEC | 1781/1788 | 10.91% | 18.85% | 22.15% | 23.15% | 0.154 |
| ECLIPSE PREDEC | 1785/1788 | 11.35% | 20.81% | 25.11% | 26.51% | 0.167 |
| BioTransformer ENVMICRO | 1679/1788 | 10.63% | 21.48% | 27.52% | 30.93% | 0.172 |

### enviPath known-pathway lookup on Soil/Sludge-derived set

| Scope | Parents found | Accepted product labels recovered | Interpretation |
|---|---:|---:|---|
| Soil/Sludge combined | 1788/1788 | 2924/2924 | Complete local known-pathway retrieval |
| BBD-parent-excluded | 1731/1731 | 2834/2834 | Complete local known-pathway retrieval |

This is lookup/oracle retrieval, not blind prediction.

