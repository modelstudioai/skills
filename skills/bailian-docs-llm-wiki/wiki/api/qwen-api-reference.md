# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope 接口。所有接口均支持多地域部署、业务空间专属域名和统一的 API Key 认证机制，开发者可根据现有技术栈和功能需求选择合适协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理、Agent 工具调用等能力：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3.8-omni-flash`（音视频端到端）、`qwen3-vl-plus`、`qwen-vl-max`、`qwen3.7-vl` 等；
- **第三方模型**：DeepSeek（v4 系列）、GLM（5.x）、Kimi（k3/k2.7-code）、MiniMax（M2.5/M2.1）等，其中三方直供模型**仅在中国站华北2（北京）地域可用**，且需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)；
- **特殊能力**：
  - OpenAI 兼容 Responses API 内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具，详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
  - Anthropic 兼容 Messages API 支持结构化 JSON 输出（需传入 `output_config.format.type = "json_schema"`）与深度思考控制（`output_config.effort`）；
  - DashScope 原生接口区分 `text-generation` 与 `multimodal-generation` 服务路径，适配不同输入类型 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生接口调用；QwQ 模型不建议设置 system message，QVQ 模型的 system message 不生效 —— 这些限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中表述一致，无矛盾。

## 关键参数

| 参数 | 类型 | 说明 | 所属接口 |
|------|------|------|----------|
| `model` | `string` | 必选。模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`。注意：OpenAI Chat 与 Responses 接口支持的模型列表存在差异，Responses 明确列出 `qwen3.8-omni-flash` 等 Omni 模型，而 Chat 文档未包含该型号，建议以 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 为准。 | 所有接口 |
| `messages` / `input` | `array` / `string|array` | 必选。对话上下文。OpenAI Chat 和 DashScope 使用 `messages` 数组；Responses 支持 `string`（纯文本）或 `array`（消息数组），更灵活。 | Chat / Responses / DashScope |
| `stream` | `boolean` | 可选，默认 `false`。启用[流式输出](../concepts/streaming-output.md)。所有接口均支持。 | 所有接口 |
| `temperature` | `number` | 可选。控制生成多样性。**OpenAI 接口范围为 `[0, 2)`，Anthropic 接口明确强调此范围与官方 `[0.0, 1.0]` 不同**，需迁移时注意校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 | OpenAI / Anthropic |
| `max_tokens` | `integer` | 必选（Anthropic）、可选（OpenAI）。语义因模型而异：对 `qwen3.8-max` 等，它限制回复+思考总长度；对多数模型仅限回复长度。详见各文档参数说明。 | OpenAI / Anthropic |
| `fps` | `float` | 可选。视频抽帧频率（默认 `2.0`），支持 `0.1–10`。DashScope 和 OpenAI Chat 均支持，但 Responses 接口未提及，应视为不支持。 | Chat / DashScope |
| `min_pixels` / `max_pixels` | `integer` | 可选。图像/视频帧像素缩放阈值，用于保障多模态输入质量。三类接口均有定义，但具体默认值和取值范围存在细微差异（如 `qwen-vl-plus` 图像 `min_pixels` 在 Chat 文档中为 `4096`，在 DashScope 文档中亦为 `4096`，一致）。 | Chat / Responses / DashScope |

## 使用方式

### 1. 域名与认证
- **统一域名格式**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 为业务空间 ID（控制台获取），`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。
- **推荐迁移**：华北2（北京）、新加坡、中国香港地域已上线业务空间专属域名，性能与稳定性更优，**强烈建议从旧域名 `dashscope.aliyuncs.com` 迁移** [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic）请求头传入百炼 API Key，需先完成 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 2. 接口选择指南
- **OpenAI 兼容 Chat**：适用于标准对话场景，路径 `/compatible-mode/v1/chat/completions`，兼容 `openai` SDK 的 `chat.completions.create()`。
- **OpenAI 兼容 Responses**：适用于需要 Agent 能力（内置工具）、简化上下文管理（`previous_response_id`）、Session 缓存（`x-dashscope-session-cache`）的复杂任务，路径 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages**：适用于已使用 `anthropic` SDK 的应用，路径 `/apps/anthropic/v1/messages`，支持 `output_config.effort` 等扩展参数。
- **DashScope 原生接口**：适用于追求最大灵活性或需细粒度控制（如 `max_frames`）的场景，路径分 `text-generation` 与 `multimodal-generation`，SDK 需配置 `base_http_api_url`。

### 3. 多轮对话
- **Responses API**：推荐使用 `previous_response_id`（自动拼接历史）或 `conversation`（会话级管理）；
- **Chat API**：需手动维护 `messages` 数组；
- **Anthropic API**：依赖 `messages` 数组顺序，无专用 ID 机制。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在华北2（北京）地域可用**，且需在控制台单独开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **协议兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)**不支持部分原生参数**（如 `background` 异步执行），且仅处理文档明确列出的参数，其余将被忽略 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **旧版路径停用**：OpenAI Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，**必须迁移至 `/compatible-mode/v1/responses`** [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **缓存与计费**：`vl_high_resolution_images=true` 时，`max_pixels` 参数失效，系统强制使用更高分辨率上限（如 `16777216`），可能显著增加 Token 消耗与费用。
- **音频/视频支持**：`qwen3.8-omni-flash` 是目前唯一在 Responses API 中明确支持 `input_audio` 和 `input_video` 类型的模型；其他模型需通过 Chat 或 DashScope 接口调用。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


