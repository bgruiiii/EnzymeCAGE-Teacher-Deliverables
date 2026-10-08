# BIOSYSMODB150 四模型121题正式结果最终评估报告

```text
TASK_ID   = biosysmodb150_g9_four_model_121_formal_offline_score_20261008
DATE      = 2026-10-08 (UTC)
MODE      = 全程离线只读；API_CALLS=0；不新增/不重跑任何模型答案
STATUS    = G9_FINAL_READY_FOR_TEACHER_REVIEW
PROTOCOL_CONFORMANCE = PARTIAL_WITH_DISCLOSED_DEVIATIONS
```

**状态说明**：8份固定种子形态材料已完成AI预审（OK=6 / OBSERVATION=1 / CONCERN=1），
用户于2026-10-08完成人工形态审阅并确认8/8 PASS；逐份结论见老师包
`shape_review/HUMAN_SHAPE_REVIEW_RECORD_20261008.md`。本状态表示材料可提交老师审阅，
不表示老师已经接受报告中披露的pilot、GLM参数、预算和执行时序偏差。

---

## 1. 执行摘要

- 四模型正式API采集已关闭（权威收口文件`API_COLLECTION_STATUS=CLOSED_READY_FOR_OFFLINE_MERGE`），
  本轮只做离线合并、评分与报告，未调用任何模型。
- 合并矩阵恰为**121 case × 4模型 = 484槽**：committed=484、terminal=482、**usable=469**、
  内容失败=13（11 invalid JSON + 2 length/empty）、工程held=2、not-dispatched=0、正式retries=0。
- 15个非可用槽按合同**不补跑、不修复JSON、不用探针/pilot答案顶替**，全部保留在各模型121分母中，
  科学五层与总分计0，evidence/abstention写NA。
- **主科学结果（每模型固定121行macro均值，权重45/10/20/15/10，0–100分制）**：

| 排名 | 模型 | 主分数 macro(121) | usable-only均值（辅助，不作排名） |
|---|---|---:|---:|
| 1 | kimi/kimi-k3 | **17.9131** | 18.2141（n=119） |
| 2 | deepseek-v4.1-flash | **12.2099** | 12.3117（n=120） |
| 3 | qwen3.8-max | **11.9753** | 12.0751（n=120） |
| 4 | ZHIPU/GLM-5.3 (low) | **8.7215** | 9.5936（n=110） |

- ±5pp权重敏感性：10个变体全部重算，**排名零变化（STABLE_ALL_10_VARIANTS，0/40 model×variant格变动）**，
  含第2/3名之间0.23分的窄差距在各变体下亦保持。
- 独立validator **8974项检查全部PASS**；7种对抗突变（重复键、替换失败答案、混入pilot、分母120、
  改权重、改scorer SHA、换审阅样本）**7/7被拒绝**，无突变对照PASS。
- 正式484槽估算总成本由usage逐槽实算为**618.3102元**（口径见§9），与账本及两份本地审计一致。

## 2. 唯一输入与身份绑定

只处理以下两份正式回包（按SHA256绑定，不按mtime猜文件）；两包tar卫生
（无绝对路径/`..`/重复成员/链接/设备）、顶层与audit内部SHA256SUMS均独立复核通过：

| 输入 | bytes | sha256 | 内部SHA复核 |
|---|---:|---|---|
| `biosysmodb150_g6r3_glm_low_then_g8p1_three_model_return_20261007T015420Z.tar.gz` | 95,804,898 | `76a45fac…b8ec` | 顶层4458/4458 + audit 521/521 PASS；成员4,897 |
| `biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz` | 117,802,093 | `e17504af…e34c` | 顶层1638/1638 + audit 268/268 PASS；成员1,804 |

绑定审计与权威文件（SHA全部实算相符）：
三模型本地审计`4ede4ada…e3a6`、Kimi本地审计`4fbc0a02…544e`、
四模型收口`73314ebc…42bd`。两包release均绑定同一内嵌四模型输入包
`48a7e683…b222`；484槽的request body SHA逐槽与派发矩阵一致；每case题面
messages SHA四模型一致（121/121唯一）。`.tmp/.lock`运行时账本一律忽略，只读权威
`global_calls.json`（377 committed / 184.780276元）与`kimi_calls.json`（121 committed / 435.86014元）。

