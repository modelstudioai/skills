# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat/Responses、Anthropic 兼容 Messages 和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及多模态能力（图像、视频、音频理解）。统一采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用协议，覆盖不同场景需求：

- **OpenAI 兼容 Chat**：适用于标准对话场景，完全兼容 `chat/completions` 接口，支持 `messages` 数组输入、`system`/`user`/`assistant` 角色、多模态内容（`image_url`、`video_url`、`input_audio`）及显式缓存（`cache_control`）。但需注意：**Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 协议 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses**：面向复杂 Agent 场景，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 多轮上下文管理、Session 缓存（`x-dashscope-session-cache: enable`）及结构化输出。其 `input` 支持 `string` 或 `array` 格式，比 Chat 更灵活 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages**：适配 Anthropic 生态，支持 `system` 字段、`tool_use`/`tool_result` 工具交互、深度思考（`thinking.type`）及结构化输出（`output_config.format`）。注意 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **DashScope 原生协议**：提供最底层控制，区分纯文本（`text-generation`）与多模态（`multimodal-generation`）服务端点，支持 `max_frames` 等细粒度视频参数，是调用 Qwen-Audio 或需要精确帧控的首选 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：文档 1 与文档 8 对 `min_pixels` 默认值的描述存在不一致。文档 1 中 `qwen3.7` 图像输入默认值为 `65536`，而文档 8 同样列出 `Qwen3.7` 默认值为 `65536`，但未明确是否包含商业版/开源版差异；文档 7 则未提及该参数。建议以最新文档 1 的说明为准，并在实际调用中显式指定以避免歧义。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例 |
|------|----------|------|------|
| `model` | 全部 | 必选，模型 ID。Chat/Responses/DashScope 均支持 `qwen3.8-max`、`qwen3.7-plus` 等；Anthropic 协议额外支持 `qwen3-coder-flash`、`qwen3-vl-plus` [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 | `"qwen3.7-plus"` |
| `messages` / `input` | Chat & DashScope / Responses | Chat 和 DashScope 使用 `messages` 数组；Responses 使用 `input`（`string` 或 `array`）。`input` 在 Responses 中可直接传字符串，更简洁。 | `{"input": "你好"}` (Responses) |
| `fps` | Chat, Responses, DashScope | 视频抽帧频率（单位：帧/秒），取值 `[0.1, 10]`，默认 `2.0`。影响帧数与时序理解，需与 `total_pixels`/`max_frames` 配合使用。 | `"fps": 4.0` |
| `min_pixels` / `max_pixels` / `total_pixels` | Chat & DashScope | 控制图像/视频帧分辨率。`min_pixels`（最小像素）、`max_pixels`（最大像素）、`total_pixels`（所有帧总像素上限）。各参数默认值因模型和输入类型而异，详见文档 1。 | `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": 65536}` |
| `max_frames` | DashScope only | DashScope 独有参数，限制视频抽取帧数上限（如 `qwen3.7` 系列默认 `8000`）。OpenAI 兼容 API 不支持此参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。 | `"max_frames": 2000` |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | Responses 用 `reasoning.effort`（如 `"high"`），Anthropic 用 `output_config.effort`（如 `"xhigh"`），控制思考强度。二者语义一致，但参数路径不同。 | `"reasoning": {"effort": "high"}` (Responses) |

## 使用方式

1. **认证与域名**：所有协议均需 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并通过业务空间专属域名调用（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。旧域名（如 `dashscope.aliyuncs.com`）仍可用，但**强烈建议迁移至新域名以获得更高性能与稳定性** [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
2. **SDK 配置示例**：
   - OpenAI SDK：设置 `base_url` 为对应地域的兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
   - DashScope SDK：Python 中通过 `workspace` 和 `region` 参数配置（如 `workspace="xxx", region="cn-beijing"`）。
3. **多轮对话**：
   - Chat：手动维护 `messages` 数组。
   - Responses：使用 `previous_response_id` 自动拼接历史，或启用 `x-dashscope-session-cache` 实现无感缓存。
   - Anthropic：依赖 `messages` 数组顺序，无内置 ID 机制。
4. **工具调用**：
   - Responses：在 `tools` 数组中声明内置工具（如 `web_search`）或自定义 function。
   - Anthropic：在 `tools` 中声明，配合 `tool_use`/`tool_result` 消息交互。
   - Chat：仅支持 `tool_calls` 输出，需客户端自行处理并回传结果。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、Kimi）**仅在中国站的华北2（北京）地域可用**，且需在百炼控制台单独开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **协议能力差异**：
  - Chat API **不支持 Qwen-Audio**；Audio 输入必须使用 DashScope 协议。
  - Responses API **不支持异步执行**（`background` 参数已废弃），仅同步调用。
  - Anthropic API **不提供 `/v1/models` 接口**，客户端需预置模型列表。
- **参数兼容性**：OpenAI Responses API **忽略所有未在文档中明确列出的 OpenAI 参数**（如 `n`、`logit_bias`），仅处理已声明参数 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **计费与 [Token](../concepts/token.md)**：`total_pixels` 直接影响图像 [Token](../concepts/token.md) 消耗（每 32×32 像素 ≈ 1 [Token](../concepts/token.md)）；`reasoning_tokens` 在 Responses 中单独计费；`cached_tokens` 在启用 Session 缓存时可降低成本。务必参考各模型的 [计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)。
- **弃用提示**：`thinking.budget_tokens`（Anthropic）和 `vl_high_resolution_images`（Chat）等参数已被标记为**即将废弃**，新接入应优先使用 `output_config.effort` 和 `max_pixels` 替代。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


