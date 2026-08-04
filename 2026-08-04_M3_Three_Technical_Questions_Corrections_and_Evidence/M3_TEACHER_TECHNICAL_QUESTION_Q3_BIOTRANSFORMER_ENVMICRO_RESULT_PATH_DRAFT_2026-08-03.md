# M3 给黄老师的技术问题回复草稿 Q3：BioTransformer ENVMICRO 结果产出路径

日期：2026-08-03  
状态：draft；本文件只解释我们实际使用的 BioTransformer 环境/微生物转化模块，不讨论人体代谢、CYP、Phase II 等未使用模块。

## 0. 简短结论

我们当前用到的 BioTransformer 路径是：

```text
单个 parent pollutant SMILES
→ BioTransformer 3.0 的 ENVMICRO / environmental microbial biotransformation 模块
→ 生成一批候选一代环境转化产物
→ adapter 用 RDKit 规范化、去重、保留 Top-10
→ 本地用 restricted answer key 评分
```

执行命令固定为：

```text
java -jar <biotransformer-3.0.0.jar> -k pred -b env -ismi <parent_smiles> -ocsv <case_output_csv> -s 1
```

这里最关键的是：

```text
-b env
```

它对应我们关心的环境/微生物转化模块。我们没有使用人体代谢模块，也没有使用全模块参数。257 条 valid single-parent 技术测试中，257 个 `command.txt` 全部是 `-b env`，并且 `forbidden -a=0`。

## 1. 这个工具在我们流程里回答什么问题

BioTransformer ENVMICRO 回答的是：

```text
给定一个污染物母体分子，环境/微生物转化规则可能生成哪些一代产物？
```

它不回答：

```text
这个完整反应是否存在；
哪个酶催化这个反应；
该反应对应哪个 Rhea ID；
该反应对应哪个 EC；
候选酶在 EnzymeCAGE 里排第几；
产物是否一定是新污染物真实环境降解路径。
```

因此它在我们三段式路线中的位置应是：

```text
污染物 parent → 产物预测/路径候选生成
```

后续如果要找酶，还需要把预测出的 parent → product pair 再交给反应找酶/候选酶生成/EnzymeCAGE ranking 流程。不能把 BioTransformer 的产物预测结果直接解释为酶筛选结果。

## 2. 输入是什么

我们使用的是 single-parent 输入。

在 18 条小污染物 benchmark 中，输入表是：

```text
03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728/
```

blind 输入 CSV：

```text
POLLUTANT_DEGRADATION_STRICT_SINGLE_PARENT_BLIND_INPUTS_V0_1.csv
```

字段包括：

```text
benchmark_case_id
pollutant_name
pollutant_category
source_database
parent_comp_id
parent_url
parent_smiles
parent_canonical_smiles
parent_inchikey
case_policy
case_note
```

输入只给 parent SMILES，不给已知产物，不给 EAWAG-BBD reaction ID，不给答案表，不给 Rhea/EC/酶信息。

在命令层面，每个 case 取 `parent_smiles` 进入：

```text
-ismi <parent_smiles>
```

例如 Alachlor 的实际命令为：

```text
java -jar .../biotransformer-3.0.0.jar -k pred -b env -ismi CCc1cccc(CC)c1N(COC)C(=O)CCl -ocsv .../SPD-BBD-ala/vendor_output.csv -s 1
```

## 3. BioTransformer 内部使用哪个模块

工具身份：

```text
tool_id=biotransformer_envmicro
tool_display_name=BioTransformer 3.0 ENVMICRO
repository=https://github.com/Wishartlab-openscience/Biotransformer.git
commit=7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
jar_sha256=e5c3c27de7dfc87b448f1eed6fe986ef48ed90c53bad9b848f95378f08efee80
```

固定命令：

```text
java -jar <jar> -k pred -b env -ismi <parent_smiles> -ocsv <case_output_csv> -s 1
```

本轮只关心：

```text
-b env
```

也就是 environmental / microbial 转化模块。输出 CSV 里 `Biosystem` 字段也记录为：

```text
ENVMICRO
```

例如 raw vendor output 中多行显示：

```text
Enzyme(s)=Unspecified environmental bacterial enzyme
Biosystem=ENVMICRO
Reaction=EAWAG_RULE_...
Reaction ID=BTMR...
```

这些字段可以作为 BioTransformer 规则来源/模块 provenance 披露，但不能当作我们已经确定了真实催化酶。尤其 `Unspecified environmental bacterial enzyme` 不是可直接进入 EnzymeCAGE ranking 的 UniProt UID。

## 4. `-s 1` 在我们这里是什么意思

我们使用：

