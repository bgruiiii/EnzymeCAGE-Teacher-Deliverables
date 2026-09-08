# 晨羽数据库与模型权重上云清单（给黄老师审阅）

日期：2026-09-08
状态：`LIVE_INVENTORY_CORRECTED_LOCALLY_FOR_TEACHER_REVIEW`
说明：本清单只统计晨羽数据库、特征/索引、映射数据及模型权重；不包含应用源码、LangGraph、wrapper、Python环境、
日志和workspace。当前只调研，尚未上传或迁移。

## 一、结论

晨羽目前已定位、值得进入云迁移候选的内容可分为：

```text
1. 酶特征数据库；
2. 反应与路线知识数据库；
3. 反应预测所需模板/corpus/donor与ranker权重；
4. 酶—宿主/微生物映射数据库；
5. 微生物F1—F15性状数据库；
6. EnzymeCAGE模型权重。
```

当前已知合计下限：

```text
数据库/特征/映射＋EnzymeCAGE 3B/600M两套权重＋depending v3.2数据/ranker
=56,532,141,928 B
=52.650 GiB
```

其中600M为fallback。若首批只保留当前3B主模型：

```text
56,275,451,998 B
=52.411 GiB
```

是否同时上云3B、600M及保留多少历史模型版本，请黄老师决定。模型权重与数据库分目录管理，但都列入本次容量调研。

## 二、酶特征数据库

| 数据资产 | 晨羽路径 | 大小 | 格式 | 用途 | 建议 |
|---|---|---:|---|---|---|
| GVP蛋白特征 | `/usrdata/EnzymeCAGE_data/feature/protein/gvp/gvp_protein_feature_flat.pt` | 16,376,782,766 B | PyTorch `.pt`字典 | 候选酶结构/GVP节点与边特征 | 首批P0；OSS权威副本＋NAS/CPFS/NVMe运行缓存 |
| ESM2-3B口袋节点特征 | `/usrdata/EnzymeCAGE_data/feature/protein/ESM2_3B_corrected_107705/pocket_node_feature/esm_node_feature.torch.pt` | 37,652,506,777 B | PyTorch `.pt`字典 | 候选酶口袋残基特征 | 首批P0；后续按UID分片，避免每进程全量加载 |
| ESM2-3B全蛋白均值特征 | `/usrdata/EnzymeCAGE_data/feature/protein/ESM2_3B_corrected_107705/protein_level/seq2feature.pkl` | 932,295,619 B | pickle映射 | 全蛋白序列向量 | 首批P0；保留原文件并规划Parquet/Arrow/安全分片 |
| D4可计算UID白名单 | `m3_agent_data_assets/assets/d4/uid_asset_availability.csv.gz` | 4,444,684 B；107,705 UID | gzip CSV | forward前判断UID计算资产完整性 | 首批P0；可转SQLite/Parquet键索引 |
| UID/sequence来源表 | `formal_splits/formal_filtered_{train,valid,test}.csv` | 合计602,825,079 B | CSV | 当前wrapper初始化时建立UID→唯一sequence映射 | 当前P0；以后抽出紧凑UID-sequence表后，split可降为归档 |

前三项大特征合计54,961,585,162 B（51.187 GiB），是首批容量和运行IO的主体。

## 三、EnzymeCAGE反应特征数据库

| 数据资产 | 晨羽路径 | 大小 | 格式/数量 | 用途 | 建议 |
|---|---|---:|---|---|---|
| 分子构象及图 | `feature/reaction/molecule_conformation_round1_full_20260707` | 35,359,437 B | 4,239 SDF＋`mol2id.csv`＋`mol_graph_dict.pt` | 反应物/产物三维图 | 首批P0；小文件多，适合NAS/CPFS或打包图存储 |
| DRFP反应特征 | `feature/reaction/drfp/rxn2fp.pkl` | 41,663,310 B | pickle | 反应全局向量 | 首批P0；运行前本地缓存 |
| 反应中心 | `feature/reaction/reacting_center/reacting_center.pkl` | 4,494,676 B | pickle | 原子反应中心mask | 首批P0；与DRFP/构象同版本发布 |

`mol_graph_dict.pt`为25,927,011 B可重建cache。黄老师可选择：上传cache以缩短云端启动，或只上传SDF＋mol2id并在
云端重建；容量表不能同时把archive、SDF和cache重复计算。

后来新增的T3B反应资产目前只是最小staged样本，后续所有新反应DRFP/AAM/center/mol graph作为
`new_reaction_assets`版本化delta追加，不阻塞现有反应库先上云。

