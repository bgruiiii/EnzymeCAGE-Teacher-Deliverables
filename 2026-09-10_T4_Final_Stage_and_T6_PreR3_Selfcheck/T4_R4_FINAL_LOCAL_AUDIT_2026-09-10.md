# T4-R4 clean external closure与三文件最终返回本地审计

日期：2026-09-10
审计方式：本地只读独立核验；未运行模型、评分、重合或OOF；未修改原返回包

审计对象：

```text
enzymecage_three_module_t4_r4_clean_external_closure_order_three_file_final_20260910.tar.gz
bytes=301515
SHA256=022ac616aa97bbe33cab49194a1647b8c253734e12bd0617b99241498cfb28b7

identity SHA256=2ed6a6383b327289ef54657c0e2f70434e6dbdcb12fa076a61254f209dd0b69a
validation SHA256=e25a9d6359fefaa924b186f69463b32289d79ba754263eb793c5efdc2b2fa31a
```

## 1. 最终裁定

```text
LOCAL_AUDIT_VERDICT = PASS_T4_FINAL_CONTENT_AND_EXTERNAL_THREE_FILE_CLOSURE
ARCHIVE_SAFETY = PASS
ARCHIVE_MANIFEST = PASS_75_OF_75
IDENTITY = PASS_ARCHIVE_BYTES_SHA_ROOT_FILES
CONTENT_GATES = PASS_C01_TO_C20
PREWRITE_GATES = PASS_P01_TO_P09
POSTWRITE_GATES = PASS_Q01_TO_Q08
V23 = PASS_25_OF_25
V23_MUTATIONS = PASS_8_OF_8
CLOSURE_MUTATIONS = PASS_10_OF_10
R3_NONWHITELIST_CONTENT = PASS_58_OF_58_BYTE_IDENTICAL
MODEL_RERUN = false
RAW_PREDICTIONS_CHANGED = false
METRICS_CHANGED = false
STRICT_UNSEEN_BLIND_EVALUATION = NOT_ESTABLISHED
CURRENT_METRICS = VALID_RUNTIME_BLIND_IN_DOMAIN_RECOVERY
MODEL_ROLE_DECISION = AWAITING_HUANG_TEACHER_REVIEW
T6_INDEPENDENT_AND_NOT_BLOCKED_BY_T4 = true
RERUN_REQUIRED = false
```

T4正式18条的模型运行、评分、训练重合审计、报告事实和外置交付现已全部封口。无需T4-R5，不再因标题、格式或其他P2事项返工。下一步是将中立A/B裁定请求和三文件提交黄老师，由老师决定接受当前runtime-blind in-domain口径还是另发strict held-out/OOF协议。

## 2. Archive与三文件

```text
gzip=PASS
single root=PASS
members=80
regular files=76
directories=4
unsafe members=0
MANIFEST.files=76/76
MANIFEST.sha256=75/75
```

identity独立匹配：

```text
archive bytes=301515
archive SHA256=022ac616aa97bbe33cab49194a1647b8c253734e12bd0617b99241498cfb28b7
single root=当前T4-R4 task
regular files=76
```

validation：

```text
C01—C20=20/20 PASS
P01—P09=9/9 PASS
Q01—Q08=8/8 PASS
POSTWRITE_STATUS=PASS_8_OF_8
OVERALL=PASS
EXTERNAL_THREE_FILE_DELIVERY=PASS
```

P07证明validation及临时同名文件在首次写入前均不存在；Q06—Q08证明run-id/nonce/时间链和第二fresh unpack成立，关闭了R3循环依赖。

## 3. 科学与评测内容零漂移

以下固定SHA全部命中：

```text
normalized predictions=6e52ada071c0b12d36aa8490bbdcc0b9928461861432ba1be5365764d30209e4
reaction BY_ASSET=aa9e8eedc788efeb0a8ec285a2e83db1516cb16c60a092ab080d81a63a13aeda
product BY_ASSET=ac96263dadc78a0b32ca69cb85b5815e3ff5ca83d86dbd4879825d7c4dd443ba
metrics=75a50d517d25ef96aae8b35b67b8fb163788ba1b22fc8e93288bda002a138a15
ECLIPSE reaction×fold=f902c953ebe582bba941b4b88435475fd903291743dca39616edd5e58e8cf989
ECLIPSE parent×fold=b2a0e756f80030607977a02aea03ffb7d9dc8c99cfae2903a9852f52da977669
boundary matrix=e4eb988ffb274f1e1eb31c7c1a44fc2c0b6da3fd0e7a50adc3cc2d3bbd47aad2
teacher draft=9465ee87d126764746b7b8fde87b1874b03feeecd8c4b34941ad3148ba1ca964
```

独立重算：reaction/product两表均312行、312唯一键；13/39 pair、15/18 parent、16/39 product、ECLIPSE 390/180与113 hit cells保持。

R3 64个基线文件均可追踪；58个非白名单文件逐字节一致，changed_outside_whitelist=[]。变化仅为README/AUTHORITY/LOG/STATUS/manifest和R4 closure证据。

## 4. Validator与mutation

V23保持：

```text
25 explicit subchecks
clean PASS
always-true findings=0
mutations=8/8 detected
```

R4 closure mutation：

```text
10/10 detected
clean chain PASS
pre-existing sidecar never reused/deleted
no validation record written before prewrite gates pass
```

因此不是固定PASS或自引用放行。

## 5. 已披露非阻塞事故

执行端记录：一次打包命令因shell中`TASK_ID`未设置，在return root创建两个空名临时文件；正式T4-R4 archive/identity/validation当时均不存在且未被写入，临时文件随后删除，并新增canonical archive-name freshness guard。

该事件有command log与validation incident note，未污染正式三文件、科学结果或旧包，属于已关闭P2执行事故，不触发返工。

## 6. 老师审阅边界

可正式提交：

```text
T4评测结果与重合边界；
runtime-blind in-domain recovery口径；
A/B中立裁定请求；
archive/identity/validation三文件和本地审计。
```

仍不得写：

```text
strict unseen已建立；
depending或ECLIPSE主模型已由学生决定；
T4阻塞T6；
T6整体已经通过。
```