```text
-s 1
```

在本轮 benchmark 里，它被作为 one-step / first-generation product 预测使用。也就是：

```text
parent pollutant
→ predicted first-generation products
```

这与我们的 18 条小 benchmark 设计一致：答案表也是 EAWAG-BBD 来源的 direct first-generation product molecule(s)。

本轮没有让 BioTransformer 展开多步完整路径，因此不能说它已经完成了完整降解路径规划。它目前只作为“一代产物候选生成器”被测试。

## 5. 原始输出是什么

每个 case 产生一个 raw vendor CSV，例如：

```text
raw/cases/SPD-BBD-ala/vendor_output.csv
```

vendor CSV 包含的核心字段包括：

```text
InChI
InChIKey
SMILES
Reaction
Reaction ID
Enzyme(s)
Biosystem
Precursor SMILES
Precursor InChIKey
```

我们真正拿来做产物评分的是：

```text
SMILES
InChIKey
```

`Reaction`、`Reaction ID`、`Enzyme(s)`、`Biosystem` 只作为 BioTransformer 自身输出 provenance 记录，不作为真实酶证据。

## 6. adapter 怎么把 raw output 变成我们可评分的预测表

adapter 做了这些事：

1. 读取每个 case 的 `vendor_output.csv`；
2. 取每行 `SMILES`；
3. 用 RDKit 解析；
4. 生成 canonical SMILES 和 InChIKey；
5. 按 InChIKey / canonical SMILES 去重；
6. 按 vendor CSV 原始行顺序保留 rank；
7. 最多保留 Top-10；
8. 写入 normalized JSONL。

normalized prediction 的字段形如：

```json
{
  "case_id": "SPD-BBD-ala",
  "tool_id": "biotransformer_envmicro",
  "tool_display_name": "BioTransformer 3.0 ENVMICRO",
  "input_parent_smiles": "...",
  "case_status": "ok",
  "predictions": [
    {
      "rank": 1,
      "product_smiles_raw": "...",
      "product_smiles_canonical": "...",
      "product_inchikey": "...",
      "raw_score": null,
      "score_semantics": "absent",
      "rank_semantics": "vendor_csv_row_order_deduplicated_adapter_rank_not_native_confidence"
    }
  ]
}
```

这个 rank 的含义非常重要：

```text
rank 不是 BioTransformer 给出的概率或置信度。
rank 是 vendor CSV 行顺序经过 RDKit parse、去重、Top-10 截断后的 adapter rank。
raw_score=null，score_semantics=absent。
```

因此给老师解释时不能说“BioTransformer 第 1 名置信度最高多少分”。只能说“按工具输出顺序规范化后的 Top-K 产物候选”。

## 7. 每个底物预测产物数量是否固定

不固定。

18 条小污染物 benchmark 的 BioTransformer ENVMICRO 结果：

```text
case_count=18
ok_count=18
no_prediction_count=0
tool_error_count=0
raw_product_rows=80
normalized_prediction_count=72
min_predictions_per_case=1
max_predictions_per_case=10
mean_predictions_per_case=4.0
```

也就是说，工具对不同母体输出的产物数量不同。adapter 最多保留 Top-10；如果某个 case 原始输出超过 10 个，后续评分只看规范化后的前 10 个。

257 条 valid single-parent 技术测试中：

```text
ok=229
no_prediction=28
tool_error=0
raw_product_rows=1837
parse_pass_product_rows=1806
parse_fail_product_rows=31
deduplicated_top10_product_rows=1374
cases_with_gt10_products_before_cap=54
```

这进一步说明 BioTransformer ENVMICRO 的输出数量不是固定的，并且存在 RDKit parse 失败、重复产物和 Top-10 截断。

## 8. 怎么评分

HPC 端只生成预测，不读取 restricted answer key，不做评分。

证据：

```text
operator_or_executor_note=no answer key read; no scoring performed
forbidden_assets_accessed=false
return package did not contain restricted answer files
```

本地评分时才读取 restricted answer key：

```text
03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_degradation_strict_single_parent_benchmark_v0_1_20260728/restricted/POLLUTANT_DEGRADATION_STRICT_SINGLE_PARENT_RESTRICTED_ANSWER_KEY_V0_1.jsonl
```

评分逻辑：

```text
case-level：只要 Top-K 里任意预测产物命中该 parent 的任一 accepted first-generation product，就算该 case hit。
product-level：把 accepted first-generation product label 逐个计数，看 Top-K 覆盖了多少个 label。
```

18 条小污染物 benchmark 的 BioTransformer ENVMICRO 评分：

