# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用。新版智能体 API 与旧版/工作流 API 在参数设计上存在差异，需按应用类型选用对应文档 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 或 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **多模态能力**：支持图像（`image_list` / `input_image`）和文件（`file_list` / `input_file`）输入，要求应用内配置对应视觉模型（如千问VL系列）或文件处理方式（如全文引用、切片检索）。
- **[长期记忆](../concepts/long-term-memory.md)**：仅智能体应用支持 `memory_id` 参数，用于启用用户级[长期记忆](../concepts/long-term-memory.md)；该功能需在应用中提前开启开关并发布 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **RAG 检索**：仅智能体应用支持 `rag_options` 参数，可指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）进行精准检索。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 文档同样标注“仅适用于华北2（北京）地域”，但 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) 也重复声明相同地域限制。所有主流调用路径均未提及对其他地域（如德国法兰克福、新加坡）的原生支持——这与文档1中“在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域下的模型时，API 请求中才必须包含 `Workspace ID`”的说明存在隐含矛盾：即这些地域的应用调用虽需 Workspace ID，但其基础 API 调用能力是否可用，原始文档未明确覆盖。开发者应以控制台实际可用性及最新 SDK 兼容性为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 适用场景 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取。HTTP 调用时需填入 URL 路径，SDK 调用时作为独立参数。 | 所有调用方式 |
| `prompt` | string | 是（单轮） | 用户指令文本。HTTP 调用时置于 `input.prompt`；SDK 中为独立字段。 | 新版智能体、旧版智能体（单轮） |
| `messages` | array | 是（多轮） | 多轮对话消息数组（含 `system`/`user`/`assistant` 角色）。若传入则忽略 `prompt` 和 `session_id`。 | 旧版智能体、工作流、Responses API |
| `session_id` | string | 否 | 对话历史标识符，有效期 1 小时。仅新版/旧版智能体支持，工作流不支持。 | 新版/旧版智能体（单轮+历史） |
| `workspace` | string | 否 | 业务空间 ID，调用子业务空间或特定地域（德、新、港、日）应用时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | 所有调用方式（条件必需） |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。流式需客户端逐块读取；HTTP 需设 Header `X-DashScope-SSE: enable`，Responses API 直接传 `stream=true`。 | 所有调用方式 |
| `incremental_output` | boolean | 否 | 仅流式下生效，控制输出为全量追加（`false`）或增量 delta（`true`，推荐）。 | 新版/旧版智能体 |
| `flow_stream_mode` | string | 否 | 工作流专属流式模式，取值 `message_format_plus`（推荐）、`message_format` 或 `full_thoughts`（不推荐新业务）。 | 工作流 |
| `biz_params` | object | 否 | 传递自定义变量、插件参数（`user_prompt_params`, `user_defined_params`, `user_defined_tokens`）。 | 旧版智能体、工作流、Responses API（通过 `extra_body`） |
| `memory_id` | string | 否 | 长期记忆体 ID，需应用内开启长期记忆开关。 | 仅智能体应用 |
| `rag_options` | object | 否 | RAG 检索配置，含 `pipeline_ids`（必选）、`file_ids`、`metadata_filter` 等。 | 仅智能体应用 |

## 使用方式

- **DashScope 原生 API**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（新版/旧版智能体、工作流）  
  或 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（Responses API）。  
  推荐使用官方 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python/Java），自动处理 endpoint 与鉴权；HTTP 调用需手动设置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` Header。

- **OpenAI 兼容 Responses API**  
  提供同步（`/responses`）与异步（`background=true`）两种模式，无缝复用 OpenAI 生态代码。  
  - 同步：适用于实时交互，响应时间敏感场景；  
  - 异步：适用于耗时任务（如报告生成、多步骤工具链），立即返回 `task_id`，后续通过 `GET /responses/{task_id}` 查询结果。  
  > **注意**：异步调用不支持 `stream=true`，且当前不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动恢复，每次请求需传完整 `messages`。

- **调试与验证**  
  控制台提供“应用卡片 → 发布 → API 调试”一站式在线调试入口，支持参数填写与实时响应查看，是开发初期首选验证方式。

## 限制和注意事项

- **地域与权限限制**：所有 API 文档均声明“仅适用于华北2（北京）地域”。跨地域调用（如法兰克福、新加坡）必须显式传入 `Workspace ID`，且需确认该地域服务已开通；业务空间管理操作（如查询所有 Workspace ID）仅主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号可执行 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `enable_thinking` 要求 Java SDK ≥ 2.20.0，`flow_stream_mode` 要求 Java SDK ≥ 2.22.23，`file_list` 要求 Python SDK ≥ 1.24.7 / Java SDK ≥ 2.21.13。低版本 SDK 可能导致参数被忽略或报错。
- **参数冲突与覆盖规则**：  
  - `model_id` 参数优先级高于控制台配置；  
  - `messages` 与 `session_id`/`prompt` 同时存在时，`messages` 优先生效；  
  - `workspace` 仅在子业务空间或特定地域下必需，缺失将导致 403 或 404 错误。
- **安全实践**：API Key 严禁硬编码，务必通过环境变量（如 `DASHSCOPE_API_KEY`）注入；生产环境应结合 RAM 策略最小化授权范围。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


