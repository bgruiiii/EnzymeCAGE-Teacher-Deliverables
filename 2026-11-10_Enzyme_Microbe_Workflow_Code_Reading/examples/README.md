# 合成字段示例

本目录所有记录均为**SYNTHETIC**，只解释字段与关系，不来自真实题目／Gold／模型输出，不代表生物学有效路径、酶活性、菌株性状或端到端运行。

- [given_path.synthetic.json](given_path.synthetic.json)：t6有序节点链输入，拆步预期只表示相邻字符串关系；不携带任意DAG。
- [rankings.synthetic.tsv](rankings.synthetic.tsv)：沿真实评价表头演示`step_id/runtime_uid`，不填真实Gold标记。
- [host_trait.synthetic.json](host_trait.synthetic.json)：说明来源／性状证据分层，值是假设占位，不供runtime当实测。

三个例子不是同一次系统运行的联合产物。没有现役胶水时，不把格式示例拼成科学端到端演示。