```text
case Hit@1  = 9/18  = 50.00%
case Hit@3  = 13/18 = 72.22%
case Hit@5  = 16/18 = 88.89%
case Hit@10 = 16/18 = 88.89%
MRR@10 = 0.6194

accepted_product_labels=39
product recall@1  = 9/39  = 23.08%
product recall@3  = 14/39 = 35.90%
product recall@5  = 19/39 = 48.72%
product recall@10 = 20/39 = 51.28%
```

解释：

```text
BioTransformer ENVMICRO 对“每个污染物至少找回一个已知一代产物”的能力较强；
但对多路径/多一代产物的完整覆盖仍然有限。
```

## 9. 目前结果怎么解读

BioTransformer ENVMICRO 在 EAWAG-BBD-derived 18 条 known-pathway pollutant degradation benchmark 上明显强于 enviFormer latest-current。

对比结果：

| metric | BioTransformer ENVMICRO | enviFormer latest-current |
|---|---:|---:|
| case Hit@10 | 16/18 = 88.89% | 1/18 = 5.56% |
| product recall@10 | 20/39 = 51.28% | 1/39 = 2.56% |
| mean predictions / case | 4.00 | 9.06 |

但必须保留边界：

```text
这个 benchmark 来自 EAWAG-BBD 已知污染物降解路径；
BioTransformer ENVMICRO 的环境规则/数据库 lineage 与 EAWAG-BBD 类知识可能有重叠；
因此这是 known-pathway pollutant benchmark performance，不是 unseen/new-pollutant generalization proof。
```

另外，BioTransformer 仍然没有完全恢复所有 known first-generation products：

```text
Pyrene：0/3 labels recovered
Toluene：0/5 labels recovered
多产物 case 往往只恢复其中一部分
```

所以它适合作为：

```text
污染物一代产物候选生成器；
已知路径/规则路径的优先工具；
后续反应找酶流程的上游输入来源之一。
```

但不应被描述为：

```text
完整降解路径数据库；
真实环境路径 oracle；
新污染物泛化能力已验证；
酶和 EC 自动确定工具。
```

## 10. 给老师的建议口径

可以这样回复：

```text
BioTransformer 这一路我们只使用 ENVMICRO/environmental microbial 模块，命令固定为 `java -jar ... -k pred -b env -ismi parent_smiles -ocsv output.csv -s 1`。没有使用人体代谢/CYP/Phase II 等模块，也没有使用全模块参数。

在我们流程里，它的输入是单个污染物 parent SMILES，输出是一批一代环境转化产物候选。每个底物输出数量不固定，adapter 用 RDKit 规范化、去重并最多保留 Top-10；rank 是 BioTransformer vendor CSV 行顺序经过 adapter 处理后的顺序，不是概率或置信度分数。

HPC 端只生成预测，不读取答案；本地再用 EAWAG-BBD-derived restricted answer key 评分。18 条 strict single-parent 小污染物 benchmark 上，BioTransformer ENVMICRO 达到 case Hit@10=16/18，product recall@10=20/39，明显强于 enviFormer latest-current。但这个结果只能说明 known-pathway pollutant benchmark 上表现较好，不能直接证明新污染物未见路径泛化。

后续建议把 BioTransformer ENVMICRO 作为上游一代产物候选生成器；若目标污染物已经在可靠数据库中有已知路径，优先做数据库检索/证据回源，再用预测工具补充可能产物；对数据库中没有的污染物，再把 ENVMICRO 预测产物作为候选进入后续反应找酶和 EnzymeCAGE ranking。
```

## 11. 证据文件

18 条小污染物 BioTransformer ENVMICRO 返回评分审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_SMALL_POLLUTANT_STRICT_V0_1_BIOTRANSFORMER_ENVMICRO_RETURN_SCORING_AUDIT_2026-07-29.md
```

18 条小污染物两工具对比审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_SMALL_POLLUTANT_STRICT_V0_1_TWO_TOOL_COMPARATIVE_SCORING_AUDIT_2026-07-29.md
```

257 条 valid single-parent BioTransformer ENVMICRO 返回审计：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/04_Local_Review_Audits/ENZYMECAGE_M3_P1_2_1_THREE_TOOL_VALID_SINGLE_PARENT_BIOTRANSFORMER_ENVMICRO_PREDICTION_R4_RETURN_LOCAL_AUDIT_2026-07-28.md
```

18 条小污染物 BioTransformer ENVMICRO 返回包：

```text
custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01/03_HPC_Returned_Result_Summaries/enzymecage_m3_p1_2_1_small_pollutant_strict_v0_1_biotransformer_envmicro_prediction_20260728.tar.gz
```

