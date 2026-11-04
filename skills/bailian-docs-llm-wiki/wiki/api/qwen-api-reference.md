# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

- **核心模型**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3-vl-plus`、`qwen3-coder-flash`；开源模型如 `qwen3.5-397b-a17b`、`qwen3.8-27b`；第三方模型如 `deepseek-v4.1-flash-1017`、`kimi-k3.1-pro`、`glm-5.3`。
- **多模态能力**：Qwen-VL、Qwen-Omni、Qwen3-VL 系列支持图像、视频（`video_url`/`video`）、音频（`input_audio`）输入；其中 Qwen-Omni 系列支持音视频联合理解 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **高级功能**：
  - 内置工具链：Responses API 原生支持 `web_search`、`web_extractor`、`code_interpreter`、`file_search` 等工具，无需客户端实现调度逻辑；
  - 结构化输出：Anthropic 兼容 Messages API 通过 `output_config.format` 启用 JSON 输出；
  - 显式缓存：所有协议均支持 `cache_control: {type: "ephemeral"}` 标记可复用内容块；
  - 深度思考：通过 `reasoning.effort`（Responses）或 `output_config.effort`（Anthropic）控制推理强度，`max_tokens` 行为因模型而异（详见下文关键参数说明）。

> **注意**：Qwen-Audio **不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生 API 调用 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|--------|-------------|------|
| `model` | 全协议必选 | 必须使用百炼控制台实际开通的模型 ID；OpenAI 兼容 Chat 与 DashScope 协议支持更广谱模型（含 Qwen-Audio），而 Responses 和 Anthropic 协议对模型有明确白名单限制（如 Responses 仅列 `qwen3.8-max` 等具体版本）[OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 |
| `max_tokens` | 全协议 | **行为不一致**：在 Anthropic 兼容 Messages 中，对 `qwen3.8-max`/`deepseek-v4` 等模型，该值限制「回复+思考」总长度；对 `glm-5.2`，若传 `thinking.budget_tokens` 则仅限回复长度；对多数模型（如 `qwen-plus`）则仅限回复长度。DashScope 协议中该参数未显式定义，由 `max_output_tokens` 控制。 |
| `temperature` | 全协议 | OpenAI/Responses 取值范围 `[0, 2)`；Anthropic 兼容协议明确标注其范围与官方 `[0.0, 1.0]` 不同，迁移时需校准 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |
| `fps` / `min_pixels` / `max_pixels` | OpenAI Chat & DashScope | 控制视频/图像预处理，但参数粒度存在差异：OpenAI Chat 支持 `total_pixels` 限制整体帧像素总量，而 DashScope 协议提供 `max_frames` 控制抽帧数量上限，且明确说明 OpenAI 兼容 API **不支持自定义 `max_frames`** [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。 |
| `previous_response_id` | 仅 Responses | 实现无状态多轮对话的核心参数，服务端自动拼接历史上下文；与 `conversation` 互斥，且仅当创建时 `store=true` 才生效。 |

## 使用方式

- **协议选择**：
  - 已有 OpenAI SDK 用户：优先使用 `/compatible-mode/v1/chat/completions`（标准 Chat）或 `/compatible-mode/v1/responses`（增强 Agent 能力）；
  - 需要结构化输出或深度思考精细控制：选用 Anthropic 兼容 `/apps/anthropic/v1/messages`；
  - 追求最大灵活性或调用 Qwen-Audio 等非标准模型：使用 DashScope 原生 `/api/v1/services/aigc/.../generation`。
- **接入地址**：所有协议均推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），华北2（北京）、新加坡、中国香港地域已全面支持，旧域名（`dashscope.aliyuncs.com`）仍可用但不保证长期兼容 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **认证**：统一使用百炼 API Key，通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic 协议）头传递。
- **SDK 配置示例**：
  ```python
  # OpenAI SDK (Chat/Responses)
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  # DashScope SDK
  client = dashscope.Client(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      workspace="{WorkspaceId}",
      region="cn-beijing"
  )
  ```

## 限制和注意事项

- **地域与模型绑定**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，调用前需在百炼控制台单独开通 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **上下文截断策略**：Responses API 为内置工具预留约 20% 上下文空间，输入超出模型窗口 80% 时将自动截断且**不报错**，需主动监控 `usage.input_tokens` [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **流式响应差异**：OpenAI Chat 的 `stream` 返回 `text/event-stream`；Responses API 的 `stream=true` 返回 `application/x-ndjson`；Anthropic Messages 的 `stream=true` 返回 `text/event-stream`，但事件类型（`content_block_start` 等）与 OpenAI 不同。
- **API 生命周期**：OpenAI 兼容 Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已**停止维护**，必须迁移至 `/compatible-mode/v1/responses` [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **缓存与计费**：`store=false` 创建的 Responses 无法被 `previous_response_id` 引用，且不计入 Session 缓存；显式缓存（`cache_control`）命中时按缓存 Token 计费，未命中则按原始 Token 计费。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


