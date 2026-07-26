# M3-P1-2.1B 三模型 RDKit 技术验证：HPC 返回本地审计

审计日期：2026-07-26（Asia/Shanghai）  
任务：`enzymecage_m3_p1_2_1b_three_model_rdkit_technical_validation_20260726`  
包版本：`m3-p1-2-1b-three-model-rdkit-validation-payload-v0.1`  
结论：**PASS — TECHNICAL VALIDATION COMPLETE; NOT TARGET-SCORED**

## 1. 本地收到的返回件

收到：

```text
03_HPC_Returned_Result_Summaries/
  enzymecage_m3_p1_2_1b_three_model_rdkit_technical_validation_20260726.tar.gz
  enzymecage_m3_p1_2_1b_three_model_rdkit_technical_validation_20260726.tar.gz.identity.txt
```

未收到同名 live return directory。

```text
archive SHA256:
  4ce4b3955856c8abe29d3dbb86f8892e228b65bffb71a1d5b63dc70627f03856
archive bytes:
  30237
identity SHA256:
  17df31abdcdcf4ccaff50418bb27de9c243edd41c2d7bf44cec79767d99d9626
transport status:
  ARCHIVE_AND_IDENTITY_PRESENT_EXTRACTED_DIRECTORY_MISSING
```

identity 中记录的 archive SHA256、bytes、成员数、manifest 和 final status
均已从 archive 独立重算并匹配。

## 2. Archive 安全和完整性

```text
tar members:
  36
regular files:
  29
directories:
  7
other member types:
  0
single root:
  PASS
duplicate / absolute / .. / backslash:
  absent
symlink / hardlink / device / FIFO / socket:
  absent
manifest entries:
  28
manifest SHA256:
  4921d9295792f721dc03f4a0b7af8429e4bc255ec9fcd3ac7b126c49dba9b884
fresh extraction manifest:
  28/28 PASS
```

跨主机重建的 tar/gzip 字节不完全相同，但 36 个成员的名称、类型、mode、size
和文件 SHA256 全部一致：

```text
semantic member equality:
  PASS
byte-identical cross-host tar reconstruction:
  NOT ESTABLISHED
```

这不影响收到的 archive 自身身份和内部完整性。

## 3. 冻结输入和代码身份

返回中的 policy、schema、用户三模型选择裁定、统一输入、三个模型原文、runner、
validator 和 orchestrator 均与本地冻结文件逐字节相同。

```text
policy SHA256:
  3058d621fe1e37d481b98839cd9c57d1c1b33170dfa9acf78abd82088cd4fb05
unified input SHA256:
  54861e7d7c4346fd4521d6dccfaea2e3fb4ae257c1c3631d4e7be60c3ef4cd3d
payload manifest SHA256:
  a51b24dec604167510bce683c414978136f2b56e2f6a8bfa35caee0a6e7b6588
runner SHA256:
  3cd636e2eb155935c62357f3708ac5a5cc7b3b73f79ed4ff8f6ea9d604d11dc6
validator SHA256:
  67ea051a85fed78bca44226ac52cd9d64133d3a25995c0e9c76f8c3f897b790b
orchestrator SHA256:
  a398538f917f4c65bd83cbd22fcea18f22125589318d495f1ae0a45079303dd9
```

三个原始来源：

```text
ChatGPT source SHA256:
  f50428618d245ecf1b41ecf1a84c452dd599a17cdc22ab2d3ea475e525e79600
DeepSeek source SHA256:
  669dfb8eb304e9c7646e20e40965b8a3652ac293dfe9b7fa058fe36176249192
Qwen source SHA256:
  b6cc9bcf315f8d209c60110bbc754e8864b5f063537f47ea9141270fc3de746f
```

模型/版本名称来自用户填写和原文标签，本任务没有平台 API attestation，因此
只能记为 `USER_SUPPLIED_LABEL_NOT_PLATFORM_VERIFIED`。

## 4. HPC 执行状态

```text
FINAL_STATUS:
  M3_P1_2_1B_THREE_MODEL_RDKIT_TECHNICAL_VALIDATION_READY_FOR_LOCAL_AUDIT
script exit:
  0
runner exit:
  0
independent validator exit:
  0
Python:
  3.12.3
RDKit:
  2026.03.3
device:
  CPU_ONLY
answer key:
  NOT_READ_OR_PARSED
target scoring:
  LOCKED_NOT_PERFORMED
final Route B adoption:
  NOT_APPROVED
```