## 3. 冻结评分器硬门（全部实算断言通过）

```text
G1 gold manifest    c424763c…e06e   G2 questions manifest ae5780e5…5520
G3 gate             32c15520…caa2   G3 manifest           24f1004c…2e8a
scorer.py           a326eee6…9c61   score_recipe.md       8b79daf9…8392
validators.py       c3021644…3899   teacher approval      1fa908f5…a5d0
RDKit               2026.03.5（python3实测）
teacher approval文件 = 00_Authority_Teacher_Plan/TEACHER_REPLY_BIOSYSMODB150_G2_G3_SIGNOFF_2026-09-28(1).md
```

G3 validator就地重跑：**162项检查全PASS**；三mock实跑science=**100.0 / 0.0 / 77.36**，
与`mock_expected.json`逐层一致；controlled-input f1–f5与rule fixtures（D1–D6）全PASS。
scorer/gold/mask/阈值/权重/mock零修改；冻结目录零污染（无`__pycache__`落盘，G3内部SHA复核通过）。
源码顶部无残留PENDING状态覆盖冻结manifest与老师D1–D6回签（invalidation ledger记录
PENDING_REFREEZE已于2026-09-28解决）。

**D3披露（按score_recipe要求）**：步骤对齐Jaccard阈值冻结为0.5；在partial mock上
0.4/0.5/0.6三档不可区分（pathway层恒为77.78），本轮正式评分沿用冻结0.5，
真实阈值敏感case仅记录、绝不中途调参。

## 4. 484槽合并索引

`FORMAL_484_SLOT_INDEX.tsv`（唯一键=case_id+exact_model_id，按G2正典case序×固定模型序排列）
与`FORMAL_MERGE_MANIFEST.json`由`code/build_formal_484_slot_index.py`生成，**8295项断言全PASS**。
每行含：源tar SHA、原slot、request body SHA（重算一致）、raw SHA（held为null）、status、
engineering class、finish、JSON/schema判定、四类token、时长、request ID（482个终态全非空且唯一）、
committed UTC（484/484合法ISO）、fingerprint与失败原因。未复制任何pilot/smoke/probe答案，
未修JSON，未从reasoning提取答案。

每模型终态/可用与失败清单（与收口文件逐项一致）：

| 模型 | committed | terminal | usable | 失败清单（固定，不补跑） |
|---|---:|---:|---:|---|
| qwen3.8-max | 121 | 120 | 120 | held: BIOPATH150_084（G8P1-S208，工程结果未知） |
| deepseek-v4.1-flash | 121 | 121 | 120 | length+empty: BIOPATH150_125（G8P1-S308，65,536全reasoning） |
| ZHIPU/GLM-5.3 low | 121 | 121 | 110 | invalid JSON×11: 021,077,092,114,119,123,125,127,132,138,146 |
| kimi/kimi-k3 | 121 | 120 | 119 | held: BIOPATH150_050（G8P2-K042）；length+empty: BIOPATH150_128（G8P2-K106） |
| 合计 | **484** | **482** | **469** | 内容失败13 + held 2 |

## 5. 主科学结果（固定121分母，macro-case均值）

评分适配：469份usable原始visible直接`json.load`后调用冻结
`score_answer(case_id, answer, parse_status="VALID")`，无预清洗/字段补全/名称替换/结构改写；
15个非可用槽调用同一冻结函数非字典路径`score_answer(case_id, None, parse_status=<原因>)`，
原因值区分`INVALID_JSON` / `LENGTH_EMPTY` / `RESULT_UNKNOWN_HELD`。先评分每模型前3个可用case
并复核输出结构（`work/staged_first3_per_model.json`），再完成484行；每槽权重复算
（45/10/20/15/10）与scorer输出一致（双层2位小数舍入容差内）。

