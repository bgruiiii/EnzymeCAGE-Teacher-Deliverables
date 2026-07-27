# M3-P1-2.1 反应预测器 A/B/C 老师展示版 HTML 本地独立审计

审计日期：2026-07-26（Asia/Shanghai）  
审计对象：
`M3_P1_2_1_REACTION_PREDICTOR_ABC_ROUTE_TEACHER_PRESENTATION_2026-07-26.html`  
对象 SHA256：
`8353d05aec21d7a8c8c47061ba960d39fee20693b69d30a481cef883511d0a84`  
结论：**PASS FOR OFFLINE TEACHER PRESENTATION / FACTS CONSISTENT / NO EXECUTION AUTHORIZATION**

## 1. 文件定位与用途

HTML 与详细 Markdown 选择卡同目录，作为刘老师会前的可视化展示层：

```text
01_Path_Contract_Objective/M3_P1_PreTeacher_Adjudication_2026-07-26/
M3_P1_2_1_REACTION_PREDICTOR_ABC_ROUTE_TEACHER_PRESENTATION_2026-07-26.html
```

证据权威来源仍是：

```text
M3_P1_2_1_REACTION_PREDICTOR_BIOLOGICAL_ROUTE_SELECTION_CARD_2026-07-26.md
ENZYMECAGE_M3_P1_2_1_THREE_ROUTE_ANSWER_KEY_UNLOCK_AND_TARGET_SCORING_LOCAL_AUDIT_2026-07-26.md
```

HTML 只改变信息展示方式，没有修改 A/B/C 原始输出、答案钥匙、评分政策或机器报告。

## 2. 正式选择框架审计

页面顶部、导航、推荐区和正式勾选区均以黄老师原始 A/B/C 为主框架：

```text
A:
  专业反应预测工具
B:
  LLM 生成候选 reaction SMILES
C:
  规则库/已知降解路径模板
```

刘老师正式勾选区只有 A/B/C 三项。页面没有把 R1/R2 提升为主选项。

## 3. 关键数字一致性

### 3.1 统一门禁

| 页面数字 | 权威结果 | 审计 |
|---|---|---|
| 解锁前 25/25 | 25/25 PASS | PASS |
| 独立重算 43/43 | 43/43 PASS | PASS |
| 评分器反向测试 6/6 | 6/6 PASS | PASS |
| 当前可直接生产路线 0 | 没有一路 production ready | PASS |

### 3.2 Route A

```text
valid case execution:
  6/6
raw products:
  26
RDKit parse:
  25/26
parseable-subset diagnostic case hit:
  4/6，醒目标注“非正式分数”
full reaction:
  none
formal verdict:
  NOT SCOREABLE / contract incompatible
```

页面没有删除或修复 RP-P06 的不可解析产物，也没有把 4/6 写成正式 Top-K。

### 3.3 Route B

```text
ChatGPT-labelled predictions:
  24
DeepSeek-labelled:
  9
Qwen-labelled:
  26
total:
  59
RDKit parse and substrate-left retention:
  59/59
```

模型评分：

| 模型标签 | Top-1 | Top-3 | Top-5 |
|---|---:|---:|---:|
| ChatGPT-labelled | 4/6 | 5/6 | 5/6 |
| DeepSeek-labelled | 4/6 | 4/6 | 4/6 |
| Qwen-labelled | 4/6 | 4/6 | 5/6 |

页面明确 `Top-5=5/6` 只指 diagnostic 主要产物，不指完整反应、Rhea、EC 或正确酶。
模型版本继续写成用户界面标签，不冒充 API attestation。

### 3.4 Route C

```text
Rhea raw/searchable:
  36,014 / 36,012
correct directed Rhea Top-1/3/5:
  4/6, 5/6, 6/6
full reaction Top-5:
  6/6
target non-null frozen Rhea EC:
  5/6
D4-valid pool nonempty:
  4/6
```

页面明确：

- C-exact 是已知 Rhea 查表 baseline，不是未知反应预测；
- Paraoxon/Carbaryl 虽正确 Rhea rank 1，但冻结 Rhea→UniProt 映射为空；
- Carbaryl 冻结 Rhea EC 继续保持 `null`；
- C-generic 仍为未建立、未运行、未评分、`NOT_READY`。

## 4. 优缺点和决策含义

页面为每条路线分别展示：

```text
本轮实际测试对象
关键实测数字
优点
缺点/风险
选择后下一动作
production 锁
```

学生推荐 B 被明确写成“下一阶段研究方向”，没有写成刘老师已选择或黄老师已授权。
C-exact 被建议保留为已知反应守门层，但没有冒充所选预测 fallback。

## 5. R1/R2 身份隔离

R1/R2 位于独立虚线视觉区域，并在区域顶部和底部重复标注：

```text
学生侧/Codex 建议
不是黄老师原始 A/B/C
未执行
未评分
没有 Rhea/EC/酶池成绩
未获老师授权
不得冒充 A/B/C 已完成结果
```

页面建议顺序是：若正式选择 B，R2 完整反应 blind pilot 优先，R1 已知 Rhea
有方向桥接仅作附加工程实验。该顺序被标作建议，不是实测结论。

## 6. HTML 技术结构审计

```text
doctype:
  html5
charset:
  utf-8
external JavaScript:
  none
external CSS:
  none
external image/font dependency:
  none
offline open:
  yes
responsive breakpoints:
  900px / 620px
print stylesheet:
  A4
```

使用 `lxml.etree.HTMLParser(recover=False)` 解析：

```text
root:
  html
parser errors:
  0
section ids:
  10
unique section ids:
  10
navigation links:
  10
missing navigation targets:
  0
tables:
  2
details blocks:
  1
```

当前环境未安装 Chromium/Firefox/WeasyPrint 等图形渲染器，因此没有生成像素级截图；
结构、导航目标、离线依赖和 CSS 响应/打印规则已完成静态验证。打开浏览器后的最终字号
与打印分页仍建议由用户在实际展示设备上快速目视一次。

## 7. 索引和哈希

HTML 已加入：

```text
FILE_INDEX.md
M3_NEXT_ROUND_PRETEACHER_MASTER_INDEX_AND_DECISION_STATUS_2026-07-26.md
PRETEACHER_SELECTION_PACKAGE_SHA256SUMS.txt
```

选择包哈希清单执行 `sha256sum -c` 后必须包含本 HTML 的 `OK`。

## 8. 最终结论

```text
A/B/C main-choice fidelity:
  PASS
numeric consistency:
  PASS
product/full-reaction/enzyme boundary:
  PASS
C-exact/C-generic separation:
  PASS
R1/R2 non-executed labeling:
  PASS
offline self-contained structure:
  PASS
HTML parser:
  PASS, 0 errors
production authorization:
  NO
```

该 HTML 可以作为老师会议展示入口；正式裁定和科学证据仍以对应 Markdown、机器报告和
独立审计为准。
