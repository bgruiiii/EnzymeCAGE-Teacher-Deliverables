# T6 G5 M3 reaction SHA→canonical SMILES本地恢复说明

日期：2026-09-08

## 结果

```text
S1 / RHEA 11532
reaction=NCC(=O)O.O.O=O>>N.O=CC(=O)O.OO
SHA256=19fe5b26e16a1a8ca60628be8718d3162cabded0299e2276a8503aec787bcf15
match=true

S2 / RHEA 46976
reaction=CN1CCC[C@H]1c1ccc(O)nc1.O=O>>CN1CCC=C1c1ccc(O)nc1.OO
SHA256=9737dd8c994296811f87278e33cc7c8b1743112ddf9ecb745ba6de1e1dc2971a
match=true
```

两个字符串均来自既有冻结M3结果表，不按Rhea名称或相似反应猜测；本地用UTF-8原字符串、不加换行重新计算SHA，
与T6-R2缺口表的hash逐字节一致。机器可读表见同目录
`M3_T6_G5_REACTION_SHA_TO_CANONICAL_SMILES_LOCAL_RECOVERY_2026-09-08.csv`。

## 来源

```text
S1:
03_HPC_Returned_Result_Summaries/m3_p0_preimplementation_evidence_collection_20260717/
outputs/p0_reaction_difficulty_inventory.csv:358

S2:
03_HPC_Returned_Result_Summaries/m3_p0a_local_rhea_source_metric_correction_20260717/
outputs/p0_reaction_difficulty_inventory.csv:193
```

多份后续M3 correction目录还包含相同hash/reaction pair，可在Chenyu预检中交叉验证archive/member身份。

## Authority边界

本恢复关闭的是“能否找回原始reaction string”的数据定位问题，不自行决定公共I/O。正式M3输出是否必须同时携带
`canonical_reaction_smiles`和`reaction_sha256`，仍等待黄老师G5字段契约裁定；在老师确认前不修改生产schema或节点。
