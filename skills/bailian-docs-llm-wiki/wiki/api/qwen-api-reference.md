# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat/Responses、Anthropic 兼容 Messages 以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及多模态能力，并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

- **核心模型**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.7-flash`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3-vl-plus`、`qwen3-coder-flash`；开源模型如 `qwen3.5-397b-a17b`、`qwen3.8-27b`；第三方直供模型（DeepSeek、Kimi、GLM、MiniMax）仅限华北2（北京）地域且需在控制台开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **多模态能力**：Qwen-VL、Qwen-Omni、QVQ 系列支持图像、视频（URL/Base64/本地文件）、音频（仅 `qwen3.8-omni-flash`）输入；视频处理支持 `fps` 抽帧控制、`min_pixels`/`max_pixels` 分辨率自适应及 `total_pixels` 总像素限制 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。
- **高级功能**：
  - **工具调用（Function Calling）**：Responses API 内置 `web_search`、`code_interpreter`、`web_extractor` 等工具；OpenAI Chat 和 Anthropic Messages 支持自定义 `function` 工具 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
  - **结构化输出**：Anthropic Messages 支持 `output_config.format.json_schema` 强约束 JSON 输出，qwen3.8/3.7/DeepSeek/GLM 系列可严格校验字段类型与层级 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
  - **深度思考**：通过 `reasoning.effort`（Responses）或 `thinking.type` + `output_config.effort`（Anthropic）控制推理强度，`qwen3.8-max` 默认 `xhigh`，`glm-5.3` 默认 `max`。
  - **显式缓存**：所有协议均支持 `cache_control: {type: "ephemeral"}` 标记缓存断点，提升重复请求性能。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生协议调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型的 `system` 消息无效 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 关键参数

| 参数 | 协议适用性 | 说明 |
|------|------------|------|
| `model` | 全协议必选 | 必须使用百炼控制台实际可用的模型 ID（如 `qwen3.8-max`），非列表中模型可能受限于 Agent 能力 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 |
| `messages` / `input` / `content` | Chat/Responses/Anthropic | Chat 和 Anthropic 使用标准消息数组；Responses 支持 `string` 或 `array` 输入，且 `user` 消息支持 `input_audio`/`input_video`（仅 `qwen3.8-omni-flash`）[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 |
| `max_tokens` | Anthropic/Chat | Anthropic 协议中，`qwen3.8-max`/`deepseek-v4` 等模型该值限制「回复+思考」总长度；而 `qwen3.7-plus` 等模型仅限制回复长度，思考 Token 由 `thinking.budget_tokens` 单独控制 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |
| `temperature` | 全协议可选 | 取值范围为 `[0, 2)`，**不同于 Anthropic 官方的 `[0.0, 1.0]`**，迁移时需调整 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | 多模态场景 | 控制视频/图像预处理，`fps` 同时影响抽帧频率与时间动态理解；`total_pixels` 限制视频总像素（单帧×帧数），避免 Token 溢出 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |

## 使用方式

- **接入地址**：统一使用业务空间专属域名（推荐）或旧版全局域名。  
  - 专属域名格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）；  
  - 协议路径：  
    - OpenAI Chat：`/compatible-mode/v1/chat/completions`；  
    - OpenAI Responses：`/compatible-mode/v1/responses`；  
    - Anthropic Messages：`/apps/anthropic/v1/messages`；  
    - DashScope 原生：文本模型用 `/api/v1/services/aigc/text-generation/generation`，多模态用 `/api/v1/services/aigc/multimodal-generation/generation` [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。  
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头传入百炼 API Key [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。  
- **SDK 配置**：  
  - OpenAI SDK：设置 `base_url` 为对应协议域名；  
  - Anthropic SDK：设置 `base_url` 为 `/apps/anthropic` 路径；  
  - DashScope SDK：设置 `base_http_api_url` 为 `/api/v1` 路径。  
- **多轮对话**：  
  - Chat：手动维护 `messages` 数组；  
  - Responses：使用 `previous_response_id` 自动拼接历史上下文，或启用 `x-dashscope-session-cache: enable` 实现服务端自动缓存；  
  - Anthropic：无内置会话管理，需客户端维护 `messages`。

## 限制和注意事项

- **地域与模型绑定**：第三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **协议差异**：  
  - OpenAI Responses API **不支持异步参数 `background`**，仅同步调用；旧版路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移到 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。  
  - Anthropic Messages **不提供 `/v1/models` 接口**，客户端模型发现请求将返回 404；`thinking.budget_tokens` 参数已标记为“即将废弃”，新接入应使用 `output_config.effort` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。  
- **上下文长度**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超长部分将自动截断 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。  
- **流式响应**：所有协议均支持 `stream=true`，但 Responses 的流式事件字段为 `response.output_text.delta`，而 Chat/Anthropic 使用标准 OpenAI/Anthropic 流式格式。  
- **计费与缓存**：`store=false` 的 Responses 不可被 `previous_response_id` 引用；`x-dashscope-session-cache` 缓存命中时，`usage.input_tokens_details.cached_tokens` 返回命中数，按缓存计费。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


