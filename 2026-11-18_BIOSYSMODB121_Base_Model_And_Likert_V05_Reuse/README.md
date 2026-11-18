# 六基模测试与Likert V0.5评分体系：完整复用交接

2026-11-18。交给师兄参考。包内提供我们已经完成的题目、原答、API派发框架、评分代码和参考数据；师兄自行决定新实验20题、GPT型号、题面及运行安排。**本包整理期间没有采集新答案，也没有为“不限路线”实验给新分。**

## 拉取与进入目录

```bash
git clone https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables.git
cd EnzymeCAGE-Teacher-Deliverables/2026-11-18_BIOSYSMODB121_Base_Model_And_Likert_V05_Reuse
```

已拉取过仓库时先`git pull`，再进入上述日期目录；无需下载或解压压缩包。

## 从哪里开始

| 需要什么 | 在哪里 |
|---|---|
| 原来121道完整题目 | `questions/original_messages/`，真正发送的是各文件的`messages`，不是整个元数据文件 |
| 污染物/旧路线/氧条件可读索引 | [POLLUTANT_INDEX_121.tsv](questions/POLLUTANT_INDEX_121.tsv) |
| 国内4个、国外2个模型怎样发送 | [模型与实际请求说明](docs/GENERATION.md)，以及`generation_framework/`的17份历史源码 |
| 六模型真实原请求的封套 | `examples/original_generation_requests/`及[6份索引](examples/ORIGINAL_API_REQUEST_INDEX_6.tsv)，均不含鉴权头 |
| 六模型已选原答 | `existing_outputs/answers/`；726位置索引见[ANSWER_INDEX_PORTABLE_726.tsv](existing_outputs/ANSWER_INDEX_PORTABLE_726.tsv) |
| Likert V0.5实际规则与可运行代码 | [likert_v05/README.md](likert_v05/README.md)，命令入口`likert_v05/tools/likert_cli.py` |
| 原任务Gold/accepted/范围参考 | `reference/gold_121/`和`reference/original_task_contracts/`；060/094/023补充见`reference/case_overrides/` |
| 最后一次补评分的实际源码 | `latest_scoring_source/`；用于解释代码沿革，不直接启动旧批次入口 |
| 代码是否能校验真实评分结果 | `examples/real_original_task/`，一个原任务七维真实样例，已有离线验证 |
| 新实验可能卡在哪里 | [不限路线任务的适用边界](docs/OPEN_ROUTE_SCOPE.md) |
| 拉取后有哪些命令可以用 | [运行与输入输出](docs/RUNNING.md) |

## 我们原来确实给了哪些条件

原121题不仅给污染物，还给了**指定降解路线名称/限定词、已有氧条件（aerobic/anaerobic，未指明时null）、结构化交付要求**。原题内要求逐步反应、每步首选酶/EC、微生物与性状。不是只让模型报一个酶，也不是让它返回有序Top-3/5候选。

所以师兄提出的“只给污染物、让模型自己选路线”是另一个任务设置。原题和字段都在包内，师兄可自行处理；**不要将旧路线名、旧氧条件或完整case_metadata不经处理又发送给模型，造成名义上不限、实际仍提示原路线。** 本包没有帮师兄删改题目，也没有替他选20题。

## 原工具能否用于新任务

**调用、收流、结构校验、七维评分请求/返回、合并和总分复算这些工具可以复用。** 但现有任务范围和部分程序上限是针对原来的指定路线构建的，不能将旧答案的CTX、对齐结果、上限或失败证明当成新答案事实。

只给污染物后，模型可能选择另一条真实路线；原Gold只覆盖既定路线时，未命中不等于答错。此时需由师兄明确评价目标、能接受的参考范围及缺口，再决定如何装配评分输入；可能产生真实NE或需复核。**“代码能返回分”与“分数适用于新任务”必须分开检查。** 详见OPEN_ROUTE_SCOPE，包内没有偷偷改V0.5条款。

## 拉取后先做零费用验证

在此目录运行（Python≥3.10，命令不会发API）：

```bash
python3 -B tools/verify_bundle.py
python3 -B generation_framework/tools/replay_demo.py
python3 -B likert_v05/tools/likert_cli.py validate --request examples/real_original_task/request.json --response examples/real_original_task/response.json
python3 -B likert_v05/tools/likert_cli.py merge --request examples/real_original_task/request.json --response examples/real_original_task/response.json --out work/original_task_rating.json
```

最后一个命令用原任务真实回包验证七维合并与总分，结果只写work。这个样例不能换上新答案后继续用旧的program范围。

另有`tools/collect_one.py`：新整理的薄单次调用入口，支持现成Chat/Responses请求body，默认dry-run，可供师兄接自己的题目和Key。它不是作者原实验的完整批量调度器，不自动选20题、改题、重试或计算科学分。历史框架和这个相对路径适配入口分开标注。

## 当前采用版本与历史目录的关系

评分代码目录是2026-11-14导出的可运行适配版和历史快照，里面“706份”是当时数量。后续沿S8实际规则及定向补评，S12修正060/094参考后，已发布基线为**726位置、723个位置可算总分、共同118题；238/5061维MISSING，NE=0**。历史723份并非全部同一个System。此包的既有分数按这一发布快照保留，不含正在开展的MiMo独立裁判或未来真人评分。

本次科学规则正文SHA为`4d891baa45d1887d2fa7c67d5e90ffbd37341b79f8c664e73118e5bd7b03a128`，文件是`likert_v05/rubric/SYSTEM_RUBRIC_USED_S8.txt`。历史候选/DRAFT标记保留，不代老师/专家补签科学批准。

## 之前给老师汇报的线上入口

- [V0.5评分代码](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-11-14_Likert_V05_Scoring_Code)
- [V0.5最终结果与新旧变化](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-11-15_BIOSYSMODB121_Likert_V05_Results_And_Attribution)
- [外模采集与审计](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-11-11_BIOSYSMODB121_Foreign_Model_Collection_Final_Audit)
- [六模型原答与Hit@1](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/main/2026-11-16_BIOSYSMODB121_Six_Model_Pathway_Enzyme_Hit1)

本目录附有实际题目和参考数据，师兄可从本仓库拉取后本地复用。密钥、私人账本、鉴权头不在仓库中，运行时使用自己的接口和账户配置。Gold原表保留来源与许可字段，来源限制见[来源说明](NOTICE.md)。
