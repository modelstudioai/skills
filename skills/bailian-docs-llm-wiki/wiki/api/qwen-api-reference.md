# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：适用于已使用 OpenAI SDK 的项目，可零代码迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开文本生成模型。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容 Responses（带工具增强）**：在标准 Chat Completions 基础上，自动集成联网搜索、代码解释器与网页内容提取能力，会话状态由服务端自动维护。该模式不支持自定义 `messages` 历史管理，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：支持 `tool_use`、`thinking` 等结构化输出能力，适用于需要显式推理链或复杂工具编排的场景。注意其 `system` 字段行为与 OpenAI 不同，详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：提供最完整的参数控制（如 `top_p`、`repetition_penalty`、`enable_search` 细粒度开关）、流式响应控制及私有[模型部署](../concepts/model-deployment.md)支持，是高级定制场景的首选。

> **注意**：`qwen-vl`（[多模态](../concepts/multi-modal.md)）和 `qwen-audio` 模型**不支持** [OpenAI 兼容接口](../concepts/openai-compatibility.md)，仅可通过 DashScope 原生接口调用，相关限制请参考官方[多模态](../concepts/multi-modal.md)文档。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo` | 必填 |
| `messages` | array | 对话历史，格式为 `[{ "role": "user", "content": "..." }]`；OpenAI/Anthropic 接口强制要求此字段 | — |
| `temperature` | number | 控制输出随机性，范围 `[0.0, 2.0]` | `1.0` |
| `max_tokens` | integer | 最大生成 token 数，受模型上下文长度限制 | `2048`（部分模型为 `8192`） |
| `tools` / `tool_choice` | array / object | 工具定义与调用策略，仅 DashScope 和 Anthropic Messages 支持完整语义解析 | `null` |

> **注意**：`stream` 参数在 [OpenAI 兼容接口](../concepts/openai-compatibility.md)中返回 `text/event-stream`，但在 DashScope 接口中需显式设置 `stream=true` 并处理 `SSE` 或 `JSON Lines` 格式——二者协议细节存在差异，不可混用。

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 `Bearer <your_api_key>`（DashScope）或 `Bearer <your_dashscope_api_key>`（OpenAI/Anthropic 兼容接口）；
2. **Endpoint 示例**：
   - DashScope：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`
3. **SDK 调用**：推荐使用 `dashscope` Python SDK（v1.20.0+），它自动适配多协议并统一错误码；旧版 `openai` SDK 需配置 `base_url` 为百炼 OpenAI 兼容地址。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 [prompt](../guides/prompt.md) + history）不得超过模型最大上下文窗口（例如 `qwen-max` 为 32768 tokens），超长将被截断且**不报错**；
- [OpenAI 兼容接口](../concepts/openai-compatibility.md)对 `functions` 字段的支持已废弃，应改用 `tools`（符合 OpenAI v1.0+ 规范），否则可能触发 400 错误；
- 所有接口均禁止用于生成违法、有害、歧视性内容，违规调用将触发实时风控并冻结配额；
- 流式响应中，DashScope 返回 `output.text` 字段增量更新，而 OpenAI 兼容接口返回 `choices[0].delta.content`，客户端需按协议分别解析。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


