# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等高频、低延迟、强确定性的业务场景。其接口协议遵循 TypeSafe System One 标准，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或版本别名。
- 支持三类结构化问题类型：
  - `choice`：多选一决策（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如“是否需升级”），返回 P(yes) 概率值（浮点数，0.0–1.0）；
  - `score`：有序量表评分（如“严重度 1–4 级”），返回概率加权期望等级索引（可为小数）及各级概率分布。
- 所有类型均返回完整 `probabilities` 分布，`choice` 和 `score` 额外返回 `confidence`（0.0–1.0），便于下游做阈值过滤或结果融合。

> **注意**：文档中多次强调该模型“不生成文本”，与通用大语言模型（LLM）的文本生成范式有本质区别；若业务需要生成解释性文本，请勿误用本模型，可参考 [通用模型 API](../../raw/model-api-reference/llm/llm-api.md)。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | `String` | 必填 | 固定为 `"decision-model-preview"` |
| `state` | `String` / `Object` / `Array` | 必填 | 待决策的原始业务上下文（如工单 JSON、对话文本等），将被序列化后送入模型；超长（>65536 token）将被拒绝 |
| `questions` | `Object` | 必填 | 键为自定义问题 ID，值为问题对象；最多支持 **16 个问题**（延迟近线性增长） |

问题对象（`questions[key]`）字段：
- `type`：必填，取值 `"choice"` / `"noul"` / `"score"`
- `instructions`：可选，自然语言描述问题意图或评判标准
- `criteria`：按类型区分：<br> • `choice`：`{ "key": "desc" }` 映射（≤255 项，建议含 `"other"` 兜底）<br> • `noul`：可选 `{"true": "...", "false": "..."}` 描述（非必需）<br> • `score`：`["level0 desc", "level1 desc", ...]` 数组（2–255 级，**强烈建议 3–7 级**且语义可清晰区分）

更多细节请参阅 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的“请求参数”章节。

## 使用方式

### SDK 调用（推荐）
- **Python**：使用 DashScope SDK ≥2.0.1，调用 `client.decision.create()`  
- **Java**：使用 DashScope SDK ≥2.23.3，使用 `com.alibaba.dashscope.decision` 包  
- SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL  

### 通用 HTTP 调用
- 协议：`POST /compatible-mode/v1/systemone`
- Header：`Authorization: Bearer $DASHSCOPE_API_KEY`，`Content-Type: application/json`
- Body：符合上述参数结构的 JSON 对象  
- 各地域 endpoint 见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的“请求地址”节

在线调试推荐使用 [Playground](https://bailian.console.aliyun.com/systemone_playground)，支持预设场景快速验证逻辑与输出格式。

## 限制和注意事项

- **问题数量限制**：单次请求最多 16 个 `questions`，超出将报错；实际部署中建议控制在 8 个以内以保障延迟稳定性。
- **上下文长度**：`state` 序列化后总 token 数不得超过 **65536**，超限直接拒绝（非截断）。
- **选项与等级规模**：
  - `choice` 选项数 ≤ 255，但过多选项会显著降低判别精度，建议 ≤ 10 项并提供明确语义区分；
  - `score` 等级数建议 **3–7 级**，超过 7 级易导致相邻等级概率混淆，影响 `score` 输出可解释性。
- **SDK 版本强依赖**：旧版 DashScope SDK（Python <2.0.1 / Java <2.23.3）**完全不支持** `decision` 接口，调用将抛出 `AttributeError` 或 `ClassNotFoundException` —— 此限制已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中明确标注。
- **无流式响应**：该模型仅支持同步阻塞式调用，不支持 `stream=true` 或 SSE 流式返回。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


