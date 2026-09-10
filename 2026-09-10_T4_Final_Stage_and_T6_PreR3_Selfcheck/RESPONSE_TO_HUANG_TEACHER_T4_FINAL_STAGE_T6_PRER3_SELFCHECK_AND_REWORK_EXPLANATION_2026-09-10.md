# 给黄老师的T4/T6最新进度、返工说明与下一步（2026-09-10）

状态：提交黄老师审阅。T6进入R3前自查已完成并通过本地审计；T4科学/评测内容已完成，目前只剩R4外置交付封口，尚未写成正式最终通过。

黄老师您好，

收到您09-09对T4 18条、G1—G5和下一步的正式裁定后，我们并行推进了T4和T6。先报告当前可核状态，再说明为什么T6自查又经过多轮纠正、为什么本轮耗时明显长于之前。

## 一、当前结论

### 1. T4

T4 18条已经按您回签的parent-only身份完成depending v3.2与ECLIPSE runtime-blind评测，raw prediction先冻结、后评分。当前结果和边界为：

```text
depending v3.2 Hit@1/3/5/10 = 10/12/14/15（分母18），MRR@10=0.6366
ECLIPSE Hit@1/3/5/10 = 6/13/15/16（分母18），MRR@10=0.5343
depending product recovery = 19/39
ECLIPSE product recovery = 21/39
STRICT_UNSEEN_BLIND_EVALUATION = NOT_ESTABLISHED
CURRENT_METRICS = VALID_RUNTIME_BLIND_IN_DOMAIN_RECOVERY
MODEL_ROLE_DECISION = AWAITING_HUANG_TEACHER_REVIEW
```

重合审计主事实：depending可审计corpus中，13/39正确parent-product对在同一具体记录共同出现；15/18 parent出现在corpus reactant侧；16/39正确product曾出现在corpus product侧。三个ranker训练行身份不可恢复，故训练重合对18/18均为UNKNOWN，不能写成0。ECLIPSE为全10-fold聚合，存在TRAIN暴露，不是strict OOF。

T4内容审计已通过；当前只等待T4-R4外置closure三文件返回和本地快审。通过后，本包将保留中立两选项请您裁定：

```text
A. 接受当前runtime-blind in-domain recovery口径，进入模型角色讨论；
B. 由您下发严格held-out/OOF协议后另行执行。
```

本T4裁定不阻塞独立T6。

### 2. T6 microbe/G3/G4自查

按您09-09“8001不重启、不重建；直连UniProt/KEGG reviewed-only + 冻结reviewed UID映射表降级；先回传自查再谈重跑”的要求，当前自查已完成并通过本地审计：

```text
8001 active dependency=0
4 unique enzyme UID / 8 route records = UNIPROT_REVIEWED
Path L：4/4 live UniProt reviewed
Path F：4/4 live失败后命中冻结reviewed UID map fallback
Path U：live与map都失败时0 resolved + 4 UNRESOLVED
ABSENT：UID无精确map行时只降级该UID，不做名称/前缀/TaxID模糊匹配
microbe候选生产主键=positive NCBI TaxID
host identity signature与evidence record identity分开
downstream conversion二次mapper/query/request/map scan=0
G-SCHEMA Draft202012：8/8正例通过、12/12负例拒绝
13 suites / 155 tests：155 PASS，0 fail/error/skip
```

冻结UID map：

```text
bytes=104025134
SHA256=7b92e8e625cb73f070c8e902687ea5bbdbf749f04a19828e550e3fe205684fe6
```

四条fallback证据hash现覆盖CSV完整原始CRLF行bytes，不再删除行终止符。Q7X2D3的live名称与map名称在声明的规范化下仍不相等，仅TaxID一致；本任务没有自行裁定同义关系。

最终三文件本地收件：

```text
archive bytes=146872
archive SHA256=14c6b3ab04b7306eed2c52ece849039a37dfab8245ef48a5335df3faa32a494b
identity与archive=PASS
pre-write P01—P12=12/12 PASS
post-write Q01—Q10=10/10 PASS
mutation=12/12 PASS
final-readonly=PASS
```

### 3. 尚未完成的T6部分

上述只是进入T6-R3前的microbe/fallback/证据自查，不是T6整体通过：

```text
C8→T5真实连续回归=NOT_RUN
T6-R3真实LangGraph invoke/stream=NOT_RUN
20项终验=NOT_COMPLETE
T6_OVERALL_READY=false
G7_PASSED=false
```

我们没有修改您负责的graph/state/router/edge，也没有把组件测试写成整链通过。

## 二、为什么又改了多次

这次确实返工次数过多。原因分为必要的科学/工程纠正和本可避免的执行/审计错误两类。

### 1. 必要纠正

1. 第一轮只确认8001调用点和4个UID entryType，发现历史8条UNRESOLVED实际上对应4个reviewed UniProt UID；需要继续把真实来源证据接到production节点，而不能只改报告。
2. 下一轮拿到4份reviewed响应，但新增hostEvidence helper没有真正进入microbe节点输出；冻结104MB UID map fallback也只写在报告中，没有production reader；宿主signature还错误使用enzyme UID。这三项会直接导致断网重回UNRESOLVED或同宿主多酶被拆开，必须改代码。
3. 实现production fallback后，需要真实走live、fallback、双失败三路径，并验证state、G-SCHEMA和同宿主聚合，测试范围从16项扩大到142/155项。

