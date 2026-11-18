# 来源与移植说明

`SOURCE_MANIFEST.tsv`逐文件记录原项目相对路径、原SHA、导出SHA及变换方式；`BYTE_IDENTICAL`表示原文件逐字节导出，不表示此脚本可脱离其私有数据路径直接运行。完整目录的交付SHA另见根`SHA256SUMS`。

`code/runtime/`来自实际S6运行环境；`code/executed_workflows/`来自后续实际运行的装配、主链接线、费用/凭据、格式恢复及补证执行脚本。保留接口，不虚构它们最初就在同一个可安装包里。

`code/likert_eval/validation.py`直接抽取实际S8 `validate()`、离线恢复`normalize()`和最后使用的`normalize_response()`。只将其辅助导入接到本包common，并将`REC.normalize`接为本地同名函数；未改分档/范围/引用/身份判断逻辑。`pipeline.py`、`runner.py`和CLI是此次明确标注的相对路径I/O适配层，不冒充新的历史实跑版本。

原总分、SSE、账本、归档组件直接从导出的实际F2代码导入，没有另写一份近似公式或假的transport。

`ASSEMBLY_IDENTITY.json`记录本次整理时参考的个人教师仓库main身份。源码中保留的历史冻结状态、项目相对路径、固定case或环境常量只为保留真实实现证据；完整benchmark材料、真实盲映射、API密钥和原通信不在公开目录中。
