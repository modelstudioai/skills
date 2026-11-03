# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 Qwen 模型调用方式，包括 OpenAI 兼容的 Chat 和 Responses API、DashScope 原生 API 以及 Anthropic 兼容的 Messages API。开发者可根据现有技术栈和功能需求选择最适配的接口，所有路径均支持多地域部署，并统一通过业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）进行高性能、高稳定性调用。API Key 配置与 SDK 安装等前置准备请参考 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 和 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 支持的模型/功能

Qwen 系列模型覆盖文本生成、[多模态](../concepts/multi-modal.md)理解（VL）、语音（Audio）、代码（Coder）、数学（Math）、全模态（Omni）等能力，同时支持 DeepSeek、Kimi、GLM、MiniMax 等第三方直供模型。不同 API 协议对模型的支持范围存在差异：

- **OpenAI 兼容 Chat API**（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）支持 `Qwen`、`Qwen-VL`、`Qwen-Coder`、`Qwen-Omni`、`Qwen-Math` 及三方模型（如 `DeepSeek`、`Kimi`），但明确指出 **Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 协议。
- **OpenAI 兼容 Responses API**（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）聚焦 Agent 场景，内置联网搜索、网页抓取、代码解释器等工具，当前仅支持 `qwen3.8-max`、`qwen3.7-plus` 等 Qwen 自研文本模型及部分 DeepSeek/GLM/Kimi 模型；非列表中模型仅支持基础兼容能力，Agent 功能受限。
- **DashScope 原生 API**（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）支持最全模型谱系，包括 `Qwen-Audio`、`Qwen-VL`、`Qwen-Coder` 及全部第三方直供模型，是调用音视频等非文本模态的唯一推荐路径。
- **Anthropic 兼容 Messages API**（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 及 `deepseek-v4`、`glm-5.3` 等模型，特别强化了结构化输出（`format`）与深度思考（`output_config.effort`）能力。

> **注意**：文档 1 与文档 6 对 `Qwen-Audio` 的支持描述存在矛盾——文档 1 明确声明其“不支持 OpenAI 兼容协议”，而文档 6 在模型列表中包含 `千问Audio` 且未加限制。依据文档 1 的权威性声明，应以 **DashScope 原生 API 为 Qwen-Audio 的唯一可用接口**，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)不可用。

## 关键参数

各 API 的核心参数设计兼顾兼容性与平台扩展能力，关键字段如下：

- **`model`**：必填字符串，值需严格匹配控制台发布的模型 ID（如 `qwen3.8-max`、`qwen3-vl-plus`）。模型列表详见各文档，例如 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 明确列出 Qwen 3.x 系列及 DeepSeek v4 的具体版本。
- **输入内容结构**：
  - Chat API 使用 `messages` 数组，支持 `system`/`user`/`assistant` 角色，`user` 消息的 `content` 可为 `string` 或含 `type: "image_url"`/`"video_url"` 等的 `array`。
  - Responses API 使用更灵活的 `input` 字段，支持 `string`（纯文本）或 `array`（含 `EasyInputMessage`、`ResponseOutputMessage` 等结构化类型），并原生支持 `input_file`（PDF）、`input_audio`、`input_video`。
  - Anthropic API 使用 `messages` + `system` 字段，`content` 支持 `text`/`image`/`video`/`tool_use` 等类型，其中 `image`/`video` 的 `source.type` 必须为 `url` 或 `base64`。
- **[多模态](../concepts/multi-modal.md)控制参数**：
  - `min_pixels`/`max_pixels`/`total_pixels`（Chat & DashScope）：控制图像/视频帧的分辨率缩放与总像素预算，不同模型有不同默认值与范围（如 `qwen3.8-max` 默认 `min_pixels=65536`，`max_pixels=2621440`）。
  - `fps`（Chat & DashScope & Anthropic）：视频抽帧频率，单位 fps，影响动态理解精度。
  - `max_frames`（DashScope 专有）：视频抽帧总数上限，Chat API 不支持此参数，由服务端自动管理。
- **高级功能参数**：
  - `cache_control`（Chat & Anthropic）：启用显式缓存，`type` 固定为 `"ephemeral"`。
  - `reasoning.effort`（Responses）或 `output_config.effort`（Anthropic）：控制模型思考强度，取值如 `"xhigh"`/`"high"`/`"low"`，不同模型映射规则不同（见 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。
  - `tools`（Responses & Anthropic）：定义可调用工具，Responses 支持内置工具（如 `web_search`），Anthropic 支持自定义 `web_search_20250305` 等。

## 使用方式

### 接入地址与认证
所有 API 均采用 `{WorkspaceId}.<region>.maas.aliyuncs.com` 作为 base URL，地域包括 `cn-beijing`（华北2）、`ap-southeast-1`（新加坡）、`us-east-1`（美国弗吉尼亚）等。调用时需将 `{WorkspaceId}` 替换为控制台获取的真实业务空间 ID。认证统一使用百炼 API Key，可通过 `Authorization: Bearer <api_key>` 或 `x-api-key: <api_key>`（Anthropic）请求头传递。

### 协议选择指南
- **快速迁移 OpenAI 应用**：优先选用 **Chat Completions API**（`/compatible-mode/v1/chat/completions`），其参数与 OpenAI 最接近，适合纯文本或[多模态](../concepts/multi-modal.md)对话场景。
- **构建复杂 Agent**：选用 **Responses API**（`/compatible-mode/v1/responses`），利用其内置工具链、`previous_response_id` 上下文管理、Session 缓存（`x-dashscope-session-cache: enable`）等特性，显著降低多轮对话开发成本。
- **调用音视频/本地文件等非标准模态**：必须使用 **DashScope 原生 API**（`/api/v1/services/aigc/multimodal-generation/generation`），因其支持 `input_file`、`input_audio` 等独有类型。
- **迁移 Anthropic 应用或需要强结构化输出**：选用 **Anthropic Messages API**（`/apps/anthropic/v1/messages`），利用其 `format` JSON Schema 约束与 `output_config.effort` 精细控制能力。

### 示例调用流程（Responses API）
1. 发送 `POST /responses` 请求，携带 `model="qwen3.8-max"`、`input=["你好"]`、`tools=[{"type":"web_search_20250305","name":"web_search"}]`；
2. 获取响应中的 `id`（如 `resp_xxx`）与 `output` 中的 `message.id`（如 `msg_xxx`）；
3. 后续请求传入 `previous_response_id="resp_xxx"`，实现上下文自动拼接；
4. 如需查询历史输入，调用 `GET /responses/{resp_xxx}/input_items`。

## 限制和注意事项

- **域名迁移强制要求**：华北2（北京）、新加坡、中国香港地域已全面推广业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移以获得“卓越的性能和更高的稳定性”（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）。
- **API 路径废弃**：OpenAI 兼容 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到新版 `/compatible-mode/v1/responses`（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **上下文长度限制**：Responses API 为预留工具调用空间，实际最大输入上下文约为模型窗口大小的 80%，超出部分将自动截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。
- **三方模型地域限制**：DeepSeek、Kimi 等第三方直供模型仅在中国站华北2（北京）地域可用，调用前需在控制台开通对应服务（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **参数兼容性**：Responses API 严格遵循“仅处理本文档明确列出的参数”原则，任何未提及的 OpenAI 参数（如 `background`）均被忽略（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