| 层（权重pp） | qwen3.8-max | deepseek-v4.1-flash | ZHIPU/GLM-5.3 low | kimi/kimi-k3 |
|---|---:|---:|---:|---:|
| pathway (45) | 17.7797 | 17.4874 | 12.5907 | **25.6726** |
| smiles (10) | 28.0992 | 28.0992 | 19.8347 | **40.4959** |
| enzyme (20) | 3.8914 | 4.4388 | 3.1289 | **5.5175** |
| microbial_identity (15) | 2.5756 | 4.2285 | 2.9760 | **8.0506** |
| traits (10) | 0.0000 | 0.0873 | 0.0000 | 0.0000 |
| **加权总分 (100)** | **11.9753** | **12.2099** | **8.7215** | **17.9131** |

解读要点：

- kimi/kimi-k3五层中四层领先，主分数第一（17.9131）。
- 第2/3名差距极小（deepseek 12.2099 vs qwen 11.9753，0.23分）：qwen的pathway层略高
  （17.78 vs 17.49），但deepseek在enzyme/microbial/traits三层反超；该名次在全部10个
  ±5pp权重变体下保持不变（§7）。
- **traits层全体趋零**（仅deepseek 0.0873）：D1冻结的数值cell严格精确匹配gold共识标量，
  四模型几乎全部弃答或偏差，属全局现象而非某模型异常；该层权重10pp，对总分影响有限。
- 绝对分数低是gold严格性所致（精确同分异构SMILES、精确TaxID、步骤全召回、数值性状精确匹配），
  仅用于四模型同题同参数横向比较，**不得与EnzymeCrew/EnzymeCAGE宣称同任务可比**
  （任务形式化不同）。
- micro counts仅辅助；usable-only均值只作披露（§1表），不作主排名。

## 6. 三条独立轴（分开报告，绝不折入science总分）

### 6.1 证据轴（evidence_axis.tsv）

| 模型 | verified | unverified | hallucination | ref_missing | overclaim | 证据链完整率* |
|---|---:|---:|---:|---:|---:|---:|
| qwen3.8-max | 6 | 3 | 83 | 0 | 22 | 0.6417 |
| deepseek-v4.1-flash | 1 | 2 | 19 | 0 | 255 | 0.9083 |
| ZHIPU/GLM-5.3 low | 0 | 28 | 14 | 0 | 146 | 0.8818 |
| kimi/kimi-k3 | 8 | 194 | 396 | 5 | 396 | 0.0420 |

\* 证据链完整率=usable槽中(hallucination=0且ref_missing=0)的占比（本文档口径，脚本计算）。

按冻结判词：`evidence_hallucination`=声称DATABASE_DIRECT但record_id本地不可解析、
claim_scope不匹配或accession非法/本地缺失（F5措辞为LOCAL_LOOKUP_ABSENT，**绝不宣称全局不存在**）。
kimi引用证据最多（含大量DATABASE_DIRECT/LITERATURE_DIRECT），离线本地核验无法解析的也最多
（396条），故其证据链完整率最低——这反映"高引用+离线不可解析"的组合，不改变其科学分。
qwen/GLM引用少而保守；deepseek引用少但overclaim高（255，见下）。

### 6.2 弃答轴（abstention_axis.tsv）——null是recall miss，绝不算overclaim

| 模型 | gold步骤召回缺失 | null弃答 | overclaim | 含null案 | 含overclaim案 | usable平均召回 |
|---|---:|---:|---:|---:|---:|---:|
| qwen3.8-max | 469 | 2 | 22 | 2 | 6 | 0.1193 |
| deepseek-v4.1-flash | 460 | 13 | 255 | 5 | 46 | 0.1260 |
| ZHIPU/GLM-5.3 low | 435 | 2 | 146 | 2 | 41 | 0.0960 |
| kimi/kimi-k3 | 434 | 20 | 396 | 10 | 86 | 0.1733 |

overclaim=高置信非null错误且无可解析证据（D4：只独立报告，绝不从科学分扣除；
诚实null永不劣于编造）。15个非可用槽evidence/abstention一律NA，不伪造零claim。

