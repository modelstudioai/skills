# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、[多模态](../concepts/multimodal.md)输入、自定义参数传递等能力，适用于构建生产级 AI 应用集成。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用和工作流应用三类，但各类型支持的参数与行为存在差异。例如，`enable_thinking` 参数仅在 [新版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 中定义，而 `flow_stream_mode` 仅适用于工作流应用，见 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **[多模态](../concepts/multimodal.md)能力**：支持图像（需选用通义千问 VL 系列模型）和文件（仅智能体应用）输入，相关配置要求详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **[长期记忆](../concepts/memory.md)**：仅旧版及新版智能体应用支持 `memory_id` 参数，用于启用用户级[长期记忆](../concepts/memory.md)；工作流应用不支持该功能。
- **思考模式**：新版智能体应用支持 `enable_thinking` 和 `has_thoughts` 组合控制深度思考过程的生成与返回；工作流应用则通过 `has_thoughts` 控制插件调用与知识检索过程的透出。

> **注意**：文档中关于 `workspace` 参数的使用说明存在不一致。[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域下为必需，且是 Base URL 的组成部分；而 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 和 [新版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 均描述为“仅调用子业务空间的应用时需传递”，未提及地域限制。开发者应以控制台实际地域要求为准，优先参考前一文档的地域性说明。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属接口 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取。HTTP 调用时需嵌入 URL 路径。 | 全部 |
| `prompt` / `input` | string / object | 是 | 用户指令或结构化输入。`prompt` 用于 DashScope API 单轮文本；`input` 用于 Responses API，支持字符串、消息数组及[多模态](../concepts/multimodal.md)内容。 | DashScope API / Responses API |
| `session_id` | string | 否 | 对话历史标识，仅智能体应用支持，1 小时无请求后失效。 | DashScope API |
| `messages` | array | 否 | 多轮对话消息数组（system/user/assistant），替代 `prompt` 和 `session_id`。DashScope SDK 要求 Python ≥1.20.14，Java ≥2.17.0。 | DashScope API |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。Responses API 默认 `false`；DashScope API 默认 `false`，推荐设为 `true`。 | 全部 |
| `incremental_output` | boolean | 否 | 流式模式下是否增量输出（即后续 chunk 不重复前序内容）。仅 DashScope API 支持。 | DashScope API |
| `flow_stream_mode` | string | 否 | 工作流专属流式模式，取值 `message_format_plus`（推荐）、`message_format` 或 `full_thoughts`（不推荐新业务）。 | DashScope API（工作流） |
| `biz_params` | object | 否 | 传递自定义变量、插件参数及用户鉴权信息，结构复杂，需与应用内配置严格一致。 | 全部 |
| `workspace` | string | 否（但受地域/业务空间约束） | 业务空间 ID，调用子业务空间应用或特定地域模型时必需，需通过 Header `X-DashScope-WorkSpace` 传递（DashScope）或作为 URL 路径一部分（Responses）。 | 全部 |

## 使用方式

- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  推荐用于需要最大灵活性和性能的场景。SDK 调用简洁（如 Python `Application.call()`），HTTP 调用需将参数按 `input`（如 `prompt`, `session_id`）和 `parameters`（如 `stream`, `incremental_output`）对象组织。流式需设置 Header `X-DashScope-SSE: enable`。

- **OpenAI 兼容 Responses API**  
  Endpoint（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  Endpoint（异步）：同上，请求体中 `background=true`  
  适用于复用现有 OpenAI 生态代码库。`input` 字段统一承载所有输入（含多轮消息、图片、文件），`stream` 和 `background` 为顶层布尔参数。异步调用必须配合轮询 `retrieve` 接口获取结果，且不支持流式。

- **调试与开发**  
  控制台提供“应用卡片 → 发布 → API 调试”在线调试入口，可快速验证参数组合。所有调用均需配置有效的 `DASHSCOPE_API_KEY`（通过环境变量或代码传入）。

## 限制和注意事项

- **地域限制**：[工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) 和 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 均明确标注“仅适用于华北2（北京）地域”，其他地域调用可能失败。
- **参数冲突**：当 `messages` 与 `session_id` 同时传入时，DashScope API 会忽略 `session_id` 和 `prompt`，以 `messages` 为准；Responses API 则要求每次请求传递完整对话历史，暂不支持 `pre_response_id` 或 `conversation_id` 上下文复用。
- **版本兼容性**：多个参数对 SDK 版本有强依赖。例如，`messages` 要求 DashScope Python SDK ≥1.20.14；`flow_stream_mode` 要求 Python ≥1.24.0 / Java ≥2.22.23；`file_list` 要求 Python ≥1.24.7 / Java ≥2.21.13。务必检查 SDK 版本。
- **异步限制**：Responses API 的异步模式（`background=true`）不支持[流式输出](../concepts/streaming-output.md)（`stream=true`），且任务状态需主动轮询，无 Webhook 回调机制。
- **凭证获取**：APP ID 和 Workspace ID **仅能通过控制台手动获取**，不支持 API 或 CLI 查询，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)


