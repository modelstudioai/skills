# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的推理模型，一次前向计算即可返回分类、是非判断、有序评分及其概率分布与置信度，**不生成文本输出**。适用于工单分流、内容审核、智能体完成度校验、任务路由等低延迟、高确定性要求的场景。其接口协议遵循 TypeSafe System One 规范，详见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`（预览版），无其他变体或历史版本。
- 支持三类结构化问题：
  - `choice`：多选一判定（如“派单团队”），返回选中选项、各选项概率及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断，返回 `P(yes)` 概率值（浮点数，0–1）；
  - `score`：有序量表打分（如严重度 1–4 级），返回概率加权期望等级索引（可为小数）及各级概率分布。
- 所有类型均返回完整 `probabilities` 分布，`choice` 和 `score` 额外返回 `confidence` 字段；`noul` 不提供置信度（因本身即概率输出）。
- 一次请求最多支持 **16 个问题**，模型对全部问题并行处理，结果原子性返回。更多能力细节请参考 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | 是 | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | Body | 是 | 待决策的原始业务上下文（如工单文本、对话 JSON、结构化对象），将被序列化后送入模型 |
| `questions` | `Object` | Body | 是 | 键为问题 ID（字符串），值为问题对象；每个问题对象含 `type`（`choice`/`noul`/`score`）、`instructions`（可选描述）、`criteria`（按类型定义） |
| `Authorization` | `String` | Header | 是 | `Bearer $DASHSCOPE_API_KEY`，API Key 须配置为环境变量或显式传入 |
| `Content-Type` | `String` | Header | 是 | 必须为 `"application/json"` |

> **注意**：`criteria` 字段格式严格依赖 `type`：  
> - `choice`：`{"option_key": "description"}` 映射（建议补 `other` 兜底项）；  
> - `noul`：仅需 `instructions`，`criteria` 字段**被忽略**（文档中虽列出但实际不生效）；  
> - `score`：`["level_0_desc", "level_1_desc", ...]` 字符串数组（索引即等级）。  
> 此行为已在 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 的示例与返回结构中验证，旧版文档若声称 `noul` 支持 `criteria` 属于过时描述。

## 使用方式

- **SDK 调用（推荐）**：
  - Python：使用 `dashscope>=2.0.1`，调用 `client.decision.create(...)`；
  - Java：使用 `dashscope-sdk-java>=2.23.3`，通过 `DecisionModel` 类调用；
  - SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。
- **通用 TypeSafe SDK**：安装 `typesafe-sdk`，设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one(...)`。
- **curl 直连**：需手动替换 `{WorkspaceId}` 和地域域名，Header 中携带 `Authorization` 与 `Content-Type`，Body 为标准 JSON。
- **在线调试**：优先使用 [Playground](https://bailian.console.aliyun.com/systemone_playground)（见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)），支持预设场景快速验证逻辑与概率分布。

## 限制和注意事项

- **上下文长度**：最大 `65536` token，超长 `state` 将直接拒绝（HTTP 400），不截断。
- **问题规模**：
  - 单次请求最多 16 个问题；
  - `choice` 选项数 ≤ 255；
  - `score` 等级数 2–255（**强烈建议 3–7 级**，过多等级易导致概率分散、置信度下降）。
- **性能特征**：延迟与问题数量近似线性增长，与输出长度无关（因无文本生成）。
- **错误处理**：Python SDK 抛出 `DashScopeError`，Java SDK 抛出 `ApiException`；通用错误码说明见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。
- **地域与 Endpoint**：必须显式指定 `region`（如 `cn-beijing` 或 `ap-southeast-1`），不同地域 endpoint 域名不同，不可混用。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


