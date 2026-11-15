# 数据字典

- LIKERT_V05_SCORES_726.tsv：一行一个(model, case)，固定每模型121位。likert_status=COMPARABLE的723行有总分，其余3行为空；program_binding_status区分正文匹配评分与工程失败按原政策记零。
- LIKERT_V05_RATINGS_723.jsonl：实际采用的七维评价正文、总分、复审标记和私有源记录SHA；是多阶段验证/复用后的合并视图，不冒称723次单轮七维重买。
- V04_V05_DIMENSION_CHANGE_3360.tsv：原四模型480×7，一行一维。delta_score=新−旧；weighted_total_delta_contribution=delta×原权重/10。approved_reference_scope_changed标记060/094的56维。
- CHANGE_ATTRIBUTION_3360.tsv：同一差值的可读理由、规则/参考/证据/执行背景和限制。attribution_labels可以多标签，不表示独立因果效应。
- FOUR_MODEL_FULL120_AND_CORE118.tsv：修正后全120视图与原118题基础参考不变视图分列。THREE_VIEW_CORE118_SUMMARY.tsv保留原三视图。
- FOUR_MODEL_DIMENSION_CHANGE_28.tsv：四模型×七维，均为同120题，含变化方向计数。
- NATIVE_RECOVERY_AND_REVIEW_SENSITIVITY.tsv：全120、共同100无原四模型恢复题、同删004后的119题；不将含累计接收的外模集合称为严格first-only。
- ANSWER_VERSION_ALIGNMENT_20.tsv：A首答与既定B恢复版不同的20位。所选B程序分在两题修正前后的列分别命名，避免把版本和参考改变混为一谈。
- PROGRAM_REFERENCE_SCOPE_CHANGE_12.tsv：同代码、同答案在旧/新参考下的五层分；本地函数调用，无新增模型采样。
- UNSCORED_POSITIONS_3.tsv：未评分原因；它们不是NE，也不默认为Likert=0。
- COUNTS.json：快照计数及已知费用估算。均值仅描述当前答卷/网关/裁判条件，不是普遍能力或显著性结论。
