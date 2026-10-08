# G9 形态审阅 AI 预审（8份固定种子样本）

TASK_ID：`biosysmodb150_g9_four_model_121_formal_offline_score_20261008`
生成日期：2026-10-08（UTC）
抽样：`random.Random(20261006)`，抽样脚本仅读取排序后的121个case ID；实际执行时间在全量评分后，
但选择完全由预先冻结的seed与模型顺序决定，不读取答案内容作选择、未换样；
抽到失败/held亦不换样（本轮8份恰好全部为USABLE槽）。
导出：8份原始visible逐字节复制，SHA与484槽索引一致（见`SHA256SUMS`、`checklist.tsv`）。

判级词汇：`OK` / `OBSERVATION` / `CONCERN`（AI预审，仅形态层面，不改科学分）。
本文件保留原AI预审角色；真实人工结论见`HUMAN_SHAPE_REVIEW_RECORD_20261008.md`，8/8 PASS。

## 逐份预审

| # | 模型 | case | slot | JSON/schema | AI预审判级 | 人工审阅 |
|---|---|---|---|---|---|---|
| 1 | qwen3.8-max | BIOPATH150_077 | G8P1-S190 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |
| 2 | qwen3.8-max | BIOPATH150_012 | G8P1-S031 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |
| 3 | deepseek-v4.1-flash | BIOPATH150_105 | G8P1-S260 | 0错0警 | CONCERN | PENDING_LOCAL_HUMAN_REVIEW |
| 4 | deepseek-v4.1-flash | BIOPATH150_044 | G8P1-S110 | 0错0警 | OBSERVATION | PENDING_LOCAL_HUMAN_REVIEW |
| 5 | ZHIPU/GLM-5.3 | BIOPATH150_145 | G8P1-S354 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |
| 6 | ZHIPU/GLM-5.3 | BIOPATH150_044 | G8P1-S111 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |
| 7 | kimi/kimi-k3 | BIOPATH150_080 | G8P2-K066 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |
| 8 | kimi/kimi-k3 | BIOPATH150_028 | G8P2-K026 | 0错0警 | OK | PENDING_LOCAL_HUMAN_REVIEW |

### 1. qwen3.8-max / BIOPATH150_077（protocatechuate degradation III, para-cleavage）
4步主链（4,5-双加氧开环→半醛脱氢→草酰琥珀酸异构/水合→羟醛裂解为丙酮酸+草酰乙酸），
路线化学自洽；1个profile（Sphingobium sp. SYK-6，taxid诚实置null）；1条INTERNAL_KNOWLEDGE证据；
uncertainties如实声明SMILES/EC未核实。null叶比0.2679，题面复读2/191（仅化合物名级别）。
小观察：step3反应类型写"isomerization/hydration"而酶名为hydrolase，命名轻微不一致，不影响形态。
**AI预审：OK。**

### 2. qwen3.8-max / BIOPATH150_012（nitroglycerin degradation）
3步连续还原脱硝（NG→1,2-GDN→1-GMN→甘油+亚硝酸），酶统一为nitroglycerin reductase并
明确声明EC未定；profile Agrobacterium radiobacter（taxid null，与文献惯例一致）；2条内部知识证据；
uncertainties披露1,2/1,3支路选择与辅因子未纳入。结构完整、诚实。**AI预审：OK。**

### 3. deepseek-v4.1-flash / BIOPATH150_105（4-coumarate degradation, anaerobic）
5步厌氧主链（CoA活化→水合/裂解→醛脱氢→再活化→还原脱羟基生成benzoyl-CoA），
化学计量合理，profile Rhodopseudomonas palustris CGA009（taxid 258594，菌株级正确）。
**但evidence_registry为空数组（0条），uncertainties也为空**：一个引用了具体菌株CGA009与
酶系CouA-E的答案却零证据登记、零不确定性声明，证据纪律缺失；schema允许空数组故0错0警，
客观检查表shell=Y仅由"零证据"触发（steps/profiles实质存在，非模板空壳）。
证据轴按冻结规则计（verified=0），不属overclaim。**AI预审：CONCERN（证据登记为空）。**

