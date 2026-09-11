# 本地老师审阅包验证摘要

日期：2026-09-11

## 验证范围

本文件验证本GitHub老师审阅包的结构、所含两个原始archive、审计材料与关键证据是否可读取和按SHA追溯。它不冒充R2执行器缺失的external validation，也没有重跑GPU、模型或当前老师graph。

## 两个原始archive

```text
R1 checkpoint:
gzip=PASS
single root=PASS
members=397
regular files=368
unsafe paths=0
links/special=0
MANIFEST.sha256=367/367 PASS
archive SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf

R2 technical completion:
gzip=PASS
single root=PASS
members=183
regular files=156
unsafe paths=0
links/special=0
MANIFEST.sha256=155/155 PASS
archive SHA256=6844b68ac782c51556e91d77cba7c3f5f12e4e1c679a270fbcdc97ad49c3b162
```

## 两段运行关系

```text
R1=第一次模型返回，保存E0—E7和stage8前检查点
R2=更换模型后从R1继续§8-B
R2 RESUMED_FROM_CHECKPOINT_SHA256=50efeafdc175141a947ce27be3cf5953bb8892a8b40aca4e9be3ab3e96cf4fdf
E0_E7_RERUN=false
```

因此，E0—E7不是缺失或未运行，而是按R2续跑合同位于第一次返回的检查点中。本包同时包含R1/R2原包，并把19项E0—E7关键文件展开到`evidence/e0_e7/`。

## 内容门

```text
teacher authority files=present
teacher-facing decision request=present
teacher requirement compliance matrix=present, 27 rows
E0-E7 checkpoint evidence index=present, 19 rows
R1 local independent audit=present
R2 local independent audit=present
reusable runtime recipe=present
timing attribution=present
executor-error attribution=present
asset reuse plan=present
key R2 graph/test/smoke/C8 evidence=present
T6_OVERALL_READY=false
G7_PASSED=false
```

## 未闭环项

```text
R2 original external identity=MISSING_LOCAL
R2 original external validation=MISSING_LOCAL
TEST-01—20=not all independently established
C8→T5 graph-native continuous=not established
enviPath lookup then depending=not established
source provenance=fail
task-ID public contract=fail
original scientific mutation coverage=incomplete
teacher adjudication=required
```

这些缺口已保留为FAIL/PARTIAL，不因GitHub封包而改写成PASS。
