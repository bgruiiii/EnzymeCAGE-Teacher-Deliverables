# Fig.3 统一返包 R1：仅B/D字段与说明返修（本地CPU，2026-11-23）

对`review/REVIEW_REPORT.md`的定向返修。数值零重算：A/3a/3b/第六规则/12匹配步等**逐字节复制**于`approved_numeric/`并登记来源SHA；review目录只读引用未改；BASE包未改（其RUNEND在清单后被改写一项如实留在CHANGELOG）。

## 包内容
- 修正B：`UID_SPECIES_TRACE_7468_R1.tsv`（7468行，三列+一标志+谓词+定位）、`SPECIES_FIELD_DICTIONARY_AND_JOIN_PROTOCOL_R1.tsv`（采用列答案）、`SPECIES_TRACE_STATUS_COUNTS_R1.tsv`（5579基线；22占位单列；601/5607等分层；C8非门）；V1覆盖表降级为广义对照附录（原字节保留）。
- 修正D：`CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv`（三证据轴+可用性标注，NOT_AVAILABLE不硬凑）、`CASE_EXPORT_RUN_CONTRACT_R1.json`（run_id/mode推导/GOLD_NOT_AVAILABLE/性状后端状态契约）、`CASE_EXPORT_EXAMPLE_SCHEMA_ONLY_R1.json`（三轴示例，RAW覆盖范围如实限定，未生成新案例）。
- 收口：CHANGELOG、E真断言`LIMITATIONS_CONFIRMATION_Q66Q78_R1.json`、CHECKS（3c按实际84=60+24校验、恒真检查删除）、RUNEND先于MANIFEST、INPUTS/MANIFEST。
- 脚本：`scripts/s7_r1b_fields.py`、`scripts/s8_r1d_protocol.py`（s6终装配在BASE，本包由assemble_r1.py）。

## 关键数字（机器检查全真）
7408已识别物种 / 22占位 / 30 no-hit / 7 source-set / 1冲突 = 7468；5601记录基础层保留；**5579=follow-up基线**；1798 false层与trace层并存获确认；229歧义flag未被改判；已通过区间与掩码SHA与review登记一致。
