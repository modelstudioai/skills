# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接入方式。所有接口均需通过百炼平台鉴权，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（具体可用模型以控制台为准）。各接口支持的功能略有差异：

- **OpenAI 兼容 Chat Completions**：支持标准 `chat/completions` 请求，适用于迁移 OpenAI 应用；但[不原生支持工具调用的结构化响应](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)，需自行解析。
- **OpenAI 兼容-Responses**：内置联网搜索、代码解释器等工具链，自动维护对话历史；其行为与标准 OpenAI 接口存在差异，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)。
- **Anthropic 兼容-Messages**：支持 `messages` 格式请求，完整兼容 Anthropic 的 `tool_use` 和 `thinking` 机制；注意该接口对 `system` 字段的处理逻辑与 DashScope 不同，详见 [原文标题](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope**：百炼原生接口，支持最全参数（如 `top_p`、`repetition_penalty`、`enable_search`），且是唯一支持流式响应中返回工具调用中间步骤的通道；推荐新项目优先选用。

> **注意**：`qwen-max` 在 DashScope 接口中默认启用增强推理模式，但在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中该能力被禁用——此行为差异已在 [原文标题](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中明确说明，但未在 OpenAI 文档中同步更新。

## 关键参数

| 参数名 | 类型 | 说明 | 接口支持情况 |
|--------|------|------|--------------|
| `model` | string | 必填，如 `"qwen-max"` | 全部支持 |
| `messages` | array | 对话历史，格式为 `[{ "role": "...", "content": "..." }]` | 全部支持（Anthropic 接口要求 `role` 为 `"user"`/`"assistant"`/`"tool"`） |
| `tools` | array | 工具定义列表（JSON Schema） | DashScope、Anthropic、OpenAI-Responses 支持；标准 OpenAI Chat Completions **不支持** |
| `tool_choice` | string/object | 控制工具调用策略 | 仅 DashScope 和 Anthropic 支持；OpenAI-Responses 使用隐式调度 |
| `stream` | boolean | 是否启用流式响应 | 全部支持，但 OpenAI-Responses 的流式字段命名与标准 OpenAI 不一致 |

## 使用方式

1. 获取 API Key：登录百炼控制台 →「API 密钥管理」创建密钥；
2. 设置请求头：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`；
3. 发送 POST 请求至对应 endpoint（例如 DashScope：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）；
4. 解析响应：非流式返回 `output.text`；流式响应需按 SSE 格式逐 chunk 解析。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（含系统提示与工具描述），超限将返回 `400 Bad Request`；
- 工具调用最大嵌套深度为 3 层（即 tool → tool → tool），超出将被截断；
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的 `max_tokens` 实际表示输出 token 上限，而 DashScope 接口的 `max_tokens` 表示总上下文 token 上限（输入+输出），此差异易引发误用；
- 所有接口均不支持跨会话状态共享；若需长程记忆，请自行实现 history 缓存或使用百炼提供的对话服务（非本 API 范畴）。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


