# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障推理性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用协议：

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：提供 `/chat/completions`（标准对话）和 `/responses`（增强 Agent 能力）两类端点。其中 `/responses` 是百炼特有扩展，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库搜索等工具，且支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存。详见 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)。
- **Anthropic 兼容接口**：提供 `/v1/messages` 端点，支持 `system` 消息、结构化输出（`output_config.format`）、深度思考（`output_config.effort`）及工具调用（`tools` + `tool_choice`），适用于从 Claude 生态迁移的场景。[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 文档详细说明了与官方 API 的关键差异。
- **DashScope 原生接口**：提供 `/text-generation/generation`（纯文本）和 `/multimodal-generation/generation`（多模态）两个专用端点，对图像、视频、音频等输入格式控制更细粒度（如 `max_frames`、`vl_high_resolution_images`），是调用 `Qwen-Audio` 等非 OpenAI 兼容模型的唯一途径。[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 明确了其输入结构与模型映射规则。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生 API 调用（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。而 OpenAI 兼容的 `/chat/completions` 接口明确声明不支持该模型。

## 关键参数

所有协议共有的核心参数包括：
- `model`：必填，指定模型 ID（如 `qwen3.8-max`、`qwen3-vl-plus`），不同协议支持的模型范围略有差异（例如 `/responses` 专有列表见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- `messages` / `input`：必填，承载对话上下文；OpenAI `/chat/completions` 和 DashScope 使用 `messages` 数组；OpenAI `/responses` 支持更灵活的 `input` 字符串或结构化数组。
- `stream`：布尔值，控制是否启用流式响应。

协议特有关键参数：
- **OpenAI `/responses`**：`previous_response_id`（串联多轮）、`tools`（内置+自定义工具）、`reasoning.effort`（思考强度）、`store`（是否持久化响应供后续引用）。
- **Anthropic `/messages`**：`max_tokens`（语义因模型而异，需特别注意 glm-5.2 等模型对 `thinking.budget_tokens` 的处理逻辑）、`output_config.effort`（替代已废弃的 `thinking.budget_tokens`）、`tool_choice`（精细控制工具调用策略）。
- **DashScope**：`min_pixels` / `max_pixels` / `total_pixels`（图像/视频像素控制）、`fps`（视频抽帧率）、`max_frames`（视频帧数上限，仅 DashScope 支持）。

## 使用方式

1. **认证与域名配置**：  
   所有请求均需在 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头中传入百炼 API Key。**强烈建议使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性（该建议在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)、[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中多次强调）。

2. **SDK 与 HTTP 调用**：  
   - OpenAI SDK：配置 `base_url` 为对应地域的兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），然后调用 `client.chat.completions.create()` 或 `client.responses.create()`。
   - Anthropic SDK：配置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`，调用 `client.messages.create()`。
   - DashScope SDK：配置 `base_http_api_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`，再按模型类型选择 `TextGeneration.call()` 或 `MultiModalConversation.call()`。

3. **辅助操作接口**（仅 `/responses` 协议提供）：  
   - `GET /responses/{response_id}`：检索已完成响应（[获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)）。
   - `DELETE /responses/{response_id}`：删除已存储响应（[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）。
   - `GET /responses/{response_id}/input_items`：获取某次响应所依赖的全部输入项（含历史轮次，[获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)）。

## 限制和注意事项

- **协议兼容性边界**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**仅处理文档明确列出的参数**，未提及的 OpenAI 参数（如 `/responses` 的 `background`）会被忽略；`/chat/completions` 不支持 `Qwen-Audio`，而 `/responses` 对非直供模型的 Agent 能力有限制（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **上下文与 [Token](../concepts/token.md) 限制**：`/responses` API 为预留工具调用空间，实际可用输入上下文约为模型窗口的 80%（自动截断，不报错）；`/chat/completions` 的 `max_tokens` 在不同模型下语义不同（如 `glm-5.2` 下其含义取决于是否传 `thinking.budget_tokens`），务必查阅对应模型文档。
- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek）**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；旧版 URL `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移至 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **数据格式细节**：DashScope 的 `video` 字段支持 `string`（单文件 URL）或 `array`（图片列表），而 OpenAI `/chat/completions` 统一使用 `type: "video_url"` 或 `type: "video"` 的对象结构；`/responses` 的 `input` 中 `input_audio`/`input_video` 仅限 `qwen3.8-omni-flash`，且 `fps` 必须为数字而非字符串（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


