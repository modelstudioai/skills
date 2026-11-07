# qwen api reference

Qwen API Reference 文档汇总了阿里云百炼平台提供的千问系列模型调用方式，涵盖 OpenAI 兼容、Anthropic 兼容及原生 DashScope 三种协议。开发者可根据技术栈和功能需求选择合适接口，所有接口均支持多模态输入（文本、图像、音频、视频）与高级能力（工具调用、深度思考、显式缓存等）。

## 支持的模型/功能

- **核心模型**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3-vl-plus`、`qwen3-coder-flash` 等全系千问商业版与开源模型；同时支持 DeepSeek（如 `deepseek-v4.1-flash-1017`）、Kimi（如 `kimi-k3.1-pro`）、GLM（如 `glm-5.3`）等第三方直供模型。
- **多模态能力**：Qwen-VL、Qwen-Omni、Qwen3.8-Omni-Flash 等模型支持图像、视频、音频理解；其中 Qwen-Omni 系列可同时处理音视频流与文本，Qwen-VL 系列专注视觉理解 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **Agent 能力**：OpenAI 兼容的 Responses API 内置 `web_search`、`web_extractor`、`code_interpreter`、`file_search` 等工具，并支持自定义 function 工具调用；Anthropic 兼容 Messages API 同样支持 `web_search_20250305` 等联网搜索工具 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。
- **结构化输出与思考控制**：通过 `output_config.effort`（Anthropic）或 `reasoning.effort`（Responses）控制推理强度；支持 JSON Schema 结构化输出（部分模型如 `deepseek-v4.1-flash` 不支持）[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 协议调用；QwQ 模型不建议设置 system message，QVQ 模型的 system message 不生效 —— 此矛盾信息在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致，但需开发者主动规避。

## 关键参数

| 参数 | 类型 | 说明 | 适用协议 |
|------|------|------|----------|
| `model` | string | 必填。模型 ID，如 `qwen3.8-max` 或 `kimi-k3.1-pro`。注意不同协议支持的模型列表存在差异（如 Responses API 明确列出 `qwen3.8-omni-flash`，而 Anthropic API 未列该型号） | 全部 |
| `input` / `messages` | array/string | 必填。输入内容格式：Responses API 支持 `string` 或 `array`（含 `input_text`/`input_image` 等结构化类型），OpenAI Chat 使用标准 `messages` 数组，DashScope 需嵌套于 `input.messages` | Responses / OpenAI Chat / DashScope |
| `stream` | boolean | 是否启用流式响应，默认 `false` | 全部 |
| `store` | boolean | Responses API 特有：是否持久化响应以便后续 `previous_response_id` 引用，默认 `true` | Responses |
| `previous_response_id` | string | Responses API 特有：实现多轮对话的轻量级上下文管理，替代手动拼接 `messages` | Responses |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | number | 视频/图像预处理参数，控制抽帧频率、分辨率缩放与总像素上限。`fps` 在 OpenAI Chat 和 DashScope 中行为一致，但 DashScope 额外支持 `max_frames` | OpenAI Chat / DashScope |
| `reasoning.effort` / `output_config.effort` | string | 控制深度思考强度（`low`/`medium`/`high`/`max`/`xhigh`），取值映射因模型而异（如 `qwen3.8-flash` 的 `max` 映射为 `xhigh`） | Responses / Anthropic |

## 使用方式

- **协议选择**：
  - 已使用 OpenAI SDK 的项目：优先选用 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)（基础对话）或 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)（带工具、缓存、多轮管理的增强版）；
  - 已使用 Anthropic SDK 的项目：选用 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)，注意 `temperature` 范围为 `[0, 2)`（非官方 `[0.0, 1.0]`）；
  - 需要最大灵活性或迁移旧 DashScope 应用：选用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)，但需注意请求体结构（如 `messages` 需置于 `input` 对象内）。

- **Endpoint 配置**：
  - 所有协议均推荐使用业务空间专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优；
  - [OpenAI 兼容接口](../concepts/openai-compatibility.md)路径为 `/compatible-mode/v1/chat/completions`（Chat）或 `/compatible-mode/v1/responses`（Responses）；
  - Anthropic 兼容接口路径为 `/apps/anthropic/v1/messages`；
  - DashScope 原生接口路径为 `/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态）。

- **认证**：统一使用百炼 API Key，通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic）头传递。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在百炼控制台单独开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **API 迁移要求**：OpenAI 兼容 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移至 `/compatible-mode/v1/responses` [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **上下文长度**：Responses API 为内置工具预留约 20% 上下文缓冲区，实际可用输入长度约为模型窗口的 80%，超出部分自动截断（不报错）[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **缓存与计费**：显式缓存（`cache_control.type=ephemeral`）和 Session 缓存（`x-dashscope-session-cache: enable`）均可降低 Token 消耗，但命中缓存仍按缓存 Token 计费；`cached_tokens` 字段在响应 `usage` 中明确返回 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)。
- **音视频限制**：Qwen-Audio 仅支持 DashScope 协议；Qwen-VL 输入视频时，`fps` 默认值为 2.0，取值范围 `[0.1, 10]`，而 MiniMax 模型的 `fps` 范围为 `[0.2, 5]` —— 开发者需按目标模型查阅具体约束 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


