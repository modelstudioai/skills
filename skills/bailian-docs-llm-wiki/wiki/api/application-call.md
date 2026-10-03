# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容模式），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用，但不同 API 路径和参数支持范围存在差异。新版智能体应用需使用 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)，而工作流与旧版智能体统一由 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 覆盖。
- **多模态能力**：支持图像（URL 或 Data URL Base64 编码）和文件（URL）输入，要求应用内选用通义千问 VL 系列模型（视觉理解）或配置对应文件处理方式（如“全文引用”）。
- **RAG 检索**：仅智能体应用支持 `rag_options` 参数，可指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据过滤（`metadata_filter`）及标签（`tags`）等。
- **[长期记忆](../concepts/memory.md)**：仅智能体应用支持 `memory_id` 参数，用于启用用户级[长期记忆](../concepts/memory.md)体。
- **OpenAI 兼容模式**：通过 Responses API（同步/异步）复用 OpenAI SDK 生态，路径为 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`，详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：新版智能体应用 API 与工作流/旧版智能体 API 在 `messages` 字段支持上存在不一致——前者未定义 `messages` 参数（仅支持 `prompt` + `session_id`），后者明确支持 `messages` 数组实现多轮对话且优先级高于 `session_id`。开发者需根据所选应用类型严格匹配对应文档。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属 API |
|--------|------|----------|------|-----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取。HTTP 调用时需填入 URL 路径；SDK 调用时作为参数传入。 | 全部 |
| `prompt` | string | 是（DashScope API） | 单轮文本输入指令。仅 DashScope API 使用；Responses API 中由 `input` 字段替代。 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)、[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `input` | string/array | 是（Responses API） | Responses API 的核心输入字段：支持字符串（单轮）或消息数组（多轮/多模态）。消息结构含 `role`（system/user/assistant）与 `content`（支持 `input_text`/`input_image`/`input_file`）。 | [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) |
| `session_id` | string | 否 | 用于恢复云端存储的对话历史（仅 DashScope API）。1 小时无请求自动失效。 | 全部 DashScope API |
| `messages` | array | 否（仅旧版/工作流） | 多轮对话上下文数组，格式为 `[{"role":"user","content":"..."}, ...]`。若与 `session_id` 同时传入，以 `messages` 为准。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)（默认 `false`）。DashScope API 需在 Header 中设 `X-DashScope-SSE: enable`；Responses API 直接设 `stream=true`。 | 全部 |
| `workspace` | string | 否 | 子业务空间 ID，仅当应用部署于子空间或特定地域（如德国法兰克福、新加坡等）时必需。通过 Header `X-DashScope-WorkSpace` 传递（DashScope API）或 `extra_body`（Responses API）。 | 全部 |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息（`user_defined_params`, `user_defined_tokens`）。Responses API 中需通过 `extra_body` 包裹。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)、[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) |
| `rag_options` | object | 否（仅智能体） | RAG 检索配置对象，含 `pipeline_ids`（必选）、`file_ids`、`metadata_filter` 等。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |

## 使用方式

### 1. 凭证准备
- 获取 `APP ID` 和（如需）`Workspace ID`：通过 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指引，在控制台应用管理页或业务空间管理页手动复制。**注意：目前不支持 API 或 CLI 查询**。
- 获取 `DASHSCOPE_API_KEY`：通过密钥管理页面创建并配置至环境变量（推荐），避免硬编码。

### 2. 调用入口
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：
  - 终端：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK：Python/Java SDK 的 `Application.call()` 方法（新版智能体）或通用 `Application` 类（旧版/工作流）。
- **OpenAI 兼容模式**（推荐用于快速迁移/生态复用）：
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步：同上 endpoint，但请求体中 `background=true`，后续通过 `GET /responses/{task_id}` 查询结果。

### 3. 代码示例（核心逻辑）
- **DashScope 单轮调用（Python）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```
- **Responses 同步多轮（Python）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
  )
  response = client.responses.create(
      input=[{"role":"user","content":"你好"}]
  )
  ```
- **Responses 异步任务（Python）**：
  ```python
  response = await client.responses.create(
      input="生成报告",
      background=True
  )
  task_id = response.id
  # 后续轮询 retrieve(task_id)
  ```

## 限制和注意事项

- **地域限制**：所有文档均明确标注“仅适用于华北2（北京）地域”。其他地域（如德国法兰克福、新加坡）调用时，必须显式传入 `Workspace ID`，且其值是 Base URL 的组成部分（见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。
- **SDK 版本强依赖**：关键功能需满足最低 SDK 版本，例如：
  - `incremental_output`：Python SDK ≥ 1.24.7，Java SDK ≥ 2.21.13；
  - `flow_stream_mode`：Java SDK ≥ 2.22.23；
  - `enable_thinking`：Java SDK ≥ 2.20.0。
  低版本 SDK 可能导致参数被忽略或报错。
- **异步与流式的互斥性**：`background=true` 与 `stream=true` **不可同时设置**（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)），否则请求将被拒绝。
- **参数作用域隔离**：`rag_options`、`memory_id`、`file_list` 等参数**仅对智能体应用生效**；工作流应用需通过 `biz_params` 传递节点级参数，且必须在控制台发布前完成插件/变量配置。
- **会话状态管理**：DashScope API 的 `session_id` 机制与 Responses API 的 `messages` 数组机制**不互通**。若需跨请求维护上下文，应统一选择一种模式并自行管理完整历史（尤其是 Responses API 明确说明“基于 `pre_response_id` 的上下文功能将在后续支持”，当前需全量传递）。

## 来源文档

- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


