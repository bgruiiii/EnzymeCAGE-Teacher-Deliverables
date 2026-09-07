# 为什么近期出现多轮修正

这些多轮并不是“任务没有开展”或“同一模型一直训练失败”，而是在真实组件逐步接入时，本地独立审计发现返回包
的实现、证据或状态声明不能支持直接放行。我们选择修正后再进入下游，以免错误PASS进入完整智能体后更难定位。

## 1. T1：输入合同与真实代码版本不一致

早期冻结回归要求完整反应输入，但当前胶水层只使用底物侧输入。如果直接按文件名判断，会把不同语义的结果混为
同一基线。因此先重建full-reaction合同，再修pool上限、CPU入口和wrapper metadata，最终形成可复现的staged
基线。这不是模型失效，而是版本和输入语义必须先对齐。

## 2. T2：先缺owner资产，后补运行与验收门

### 2.1 最初卡点：生成器资产不完整

最初远端分支缺少任意单SMILES fresh generation所需的完整模板、语料、donor index和模型资产，固定93案例pool
不能替代生成器。我们先定位缺件并向owner请求bundle。师兄补齐后，本地核到manifest 30/30，才开始真实adapter。

### 2.2 核心模型能力其实较早已成立

非固定池Benzotriazole技术smoke已真实生成48个候选并返回Top-10，USPTO、enviPath和retrieval三个来源及三个
LightGBM ranker均进入运行。后续返修主要不是重新训练模型，而是修运行安全与验收真实性。

### 2.3 为什么继续出现R1—R4

本地审计依次发现：

```text
初包：没有runtime资产SHA门；所谓depth2没有实际进入第二层；CLI漏初始化；模型执行事实和93池计数误报；
R1：首次身份门已加，但同root资产变化会复用旧cache；8项mutation没有逐项隔离；validator复用构建clone；
R2：生产cache与ancestor逻辑改善，但cycle测试是恒真表达式，访问日志仍记录bound method；
R3：真实cycle和cache恢复已修，但交付访问日志与fresh报告复用了R2旧文件，部分计数是硬编码0；
R4：T2B主合同功能门已经满足；新增高级access audit自身递归产生283万行，故只作限制记录，不再阻塞T2C。
```

因此当前结论是：T2B技术adapter已经可用于下一步staged接线，但不能把R4的高级访问审计宣传为正式闭合，也
不能把技术smoke写成科学准确率结论。

## 3. T5：性状证据边界比“查到一个菌名”复杂

T5反复修正主要发生在UID→source identity、host evidence来源枚举、跨步骤supporting enzyme合并、route order、
trait precedence/conflict和真菌缺失fail-closed等边界。这些修正是为了防止：

```text
物种级信息冒充原始菌株观测；
代表菌株冒充酶来源菌株；
预测性状覆盖观测性状；
同一宿主的多个步骤被错误合并；
真菌缺数据时套用原核预测；
性状被误用于hard filtering或未经授权的综合分数。
```

目前T5可写成staged合同链通过，但真实多步整链仍要等待T2/T3输入后复验。

## 4. T4不是返修问题，而是权威输入缺失

T4要求同一份、答案隔离、身份冻结的正式18条blind输入。本地已有历史18条小测试gold/schema，但没有证据证明
它就是老师本轮指定的T4输入。擅自替换会导致不同模型不在同一口径比较，因此保持`BLOCKED_INPUT_MISSING`。

## 5. 当前采取的原则

```text
核心功能达到老师合同门后允许带限制进入下一stage；
后加的增强型审计工具若有瑕疵，记录限制但不无限返修；
文件名或执行方自报PASS不能代替本地审计；
技术smoke不外推为科学准确率；
staged结果不外推为production完成；
缺老师指定输入时如实报告，不自行替代。
```
