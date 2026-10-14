# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型，并统一通过业务空间专属域名接入，保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持以下核心模型与能力：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3-coder-flash`、`qwen-plus` 等；
- **多模态模型**：`qwen3.8-omni-flash`、`qwen3.7-vl-plus`、`qwen3-vl-plus`、`QVQ`、`QwQ`（注意：QwQ 不建议设置 system message，QVQ 的 system message 不生效）；
- **音频/视频理解**：`qwen3.8-omni-flash` 支持 `input_audio` 和 `input_video`；`Qwen-VL` 和 `QVQ` 支持图像与视频输入（含 `video_url`、`video` 图像列表、`fps`、`min_pixels`、`max_pixels`、`total_pixels` 等参数）；
- **Agent 能力**：OpenAI 兼容的 Responses API 内置联网搜索、网页抓取、代码解释器、文搜图、知识库搜索等工具；Anthropic 兼容 Messages API 支持 `tool_use`/`tool_result` 流程；DashScope 原生协议需配合 SDK 工具链使用。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅支持 DashScope 协议 [Qwen-Audio不支持OpenAI兼容协议，仅支持DashScope协议](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
> **注意**：`max_frames` 参数在 OpenAI 兼容 API 中不支持自定义，仅 DashScope 原生协议支持 [使用 OpenAI 兼容API调用时，不支持自定义`max_frames`参数](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

## 关键参数

| 参数 | 类型 | 说明 | 所属协议 |
|------|------|------|----------|
| `model` | `string` | 必填。模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`。不同协议支持范围略有差异（Responses API 列表最全，Chat API 包含三方模型） | 全部 |
| `messages` / `input` | `array` / `string` | 对话上下文或纯文本输入。OpenAI Chat 和 DashScope 使用 `messages`；Responses API 同时支持 `string` 和 `array` 格式 | Chat / DashScope / Responses |
| `system` | `string` or `array` | Anthropic 协议专用系统提示字段；OpenAI Chat 中为 `messages[0].role === 'system'` | Anthropic |
| `tools` | `array` | 工具定义数组。Responses API 支持内置工具（如 `web_search`）和自定义 function；Anthropic 支持 `tool_use`；DashScope 需结合 SDK 工具注册 | Responses / Anthropic |
| `reasoning.effort` / `output_config.effort` | `string` | 控制思考强度（`low`/`medium`/`xhigh`/`max`）。Responses API 使用 `reasoning.effort`；Anthropic 使用 `output_config.effort`；DashScope 未显式暴露该参数 | Responses / Anthropic |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | `number` | 视频/图像预处理参数，用于控制抽帧频率与分辨率缩放。全部协议均支持，但字段位置和嵌套结构不同（如 Chat API 在 `image_url`/`video_url` 对象内，DashScope 在 `video` 对象顶层） | Chat / DashScope / Responses（部分） |

## 使用方式

### 1. 接入地址（Base URL）

所有协议均推荐使用**业务空间专属域名**（华北2、新加坡、中国香港地域已上线），格式为：  
`https://{WorkspaceId}.{region}.maas.aliyuncs.com/{path}`  
其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。

- **OpenAI 兼容 Chat**：`/compatible-mode/v1/chat/completions`  
- **OpenAI 兼容 Responses**：`/compatible-mode/v1/responses`（旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用）  
- **Anthropic 兼容 Messages**：`/apps/anthropic/v1/messages`  
- **DashScope 原生协议**：  
  - 文本模型：`/api/v1/services/aigc/text-generation/generation`  
  - 多模态模型：`/api/v1/services/aigc/multimodal-generation/generation`

> **注意**：Anthropic 协议不提供 `/v1/models` 接口，客户端模型发现请求将返回 404 [接口范围：仅提供 Messages 接口（`/v1/messages`），不提供模型列表接口（`/v1/models`）](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

### 2. 认证与 SDK

- 统一使用百炼 API Key，通过 `Authorization: Bearer <key>` 或 `x-api-key`（Anthropic）头传递；
- OpenAI SDK 可直接复用（配置 `base_url` 即可）；Anthropic SDK 需替换 `base_url`；DashScope SDK 需设置 `base_http_api_url`；
- 所有协议均支持流式响应（`stream=true`）和 Session 缓存（如 Responses API 的 `x-dashscope-session-cache: enable` 头）。

### 3. 核心操作示例

- **创建响应（Responses API）**：`POST /compatible-mode/v1/responses`，支持 `previous_response_id` 实现多轮对话状态管理；  
- **获取/删除响应**：`GET /responses/{id}` 和 `DELETE /responses/{id}`，仅当创建时 `store=true` 才可操作；  
- **查询输入项**：`GET /responses/{id}/input_items`，用于审计多轮对话历史；  
- **结构化输出（Anthropic）**：启用 `output_config.format.type = "json_schema"` 并传入标准 JSON Schema，严格模式仅限 `qwen3.8`/`deepseek`/`glm` 系列 [结构化输出配置](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

## 限制和注意事项

- **上下文长度**：Responses API 最大输入上下文约为模型窗口的 80%，超出部分自动截断（不报错）；  
- **参数兼容性**：OpenAI 兼容 API **忽略所有未文档化的 OpenAI 参数**（如 `background` 异步参数不支持）；  
- **温度范围差异**：Anthropic 协议中 `temperature` 取值范围为 `[0, 2)`，不同于官方 `[0.0, 1.0]`，迁移时需校验 [temperature 取值范围](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)；  
- **缓存行为**：`cache_control: {type: "ephemeral"}` 在 Chat、Anthropic、DashScope 中语义一致，但仅在明确支持显式缓存的模型（如 `qwen3.8-max`）上生效；  
- **计费单位**：`created_at` 字段在 Responses API 返回中为毫秒级时间戳，而 Chat/Anthropic/DashScope 为秒级，解析时需注意单位差异；  
- **废弃参数**：`thinking.budget_tokens` 在 Anthropic 协议中即将废弃，新接入应使用 `output_config.effort` 替代。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


