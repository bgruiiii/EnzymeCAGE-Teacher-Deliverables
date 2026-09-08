# 给黄老师：T6-R2真实接线缺口、待裁定事项与学生侧并行工作

日期：2026-09-08

黄老师您好。我们按您09-02八项裁定继续执行T2/T3/T5/T6，并严格遵循您09-08对编排权的最新边界：没有新增、
删除或重排节点，没有为让测试变绿擅自改LangGraph；当前只把真实运行暴露的公共I/O和节点契约缺口反馈给您。

## 一、当前做到哪里

```text
T2：depending v3.2单SMILESadapter、多步route task和typed回挂已有staged证据；
T3A：3/3找到合格proxy，但0/3完成proxy真实EnzymeCAGE排名；
T3B：三条新反应资产已生成、原生loader加载并完成三GPU五seed真实forward；
T5：UID→source_signature→F1—F15和跨步骤聚合合同实现可运行；
T6-R1：3 reaction×2 UID×5 seed base/repeat真实forward通过；
T6-R2：真实StateGraph compile/invoke/stream执行，但在route_bridge断点停止；
20项本地纠正结果：15 PASS / 3 PARTIAL / 1 FAIL / 1 BLOCKED；
8条真实来源记录已组合，只有6/8通过统一schema；
G7仍未通过。
```

本次T6-R2返回archive：

```text
bytes=93195
SHA256=611f759cc0471cb7826ecffb0e4c0f4e735ecd340a2435cb54fc23ffad25b047
manifest=52/52 OK
status=T6_REMAINDER_EVIDENCE_COMPLETE_WITH_CONTRACT_GAPS
```

## 二、对照您09-02任务安排

| 老师任务 | 当前状态 | 尚未完成 |
|---|---|---|
| 任务0 源码/安全/环境冻结 | `PASS_WITH_LIMITATIONS` | 历史sidecar及最终部署身份继续留账；不在反馈中保留任何凭据 |
| 任务1 M3三案例复验 | 组件级`PASS_WITH_LIMITATIONS` | 当前T6真实图尚未完成B-primary/C-fallback/recall-failure三案例贯通 |
| 任务2 depending v3.2封装与接线 | adapter已通过；真实图接线未闭 | Torch环境缺LightGBM；predicted/candidate共享state漂移 |
| 任务3 新反应资产双轨 | T3B真实资产轨可用；T3A selection-only | proxy真实ranking仍未完成；T3B已足以支持当前技术验证 |
| 任务4 T4正式18条 | 已按09-08裁定回传A7/gold parent-only清单及SHA | 等您回签后才能运行depending v3.2＋ECLIPSE盲测 |
| 任务5 C8 adapter | adapter/15 trait slots/红线通过 | 当前图未到trait；宿主合法来源服务未闭，聚合覆盖0/3 |
| 任务6 测试 | 已真实执行并固定缺口 | 20项未全过；真实图未整链；schema仅6/8 |

## 三、真实图当前在哪里停止

nicotine已知反应检索真实得到10条`candidate_reactions`，随后：

```text
orchestrator
→ substrate
→ reaction（10 candidates）
→ route_bridge
→ fail_closed: no predicted route edges provided
```

因此没有到达enzyme_pool、EnzymeCAGE、organism mapping、aggregation、trait、explanation和synthesis。T6-R1的模型
forward仍是真实有效证据，但T6-R2的8条表是由真实T1/T6-R1/T5来源在task层组合，不是同一次图从头走到底。

## 四、请老师裁定/下发契约的五个缺口

### G1：已知检索反应与route bridge输入不兼容

```text
producer输出=candidate_reactions
route_bridge需要=predicted_route_edges
结果=已知反应检索成功后反而fail-closed
是否需要拓扑变化=true
```

请您在节点契约中规定已知lookup反应如何进入后续单步任务。学生侧不建议节点数量、不选择绕过/转换路线，等待您的
正式契约。

### G2：predicted/candidate共享state和ReactionTask版本漂移

真实测试出现：

```text
KeyError: predicted_reactions
KeyError: candidate_reactions
ReactionTask / ReactionTaskG producer-consumer shape不一致
```

请您确定生产公共字段名、对象版本及producer/consumer最小字段。我们建议至少保留既有
`source_tag/source_tool/model_version/raw_score/score_semantics/evidence_hash/depth/parent`信息；具体键名以您契约为准。

### G3：宿主来源证据服务不可用