## 四、反应与候选酶知识数据库

| 数据资产 | 大小 | 格式/规模 | 用途 | 建议 |
|---|---:|---|---|---|
| Rhea reaction SMILES | 11,189,076 B | TSV | 已知反应和路线身份 | 首批P0，OSS原始表＋Parquet/SQLite查询副本 |
| Rhea→Swiss-Prot | 8,622,649 B | TSV | 反应—蛋白证据 | 首批P0 |
| Rhea方向表 | 440,280 B | TSV | 规范化反应方向 | 首批P0 |
| Rhea→EC | 193,357 B | TSV | EC候选入口 | 首批P0 |
| Route C参考反应 | 912,998 B | gzip CSV；4,051反应 | full-reaction相似检索 | 首批P0 |
| Route C Morgan radius-8 | 3,256,379 B | RDKit pickle | 相似度计算 | 首批原样；后续转显式稀疏向量并固定RDKit版本 |
| Route B EC→UID | 618,715 B | gzip CSV | B-primary候选酶池 | 首批P0 |

上述M3/Rhea/Route B/C/D4数据整包现有约29.75MB，体量小，值得完整版本化上云。

## 五、depending v3.2反应预测数据和ranker

T2B已审计的完整八项运行资产如下。晨羽live盘点本次没有逐项复核完整路径，因此最终上传前需再做一次逐文件身份核验，
但不能只用本次盘点中的4.8MB retrieval目录替代它们。

| 资产 | 大小 | 格式 | 类型 |
|---|---:|---|---|
| `reaction_analogy/templates.json` | 11,217,167 B | JSON | 生成模板数据 |
| `reaction_v3/data/lib_envipath/templates.tsv.gz` | 31,059 B | gzip TSV | enviPath模板数据 |
| `data/hfix/templates_implicitH.jsonl` | 138,383 B | JSONL | implicit-H规则数据 |
| `reaction_analogy/data/corpus_v1/corpus_v1.jsonl` | 47,818,894 B | JSONL；37,680记录 | retrieval corpus |
| `reaction_analogy/data/corpus_v1/donor_index.jsonl` | 13,734,527 B | JSONL；14,334 donor | donor索引 |
| `uspto_ranker.txt` | 1,263,228 B | LightGBM文本权重 | 模型权重 |
| `envipath_ranker.txt` | 645,960 B | LightGBM文本权重 | 模型权重 |
| `retrieval_ranker.txt` | 659,831 B | LightGBM文本权重 | 模型权重 |

```text
五项数据合计=72,940,030 B
三个ranker合计=2,569,019 B
全部合计=75,509,049 B
```

depending当前仍是evaluation candidate。是否纳入首批云端正式运行由黄老师结合T4结果决定；即使暂不启用，也建议
把已固定身份的八项作为一个不可拆的候选版本保存，避免模板、corpus和ranker错配。

## 六、酶—宿主与微生物映射数据库

| 数据资产 | 大小 | 格式/规模 | 用途 | 当前判断 |
|---|---:|---|---|---|
| UID→source_signature | 104,025,134 B | 26列CSV；168,335 UID、3,234 source | 候选酶精确映射微生物来源 | 首批P0，转Parquet/SQLite唯一键索引 |
| Rhea→Swiss-Prot | 8,622,649 B | TSV | 反应—蛋白证据连接 | 已在Rhea表中计数，不重复 |
| enzyme2organism后台库 | 未定位 | 当前只发现`localhost:8001` HTTP endpoint | UID→organism | 必须继续追踪后台数据库；endpoint本身不上传 |
| taxonomy crosswalk | 未完整定位 | CSV/TSV/JSON待核 | strain/species/representative strain分辨率 | 建议上云，待晨羽补路径与大小 |

这里不能把HTTP服务写成“无需迁移”后结束。若最终云端仍调用该服务，需要迁移其后台数据库或明确改用已经冻结的
UID→source映射及其他宿主数据源。

## 七、微生物性状数据库

