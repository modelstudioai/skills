# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流千问系列模型（如 `qwen3.8-max`、`qwen3.7-plus`）及多模态能力（图像、视频、音频），并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持以下核心模型与能力：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3.5-ocr`、`qwen-coder-flash` 等全系商业版与开源版文本大模型；
- **多模态模型**：`qwen3.8-omni-flash`（音视频理解）、`qwen3-vl-plus`（视觉语言）、`qwen3.5-ocr`（文档解析）；
- **第三方模型**：DeepSeek（v4 系列）、Kimi（k3/k3.1-pro）、GLM（5.x）、MiniMax（M3/M3.1-Flash）等直供模型，但部分能力受限（如三方模型在 OpenAI 兼容协议下不支持内置工具）；
- **高级功能**：
  - 内置 Agent 工具（仅 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md) 支持 `web_search`、`code_interpreter`、`file_search` 等）；
  - 显式缓存（`cache_control.type = "ephemeral"`）与 Session 缓存（`x-dashscope-session-cache: enable`）；
  - 结构化输出（Anthropic 兼容协议的 `output_config.format`）与深度思考（`output_config.effort` 或 `thinking.type`）；
  - 多轮对话管理（`previous_response_id` 或 `conversation`）。

> **注意**：Qwen-Audio 仅支持 DashScope 协议，[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 明确声明其不支持 OpenAI 兼容协议；同理，QwQ 模型不建议设置 system message，QVQ 模型的 system message 不生效，该限制在多个文档中一致，无需修正。

## 关键参数

| 参数 | 协议 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | 全协议必选 | 模型 ID，需严格匹配控制台可用列表 | `"qwen3.7-plus"` |
| `messages` / `input` | Chat/Responses 必选 | 对话消息数组或字符串输入；Responses 支持 `string`、`array` 及 `ResponseOutputMessage` 回传 | `[{"role":"user","content":"你好"}]` |
| `system` | Anthropic 兼容必选（可选） | Anthropic 协议专用系统提示字段，支持 `string` 或带 `cache_control` 的 `array` | `"你是一个助手"` |
| `max_tokens` | Anthropic 兼容必选 | 输出长度上限；对 `qwen3.8-max` 等模型，该值同时约束回复+思考 [Token](../concepts/token.md) | `2048` |
| `reasoning.effort` / `output_config.effort` | Responses / Anthropic | 控制思考强度（`low`/`medium`/`max`/`xhigh`），不同模型默认值与映射规则不同（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)） | `"max"` |
| `min_pixels` / `max_pixels` / `total_pixels` | 多模态必选（可选） | 图像/视频分辨率控制参数，各模型取值范围与默认值存在差异（如 `qwen3.8-omni-flash` 默认 `min_pixels=24576`，而 `qwen3-VL` 为 `65536`） | `{"min_pixels":65536,"max_pixels":8388608}` |
| `fps` | 视频输入必选（可选） | 抽帧频率（单位：帧/秒），影响视频理解精度与时序建模能力 | `2.0` |

> **注意**：`temperature` 在 Anthropic 兼容协议中取值范围为 `[0, 2)`，而 Anthropic 官方为 `[0.0, 1.0]`，迁移时需校准（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）；`max_frames` 仅 DashScope 协议支持，OpenAI 兼容协议自动使用模型默认值（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。

## 使用方式

### 1. 接入地址（Base URL）
所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并优先使用地域专属域名：

- **华北2（北京）**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **中国香港**：`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com`

> **重要**：旧域名 `dashscope.aliyuncs.com` 仍可用，但官方强烈建议迁移至专属域名以获得更高性能与稳定性（该提示在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)、[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中四次重复强调）。

### 2. 协议选择
- **OpenAI 兼容**：适用于已集成 OpenAI SDK 的项目，路径为 `/compatible-mode/v1/chat/completions`（Chat）或 `/compatible-mode/v1/responses`（Responses）。Responses 提供更优 Agent 能力与上下文管理（`previous_response_id`）；
- **Anthropic 兼容**：路径为 `/apps/anthropic/v1/messages`，支持 `output_config.effort` 等扩展参数，但不提供 `/v1/models` 列表接口；
- **DashScope 原生**：路径为 `/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态），SDK 需显式指定 `region` 与 `workspace`。

### 3. 认证
- 通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key: <API_KEY>` 请求头传入；
- API Key 需提前在百炼控制台获取并配置（见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。

## 限制和注意事项

- **协议差异**：OpenAI 兼容协议**忽略所有未明确文档化的参数**（如 `background` 异步参数不支持），Requests 将静默丢弃；Anthropic 兼容协议**不支持 `model.list` 接口**，客户端需自行维护模型列表；
- **上下文长度**：Responses API 为内置工具预留约 20% 上下文空间，实际可用输入长度约为模型窗口的 80%，超长内容将自动截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；
- **存储与检索**：`store=true` 是启用 `previous_response_id`、`GET /responses/{id}` 和 `GET /responses/{id}/input_items` 的前提条件；`store=false` 的响应无法被后续 API 访问；
- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek）**仅在中国站华北2（北京）地域可用**，且需在控制台单独开通（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）；
- **废弃参数**：`thinking.budget_tokens` 在 Anthropic 兼容协议中已标记为“即将废弃”，新接入应使用 `output_config.effort`（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


