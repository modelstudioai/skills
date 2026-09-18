# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型（如 DeepSeek、GLM、Kimi）。统一采用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）以保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持以下核心模型系列及能力：

- **文本生成模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3-vl-plus`、`qwen3.8-omni-flash`、`qwen-vl-max`、`QVQ`、`Qwen2.5-VL`，支持图像、视频、音频理解；
- **专用模型**：`qwen3-math`（数学推理）、`qwen3-audio`（仅 DashScope 协议支持，[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；
- **第三方模型**：DeepSeek（`deepseek-v4-pro` 等）、GLM（`glm-5.3`）、Kimi（`kimi-k3`）、MiniMax（`MiniMax-M2.5`），其中三方直供模型**仅在中国站华北2（北京）地域可用**，且需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

> **注意**：`Qwen-Audio` 明确不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；`QwQ` 模型不建议设置 `system` 消息，`QVQ` 模型中 `system` 消息无效。

功能层面，各协议能力有明确分工：
- **OpenAI Chat Completions**：标准对话流，适用于简单 [prompt](../guides/prompt.md) 工程与基础多轮交互；
- **OpenAI Responses**：增强型对话 API，内置联网搜索、网页抓取、代码解释器等工具调用能力，并支持 `previous_response_id` 上下文自动管理与 Session 缓存 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **Anthropic Messages**：兼容 Anthropic 生态，支持结构化输出（JSON Schema）、显式缓存断点（`cache_control`）及深度思考配置（`output_config.effort`）；
- **DashScope 原生协议**：最底层能力，区分 `text-generation` 与 `multimodal-generation` 服务端点，对多模态输入（如 `video`、`image` 字段）控制粒度更细（如 `max_frames`）。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，模型 ID。OpenAI Chat 与 DashScope 支持范围最广；Responses 仅限指定列表（如 `qwen3.8-max`, `deepseek-v4-flash`）；Anthropic 支持额外第三方模型（如 `glm-5.1`, `MiniMax-M2.1`） |
| `messages` / `input` | Chat & DashScope / Responses | 对话消息数组（Chat/DashScope）或灵活字符串/数组输入（Responses）；Responses 的 `input` 支持 `input_audio`/`input_video`（仅 `qwen3.8-omni-flash`） |
| `stream` | 全部 | 是否启用[流式输出](../concepts/streaming-output.md)，默认 `false` | `true` |
| `temperature` | 全部 | 控制生成多样性；**OpenAI/Responses 取值范围为 `[0, 2)`，Anthropic 兼容协议亦同，但 Anthropic 官方为 `[0.0, 1.0]`**，迁移时需校验 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) |
| `max_tokens` | Chat/Responses/Anthropic | 含义因协议而异：Chat 中为输出上限；Responses 中为输出+思考总上限（若开启思考）；Anthropic 中依模型不同，可能仅限输出或含思考 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) |
| `min_pixels` / `max_pixels` | Chat & DashScope | 图像/视频帧像素缩放阈值，单位为总像素数；取值与模型强相关（如 `qwen3.8-max` 默认 `min_pixels=65536`, `max_pixels=2621440`）；DashScope 协议额外支持 `max_frames` 控制抽帧总数 |
| `fps` | Chat & DashScope | 视频抽帧频率（帧/秒），范围 `[0.1, 10]`，默认 `2.0`；同时用于建模时间动态，支持 `qwen3.7+`、`Qwen3-VL`、`QVQ` 等系列 |
| `tools` | Responses & Anthropic | 内置工具（`web_search`, `code_interpreter`）或自定义 function 工具；Responses 中 `qwen3.8-omni-flash` 仅支持 `web_search`，其余模型需配合思考模式启用 |

## 使用方式

### 1. 基础接入
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（见 [业务空间ID获取文档](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）；
- 配置百炼 API Key（通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <key>` / `x-api-key: <key>`）；
- **强烈建议迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但新域名提供更高性能与稳定性 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 协议选择指南
- **快速迁移 OpenAI 应用**：使用 `/compatible-mode/v1/chat/completions`（Chat）或 `/compatible-mode/v1/responses`（Responses），后者推荐用于需工具调用或长上下文管理的场景；
- **迁移 Anthropic 应用**：使用 `/apps/anthropic/v1/messages`，注意 `temperature` 范围与 `max_tokens` 行为差异；
- **需要精细控制多模态输入**（如本地视频文件、帧数限制）：使用 DashScope 原生协议 `/api/v1/services/aigc/multimodal-generation/generation`，其 `video` 字段支持 `array`（图像列表）与 `string`（视频 URL）双格式，并独有 `max_frames` 参数。

### 3. 多轮对话
- **Chat API**：手动维护 `messages` 数组，将上一轮 `assistant` 输出追加至当前 `messages` 尾部；
- **Responses API**：传入 `previous_response_id` 自动加载历史上下文，或使用 `conversation` 参数绑定会话；
- **Anthropic API**：通过 `messages` 数组自然延续，无专用上下文 ID 机制。

## 限制和注意事项

- **地域限制**：三方直供模型（DeepSeek、Kimi、GLM 等）**仅支持华北2（北京）地域**，其他地域调用将失败；
- **协议弃用**：OpenAI Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **参数兼容性**：OpenAI Responses API **不支持 `background`（异步）参数**，仅同步调用；Anthropic Messages API **不提供 `/v1/models` 接口**，客户端模型发现请求将返回 404；
- **缓存与计费**：显式缓存（`cache_control: {type: "ephemeral"}`）仅 Anthropic Messages 和 OpenAI Chat（`type: "text"`/`"image_url"` 内）支持；Session 缓存（`x-dashscope-session-cache: enable`）仅 Responses API 支持；
- **模型行为差异**：`system` 消息在 `QwQ` 模型中不建议设置，在 `QVQ` 模型中无效；`Qwen-Audio` 不支持 OpenAI 协议，必须使用 DashScope 协议；
- **输入大小限制**：PDF 文件（`input_file`）最大 100 MB，图片最大 20 MB；视频 URL 需公网可访问，Base64 编码需包含完整 MIME 前缀（如 `data:video/mp4;base64,...`）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


