# Likert v0.4 M2证据核验原型最终本地审计

- 审计日期：2026-10-22
- 输入目录：`50_BIODEGRADATION_LIKERT_V04_M2_EVIDENCE_PROTOTYPE_20261022`
- 执行卡SHA256：`04821a55e42f8d7bde4ad0b70cab101688f2274f85b24bee9eaa4a1a4b82536b`
- 回包SHA256：`f75cc2f1b18a465f47bfb98fe3bc4816fe4de6a18da7ded082ef915e665ba33a`
- 审计结论：`M2_PASS_WITH_NONBLOCKING_FOLLOWUPS`
- v0.4状态：候选R1，未冻结

## 一、结论

M2小规模统一证据核验原型通过。五类批准来源均完成受控抓取，网络与调用纪律合规；冻结raw能够在断网条件下逐字节重建规范化记录、三态核验结果和人工复核队列；L2/L3没有被程序越权终裁；未生成Likert分数、D5严重度/cap、gold修改或模型结论。

本次通过只证明“小规模评价侧证据核验原型可行”，不等于150题生产系统完成，也不授权进入正式全量核验。M4仍须等待M3高影响问题闭合；M7生产化仍依赖M6。

## 二、独立复核结果

### 2.1 身份、封装与输入

1. 执行卡、老师批复、总合同、用户确认、M1 R1最终审计SHA均复算一致。
2. 50目录`SHA256SUMS`和`SHA256SUMS_INTERNAL`全部通过。
3. 确定性tar为单根目录；144个tar成员中无绝对路径、`..`、软/硬链接、设备成员或重复成员；内部132个内容文件哈希全部通过。
4. 从独立临时解包树按固定mtime、uid/gid、排序和`gzip -n`重建tar，得到与原包完全相同的SHA256：`f75cc2f1…ba33a`。
5. 36目录内部`SHA256SUMS`复验46/46通过；49/42/36只读输入的实测SHA与冻结身份一致。

执行卡§2.3中的`36/retrieval_log.tsv`值确为61字符，属于不可成立的SHA文本。执行器没有据此伪造匹配，而是使用卡内已正确绑定的`36/SHA256SUMS`，再由该清单解析并复算真实64字符SHA；文件内容与36目录内部清单一致。该处为执行卡编制错误，不构成本次输入篡改，但以后生成执行卡时必须增加SHA长度和格式预检。

### 2.2 网络与调用纪律

1. `query_plan.tsv`、`retrieval_log.tsv`、`logs/ledger.json`和30组raw三件套一一对应。
2. 实际网络attempt为30/40，重试0，并发1；每个logical query仅一次请求。
3. 访问主机仅为：`eutils.ncbi.nlm.nih.gov`、`www.enzyme-database.org`、`rest.uniprot.org`、`www.ebi.ac.uk`；全部HTTPS且与白名单一致。
4. 30次请求均为HTTP 200；未发生401/403、429、5xx、超时或重定向。
5. 同主机最小UTC启动间隔复算为至少1秒，满足执行卡节流要求。
6. 每个raw body的字节数和SHA均与meta、retrieval log一致；敏感响应头未落盘。
7. 模型API调用0，商业API费用0；未发现真实key、cookie、Authorization或代理凭据泄漏。测试代码中的合成secret字符串不属于凭据。

### 2.3 解析、三态和人工边界

独立统计与交付一致：

```text
normalized_records=39
claims=74
SUPPORTED=43
CONTRADICTED=12
UNRESOLVED=19
human_review_queue=26
L2=10
L3=1
```

抽查全部12条`CONTRADICTED`，均有明确官方记录和字段级反证，不存在因无结果、接口失败或相近条目而判矛盾。代表性事实包括：

- TaxID 336257指向真菌条目，不支持PM1；28040不指向GJ10；390235为W619而非F1；
- EC 4.5.1.5为S-carboxymethylcysteine synthase；1.14.15.28不是xylene monooxygenase；
- P12994为*E. coli* YbhB，不是GJ10 DhlA；
- `NC_009512.1`的efetch历史正文仍存在，但esummary明确`status=suppressed`；
- PMID 6501223是Finette等1984论文，不是Zylstra 1989论文。