### 6.3 工程轴（engineering_axis.tsv，终态槽实测）

| 模型 | completion tokens mean/median/P90/max | 时延s mean/median/P90/max | 429/5xx/timeout/重试 |
|---|---|---|---|
| qwen3.8-max | 29,592 / 29,236 / 39,269 / 48,165 | 673.4 / 654.7 / 941.3 / 1,098.2 | 0/0/0/0 |
| deepseek-v4.1-flash | 25,318 / 24,655 / 33,851 / 65,536 | 160.6 / 154.6 / 229.1 / 382.8 | 0/0/0/0 |
| ZHIPU/GLM-5.3 low | 3,622 / 3,305 / 4,993 / 15,620 | 42.2 / 37.5 / 62.1 / 234.6 | 0/0/0/0 |
| kimi/kimi-k3 | 34,642 / 34,661 / 51,260 / 65,536 | 835.1 / 808.3 / 1,273.4 / 1,614.8 | 0/0/0/0 |

（P90=排序后最近秩法，索引round(0.9×(n−1))；qwen按120终态、kimi按120终态计。）

## 7. ±5pp权重敏感性与排名稳定性

数学规则复制自`G9_reporting_preflight/sensitivity_spec.json`（仅规则与10组变体权重，
**未复制任何SYNTHETIC分数或五模型名单**）；scorer binding改为冻结G3实际SHA，
模型集改为本轮四模型（`scores/sensitivity_spec_bound.json`）。对五层分别±5pp、
其余四层按比例重归一，10变体每组和精确=100（程序断言）；用同一484行层分重算，
未重跑scorer。

结果（`scores/sensitivity_results.tsv`，40行）：**全部10个变体下排名与base完全一致**
（kimi > deepseek > qwen > GLM-low），0/40格排名变动；各模型分数随权重的漂移幅度：
kimi ±1.2546分内（smiles±5pp最敏感）、qwen ±0.8958、deepseek ±0.8827、GLM ±0.6174，
均不足以改变名次（第1/2名差距5.70分，第2/3名差距0.23分在各变体下亦保持）。
结论：主排名对±5pp权重扰动**稳定**。

## 8. 失败、held与GLM-low格式稳定性（不补跑裁决）

- **GLM-low格式稳定性**：121槽无一length/空正文、平均42.2s最省成本，但11/121正文JSON语法无效
  （可用率90.91%，四模型最低）。11份均以`{`开头`}`结尾、含实质内容，属内部语法错误；
  按合同不得离线补JSON冒充原始可用答案，失败率作为该模型/配置的正式表现进入本报告。
- deepseek与kimi各1槽思考耗尽总预算（finish=length、visible=0），属模型内容终态。
- 2个held（qwen 084 / kimi 050）为相邻时间客户端shutdown事件，工程结果未知，
  单列披露、不冒充模型科学回答；可能已达服务端，重发将违反at-most-once，永久held。
- 重跑裁决全部false（两份审计+收口文件一致）：`RERUN_*=false`、`RESUME_NOT_DISPATCHED=0`。
  若将来做工程复现实验，只能作为独立supplement，不得替换正式槽或抬高正式成功率。

## 9. 成本实算与口径披露

逐槽按权威账本同一公式实算：终态槽`(prompt×in价 + completion×out价)/1e6`；
held槽按最坏预留`(10000×in + 65536×out)/1e6`结算（qwen 2.479296元、kimi 6.7536元，
与账本`reconciled_held`逐值一致）。单价（元/百万token，冻结budget guard配置）：
qwen 12/36、deepseek 2/8、GLM 8/28、kimi 20/100。

| 模型 | usage实算 | held预留 | 正式小计 |
|---|---:|---:|---:|
| qwen3.8-max | 136.3089 | 2.479296 | 138.7882 |
| deepseek-v4.1-flash | 25.9615 | — | 25.9615 |
| ZHIPU/GLM-5.3 low | 17.7004 | — | 17.7004 |
| kimi/kimi-k3 | 429.1065 | 6.7536 | 435.8601 |
| **正式484槽合计** | | | **618.3102元** |

