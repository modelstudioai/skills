# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者可使用 DashScope 原生 API 或 OpenAI 兼容的 Responses API 发起请求，支持文本、图像、文件、多轮对话、插件调用、RAG 检索等多种能力。所有调用均需提供有效的 `APP ID` 和 `API Key`，部分场景还需 `Workspace ID`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数集存在差异。
- **模型能力**：
  - 文本生成：默认支持所有百炼托管大模型（如 Qwen 系列）；
  - 视觉理解：需在应用中选用 [图像与视频理解](raw/model-user-guide/model-experience/text-generation-model/vision.md) 模型，并传入 `image_list`（DashScope API）或 `input_image`（Responses API）；
  - 文件问答：仅智能体应用支持，需配置文件处理方式为“全文引用”或“切片检索”，并通过 `file_list`（DashScope）或 `input_file`（Responses）传入 URL；
  - 深度思考模式：通过 `enable_thinking` + `has_thoughts` 参数启用，适用于 [深度思考模型](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)，输出 `thought` 字段。
- **高级功能**：
  - RAG 检索：仅智能体应用支持，通过 `rag_options` 指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据过滤（`metadata_filter`）等；
  - [长期记忆](../concepts/long-term-memory.md)：仅智能体应用支持，通过 `memory_id` 关联已创建的记忆体；
  - 自定义插件与变量：通过 `biz_params` 传递用户提示词变量（`user_prompt_params`）、插件参数（`user_defined_params`）及用户级鉴权信息（`user_defined_tokens`）。

> **注意**：新版智能体 API 文档 [新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 文档 [工作流与旧版智能体应用 API](raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 也标注相同限制；但 Responses API 的两篇子文档（同步/异步）同样声明“仅适用于华北2（北京）地域”。这表明当前所有 `application call` 能力均未在其他地域 GA，开发者需确保应用部署于北京地域，否则调用将失败。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属 API |
|--------|------|----------|------|-----------|
| `app_id` | string | ✅ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)获取。HTTP 调用时需填入 URL 路径；SDK 调用时作为方法参数。 | 全部 |
| `prompt` | string | ✅（DashScope 单轮） | 用户单轮指令文本。DashScope API 中必须与 `input` 对象配合使用；Responses API 中被 `input` 替代。 | DashScope |
| `input` | string/array | ✅（Responses） | 核心输入：支持字符串（单轮）或消息数组（多轮/[多模态](../concepts/multi-modal.md)）。消息数组支持 `system`/`user`/`assistant` 角色及 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `session_id` | string | ❌（可选） | 对话历史标识，启用后自动加载云端会话上下文（1 小时失效）。**注意**：若同时传入 `messages`，则 `session_id` 和 `prompt` 将被忽略。 | DashScope |
| `messages` | array | ❌（可选） | 多轮对话上下文数组，替代 `prompt` + `session_id`。每个元素含 `role`（`system`/`user`/`assistant`）和 `content`。 | DashScope |
| `workspace` | string | ❌（条件必选） | 业务空间 ID，仅当应用位于[子业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)或调用德国/北京/新加坡/香港/东京地域模型时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递。详情见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 | 全部 |
| `stream` | boolean | ❌（可选） | 是否[流式输出](../concepts/streaming-output.md)。`true` 时返回 SSE 数据流，推荐用于降低超时风险。DashScope 需 Header `X-DashScope-SSE: enable`；Responses 直接置 `stream=true`。 | 全部 |
| `incremental_output` | boolean | ❌（仅 DashScope 流式） | [流式输出](../concepts/streaming-output.md)时是否增量返回（`true`）而非全量追加（`false`）。影响客户端拼接逻辑。 | DashScope |
| `flow_stream_mode` | string | ❌（仅工作流） | 工作流流式模式，取值 `message_format_plus`（推荐）、`message_format` 或 `full_thoughts`（不推荐新业务）。 | DashScope |
| `background` | boolean | ❌（仅 Responses 异步） | 设为 `true` 启用异步调用，立即返回任务 ID。**注意**：异步模式下 `stream` 不生效。 | Responses |

## 使用方式

### 1. 准备工作
- 在控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 创建并发布目标应用，获取 `APP ID`；
- 在 [密钥管理](https://bailian.console.aliyun.com/#/api-key) 获取 `DASHSCOPE_API_KEY`，并配置至环境变量（推荐）或代码中；
- 如需跨业务空间调用，按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 指南获取 `Workspace ID`。

### 2. API 选择
- **DashScope 原生 API**：功能最全，支持所有高级参数（如 `rag_options`, `memory_id`, `flow_stream_mode`），Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。适用于需要精细控制的场景。
- **Responses API（OpenAI 兼容）**：提供同步（`/responses`）与异步（`/responses?background=true`）两种模式，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。适合快速迁移 OpenAI 生态项目，但部分参数（如 `rag_options`）需通过 `extra_body` 透传。

### 3. 代码示例（核心逻辑）
- **DashScope 单轮文本调用（Python SDK）**：
  ```python
  from dashscope import Client
  client = Client(api_key=os.getenv("DASHSCOPE_API_KEY"))
  response = client.apps.completions.create(
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.text)
  ```
- **Responses 同步多轮调用（Python SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url=f"https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
  )
  response = client.responses.create(
      input=[{"role": "user", "content": "你好"}]
  )
  ```
- **Responses 异步调用（Python SDK）**：
  ```python
  response = await client.responses.create(
      input="生成一份报告",
      background=True  # 立即返回 task_id
  )
  # 后续通过 client.responses.retrieve(task_id) 轮询结果
  ```

## 限制和注意事项

- **地域限制**：所有 `application call` API 当前**仅支持华北2（北京）地域**，跨地域调用将失败。请确认应用、API Key 及 Workspace 均位于北京地域。
- **凭证获取**：`APP ID` 和 `Workspace ID` **仅支持通过控制台手动获取**，不提供 API 或 CLI 查询接口，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：
  - DashScope Python SDK ≥ 2.0.1（`file_list`, `messages`, `rag_options`）；
  - DashScope Java SDK ≥ 2.22.23（`flow_stream_mode`）；
  - Responses Python SDK 需兼容 OpenAI v1.x。
- **参数冲突与覆盖规则**：
  - 若 API 请求中 `parameters.model_id` 与应用控制台配置的模型不一致，以 API 参数为准；
  - 若同时传入 `messages` 和 `session_id`，`messages` 优先，`session_id` 被忽略；
  - `enable_thinking=true` 时，必须同时设置 `has_thoughts=true` 才能在响应中看到 `thought` 字段。
- **异步限制**：Responses 异步调用不支持 `stream=true`，且任务状态轮询需自行实现（无 Webhook）。
- **安全提醒**：生产环境严禁硬编码 `DASHSCOPE_API_KEY`，务必使用环境变量或密钥管理服务。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


