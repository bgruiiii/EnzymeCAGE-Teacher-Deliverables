# 黄老师要求逐项对照矩阵

| 要求 | 来源 | 状态 | 证据/说明 |
|---|---|---|---|
| 指定路线为主实验 | 09-26 §一 | PASS | 121题均绑定指定route scope |
| cycle/矛盾case进quarantine | 09-26 §三 | PASS | 正式case SHA绑定G1 formal 121，quarantine未混入 |
| 搜索输入条件对称 | 09-26 §四 | PASS | 四模型统一search=false，不宣称联网能力 |
| observed-gold traits分母 | 09-26 §五、G3 D1 | PASS | 冻结mask/scorer SHA与老师回签一致 |
| smoke全过再pilot | 09-26 §六 | PARTIAL | 最终GLM-low独立smoke3/3；非单轮统一四模型smoke |
| pilot有效率≥98% | 09-26 §六 | DEVIATION | 统一四模型37/40；后续模型定向诊断不能替代统一pilot |
| pilot截断≤10% | 09-26 §六 | PASS | 统一pilot length/empty 3/40≤4/40 |
| pilot后预算老师确认 | 09-26 §六/§八 | DEVIATION | 用户批准分阶段硬顶，老师未逐字批准金额 |
| 每模型2题人工形态审阅 | 09-26 §六 | PASS_POST_HOC | 正式8份固定seed，用户人工8/8 PASS；时点在全量后 |
| smoke/pilot不进正式评分 | 09-26 §六 | PASS | 正式484全部独立请求，探针/pilot抵扣0 |
| 步骤对齐先冻结 | 09-26 §七、G3 D3 | PASS | Jaccard0.5、方向、tie-break均冻结 |
| 证据lookup独立轴 | 09-26 §七、G3 D4 | PASS | verified/unverified/hallucination独立报告 |
| SMILES同版RDKit | 09-26 §七、G3 D6 | PASS | RDKit 2026.03.5，isomeric主口径 |
| 一次回答、失败不补问 | 09-26 §八.1 | PASS | 484 committed、0正式retry、15非可用保留分母 |
| 评分器先冻结+三mock | 09-26 §八.2 | PASS | scorer SHA冻结；162/162；100/0/77.36 |
| 题面泄漏检查+人工抽审 | 09-26 §八.3、G2回签 | PASS | G2 PASS、13题老师侧材料已回签 |
| 记录版本/fingerprint | 09-26 §八.4 | PASS_WITH_LIMITATION | Kimi 5 fingerprint分层；其余网关NOT_EXPOSED |
| case_id隔离gold | 09-26 §八.6 | PASS | 484唯一键case_id+model，121 case集合一致 |
| JSON解析与schema分列 | 09-26 §八.7 | PASS | syntax/form/schema/extra warnings独立保存 |
| science/evidence/engineering分轴 | 09-26 §二 | PASS | 最终报告三轴分列，未混分 |
| ±5pp敏感性 | 09-26 §二 | PASS | 10变体，排名0变化 |
| 不与EnzymeCAGE直接同分比较 | 09-26 §十 | PASS | 报告明确任务形式不同 |
| 五模型原设计 | 09-26总表 | SUPERSEDED_PENDING_CONFIRMATION | 后续老师原则批准转为四模型121题，请老师确认本轮口径 |

总体：科学计算与证据纪律通过；执行前置存在已披露偏差，状态为
`READY_FOR_TEACHER_REVIEW_WITH_DISCLOSED_PROTOCOL_DEVIATIONS`，不写成无偏差验收PASS。

