# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat 和 Responses、Anthropic 兼容 Messages，以及原生 DashScope 协议。所有接口均支持多地域部署与业务空间专属域名，开发者可根据现有技术栈选择最适配的接入方式。

## 支持的模型/功能

Qwen 系列模型（如 `qwen4-max`、`qwen3.8-plus`、`qwen3.7-flash`、`qwen3-vl-plus`、`qwen3-coder-flash`）是核心支持对象，同时兼容第三方直供模型（如 `deepseek-v4.1-flash`、`kimi-k3.1-pro`、`glm-5.3`、`MiniMax-M2.5`）。不同协议对模型能力的支持存在差异：

- **OpenAI 兼容 Chat**（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）支持标准 `chat/completions` 流式/非流式调用，但明确不支持 `Qwen-Audio`（仅 DashScope 协议支持）；
- **OpenAI 兼容 Responses**（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）提供增强能力：内置联网搜索、网页抽取、代码解释器、文搜图、知识库检索等[工具调用](../concepts/tool-calling.md)，且支持 `previous_response_id` 实现无状态多轮对话管理；
- **Anthropic 兼容 Messages**（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）支持 `thinking` 块、结构化输出（`output_config`）及显式缓存（`cache_control`），但 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同；
- **DashScope 原生协议**（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）是底层统一协议，区分文本（`text-generation`）与多模态（`multimodal-generation`）服务端点，支持 `Qwen-Audio` 及更细粒度的输入控制（如 `image` 对象内嵌 `max_pixels`）。

> **注意**：文档 1 与文档 8 在模型列表描述上存在不一致——文档 1 称“Qwen-Audio 不支持 OpenAI 兼容协议”，而文档 8 明确将其列为 DashScope 协议支持模型。该差异属实，应以文档 8 为准：Qwen-Audio 仅可通过 DashScope 协议调用。

## 关键参数

| 参数 | 协议支持 | 说明 |
|------|----------|------|
| `model` | 全部 | 必填。需使用百炼控制台实际开通的模型 ID（如 `qwen3.8-max`），非列表中模型可能受限于 Agent 能力（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。 |
| `messages` / `input` / `content` | 各协议对应字段 | OpenAI Chat 与 DashScope 使用 `messages` 数组；Responses API 支持 `string` 或 `array` 格式的 `input`；Anthropic 使用 `messages` + `content` 结构化数组。多模态输入（图像/音频/视频）在各协议中字段名与嵌套层级不同（如 Chat 中为 `image_url`，Anthropic 中为 `image`，DashScope 中为 `image`）。 |
| `max_tokens` | Responses、Anthropic、DashScope | 含义因协议而异：在 Anthropic 协议中，对 `qwen4-max` 等模型表示“回复+思考”总长度上限；在 Responses 中为纯输出上限；在 DashScope 中需结合 `parameters.max_output_tokens` 使用。 |
| `store` | Responses 专属 | 布尔值，设为 `true` 才可后续通过 `response_id` 调用 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md) 或 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)。 |
| `x-dashscope-session-cache: enable` | Responses 专属 | 请求头参数，启用服务端自动上下文缓存，降低多轮延迟，无需修改业务逻辑。 |

## 使用方式

### 地域与认证
所有协议均采用统一的业务空间域名模式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。API Key 通过 `Authorization: Bearer <key>`（OpenAI/Anthropic）或 `x-api-key`（Anthropic）或 SDK 自动注入（DashScope）传递。

### 接入路径对比
- **OpenAI Chat**：`/compatible-mode/v1/chat/completions` —— 适合已集成 OpenAI SDK 的用户，快速迁移；
- **OpenAI Responses**：`/compatible-mode/v1/responses` —— 适合需工具链、多轮状态管理、结果持久化的生产场景；
- **Anthropic Messages**：`/apps/anthropic/v1/messages` —— 适合已有 Anthropic 生态（如 Claude 工具）的用户；
- **DashScope**：`/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态）—— 适合追求最大灵活性与底层控制的用户。

> **注意**：文档 4 明确指出 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移到 `/compatible-mode/v1/responses`，否则功能不可保障。

## 限制和注意事项

- **上下文长度**：Responses API 为内置工具预留约 20% 上下文缓冲区，实际可用输入长度约为模型窗口的 80%，超出部分将静默截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；
- **缓存机制**：OpenAI Chat 协议不支持显式缓存断点；DashScope 与 Anthropic 协议支持 `cache_control`（仅 `qwen4-max` 支持 `ttl`）；Responses API 通过 `x-dashscope-session-cache` 头实现会话级自动缓存；
- **多模态细节差异**：
  - 图像精度控制：Chat 协议通过 `image_url.detail`（`high`/`low`/`auto`）设置，DashScope 协议通过 `image.max_pixels` 设置；
  - 视频输入：Chat 协议支持 `video_url`（含 `fps`）与 `video`（图片列表）两种形式；Responses 协议仅支持 `input_video`（单 URL）；Anthropic 协议支持 `video` 类型内容块；
- **错误处理**：`response_id` 相关操作（获取、删除、查询输入项）均要求原始请求中 `store=true`，否则返回 `not found` 错误（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)、[获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)）；
- **计费单位**：`created_at` 字段在 Responses API 的 `list-input-items` 接口返回毫秒级时间戳，而 `retrieve-a-response` 返回秒级时间戳，日志分析时需注意单位差异。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


