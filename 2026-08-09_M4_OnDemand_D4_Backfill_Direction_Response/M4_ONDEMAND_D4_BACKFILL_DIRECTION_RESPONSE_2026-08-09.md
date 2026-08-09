# M4 D4 按需补资产工具化立项方向回应

日期：2026-08-09  
状态：提交老师审阅的 M4 立项方向回应；不构成 M4 正式实施完成。  
依据：黄老师 2026-08-07 回复中 M4 合同立项方向评估要求。

## 0. 交付位置边界

老师 2026-08-07 明确要求 S1/S2 修正后 push 至原交付包位置；但对本次 M4 立项方向回应，只要求提交方案内容：

```text
1) 工具化方案设计；
2) 工作量/时间线评估；
3) Phase 1 验收 UID 子集选择口径。
```

老师未在该回复中指定 M4 方向回应的 GitHub 上传目录或新交付包位置。因此本次按日期建立 M4 专用回应包提交；若老师后续指定其他位置或格式，再按老师要求同步/迁移。

```text
交付包：
2026-08-09_M4_OnDemand_D4_Backfill_Direction_Response/

本包只提交立项方向回应与本地审计；
不包含 M4 implementation output；
不包含 staged D4 assets；
不包含 production D4 merge。
```

## 1. 总体回应

我们接受老师提出的 M4 合同立项方向：先把 D4 按需补资产做成可审计、可缓存、可查询状态的工具化流程，而不是一次性全量重建。

建议 Phase 1 作为本期核心：

```text
1. P2Rank predicted-pocket supplementation：
   对 strict missing-pocket / missing-D4 UID 做 predicted-pocket staged 补充；
   该路线必须作为 lower-evidence tier 标注，不能等同 strict AlphaFill pocket。

2. ESM-2 3B on-demand extraction/cache：
   按 UID 和 pocket 定义补当前 3B 特征，缺哪个补哪个，落 staged cache；
   不一次性全量提取 88,038 个 strict ESM2-3B-missing UID。

3. GVP + pocket-node ESM + isolated loader validation：
   GVP 与 pocket-node ESM 必须来自同一 pocket 定义；
   必须实际通过 isolated load_geometric_dataset(...) / dataset[0] 构造。

4. staged package discipline：
   所有资产先 staged，保留来源、参数、版本、SHA256、状态表；
   不直接写 production D4，不修改 production pool。
```

Phase 2 可作为可选扩展：

```text
GVP / ESM-C 资产物化恢复。
```

其中 GVP 可能需要去 340 主机查历史资产；ESM-C 600M 历史资产不能作为当前 ESM-2 3B 输入的替代。

## 2. Phase 1 工具化设计

### 2.1 Pocket route

优先保留 strict AlphaFill 8 A ligand-neighborhood route 作为较高证据路线。若 AlphaFill transplant metadata 不可用、AlphaFill 404、或 strict pocket extraction invalid，则使用 P2Rank predicted-pocket 作为 lower-evidence staged fallback。

Phase 1 验收建议以 AlphaFoldDB-only structure acquisition + P2Rank 作为默认 predicted-pocket route，因为 08-03 控制实验表明该口径更清晰、可复现性更好：

```text
strict AlphaFill route: PASS_FULL_D4_LOADER = 16 / 100
mixed-structure P2Rank: PASS_PREDICTED_POCKET_D4_LOADER = 42 / 100
AlphaFoldDB-only P2Rank: PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER = 45 / 100
```

但该结果只能说明 staged D4 constructability / loader eligibility，不说明：

```text
P2Rank pocket 与 AlphaFill pocket 等价；
预测 pocket 已进入 production D4；
任意 UID 都一定能补成功；
目标反应生物学正确性已验证。
```

P2Rank 工具身份按验收包记录：

```text
P2Rank version = 2.5.1
command form = prank predict -threads 4 -c alphafold -visualizations 0 ...
per-UID .ds dataset file invocation required
```

此前小测观察到的 P2Rank 路径是任务运行时临时路径，不应写成 Chenyu 长期固定工具路径。正式 Phase 1 前应先做只读 preflight，记录当前 `prank` / `p2rank` / Java 版本与 SHA256；若不存在稳定路径，再按授权建立隔离版本化工具目录。

### 2.2 ESM-2 3B on-demand/cache

