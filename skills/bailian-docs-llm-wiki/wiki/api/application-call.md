# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 方式调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持同步与异步两种执行模式，并兼容 DashScope 原生协议和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，便于开发者快速集成到现有系统中。所有调用均需提供有效的 `APP ID` 和 `API Key`，部分场景还需指定 `Workspace ID`。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体、工作流三类应用，但不同 API 路径和参数集存在差异。
- **模型能力**：
  - 文本生成：默认使用应用配置的 LLM（如 Qwen-Plus），可通过 `model_id` 参数覆盖（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）；
  - 多模态理解：支持图像（VL 系列模型）和文件（PDF/DOCX/MP3 等）输入，需在应用内启用对应模型及处理方式（如“自定义处理”或“全文引用”）；
  - 深度思考模式：通过 `enable_thinking` 和 `has_thoughts` 参数控制是否返回思考过程（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）；
  - RAG 检索：智能体应用支持通过 `rag_options` 指定知识库（`pipeline_ids`）和文档（`file_ids`）进行精准检索（见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。
- **交互模式**：
  - 同步调用：适用于低延迟场景，直接返回完整结果；
  - 异步调用：适用于耗时任务（如多步骤工具链、长文档分析），返回 `task_id` 后轮询获取结果（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）；
  - [流式输出](../concepts/streaming-output.md)：支持 `stream=true` 实时响应，工作流应用需额外配置 `flow_stream_mode`（如 `message_format_plus`）以正确解析节点级增量数据（见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）。

> **注意**：新版智能体 API（[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API（[工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）和 Responses API（[Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)）同样标注“仅适用于华北2（北京）地域”，但文档 1 中指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项，且 Base URL 与地域强绑定。这表明实际地域支持范围可能超出文档声明，建议以控制台可用地域和实际请求 Base URL 为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在控制台应用卡片中获取；HTTP 调用时需嵌入 URL 路径（如 `/apps/{APP_ID}/completion`） | 全部 |
| `prompt` | string | 是（DashScope） | 单轮文本输入指令；若使用 `messages` 则此项忽略 | DashScope |
| `input` | string/array | 是（Responses） | 支持字符串（单轮）或消息数组（多轮/多模态）；`content` 数组可含 `input_text`/`input_image`/`input_file` | Responses |
| `session_id` | string | 否 | 对话历史标识，1 小时无请求自动失效；与 `messages` 冲突时优先使用 `messages` | DashScope |
| `messages` | array | 否（DashScope） | 多轮对话上下文，含 `system`/`user`/`assistant` 角色；`content` 支持文本、图片 URL、文件 URL | DashScope、Responses |
| `workspace` | string | 否 | 子业务空间 ID；HTTP 调用需通过 Header `X-DashScope-WorkSpace` 传递 | 全部 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)；Responses API 中 `background=true` 时不可设为 `true` | 全部 |
| `flow_stream_mode` | string | 否（仅工作流） | 工作流流式模式：`message_format_plus`（推荐）、`message_format`、`full_thoughts`（不推荐） | DashScope |
| `biz_params` | object | 否 | 传递自定义变量、插件参数（`user_defined_params`）或用户鉴权信息（`user_defined_tokens`） | DashScope、Responses（via `extra_body`） |
| `rag_options` | object | 否（仅智能体） | 控制知识库检索：`pipeline_ids`（必填）、`file_ids`、`metadata_filter` 等 | DashScope |

## 使用方式

### 1. 准备工作
- 获取凭证：通过控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 获取 `APP ID`；通过 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 获取并配置 `DASHSCOPE_API_KEY` 环境变量；子业务空间应用还需按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 指南获取 `Workspace ID`。
- 选择协议：
  - **DashScope 原生 API**：路径为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（同步）或 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`（Responses）；
  - **OpenAI 兼容 API**：需设置 `base_url = "https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/"`，调用 `client.responses.create()`。

### 2. 示例调用
- **DashScope 同步（Python SDK）**：
  ```python
  from dashscope import Application
  response = Application.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      app_id="YOUR_APP_ID",
      prompt="你是谁？"
  )
  print(response.output.text)
  ```
- **Responses 同步（OpenAI SDK）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/"
  )
  response = client.responses.create(input="你是谁？")
  print(response.output[0].content[0].text)
  ```
- **Responses 异步（Python SDK）**：
  ```python
  response = await client.responses.create(
      input="生成一份报告",
      background=True
  )
  task_id = response.id
  # 后续调用 client.responses.retrieve(task_id) 查询状态
  ```

## 限制和注意事项

- **地域限制**：所有文档均标注“仅适用于华北2（北京）地域”，但实际调用需匹配 `Workspace ID` 所属地域的 Base URL（如德国法兰克福需使用对应地域 endpoint），详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **SDK 版本要求**：
  - `incremental_output` 参数：Python SDK ≥ 1.24.7，Java SDK ≥ 2.21.13；
  - `flow_stream_mode`：Python SDK ≥ 1.24.0，Java SDK ≥ 2.22.23；
  - `enable_thinking`：Java SDK ≥ 2.20.0（见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。
- **功能约束**：
  - `background=true` 时，`stream=true` 不被支持（见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）；
  - `full_thoughts` 模式已被标记为“不推荐新业务使用”，应改用 `message_format` 或 `message_format_plus`（见 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)）；
  - `memory_id` 和 `file_list` 仅智能体应用支持；`flow_stream_mode` 仅工作流应用支持。
- **安全实践**：禁止在代码中硬编码 `API Key`，务必通过环境变量或密钥管理服务注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)


