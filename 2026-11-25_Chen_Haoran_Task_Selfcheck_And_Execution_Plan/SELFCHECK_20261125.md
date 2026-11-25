# 陈浩然侧任务自检回执与冲突规划（2026-11-25）

**37项：DONE 12；PARTIAL 18；NOT_FOUND 3；CLOSED 4；REQUIRE_HUMAN 0。**

本轮按用户要求先自检和规划。依据老师自检单逐项读取实际文件、重数表行、核既有记录；只新增本目录两个回执文件。未补作业、未执行项目测试/评分/模型、未写库、未修改既有代码/数据/台账或历史交付，也未发消息或推送。§1/§5明确要求创建这两个回执，作为只读审计的输出例外；本轮“先自查”的范围不扩成边审边修或直接改main。

`PARTIAL`表示按本次更严格检查项尚有缺口，不表示已接收的旧交付作废；尤其来源表的typed缺失、旧量表状态和旧运行审批不能靠补字或改标签变成DONE。`CLOSED`按本次新单记裁定，不算欠账。DONE仅对相应检查标准负责，不扩大为科学效度、完整链路或生产部署通过。

## 扫描范围及证据边界

- 本地根：`/home/a/EnzymeCAGE`；所有TSV evidence路径相对此目录上级项目文档根：`/home/a/EnzymeCAGE/custom/docs/enzyme_feature_expansion/ENZYMECAGE_LUCAPCYCLE_MODEL_TRAINING_RUN_2026-07-01`。不同子目录的同名文件不能混为同一版本。
- 首轮枚举494438个文件路径，包含未提交工作区、历史交付与归档；排除Git对象/依赖缓存正文和凭据类文件。未读Key、密码、`.env`或shell历史。目录/文件名检索不等于逐字阅读全部文件；本次实际读取与判定有关的原件，证据全列在TSV。
- 发现37个Git元数据入口，归并22个可识别公用Git目录；扫描本地heads和remote-tracking分支。promisor仓另用仅本地对象的tree遍历，未fetch。教师交付仓8个ref、7个不同tip的目录树均可本地读取，未发现统一Harness发布或本轮正式发布审批。
- 两个仅下载提交信息的metadata副本缺tree对象：v44提交92831b12、main提交9aff0c2。它们分别有已取得的482文件代码归档和用户提供的main归档/工作副本补足文件查看；没有为自检联网补fetch。一个旧`.claude`工作树Git指针不可直接解析，其根仓对应ref存在，工作区文件仍在扫描范围。不能据本次结果宣称已检查用户未挂载电脑或未交接远端工作区。
- 根工作区现场status为10个tracked改动/1720个untracked条目；隔离接线副本为11个tracked改动/679个untracked条目。这是Git条目数，不是任务数；本轮没有清理或提交它们。
- 数字使用文件原值和机械计数。Qwen保留整数48417/58360及精确分数；报告展示0.829626，不在自检里重新四舍五入为新数。费用保留3.71872300与14.8748920原精度，不跨币种相加。

## 按模块统计

| 模块 | 检查行 | DONE | PARTIAL | NOT_FOUND | CLOSED | REQUIRE_HUMAN |
|---|---:|---:|---:|---:|---:|---:|
| A 基模参数 | 9 | 4 | 2 | 0 | 3 | 0 |
| B Likert | 3 | 0 | 3 | 0 | 0 | 0 |
| C 酶/宿主/接线 | 6 | 4 | 2 | 0 | 0 | 0 |
| D Fig.3 | 6 | 3 | 1 | 2 | 0 | 0 |
| E 三项裁决 | 6 | 1 | 4 | 1 | 0 | 0 |
| F Harness | 7 | 0 | 6 | 0 | 1 | 0 |

## 实际读到的关键数字

