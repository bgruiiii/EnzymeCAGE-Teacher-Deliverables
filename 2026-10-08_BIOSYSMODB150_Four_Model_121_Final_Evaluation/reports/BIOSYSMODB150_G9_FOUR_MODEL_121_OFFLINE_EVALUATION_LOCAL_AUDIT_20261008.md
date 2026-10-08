# BIOSYSMOdb150 四模型121题G9离线评估本地审计

日期：2026-10-08  
方式：本地只读复核、零API调用；未修改评分、模型答案或封存tar。

## 审计结论

```text
SCORING_VALID=true
PACKAGE_VALID=true
API_CALLS=0
ROWS=484
USABLE=469
CONTENT_FAILURES=13
HELD=2
PRIMARY_RANKING=KIMI > DEEPSEEK > QWEN > GLM_LOW
SENSITIVITY=STABLE_ALL_10_VARIANTS
FINAL_STATUS=G9_SCORED_PENDING_LOCAL_HUMAN_SHAPE_REVIEW
TEACHER_READY=false
```

评分、排名、成本、敏感性、失败分母和封包主体均可信。当前不能升级为最终发布PASS，原因是8份形态
样本尚无真实人工签字；另有一项抽样时间顺序表述需要在最终老师版重打包时校正。

## Findings

### F1（中）：抽样算法有效，但“先于任何答案内容读取”表述与实际顺序不符

`COMMANDS.log`与文件mtime显示：全量评分于`2026-10-08T01:52:40Z`完成，抽样manifest于
`01:57:44Z`生成。报告、AI预审和抽样说明却写成抽样先于任何答案内容读取。

抽样结果仍有效：脚本输入仅为排序后的121 case ID，固定`random.Random(20261006)`，模型顺序固定，
独立复算得到完全相同的8个样本；mutation也能检出换样，未发现按答案好坏重抽。该问题不改变样本、
评分或排名，但属于provenance时间线过度声称。最终老师版应改为：

```text
抽样在全量评分后执行；抽样算法仅读取case ID，由预先冻结的seed和模型顺序唯一决定，
未读取答案内容作选择、未换样。
```

### F2（低）：sidecar的“48 members”是文件数，不是tar总成员数

tar实际含54个成员：48个普通文件（其中MANIFEST自身1个）和6个目录；MANIFEST列47行，完整覆盖除
自身外的47个普通文件，逐字节复核全过。identity/validation sidecar位于同基名
`.identity.txt/.validation.txt`，确实存在；其中`members=48`应解释为regular files。该措辞不影响
包卫生，但最终重打包时建议写`regular_files=48; tar_members=54`避免歧义。

### F3（状态门）：人工形态审阅仍未完成

8份材料均为可用正式槽，JSON/schema/15-trait结构通过。AI预审为6 OK、1 OBSERVATION、1 CONCERN：

- DeepSeek case044：单步总反应且uncertainties为空，属极简形态观察。
- DeepSeek case105：5步/1 profile但`evidence_registry=[]`且uncertainties为空，属证据纪律concern。

AI不能代替人工。人工可依据合同分别记录PASS、PASS_WITH_OBSERVATION、PASS_WITH_CONCERN或FAIL；
无论结论如何，都不得换样、补问或改变已冻结科学分。人工记录在场前只能保持PENDING。

## 包身份与完整性

```text
file=biosysmodb150_four_model_121_g9_offline_evaluation_20261008.tar.gz
bytes=267394
sha256=a22fe97568f899d9de4a98a940b1eb2dbe28b550e62355727e7fcaf622e74385
tar_members=54
regular_files=48
manifest_rows=47
```

- 单根、无绝对路径、`..`、重复、链接或设备。
- MANIFEST覆盖除自身外全部普通文件；47/47 bytes与SHA复核通过。
- identity SHA=`bc7717266e62f1938cd35b615f6f6743e5aaee5ae7196f2cf38bc86ce57a362a`。
- validation SHA=`c5582f59ec2dc9706a36a1050d0a584290e7a1588214ed391cc03510e62e994d`。
- 两份巨型正式raw未复制入小包，只以绝对定位、bytes与SHA绑定，符合收口合同。

## 独立评分复算

独立读取484槽索引并直接调用冻结`scorer.py`重算全部槽：469个usable走原始visible `json.load`，
15个非可用走`score_answer(case_id, None, parse_status=...)`。逐槽pathway、SMILES、enzyme、
microbial、traits和science总分与交付结果零差异；所有非可用槽五层与总分均为0。

固定121分母macro复算：

| 排名 | 模型 | 主分数 | usable-only辅助分 |
|---:|---|---:|---:|
| 1 | kimi/kimi-k3 | 17.9131 | 18.2141 |
| 2 | deepseek-v4.1-flash | 12.2099 | 12.3117 |
| 3 | qwen3.8-max | 11.9753 | 12.0751 |
| 4 | ZHIPU/GLM-5.3 low | 8.7215 | 9.5936 |

逐行重新应用45/10/20/15/10权重无不一致。10个±5pp变体、40个模型-变体格全部独立重算一致，
排名变化0；最大绝对漂移分别为Kimi 1.2546、Qwen 0.8958、DeepSeek 0.8827、GLM 0.6174。

## 冻结门与工程复核

- 两源正式包、两审计与权威收口SHA匹配；484唯一键、4×121、469/13/2正确。
- G1/G2/G3与老师回签8项SHA匹配，RDKit=2026.03.5；G3门162/162，mock=100/0/77.36。
- 独立validator再次运行8974/8974通过；突变电池7/7检出且无突变对照PASS。
- 正式成本由usage及两个held预留独立复算为618.310244元。
- Kimi五fingerprint分层计数与正式审计一致；所有组均保留。
- 旧SYNTHETIC 605行结果未混入真实484行；fixture label为正式四模型标签。

## 收尾裁决

```text
G9_NUMERIC_SCORING_CLOSED=true
G9_PACKAGE_ACCEPTED_AS_PENDING_ARTIFACT=true
NO_MORE_MODEL_API_CALLS=true
REMAINING_BLOCKER=LOCAL_HUMAN_SHAPE_REVIEW_8
```

下一步只需人工审阅8份固定样本并形成签字/日期/逐样本结论。随后离线修正F1/F2措辞，把人工记录
加入包，重新运行validator并版本化生成老师审阅版；不得原地覆盖本PENDING tar，也不得改变任何分数。
