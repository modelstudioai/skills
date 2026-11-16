# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 Qwen 模型调用方式，包括 OpenAI 兼容的 Chat 和 Responses API、Anthropic 兼容的 Messages API，以及原生 DashScope API。所有接口均支持多地域部署、多模态输入（文本/图像/音频/视频）和高级功能（如工具调用、显式缓存、深度思考）。开发者可根据现有技术栈选择最适配的协议，无需修改核心逻辑即可迁移。

## 支持的模型/功能

Qwen 系列模型在百炼平台以商业版与开源版双轨提供，覆盖通用语言理解（`qwen-plus`, `qwen3.7-max`, `qwen4-max`）、代码生成（`qwen3-coder-flash`）、多模态理解（`qwen3-vl-plus`, `qwen3.8-omni-flash`）、数学推理（`qwen-math`）及语音处理（`qwen-audio`）等场景。第三方直供模型（如 DeepSeek、Kimi、GLM、MiniMax）亦受支持，但需注意地域限制：三方模型**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

功能层面，三大协议能力存在差异：
- **OpenAI Chat Completions**：轻量级对话接口，支持标准 messages 格式，但**不支持 Qwen-Audio 的 OpenAI 兼容协议**，仅可通过 DashScope 协议调用 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI Responses API**：增强型接口，内置联网搜索、网页抓取、代码解释器等工具，并支持 `previous_response_id` 简化多轮上下文管理与 `x-dashscope-session-cache` 自动缓存 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic Messages**：兼容 Anthropic 协议，支持结构化 `tool_use`/`tool_result` 交互、`thinking` 深度推理块及 `cache_control` 显式缓存断点，适用于需要精细控制思考过程的场景 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：文档 1 与文档 8 对 `qwen-audio` 的支持描述存在矛盾。文档 1 明确指出“Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议”，而文档 8 在模型列表中包含 `千问Audio` 但未强调此限制。应以文档 1 为准，即 `qwen-audio` 仅能通过 DashScope API 调用。

## 关键参数

核心参数因协议而异，但模型标识、输入格式与性能控制是共性重点：

- **`model`**：必选字符串，值需严格匹配控制台发布的模型 ID（如 `qwen4-max`, `qwen3.8-omni-flash`, `deepseek-v4.1-flash`）。不同协议支持的模型范围有差异，例如 Responses API 明确列出 `qwen4-max` 等数十个型号，而 Anthropic Messages 还额外支持 `qwen3-coder-flash` 和 `qwen3-vl-plus` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

- **多模态输入**：
  - *图像*：Chat Completions 使用 `{"type": "image_url", "image_url": {"url": "...", "detail": "high"}}`；DashScope 使用 `{"image": "https://...", "detail": "high"}`；Anthropic 使用 `{"type": "image", "source": {"type": "url", "url": "..."}}`。
  - *视频*：Chat Completions 与 DashScope 均支持 `video_url`（文件）和 `video`（图像列表），但 DashScope 额外提供 `max_frames` 参数控制抽帧上限，而 OpenAI 兼容 API 不支持该参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。
  - *音频*：仅 Responses API 和 DashScope 支持 `input_audio` 或 `audio` 字段，Chat Completions 不支持。

- **性能与控制**：
  - `temperature`：取值范围为 `[0, 2)`，**与 Anthropic 官方的 `[0.0, 1.0]` 不同**，迁移时需校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
  - `max_tokens`：语义因模型而异。对 `qwen4-max` 和 `deepseek-v4` 系列，它限制“回复内容 + 思考过程”的总长度；对其他模型（如 `qwen-plus`），仅限制回复内容 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
  - `reasoning.effort`（Responses）或 `thinking.type`（Anthropic）：用于开启/关闭深度思考，部分模型（如 `qwen4-max`）默认开启。

## 使用方式

所有 API 均基于业务空间专属域名，需将 `{WorkspaceId}` 替换为控制台获取的真实 ID。**强烈建议使用新域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），因其提供更高性能与稳定性，旧域名（如 `https://dashscope.aliyuncs.com`）虽仍可用但已不推荐 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**（Chat & Responses）：
  - `base_url` 统一为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。
  - Chat endpoint：`POST /chat/completions`。
  - Responses endpoint：`POST /responses`（新版路径，旧版 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用）[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
  - 认证：通过 `Authorization: Bearer <API_KEY>` 请求头。

- **Anthropic 兼容接口**：
  - `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`。
  - Endpoint：`POST /v1/messages`。
  - 认证：支持 `x-api-key` 或 `Authorization: Bearer` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

- **DashScope 原生接口**：
  - `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1`。
  - Endpoint 分模型类型：纯文本用 `/services/aigc/text-generation/generation`，多模态用 `/services/aigc/multimodal-generation/generation` [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。
  - 认证：SDK 中配置 `api_key` 与 `workspace`，HTTP 调用需 `Authorization` 头。

## 限制和注意事项

- **地域与模型绑定**：三方直供模型（DeepSeek/Kimi/GLM/MiniMax）仅限华北2（北京）地域，且需在控制台单独开通；Qwen-Audio 仅支持 DashScope 协议，不支持 OpenAI 兼容 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **上下文长度**：Responses API 为预留工具调用空间，实际可用上下文约为模型窗口的 80%，超出部分自动截断而不报错 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **缓存与计费**：`min_pixels`/`max_pixels` 影响图像/视频 Token 计算，`max_pixels` 最大值为 `16777216`（`qwen4-max`）；显式缓存（`cache_control`）仅 `qwen4-max` 支持 `ttl`（`5m`/`1h`）[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **Response 生命周期**：`GET /responses/{id}` 和 `DELETE /responses/{id}` 仅对创建时 `store=true` 的响应有效；`GET /responses/{id}/input_items` 返回的 `created_at` 时间戳单位为**毫秒**，与其他接口的**秒**单位不同 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


