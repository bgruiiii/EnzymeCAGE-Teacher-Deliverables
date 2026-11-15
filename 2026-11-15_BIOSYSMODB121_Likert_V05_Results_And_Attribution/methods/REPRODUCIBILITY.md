# 离线复算与来源边界

在本目录执行：

```bash
python3 tools/verify_release.py
```

脚本只用Python标准库核全部SHA、726位置唯一性、723份评分与总分、共同118题、480份3360维新旧差值、加权贡献及汇总均值。无需原答案、Gold、密钥或网络。

`python3 tools/make_figures.py`可从公开CSV重建两张图（需matplotlib）。图实际采用DejaVu Serif，字体和库版本见figures/FIGURE_METADATA.json。Excel由同一组脱敏公开表生成，不含私有路径或外部数据连接。评分程序本身和本次数值复核是两个入口：[实际评分实现](https://github.com/bgruiiii/EnzymeCAGE-Teacher-Deliverables/tree/5867a2e403bcc8a4ca3720fb15ba3a877695c998/2026-11-14_Likert_V05_Scoring_Code)。

公开的私有源记录SHA、请求/System/响应SHA是对本地原件的连接，不能凭哈希恢复原始通信；原题答/完整Gold/原始wire不随此包公开。独立数字复算不等于独立生物学复审或重新重放云端服务。

发布表只删除私有路径与内部匿名ID、原件定位字段，原数值/状态不改。评分理由中的本地路径用标记替代，数据支持范围与原理由保留；评分方补证不回填成模型原引用。具体表字段见[数据字典](DATA_DICTIONARY.md)。

BIOPATH题目及参考来自项目冻结的BIOSYSMOdb v2派生资料；原数据库、论文、BacDive/官方酶库等第三方原许可/署名约束继续适用。本仓库公开研究评价派生表和必要出处，不授予原数据库或第三方全文的重新分发许可。
