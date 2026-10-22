# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 Qwen 模型调用方式，包括 OpenAI 兼容 Chat 和 Responses API、DashScope 原生 API 以及 Anthropic 兼容 Messages API。开发者可根据现有技术栈和功能需求（如多轮对话管理、工具调用、结构化输出、音视频理解等）选择最适配的接口。所有接口均支持多地域部署，并推荐使用业务空间专属域名以获得更优性能与稳定性。

## 支持的模型/功能

Qwen 系列模型覆盖文本生成（`qwen3.8-max`、`qwen3.7-plus`、`qwen-flash` 等）、多模态理解（`qwen3.8-omni-flash`、`qwen3-vl-plus`、`Qwen2.5-VL`）、代码生成（`qwen3-coder-flash`）、数学推理（`qwen-math`）及音频理解（`qwen-audio`）。第三方模型（如 `deepseek-v4.1-flash-1017`、`glm-5.3`、`kimi-k3`）亦受支持，但能力范围存在差异：例如 `Qwen-Audio` 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；`QwQ` 模型不建议设置 `system` 消息，而 `QVQ` 模型则忽略 `system` 消息 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

功能层面，**OpenAI 兼容 Chat API** 适用于标准对话场景，支持 `messages` 数组输入与 `tool_calls`；**OpenAI 兼容 Responses API** 提供增强能力，包括内置联网搜索、网页抓取、代码解释器等工具，支持 `previous_response_id` 多轮上下文管理与 Session 缓存，且允许纯字符串输入 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)；**DashScope 原生 API** 是底层协议，区分 `text-generation` 与 `multimodal-generation` 服务端点，对图像/视频输入格式（如 `image` 字段直接传 URL 或 Base64）有更细粒度控制；**Anthropic 兼容 Messages API** 支持 `thinking` 深度推理与 `output_config.effort` 控制思考强度，同时提供结构化 JSON 输出能力 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。

> **注意**：文档 1 与文档 7 对 `max_frames` 参数的支持描述存在矛盾——文档 1（OpenAI 兼容 Chat）明确指出“Qwen-Audio不支持OpenAI兼容协议”，而文档 7（DashScope API）在 `video` 字段说明中未提及其限制，且 `max_frames` 在 OpenAI 兼容路径下被标注为“不支持自定义”。实际开发中，若需视频帧数控制，应优先选用 DashScope 原生 API 或确认模型是否在 Responses API 中启用对应能力。

## 关键参数

| 参数 | 作用 | 适用接口 | 说明 |
|------|------|----------|------|
| `model` | 指定调用模型 | 全部 | 必填。模型列表因接口而异：Chat API 支持广谱模型（含三方直供），Responses API 明确限定为 `qwen3.8-*`/`qwen3.7-*` 等系列及部分 DeepSeek/GLM/Kimi，Anthropic API 则按 Max/Plus/Flash/VL 分类列出 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。 |
| `messages` / `input` | 输入内容 | Chat / Responses | Chat 使用标准 `messages` 数组；Responses 支持 `string` 或 `array`（含 `EasyInputMessage` 结构），并引入 `ResponseOutputMessage`、`Function Call Output` 等专用类型以简化多轮交互。 |
| `fps`, `min_pixels`, `max_pixels`, `total_pixels` | 视频/图像预处理 | Chat / DashScope / Anthropic | 控制抽帧频率、分辨率缩放与总像素预算。`fps` 默认 2.0，取值范围 [0.1, 10]；`min_pixels`/`max_pixels` 因模型而异（如 `qwen3.8-max` 图像默认 `65536`/`2621440`）；`total_pixels` 影响 Token 消耗，长视频建议调低 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。 |
| `tools`, `tool_choice`, `parallel_tool_calls` | 工具调用控制 | Responses / Anthropic | Responses 支持内置工具（`web_search`, `code_interpreter`）与自定义 function；Anthropic 支持 `web_search_20250305` 等日期后缀工具，且要求 `system` 中传入 `x-anthropic-billing-header` 才能生效。 |
| `stream`, `store`, `previous_response_id` | 流式/状态管理 | Responses | `stream=true` 启用流式；`store=false` 时响应不可被 `previous_response_id` 引用；`previous_response_id` 是 Responses API 的核心多轮机制，替代手动拼接 `messages`。 |
| `temperature`, `top_p`, `max_tokens` | 生成控制 | 全部 | `temperature` 范围统一为 [0, 2)，但 Anthropic 兼容接口特别强调其与官方 [0.0, 1.0] 的差异；`max_tokens` 含义因模型而异：对 `glm-5.3` 表示回复+思考总长，对多数模型仅限回复长度 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。 |

## 使用方式

### 接入地址与认证
所有接口均需替换 `{WorkspaceId}` 为真实业务空间 ID，并配置百炼 API Key（通过 `Authorization: Bearer` 或 `x-api-key` 请求头）。推荐使用业务空间专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）仍可用但非最优 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

- **OpenAI 兼容 Chat**：`POST /compatible-mode/v1/chat/completions`
- **OpenAI 兼容 Responses**：`POST /compatible-mode/v1/responses`（新版路径，旧版 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用）
- **DashScope 原生**：文本模型用 `/api/v1/services/aigc/text-generation/generation`，多模态模型用 `/api/v1/services/aigc/multimodal-generation/generation`
- **Anthropic 兼容**：`POST /apps/anthropic/v1/messages`

### 典型调用流程（Responses API）
1. 发起首次请求，`input` 为用户问题，`store=true`；
2. 解析响应，提取 `id`（如 `resp_xxx`）与 `output[].id`（如 `msg_xxx`）；
3. 下次请求传入 `previous_response_id=resp_xxx`，新 `input` 将自动追加至历史上下文；
4. 如需查询历史输入项，调用 `GET /responses/{response_id}/input_items`；
5. 如需删除已存储响应，调用 `DELETE /responses/{response_id}`。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）仅在中国站华北2（北京）地域可用，且需在控制台单独开通服务 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **上下文长度**：Responses API 的最大输入上下文约为模型窗口大小的 80%，超出部分将自动截断而不报错；Chat API 无此显式说明，但受模型原生窗口限制。
- **缓存与计费**：`cache_control.type=ephemeral` 用于显式缓存，命中后按缓存计费；Session 缓存（`x-dashscope-session-cache: enable`）由服务端自动管理，降低多轮延迟 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **错误处理**：`GET /responses/{id}` 或 `DELETE /responses/{id}` 时，若 `id` 不存在或 `store=false`，返回 `InvalidParameter` 错误；`input_items` 查询中 `has_more=true` 时需用 `last_id` 分页。
- **音视频支持**：`qwen3.8-omni-flash` 是唯一在 Responses API 中支持 `input_audio`/`input_video` 的模型；其他模型需通过 DashScope 原生 API 或 Chat API（后者需 `type=input_audio` 等）接入。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)