全部19条`UNRESOLVED`均带明确原因；不存在UNRESOLVED行夹带`contradiction_detail`。11条L2/L3全部保持UNRESOLVED并进入`PENDING_HUMAN`队列。历史预期没有参与状态生成，只在当前状态生成后用于触发快照分歧队列；独立检查未见循环判定。

“记录存在不等于支持具体声称”“物种级记录不自动支持菌株级断言”“历史撤转编号不等于虚构”等边界均按合同实现。

### 2.4 离线重放与测试

在fresh extract中使用`python3 -B`独立重跑：

- 离线单元测试32/32通过；
- 真实数据测试11/11通过；
- 规范化记录、三态结果、人工队列从raw重新生成后与交付文件逐字节一致；
- 重放过程通过socket connect阻断和代理黑洞运行，没有网络依赖；
- 测试过程未生成`.pyc`或污染封装树。

因此M2的核心可重放性成立。

## 三、非阻塞问题及后续强制修正

### F1：UniProt库级release头未保存

两次UniProt响应的meta均显示官方返回了`x-uniprot-release`与`x-uniprot-release-date`头名，但抓取器没有把这两个非敏感版本头列入保存白名单，只记录为被删除头名。`SNAPSHOT_MANIFEST.json`因而写成`UNIPROT=NOT_EXPOSED`，该表述不准确。

本问题不阻塞M2：两个条目的原始JSON正文、访问UTC、body SHA、accession、entry version、sequence version和`lastAnnotationUpdateDate`均已冻结，足以唯一审计本次事实判断；重新联网不会改变现有三态结论。

强制后续：M4若沿用本快照，必须披露“库级release header值未保留”，不得写`NOT_EXPOSED`；M7生产抓取器必须将`x-uniprot-release`和`x-uniprot-release-date`加入安全保存头，并增加测试。若黄老师要求M4精确绑定UniProt库级release，须另行授权最多2次元数据补抓，不得静默重写50目录。

### F2：重放比较日志包含运行时UTC

三份科学输出可逐字节重放，最终冻结tar也可从冻结树确定性重建；但`replay_offline.py`每次运行会用当前UTC改写已纳入tar的`logs/replay_comparison.json`。因此“核心输出与冻结包确定性”成立，“按完整复现命令重新运行后整个工作树仍不变”不成立。

强制后续：M4/M7应把该文件明确排除为runtime log，或使用冻结snapshot UTC，不能继续把动态日志算入确定性交付树。

### F3：报告覆盖范围措辞过宽

74条断言覆盖多个关键裁决案例和执行卡夹具，但并非对17项裁决中每个维度、每条证据做全量重审。因此报告中的“当前官方快照完全复现17项裁决所依据的事实”应收窄为：

> 本原型登记的74条断言与17项裁决材料中对应的历史预期零不一致。

该措辞修正不改变任何机器结果，不允许据此声称17项人工裁决已被第二名独立专家重新确认。

## 四、阶段状态

- M2：PASS。
- M3：保持`NOT_STARTED`，可在独立零网络窗口执行。
- M4：LOCKED，等待M3高影响结果和生物侧确认；本审计不授权提前制作人工包。
- M7：LOCKED，且必须吸收F1/F2工程修正。
- v0.4：仍为候选R1，`V04_FROZEN=false`。

```text
FINAL_AUDIT_STATUS=M2_PASS_WITH_NONBLOCKING_FOLLOWUPS
PHASE=M2
NETWORK_ATTEMPTS=30/40
MODEL_API_CALLS=0
NORMALIZED_RECORDS=39
CLAIMS=74
SUPPORTED=43
CONTRADICTED=12
UNRESOLVED=19
HUMAN_REVIEW_QUEUE=26
OFFLINE_CORE_REPLAY_PASS=true
DETERMINISTIC_TAR_REBUILD_PASS=true
LIKERT_SCORES_ASSIGNED=false
D5_CAPS_ASSIGNED=false
GOLD_MODIFIED=false
V04_FROZEN=false
M3_UNLOCKED=true
M4_UNLOCKED=false
NEXT_ACTION=运行并审计M3；M4集成时披露UniProt release头缺失并修正动态重放日志策略
```