### 4. deepseek-v4.1-flash / BIOPATH150_044（methylphosphonate degradation I）
仅1步总反应（C-P lyase：甲基膦酸根+水→甲烷+磷酸），profile E. coli K-12 MG1655
（taxid 511145为基因组级注释，非模式株595495，属可接受差异）；2条内部知识证据；
uncertainties为空。单步极简但内容与该路线的"总反应"性质一致，非空壳。
**AI预审：OBSERVATION（单步极简+零不确定性声明；taxid取基因组级）。**

### 5. ZHIPU/GLM-5.3 / BIOPATH150_145（sulfoquinovose degradation V）
4步SQ磺酸糖降解主链（异构→醛缩裂解→脱氢→C-S裂解释放亚硫酸），属该途径公认骨架；
2个属级profile（Klebsiella sp.、Pseudomonas sp.，taxid诚实null）；1条内部知识证据；
uncertainties明确声明"15项性状全部null、路线编号V低置信"。null叶比0.5415为8份中最高，
但与其全面诚实弃答策略一致，非模板空壳。**AI预审：OK。**

### 6. ZHIPU/GLM-5.3 / BIOPATH150_044（methylphosphonate degradation I）
1步C-P裂解总反应，enzyme给出PhnGHIJKLM复合体细节；profile E. coli K-12（taxid 83333）；
1条内部知识证据；uncertainties解释EC 4.7.1.1为复合体总反应编号、K-12保藏/基因组号未确认置null。
结构完整、自我披露充分。**AI预审：OK。**

### 7. kimi/kimi-k3 / BIOPATH150_080（ferulate degradation）
5步CoA依赖型阿魏酸主链（Fcs活化→Ech水合/逆羟醛→香草醛脱氢→VanAB去甲基→PCA 3,4-双加氧），
4个profile（HR199/AN103/SYK-6/ADP1菌株级，ADP1给taxid 62977）；8条证据
（7 LITERATURE/DATABASE_DIRECT + 1 INTERNAL）；uncertainties讨论EC 1.14.13.82归属置信度。
题面复读5/191为notes引用题面所致，属正常。8份中信息量最大。**AI预审：OK。**

### 8. kimi/kimi-k3 / BIOPATH150_028（creatinine degradation I）
3步主链（肌酐酶→肌酸酶→肌氨酸氧化酶），酶名含EC（3.5.2.10/3.5.3.3）；
profile Pseudomonas putida（taxid 303）；6条证据（5 DATABASE_DIRECT+1 INTERNAL）；
uncertainties说明F5/F14置null原因与S3氧条件依赖。**AI预审：OK。**

## 横向形态观察（不影响科学分）

- 8/8直接`json.load`成功、冻结schema 0错0警、接收端degenerate全False：本轮抽样中
  四模型usable槽形态一致性良好。
- 证据纪律差异明显：kimi两份共14条证据（多为DIRECT类），deepseek_105为0条。
  该差异已由冻结evidence轴独立计量，未折入science总分。
- 诚实弃答（null+uncertainties声明）在qwen/GLM/kimi样本中普遍；deepseek两份
  uncertainties均为空数组，与其余三模型风格不同，人工审阅时建议留意。
- 15-trait结构：8/8样本所有profile均含恰好15个F键（F1–F15），结构合规；
  内容多为null（GLM_145为全null并有声明），traits层得分为0属gold严格所致的全局现象。
- 题面复读均为化合物/路线名级别的短片段（≤5/191 chunk），未发现整段抄题。

## 状态

```text
AI_PRE_REVIEW=COMPLETE (8/8: OK=6, OBSERVATION=1, CONCERN=1)
HUMAN_SHAPE_REVIEW=PENDING_LOCAL_HUMAN_REVIEW
FINAL_LABEL_UNTIL_HUMAN_REVIEW=G9_SCORED_PENDING_LOCAL_HUMAN_SHAPE_REVIEW
```
