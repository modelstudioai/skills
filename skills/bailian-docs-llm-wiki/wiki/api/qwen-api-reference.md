# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及多模态能力（图像、视频、音频理解）。统一采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持三大类调用协议，覆盖不同场景需求：

- **OpenAI 兼容协议**：提供 `/chat/completions`（标准对话）和 `/responses`（增强版 Agent 能力）两类端点。其中 `/responses` 是百炼特有扩展，内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具链，并支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存，详见 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)。
- **Anthropic 兼容协议**：通过 `/apps/anthropic/v1/messages` 提供 Messages 接口，支持结构化输出（`output_config.format=json_schema`）、显式缓存（`cache_control`）、深度思考（`thinking.effort`）等高级能力，适用于需强约束 JSON 输出或复杂推理的场景。
- **DashScope 原生协议**：提供 `/api/v1/services/aigc/text-generation/generation`（纯文本）和 `/api/v1/services/aigc/multimodal-generation/generation`（多模态）两个专用端点，对音视频输入（如 `video`、`image` 字段）和参数（如 `max_frames`）控制更精细，是调用 `qwen-audio` 或高精度视频理解的首选，详见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 仅支持 DashScope 原生协议，不支持 OpenAI 兼容协议（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；而 `/responses` API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。

## 关键参数

各协议共性参数与关键差异如下：

| 参数 | OpenAI `/chat/completions` | OpenAI `/responses` | Anthropic `/messages` | DashScope 原生 |
|------|----------------------------|---------------------|------------------------|----------------|
| **`model`** | 必选，支持 `qwen3.8-max`、`qwen3-vl-plus`、`deepseek-v4-pro` 等（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)） | 必选，列表更聚焦于 Qwen 商业版（如 `qwen3.8-max`、`qwen3.7-plus`），第三方模型 Agent 能力受限 | 必选，明确分组为 Max/Plus/Flash/Turbo/Coder/VL 等系列（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | 必选，支持 `qwen-audio` 等 DashScope 特有模型（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)） |
| **输入格式** | `messages[]` 数组，`content` 支持 `text`/`image_url`/`video_url` 等类型 | `input` 支持 `string` 或 `EasyInputMessage[]`，`content` 元素支持 `input_audio`/`input_video`（仅 `qwen3.8-omni-flash`） | `messages[]` + `system`，`content` 支持 `text`/`image`/`video`/`tool_use`/`tool_result` | `input.messages[]`，`content` 支持 `text`/`image`/`video`，`video` 支持 `max_frames` 控制抽帧数 |
| **多模态控制** | `min_pixels`/`max_pixels`/`total_pixels`/`fps` | `min_pixels`/`max_pixels`/`fps`（音视频字段在 `input_audio`/`input_video` 中） | `min_pixels`/`max_pixels`/`fps`（`video` 类型下） | `min_pixels`/`max_pixels`/`fps`/**`max_frames`**（DashScope 特有） |
| **Agent 工具** | 仅基础 `function_call` | 内置 `web_search`/`web_extractor`/`code_interpreter` 等，支持 `tools` 数组混合调用 | `tools` 数组定义，支持 `tool_use`/`tool_result` 流程 | 不直接支持，需通过 DashScope SDK 的 `ToolCall` 机制实现 |

## 使用方式

### 1. 基础调用流程
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头传入百炼 API Key（需先[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- **域名**：使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），`{WorkspaceId}` 在百炼控制台“业务空间详情”中获取。华北2（北京）、新加坡、中国香港地域强烈建议迁移至此新域名（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **SDK 配置**：
  - OpenAI SDK：设置 `base_url` 为对应地域的兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
  - Anthropic SDK：设置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`。
  - DashScope SDK：设置 `base_http_api_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`。

### 2. 核心端点示例
- **OpenAI Chat**：`POST /compatible-mode/v1/chat/completions`（标准对话）
- **OpenAI Responses**：`POST /compatible-mode/v1/responses`（带工具链的 Agent）
- **Anthropic Messages**：`POST /apps/anthropic/v1/messages`（结构化输出与深度思考）
- **DashScope Text**：`POST /api/v1/services/aigc/text-generation/generation`
- **DashScope Multimodal**：`POST /api/v1/services/aigc/multimodal-generation/generation`

### 3. 辅助操作
- **获取响应**：`GET /compatible-mode/v1/responses/{response_id}`（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)）
- **查询输入项**：`GET /compatible-mode/v1/responses/{response_id}/input_items`（用于调试多轮对话历史）
- **删除响应**：`DELETE /compatible-mode/v1/responses/{response_id}`（清理已存储的响应）

## 限制和注意事项

- **模型能力差异**：`QwQ` 模型不建议设置 `system` 消息，`QVQ` 模型设置 `system` 消息无效（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；`Qwen-Audio` 仅 DashScope 协议可用。
- **参数兼容性**：OpenAI `/responses` API **忽略所有未文档化的 OpenAI 参数**（如 `background`），且 `reasoning.effort` 为百炼特有控制项；Anthropic 协议中 `temperature` 取值范围为 `[0, 2)`，与官方 `[0.0, 1.0]` 不同，迁移时需校验（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。
- **上下文与缓存**：`/responses` API 的最大输入上下文约为模型窗口的 80%（预留 20% 给工具调用），超长内容将自动截断；`x-dashscope-session-cache: enable` 可启用服务端自动缓存，降低多轮延迟。
- **计费与 Token**：`/responses` API 的 `usage.output_tokens_details.reasoning_tokens` 明确计入推理 Token；`/chat/completions` 和 `/messages` 的 `max_tokens` 含义因模型而异（如 `glm-5.3` 将其视为回复+思考总和，而其他模型仅限回复），务必查阅对应模型文档。
- **地域与域名**：旧域名（如 `dashscope.aliyuncs.com`）仍可用，但新业务**必须使用业务空间专属域名**以获得最佳性能，该要求在全部 8 篇原始文档中被反复强调。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