`enzyme2organism`的`127.0.0.1:8001`当前关闭。UID map仍能找到微生物名称和source_signature，但没有合法
`UNIPROT_REVIEWED/KEGG_SUPPLEMENT/BACDIVE_OBSERVED`来源，8条全部`host_evidence_sources=UNRESOLVED`，聚合结果：

```text
covered_step_count=0
total_route_step_count=3
organism aggregates=[]
```

请您确认正式节点契约使用该服务，还是下发等价冻结host evidence数据源/字段。学生侧等待期间只做服务程序和后台
数据库只读定位，不自行用名称或TaxID替代reviewed provenance。

### G4：未解析宿主在统一schema中的表示

当前schema中hostEvidence允许`UNRESOLVED`，但organismAggregate的`host_evidence_source`不允许。请您裁定：

```text
未解析路线保持organism_aggregates=[]并单列unresolved ledger；
或允许显式UNRESOLVED organism aggregate。
```

学生侧不自行改enum。

### G5：M3 recall证据缺canonical reaction SMILES

T1-R2-R1摘要只带`query_reaction_sha256`，没有G-SCHEMA要求的`parent>>product`字符串，导致S1/S2 schema失败。
本地现已从冻结M3证据中精确恢复原字符串，并用UTF-8原字符串重新计算SHA，2/2与既有记录一致：

```text
S1 / RHEA 11532
NCC(=O)O.O.O=O>>N.O=CC(=O)O.OO
SHA256=19fe5b26e16a1a8ca60628be8718d3162cabded0299e2276a8503aec787bcf15

S2 / RHEA 46976
CN1CCC[C@H]1c1ccc(O)nc1.O=O>>CN1CCC=C1c1ccc(O)nc1.OO
SHA256=9737dd8c994296811f87278e33cc7c8b1743112ddf9ecb745ba6de1e1dc2971a
```

因此G5的数据定位问题已经关闭，当前只剩公共I/O合同问题。请您确认正式M3输出是否必须同时携带
`reaction_smiles`和`reaction_sha256`；学生侧不自行改变正式输出合同。

机器可读缺口表见`T6_R2_PUBLIC_IO_FIELD_GAPS_FOR_TEACHER.csv`；恢复来源与2/2重算见
`T6_G5_REACTION_FIELD_RECOVERY_NOTE.md`和`T6_G5_REACTION_SHA_TO_CANONICAL_SMILES_RECOVERY.csv`。

## 五、当前另有一个纯工程环境问题

```text
enzymecage_py312：有Torch/EnzymeCAGE，无LightGBM；
T2B v3.2环境：有LightGBM，无Torch。
```

所以TEST-01被BLOCKED。若您的节点契约要求同进程，我们将准备受控统一环境；若节点契约规定跨进程/服务调用，我们
按其实现。等待期间只做依赖版本、wheel和兼容性预检，不提前选择部署边界。

## 六、等待老师裁定期间学生继续做什么

我们不会停工，也不会越权改图。可以并行完成：

```text
1. 只读定位enzyme2organism服务程序、后台数据库和冻结身份；
2. 核Torch/LightGBM兼容版本与可复现安装材料，不决定节点部署方式；
3. M3 reaction SHA→canonical parent>>product对应表已2/2恢复；等待期间在晨羽交叉核其archive/member身份；
4. 区分已被ReactionTaskG正式替代的旧测试与仍有效测试，保留替代断言证据；
5. 修复测试执行时失效的/tmp G-SCHEMA路径，改为task-local冻结输入，不改production；
6. 补收T6-R1/R2缺失的identity/validation sidecar；
7. 继续完成SCNET/微生物预测性状数据，但不在验证完成前并入C8 base；
8. 等您回签T4输入后按指定模型和固定评分脚本运行，不提前读取gold。
```

上述准备完成后，待您的节点契约和G2/G4/G5公共字段裁定到位，我们只需做一次定向T6-R3，不重跑已经通过的T6-R1
三GPU五seedforward。

## 七、我们没有自行裁定的事项

```text
没有决定已知lookup是否绕过route bridge；
没有决定candidate_reactions和predicted_route_edges如何合并；
没有新建/拆分/合并节点；
没有改变route_aggregation/trait/explanation顺序；
没有修改UNRESOLVED schema enum；
没有以UID map名称字段冒充reviewed host evidence；
没有把15/20写成20/20；
没有把6/8 schema写成8/8；
没有写G7通过。
```

请您优先下发：G1对应节点契约、G2公共state对象、G4 unresolved聚合表示，并确认G3 host evidence来源和G5
reaction_smiles字段。我们收到后按契约继续，不另行提出拓扑方案。
