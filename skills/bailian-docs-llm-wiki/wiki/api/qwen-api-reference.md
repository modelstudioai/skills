# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型（如 DeepSeek、GLM、Kimi）。统一使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）可获得更优性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用协议，覆盖不同场景需求：

- **OpenAI 兼容协议**：提供 `/chat/completions`（标准对话）和 `/responses`（增强版 Agent）两类端点。`/responses` 是百炼特有扩展，内置联网搜索、网页抓取、代码解释器、文搜图等工具能力，并支持 `previous_response_id` 多轮上下文管理与 Session 缓存。详见 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)。
- **Anthropic 兼容协议**：通过 `/apps/anthropic/v1/messages` 提供 Messages 接口，支持结构化输出（`output_config.format=json_schema`）、显式缓存控制（`cache_control`）及深度思考配置（`thinking.type` 和 `output_config.effort`），适用于需要强约束 JSON 输出或复杂推理的场景。
- **DashScope 原生协议**：提供 `/text-generation/generation`（纯文本）和 `/multimodal-generation/generation`（多模态）两个专用端点，对图像、视频、音频等输入格式控制更细粒度（如 `max_frames`、`min_pixels`），是调用 `Qwen-Audio` 等非 OpenAI 兼容模型的唯一途径。详见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生协议调用；而 Anthropic 兼容协议当前**不支持音频/视频输入**，仅限文本与图像。

## 关键参数

各协议共性参数与关键差异如下：

| 参数 | OpenAI Chat | OpenAI Responses | Anthropic Messages | DashScope |
|------|-------------|------------------|----------------------|-----------|
| **model** | 必选，支持 `qwen3.8-max` 等全系列及三方模型（见[文档2](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)） | 必选，列表更聚焦于百炼直供模型（如 `qwen3.8-omni-flash`），三方模型 Agent 能力受限（见[文档3](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)） | 必选，明确分组列出 Max/Plus/Flash/VL/开源/第三方模型（见[文档7](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | 必选，明确区分文本模型与多模态模型路径（见[文档8](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)） |
| **input / messages** | `messages` 数组，`content` 支持 `text`/`image_url`/`video_url` 等类型 | `input` 支持 `string` 或 `array`；`array` 中 `content` 元素支持 `input_text`/`input_image`/`input_file`/`input_audio`（仅 `qwen3.8-omni-flash`） | `messages` 数组，`content` 支持 `text`/`image`/`video` 类型，`image`/`video` 需 `source` 指定 `url` 或 `base64` | `messages` 在 HTTP 请求中需置于 `input` 对象内；`content` 支持 `text`/`image`/`video`，`image` 可为 URL/Base64/本地路径 |
| **temperature** | 取值范围 `[0, 2)` | 同左 | 取值范围 `[0, 2)`，**与 Anthropic 官方 `[0.0, 1.0]` 不同**，迁移时需校验（见[文档7](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | 同左 |
| **max_tokens** | 控制输出长度 | 同左 | 行为因模型而异：对 `qwen3.8-max` 等为“回复+思考”总长；对 `glm-5.2` 等可单独用 `thinking.budget_tokens` 控制思考长度（见[文档7](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | 同左（DashScope 协议中为 `max_output_tokens`） |
| **扩展能力** | 无原生工具调用字段，需通过 `tools` 参数启用 | `tools` 参数直接支持 `web_search`/`code_interpreter` 等内置工具及自定义 function | `tools` + `tool_choice` + `output_config.effort` 构成完整 Agent 控制链 | 无原生工具调用，需自行集成 |

## 使用方式

1. **认证与域名**：所有请求均需在 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头中传入百炼 API Key。**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），华北2（北京）、新加坡、中国香港地域已全面支持，性能与稳定性显著优于旧域名 `dashscope.aliyuncs.com`（见[文档2](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[文档3](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)、[文档7](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)、[文档8](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
2. **SDK 配置**：
   - OpenAI SDK：设置 `base_url` 为对应地域的兼容模式地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
   - Anthropic SDK：设置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`。
   - DashScope SDK：设置 `base_http_api_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`。
3. **多轮对话**：
   - OpenAI Responses：使用 `previous_response_id` 自动拼接历史上下文，或使用 `conversation` 管理会话生命周期。
   - OpenAI Chat / Anthropic / DashScope：需手动维护 `messages` 数组，将历史 `user`/`assistant` 消息按顺序追加。

## 限制和注意事项

- **协议兼容性**：OpenAI 兼容 API **不支持** `background`（异步）等部分 OpenAI 参数，且 `reasoning.effort` 等百炼特有参数仅在 Responses 端点生效（见[文档3](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **模型能力边界**：`QwQ` 模型不建议设置 `system` 消息，`QVQ` 模型设置 `system` 消息无效；`Qwen-VL` 输入视频时，`fps` 参数默认值为 `2.0`，取值范围 `[0.1, 10]`（见[文档2](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[文档8](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
- **输入尺寸限制**：图像/视频处理受 `min_pixels`/`max_pixels`/`total_pixels`（OpenAI）或 `max_frames`（DashScope）等参数约束，不同模型取值范围差异较大，务必查阅对应模型文档（见[文档2](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[文档8](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
- **响应管理**：`/responses` 端点支持 `GET /responses/{id}` 获取、`GET /responses/{id}/input_items` 查看输入历史、`DELETE /responses/{id}` 删除响应，但**仅当创建请求中 `store=true` 时，响应 ID 才可被检索或删除**（见[文档4](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[文档5](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)、[文档6](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


