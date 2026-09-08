# 给黄老师的09-08阶段回复

黄老师您好，您09-08的回复我们已收到并逐项落实。

## 1. T4正式18条输入身份回传

按您的裁定，我们已将本轮T4唯一候选身份定位为：08-04生成、08-07由您在A7/A8/A9审计中接受冻结的
`enzymecage_m3_p1_2_1_small_pollutant_gold_standard_schema_scoring_freeze_rerun1_20260804.tar.gz`。

该archive本地SHA256为：

```text
58feccb30056847acee41d2436263d770eea35a44d5d2d5a78e0ad20a06a3d3e
```

我们从包内冻结的blind parent表与cases表提取了18条：`case_id / parent_name / parent_smiles /
parent_smiles_rdkit_canonical`，见[`T4_FORMAL_18_PARENT_INPUTS.csv`](T4_FORMAL_18_PARENT_INPUTS.csv)。本次GitHub
包只含parent字段，不含reaction、product、accepted answer或其他gold衍生字段。请您核对回签；回签后我们将其
锁为T4唯一输入身份。

T4后续严格按您规定执行：只把parent输入发预测端；gold零接触模型；先冻结原始输出再评分；目标模型为
depending v3.2和ECLIPSE；BioTransformer/enviFormer沿用已录基线；评分固定使用已冻结脚本，报告
K=1/3/5/10、MRR@10和product recovery。

## 2. 三模块主线最新进度

09-07反馈之后，T2C/T2D/T3继续推进：

```text
T2整体 = PASS_WITH_LIMITATIONS_STAGED
G4预测接线门 = PASS_WITH_LIMITATIONS
T3A proxy轨 = PARTIAL_PASS_SELECTION_BLOCKED_RANKING
T3B真实资产轨 = PASS_WITH_LIMITATIONS_NATIVE_LOADER_3_OF_3
G5反应资产门 = PASS_WITH_LIMITATIONS_T3B
T5整体 = PASS_WITH_LIMITATIONS_STAGED_CONTRACT_ONLY
G6性状接线门 = PASS_WITH_LIMITATIONS_CONTRACT_TRACK
```

其中，T2已经从单SMILES adapter继续到predicted→candidate转换、多步route edge拆分、唯一
`reaction_task_id`和typed回挂；T3B三条staged新反应资产均由原生`load_geometric_dataset`真实加载，
dataset length及`ds[0]`均成功。T3A三条proxy选择成立，但0/3完成真实proxy EnzymeCAGE排名，因此仍只作为低等级
proxy边界证据。

T6当前仍在执行，尚未完成。执行端已报告固定输入SHA、T2D/T5C三方合并及真实LangGraph compile等中间证据，
但3B EnzymeCAGE forward在无GPU执行器上加载缓慢，6/6 forward、完整invoke/stream、TEST-01—20、mutation、
determinism、schema终验和archive三文件尚未闭合。该快照尚未取回做本地独立审计，因此当前必须写：

```text
T6 = IN_PROGRESS / EXECUTOR_CHECKPOINT_NOT_LOCALLY_AUDITED
G7 = NOT_PASSED
production merge = false
```

详细边界见[`CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md`](CURRENT_ENGINEERING_PROGRESS_AND_T6_CHECKPOINT.md)。

## 3. 智能体编排裁定确认

我们接受您§三的裁定：11个概念角色只作专利科学解读，不作为工程拆分依据。当前T6中按此前冻结合同形成的
13节点compile结果只保留为staged技术探索证据，不写成您已批准的最终拓扑，不进入production。后续不再自行
提出节点数量、节点拆并、总协调、错误恢复或持久化方案，只按您下发的节点契约实施。

目前尚未确认需要您修改的公共I/O字段。T6和后续节点契约接线中若出现真实字段缺口，我们会按您要求以
“字段名 / 出现场景 / 建议 / 最小复现样例”单独反馈，不用暂定拓扑问题冒充I/O缺口。

## 4. 下一步

```text
1. 等您回签本次18条parent-only清单和SHA，锁定T4输入身份；
2. 继续完成T6运行证据，但不把暂定拓扑写成老师批准，不merge production；
3. T6返回后先做本地独立审计，再报告G7是否通过；
4. T4回签后对depending v3.2和ECLIPSE执行盲隔离预测、冻结原始输出并按固定脚本评分；
5. 不重跑BioTransformer/enviFormer，不使用自建NON-BBD集合替代T4。
```