| 原件 | 现场读取结果 | 说明 |
|---|---|---|
| QWEN_PAIRED2_RESULTS.tsv | 2行；低档48417，高档58360 | 不据两对宣称非劣 |
| CALL_ACCOUNTING_83_CURRENT.tsv | 83行；已观察Go费用26行；list 3.71872300、allowance 14.8748920、observed cash 0 | UNKNOWN预留8行；不是全账户cash为0 |
| LIKERT_V05_SCORES_726.tsv | 726行；COMPARABLE 723、UNSCORED 3 | 有旧维度MISSING，不能套新三态改写 |
| HUMAN_EVAL_SCORE_TEMPLATE.tsv | 1008行；非空score 0 | 计划/空表不是真人评分 |
| SIX_MODEL_STEP_RESULTS_2292.tsv | 2292行；382个step各6臂 | 旧五臂排名82240行；新臂原始382份、16448候选关联可追 |
| MICROBE_UID_EVIDENCE_FOR_PAPER_7468.tsv.gz | 7468行；FOUND 7430、FOUND_SOURCE_SET 7、NO_HIT 30、IDENTITY_CONFLICT 1 | species_name空31，source_signature空38，保留真实缺失 |
| Fig3补件 | UID表7468行；3a 60行；3b 72行；集合关系42行；3c 84行 | CASE_EXPORT示例为SCHEMA_ONLY |
| 既有本地接口验证记录 | LEA 15测试/6CLI；接线输入23测试/5CLI；recorded new model/API=0 | 本轮只读记录，未重跑测试 |

## 冲突、歧义与实际未完成：不能混为一类

| 项目 | 现有工作与新单的关系 | 处理原则 |
|---|---|---|
| L02、H04：旧状态与新四态 | 旧结果是COMPARABLE/UNSCORED，逐维SCORED/MISSING；新单要求NOT_REQUIRED/NOT_APPLICABLE或新applicability。两套含义不能直接替换 | 保留旧结果；新适配按明确版本/范围设计。不能把3个未评分位置改成“不要求”以凑726，不能把旧MISSING改成NE |
| R01b：“NE（无用条目）” | 11-24原裁定NE是“已检索仍不可判”，NOT_REQUIRED才是不要求。NE率阈值与“七维全适用才给总分”的逐题/全局口径仍需精确定义 | 记PARTIAL并集中列定义问题，不由AI补算法，不重归一化，不据此打新分 |
| R01a/R03：121与376 | 121是路线/案例视图，用户已确认417−41=376单步范围；新题面/原答/生成配置仍未交齐 | 明确单位与题面版本，不能把旧121表当新冻结清单，也不重判41项是否酶促 |
| E06：“接到main”与Q6授权 | 这是目标/权限歧义，不必认定老师两次裁定相互推翻。Q6允许隔离分支与一个真实案例，维护者合并部署 | 当前因真实后端/完整案例未验收而PARTIAL；不是因为我们无main写权限就不用做，也不是要直接改生产main |
| E03：“每条有物种” | 7468行表已完整交付，合法NO_HIT/冲突/来源集合仍有空字段；旧采用还明确22个占位未识别标签 | 自检严格字面记PARTIAL，说明真实缺失；请老师区分“交付表完备”与“每个对象都鉴定成功”，不为形式通过伪填或另开全面补证 |
| R02：旧RELEASE_APPROVAL同名文件 | 本地有12份旧校准/运行/修复级同名文件，不能说整个磁盘没有；但没有完成目标代码发布冻结所需的审批绑定 | 旧运行授权保持原义；后续只补旧指定路线的发布手续，不复制旧审批冒充、不倒签、不触动正文/权重/公式 |
| Harness H01–H06 | 本次新增范围；有执行器、SSE解析、分类/费用/评分等组件，但没有满足新统一合同的整套实现与83/723统一重放证据 | 可规划复用组件，不把它们说成已完成Harness；也不把新要求写成我们一直欠交的旧整项 |
| B06/B07/K01/H07 | 新单明确暂停/不做；旧报告里“直连是否还要补”等属于旧时点 | CLOSED，不重开40题、最小预算、Moonshot直连或依赖40题的分层矩阵 |

## 所有PARTIAL与NOT_FOUND：逐项一行

