# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：通过 `image_list`（DashScope API）或 `input_image`（Responses API）支持图像理解；通过 `file_list` 或 `input_file` 支持文档、音视频文件问答（仅智能体应用）[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
- **[长期记忆](../concepts/memory.md)**：智能体应用可通过 `memory_id` 参数启用[长期记忆](../concepts/memory.md)，自动构建、保存并恢复用户偏好信息 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **RAG 检索**：智能体应用支持通过 `rag_options` 配置知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）等多维度检索 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **思考模式**：深度思考模型支持 `enable_thinking` + `has_thoughts` 组合开启思考过程输出，`thought` 字段返回推理链，`text` 字段返回最终答案 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。

> **注意**：新版智能体应用 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体应用 API 同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项。这表明实际地域支持范围可能已扩展，但官方 API 文档尚未同步更新，开发者应以控制台可用地域和 Base URL 实际配置为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本输入指令。 | DashScope API |
| `input` | string/array | 是（Responses） | 支持字符串（单轮）或消息数组（多轮/多模态）。`content` 数组内可嵌套 `input_text`/`input_image`/`input_file`。 | Responses API |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求后失效。与 `messages` 冲突时，后者优先。 | DashScope API |
| `messages` | array | 否（DashScope） | 多轮对话上下文，含 `system`/`user`/`assistant` 角色消息。 | DashScope API |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)。DashScope 需 Header `X-DashScope-SSE: enable`；Responses 直接传 `stream=true`。 | 全部 |
| `workspace` | string | 否 | 子业务空间 ID，调用子空间应用或特定地域模型时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | DashScope API |
| `biz_params` | object | 否 | 传递自定义变量、插件参数（`user_defined_params`）、用户鉴权（`user_defined_tokens`）等。 | DashScope API & Responses API（via `extra_body`） |

## 使用方式

### 1. 协议选择
- **DashScope 原生 API**：功能最全，推荐用于新项目。Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `/api/v2/apps/...`（异步，部分场景）。
- **OpenAI 兼容 Responses API**：便于迁移现有 OpenAI 代码。同步 Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`；异步需设置 `background=true` [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 2. 认证与凭证
- **API Key**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并配置为环境变量 `DASHSCOPE_API_KEY`。
- **APP ID & Workspace ID**：必须通过控制台手动获取，不支持 API 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

### 3. SDK 与 HTTP 示例
- **SDK**：Python/Java DashScope SDK 或 OpenAI Python SDK（需指定 `base_url`）。版本要求严格，如新版智能体 API 要求 Java SDK ≥ 2.20.0。
- **HTTP**：`Authorization: Bearer ${DASHSCOPE_API_KEY}` + `Content-Type: application/json`。流式请求需额外添加 `X-DashScope-SSE: enable`（DashScope）或 `stream=true`（Responses）。

## 限制和注意事项

- **地域限制**：所有当前公开的 API 文档均标注“仅适用于华北2（北京）地域”，但实际业务空间（Workspace）机制覆盖多地域，调用前务必确认所用 `Base URL` 与目标地域匹配。
- **参数冲突**：`session_id` 与 `messages` 同时存在时，`messages` 优先生效；`prompt` 与 `messages` 同时存在时，`messages` 优先生效。
- **异步限制**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true` 会被忽略）[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **版本兼容性**：`incremental_output`（DashScope）与 `stream`（Responses）语义不同：前者控制 chunk 内容是否增量（delta），后者控制是否启用 SSE 流；两者可同时启用以获得最佳体验。
- **安全实践**：禁止在代码中硬编码 `DASHSCOPE_API_KEY`，务必使用环境变量或密钥管理服务。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)


