# M3-P1-2.1A Route A BioTransformer EnvMicro Rerun 1 v0.5 返回本地独立审计

审计日期：2026-07-24（Asia/Shanghai）  
审计对象：HPC rerun 1 v0.5 archive 与 identity  
审计方式：只读本地解包与字段级核验  
答案钥匙：**未查看、未解析、未用于评分；仅做既有合同清单的 hash 校验**  
结论：**RAW EXECUTION PASS / UNIFIED CONTRACT INCOMPATIBLE / NOT SCORED**

## 1. 审计边界

本审计回答：

1. 返回身份和内部文件是否自洽；
2. 冻结输入、脚本、源码 commit、CLI 和执行环境是否符合 v0.5 预注册；
3. 7 个 case 的原厂执行、字段、重复与多产品关系是什么；
4. 返回能否在不编造字段的前提下进入统一合同；
5. 还有哪些验证必须保持为 pending。

本审计不：

- 修改原始 archive、identity 或 CSV；
- 补造标准化 JSON；
- 查看、解析或使用 `UNIFIED_PILOT_ANSWER_KEY.json` 的答案内容；
- 做 Top-1/3/5、Rhea、EC 或酶池恢复评分；
- 选择 A/B/C 最终路线；
- 把原厂运行成功写成科学正确或老师验收。

审计使用临时目录解包。项目目录中没有创建或伪造 HPC 原始 return directory。

## 2. 审计对象

```text
archive:
  03_HPC_Returned_Result_Summaries/
  enzymecage_m3_p1_2_1a_biotransformer_envimicro_one_step_pilot_rerun1_20260724.tar.gz
archive SHA256:
  48f8253b3526dbfed99d731fcc40326361fc6f10fdd7133a84181c27fddc2b8a
archive bytes:
  31783

identity:
  03_HPC_Returned_Result_Summaries/
  enzymecage_m3_p1_2_1a_biotransformer_envimicro_one_step_pilot_rerun1_20260724.tar.gz.identity.txt
identity SHA256:
  3deeba6f37d7b2000204a340a7d0d14e20d19e0ce4c51677f28bb5a0d5170c7e
```

本地目录顶层只有 archive 与 identity，同名解包目录缺失：

```text
transport completeness:
  2/3
archive:
  present
identity:
  present
original returned directory:
  missing
```

这是运输偏差，不影响 archive 内部只读审计；但不得写成三件套完整。

## 3. Archive 安全和身份核验

| 检查 | identity | 实测 | 结果 |
|---|---:|---:|---|
| SHA256 | `48f825...c2b8a` | 一致 | PASS |
| bytes | 31783 | 31783 | PASS |
| tar members | 82 | 82 | PASS |
| regular files | 69 | 69 | PASS |
| regular-file bytes | 138125 | 138125 | PASS |
| manifest entries | 68 | 68 | PASS |
| manifest SHA256 | `e314b8...62417e` | 一致 | PASS |
| final-status SHA256 | `92bc6a...784e5` | 一致 | PASS |
| single root | rerun task ID | 一致 | PASS |
| owner/group | 0/0 | 0/0 | PASS |
| member mtime | 0 | 0 | PASS |
| lexical order | yes | yes | PASS |

安全成员审计：

```text
absolute paths: 0
parent traversal: 0
symlinks: 0
hardlinks: 0
devices/FIFO/socket: 0
multiple roots: 0
unexpected member types: 0
```

gzip header 为 method 8、flags 0、mtime 0、XFL 2；与确定性 `gzip -n -9`
声明相容。内部 `MANIFEST.sha256` 独立复核为 `68/68 PASS`。

裁定：

```text
archive safety and internal integrity:
  PASS
transport:
  INCOMPLETE 2/3 (ARCHIVE AUDITABLE)
```

## 4. 输入与脚本身份

冻结输入：

```text
returned UNIFIED_PILOT_INPUTS.json:
  54861e7d7c4346fd4521d6dccfaea2e3fb4ae257c1c3631d4e7be60c3ef4cd3d
local frozen UNIFIED_PILOT_INPUTS.json:
  54861e7d7c4346fd4521d6dccfaea2e3fb4ae257c1c3631d4e7be60c3ef4cd3d
byte comparison:
  PASS
```

输入 payload：

```text
returned declaration:
  35a7f0e817da8f9f27e83b1a2d9c317a288102defdb30a3ecadc52faf8cff2a8
local payload:
  35a7f0e817da8f9f27e83b1a2d9c317a288102defdb30a3ecadc52faf8cff2a8
payload bytes:
  5023
```

脚本：

```text
returned script:
  714e33ae234a5a3d65c0ed9f22556663094c24fe7244595d970e4bc9fa2d7224
v0.5 payload script:
  714e33ae234a5a3d65c0ed9f22556663094c24fe7244595d970e4bc9fa2d7224
byte identity:
  PASS
```

