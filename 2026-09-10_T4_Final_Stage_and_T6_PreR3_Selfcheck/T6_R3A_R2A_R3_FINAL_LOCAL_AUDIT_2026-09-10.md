# T6-R3A-R2A-R3 clean external validation顺序与三文件封口返回本地审计

日期：2026-09-10
审计方式：本地只读独立核验；另在`/tmp`复制archive重放clean closure；未修改原返回包；未运行模型/T6-R3

审计对象：

```text
03_HPC_Returned_Result_Summaries/
enzymecage_three_module_t6_r3a_r2a_r3_clean_external_validation_order_three_file_final_20260910.tar.gz

bytes=146872
SHA256=14c6b3ab04b7306eed2c52ece849039a37dfab8245ef48a5335df3faa32a494b
```

## 1. 裁定

```text
LOCAL_AUDIT_VERDICT = PASS_T6_R3A_MICROBE_SELFCHECK_AND_CLEAN_EXTERNAL_CLOSURE
ARCHIVE_SAFETY = PASS
ARCHIVE_MANIFEST = PASS_50_OF_50
CONTENT_PRESERVED_FROM_R2A_R2 = PASS_34_OF_34_NONWHITELIST
ARCHIVE_INTERNAL_STATUS = PASS_HONEST_EXTERNAL_PENDING
CLEAN_CLOSURE_MUTATIONS = PASS_12_OF_12
LOCAL_CLEAN_CHAIN_VALIDATION_ABSENT_AT_START = true
LOCAL_CLEAN_CHAIN_PREWRITE = PASS_12_OF_12
LOCAL_CLEAN_CHAIN_POSTWRITE = PASS_10_OF_10
LOCAL_CLEAN_CHAIN_FINAL_READONLY = PASS
EXTERNAL_THREE_FILE_DELIVERY_RECEIVED_LOCALLY = PASS
EXTERNAL_IDENTITY = PASS_ARCHIVE_BYTES_SHA_ROOT_FILES
EXTERNAL_VALIDATION = PASS_P12_OF_12_Q10_OF_10_OVERALL
RERUN_REQUIRED = false
ACTION_REQUIRED = NONE_FOR_THIS_SELFCHECK_CLOSURE
T6_R3_EXECUTED = false
T6_OVERALL_READY = false
G7_PASSED = false
TEACHER_SELFCHECK_SENT = false
```

本轮的clean closure实现和三文件本地收件均已通过；不再需要写新prompt或在chenyu重跑。

注意：这只表示T6进入R3前的microbe/fallback/证据自查封口完成，不表示真实T6-R3、20项终验或G7已经完成。

## 2. Archive和内部状态

```text
gzip=PASS
single root=PASS
members=53
regular files=51
directories=2
unsafe members=0
MANIFEST.files=51/51
MANIFEST.sha256=50/50
sha256sum -c=50/50 PASS
```

archive内部正确写：

```text
T6_R3A_R2A_R3_CONTENT_READY_FOR_EXTERNAL_VALIDATION
CONTENT_PRESERVED_FROM_R2A_R2=true
PACKAGE_INTERNAL_EVIDENCE_CONSISTENCY=PASS
EXTERNAL_VALIDATION=PENDING_AT_ARCHIVE_TIME
EXTERNAL_THREE_FILE_DELIVERY=PENDING_AT_ARCHIVE_TIME
T6_R3_EXECUTED=false
T6_OVERALL_READY=false
G7_PASSED=false
```

这与archive打包时事实一致，没有提前伪造sidecar PASS。

## 3. R2内容未漂移

`R2_CONTENT_NONMUTATION.json`记录：

```text
R2 baseline files=44
nonwhitelist checked=34
mismatches=[]
overall=PASS
```

固定scientific evidence、patch、Path、M1—M8、G-SCHEMA、155项矩阵均未改。R3只更新README/AUTHORITY/STATUS/LOG/manifest和新增clean closure脚本/报告。

## 4. Clean closure实现正确

正式`r3_clean_closure.py`顺序：

```text
拒绝pre-existing validation；
pre-write P01—P12；
validation.open("x")首次独占创建；
post-write Q01—Q10；
atomic replace封口；
final-readonly只读确认。
```

P12显式检查validation及`.tmp/.partial/.failed/.bak`全部不存在。archive内部不提前写external PASS。

## 5. Mutation证据

包内：

```text
mutations=12/12 PASS
clean_chain.validation_absent_at_start=true
clean_chain.validation_not_touched_before_prewrite=true
clean_chain.pre_pass=12
clean_chain.post_pass=10
clean_chain.readonly=PASS
```

覆盖prewrite预置空validation、缺identity、坏identity SHA、archive篡改、坏M2、旧fallback hash、坏G-SCHEMA、SKIP、写后删除validation、少P门、伪P12和引用旧sidecar。

本地重新运行同一harness：

```text
mutations=12/12
clean_chain=PASS
exit=0
```

## 6. 本地独立clean-chain重放

为排除包内自报，在`/tmp`复制archive并新建identity；确认validation不存在后执行包内closure：

```text
validation_absent_before=true
pre=12
post=10
readonly=PASS
readonly_exit=0
closure_exit=0
```

最终validation中：

```text
P12 measured：validation及四种临时路径全部false（写前不存在）
Q01—Q10全部PASS
POSTWRITE=PASS_10_OF_10
OVERALL=PASS
EXTERNAL_STATUS=T6_R3A_R2A_R3_CLEAN_EXTERNAL_CLOSURE_READY_FOR_LOCAL_AUDIT
EXTERNAL_THREE_FILE_DELIVERY=PASS
final-readonly所有检查=true
```

说明closure逻辑已真实关闭，不需再返工。

## 7. 三文件最终收件

本地已收到同basename三个regular non-symlink实物：

```text
identity archive bytes=146872
identity archive SHA256=14c6b3ab04b7306eed2c52ece849039a37dfab8245ef48a5335df3faa32a494b
identity root和regular_files=当前task/51
validation P=12/12
validation Q=10/10
OVERALL=PASS
final-readonly=PASS
```

identity与落盘archive独立复算一致；validation记录P12写前不存在、Q01—Q10全PASS和当前run-id/nonce。T6-R2A-R3外置交付状态正式本地收件PASS。

## 8. 老师反馈边界

当前先不发送中间汇报，按用户要求等待T4和T6相关封口都完成后一次性发黄老师。

最终反馈必须区分：

```text
microbe direct REST/map fallback/TaxID/host evidence自查=完成并审计；
T6-R3真实LangGraph invoke/stream=未运行；
C8→T5真实连续回归=未运行；
20项终验/G7=未通过。
```

不得把本轮external closure PASS写成T6 overall PASS。
