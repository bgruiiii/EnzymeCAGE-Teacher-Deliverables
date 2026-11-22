# R4真实评分采用结论（2026-11-22）

采用：独立复核14项关键检查全部通过，无需再跑GPU。两个预先固定的评分池分别为S02 `BIOPATH150_001__S02__BSY-r00595` 13个候选、S03 `BIOPATH150_013__S03__BSY-r00201` 31个候选，全部真实评分且未丢候选。五seed共220个概率值，直接平均一次，与44个输出分数一致到1e-15；排序为(-score,uid)，Top10仅显示前缀。

核对了目标反应/model key、冻结UID顺序/序列SHA、已有档案身份、CPU原生资产可用性、7模块/5checkpoint/pool起止回执。复核只读本地材料，未重新加载模型或生成资产。原v1缺项来自其索引范围，不能再称项目整体缺资产。

与C2比较仅作信息性对照：S02名次13/13一致，最大概率差5.86084226150696e-8；S03名次31/31一致，最大概率差7.442257873302438e-7。不以此宣称whole-step与bounded16协议等同，也不更改原数值门。

失败尝试1–5和成功attempt6全部留存。attempt1/2的失败可从stdout/归档读取；本地并无各自独立FAIL.json，不要求补造。END是在进程内取的GPU快照；执行者另报退出后释放，本地主审未重新连接节点核当前资源。不影响已保存评分结论。

R4源码的适配只接已有CURRENT95索引，补齐overlay视图的values只读探针；未更改底层文件。其临时绑定在单进程初始化完成后恢复；并发服务部署需由维护者处理，不能据此称已部署main。

随包提供按实际worker路径整理的原生配置示例；该配置不是一次新CLI端到端运行的凭证。此次新增验收范围是两个固定池的真实评分，检索/来源/性状沿用此前各自已核材料。未知反应/酶真缺件仍由已有生成工具按需处理；自动补建回填未接默认分支。

[独立机器核查](../evidence/tool_r4/INDEPENDENT_CHECKS.json)、[完整尝试记录](../evidence/tool_r4/native_results/)、[实际worker与登记](../evidence/tool_r4/return_sources/scripts/)、[R4源码](../tools/standalone/)、[原生配置示例](../tools/standalone/config_examples/tool_config_chenyu_native_c95.json)。

原三张微生物论文表直接采用，四个消费输入SHA未变。原五组分数、Gold、池和历史数值限制不变；main合并/部署由黄老师决定。