archive 不含 answer key；本审计没有查看或解析本地 answer key 内容。完整合同
资产自查中，`sha256sum -c` 只按既有 manifest 读取文件并比对 hash，没有输出
或解释答案内容。

## 5. 源码、后端和构建

```text
repository:
  https://github.com/Wishartlab-openscience/Biotransformer.git
requested commit:
  7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
actual commit:
  7149f7ec6b2f32f9f789bab53aa4a71db49e59e2
mapping:
  env -> bType.ENV -> EnvMicroBTransformer
JAR SHA256:
  dcd19b849a5be49a148a7e12e9d25c606bd2162629b35ced594c5f4c88085954
```

构建环境与结果：

```text
OpenJDK:
  1.8.0_492
javac:
  1.8.0_492
Maven:
  3.8.7
build exit:
  0
build wall:
  55.07 s
build max RSS:
  1024028 KiB
vendor tests:
  9 run / 0 failures / 0 errors / 0 skipped
```

`git status` 构建前为空，构建后只有生成的 JAR 与 `target/`，没有记录源码修改。

构建 warning 不可忽略：

- 多个 `*-SNAPSHOT` metadata 请求涉及 Maven HTTP blocker/cached metadata；
- deprecated/unchecked API；
- assembly destination 替换和非确定性警告；
- stderr 两条 `Maybe RingTemplateError`。

这些 warning 没有导致本次失败；但固定源码 commit 没有完全固定 Maven SNAPSHOT
依赖。JAR hash 固定了本次二进制身份，返回包没有携带 JAR 本体，故未来 rebuild
仍须重新比较 hash。

裁定：

```text
source/CLI identity:
  PASS
this-run build and vendor tests:
  PASS
full dependency reproducibility:
  PARTIAL / NOT PROVEN
```

## 6. 运行结果逐 case 核验

| case | exit | CSV | rows | Reaction ID groups | unique products | wall | max RSS KiB |
|---|---:|---|---:|---:|---:|---:|---:|
| RP-P01 | 0 | yes | 5 | 4 | 5 | 1.14 s | 194124 |
| RP-P02 | 0 | yes | 2 | 1 | 2 | 1.14 s | 187892 |
| RP-P03 | 0 | yes | 6 | 3 | 6 | 1.12 s | 197112 |
| RP-P04 | 0 | yes | 2 | 2 | 2 | 1.09 s | 177820 |
| RP-P05 | 0 | yes | 6 | 2 | 4 | 1.27 s | 197652 |
| RP-P06 | 0 | yes | 5 | 4 | 5 | 1.15 s | 186772 |
| RP-N01 | 1 | no | 0 | 0 | 0 | 0.18 s | 42408 |

`RUN_SUMMARY.tsv`、各 case 的 `exit_code.txt`、CSV 存在性和 GNU time exit
status 交叉一致。

有效 case：

```text
exit=0:
  6/6
CSV present:
  6/6
stderr empty:
  6/6
total product rows:
  26
unique products within case:
  24
Reaction ID groups:
  16
```

非法 case：

```text
exit=1:
  yes
CSV absent:
  yes
exception:
  org.openscience.cdk.exception.InvalidSmilesException
reason:
  Unclosed ring detected
```

## 7. CSV 字段和产品关系

六个 CSV 都有相同 23 列。26/26 行以下字段非空：

```text
InChI
InChIKey
SMILES
Molecular formula
Major Isotope Mass
ALogP
Metabolite ID
Reaction
Reaction ID
Enzyme(s)
Biosystem
Precursor SMILES
Precursor InChI
Precursor InChIKey
```

26/26 行：

```text
Biosystem:
  ENVMICRO
Enzyme(s):
  Unspecified environmental bacterial enzyme
Precursor SMILES equals corresponding frozen input:
  yes
```

原厂可选注释 `Synonyms`、`PUBCHEM_CID` 与 `Precursor ID` 在全部行为空；本次
没有使用 PubChem annotation，符合预注册。

Reaction ID 分组大小：

```text
RP-P01:
  BTMR0654=1, BTMR0683=1, BTMR0716=1, BTMR0724=2
RP-P02:
  BTMR0892=2
RP-P03:
  BTMR0671=1, BTMR0699=4, BTMR0917=1
RP-P04:
  BTMR0662=1, BTMR0671=1
RP-P05:
  BTMR0699=3, BTMR0777=3
RP-P06:
  BTMR0654=2, BTMR0683=1, BTMR0716=1, BTMR0825=1
```

RP-P05 的两个产品分别在两个 Reaction ID 下各出现一次，故 6 行只有 4 个唯一
产品。这证明：

