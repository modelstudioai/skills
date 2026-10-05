# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、自定义参数传递等关键功能，适用于构建生产级 AI 应用集成。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用。其中，[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 专为 Agent 2.0 设计，而 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 覆盖更广的兼容场景。
- **多模态能力**：支持图像（需选用通义千问 VL 系列模型）和文件（仅智能体应用）输入，通过 `image_list` 或 `file_list`（DashScope API）及 `input_image`/`input_file`（Responses API）字段传入。
- **调用模式**：
  - **同步调用**：适用于实时交互，立即返回结果（如 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 所述）；
  - **异步调用**：适用于耗时任务（如复杂报告生成），返回任务 ID 后可轮询状态，避免超时。
- **思考与检索增强**：支持 `enable_thinking`（新版智能体）和 `has_thoughts`（所有类型）控制思考过程输出；支持 `rag_options` 配置知识库检索（仅智能体应用）。

> **注意**：文档中明确指出，[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 和 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 均声明“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项，且是 Base URL 的组成部分。这表明实际地域支持范围大于文档所限，开发者应以控制台可用地域和实际请求成功率为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 获取。HTTP 调用时需嵌入 URL 路径。 | DashScope & Responses |
| `prompt` / `input` | string / array | 是 | 用户指令。`prompt` 用于单轮文本（DashScope）；`input` 可为字符串或消息数组（Responses），支持 `system`/`user`/`assistant` 角色及多模态内容。 | DashScope / Responses |
| `workspace` | string | 否 | 子业务空间 ID，仅当应用位于子空间或特定地域（如法兰克福）时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递。 | DashScope & Responses |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。推荐设为 `true` 以降低超时风险。Responses API 中 `background=true` 时不可用。 | DashScope & Responses |
| `incremental_output` | boolean | 否 | 仅流式模式下有效，控制是否增量输出（`true`）或全量追加（`false`）。 | DashScope |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息，结构详见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。 | DashScope & Responses |
| `rag_options` | object | 否 | 检索知识库配置，含 `pipeline_ids`（必填）、`file_ids`、`metadata_filter` 等，**仅智能体应用支持**。 | DashScope |

## 使用方式

- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  推荐用于需要完整功能（如 `flow_stream_mode` 工作流推流、`memory_id` [长期记忆](../concepts/memory.md)）的场景。SDK 调用简洁，HTTP 调用需注意参数嵌套层级（`prompt` 在 `input` 内，`workspace` 在 Header）。

- **OpenAI 兼容 Responses API**  
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - 异步：同上 endpoint，请求体中 `background=true`  
  适用于复用现有 OpenAI 生态代码的场景，`input` 字段直接接受消息数组，语义更直观。但异步模式不支持流式，且部分高级功能（如 `flow_stream_mode`）不可用。

- **调试与 SDK**  
  控制台提供“应用卡片 → 发布 → API 调试”在线调试入口。各语言 SDK（Python/Java/Node.js 等）均提供封装方法（如 `Application.call()` 或 `client.responses.create()`），详情见对应 SDK 文档。

## 限制和注意事项

- **地域与 Workspace 依赖**：调用子业务空间应用或非北京地域模型（如法兰克福）时，`workspace` 为必需参数，且影响 Base URL 构成。务必通过 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指引正确获取。
- **会话与状态管理**：`session_id` 有效期为 1 小时无请求，超时后失效；`messages` 参数可替代 `session_id` 实现完全可控的上下文管理，但需客户端自行维护历史。
- **版本与兼容性**：不同 SDK 版本对参数支持有差异（如 `flow_stream_mode` 要求 Java SDK ≥2.22.23），请严格按文档要求升级。`model_id` 参数可覆盖控制台配置，但仅在新版智能体 API 中明确支持。
- **异步限制**：Responses API 的异步调用不支持 `stream=true`，且需自行实现轮询逻辑；DashScope API 当前未提供原生异步接口，需结合 `background` 模式或业务层重试机制实现。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)


