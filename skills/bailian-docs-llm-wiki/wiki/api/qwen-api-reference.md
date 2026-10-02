# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及多模态能力（图像、视频、音频），并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持全系列千问模型，覆盖文本生成、多模态理解、代码生成、数学推理等场景：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3.8-omni-flash`、`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-max`、`QVQ`、`Qwen-Omni`；
- **第三方模型**：DeepSeek（v4 系列）、Kimi（k3/k2 系列）、GLM（5.x 系列）、MiniMax（M2/M3 系列）等，但需注意地域限制——[三方直供模型仅在中国站华北2（北京）地域可用](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)；
- **特殊能力**：
  - OpenAI 兼容 Responses API 提供内置工具链（联网搜索、网页抓取、代码解释器、文搜图等），详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
  - Anthropic 兼容 Messages API 支持结构化输出（JSON Schema）、显式缓存控制及深度思考配置（`output_config.effort`）；
  - DashScope 原生协议支持细粒度视频参数（如 `max_frames`、`fps`），但 [OpenAI 兼容 API 不支持自定义 `max_frames`](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

> **注意**：Qwen-Audio 模型**不支持 OpenAI 兼容协议**，仅可通过 DashScope 协议调用，该限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 文档中明确说明。

## 关键参数

不同协议的核心参数存在差异，需按协议区分使用：

| 参数 | OpenAI Chat (`/chat/completions`) | OpenAI Responses (`/responses`) | Anthropic Messages (`/messages`) | DashScope Native |
|------|-----------------------------------|----------------------------------|----------------------------------|------------------|
| **输入格式** | `messages: [{role, content}]`，`content` 支持 `text`/`image_url`/`video_url` 等类型 | `input: string \| array`，支持 `EasyInputMessage` 结构及 `ResponseOutputMessage` 复用 | `messages: [{role, content}]`，`content` 为 `text`/`image`/`video` 数组 | `messages` 需嵌套于 `input` 对象内；`image`/`video` 为独立字段（非数组元素） |
| **系统提示** | `messages[0].role === 'system'` | `instructions` 字符串或 `input` 中 `role: 'system'` | `system: string \| array` | `messages[0].role === 'system'` |
| **流式开关** | `stream: boolean` | `stream: boolean` | `stream: boolean` | `stream: boolean`（DashScope SDK 默认关闭） |
| **思考控制** | 无原生支持 | `reasoning.effort`（`low`/`medium`/`xhigh`） | `output_config.effort`（`low`/`high`/`max`/`xhigh`） | 无直接对应，需通过 `enable_thinking` + `thinking_budget`（已逐步废弃） |
| **视频抽帧** | `fps`（float）、`min_pixels`/`max_pixels`/`total_pixels` | `fps`（number）、`min_pixels`/`max_pixels` | `fps`（number） | `fps`（float）、`max_frames`（integer）、`min_pixels`/`max_pixels` |

> **注意**：`temperature` 取值范围在 Anthropic 兼容协议中为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校验参数值——该差异在 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md) 中重点标注。

## 使用方式

### 1. 统一接入地址
所有协议均使用**业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID。推荐优先使用新域名（如华北2：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。

### 2. 协议选择指南
- **OpenAI 兼容 Chat**：适用于标准对话场景，快速迁移现有 OpenAI 应用。端点为 `/compatible-mode/v1/chat/completions`。
- **OpenAI 兼容 Responses**：适用于需要内置 Agent 能力（如自动调用搜索、代码执行）的复杂任务。端点为 `/compatible-mode/v1/responses`，并提供配套的 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)、[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md) 和 [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md) 等管理接口。
- **Anthropic 兼容 Messages**：适用于已集成 Anthropic SDK 的应用，支持结构化输出与显式缓存。端点为 `/apps/anthropic/v1/messages`。
- **DashScope 原生协议**：适用于需要最大灵活性（如精细控制 `max_frames`）或使用官方 DashScope SDK 的场景。端点分文本（`/text-generation/generation`）与多模态（`/multimodal-generation/generation`）两类。

### 3. 认证与 SDK
- 所有协议均通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头认证；
- OpenAI/Anthropic 协议可直接使用其官方 SDK（如 `openai==1.50.0+`、`anthropic==0.40.0+`），仅需替换 `base_url` 和 `api_key`；
- DashScope 协议需使用 `dashscope` SDK，并配置 `base_http_api_url`。

## 限制和注意事项

- **地域与模型绑定**：第三方模型（DeepSeek/Kimi/GLM/MiniMax）仅在华北2（北京）地域可用，且需在控制台开通服务后方可调用；
- **上下文长度**：Responses API 为预留工具调用空间，实际可用上下文约为模型窗口的 80%，超出部分将自动截断（不报错）；
- **缓存行为**：Session 缓存（`x-dashscope-session-cache: enable`）仅对 Responses API 生效；显式缓存（`cache_control: {type: "ephemeral"}`）仅 Anthropic 兼容协议支持；
- **音视频支持差异**：
  - `qwen3.8-omni-flash` 在 Responses API 中支持 `input_audio`/`input_video` 类型；
  - `Qwen-Audio` 仅 DashScope 协议支持；
  - `Qwen-VL` 视频理解能力受限于具体模型版本（如仅部分 `qwen-vl-plus` 支持视频文件），详见 [视频理解（Qwen-VL）](../../raw/model-user-guide/model-experience/vision-model/vision.md)；
- **废弃参数**：`thinking.budget_tokens` 已标记为“即将废弃”，新接入应使用 `output_config.effort`（Anthropic）或 `reasoning.effort`（Responses）替代。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


