# BIOSYSMOdb150 G8-P2 Kimi K3 121题正式回包本地审计

日期：2026-10-08  
方式：本地只读、零API调用；不修改原回包、历史gate或模型答案。

## Findings

### F1（高）：两个非可用槽均不得重跑

Kimi 121个正式槽全部已经提交，120个有终态，119个可用，`NOT_DISPATCHED=0`。

- `G8P2-K106 / BIOPATH150_128`：HTTP 200、完整SSE、`finish=length`、completion=65,536、
  reasoning正文文件约211 KB、visible=0；属于模型思考耗尽总输出预算。
- `G8P2-K042 / BIOPATH150_050`：先落`DISPATCH_COMMITTED`，客户端shutdown后仅留请求体，
  无raw/provider request ID；状态为`RESULT_UNKNOWN_HELD_NEVER_RESENT`。

老师合同禁止因length、空正文或JSON内容失败重问；本轮又冻结为每题一次、零自动重试和at-most-once。
前者是模型内容终态，后者可能已经到达服务端，均不能补发或用探针答案替换。若以后做复现实验，只能
作为独立supplement，不得改变正式121题分母。

### F2（中）：五个system fingerprint必须在最终报告披露

120个终态响应均返回exact model=`kimi/kimi-k3`，但分布在5个fingerprint：

| fingerprint | 终态 | 可用 | 平均秒 | completion均值 |
|---|---:|---:|---:|---:|
| `fpv0_3f6baf1f` | 24 | 24 | 779.7 | 32,155.8 |
| `fpv0_c96a51ed` | 20 | 20 | 849.3 | 34,462.7 |
| `fpv0_cabe88c9` | 30 | 30 | 880.4 | 35,497.9 |
| `fpv0_df2f7ec7` | 30 | 30 | 796.3 | 31,999.9 |
| `fpv0_e8884bc8` | 16 | 15 | 888.0 | 41,941.2 |

这可能反映后端副本/版本路由，不能仅凭字符串断定模型版本实质改变。五组无系统性格式退化，唯一
length出现在`e8884bc8`组。G9应保留fingerprint字段，并至少报告按fingerprint的样本量、可用率和
token/耗时，不在见到科学分后选择性剔除任何组。

### F3（中）：身份记录声称的“用户明确豁免”不准确

`provenance/uploads/IDENTITY_GATE.md`写用户明确说过“这两个不是必要的 不需要了”，据当前本地会话
记录，该逐字引语没有得到确认；此前本地回复只说明缺少两个辅助件可由直接实算tar身份替代。
这是authority/provenance表述错误，应由本地审计更正，不能继续引用为用户原话。

实际身份门不依赖该引语：正式源tar SHA、内嵌121输入SHA、成员卫生、内部SHA和121个Kimi body
均已独立实算。因此该问题不影响调用或答案真实性，也无需重跑。

### F4（低）：回包含旧tmp账本与锁文件

权威`ledger/kimi_calls.json`为121 committed、435.86014元；`kimi_calls.json.tmp`为旧的42次、
139.579元快照。`.runner.lock`和`kimi_calls.json.lock`未列入内部SHA，但外层tar SHA绑定全包。
后续只读权威`.json`并忽略`.tmp/.lock`；未来packager应排除这些运行时文件。

## 回包身份与可复现性

```text
file=biosysmodb150_g8p2_kimi_k3_121_formal_return_20261007T141621Z.tar.gz
bytes=117,802,093
sha256=e17504af6c2927e9ba37c9f31eb0ec75aa346bfdc1ac28badd213fbcdf31e34c
members=1,804
uncompressed_bytes_about=2,347,397,120
```

- 无绝对路径、`..`、重复成员、链接或设备。
- 顶层`SHA256SUMS`独立复核1,638/1,638通过；`audit/SHA256SUMS`为268/268通过。
- 内部SHA覆盖全部实质文件；仅SHA自身和两个运行锁文件未覆盖，外层tar SHA覆盖全包。
- detached replay逐字节复现`G8_P2_KIMI_PARTIAL_AUDITED`、completion matrix和RUN_REPORT；
  integrity=0。
- 未检出API key或Bearer凭证形态。

## 输入、调用与参数合同

```text
FORMAL_SLOTS=121
FORMAL_COMMITTED=121
TERMINAL=120
RESULT_UNKNOWN_HELD=1
NOT_DISPATCHED=0
RETRIES=0
PROBE_ANSWERS_ADOPTED=0
```

新矩阵与原四模型输入包的121个Kimi行case顺序完全相同；121个request body逐字节相等，零差异。
请求均为`kimi/kimi-k3`、64K、temperature=0、search=false、stream/include_usage=true，且无任何
thinking/reasoning/repetition控制字段。121份slot status均含合法ISO UTC `committed_utc`；120个
provider request ID全部唯一；响应model字段全部为精确ID。

usable使用原始visible直接`json.loads`，不剥代码围栏。本轮只有K106直接JSON失败，原因是visible
为空；无围栏答案被“救活”。形态检查为degenerate=0、extra warnings=0、repeat=0。

## 正式结果与预算

```text
KIMI_TERMINAL=120/121
KIMI_USABLE_JSON=119/121 (98.35%)
KIMI_LENGTH_OR_EMPTY=1/121
KIMI_REPEAT=0/121
KIMI_HELD=1/121
```

正式`BIOPATH150_007`与`015`均一次成功，说明旧pilot故障未在正式对应槽复现；探针答案没有混入。

120个终态的实测均值：835.053秒/题，中位808.275秒，P90 1,273.652秒，最大1,614.841秒；
completion均值34,641.6。串行终态耗时合计约27.835小时。按20/100元每百万token核算并含held
最坏预留，权威账本估算435.86014元，低于独立1000元硬顶。

## 重跑与阶段结论

```text
RERUN_KIMI_LENGTH_1=false
RERUN_KIMI_RESULT_UNKNOWN_1=false
RESUME_NOT_DISPATCHED=0
KIMI_API_COLLECTION_CLOSED=true
```

Kimi正式API采集可以关闭。后续只做离线四模型合并、固定分母评分、fingerprint分层披露与人工形态
复核；不得用pilot、探针或补跑答案填补K050/K106。
