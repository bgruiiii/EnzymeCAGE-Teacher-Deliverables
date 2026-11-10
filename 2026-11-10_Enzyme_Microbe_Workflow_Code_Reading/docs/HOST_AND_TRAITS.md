# 酶来源、微生物性状与登记信息

## 1. 酶UID到宿主

酶的相似反应匹配／排序分数与宿主证据是两层。不能因为酶分高就认定某菌能降解目标污染物，也不能把物种代表菌株当成原酶来源菌株。

[microbe_recommender.py](../code/depending_t6_prod/src/tools/microbe_recommender.py)保留三态：`LIVE_UNIPROT_REVIEWED`、`FROZEN_REVIEWED_UID_MAP_FALLBACK`、`UNRESOLVED`。UniProt reviewed信息与KEGG补充证据分列；现场网络失败可按合同走冻结表，不能编造宿主。

UID权威表携带TaxID、organism、菌株、proteome、assembly、歧义及来源。使用UID／source_signature精确关系，避免仅凭近似物种名兜底。解析粒度为`EXACT_STRAIN/SPECIES/UNRESOLVED`，不自动提升。

[organism_aggregator.py](../code/depending_t6_prod/src/utils/organism_aggregator.py)按来源合同汇总支持酶。相同酶序列的多个UID／来源仍要保留证据，不能把序列去重误当宿主合并。

## 2. 图内先选菌，后做性状注释

静态t6顺序是`microbe → organism_selection → trait → synthesis`，不是“先用trait_score筛掉菌，再排序”。选菌层有LLM硬依赖，未配置时fail-closed；trait消费只作注释，不改变ranker排名、不硬过滤。

另外有[LLM重排节点](../code/depending_t6_prod/src/nodes/llm_reranking_node.py)在宿主映射之前做可选后处理，失败时透传；它的解释／confidence不等于神经模型校准概率或观测性状。它未纳入CURRENT95五模型比较链。

## 3. MetaTraits离线整理与实际runtime输入

```text
MetaTraits bulk快照
→ C7字段／性状映射
→ C8按source_signature、trait_id构建lookup
→ C8TraitAdapter.annotate读取冻结lookup与UID表
→ HostTraitAnnotation／TraitRecord
```

代码：[MetaTraits字段映射](../code/metatraits_etl/run_metatraits_c7_1_mapping.py)、[C8构建器](../code/c8_lookup_index_builder/run_c8_1_lookup_index.py)、[runtime adapter](../code/depending_t6_prod/src/tools/trait_query.py)。bulk下载脚本是历史工具，不要为了阅读运行它。

adapter直接打开的是：

- UID来源CSV，合同168335行／26列。
- `C8_METATRAITS_LOOKUP_INDEX.jsonl`，合同37170行，即2478个来源×15个F1–F15槽位。

37170是完整槽位数，**不是37170条已观测阳性性状**。各槽位可能有观测、缺失或身份限定。adapter先核固定文件身份／列数／唯一键；资产路径换了不能忽略其SHA门。

入口是`C8TraitAdapter.annotate(organism_candidates)`，不是`.query`。`matched_observed_examples`按实际分号保守拆值；不声称做了数值区间生物学推理。

## 4. BacDive在什么位置

BacDive提供来源身份、登记／保藏可见性及离线构建资料。C8构建器可读取已有BacDive closure／代表菌株表，和MetaTraits资料关联；单独的availability CSV保留登记分辨率及证据。

**当前trait adapter没有直接读取BacDive availability CSV，也没有在线调用BacDive API。**schema允许`BACDIVE_OBSERVED`枚举不证明某次adapter实际读了该表；直接消费者未定位处只列离线资源／引用，不补造在线服务。

`exact_culture_collection/representative_record_available/has_any_culture_collection`等登记状态不等于目前能下单，更不等于该保藏菌株已验证目标污染物降解。登记、可购买、功能验证分开。

## 5. 预测、缺失与输出边界

目前adapter输出观测／缺失／身份限定类：`OBSERVED/MISSING/IDENTITY_ONLY`。真菌在当前MetaTraits范围外时保留identity-only，不把缺失填成阴性结论。

porTraits等预测层有冻结文件，lookup可能标记预测候选可用；当前runtime只产生“候选存在但未启用”的警告，未读取预测资产作为补值、筛选或排名依据。**资产存在≠已在production启用。**

每条性状保留`source_signature/trait_id/source_record_id/evidence_class/resolution`等来源，`used_for_hard_filtering=False`、`used_for_ranking=False`。不产生trait_score/total_score，不能把性状注释写成目标降解功能证明。

## 6. 逐步／路径层结果

[route_step_organism_aggregator.py](../code/depending_t6_prod/src/utils/route_step_organism_aggregator.py)按步骤与宿主身份汇总覆盖和性状，保留物种／菌株及冲突边界。缺一步证据就保留缺失，不能用其他步骤的酶凑齐。

这是既有组件实现，不是本包新组装的整链应用。历史图内至选菌层与图外trait/T5组件组合已被验收；连续图内到synthesis尚未据现有记录确认，详见[状态说明](STATUS_AND_LIMITS.md)。
