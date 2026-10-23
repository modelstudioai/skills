# qwen api reference

阿里云百炼平台提供多种 API 协议兼容方式调用 Qwen 系列大模型，包括 OpenAI 兼容 Responses/Chat、Anthropic 兼容 Messages 以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持多模态输入（文本、图像、音视频）、工具调用（联网搜索、代码解释器等）及高级推理控制（思考强度、结构化输出）。核心能力统一由百炼业务空间（Workspace）托管，需配置专属域名与 API Key。

## 支持的模型/功能

Qwen API 支持全系列千问模型（`qwen3.8-*`、`qwen3.7-*`、`qwen3.6-*`、`qwen3.5-*`）、Qwen-VL/QVQ 多模态模型、Qwen-Coder、Qwen-Omni 及第三方直供模型（如 `deepseek-v4.*`、`glm-5.*`、`kimi-k3`）。不同协议对模型能力的支持存在差异：

- **OpenAI 兼容 Responses API** 是首选推荐接口，专为复杂 Agent 场景设计，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库搜索等工具，并支持 `previous_response_id` 简化多轮上下文管理与 `x-dashscope-session-cache: enable` 自动会话缓存。详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **OpenAI 兼容 Chat API** 更贴近标准 OpenAI `chat/completions` 语义，适用于通用对话场景，但不支持 Responses API 的部分高级特性（如原生 `reasoning` 输出类型、`web_search_call` 结构化返回）。其 `messages` 格式与 Responses 的 `input` 数组在字段命名和嵌套层级上存在不一致。
- **Anthropic 兼容 Messages API** 提供深度思考（`thinking.budget_tokens` / `output_config.effort`）与结构化 JSON 输出（`format`）等高级能力，但仅支持 `/v1/messages` 接口，不提供模型列表查询；其 `system` 字段支持数组形式以启用显式缓存，而 OpenAI 协议中 `system` 仅作为 `messages` 的首元素。相关细节见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生 API** 是底层协议，路径为 `/api/v1/services/aigc/{text-generation|multimodal-generation}/generation`，需区分文本与多模态服务端点，且 HTTP 请求体需将 `messages` 封装在 `input` 对象内。该协议对 `max_frames` 等视频参数支持更细粒度控制，但缺少 Responses API 的 `store`/`previous_response_id` 语义。参考 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 2 明确指出 `qwen3.8-omni-flash` 支持 `input_audio`/`input_video` 类型，而文档 3 中 `Chat API` 的 `User Message` 虽也列出 `input_audio`/`video_url`，但未声明模型限制；实际使用时应以文档 2 的 Responses API 为准，因其是唯一明确标注音视频支持模型的权威来源。

## 关键参数

| 参数 | 协议支持 | 说明 |
|------|----------|------|
| `model` | 全部 | 必填。Responses API 严格限定可用模型列表（如 `qwen3.8-max`, `qwen3.8-omni-flash`），非列表中模型仅支持基础能力；Chat 和 Anthropic 协议列表更宽泛，但三方模型（如 SiliconFlow DeepSeek）仅限华北2地域且需控制台开通。 |
| `input` (Responses) / `messages` (Chat & Anthropic) / `input.messages` (DashScope) | 全部 | 输入内容。Responses 支持 `string` 或 `array`（含 `EasyInputMessage`），Chat 与 Anthropic 强制 `array`，DashScope 需包裹在 `input` 对象内。`qwen3.8-omni-flash` 在 Responses 中明确支持 `input_audio`/`input_video`；Chat 中对应字段为 `input_audio`/`video_url`，但未声明模型限制。 |
| `previous_response_id` | 仅 Responses | 多轮对话核心参数，服务端自动拼接历史上下文。不能与 `conversation` 同时使用。 |
| `store` | 仅 Responses | 控制响应是否持久化，默认 `true`；设为 `false` 时 `previous_response_id` 不可用。 |
| `stream` | 全部 | 是否[流式输出](../concepts/streaming-output.md)，默认 `false`。Responses 流式事件字段为 `response.output_text.delta`；Chat/Anthropic/DashScope 使用标准 SSE 格式。 |
| `tools` | Responses & Anthropic | 工具定义数组。Responses 支持内置工具（`web_search`, `code_interpreter`）与自定义 function；Anthropic 需声明 `web_search_20250305` 等带日期后缀的 type。 |
| `reasoning.effort` (Responses) / `output_config.effort` (Anthropic) / `thinking.budget_tokens` (Anthropic, deprecated) | Responses & Anthropic | 控制思考强度。Responses 使用 `reasoning.effort`（值如 `none`, `low`, `medium`, `xhigh`）；Anthropic 使用 `output_config.effort`（值如 `low`, `high`, `max`）或已废弃的 `thinking.budget_tokens`。 |
| `temperature`, `top_p` | 全部 | 采样参数。Anthropic 协议中 `temperature` 取值范围为 `[0, 2)`，与官方 `[0.0, 1.0]` 不同，迁移时需注意。 |

