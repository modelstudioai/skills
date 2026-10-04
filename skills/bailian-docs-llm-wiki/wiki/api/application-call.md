# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过标准化 API 接口调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入、配置上下文与输出行为，即可获得结构化响应。该能力同时支持 DashScope 原生协议与 OpenAI 兼容模式，兼顾功能完整性与生态迁移便利性。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）及工作流（Workflow）三类应用，对应不同 API 路径与参数集。  
- **模型能力**：底层可调用通义千问系列（Qwen）、深度思考模型（Deep Thinking）、千问 VL 等多模态模型；具体可用模型由应用创建时选定，API 调用时可通过 `model_id` 参数覆盖（[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。  
- **多模态输入**：支持图像（`image_list` 或 `input_image`）、文件（`file_list` 或 `input_file`）输入，需在应用中启用对应模型与处理方式（如 VL 模型、全文引用/切片检索）；相关说明见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。  
- **[长期记忆](../concepts/memory.md)与 RAG**：智能体应用支持 `memory_id`（[长期记忆](../concepts/memory.md)）和 `rag_options`（知识库/文档检索）参数，实现个性化与知识增强（[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项——这表明实际服务已支持多地域，文档地域限制描述存在滞后，应以控制台实际可用地域为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | ✓ | 应用唯一标识，从控制台应用卡片复制获取（[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。HTTP 调用时需嵌入 URL 路径。 | DashScope / OpenAI |
| `prompt` 或 `input` | string / array | ✓ | 单轮文本输入（`prompt`）或完整对话历史/多模态内容（`input` 数组）。OpenAI 模式下 `input` 支持 `messages` 格式及 `content` 内嵌 `input_text`/`input_image`/`input_file`。 | DashScope (`prompt`) / OpenAI (`input`) |
| `session_id` | string | ✗ | 对话会话标识，用于恢复云端历史。1 小时无请求自动失效。与 `messages` 同时存在时，`messages` 优先（[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。 | DashScope |
| `workspace` | string | ✗ | 子业务空间 ID，仅当应用位于子空间或调用特定地域模型时必需；HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递（[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。 | DashScope |
| `stream` | boolean | ✗ | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。DashScope 需 Header `X-DashScope-SSE: enable`；OpenAI 模式直接设 `stream=true`（[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)）。 | DashScope / OpenAI |
| `background` | boolean | ✗ | OpenAI 模式专属，设为 `true` 启动异步任务，立即返回 `task_id`（[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。 | OpenAI |
| `biz_params` | object | ✗ | 传递自定义变量、插件参数等，结构为 `{ "user_prompt_params": {}, "user_defined_params": {} }`（[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。 | DashScope / OpenAI（需 `extra_body`） |

## 使用方式

- **DashScope 原生协议**：  
  - HTTP Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（新版/旧版智能体、工作流统一路径）。  
  - SDK 调用：Python/Java SDK 提供 `Application.call()` 方法，自动处理 endpoint 与鉴权（[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。  

- **OpenAI 兼容模式（Responses API）**：  
  - 同步调用 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。  
  - 异步调用：在请求体中添加 `"background": true`，后续通过 `GET /responses/{task_id}` 查询结果（[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。  
  - SDK：使用标准 `openai` 客户端，配置 `base_url` 指向百炼兼容 endpoint 即可复用现有代码（[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)）。  

- **调试与验证**：所有应用均支持控制台内 **应用卡片 → 发布 → API 调试** 实时测试，无需编码即可验证参数与响应。

## 限制和注意事项

- **地域与权限**：`Workspace ID` 仅在子业务空间或特定地域（如法兰克福、新加坡）调用时必需；主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号才能查询全部 Workspace ID（[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。  
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 需 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`enable_thinking` 需 Java SDK ≥2.20.0（[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。  
- **异步与流式互斥**：OpenAI 模式下 `background=true` 与 `stream=true` 不可同时设置，异步任务不支持[流式输出](../concepts/streaming-output.md)（[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。  
- **参数冲突规则**：当 `messages` 与 `session_id`/`prompt` 同时传入时，`messages` 优先生效；`biz_params` 中的 `user_prompt_params` 与 `user_defined_params` 需与应用内配置的变量名、插件 ID 严格一致，否则被忽略（[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


