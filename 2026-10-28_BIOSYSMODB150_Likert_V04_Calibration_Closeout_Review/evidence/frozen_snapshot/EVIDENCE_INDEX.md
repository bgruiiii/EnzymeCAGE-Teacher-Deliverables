# 统一事实证据树索引（EVIDENCE_INDEX）

- 快照ID：M4_CALIBRATION_EVIDENCE_SNAPSHOT_20261026；构建日期：2026-10-26；零网络派生。
- 组织方式：按**来源库→记录/科学对象**组织；不按答案、匿名编号或历史裁决项组织。
- 净化声明：本树只含客观来源事实（官方记录字段+raw定位+SHA+采集时间+支持范围注记）；
  不含claim级历史判定、严重度、答案分数或17项裁决关联。声称比对由评价者本人完成，
  逐精确声称登记FACT_VERIFICATION_STATUS（三态只是事实核对结果，不等于D5来源状态或关键错误）。

## 目录结构

```text
facts/IUBMB_EXPLORENZ/   EC条目事实卡（accepted name/reaction/状态/历史）
facts/NCBI_TAXONOMY/     分类记录事实卡（学名/rank/lineage/状态）
facts/NCBI_NUCCORE/      核酸记录事实卡（含suppressed等历史状态；历史存在≠当前有效≠虚构）
facts/UNIPROT/           蛋白记录事实卡（含release头未保留披露，记录级版本绑定）
facts/PUBMED/            文献书目事实卡（存在性≠支持每条子声称）
facts/BACDIVE/           菌株记录事实卡（153432/12880/13580；含义限定注记）
f7_interpretation/       F7底物面板解释层（+/-符号与测试类型原义恢复）
crosswalk/               已核实物种名称关系（别名不因字面不同直接判错）
EVIDENCE_COVERAGE_REGISTER.tsv  答案标识符→事实卡覆盖登记（含OUT_OF_SNAPSHOT_UNRESOLVED）
MANIFEST.json / SHA256SUMS      快照manifest（其SHA=evidence_snapshot_sha）与全树哈希
```

## 使用规则

1. 评价者按答案中的标识符（EC/TaxID/登录号/保藏号/PMID）在facts/下定位事实卡；
   查EVIDENCE_COVERAGE_REGISTER.tsv确认覆盖状态。
2. OUT_OF_SNAPSHOT_UNRESOLVED＝本快照未覆盖：登记UNRESOLVED提交协调端，不联网补齐，
   不判虚构也不判支持。
3. 事实卡support_scope_note说明该记录支持什么/不支持什么；不得把证据自动扩展到未声称内容。
4. F7相关判定必须先读f7_interpretation/面板与NOTES（裸名称列表≠阳性碳源清单）。
5. 两评价者使用完全相同的本证据树（逐字节一致）；评分中发现缺证按冻结资料登记待核。
