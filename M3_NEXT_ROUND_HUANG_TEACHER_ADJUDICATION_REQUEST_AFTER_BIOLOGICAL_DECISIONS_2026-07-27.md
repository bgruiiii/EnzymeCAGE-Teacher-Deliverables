# M3 下一轮：生物学决定后黄老师确认与最小授权请求

日期：2026-07-27  
依据：

1. `TEACHER_REPLY_M3_TASKS_1_7_ACCEPTANCE_AND_TASK7_SCOPE_AND_SNAPSHOT_MTTQ02_2026-07-23(1).md`
2. `TEACHER_REPLY_M3_NEXT_ROUND_STUDENT_PREREQUISITES_SUPPLEMENT_2026-07-24(1).md`
3. 2026-07-27 生物学侧会议结论

状态：**BIOLOGICAL STRATEGY RECORDED / HUANG-TEACHER CONFIRMATION AND AUTHORIZATION PENDING**

## 1. 生物学侧已经确定的两项

### 1.1 D4 污水 Trait

选择 **T1：全部保留为 soft**。

```text
用途:
  用户参考
  候选菌使用建议
  解释信息
  uncertainty / manual-review 提示

禁止:
  自动删除候选菌
  hard rejection
  species/strain 相互继承
  把 evidence 不足写成生物学不存在
```

该选择确认黄老师既有 v1 保守口径，不申请 T2/T3 hard 升级。

### 1.2 反应预测

选择 **A-first 专业工具比较策略**：

1. 弓师兄正在开发的模型；
2. BioTransformer 3.0–ENVMICRO；
3. enviFormer。

三个工具先使用同一测试和评分合同，再增加能够披露训练暴露状态的外部泛化集，比较后
选择 A 路线内部工具。若三者均不满足最低合同，再考虑 C 路线自建数据库/规则资产。

当前准确边界：

```text
BioTransformer:
  已有旧小试；product-only，旧统一合同不兼容

enviFormer:
  论文身份已核对；项目侧技术验证进行中，尚无 benchmark 结论

弓师兄模型:
  尚待版本、入口、训练数据边界和输出合同交接

B route:
  不作为当前主路线；既有 LLM product-only 结果只保留为历史 baseline

C route:
  条件后备路线，尚未触发或建设
```

## 2. 请老师确认已收到/验收的既有交付

以下事项无需老师重新设计，只需确认：

```text
[ ] 07-22 RHEA:11880 裁定原件已按指定 SHA256 完成老师侧字节归档
[ ] Task 7 TraitValue schema + not_applicable 示例已验收
[ ] D5 07-24 新合同重审版已验收
[ ] 继续沿用 MT-D2 C 修订版：v1 不输出 organism_confidence float
[ ] D1-D3、D5-D8 既有裁定继续有效；D4 采用本轮 T1
[ ] MetaTraits 数据面和 ID 对齐属于完成后的负结果，production 继续 fail-closed
```

其中：

- Tasks 1–6 已于 2026-07-23 验收，不申请重做；
- Task 5/M3-EXT shortlist 已符合筛选边界，第二阶段仍待单独安排；
- 三案例真实 smoke 是导师侧已完成事项，不是学生欠项。

## 3. 请老师裁定的数据面与 ID 路径

### 3.1 DP：正式数据面到来前是否允许离线 candidate

```text
[ ] DP1（学生建议）
    允许 unversioned candidate 仅作隔离、可丢弃的离线解析器/validator/缓存小试；
    明标 offline_nonproduction；
    禁止命名为 official snapshot、禁止生产、禁止 hard filtering。

[ ] DP2
    严格等待 official versioned snapshot，正式数据到来前不建立 candidate。
```

### 3.2 ID：exact ID 不可用时 species summary 的处理

```text
[ ] ID1（与本轮 soft 决定一致，学生建议）
    species summary 只作 attribution_unresolved contextual soft evidence；
    可展示，不参与 hard rejection、trait_score、排序或过滤；
    不向 strain 继承，exact-ID 未命中仍返回 unknown。

[ ] ID2
    species summary 仅保留为 D5 调研证据，不进入候选菌报告。
```