- **B04 PARTIAL**：HEADROOM=NOT_FULLY_VERIFIED；all_routes_headroom_2x_p99_proven=false；缺覆盖全部路由的2×P99/等价余量证明，不能用已配置cap或单题未触顶代替。
- **B05 PARTIAL**：追溯表现读2个成功槽，queue_binding_status均MISMATCH_DECLARED_NOT_RETROSPECTIVELY_FIXED；旧/新队列SHA均有，但未统一覆盖失败槽的阶段/是否发网络/是否计费/原始错误四字段。
- **L01 PARTIAL**：现读12行；1105-01=IMPLEMENTED_WITH_REVIEW_OPEN；02=DISPOSITION_DOCUMENTED；03=IMPLEMENTED；04=IMPLEMENTED_WITH_SCIENTIFIC_REVIEW_LIMITS；未满足四项均DELIVERED且无REVIEW_OPEN。
- **L02 PARTIAL**：现读726行，likert_status=COMPARABLE:723/UNSCORED:3；D2/D3a/D3b/D4含MISSING；未见NOT_REQUIRED/NOT_APPLICABLE旧表状态；新三态计数口径与旧冻结表不一致，不得为凑数重写历史状态/分母。
- **L03 PARTIAL**：有12题×6模型×2真人的方案；评分模板现读1008行，非空score=0；真实人评分数/身份/独立性记录NOT_FOUND，AI裁判记录不能代替真人独立效度。
- **E03 PARTIAL**：现读7468行，scientific_uid全部非空；FOUND7430/FOUND_SOURCE_SET7/NO_HIT30/IDENTITY_CONFLICT1；species_name空31、source_signature空38；表已交且typed缺失透明，但不满足每条均有明确来源物种的严格字面要求，不伪填。
- **E06 PARTIAL**：LOCAL_ONLY_NOT_PUSHED；有隔离分支及11文件改动，记录23项离线测试/5次CLI通过；graph节点目前仅准备输入，real_model_calls=0，缺真实后端绑定及完整案例验收；是否合并main由维护者决定。
- **F02a NOT_FOUND**：NOT_FOUND_FIG3_RANDOM_EXPECTATION；未找到对应Fig3外测视图的随机Hit@1/Hit@10数值及计算方法；训练random_init或其他题域random记录不替代此项。
- **F02b PARTIAL**：n_candidates逐步列存在，382步可逐项追溯；未找到对应评测视图已交付的候选池min/median/max或分位数汇总，本轮不补算分布。
- **F02e NOT_FOUND**：NOT_FOUND_MANUSCRIPT_BRIDGE_SENTENCE；未在本地论文/图注草稿找到明确说明Fig2的24/76与Fig3的228关系的交付句；自检单自身的要求不算成果。
- **R01a NOT_FOUND**：NOT_FOUND_NEW_SCOPE_121_FROZEN_LIST；旧121路线/旧题面文件不充新题面冻结；当前新任务逐条题面/清单与冻结时间未核收，121路线与376单步的单位须区分。
- **R01b PARTIAL**：原裁定已有NE原则和阈值；未见已核准的逐题互斥执行规则/总分算法；自检单NE（无用条目）与原定义已检索仍不可判不一致，不能擅自解释或重归一化。
- **R01c PARTIAL**：旧题面12题/72答案/2评价者抽样与裁决方案存在；新开放题面固定样本、核证/NE条件、独立复核和预算设计未落定；T07=NOT_STARTED，不拿旧设计冒充新任务预注册。
- **R02 PARTIAL**：代码交付status=READY_FOR_RELEASE_REVIEW；目标SOURCE_MANIFEST实算SHA=c0f92da92a30c27204fb18054c23403577cb6f115d2b941e5716f4c1bfb5e148；旧运行级approval存在但非该发布冻结；缺绑定目标SHA的发布审批人/时间，T03未完成。
- **R03 PARTIAL**：已收20题汇总与41项排除；有417/41/376范围记录；20题原请求/原答/参数、新任务冻结题面与原答未齐，不把汇报MD或旧121材料当三样齐全。
- **H01 PARTIAL**：已有run_queue(auth_path,queue_path,ledger_path,transport_factory,out_root)及逐槽目录/预算门；缺统一任务集+模型配置+预算CLI与历史83槽完整离线重放证据，不以旧单用途执行器当统一Harness完成。
- **H02 PARTIAL**：已有21项假传输回归记录，含HTTP错误/帧不完整/断流等；但每槽阶段/是否发网络/是否计费/原始错误未统一成完整四字段，真实worker另有发网前崩溃记录，缺统一Harness四字段与三类注入验收。
- **H03 PARTIAL**：现读83槽账；26行已观察费用精确合计list_usd=3.71872300、allowance_usd=14.8748920、observed_cash_usd=0；不跨币种相加；usage在原件/parse_meta中，未与三费用列统一到Harness运行账schema。
- **H04 PARTIAL**：旧Likert pipeline/程序命中表及独立LEA接口存在；旧表723可比/3未评分；缺覆盖新applicability四态+程序命中的统一评分schema与723份统一Harness重放证据，不能改旧状态来造一致。
- **H05 PARTIAL**：commit有request_sha256/queue_sha256/committed_utc，LEA另绑rubric/版本；缺统一run manifest的exact ID/全部参数/执行人等闭合及队列错配自动MISMATCH验收；现有MISMATCH_DECLARED为事后披露，不冒充自动校验。
- **H06 PARTIAL**：有主指标、边界、2题/4目标、停止规则草案；费用写发送前另行确定，缺完整预算/冻结时间与预注册时间早于首槽的机械校验；NOT_AUTHORIZED草案不等于已冻结模板。

