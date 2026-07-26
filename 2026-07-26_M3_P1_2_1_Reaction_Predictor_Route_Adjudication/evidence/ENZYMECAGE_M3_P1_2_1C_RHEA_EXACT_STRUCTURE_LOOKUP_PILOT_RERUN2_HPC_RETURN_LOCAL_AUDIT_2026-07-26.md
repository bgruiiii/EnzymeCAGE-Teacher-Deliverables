# M3-P1-2.1C Rhea 严格结构查表 Rerun 2：HPC 返回本地审计

审计日期：2026-07-26（Asia/Shanghai）  
任务：`enzymecage_m3_p1_2_1c_rhea_exact_structure_lookup_pilot_rerun2_20260726`  
包版本：`m3-p1-2-1c-rhea-exact-pilot-payload-v0.3-rerun2`  
结论：**PASS — C-EXACT RAW PILOT TECHNICALLY COMPLETE; NOT TARGET-SCORED**

## 1. 本地收到的返回件

收到：

```text
03_HPC_Returned_Result_Summaries/
  enzymecage_m3_p1_2_1c_rhea_exact_structure_lookup_pilot_rerun2_20260726.tar.gz
  enzymecage_m3_p1_2_1c_rhea_exact_structure_lookup_pilot_rerun2_20260726.tar.gz.identity.txt
```

未收到同名 live return directory。

```text
archive SHA256:
  2998bee8b101c20a34872ef2ac8450629d72b46e756cbb0e3da6c515654dffba
archive bytes:
  38478
identity SHA256:
  19e3bfedba773fbcd8f127f56354a0379b46033404d115c4455c8028919d6113
transport status:
  ARCHIVE_AND_IDENTITY_PRESENT_EXTRACTED_DIRECTORY_MISSING
```

identity 中的 archive SHA256、bytes、成员数、manifest 和 final status 已从
archive 独立重算并匹配。

## 2. Archive 安全和内部完整性

```text
tar members:
  85
regular files:
  71
directories:
  14
other member types:
  0
single root:
  PASS
duplicate / absolute / .. / backslash:
  absent
symlink / hardlink / device / FIFO / socket:
  absent
manifest entries:
  70
manifest SHA256:
  f9935ec0d9e56427122e09960ff1630c70ecebfef69055ac0515383a6bc343f0
fresh extraction manifest:
  70/70 PASS
final status SHA256:
  6f6e907260ed123ab3a5ae0d514360fdf3d3c342342962625b37359f70c6929c
```

跨主机重建的 tar/gzip 字节不完全相同，但 85 个成员的名称、类型、mode、size
和文件 SHA256 全部一致：

```text
semantic member reconstruction:
  PASS
byte-identical cross-host reconstruction:
  NOT ESTABLISHED
```

这不影响收到的 archive 自身身份和内部完整性。

## 3. 冻结包和资产身份

返回中的 policy、统一输入、输出 schema、runner、两个 validator、两个 mutator
和 orchestrator 均与本地冻结包逐字节相同。

```text
policy SHA256:
  71d76553efbffc53152d8137f77d366eda2604979fb23e548fa9bbb66f7affe6
payload manifest SHA256:
  361c2f61266990acd6f14326eda6adde45a9c411bedbc2b6b64b9bd69e6edd70
input SHA256:
  54861e7d7c4346fd4521d6dccfaea2e3fb4ae257c1c3631d4e7be60c3ef4cd3d
base runner SHA256:
  22a373d8444ba3d22d37249cb13f3915a9086766495b37306bc99efdefdb5005
rerun2 runner wrapper SHA256:
  438dc3f35262659d8447562ac0a9aeea54ff0729e3ff8bd9696df344e71d359f
base validator SHA256:
  b891a992ec4dbccd5970e0b7321e4c1670f0135921c941113530ac79b04fd37a
rerun2 validator SHA256:
  22ec0d65f69c2ca416bb56b52f4a15b757406fbe54b00303773cfd121a3a11fe
orchestrator SHA256:
  c8eac3ef4a1efacbc1a2d5d5ded5b5d40080e96bf7ed2ce3f9595d85445ee2e0
Rhea installed asset manifest SHA256:
  bb9d3180e07bdc2c66cbb1cdfe5cd4b9c43c17a91e8f869025d3471f7af4034b
```

HPC 环境：

```text
Python:
  3.12.3
RDKit:
  2026.03.3
device:
  CPU_ONLY
network policy:
  NO_NETWORK_COMMANDS_COMMON_PROXY_EGRESS_FAIL_CLOSED
```

## 4. HPC 执行状态

```text
FINAL_STATUS:
  M3_P1_2_1C_RHEA_EXACT_RERUN2_RAW_PILOT_READY_FOR_LOCAL_AUDIT
script exit:
  0
runner exit:
  0
independent validator exit:
  0
route:
  C-exact
C-generic:
  NOT_READY
answer key:
  NOT_READ_OR_PARSED
target scoring:
  LOCKED_NOT_PERFORMED
```

关键结果哈希：

