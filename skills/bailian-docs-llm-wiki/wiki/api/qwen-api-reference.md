# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope 接口。所有接口均支持多地域部署、业务空间专属域名及主流多模态能力，开发者可根据技术栈和功能需求选择最适配的协议。

## 支持的模型/功能

Qwen API 支持全系列千问模型及部分第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理、Agent 工具调用等场景：

- **文本模型**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen-turbo`、`qwen-coder-next` 等；
- **多模态模型**：`qwen3.8-omni-flash`（音视频端到端）、`qwen3-vl-plus`、`qwen-vl-max`、`QVQ`、`Qwen2.5-VL`；
- **专用模型**：`qwen3.5-math`、`qwen3.5-ocr`（PDF 解析）、`qwen3.5-audio`（仅 DashScope 协议支持，[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）；
- **第三方模型**：`deepseek-v4-pro`、`glm-5.3`、`kimi-k3`、`MiniMax-M2.5` 等（部分仅限华北2地域，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。

> **注意**：Qwen-Audio **不支持 OpenAI 兼容协议**，仅可通过 DashScope 原生接口调用；QwQ 模型不建议设置 `system` 消息，QVQ 模型的 `system` 消息无效 —— 该限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中一致确认。

## 关键参数

不同协议下核心参数语义与约束存在差异，需按协议严格使用：

| 参数 | OpenAI Chat (`/chat/completions`) | OpenAI Responses (`/responses`) | Anthropic Messages (`/v1/messages`) | DashScope Native |
|------|-----------------------------------|------------------------------------|----------------------------------------|------------------|
| `model` | 必填；支持 Qwen/VL/Coder/Omni/三方模型（见文档1） | 必填；明确列出 `qwen3.8-max` 等 50+ 具体型号（见文档2） | 必填；分 Max/Plus/Flash/Turbo/Coder/VL 等类别（见文档5） | 必填；支持同文档1范围，但 `qwen3.5-audio` 仅此处可用（见文档8） |
| `messages` / `input` | `array` of `{role, content}`；`content` 支持 `text`/`image_url`/`video_url` 等结构化类型 | `string` 或 `array`；`array` 元素为 `EasyInputMessage`，支持 `input_audio`/`input_video`（仅 `qwen3.8-omni-flash`） | `array` of `{role, content}`；`content` 为 `text`/`image`/`video` 对象，`image.source.type` 支持 `url`/`base64` | `messages` 在 `input` 对象内；`content` 为 `string` 或 `array`，`image`/`video` 字段为扁平字符串或数组（见文档8） |
| `max_tokens` | 不支持（由 `response_format` 或模型隐式控制） | 不支持（由 `reasoning.effort` + 输出长度隐式控制） | **必填**；含义依模型而异：对 `qwen3.8-max` 是回复+思考总长；对 `qwen3.5-plus` 仅为回复长度（见文档5） | 不支持（由 `stop` 参数或模型窗口隐式控制） |
| `temperature` | `[0, 2)`（文档1） | `[0, 2)`（文档2） | `[0, 2)`（文档5），**明确指出与 Anthropic 官方 `[0.0, 1.0]` 不同** | `[0, 2)`（文档8） |
| `stream` | 支持 | 支持 | 支持 | 支持 |
| `tools` | 不支持（仅 Responses 支持） | 支持内置工具（`web_search`, `code_interpreter`）和自定义 function（见文档2） | 支持 `tools` + `tool_choice` 定义[函数调用](../concepts/function-calling.md)（见文档5） | 不支持（需通过 `function_call` 模式在 `messages` 中显式构造） |

`min_pixels`/`max_pixels`/`total_pixels`（视频处理）和 `fps`/`max_frames`（抽帧控制）等视觉参数在 OpenAI Chat（文档1）、DashScope（文档8）中定义完整，Anthropic Messages（文档5）仅支持基础 `video` 类型但未说明像素参数，Responses（文档2）仅在 `input_video` 中提及 `fps`。开发者应优先参考 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 获取最新多模态参数规范。

## 使用方式

### 1. 基础接入
所有协议均需：
- 替换 `{WorkspaceId}` 为真实业务空间 ID（控制台查看）；
- 使用百炼 API Key（非 OpenAI Key），通过 `Authorization: Bearer <key>` 或 SDK 配置；
- 优先采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）仍可用但**不推荐**（文档1、2、5、8 均强调此迁移建议）。

### 2. 协议选择指南
- **快速迁移 OpenAI 应用**：用 `/chat/completions`（文档1）或 `/responses`（文档2），前者轻量，后者支持工具链与上下文缓存；
- **构建复杂 Agent**：首选 `/responses`，利用 `previous_response_id`、`tools`、`function_call` 输出结构（文档2、4）；
- **迁移 Anthropic 应用**：用 `/v1/messages`（文档5），注意 `temperature` 范围与 `output_config.effort` 控制思考强度；
- **需要音频/本地文件/细粒度视频控制**：必须用 DashScope 原生接口（文档8），其 `video` 字段支持 `max_frames`，且 `qwen3.5-audio` 仅在此处可用。

### 3. 多轮对话管理
- **`/responses`**：通过 `previous_response_id`（自动拼接历史）或 `conversation`（会话级管理）实现，配合 `store=true` 持久化（文档2、4、6）；
- **`/chat/completions`**：需客户端手动维护 `messages` 数组；
- **`/v1/messages`**：无内置会话管理，需客户端维护 `messages` 并传入全部历史。

## 限制和注意事项

- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，调用前须在控制台开通（文档1）；
- **协议废弃**：OpenAI Responses 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` **已停止维护**，必须迁移到 `/compatible-mode/v1/responses`（文档2）；
- **缓存行为**：`x-dashscope-session-cache: enable` 仅对 `/responses` 生效（文档2），`/chat/completions` 和 `/v1/messages` 需依赖 `cache_control` 显式标记（文档1、5）；
- **视频处理差异**：`total_pixels` 参数仅在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 中明确定义（含各模型取值），DashScope 文档（文档8）未提及，Anthropic 文档（文档5）未覆盖，开发音视频应用时应以该文档为准；
- **错误处理**：`/responses` 相关操作（获取、删除、列表）均要求 `store=true`，否则返回 `not found` 错误（文档4、6、7）；
- **计费单位**：`/responses` 的 `usage.output_tokens_details.reasoning_tokens` 明确分离思考 [Token](../concepts/token.md)（文档4），而 `/chat/completions` 无此细分，计费逻辑需按协议区分。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


