# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、DashScope 原生协议及 Anthropic 兼容协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 qwen3.8-max、qwen3.7-plus、qwen3-vl-plus 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持以下核心模型类型与能力：

- **文本大模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-plus` 等全系列商业版与开源版模型；
- **多模态模型**：`qwen3.8-omni-flash`、`qwen3.7-vl-plus`、`qwen3.5-vl`、`QVQ`、`Qwen2.5-VL`，支持图像、视频、音频输入；
- **专用模型**：`qwen3-coder-flash`（代码）、`qwen3.5-math`（数学）、`qwen-audio`（语音，仅 DashScope 协议支持）；
- **第三方模型**：DeepSeek（v4 系列）、Kimi（k3/k2.7-code）、GLM（5.x）、MiniMax（M2.5/M3.1-Flash）等，其中三方直供模型**仅在中国站华北2（北京）地域可用**，且需在控制台开通对应服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

功能层面，不同协议提供差异化能力：
- **OpenAI Chat Completions**：标准对话流，支持 `messages` 数组、`system` 角色、多模态 `type` 字段（`image_url`/`video_url`/`input_audio`）；
- **OpenAI Responses API**：增强型 Agent 接口，内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 多轮上下文管理与 `x-dashscope-session-cache` 自动缓存 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；
- **DashScope 原生 API**：最底层协议，区分 `text-generation` 与 `multimodal-generation` 服务端点，支持 `max_frames` 等细粒度视频参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)；
- **Anthropic Messages**：兼容 Claude 生态，支持 `tool_use`/`tool_result` 结构化工具交互、`output_config.effort` 思考强度控制及 `format` 结构化输出。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅可通过 DashScope 原生 API 调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型设置 `system` 不生效 —— 此限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致声明。

## 关键参数

| 参数 | 协议支持 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，模型 ID。OpenAI Chat 与 DashScope 支持更广谱系（含 Qwen-Audio），Responses API 仅限列表内文本/多模态模型 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) | `"qwen3.8-omni-flash"` |
| `messages` / `input` | Chat/Responses/DashScope | 对话上下文。Chat 与 DashScope 使用 `messages` 数组；Responses 支持 `string` 或 `array`（含 `EasyInputMessage` 结构）；Anthropic 使用 `messages` + `system` 字段 |
| `fps` | Chat/Responses/DashScope/Anthropic | 视频抽帧频率（单位：帧/秒），范围 `[0.1, 10]`。DashScope 文档明确支持 `max_frames`，而 OpenAI 兼容协议不支持该参数 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) |
| `min_pixels` / `max_pixels` / `total_pixels` | Chat/Responses/DashScope | 图像/视频分辨率控制参数，取值因模型和输入类型而异（如 `qwen3.8-max` 默认 `min_pixels=65536`，`Qwen2.5-VL` 默认 `3136`） | `{"type": "image_url", "image_url": {"url": "..."}, "min_pixels": 65536}` |
| `temperature` | 全部 | 采样温度，**OpenAI/Responses/DashScope 取值范围为 `[0, 2)`，Anthropic 兼容协议亦同，但需注意其官方范围为 `[0.0, 1.0]`**，迁移时需校验数值合理性 |
| `tools` | Responses/Anthropic | 工具定义数组。Responses 支持内置工具（`web_search`, `code_interpreter`）与自定义 function；Anthropic 支持 `web_search_20250305` 等带日期后缀的联网搜索工具，且要求 `system` 中传入 `x-anthropic-billing-header` 标识 |

## 使用方式

### 1. 基础接入
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台查看）；
- 配置百炼 API Key（环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer` / `x-api-key`）；
- **强烈建议迁移至业务空间专属域名**（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

### 2. 协议选择指南
- **快速迁移 OpenAI 应用**：优先使用 `/compatible-mode/v1/chat/completions`（标准对话）或 `/compatible-mode/v1/responses`（需 Agent 能力）；
- **需要精细控制视频处理**：选用 DashScope 原生 API，利用 `max_frames` 限制抽帧总数；
- **已集成 Anthropic SDK**：切换 `base_url` 至 `/apps/anthropic/v1/messages`，调整 `temperature` 范围并启用 `output_config.effort`；
- **调用 Qwen-Audio 或需 `max_frames`**：必须使用 DashScope 协议。

### 3. 多轮对话实现
- **Responses API**：通过 `previous_response_id`（推荐）或 `conversation` 字段自动管理历史上下文；
- **Chat API**：手动维护 `messages` 数组，将上一轮 `assistant` 回复追加至数组末尾；
- **Anthropic API**：按标准 messages 数组顺序拼接历史消息。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，其他地域调用将失败；
- **协议差异**：
  - Responses API 的 `/api/v2/apps/protocols/compatible-mode/v1/responses` 旧路径已停用，必须迁移至 `/compatible-mode/v1/responses`；
  - Anthropic 兼容 API **不提供 `/v1/models` 列表接口**，客户端模型发现请求将返回 404；
  - `thinking.budget_tokens` 参数在 Anthropic 协议中**即将废弃**，新接入应使用 `output_config.effort`；
- **输入限制**：
  - OpenAI Chat 的 `messages[].content` 为 `array` 时，`type` 必须显式声明（`text`/`image_url` 等），不支持 DashScope 的 `{"image": "url"}` 简写；
  - Responses API 的 `input_file`（PDF）仅 `qwen3.8-flash`/`qwen3.8-max`/`qwen3.5-ocr` 支持，且页数上限受 `ocr_options.task` 影响（`document_parsing` 时最多 50 页）；
- **缓存与计费**：`cache_control: {type: "ephemeral"}` 仅在 Chat 和 Anthropic 协议中支持显式缓存断点；Session 缓存（`x-dashscope-session-cache: enable`）仅 Responses API 支持，且默认关闭；
- **错误处理**：`store=false` 的 Responses 不可被 `retrieve` 或 `delete`；`previous_response_id` 引用的响应有效期为 7 天。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


