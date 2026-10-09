# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 和 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等高级功能，适用于构建生产级 AI 应用。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数支持存在差异。
- **多模态能力**：通过 `image_list`（DashScope API）或 `input_image`（Responses API）支持图像理解；通过 `file_list` 或 `input_file` 支持文档、音视频文件问答（仅智能体应用）[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **[长期记忆](../concepts/memory.md)**：智能体应用可通过 `memory_id` 参数启用[长期记忆](../concepts/memory.md)，自动构建、保存并恢复用户偏好信息 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **RAG 检索**：智能体应用支持通过 `rag_options` 配置知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）及标签（`tags`）等多维检索条件 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **思考模式**：对深度思考模型，可通过 `enable_thinking` + `has_thoughts` 组合开启并获取思考过程（`thought` 字段）。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 及 Responses API 同样标注“仅适用于华北2（北京）地域”。但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出，在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等地域调用时 *必须* 提供 `Workspace ID`，且该 ID 是 Base URL 的组成部分。这表明跨地域调用是支持的，但需显式指定 Workspace ID 并确保 endpoint 正确，原始文档中关于“仅北京”的限制描述存在矛盾或过时，实际应以 endpoint 和 Workspace ID 的地域匹配为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 适用 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | 是（单轮） | 用户指令文本。DashScope API 中为顶层字段；Responses API 中需放入 `input` 内容。 | DashScope API（新版/旧版） |
| `input` | string/array | 是（单轮/多轮） | Responses API 的核心输入字段，支持纯字符串或符合 OpenAI 格式的 `messages` 数组（含 `system`/`user`/`assistant` 角色）。 | Responses API |
| `session_id` | string | 否 | 对话会话 ID，用于携带云端历史。1 小时无请求后失效。 | DashScope API（新版/旧版） |
| `messages` | array | 否（多轮） | 替代 `prompt` 和 `session_id` 的多轮对话上下文数组，按顺序排列。 | DashScope API（旧版）、Responses API |
| `workspace` | string | 否（子空间/特定地域） | 业务空间 ID，调用子业务空间或非默认地域（如法兰克福、东京）应用时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | DashScope API（新版/旧版） |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope API 默认 `false`；Responses API 默认 `false`，设为 `true` 后需按 SSE 协议解析 chunk。 | 全部 |
| `incremental_output` | boolean | 否（流式下） | [流式输出](../concepts/streaming-output.md)时是否增量返回（`true`）而非全量追加（`false`）。仅 DashScope API 支持。 | DashScope API（新版/旧版） |
| `flow_stream_mode` | string | 否（工作流） | 工作流流式模式，推荐 `message_format_plus`（消息增强）或 `message_format`（消息），避免使用已废弃的 `full_thoughts`。 | DashScope API（旧版） |
| `biz_params` | object | 否 | 传递自定义变量、插件参数（`user_prompt_params`, `user_defined_params`）等。 | DashScope API（旧版）、Responses API（via `extra_body`） |
| `memory_id` | string | 否（智能体） | 长期记忆体 ID，需在应用内开启长期记忆开关并发布。 | DashScope API（旧版） |
| `rag_options` | object | 否（智能体） | RAG 检索配置对象，包含 `pipeline_ids`（必选）、`file_ids`、`metadata_filter` 等。 | DashScope API（旧版） |
| `background` | boolean | 否（Responses） | Responses API 专用，设为 `true` 即发起异步任务，立即返回 `task_id`。 | Responses API |

## 使用方式

### 1. 准备工作
- 在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 创建并发布目标应用，获取 `APP ID`。
- 在 [密钥管理](https://bailian.console.aliyun.com/#/api-key) 获取 `DASHSCOPE_API_KEY`，并配置到环境变量 `DASHSCOPE_API_KEY`。
- 如需调用子业务空间或特定地域应用，按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指引获取 `Workspace ID`。

### 2. 选择 API 协议
- **DashScope 原生 API**：功能最全，支持所有高级参数（如 `flow_stream_mode`, `rag_options`, `memory_id`），Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。推荐用于新项目或需要深度集成的场景。
- **OpenAI 兼容 Responses API**：简化集成，复用 OpenAI SDK 和生态工具，Endpoint 为 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。同步调用适合实时交互；异步调用（`background=true`）适合长耗时任务 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

### 3. 发起调用（示例）
- **DashScope HTTP 同步**：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -H "X-DashScope-WorkSpace: YOUR_WORKSPACE_ID" \
    -d '{
          "input": {"prompt": "你是谁？"},
          "parameters": {"stream": true}
        }'
  ```
- **Responses API Python 异步**：
  ```python
  from openai import AsyncOpenAI
  client = AsyncOpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/APP_ID/compatible-mode/v1/"
  )
  # 创建任务
  create_resp = await client.responses.create(input="规划北京三日游", background=True)
  task_id = create_resp.id
  # 轮询结果
  retrieve_resp = await client.responses.retrieve(task_id)
  ```

## 限制和注意事项

- **地域与 Workspace ID**：调用位于子业务空间或德国（法兰克福）、新加坡、中国香港、日本（东京）等非默认地域的应用时，`Workspace ID` 为必传项，且必须与 endpoint 地域匹配 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：不同参数依赖特定 SDK 版本。例如，`incremental_output` 要求 Java SDK ≥ 2.20.0；`flow_stream_mode` 要求 Java SDK ≥ 2.22.23；`file_list` 要求 Python SDK ≥ 1.24.7 / Java SDK ≥ 2.21.13。务必检查并升级 SDK。
- **参数互斥性**：`prompt` 与 `messages` 不可同时传入；若同时传入 `session_id` 和 `messages`，系统将优先使用 `messages`。
- **异步限制**：Responses API 的异步调用不支持 `stream=true`，且 `background=true` 时 `stream` 参数会被忽略。
- **凭证获取**：`APP ID` 和 `Workspace ID` 目前仅支持通过控制台手动获取，不支持 API 或 CLI 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **模型覆盖**：`model_id` 参数可用于运行时覆盖应用内配置的模型，但其优先级高于控制台设置，需谨慎使用。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