## 4. 请老师裁定是否发送维护方询问信

```text
[ ] MQ1（学生建议）
    允许发送已验收的通用身份询问信；
    询问 official snapshot、稳定 API、NCBI/GTDB ID、rate limit、许可和版本政策。

[ ] MQ2
    暂不发送，继续保留草案。
```

MQ1 是外部动作，未勾选前不发送。

## 5. 请老师确认反应预测三工具正式比较范围

```text
[ ] RP1（学生建议）
    授权一次 A-first 三工具统一 benchmark：
      弓师兄模型
      BioTransformer 3.0–ENVMICRO
      enviFormer

    允许:
      冻结工具身份、依赖、训练数据边界和统一输入输出；
      在现有 6 例上做回归/兼容性测试；
      构造新的 locked external set；
      分别报告 CONFIRMED_UNSEEN / LIKELY_UNSEEN / EXPOSURE_UNKNOWN；
      统一做 RDKit、Top-K、失败模式、运行时间和 EnzymeCAGE 兼容性评估；
      生成 raw output、独立 validator、mutation tests 和审计。

    禁止:
      把现有 6 例再次称作新 blind set；
      把论文成绩当本项目实测；
      修改 production reaction_prediction_node；
      直接接入 EnzymeCAGE 生产链；
      在 A 未完成前自动启动 C 资产建设。

[ ] RP2
    只记录 A-first 生物学策略；不授权新的正式统一 benchmark。
```

enviFormer 已开始的安装/可调用性工作只记为技术验证，不冒充 RP1 的完整 benchmark。

## 6. 请老师裁定 M3-EXT

```text
[ ] MX1（学生建议）
    继续锁定；保留 shortlist，不补 D4、不改池、不跑模型。

[ ] MX2
    只开放 paraoxon 两个直接证据 UID 的 D4 构造可行性检查；
    不实际补资产、不改池、不跑模型。

[ ] MX3
    在 MX2 基础上增加 EC-null 外部证据发现 pilot；
    模型/智能体结果必须人工复核，不自动写入资产。
```

## 7. 请老师裁定 M4b / M4c

```text
[ ] IM1（学生建议）
    M4b、M4c 继续锁定。

[ ] IM2
    仅授权 M4b 最小启动包：
      Task 7 schema 转 Pydantic + 字段测试；
      仅在 offline_nonproduction candidate 上验证
      soft-only / unknown / not_applicable / provenance / uncertainty；
      禁止 hard rejection、真实候选菌排序、production 和 M4c。
```

即使选择 IM2，MicrobeSelectionAgent 完整形态和 M4c 仍不启动。

## 8. 本轮建议组合

```text
DP1:
  只允许离线 nonproduction 工程准备

ID1:
  species summary 只作 contextual soft evidence

MQ1:
  发送维护方询问以争取正式数据和 ID 路径

RP1:
  完成一次三工具统一 benchmark 后再择优

MX1:
  M3-EXT 暂不扩线

IM1:
  M4b/M4c 继续锁定
```

这些只是学生建议；未勾选的项不自动生效。

## 9. 老师回传区

```text
既有交付确认:
  [ ] 07-22 原件归档
  [ ] Task 7 验收
  [ ] D5 新合同版验收
  [ ] MT-D2 / D1-D8 延续确认

MetaTraits data plane:
  [ ] DP1
  [ ] DP2

ID policy:
  [ ] ID1
  [ ] ID2

Maintainer inquiry:
  [ ] MQ1
  [ ] MQ2

Reaction predictor:
  [ ] RP1
  [ ] RP2

M3-EXT:
  [ ] MX1
  [ ] MX2
  [ ] MX3

Implementation gate:
  [ ] IM1
  [ ] IM2
```

本卡不构成对任一工具、本项目反应预测能力、MetaTraits 真实世界完整性或生产可用性的
背书。所有被授权动作仍按“一次一个子任务、一个合同、一个独立审计”执行。

