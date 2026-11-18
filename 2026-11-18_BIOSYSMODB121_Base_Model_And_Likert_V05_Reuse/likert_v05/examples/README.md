# 合成接口示例

本目录所有数据都标为SYNTHETIC，仅用于不联网验证接口。没有真实题面、原答案或Gold，也不是模型真正返回的分数。

| 文件 | 用途 |
|---|---|
| `synthetic_item.json` | 七维评分材料接口；包含预先准备的范围、匿名身份和虚拟引用目录 |
| `synthetic_request.json` | 真实请求构建函数对上述示例装配的body及SHA；仅离线，不发送 |
| `synthetic_response.json` | 人工构造的输出格式fixture；测试用整数，不代表科学评价 |
| `synthetic_merged.json` | 原公式复算示例，D4=MISSING=1保留权重 |
| `synthetic_repair_baseline.json` | 仅D3a为旧NE的七维基线 |
| `synthetic_repair_request.json` / `synthetic_repair_response.json` | 只补D3a，演示另外六维不变 |

身份由程序生成后精确回显；合成请求被live入口明确拒绝，不能通过把API key设好就意外买一次示例评分。