口径：探针/smoke/pilot为工程费用，不计入也不抵扣正式合计（三模型账本184.780276元中
非正式部分≈2.33元与此口径一致）；kimi重算值与权威账本435.86014元完全一致；
合计与收口文件"约618.31元"一致。`.tmp/.lock`旧快照一律忽略。未触发1000元硬顶。

## 10. Kimi多fingerprint分层披露（全组保留，无剔除）

120个kimi终态分布于5个system fingerprint（exact model ID与请求参数不变；
不能仅凭字符串断定模型版本实质改变）。**全部5组保留参与评分与排名，
未在见到科学分后剔除任何组**：

| fingerprint | 终态 | usable | tokens均值 | 时延mean/median/P90/max (s) |
|---|---:|---:|---:|---|
| fpv0_3f6baf1f | 24 | 24 | 32,155.8 | 779.7 / 818.3 / 1,024.5 / 1,043.8 |
| fpv0_c96a51ed | 20 | 20 | 34,462.7 | 849.3 / 818.1 / 1,148.1 / 1,577.1 |
| fpv0_cabe88c9 | 30 | 30 | 35,497.9 | 880.4 / 952.7 / 1,275.7 / 1,589.8 |
| fpv0_df2f7ec7 | 30 | 30 | 31,999.9 | 796.3 / 758.0 / 1,285.5 / 1,464.3 |
| fpv0_e8884bc8 | 16 | 15 | 41,941.2 | 888.0 / 830.9 / 1,571.1 / 1,614.8 |

唯一length失败（BIOPATH150_128）在e8884bc8组；三模型fingerprint均未暴露（NOT_EXPOSED），
held槽无响应记NA_NO_RESPONSE。分层数量与本地审计F2逐项一致。

## 11. 形态审阅（8份固定种子样本）

抽样在全量评分后执行；抽样脚本仅读排序后的121个case ID，使用
`random.Random(20261006)`，模型序qwen→deepseek→GLM→kimi，每模型依次无放回抽2；
选择由冻结seed与模型顺序唯一决定，未按答案内容选择或换样；抽到失败/held也不换样
（本轮8份恰好全为usable槽）。样本：qwen{077,012}、deepseek{105,044}、GLM{145,044}、
kimi{080,028}。8份原始visible逐字节导出（SHA与索引一致），客观检查表全过：
8/8直接`json.load`成功、冻结schema 0错0警、接收端degenerate全False、
15-trait结构（F1–F15）8/8合规、题面复读仅为化合物名级短片段（≤5/191 chunk）。

AI预审：OK=6、OBSERVATION=1（deepseek_044单步极简+零不确定性声明）、
CONCERN=1（deepseek_105 evidence_registry为空数组）。
用户人工审阅：8/8 PASS；deepseek_044保留“单步极简但与总反应路线相符”备注，
deepseek_105保留“evidence_registry为空、证据纪律较弱”备注。人工审阅只关闭形态门，
不改变科学分、证据轴或冻结样本。

## 12. 独立验证与对抗突变

独立validator（`code/validate_g9_formal_scoring.py`，不import合并builder/评分wrapper，
常量独立硬编码）重算：两源tar字节+SHA、审计/权威SHA、8项冻结门SHA、RDKit版本、
484唯一键、4×121分母与正典case序、469/13/2计数、固定失败清单、482份request body/
raw/visible逐槽SHA重算（只认正式槽正典路径，pilot/smoke/probe文件顶替必被检出）、
held槽无raw/visible/request-ID、request ID唯一性、fingerprint分层、score JSON↔TSV
逐值一致、非可用槽零分路径与NA、权重45/10/20/15/10逐槽复算、macro重算、
10组敏感性规则/和=100/逐行macro重算、抽样种子复现、导出字节SHA、五份manifest
API_CALLS=0。**结果：8974项检查，0失败（FINAL_VALIDATION.json=PASS）**。