当前 Phase 1 使用的模型合同为：

```text
model_name = esm2_t36_3B_UR50D
repr_layer = 36
embedding_dim = 2560
node feature shape = [L+2, 2560]
seq2feature shape = [2560]
pocket-node feature shape = [pocket_residue_count, 2560]
```

cache key 不应只用 UID，而应至少包含：

```text
UID;
canonical sequence SHA256;
model/checkpoint identity;
structure source and SHA256;
normalized structure SHA256;
pocket source tier and pocket residue list SHA256;
pocket PDB SHA256;
extractor script identity;
runtime/software identity.
```

这样可以避免同一 UID 在 sequence、structure 或 pocket definition 变化后误命中旧缓存。

明确不采用：

```text
ESM-C 600M 替代 ESM-2 3B；
ESM-2 650M 替代 ESM-2 3B；
旧路径或旧资产无审计复用。
```

### 2.3 GVP and loader validation

每个 PASS UID 必须同时满足：

```text
selected pocket PDB 只含目标蛋白链/目标 residues；
GVP node count == pocket-node ESM row count；
pocket_info.csv row count == GVP node count；
isolated load_geometric_dataset(...) 被实际调用；
dataset length == 1；
dataset[0] constructed；
formal assets mutated = false；
production pool mutated = false。
```

P0A434 早期小测曾出现 A/B 双链重复导致的假 58/58 对齐问题，因此 Phase 1 必须把 chain normalization、pocket residue provenance、GVP/ESM 行数一致性作为硬门槛。

### 2.4 Output discipline

每次 acceptance run 应保留：

```text
SAMPLED_UIDS.csv
SAMPLE_DESIGN_REPORT.md/json
PER_UID_STATUS_TABLE.csv
PER_UID_TIMING_RESOURCE_TABLE.csv
STRUCTURE_SOURCE_TABLE.csv
P2RANK_VERSION_AND_INSTALL_REPORT.txt
STAGED_ASSET_MANIFEST.csv
FORMAL_ASSET_MUTATION_CHECK.json
MANIFEST.sha256
FINAL_STATUS.txt
per_uid/<UID>/*
```

PASS UID 至少保留：

```text
raw sequence / structure source evidence；
P2Rank .ds input and raw output；
pocket PDB and pocket_info.csv；
ESM-2 3B node-level / seq2feature / pocket-node assets；
GVP staged asset；
single-row loader validation input；
loader validation report。
```

## 3. 工作量与时间线

建议给老师采用两档估计，避免无条件承诺过头。

最快情形：

```text
正式 M4 implementation authorization 后约 1-2 个工作日。
条件：
  Chenyu 当前 P2Rank/Java、ESM-2 3B、GVP、loader 依赖均可直接使用；
  现有小测脚本能快速改造成最小 acceptance wrapper；
  无需新增环境修复；
  只做 Phase 1 >=100 UID staged acceptance package，
  不包含全 4,681 UID processing，不包含 production merge，不包含 340 主机 Phase 2。
```

保守情形：

```text
正式 M4 implementation authorization 后约 3-5 个工作日。
触发条件：
  需要先固定 P2Rank/Java 路径；
  需要补 wrapper / cache / manifest discipline；
  需要重新做 5-10 UID smoke；
  需要完整本地 provenance / overclaim audit 后再提交。
```

此前小测 runtime 仅作为 order-of-magnitude anchor：

```text
strict AlphaFill 100 UID: all-UID mean 14.37 sec/UID, PASS-row mean 51.31 sec/UID；
mixed P2Rank 100 UID: all-UID mean 7.78 sec/UID；
AFDB-only P2Rank 100 UID: all-UID mean 13.76 sec/UID；
ESM-2 3B PASS-like rows: about 29.5-36.9 sec compute；
GPU peak allocated during 3B stages: about 11.0-11.24 GB。
```

这些小测不应线性外推成 full 4,681 UID 的保证时间，因为网络/API、queue、cache hit、fail-closed rate、当前工具路径都可能影响正式运行。

## 4. Phase 1 验收 UID 子集口径

建议使用 frozen deterministic stratified subset，至少 100 UIDs。抽样前先冻结 manifest，不在跑完后补换 UID。

推荐 universe：