```text
predicted reactions SHA256:
  4980a9b7ebcfe7bad8f34cfee118fc8a7af7d38941d0dacad569c7b84ae580f1
all exact hits SHA256:
  2f9078abab9a016c87c14938417a6be334f58c1839eec86654cee9ce8aeeb79c
scan summary SHA256:
  d8426cd343dbb5c68efbab46bed4a6f207f505e40aebb6c19b82e14be9e7c02c
exclusion evidence SHA256:
  17d6e08195a17445faa96595bc5eac51e838df6aedaf0d3eec00da3f89b6eef8
independent validation report SHA256:
  d10cdfbf5daa687c73269c08cd82831c788d67d42f24ee06b5054ca1db0967b4
mutation table SHA256:
  eac42c5095e208d450ec7caa59b46d747363e7c3d7628dbce9f7167065c80fd8
```

## 5. 两条预注册排除的核验

原始资产：

```text
Rhea reaction SHA256:
  34f7fb5eff7d230c2d0243b2a669b236b075a35ffda76ebe0137b0f5dd374e02
original rows:
  36014
```

排除 1：

```text
line:
  5561
ID:
  RHEA:22077
including-LF line SHA256:
  3b43af668cf4f07f5ec60df8be65b6fa1411f75d016163e69a967418fb4a5cb4
expected/observed:
  right molecule failed RDKit parsing
failed side:
  right only
candidate generation:
  PROHIBITED_AND_NOT_PERFORMED
```

排除 2：

```text
line:
  5562
ID:
  RHEA:22078
including-LF line SHA256:
  dd22c34cb632afbec18a9edf530959d5eff391476c5f48f4e27c098f547a1543
expected/observed:
  left molecule failed RDKit parsing
failed side:
  left only
candidate generation:
  PROHIBITED_AND_NOT_PERFORMED
```

派生搜索视图：

```text
excluded rows:
  2
searchable rows:
  36012
SHA256:
  fe0a21d3dd602d5332b6d065be6f9a440b1f1e25ec7e35f2ad5edbd801f3ade7
all other parse/integrity errors:
  FAIL_CLOSED
```

runner 和独立 validator 分别从原始 Rhea 文件重建搜索视图；两者哈希一致。
不存在第三条静默排除。

## 6. 正式 C-exact 结果

扫描：

```text
searchable Rhea rows scanned:
  36012
Rhea direction records:
  55029
asset errors:
  0
valid inputs:
  6
invalid inputs:
  1
all exact hits:
  12
```

按 case：

```text
RP-P01:
  1 hit — RHEA:18054
RP-P02:
  1 hit — RHEA:62381
RP-P03:
  1 hit — RHEA:11313
RP-P04:
  1 hit — RHEA:25186
RP-P05:
  5 hits — RHEA:10282, RHEA:20946, RHEA:27903, RHEA:36268, RHEA:36272
RP-P06:
  3 hits — RHEA:46509, RHEA:52886, RHEA:52894
RP-N01:
  rejected_invalid_input; 0 hits
```

因此 C-exact 在 6 个有效 pilot 输入上均有至少一个严格结构查表候选：

```text
valid-input lookup coverage:
  6/6
total returned predictions:
  12
```

## 7. 独立 validator

HPC 独立复算：

```text
original Rhea rows verified:
  36014
excluded rows verified:
  2
searchable rows recomputed:
  36012
exclusion policy:
  PASS_EXACTLY_RHEA_22077_AND_RHEA_22078
prediction count:
  12
reaction parse:
  12/12 PASS
molecule parse:
  12/12 PASS
substrate retention:
  12/12 PASS
atom balance:
  12/12 PASS
formal charge balance:
  12/12 PASS
```

本地用冻结原始 Rhea 和相同 `RDKit 2026.03.3` 再次运行独立 validator：

```text
derived search view SHA256:
  exact match
independent validation report:
  BYTE_IDENTICAL_PASS
```

## 8. Mutation tests

HPC 返回：

```text
confidence:
  PASS_REJECTED
reaction:
  PASS_REJECTED
invalid_status:
  PASS_REJECTED
provenance:
  PASS_REJECTED
raw_hit_drop:
  PASS_REJECTED
unregistered_rhea_parse_error:
  PASS_REJECTED
```

本地逐项重放 5 个输出 mutation，均以对应原因被 validator 拒绝。第六项重新制造
第三条未登记 Rhea 错误：

```text
error:
  reaction line 1 RHEA:10001: ReactionFromSmarts error: ValueError
asset_error_count:
  1
runner exit:
  nonzero
formal prediction/raw-hit output:
  NOT_PRODUCED
verdict:
  PASS_REJECTED_REPLAY
```

因此 `6/6 PASS_REJECTED` 已经由本地重放确认，不是只信任返回表格。

## 9. 审计裁定

```text
transport:
  PASS_WITH_LIVE_DIRECTORY_NOT_RECEIVED
frozen package identity:
  PASS
Rhea asset identity:
  PASS
two-record exclusion policy:
  PASS
formal runner:
  PASS
independent validator:
  PASS
mutation tests:
  PASS_6_OF_6
C-exact valid-input lookup coverage:
  6_OF_6
formal raw predictions:
  12
chemical/structural technical checks:
  PASS_12_OF_12
target correctness:
  NOT_EVALUATED
answer-key scoring:
  LOCKED_NOT_PERFORMED
C-generic:
  NOT_READY
final Route C adoption:
  NOT APPROVED
```

这次已经不是 rerun1 的 incomplete；C-exact 原始 pilot 在批准的两条排除合同下
正式运行并通过独立技术审计。但 `6/6 coverage` 和 `12/12 technical PASS` 不能
冒充答案准确率。下一步只能在 A、B、C 原始输出均冻结并完成各自审计后，按统一
合同决定是否解锁答案钥匙和执行盲评分。
