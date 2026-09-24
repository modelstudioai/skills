# qwen api reference

阿里云百炼平台提供多种 API 接口协议（OpenAI 兼容、Anthropic 兼容、DashScope 原生）调用 Qwen 系列大模型，支持文本、多模态、工具调用等能力。开发者可根据技术栈和功能需求选择合适协议，所有接口均基于业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）提供高性能、高稳定性服务。

## 支持的模型/功能

Qwen API 支持全系列千问模型及部分第三方模型，覆盖不同能力与场景：

- **文本生成**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态理解**：`qwen3.8-omni-flash`、`qwen3-vl-plus`、`qwen-vl-max`、`qwen3.7-vl`、`QVQ` 等，支持图像、视频（文件或帧列表）、音频输入；
- **专用能力**：`qwen3.5-math`（数学推理）、`qwen3.8-audio`（语音理解，仅 DashScope 协议支持，见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；
- **第三方模型**：DeepSeek（v4 系列）、Kimi（k3/k2.x）、GLM（5.x）、MiniMax（M2.x/M3）等，但部分直供模型仅在华北2（北京）地域可用，且需在控制台开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型中 `system` 消息无效。

功能层面，各协议能力有明确分工：
- **OpenAI 兼容 Chat**：标准对话流，适用于通用 LLM 集成；
- **OpenAI 兼容 Responses**：增强型对话 API，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 多轮上下文管理与 Session 缓存 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **Anthropic 兼容 Messages**：支持结构化输出（JSON Schema）、显式缓存断点（`cache_control`）、深度思考（`output_config.effort`），适用于需要强约束输出或精细推理控制的场景；
- **DashScope 原生 API**：最底层协议，支持 `max_frames` 等细粒度视频参数，是唯一支持 `qwen3.8-audio` 的入口。

## 关键参数

核心参数因协议而异，以下为跨协议高频参数说明：

| 参数 | OpenAI Chat | OpenAI Responses | Anthropic Messages | DashScope | 说明 |
|------|-------------|------------------|----------------------|-----------|------|
| `model` | ✅ 必选 | ✅ 必选 | ✅ 必选 | ✅ 必选 | 模型 ID，如 `qwen3.8-max`；[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 中明确列出三方模型支持地域限制 |
| `messages` / `input` | ✅ `array` | ✅ `string` 或 `array` | ✅ `messages` + `system` | ✅ `messages`（需嵌套于 `input`） | 多模态输入统一通过 `content` 数组描述，支持 `text`/`image_url`/`video_url`/`input_audio` 等类型 |
| `max_tokens` | ❌ | ❌ | ✅ 必选 | ✅（`max_output_tokens`） | Anthropic 协议下含义复杂：对 `qwen3.8-max` 表示回复+思考总长；对 `glm-5.2` 则仅限回复长度，思考由 `thinking.budget_tokens` 控制 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) |
| `temperature` | ✅ `[0,2)` | ✅ `[0,2)` | ✅ `[0,2)` | ✅ `[0,2)` | 注意该范围与 Anthropic 官方 `[0.0,1.0]` 不同，迁移时需校准 |
| `stream` | ✅ | ✅ | ✅ | ✅ | 启用流式响应，事件格式遵循各协议规范 |
| `tools` | ⚠️ 仅部分模型支持 | ✅ 内置+自定义工具 | ✅ 自定义 Function Call | ❌ | Responses API 是唯一提供预置 `web_search`/`code_interpreter` 等工具的接口 |

视频处理相关参数（如 `fps`、`min_pixels`、`max_pixels`、`total_pixels`）在 OpenAI Chat 和 DashScope 协议中定义一致，但 Anthropic 协议使用 `video` 类型块且不支持 `total_pixels`；`max_frames` 仅 DashScope 支持。

## 使用方式

### 1. 基础接入
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台「业务空间详情」页获取）；
- 使用百炼 API Key（通过 `Authorization: Bearer <key>` 或 `x-api-key` 传入）；
- 优先采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）仍可用但不推荐 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 协议选择指南
- **快速迁移 OpenAI 应用** → 用 OpenAI 兼容 Chat 或 Responses；
- **需要内置 Agent 工具（搜索/代码执行）** → 必选 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **要求 JSON Schema 强约束输出或显式缓存** → 用 Anthropic 兼容 Messages；
- **调用 Qwen-Audio 或需 `max_frames` 等高级视频参数** → 用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

### 3. 多轮对话
- **OpenAI Responses**：通过 `previous_response_id` 自动拼接历史，或使用 `conversation` 管理会话；
- **OpenAI Chat**：需手动维护 `messages` 数组；
- **Anthropic Messages**：`messages` 数组天然支持多轮，`system` 可复用；
- 所有协议均支持 `x-dashscope-session-cache: enable` 请求头启用服务端上下文缓存。

## 限制和注意事项

- **地域限制**：第三方模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在中国站华北2（北京）地域可用，调用前须在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)；
- **协议弃用**：OpenAI Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，必须迁移到 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **参数兼容性**：OpenAI 兼容 API **忽略所有未文档化的 OpenAI 参数**（如 `background`），仅处理明确列出的字段；
- **上下文截断**：Responses API 为预留工具调用空间，实际最大输入上下文约为模型窗口的 80%，超出部分自动截断不报错；
- **计费差异**：`reasoning_tokens`（思考过程 [Token](../concepts/token.md)）在 Responses API 中单独计费，需关注 `usage.output_tokens_details.reasoning_tokens` 字段；
- **缓存行为**：`vl_high_resolution_images=true` 时，`max_pixels` 参数失效，图像最大像素固定为 `16777216`（Qwen3 系列）或 `12845056`（Qwen2.5-VL/QVQ）；
- **错误处理**：`GET /responses/{id}` 等查询接口返回 `404` 时，错误体格式统一为 `{"error": {"message": "...", "type": "InvalidParameter"}}`，需按此解析。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