- CSV 是产品行表，不是“一行必等于一条完整生化反应”；
- 同一 Reaction ID 可以有多个共同产品；
- 不同 Reaction ID 也可以输出相同产品；
- 不能按行直接构造独立反应、rank 或 Top-K。

## 8. 统一合同逐项裁定

| 合同要求 | 返回证据 | 裁定 |
|---|---|---|
| 同一冻结输入 | 输入 hash 与内容一致 | PASS |
| 6 个有效输入执行 | 6/6 exit 0 + CSV | PASS |
| 非法输入 fail-closed | vendor/CDK exit 1，无 CSV | EFFECTIVE PASS |
| 调 vendor 前 RDKit 前验 | 脚本直接调用 vendor | NOT IMPLEMENTED |
| 最多 Top-5 | 尚未定义产品行/Reaction ID 聚合与合法排序 | NOT ESTABLISHED |
| 完整 `reactants>>products` | 只有 precursor 与 product rows | NOT PRODUCED |
| RDKit reaction/molecule parse | 本地无 RDKit；HPC 未记录 RDKit | NOT VERIFIED |
| 输入底物在左侧 | 未产生 reaction_smiles | NOT APPLICABLE YET |
| `[0,1]` confidence | CSV 无 score/confidence | NOT PRODUCED |
| confidence 语义 | 内部阈值/ratio 不可替代导出值 | INCOMPATIBLE |
| provenance | commit、后端、规则 ID、环境可追溯 | RAW-LEVEL PASS |
| 不秘密补参与物 | 未做适配或人工补齐 | PASS |
| 标准 schema JSON | 没有生成，且不得伪造 | NOT PRODUCED |

原厂 CSV 无 `Score`、`confidence`、`probability` 或完整 reaction-SMILES 列。
源码记录：

```text
CLI default score threshold:
  0.5
distinct EAWAG occurrence ratios:
  301 entries, all 0.5
CSV Score-property export search:
  empty
```

以上信息能解释原厂内部筛选，不能证明每个返回候选具备可导出的校准概率。不得用：

```text
0.5 threshold
0.5 rule occurrence ratio
CSV row order
Reaction ID order
人工 rank
```

伪造统一 `confidence`。

当前若未来做 product-only adapter，也只能写：

```text
native_output_type:
  product_only
reaction_completeness:
  partial_unbalanced
```

并且必须先解决同一 Reaction ID 多产品聚合、重复产品、合法 Top-5 排序和
confidence 来源。当前不得补水、氧、辅因子、质子或其他模型未输出物。

## 9. RDKit 与科学评分状态

本机系统 Python、项目 `.venv-rhea-clean` 和现有 micromamba base 均没有可用
RDKit；HPC 返回环境也没有记录 RDKit 前验或后验。

因此：

```text
RDKit input parsing:
  NOT RUN
RDKit product parsing:
  NOT RUN
RDKit reaction parsing:
  NOT RUN
atom/charge audit:
  NOT RUN
```

原厂为产品生成了 InChI/InChIKey，是 CDK/InChI 侧证据，不等价于合同指定的
RDKit PASS。

答案钥匙保持封存。以下全部未评分：

```text
Top-1 target recovery
Top-3 target recovery
Top-5 target recovery
direction correctness
Rhea recovery
EC recovery
enzyme candidate-pool recovery
```

## 10. 许可证审计

返回包携带：

```text
BioTransformer LICENSE.md
BioTransformer README.md
ENVMICRO CC BY-NC-SA 4.0 license
ENVMICRO 10-file SHA256 list
```

软件材料对 LGPL 2.1/3 的描述不完全一致；ENVMICRO 明确带有
Attribution-NonCommercial-ShareAlike 条件。本次研究小试不能被外推为商业部署
或结果再分发许可已经解决。

## 11. 独立裁定

```text
return archive integrity:
  PASS
transport:
  INCOMPLETE 2/3 (ARCHIVE AUDITABLE)
fixed input/script/source identity:
  PASS
BioTransformer build/tests:
  PASS
valid vendor executions:
  PASS 6/6
invalid vendor rejection:
  PASS 1/1
raw product candidates:
  PRODUCED (26 rows / 24 unique products / 16 reaction groups)
full reaction output:
  NOT PRODUCED
confidence:
  CONTRACT INCOMPATIBLE
Top-5:
  NOT ESTABLISHED
RDKit:
  PENDING
target scoring:
  LOCKED / NOT SCORED
route selection:
  NOT MADE
```

最终结论：

> v0.5 rerun 修复了 v0.4 的 GitHub clone 阻塞，并证明 Route A 可以对本组真实
> 底物产生环境微生物 product-only 原始候选。但它没有满足统一接口最关键的
> confidence、完整 reaction SMILES、Top-K 与 RDKit 验证要求。当前只能进入
> “原始候选可供后续比较”的状态，不能宣布 Route A 合同通过或科学命中。
