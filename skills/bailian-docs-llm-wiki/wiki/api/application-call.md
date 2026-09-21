# application call

`application call` 是指通过 API 调用阿里云百炼平台已发布的智能体（Agent）或工作流（Workflow）应用。该能力支持同步、异步及流式响应等多种调用模式，允许开发者将百炼应用无缝集成至自有系统，复用其编排逻辑、RAG、插件调用与多模态理解等能力。调用需提供 APP ID、API Key，并根据应用部署位置决定是否携带 Workspace ID。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 和 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态输入**：支持图像（URL 或 Data URL Base64）、音频、视频及文档（PDF/DOCX/TXT 等）输入，需在应用中启用对应模型（如 Qwen-VL）并正确配置文件处理方式（全文引用/切片检索/自定义处理）。
- **[长期记忆](../concepts/memory.md)与上下文管理**：智能体应用支持 `memory_id` 参数实现用户级[长期记忆](../concepts/memory.md)；工作流与智能体均支持 `session_id`（单轮历史）或完整 `messages` 数组（多轮对话）传递上下文。
- **OpenAI 兼容模式**：通过 Responses API 提供 `/v1/responses` 接口，兼容 OpenAI SDK 的 `input`、`stream`、`background` 等参数语义，便于迁移现有代码，参见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API、Responses API 同样标注“仅适用于华北2（北京）地域”。但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出，Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等地域下为必需字段，且是 Base URL 的组成部分——这表明跨地域调用能力实际存在，但当前各 API 参考文档未同步更新地域支持说明，建议以控制台实际可用地域为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 来源 |
|--------|------|------|------|------|
| `app_id` | string | ✓ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需嵌入 URL 路径。 | [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `workspace` | string | ✗（条件必选） | 业务空间 ID，仅当应用位于子业务空间或调用特定地域模型时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传入。 | [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `prompt` / `input` | string 或 array | ✓ | 单轮文本输入（`prompt`）或结构化消息数组（`input`）。`messages` 数组支持 `system`/`user`/`assistant` 角色，含文本、图片（`input_image`）、文件（`input_file`）等多模态内容。 | [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md), [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) |
| `stream` | boolean | ✗ | 是否启用[流式输出](../concepts/streaming.md)。DashScope API 需设置 `X-DashScope-SSE: enable` Header；Responses API 直接设 `stream=true`。推荐开启以降低超时风险。 | [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) |
| `background` | boolean | ✗ | 仅 Responses API 支持。设为 `true` 即发起异步任务，立即返回 `task_id`，后续通过 `retrieve` 查询结果。异步模式不支持 `stream=true`。 | [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) |
| `biz_params` | object | ✗ | 传递自定义变量、插件参数或用户鉴权信息（`user_defined_params`, `user_defined_tokens`）。需在应用内预先配置并发布。 | [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) |
| `rag_options` | object | ✗ | 智能体专属。指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据过滤（`metadata_filter`）等 RAG 检索参数。 | [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) |

## 使用方式

- **DashScope API（推荐用于高性能/全功能场景）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  支持 Python/Java SDK（需 DashScope SDK ≥2.19.3）及标准 HTTP 调用。SDK 封装了 `Application.call()` 方法，HTTP 请求体需包含 `input`（含 `prompt` 或 `messages`）和 `parameters`（含 `stream`, `incremental_output` 等）。调试可直接使用控制台「应用卡片 → 发布 → API 调试」。

- **Responses API（推荐用于 OpenAI 生态迁移）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  完全兼容 OpenAI Python SDK（`openai>=1.0.0`），初始化 `OpenAI(base_url=...)` 后调用 `client.responses.create(input=..., stream=..., background=...)`。同步调用阻塞等待结果；异步调用需配合 `client.responses.retrieve(task_id)` 轮询状态。

- **SDK 版本要求**：  
  - DashScope SDK：Python ≥1.24.7，Java ≥2.21.13（文件/图像）、≥2.22.23（工作流流式）；  
  - OpenAI SDK：Python ≥1.0.0，Java（OpenAI Client）需匹配官方版本。

## 限制和注意事项

- **地域限制**：所有 documented API 均明确标注“仅适用于华北2（北京）地域”，但 Workspace ID 的跨地域要求暗示底层支持更广。生产环境请以控制台实际开通地域为准，避免硬编码地域 URL。
- **会话时效性**：`session_id` 在连续 1 小时无请求后自动失效；`memory_id` 依赖应用内[长期记忆](../concepts/memory.md)开关开启且已发布。
- **异步约束**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming.md)**，且需自行实现轮询逻辑（建议间隔 ≥2 秒）。
- **参数冲突**：当同时传入 `session_id` 和 `messages` 时，`messages` 优先级更高，`session_id` 和 `prompt` 将被忽略。
- **模型覆盖**：`model_id` 参数可在 API 调用时覆盖应用控制台配置的默认模型，但仅对支持该模型的应用生效；思考模式（`enable_thinking`）需配合 `has_thoughts=true` 才能获取 `thought` 字段。
- **权限要求**：获取 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