```text
strict 2026 UID set 中 missing valid pocket / missing-D4 的 UID；
优先围绕 accepted F3 accounting 中 strict UID missing valid pocket = 4,681；
ESM-2 3B on-demand/cache 测试应覆盖当前 3B 缺失或 staged pocket definition 与现有特征不一致的 UID。
```

建议与 08-03 小测同构，便于和已有结果比较：

| Stratum | Target count |
|---|---:|
| `ALPHAFILL_SUCCESS_NO_POCKET_INTERSECT_FINAL_MISSING` | 35 |
| `OLD_POOL_WITH_POCKET_INTERSECT_FINAL_MISSING` | 25 |
| `OLD_POOL_WITHOUT_POCKET_INTERSECT_FINAL_MISSING` | 40 |

Freshness rule：

```text
优先选择未进入 2026-08-03 100-UID pilots 的 fresh UID；
若某 stratum 不足，则如实报告 deficit；
不得静默从别的 stratum 补齐；
可另设 2-5 个 prior PASS/blocker UID 作为 regression controls，
但不计入主 >=100 acceptance denominator。
```

验收不要求全部 UID PASS，而要求全部 UID 有且只有一个可审计 final status：

```text
PASS_AFDB_P2RANK_PREDICTED_POCKET_D4_LOADER
BLOCKED_SEQUENCE_MISSING_OR_TIMEOUT
BLOCKED_AFDB_STRUCTURE_FETCH_FAILED
BLOCKED_AFDB_P2RANK_NO_POCKET
BLOCKED_P2RANK_POCKET_MAPPING_FAILED
BLOCKED_ESM3B_EXTRACTOR_OR_CHECKPOINT
BLOCKED_GVP_OR_POCKET_ESM_ALIGNMENT
BLOCKED_LOADER_VALIDATION_FAILED
BLOCKED_OUTPUT_PATH_EXISTS
```

建议 acceptance package final status：

```text
M4_ONDEMAND_D4_PHASE1_ACCEPTANCE_COMPLETE_WITH_PASS_AND_BLOCKER_COUNTS
```

不应使用：

```text
M4_PRODUCTION_D4_BACKFILL_COMPLETE
M4_ALL_4681_UIDS_BACKFILLED
PASS_FULL_D4_LOADER
```

除非后续证据和老师授权确实支持这些说法。

## 5. Full 4,681 与 ESM2-3B 缺口处理

Phase 1 acceptance 与 full 4,681 UID status table 应分开：

```text
第一里程碑：>=100 UID frozen subset acceptance package；
第二里程碑：老师接受 Phase 1 后，再考虑 full 4,681 UID population
             或仍未处理部分的 staged status table。
```

88,038 个 strict ESM2-3B-missing UID 不建议本期全量 upfront 提取：

```text
只在 UID 被请求或与已接受 pocket-backfill UID 联动时按需提取；
不在 M4 Phase 1 acceptance 中发起 88,038 UID 全量 3B rebuild。
```

## 6. Phase 2 可选项

GVP：

```text
GVP 历史资产可能存在于 340 主机；340 主机不是 Chenyu/HPC。
目前本窗口尚未检查 340 主机，因此不能声称 GVP 资产已经找到或可用。
周一可去 340 主机查找，并在文件 identity、format、compatibility 审计后再汇报。
```

ESM-C：

```text
历史 ESM-C 资产是 600M-family 路线。
当前 M4 Phase 1 输入合同是 ESM-2 3B、2560 维、esm2_t36_3B_UR50D。
因此 ESM-C 600M 不能作为缺失 ESM-2 3B 资产的替代。
```

## 7. 请求老师裁定

请老师裁定：

```text
1. 是否同意 M4 Phase 1 先按 P2Rank predicted-pocket lower-evidence tier
   + ESM-2 3B on-demand/cache + staged loader validation 的方向立项；

2. 是否同意 Phase 1 acceptance 先做 >=100 UID frozen stratified subset，
   通过 pass/blocker counts、cache behavior、manifest/SHA256、no-production-mutation
   来验收工具化流程；

3. 是否同意 full 4,681 UID status table 放在 Phase 1 acceptance 通过后的
   下一里程碑，而不是并入首个 acceptance package；

4. 是否同意 Phase 2 只保留为 GVP/ESM-C archive/materialization recovery，
   其中 GVP 先查 340 主机，ESM-C 600M 不替代当前 ESM-2 3B。
```