## 后续执行顺序（规划，不在本轮补做）

1. **先对齐少数定义。** 统一旧/新评分状态适用范围、NE与总分的执行定义、121路线与376单步的对象单位；E06只按隔离分支实施、维护者合并理解。科学内容由老师/师姐确认，工程身份不反复索证。
2. **先做能独立收口的低成本项。** R02旧指定路线发布冻结；Fig3随机期望/候选池分布的CPU材料，以及Fig2/3衔接句由作者确认。它们不需要重新训练、调用模型或重跑旧成绩。本轮只报缺项，没有顺手生成这些结果。
3. **接线继续复用旧案例。** 优先苯并三唑两条两步分支（3个不同反应），用既有资产/原始结果作对照，补新接点及一个选定分支的真实后端验收。旧固定UID正控与自然召回池分开；三条新六步候选暂缓，不平行展开18步新路线。实际GPU/缺件计划另行明确，当前不启动。
4. **Harness拆成可核的小步。** 先冻结输入/输出/失败/费用/评分schema，复用executor.py、SSE解析、现有83槽账和LEA；再做历史83槽及723份旧评分的离线对照，保留原状态与原始差异，不为迎合新四态改旧结果。此后再决定是否开放新的真实小样本，不借Harness恢复已关闭40题。
5. **等材料和人力的部分单列。** 师兄20题原始run、新题面/原答/参数只收真正缺的原件；41排除表不重复索取。真人独立评分由真实评价者提供，AI不能补成人分。

## 本轮交付及核对

两个文件：`SELFCHECK_20261125.tsv`与本摘要。TSV为UTF-8无BOM、固定6列、37个唯一task_id，状态及置信度只用指定枚举；evidence多文件使用` ; `分隔，均已查存在。不存在的交付写NOT_FOUND或明确的局部缺项，不拿计划书、同名旧文件、旧模型结果或commit message冒充完成。
本轮未更改任务台账/最终累计稿/旧审批/评分/模型源码。后续若上传，只新增日期回执目录，不夹带既有工作区变更。当前按用户“先自检、规划”安排本地待阅，未推送，不宣称老师已收件。

输入自检单SHA256：`784ad7872c72c4a2443bf7b3a0a1f7f0222fc042f0056b380763a82ba656f0eb`。
TSV SHA256：`998e14bce33d7470139207b90534130ff5d622bf95719fe2aea2d3ab1c71724f`。