### 2. 本可避免的返工（由我们承担）

1. 我们一度把后续T5 route-step精确tuple聚合规则误套到现有microbe `OrganismAggregator`，把老师冻结的NCBI TaxID生产主键改成signature；本地审计发现后恢复。
2. 第一版fallback对`raw.rstrip(CR/LF)`求hash，却称“原始行bytes hash”；这是审计身份口径错误，后改为包含实际CRLF的完整bytes。
3. 报告曾把Q7X2D3两个不同名称写成“规范化后相等”；实际只TaxID一致，已纠正。
4. 一轮代码虽已修对，但生成脚本把上一轮旧报告直接复制进新包，造成同包内新旧聚合规则和新旧hash互相矛盾；同时validator只是固定生成V01—V28 PASS。该轮内容不能交付。
5. 下一轮重建了真实G-SCHEMA、M1—M8和validator，却在写validation前预先创建空validation来满足“三文件存在”门，形成循环自证；再次被本地独立重放发现。
6. 最后一轮才将流程改成：validation写前必须不存在 → pre-write验证 → exclusive首次写入 → second fresh unpack post-write → final readonly，并用12个mutation验证。

这些额外轮次主要来自我们对“不同聚合层的合同边界”和“外置validation的时间顺序”设计不严谨，不应归因于模型推理本身。我们保留了每个失败包和审计，没有覆盖失败证据，也没有把中间READY直接发给您。

## 三、为什么比以前慢很多

### 1. 任务性质变了

之前的任务多是单一forward或小表核对；这次从“8条为何UNRESOLVED”发展成：

```text
老师main精确base重放
→ direct REST reviewed判定
→ production节点接线
→ 104MB UID map身份门/索引/fallback
→ state provenance承载
→ TaxID聚合
→ G-SCHEMA
→ 13-suite/155项测试
→ archive/identity/validation外部封口
```

因此单轮包含的核验层数明显更多。

### 2. 必要耗时

```text
每轮都从老师固定commit/tree重建，避免在污染工作树上续跑；
UID map每个fresh进程先核104025134 bytes和固定SHA，再完整扫描一次建立168335 UID索引；
Path L/F/U/ABSENT与聚合案例使用fresh subprocess，避免cache串味；
13个suite分别fresh执行；
archive必须重新解包、核manifest、做mutation和post-write验证。
```

这些是为满足来源真实性和可复现性而付出的必要时间。

### 3. 可避免耗时

更多延迟来自“执行器实现→本地审计发现提示词/validator缺陷→重新设计小任务→再次执行”的串行返工，而非GPU或模型计算；这不是学生操作慢：

```text
R3A与R3A-R1两个包完成时间相隔约5小时14分；这包含我们对结果的审计、重新设计和执行器再次实现，不是5小时纯计算；
R2A包内可核工作窗口约2小时45分，包含loader、节点、测试、报告和多次validator修复；
R2A-R2的23条结构化worker/test命令从04:18:33Z到04:19:02Z，约29秒，说明后续长等待主要不在科学计算；
R2A-R3包内preflight到mutation/manifest阶段约4分钟，其余时段主要用于我们修正脚本、重建外置封口和重新审计。
```

我们没有可靠的逐轮端到端计时器覆盖审计、提示词重写和执行器返工，所以不把包生成时间差冒充CPU/GPU运行时。能够确定的是：后半段多轮均未用GPU/模型，慢主要是我们在合同理解、报告生成器和validator设计上的返工，以及随后增加的严格交付验证；学生始终在持续推进和配合执行。

## 四、为避免继续拖慢采取的措施

```text
1. production代码与证据封口分开，内容通过后不再反复改算法；
2. microbe TaxID聚合与T5 route-step精确聚合分开写明；
3. validator必须有真实条件和mutation，禁止固定PASS；
4. archive内部只写打包时PENDING，外置validation通过后才写delivery PASS；
5. 交付自动化必须把archive/identity/validation作为不可拆分的原子结果，避免任何人工补取环节；
6. T4/T6并行，互不等待；
7. 本次等T4-R4最后封口后只向您发送一次完整材料。
```

## 五、下一步

T4-R4三文件返回并通过本地审计后，我们将补入最终交付身份。当前先按您“先回传自查再谈重跑”的要求提交T6进入R3前自查，同时如实报告T4已经到最终封口阶段：

```text
T4 18条结果、重合边界与A/B中立裁定请求；
T6 8001/entryType/direct REST/frozen UID-map/TaxID/G-SCHEMA自查；
多轮返工与耗时说明；
下一步严格按您09-09合同执行，不自行改拓扑或模型角色。
```

在您现有裁定下，T6下一技术步骤仍是以老师修复后拓扑执行真实T6-R3并完成20项终验；本轮没有提前把该项写成已完成。