| 数据资产 | 大小 | 格式/规模 | 用途 | 建议 |
|---|---:|---|---|---|
| C8 F1—F15 lookup | 57,211,793 B | JSONL；37,170行＝2,478 source×15 trait | 运行期只读性状查询 | 首批P0，原JSONL＋Parquet/SQLite查询副本 |
| BacDive availability | 1,446,093 B | CSV；2,478行 | 证据可用性和边界 | 与C8同版本、受控权限 |
| C8 source universe | 269,234 B | CSV；2,478行 | 固定source分母 | 首批P0 |
| C8 delta review | 48,903 B | CSV；137行 | 主库外候选 | 独立delta，不静默并入base |
| MetaTraits原始bulk输入 | 276,530,176 B | tar | 重建/预测输入来源 | P1受控原始区；不是预测结果 |
| 微生物预测性状输出 | 当前未冻结 | 待完成 | 补充缺失性状的predicted evidence | 完成并验证后作为`predicted_trait_assets` delta |

微生物预测性状仍在补齐，不阻塞当前observed/identity/missing的C8 base先上云。预测结果不能覆盖observed值，也不能
在完成前写入正式base。

## 八、模型权重

| 模型 | 晨羽状态 | 大小 | 是否建议上云 |
|---|---|---:|---|
| EnzymeCAGE 3B五seed | 当前主运行模型 | 361,332,490 B | 建议首批上云 |
| EnzymeCAGE 600M五seed | fallback | 256,689,930 B | 请黄老师决定是否首批保留 |
| depending三个LightGBM ranker | evaluation candidate配套 | 2,569,019 B | 与depending八项版本绑定保存；是否启用等T4 |

模型权重建议放独立`models/<model_id>/<version>/`，与数据库base版本建立兼容矩阵；不和CSV/JSONL混在同一查询层。
源码、wrapper和Python环境不在本表，也不计入容量。

## 九、建议的云端放置

| 数据形态 | 建议 | 原因 |
|---|---|---|
| 原始数据、版本快照、模型权重、manifest | OSS版本化对象 | 权威副本、灾备、版本回滚 |
| `.pt/.pkl/.sdf`运行工作集 | NAS/CPFS＋节点本地NVMe | 当前loader要求POSIX路径，不能直接从OSS随机读取 |
| Rhea、UID map、C8、D4等键值表 | Parquet/SQLite/DuckDB；并发上来后再评估RDS/PolarDB | 当前规模不大，先避免过度建设 |
| 凭据 | KMS/Secrets Manager | 不得放数据库bucket |

首批先按现有字节身份迁移；分片、Parquet化和索引优化必须另建新版本并通过结果等价测试，不能在上传时直接替换原始
格式。

## 十、版本化增量

```text
base：当前已审计酶特征、反应库、UID-host映射、C8 lookup和老师选择的模型权重；
new_enzyme_assets delta：额外UID、OnDemand D4、后来补充的酶特征；
new_reaction_assets delta：T3B及后续新反应资产；
predicted_trait_assets delta：正在生成的微生物预测性状；
```

M4 E2中1,704条staged PASS不能直接算production库；其余1,324 no-pocket、1,650 AFDB fetch blocker和3条ESM blocker
仍待闭合。所有额外酶资产补齐、审计和promotion后再追加delta，不阻塞当前基础库先迁移。

## 十一、请黄老师决定

1. EnzymeCAGE首批只保留3B，还是3B＋600M fallback都上云；
2. depending v3.2是否随首批作为evaluation候选保存，还是等T4后进入下一波；
3. MetaTraits原始bulk和BacDive相关数据采用何种内部权限与许可复核；
4. 是否要求首批同时上传可重建`mol_graph_dict.pt`以换取更快启动；
5. 是否先建立轻量Parquet/SQLite/DuckDB索引，还是直接规划云数据库服务；
6. enzyme2organism后台数据库由哪一侧提供/迁移。

当前清单是容量与可行性调研，不代表已经上传、成本获批或production切换。

## 十二、数据来源与审计边界

本清单依据晨羽只读live盘点包：

```text
chenyu_final_pipeline_runtime_database_cloud_migration_readonly_inventory_20260908.tar
bytes=245760
SHA256=7895efc23e76993486f5e69a655db13f3ec4cc60b04d2ca32d3cd77db1567023
包内manifest=20/20 OK
```

本地没有收到该包的独立identity/validation sidecar。原包摘要还存在模板占位符、wrapper混入容量、depending资产
遗漏、formal split运行角色及MetaTraits语义等问题，因此本稿使用其live stat/path证据并做了独立口径纠正，没有
直接复制原包READY结论。详细本地审计见：

```text
04_Local_Review_Audits/
CHENYU_FINAL_PIPELINE_RUNTIME_DATABASE_CLOUD_MIGRATION_READONLY_INVENTORY_RETURN_LOCAL_AUDIT_2026-09-08.md
```
