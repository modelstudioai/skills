# decision model

决策模型是百炼平台提供的专用推理服务，基于 System One 协议实现单次前向调用即可同步输出分类标签、置信度评分、是非判断（yes/no）及对应概率分布，适用于风控审核、内容分级、策略路由等确定性判别场景。其设计目标是低延迟、高可解释性与结构化输出，不支持生成式文本续写。该能力由独立部署的 `decision-model` 系列模型提供，与通用大模型（如 qwen-max）在架构和接口协议上严格分离。

## 支持的模型/功能

- 当前可用模型包括 `decision-model-preview`（预览版），已上线模型能力、上下文长度（最大 8K tokens）、输入格式约束及计费粒度详见 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md)。
- 核心功能：一次性返回三类结构化结果——`category`（预定义类别字符串）、`score`（0.0–1.0 浮点数）、`binary_decision`（`"yes"` 或 `"no"`），以及各结果的 `confidence` 字段（同为 0.0–1.0）。
- 不支持多轮对话、流式响应、工具调用或自定义 [prompt](../guides/prompt.md) engineering；所有逻辑由模型内部决策头固化，用户仅通过 system [prompt](../guides/prompt.md) 提供任务描述与类别定义。

## 关键参数

- `input`: 必填，字符串类型，为待决策的原始文本（不可嵌套 JSON 或含控制字符）。
- `system`: 必填，字符串类型，用于声明决策任务与输出类别，例如 `"你是一个内容安全审核员，请判断以下文本是否包含暴力内容。输出类别只能是 'violence' 或 'non-violence'。"`。
- `temperature`: 固定为 `0.0`，不可修改；模型始终以确定性模式运行。
- 其他采样参数（如 `top_p`, `max_tokens`）无效，调用时传入将被忽略 —— 此行为与 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的协议定义一致。

## 使用方式

通过百炼 Model API 调用，HTTP 方法为 `POST`，Endpoint 为 `/v1/models/decision-model:predict`（预览期使用 `/v1/models/decision-model-preview:predict`）。请求体为标准 JSON：

```json
{
  "input": "这个视频展示了持刀威胁他人。",
  "system": "判断文本是否含暴力内容，仅输出 'violence' 或 'non-violence'。"
}
```

响应体包含 `category`、`score`、`binary_decision`、`confidence` 四个顶层字段，无 `choices` 或 `usage` 字段。完整请求/响应示例见 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 限制和注意事项

- 输入 `input` 长度上限为 8192 tokens；超出部分将被截断且**不触发报错**，仅静默处理 —— 请务必在客户端完成长度校验。
- `system` 字段中定义的类别必须明确、互斥且为 ASCII 字符串（不支持 emoji、空格、中文类别名）；若类别定义模糊（如 `"positive/negative/neutral"` 但未说明判定标准），模型行为不可预期。
- > **注意**：原始文档中 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 标注“支持 16K 上下文”，但实测与 [决策模型 API 参考](../../raw/model-api-reference/decision-model/decision-model-api.md) 均确认当前仅支持 8K。请以 API 实际行为为准，16K 为未来规划版本，尚未上线。

## 来源文档

- [决策模型](../../raw/model-api-reference/decision-model.md)