## 使用方式

### 基础接入
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台查看）；
- 使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**强烈建议迁移**，旧域名（`dashscope.aliyuncs.com`）性能与稳定性较低；
- 配置百炼 API Key（通过 `Authorization: Bearer` 或 `x-api-key` 头）。

### 协议选择指南
- **构建 Agent 应用**：优先选用 **OpenAI 兼容 Responses API**（`POST /compatible-mode/v1/responses`），因其内置工具链、上下文管理（`previous_response_id`）和缓存（`x-dashscope-session-cache`）开箱即用，大幅降低工程复杂度。
- **迁移现有 OpenAI 应用**：若仅需基础对话，可直接使用 **OpenAI 兼容 Chat API**（`POST /compatible-mode/v1/chat/completions`），但需注意其不支持 Responses 的 `reasoning` 输出类型及 `store` 语义。
- **需要深度思考或强结构化 JSON**：选用 **Anthropic 兼容 Messages API**（`POST /apps/anthropic/v1/messages`），利用 `output_config.effort` 和 `format` 实现高精度控制。
- **已有 DashScope SDK 集成**：继续使用 **DashScope 原生 API**，注意请求体结构（`input` 包裹 `messages`）及服务端点区分（`text-generation` vs `multimodal-generation`）。

### 关键操作示例
- **创建响应（Responses）**：`POST /compatible-mode/v1/responses`，传入 `model`, `input`, `tools`。
- **获取响应详情**：`GET /compatible-mode/v1/responses/{response_id}`，返回完整输出、Token 消耗、工具调用结果等，详见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。
- **查询输入历史**：`GET /compatible-mode/v1/responses/{response_id}/input_items`，用于调试多轮对话上下文拼接逻辑。
- **删除响应**：`DELETE /compatible-mode/v1/responses/{response_id}`，仅当 `store=true` 时有效。

## 限制和注意事项

- **协议兼容性**：所有 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**仅支持同步调用**，`background` 参数被忽略（文档 2 明确说明）。Requests 中未列出的 OpenAI 参数（如 `n`, `logit_bias`）将被静默丢弃。
- **上下文长度**：Responses API 为预留工具调用与推理空间，最大输入上下文约为模型窗口的 80%，超出部分自动截断（文档 2）。Chat API 无此说明，但实际仍受模型窗口限制。
- **音视频支持**：仅 `qwen3.8-omni-flash` 在 Responses API 中明确支持 `input_audio`/`input_video`；其他模型或协议下使用可能失败或降级处理。
- **缓存与计费**：`x-dashscope-session-cache: enable` 仅 Responses API 支持，且需在请求头中显式设置；`cache_control`（显式缓存）在 Chat 和 Anthropic 协议中通过 `content` 数组内嵌对象实现，二者机制与计费规则不同。
- **模型能力差异**：文档 2 强调“非列表中阿里云百炼直供文本生成模型仅支持基础兼容能力，Agent 能力（内置工具等）受限”，而文档 3 和 7 的模型列表更宽泛，但未强调此限制。开发者应以 Responses API 的模型列表为 Agent 能力上线基准。
- **API 路径迁移**：Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到新版 `/compatible-mode/v1/responses`（文档 2）。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


