# R1返修交主窗口复审（只审修正项+数值SHA）

## 请先跑的机器核对
1. `approved_numeric/`17件 vs 本包`APPROVED_ARTIFACTS_REGISTER.tsv` vs review/ACCEPTED_NUMERIC_IDS——8件已通过件应逐字节等于BASE原文件；BASE目录本身未被触碰（mtime/SHA）。
2. B修正：`internal_R1B_CHECKS.json`全真可独立重推——重点：22名单与review F01逐UID相等；5579=5601−22；`identified_microbe_source_for_followup`谓词可由B1原列直接复算；`ambiguity_flag_not_recoded`证明229未改判；SOURCE_SET 7未被并入"全球不可判种"。
3. D修正：`internal_R1D_CHECKS.json`；请抽查`CASE_EXPORT_PROTOCOL_FIELDS_R1.tsv`三轴与R4工具源码真实字段一一对应（schemas.py/predict.py/pool.py/retrieval_backends.py/traits_backends.py引用已给行段）；轴A的NOT_AVAILABLE标注是否覆盖了"冻结池验证运行无召回记录"的事实；示例是否仍SCHEMA_ONLY、两RAW覆盖声明是否诚实。
4. 覆盖附录降级：确认CHANGELOG与回复稿不再称V1覆盖表为最终判定B；F02的596差异未被掩盖。
5. E：`LIMITATIONS_CONFIRMATION_Q66Q78_R1.json`为真断言（对照release decision原件）；CHECKS中3c构成为84=60+24。

## 残余未知（不变，无需再审为新项）
C接线前提（授权/代码线/输入合同/GPU窗口）；整链真实案例未运行；V6占位H原子的解析全通过无UNKNOWN；师姐正式覆盖率由她计算。

未发送、未上传、未push、未改main/228/掩码/B1。通过后请按裁定一次性反馈师姐并统一更新GitHub交付。
