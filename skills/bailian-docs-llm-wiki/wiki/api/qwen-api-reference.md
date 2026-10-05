# qwen api reference

阿里云百炼平台提供多种 API 接口调用 Qwen 系列大模型，包括 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat 和 Responses）、Anthropic 兼容接口（Messages）以及原生 DashScope 接口。所有接口均支持多地域部署、业务空间专属域名，并统一通过 WorkspaceId 进行路由。开发者可根据现有技术栈选择最适配的协议，无需修改核心逻辑即可完成迁移。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，覆盖文本生成、多模态理解（图像/视频/音频）、代码生成、数学推理等场景：

- **Qwen 系列**：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3.5-ocr`、`qwen3-vl-plus`、`qwen3.8-omni-flash`、`qwen-audio`（仅 DashScope 协议支持，见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）  
- **多模态能力**：Qwen-VL、QVQ、Qwen-Omni 支持 `image_url`、`video_url`、`video`（图像列表）、`input_audio`、`input_video` 等输入类型；其中 Qwen-Omni 可同时理解视频的视觉与音频信息  
- **工具调用**：OpenAI 兼容 Responses API 内置 `web_search`、`web_extractor`、`code_interpreter`、`file_search` 等工具；Anthropic 兼容 Messages API 支持标准 `tool_use`/`tool_result` 流程  
- **结构化输出**：Anthropic 兼容接口通过 `output_config.format.type = "json_schema"` 实现强约束 JSON 输出，Qwen3.8+、DeepSeek-v4、GLM-5.3 等模型支持严格 Schema 校验  

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用。

## 关键参数

| 参数 | 作用 | 适用接口 | 说明 |
|------|------|----------|------|
| `model` | 指定模型名称 | 全部 | 必填；不同接口支持的模型范围略有差异（如 Responses API 明确列出 `qwen3.8-omni-flash`，而 Chat API 仅泛称“Qwen-Omni”） |
| `messages` / `input` | 对话上下文 | Chat / Responses / DashScope | Chat 和 DashScope 使用 `messages` 数组；Responses 支持 `string` 或 `array`；Anthropic 使用 `messages` + `system` 字段 |
| `stream` | 启用流式响应 | 全部 | 默认 `false`；流式返回时需按协议解析事件（如 OpenAI 的 `data: {...}`） |
| `temperature` / `top_p` | 采样控制 | 全部 | OpenAI/Responses 接口取值范围 `[0, 2)`；Anthropic 兼容接口明确指出其范围与官方 `[0.0, 1.0]` 不同，迁移时需校准 |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | 视频/图像预处理 | Chat / DashScope / Anthropic | 控制抽帧频率、分辨率缩放阈值；`total_pixels` 为 Responses API 特有参数，用于限制视频总像素量（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)） |
| `reasoning.effort` / `output_config.effort` | 思考强度控制 | Responses / Anthropic | Responses 使用 `reasoning.effort`（如 `"high"`），Anthropic 使用 `output_config.effort`（如 `"xhigh"`）；二者语义一致但参数路径不同 |

> **注意**：`thinking.budget_tokens` 在 Anthropic 兼容接口中已被标记为“即将废弃”，新接入应使用 `output_config.effort`；而 Responses API 的 `reasoning.effort` 为当前主推参数，无废弃提示。

## 使用方式

### 1. 域名与认证
- **基础 URL**：全部接口均采用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，支持地域包括华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港  
- **协议路径**：
  - OpenAI 兼容 Chat：`/compatible-mode/v1/chat/completions`  
  - OpenAI 兼容 Responses：`/compatible-mode/v1/responses`（旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用，见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）  
  - Anthropic 兼容 Messages：`/apps/anthropic/v1/messages`  
  - DashScope 原生：`/api/v1/services/aigc/{text-generation|multimodal-generation}/generation`  
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头传入百炼 API Key（需先[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）

### 2. 多轮对话管理
- **Chat API**：依赖客户端维护完整 `messages` 数组，服务端无状态  
- **Responses API**：提供两种轻量方案：
  - `previous_response_id`：传入上一轮 `response.id`，服务端自动拼接历史上下文  
  - `conversation`：绑定会话 ID，历史自动持久化（推荐用于长周期对话）  
- **Session 缓存**：在请求头添加 `x-dashscope-session-cache: enable`，服务端自动缓存并复用上下文，降低延迟与 Token 消耗（详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在中国站华北2（北京）地域可用，调用前需在百炼控制台开通对应服务  
- **模型能力差异**：
  - QwQ 模型不建议设置 `system` 消息；QVQ 模型的 `system` 消息无效  
  - `Qwen-Audio` 仅支持 DashScope 协议，不兼容 OpenAI（见 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）  
- **上下文截断**：Responses API 为预留工具调用空间，实际最大输入上下文约为模型窗口的 80%，超出部分自动截断且不报错  
- **视频处理限制**：`max_frames` 参数仅 DashScope 接口支持自定义；[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（Chat/Responses）强制使用各模型默认值（如 Qwen3-VL 系列为 2000）  
- **结构化输出触发条件**：Anthropic 兼容接口要求 `system` 或 `messages` 中必须包含不区分大小写的 "JSON" 关键词，否则抛出 `'messages' must contain the word 'json' in some form` 错误  

> **注意**：文档 1 与文档 8 对 `min_pixels`/`max_pixels` 的取值描述存在细微差异（如文档 1 列出 `qwen3.8-omni-flash` 的 `min_pixels` 默认值为 `24576`，文档 8 未单独列出该模型）。以最新发布的 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 为准，因其参数说明更详尽且包含 Omni 系列专项取值。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


