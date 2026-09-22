# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持多种调用协议（DashScope 原生 API 与 OpenAI 兼容 Responses API），并提供[流式输出](../concepts/streaming-output.md)、多模态输入、[长期记忆](../concepts/memory.md)、RAG 检索等关键功能，适用于构建生产级 AI 应用集成。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体及工作流三类应用，但不同 API 路径和参数集存在差异。
- **多模态能力**：通过 `image_list`（DashScope API）或 `input_image`（Responses API）支持图像理解；通过 `file_list` 或 `input_file` 支持文档、音视频文件问答（仅智能体应用）[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **RAG 检索**：智能体应用可通过 `rag_options` 参数指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据（`metadata_filter`）或标签（`tags`）进行精准检索 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
- **[长期记忆](../concepts/memory.md)**：仅智能体应用支持 `memory_id` 参数，启用后系统自动构建、保存并恢复用户偏好记忆。
- **思考过程输出**：通过 `enable_thinking=true` + `has_thoughts=true` 组合可获取模型思考链（Thoughts），但需注意该功能在部分模型上存在极小概率不输出思考过程 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

> **注意**：`flow_stream_mode`（如 `message_format_plus`）仅对工作流应用生效，且要求在控制台对应节点开启“[流式输出](../concepts/streaming-output.md)”开关；而 `incremental_output` 是 DashScope API 级别的通用流式控制参数，二者作用域不同，不可混用。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | ✓ | 应用唯一标识，从控制台应用卡片复制获取 | 全部 |
| `prompt` | string | ✓（DashScope 单轮） | 用户指令文本，仅用于单轮对话 | DashScope |
| `messages` | array | ✓（DashScope 多轮） | 包含 `system`/`user`/`assistant` 角色的消息数组，替代 `prompt` 和 `session_id` | DashScope |
| `input` | string/array | ✓（Responses） | 支持纯文本字符串或 OpenAI 格式消息数组（含 `input_text`/`input_image`/`input_file`） | Responses |
| `session_id` | string | ✗ | 对话历史标识，1 小时无请求自动失效；若同时传 `messages` 则被忽略 | DashScope |
| `workspace` | string | ✗ | 子业务空间 ID，仅当应用部署于子空间或特定地域（如法兰克福、东京）时必需，通过 Header `X-DashScope-WorkSpace` 传递 | 全部 |
| `stream` | boolean | ✗ | 是否启用[流式输出](../concepts/streaming-output.md)（`true` 推荐）。Responses API 中 `background=true` 时禁用流式 | 全部 |
| `incremental_output` | boolean | ✗ | 仅 DashScope 流式模式下有效，控制是否增量返回（`true`）或全量追加（`false`） | DashScope |
| `flow_stream_mode` | string | ✗ | 仅工作流应用有效，取值 `message_format_plus`（推荐）、`message_format` 或 `full_thoughts`（不推荐） | DashScope |
| `biz_params` | object | ✗ | 传递自定义变量、插件参数或用户鉴权信息（`user_defined_params`, `user_defined_tokens`） | DashScope / Responses（via `extra_body`） |
| `rag_options` | object | ✗ | 仅智能体应用支持，用于配置知识库检索范围与过滤条件 | DashScope |

## 使用方式

### 1. 凭证准备
- 获取 `APP_ID` 和（如需）`Workspace ID`：必须通过[控制台手动操作](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)，API/CLI 不支持查询。
- 获取 `DASHSCOPE_API_KEY`：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建，并建议配置为环境变量 `DASHSCOPE_API_KEY`。

### 2. API 选择与端点
- **DashScope 原生 API**（推荐用于高性能/全功能场景）：
  - Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - 文档入口：[DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- **OpenAI 兼容 Responses API**（推荐用于快速迁移/复用现有代码）：
  - 同步 Endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步 Endpoint：同上，但请求体中设 `"background": true`
  - 文档入口：[Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)

### 3. 调用示例（核心逻辑）
- **单轮文本（DashScope Python SDK）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```
- **多轮+图像（Responses Python SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
  )
  response = client.responses.create(
      input=[
          {"role": "user", "content": [
              {"type": "input_text", "text": "这是什么？"},
              {"type": "input_image", "image_url": "https://example.com/image.jpg"}
          ]}
      ]
  )
  ```

## 限制和注意事项

- **地域限制**：所有文档均明确标注“仅适用于华北2（北京）地域”，其他地域（如德国法兰克福、新加坡）调用需额外确认 Workspace ID 是否已正确嵌入 Base URL [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本强依赖**：多个参数（如 `image_list`, `rag_options`, `flow_stream_mode`）要求特定最低 SDK 版本（如 Java ≥2.22.23, Python ≥1.24.0），低版本将导致参数被忽略或报错。
- **异步模式约束**：Responses API 的 `background=true` 与 `stream=true` 互斥，异步任务不支持流式输出；且异步任务需主动轮询 `retrieve` 接口获取结果。
- **参数冲突规则**：当 `messages` 与 `prompt`/`session_id` 同时存在时，DashScope API 优先使用 `messages`；当 `biz_params` 中的插件参数与应用内配置不一致时，调用将失败而非静默忽略。
- **[长期记忆](../concepts/memory.md)与会话隔离**：`memory_id` 仅在智能体应用中生效，且同一 `memory_id` 下的多次调用共享记忆状态；`session_id` 则仅维护单次会话上下文，两者不可混用。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


