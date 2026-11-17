# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入（如 [prompt](../guides/prompt.md)、文件、图像等），即可获得应用封装后的结构化输出。该能力同时支持 DashScope 原生协议与 OpenAI 兼容模式（Responses API），适配不同技术栈的集成需求。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)明确注明“仅适用于华北2（北京）地域”，而[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)同样标注相同地域限制。
- **多模态能力**：支持图像理解（需选用通义千问VL系列模型）和文件问答（仅智能体应用），通过 `image_list`（DashScope）或 `input_image`/`input_file`（Responses）参数传入。
- **[长期记忆](../concepts/long-term-memory.md)**：智能体应用可启用[长期记忆](../concepts/long-term-memory.md)，通过 `memory_id` 参数指定记忆体 ID，实现跨会话的用户偏好延续。
- **RAG 检索**：智能体应用支持精细化知识库检索，可通过 `rag_options` 配置 `pipeline_ids`、`metadata_filter` 等参数，实现按知识库、文档、元数据或标签筛选。

> **注意**：文档 5 和文档 3 均声明“仅适用于华北2（北京）地域”，但[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)中明确指出，在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等地域调用子业务空间下的应用时，`Workspace ID` 是 Base URL 的组成部分。这表明跨地域调用是支持的，但具体 API 接口的地域可用性需以各接口文档为准，开发者应优先查阅对应 API 文档的地域说明。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台[应用管理](https://bailian.console.aliyun.com/#/app-center)获取 | DashScope & Responses |
| `prompt` / `input` | string/array | 是 | 用户指令或完整对话历史。`prompt` 用于单轮；`input` 在 Responses 中支持字符串或 messages 数组 | DashScope (`prompt`) / Responses (`input`) |
| `session_id` | string | 否 | 对话会话标识，用于恢复云端存储的历史上下文（1 小时内有效） | DashScope |
| `messages` | array | 否 | 多轮对话消息数组，含 `system`/`user`/`assistant` 角色，替代 `prompt` 和 `session_id` | DashScope & Responses |
| `workspace` / `X-DashScope-WorkSpace` | string | 否 | 子业务空间 ID，仅在调用子业务空间应用时必需 | DashScope（Header） |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)，默认 `false`。**注意：异步调用不支持流式** | DashScope & Responses |
| `incremental_output` | boolean | 否 | 流式模式下是否增量输出（推荐 `true`），避免重复内容拼接 | DashScope |
| `flow_stream_mode` | string | 否 | 工作流专属流式模式，`message_format_plus`（推荐）或 `message_format` | DashScope |
| `biz_params` | object | 否 | 传递自定义变量、插件参数等，结构因应用配置而异 | DashScope & Responses |

## 使用方式

### 协议选择
- **DashScope 原生协议**：功能最全，支持所有高级参数（如 `flow_stream_mode`, `has_thoughts`, `rag_options`）。Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。
- **OpenAI 兼容模式（Responses API）**：便于复用现有 OpenAI 生态代码。分为同步（`/responses`）与异步（`/responses?background=true`）两种调用路径，Endpoint 均为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。

### 调用示例（核心流程）
1. **前置准备**：在控制台创建应用、获取 `APP ID` 和 `DASHSCOPE_API_KEY`，并确保应用已发布。
2. **凭证传递**：
   - DashScope：`Authorization: Bearer ${API_KEY}` + URL 中嵌入 `APP_ID` + （子空间）Header `X-DashScope-WorkSpace: ${WORKSPACE_ID}`。
   - Responses：`Authorization: Bearer ${API_KEY}` + URL 中嵌入 `APP_ID`。
3. **构造请求体**：
   - 单轮文本：`{"input": "你是谁？"}`（Responses）或 `{"input": {"prompt": "你是谁？"}}`（DashScope）。
   - 多轮/多模态：按 `messages` 格式组织，包含 `input_text`/`input_image`/`input_file` 等子类型。
4. **处理响应**：解析 `output.text`（普通）或逐块读取 SSE 流（流式），异步调用需轮询 `retrieve` 接口。

## 限制和注意事项

- **地域限制**：DashScope v1 的 `apps/completion` 接口（文档 3 和 5）明确限定于华北2（北京）地域；Responses API（文档 4、6、7）虽未在标题中强调，但其子文档均标注“仅适用于华北2（北京）地域”，故默认遵循同一限制。
- **异步约束**：异步调用（`background=true`）**不支持[流式输出](../concepts/streaming-output.md)**（`stream=true`），且任务状态需主动轮询查询 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **参数冲突**：当 `messages` 与 `session_id` 同时存在时，DashScope API 会**优先使用 `messages` 内容，忽略 `session_id`**（见文档 5）。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Java SDK ≥ 2.20.0（文档 3），`flow_stream_mode` 要求 Java SDK ≥ 2.22.23（文档 5），使用前务必核对版本兼容性。
- **权限与凭证**：`Workspace ID` 仅主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号可查询，普通子账号无法访问业务空间管理页面 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