突变电池7/7检出（`work/mutation_results.json`）：重复键→rows/unique_keys拒；
一致篡改失败答案为可用→usable_469/invalid_11/源文件json.load拒；pilot答案顶替
（路径+SHA一致篡改）→正典路径与binding SHA拒；分母120→rows_484/model_121拒；
改权重→macro重算/变体规则拒；改scorer SHA→binding实算拒；换审阅样本→种子复现拒。

## 13. 边界与禁止事项（本轮全部遵守）

- API_CALLS=0：未读取API key、未联网、未SSH、未新增或重跑任何模型答案。
- 冻结scorer/gold/mask/阈值/权重/mock零修改；评分仅经独立wrapper只读调用。
- 不复制pilot/smoke/probe答案；不修JSON；不从reasoning提取答案；不用复现成功答案填空。
- science/evidence/engineering三轴分开；null=recall miss，绝不算overclaim。
- 不与EnzymeCrew/EnzymeCAGE宣称同任务可比；micro counts仅辅助；usable-only不作主排名。
- 主分数固定121分母；15个非可用槽计0并保留。

## 14. 交付物与复现

```text
FORMAL_484_SLOT_INDEX.tsv / FORMAL_MERGE_MANIFEST.json   484槽合并索引与清单
scores/  per_slot_scores.jsonl, per_case_scores.tsv, per_model_summary.tsv,
         evidence_axis.tsv, abstention_axis.tsv, engineering_axis.tsv,
         failure_registry.tsv, fingerprint_summary.tsv,
         sensitivity_results.tsv, sensitivity_spec_bound.json,
         usage_cost_summary.tsv/.json, SCORING_RUN_MANIFEST.json
shape_review/  sampling_manifest.json, samples/×8, checklist.tsv,
               AI_PRE_REVIEW.md, README.md, SHA256SUMS
code/    build_formal_484_slot_index.py, score_formal_484.py, run_sensitivity.py,
         compute_usage_costs.py, make_shape_review_sample.py, export_shape_review.py,
         validate_g9_formal_scoring.py, run_mutation_tests.py, package_g9_closure.py
FINAL_VALIDATION.json / SOURCE_AND_SCORER_IDENTITIES.json / COMMANDS.log / MANIFEST.tsv
gate_evidence/  G3 validator报告、三mock输出、staged样本、突变电池结果
```

复现顺序：`build_formal_484_slot_index.py` → `score_formal_484.py` →
`run_sensitivity.py` → `compute_usage_costs.py` → `make_shape_review_sample.py` →
`export_shape_review.py` → `validate_g9_formal_scoring.py` → `run_mutation_tests.py` →
`package_g9_closure.py`（全程`PYTHONDONTWRITEBYTECODE=1`，python3+RDKit 2026.03.5）。

## 15. 最终状态

```text
FINAL_STATUS = G9_FINAL_READY_FOR_TEACHER_REVIEW
PROTOCOL_CONFORMANCE = PARTIAL_WITH_DISCLOSED_DEVIATIONS
API_CALLS = 0
SLOTS = 484 committed / 482 terminal / 469 usable / 13 content failures / 2 held / 0 not-dispatched / 0 retries
PRIMARY_SCIENCE_MACRO_121: kimi/kimi-k3 17.9131 > deepseek-v4.1-flash 12.2099 > qwen3.8-max 11.9753 > ZHIPU/GLM-5.3 8.7215
SENSITIVITY = STABLE_ALL_10_VARIANTS (0/40 rank changes)
VALIDATION = PASS (8974 checks) ; MUTATIONS = 7/7 DETECTED ; G3 GATE = 162/162 + 100/0/77.36
HUMAN_SHAPE_REVIEW = PASS (8/8; USER_LOCAL_REVIEWER_CURRENT_THREAD; 2026-10-08)
FORMAL_COST_RECOMPUTED = 618.3102 CNY
```

下一步：提交黄老师复核结果与已披露协议偏差。老师若不接受偏差，则本轮降级为探索性基线；
不调用模型、不补答案、不改评分规则或选择性重跑失败槽。
