# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数支持存在差异。
- **[多模态能力](../concepts/multi-modal.md)**：通过 `image_list`（DashScope API）或 `input_image`（Responses API）支持图像理解；通过 `file_list` 或 `input_file` 支持文档、音视频文件问答（仅智能体应用）[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **[长期记忆](../concepts/long-term-memory.md)**：智能体应用可通过 `memory_id` 参数启用[长期记忆](../concepts/long-term-memory.md)，自动构建、保存与恢复用户偏好信息 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **RAG 检索**：智能体应用支持通过 `rag_options` 配置知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）等多维度检索条件 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **思考模式**：对深度思考模型，可通过 `enable_thinking` + `has_thoughts` 组合开启并获取思考过程（`thought` 字段）。

> **注意**：新版智能体应用 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体应用 API 同样标注“仅适用于华北2（北京）地域”，但 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) 也重复声明相同地域限制。这表明当前所有 `application call` 功能在地域覆盖上存在统一约束，非北京地域用户需确认服务可用性。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在控制台应用卡片中获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | 是（单轮） | 用户指令文本。DashScope API 中为必选（单轮），Responses API 中可被 `input` 数组替代。 | DashScope API |
| `input` | string/array | 是（Responses） | Responses API 的核心输入：字符串（单轮）或消息数组（多轮/多模态）。`content` 数组支持 `input_text`/`input_image`/`input_file` 类型。 | Responses API |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求后失效。仅 DashScope API 支持。 | DashScope API |
| `messages` | array | 否（DashScope） | 多轮对话消息数组（system/user/assistant），优先级高于 `prompt` 和 `session_id`。 | DashScope API |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)。DashScope API 通过 Header `X-DashScope-SSE: enable` 控制；Responses API 直接传入请求体。 | 全部 |
| `incremental_output` | boolean | 否 | 仅 DashScope API 流式模式下有效，控制是否增量输出（delta）而非全量追加。 | DashScope API |
| `workspace` | string | 否 | 子业务空间 ID，调用子空间应用或特定地域（如法兰克福、东京）模型时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | DashScope API |
| `biz_params` | object | 否 | 传递自定义变量、插件参数等。结构包含 `user_prompt_params`、`user_defined_params` 等子字段。 | DashScope API & Responses API（via `extra_body`） |
| `memory_id` | string | 否 | 智能体应用长期记忆 ID，需应用内开启开关并发布。 | DashScope API |
| `rag_options` | object | 否 | 智能体应用 RAG 检索配置，含 `pipeline_ids`（必选）、`file_ids`、`metadata_filter` 等。 | DashScope API |
| `background` | boolean | 否（Responses） | Responses API 异步模式开关，设为 `true` 即返回任务 ID。**异步不支持 `stream=true`**。 | Responses API |

## 使用方式

- **DashScope 原生 API**  
  - **Endpoint**: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  - **认证**: Header `Authorization: Bearer {DASHSCOPE_API_KEY}`  
  - **SDK**: Python/Java SDK 提供 `Application.call()` 方法，推荐使用；流式需调用 `streamCall()`。  
  - **在线调试**: 控制台应用卡片 → 发布 → API 调试。

- **OpenAI 兼容 Responses API**  
  - **同步 Endpoint**: `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  - **异步 Endpoint**: 同上，但请求体中 `background=true`。  
  - **认证**: 同 DashScope，Header `Authorization: Bearer {DASHSCOPE_API_KEY}`  
  - **SDK**: 使用 OpenAI 官方 SDK（如 `openai==1.40.0+`），配置 `base_url` 为上述地址。  
  - **多模态**: `input` 中 `content` 数组按 `type` 区分文本/图像/文件，严格遵循 OpenAI 格式。

- **地域与 Workspace 适配**  
  `Workspace ID` 是调用子业务空间应用的必需凭证，且是德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等特定地域 Base URL 的组成部分 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。务必在控制台对应地域下操作，并正确设置 `X-DashScope-WorkSpace` Header。

## 限制和注意事项

- **地域限制**：所有 `application call` 文档均明确标注“仅适用于华北2（北京）地域”，跨地域调用将失败。其他地域（如法兰克福）虽在 Workspace 获取文档中提及，但其 API 兼容性未在调用文档中确认，需谨慎验证。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Java SDK ≥ 2.20.0，`flow_stream_mode` 要求 Java SDK ≥ 2.22.23，`file_list` 要求 Python SDK ≥ 1.24.7。低版本 SDK 可能静默忽略参数。
- **异步与流式互斥**：Responses API 明确规定 `background=true` 时**不支持 `stream=true`**，二者不可同时启用。
- **凭证获取方式**：APP ID 和 Workspace ID **仅支持通过控制台手动获取**，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **参数冲突规则**：DashScope API 中，若同时传入 `messages` 和 `session_id`，则 `messages` 优先，`session_id` 和 `prompt` 将被忽略；`model_id` 参数优先级高于控制台配置。
- **长期记忆与 RAG 限定**：`memory_id` 和 `rag_options` 仅对**智能体应用**生效，工作流应用调用时传入将被忽略。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


