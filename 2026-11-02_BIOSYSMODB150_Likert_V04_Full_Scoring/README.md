# 四模型双批评测与Likert v0.4全量阶段交付

**480/480份AI评分已得到；人类效度验证进行中。** 不是人工外部效度研究全部完成。

1. [给黄老师的报告](TEACHER_REPORT.md)
2. [任务要求逐项对照](TEACHER_REQUIREMENT_DELIVERY_MATRIX.tsv)
3. [数据表](data/) / [统计](statistics/) / [图](figures/)
   [可直接筛选的Excel总表](LIKERT_V04_TEACHER_TABLES_20261102.xlsx)
4. [人类锚点状态](human_validation/STATUS.md) / [方法与限制](methods/METHODS_AND_LIMITS.md)
5. [整体下载](archives/LIKERT_V04_FULL_SCORING_TEACHER_20261102.tar.gz)

核验：`python3 methods/verify_package.py .`（标准库，无需网络）。统计复算：安装methods/requirements.txt后，`python3 methods/analyze_public.py .`。
原475份保留，5份同模型技术澄清救援分列版本；A固定121、B共同120与共同非恢复100不混算。所有历史失败与unknown留存，不等于799次历史传输全成功。
本包只公开去标识派生评分和必要事实摘要，**不含原通信raw、密钥、私有盲映射、真实评价者声明、完整gold或许可未确认raw**。尚未完成人评者请勿阅读评分表；勿把公开结果返给盲评者。
新救援执行窗口自检未冒充另一独立复审窗口；原475份独立审计及合法总分纠算边界见报告。
