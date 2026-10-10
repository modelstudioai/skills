# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API（包括 DashScope 原生接口和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入（如 prompt、messages、文件、图像等），即可获得由应用封装的完整推理、工具调用、RAG 检索等结果。该能力支持同步、异步及流式响应模式，适用于从实时对话到长周期任务的各类场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）及工作流（Workflow）三类应用，具体能力因类型而异。例如，`memory_id` 和 `rag_options` 仅限智能体应用；`flow_stream_mode` 仅限工作流应用 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **多模态能力**：支持文本、图像（需选用通义千问 VL 系列模型）、音频/视频/文档（需配置对应文件处理方式）输入，相关模型能力详见 [图像与视频理解](../../raw/model-user-guide/model-experience/vision-model/vision.md)。
- **高级功能**：
  - **长期记忆**：通过 `memory_id` 参数启用，自动构建并复用用户偏好信息；
  - **RAG 检索**：通过 `rag_options` 配置知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）等精准检索范围；
  - **插件调用**：通过 `biz_params.user_defined_params` 传递插件 ID 与参数，实现外部系统集成；
  - **深度思考模式**：通过 `enable_thinking` 与 `has_thoughts` 组合控制是否输出思考过程 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。

> **注意**：`flow_stream_mode` 的默认值在文档 4 中定义为 `full_thoughts`，但明确标注“**不推荐新业务使用**”，并建议改用 `message_format` 或 `message_format_plus`。此设计与实际最佳实践存在偏差，开发者应主动覆盖该参数而非依赖默认值。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 传输位置（HTTP） |
|--------|------|------|------|------------------|
| `app_id` | string | 是 | 应用唯一标识，从控制台获取 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) | URL 路径（`/apps/{APP_ID}/completion`） |
| `prompt` / `input` | string / array | 是 | 单轮文本输入或结构化消息数组（含 system/user/assistant 角色） | `input` 对象（DashScope）或顶层 `input` 字段（Responses API） |
| `session_id` | string | 否 | 用于恢复对话历史，1 小时无请求后失效 | `input` 对象 |
| `messages` | array | 否（替代 `prompt`） | 多轮对话上下文，优先级高于 `session_id` | `input` 对象 |
| `workspace` | string | 否（子空间必需） | 业务空间 ID，调用子业务空间或特定地域（如法兰克福、北京）应用时必需 | Header: `X-DashScope-WorkSpace` |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（`true` 推荐） | Header: `X-DashScope-SSE: enable`（DashScope）或 `stream` 字段（Responses API） |
| `incremental_output` | boolean | 否（仅 stream=true 时有效） | [流式输出](../concepts/streaming-output.md)是否增量（`true` 推荐） | `parameters` 对象 |
| `biz_params` | object | 否 | 传递自定义变量、插件参数、用户鉴权 token 等 | `input` 对象（DashScope）或 `extra_body`（Responses API） |
| `rag_options` | object | 否（仅智能体） | 控制知识库检索行为，含 `pipeline_ids`、`metadata_filter` 等 | `parameters` 对象 |

## 使用方式

- **DashScope 原生 API**（推荐用于全功能控制）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 支持 SDK（Python/Java）与 HTTP 直接调用，参数映射严格遵循各语言 SDK 文档（如 Java 中 `appId` 对应 HTTP URL 中的 `{APP_ID}`）。
  - 流式调用需设置 Header `X-DashScope-SSE: enable` 并解析 SSE 响应。

- **OpenAI 兼容 Responses API**（推荐用于快速迁移或生态集成）：
  - Endpoint（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - Endpoint（异步）：同上，但请求体中 `background=true`，返回 `task_id` 后需轮询 `GET /responses/{task_id}`。
  - 输入格式兼容 OpenAI Messages 数组，支持 `input_text`/`input_image`/`input_file` 多模态类型 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

- **调试与验证**：所有应用均提供控制台内置的 **API 调试** 功能（路径：应用卡片 → 发布 → API 调试），可免代码验证参数与响应。

## 限制和注意事项

- **地域限制**：DashScope API 文档（文档 3 和 4）及 Responses API 文档（文档 6 和 7）均明确声明“**仅适用于华北2（北京）地域**”。跨地域调用需确认目标地域是否已开放对应 API endpoint。
- **异步限制**：异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略），且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动管理，必须显式传递完整 `messages` [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **凭证获取**：APP ID 和 Workspace ID **仅支持通过控制台手动获取**，不提供 API 或 CLI 查询接口，自动化部署需预先配置 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `image_list`/`file_list` 要求 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`flow_stream_mode` 要求 Java SDK ≥2.22.23。低版本 SDK 可能导致参数无效或调用失败。
- **参数冲突**：当同时传入 `session_id` 和 `messages` 时，系统**优先使用 `messages` 内容，忽略 `session_id` 和 `prompt`**，此行为在文档 4 中明确定义，开发者需避免冗余参数。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