关键返回文件：

```text
RDKit report SHA256:
  9efa4b2dffbbf5f437e434a02001e9001ea929fcbc7d901f39cce1128a92a069
independent report SHA256:
  f4a170eb28948a37132afa49c5fe71bddb82e797c6149b7b2dd796180d3af389
extracted bodies SHA256:
  08d9ebd2f49bfa2b7349b2bdf4a056f981a7ced73c81bc9ce1c789e49bdfcd5f
```

## 5. 三模型输入状态

```text
ChatGPT:
  24 predictions
  raw contract status = PASS

DeepSeek:
  9 predictions
  raw contract status = FAIL_INVALID_CASE_ERROR_MESSAGE_MISSING

Qwen:
  26 predictions
  raw contract status = WHOLE_FILE_PREFIX_FAIL_EMBEDDED_CONTRACT_PASS

Gemini:
  EXCLUDED_OUTPUT_CONTRACT_NONCOMPLIANT
```

DeepSeek 和 Qwen 的原始合同偏差没有被隐藏或改写。它们进入三模型技术验证是
用户在独立裁定中批准的评估 cohort；老师对 relaxed intake 的批准仍为
`NOT_RECORDED`。

## 6. RDKit 技术结果

总预测数：

```text
ChatGPT:
  24
DeepSeek:
  9
Qwen:
  26
total:
  59
```

按有效 case 聚合：

```text
RP-P01:
  11
RP-P02:
  8
RP-P03:
  9
RP-P04:
  11
RP-P05:
  9
RP-P06:
  11
```

技术检查：

```text
exactly one >> delimiter:
  59/59 PASS
nonempty reaction sides:
  59/59 PASS
all molecule components parse:
  59/59 PASS
RDKit reaction parse:
  59/59 PASS
literal substrate retained on left:
  59/59 PASS
canonical substrate retained on left:
  59/59 PASS
within-source/case exact duplicate groups:
  0
within-source/case canonical duplicate groups:
  0
invalid-input rejection:
  3/3 PASS
prediction fields modified:
  false
manual reaction repair:
  NOT_PERFORMED
```

这只证明 59 条输出在冻结技术合同下“能解析且保持输入底物”。所有 Route B
输出仍标记为：

```text
native_output_type:
  product_only
reaction_completeness:
  partial_unbalanced
confidence_semantics:
  self_reported_uncalibrated
```

因此不能由 `59/59 parse` 推导“59/59 化学正确”。

## 7. 独立复算和反向检查

本地使用同版本 `RDKit 2026.03.3` 再次运行返回的独立 validator：

```text
selected source identity:
  PASS_3_OF_3
deterministic extraction:
  PASS_3_OF_3
extracted bodies:
  EXACT_MATCH
per-prediction RDKit evidence:
  INDEPENDENT_RECOMPUTATION_MATCH
duplicate groups:
  INDEPENDENT_RECOMPUTATION_MATCH
validation report:
  BYTE_IDENTICAL_PASS
```

本地额外反向测试：

```text
mutate one reported reaction:
  PASS_REJECTED
mutate one raw source byte:
  PASS_REJECTED
change extracted target_scoring to PERFORMED:
  PASS_REJECTED
```

冻结 HPC 包本身没有单独返回 mutation-test 目录；上述三项是本地返回审计新增
检查，不应冒充 HPC 原始 mutation 结果。

## 8. 审计裁定

```text
transport:
  PASS_WITH_LIVE_DIRECTORY_NOT_RECEIVED
frozen source/package identity:
  PASS
HPC runtime gate:
  PASS
runner:
  PASS
independent validator:
  PASS
Route B technical parseability:
  PASS_59_OF_59
chemical correctness:
  NOT_EVALUATED
answer-key scoring:
  LOCKED_NOT_PERFORMED
teacher approval of relaxed intake:
  NOT_RECORDED
final Route B adoption:
  NOT_APPROVED
```

B 路已经完成本轮“答案钥匙解锁前技术验证”，不需要因 RDKit 解析问题重跑。
后续应等待 C-rerun2 正式返回也完成独立审计，再按统一盲评分合同决定何时解锁
答案钥匙；不得提前用目标答案筛选或修改 B 输出。
