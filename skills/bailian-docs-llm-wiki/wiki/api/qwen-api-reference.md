# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈偏好（如 OpenAI/Anthropic 兼容性）或功能需求（如联网搜索、代码执行）选择合适接口。所有接口均需通过 API Key 认证，并遵循统一的配额与计费规则。

## 支持的模型与功能

当前 Qwen 模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）可通过以下四类接口调用：

- **OpenAI 兼容 Chat Completions**：适用于已有 OpenAI 客户端的应用迁移，支持标准 `messages` 格式和流式响应。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses**：在基础 Chat Completions 上增强，**自动集成联网搜索、代码解释器和网页内容提取工具**，并隐式管理对话历史，无需手动传入 `messages` 历史。该能力文档见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出，适用于需要可控推理链或复杂工具编排的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：提供最全参数控制（如 `top_k`、`repetition_penalty`、`enable_search` 显式开关），是调试与高阶定制的首选。

> **注意**：`OpenAI 兼容 Responses` 接口虽自动启用联网搜索，但其 `enable_search` 参数不可显式设置；而 DashScope 接口中该参数为布尔值且必须显式指定。二者行为不一致，建议生产环境优先使用 DashScope 接口以确保可预测性。

## 关键参数

通用关键参数（各接口均有对应字段，命名略有差异）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 必填，如 `"qwen-max"`；不同接口对模型别名支持不同，请以实际返回的 `models.list` 为准 |
| `messages` | array | 对话历史，格式为 `[{ "role": "user", "content": "..." }]`；`OpenAI 兼容 Responses` 接口会忽略此字段的历史维护逻辑 |
| `temperature` | number | 控制随机性（0.0–2.0），默认 `1.0` |
| `max_tokens` | integer | 生成内容最大 token 数，非请求总长度限制 |
| `stream` | boolean | 是否启用流式响应（SSE），默认 `false` |

DashScope 接口特有参数（如 `top_k`、`stop`、`incremental_output`）详见其专属文档。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`  
2. **Endpoint 示例**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **SDK 调用**：推荐使用官方 `dashscope` Python SDK（v1.20.0+），自动适配接口类型与重试策略。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system/user/assistant 内容）上限为 32768 tokens（Qwen2 系列模型），超限将返回 `400 Bad Request`。
- `OpenAI 兼容 Responses` 接口不支持 `functions` / `tools` 字段，工具调用仅通过内置能力触发，无法自定义工具 schema。
- 所有接口均**不支持跨模型 session 共享**：`session_id` 仅在同模型、同接口内有效，切换模型需重建上下文。
- 流式响应中，`OpenAI 兼容 Responses` 的 `delta.content` 可能包含工具调用中间结果（如搜索摘要），而 DashScope 接口的 `output.text` 仅返回最终生成文本。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


