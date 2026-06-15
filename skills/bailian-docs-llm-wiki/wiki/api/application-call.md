# application call

百炼应用调用 API 用于通过 HTTP 或 SDK 远程触发已发布的**智能体**和**工作流**应用，并获取模型输出。平台提供两套并行接口：原生的 **DashScope API**（功能最完整、性能最优）与 **OpenAI 兼容模式的 Responses API**（便于复用 OpenAI 生态代码与工具）。本页面归纳两套接口的端点、调用方式、输入输出与典型差异，作为编写应用调用代码的入口。

> **注意**：本组接口仅适用于中国大陆版（北京地域）。其他地域调用方式以对应地域文档为准。

## 凭证准备

调用任意应用接口前，需要先准备以下三类凭证：

- **API Key**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)创建并配置到环境变量 `DASHSCOPE_API_KEY`。
- **APP ID**：每个应用的唯一标识。在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面的应用卡片上复制；HTTP 调用时将其拼到 URL 的 `APP_ID` 占位符位置，SDK 调用时作为 `app_id`/`appId` 参数传入。
- **Workspace ID**（条件必填）：[业务空间](../concepts/workspace.md)标识。当应用位于**子[业务空间](../concepts/workspace.md)**，或调用德国（法兰克福）地域下的模型时，请求中必须携带 `Workspace ID`。

> **注意**：目前 APP ID 与 Workspace ID 只能通过控制台手动获取，不支持通过 API 或 CLI 查询。详细的控制台操作步骤参见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 两套 API 体系

百炼应用调用提供两条并行的 API 路径，开发者可按需要选择：

| 维度 | DashScope API | OpenAI Responses API |
| --- | --- | --- |
| 适用应用类型 | 智能体（含新版 Agent 2.0）、工作流 | 智能体、工作流 |
| HTTP 端点 | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| SDK | DashScope Python / Java SDK（`Application.call`） | OpenAI 官方 SDK（`client.responses.create`） |
| 请求结构 | `{ "input": { "prompt": ... }, "parameters": {}, "debug": {} }` | `{ "input": "..." }` 或消息数组 |
| 主要优势 | 功能最全、性能最高，支持多轮上下文、流式、Plugin、RAG、Function Calling 等 | 易于迁移现有 OpenAI 代码、复用 OpenAI 生态工具 |
| 多模态输入 | 支持文本/图片/文件/音视频等场景 | 支持 `input_text` / `input_image` / `input_file` 三种内容块 |
| 异步调用 | 通过原生[异步任务](../concepts/async-task.md)接口 | 在请求体设置 `background=true` |

> **注意**：如果应用同时希望获得完整功能与最优性能，应优先选择 DashScope API；OpenAI Responses API 适合需要快速接入 OpenAI 生态或迁移已有代码的场景。

## DashScope API 调用

### 端点与 SDK

- HTTP：`POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion`，需在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。
- Python：`from dashscope import Application` → `Application.call(api_key=..., app_id=..., prompt=...)`。
- Java：`ApplicationParam.builder().apiKey(...).appId(...).prompt(...).build()` 后调用 `application.call(param)`，建议 SDK 版本 ≥ 2.12.0。
- 其它语言：可使用 PHP、Node.js、Go 等任何能发起 HTTP 请求的环境直接调 HTTP 接口。

### 请求体字段

- `input.prompt`（string，必选）：用户输入。
- `input.messages`（array，可选）：多轮对话历史，每个元素含 `role`、`content`。
- `input.biz_params`（object，可选）：工作流应用的业务变量；新版智能体应用按其专属字段约定填写。
- `parameters`（object，可选）：模型/流程级别参数，如 `top_p`、`top_k`、`temperature`、`incremental_output`（[流式输出](../concepts/streaming.md)增量模式）等。
- `debug`（object，可选）：调试信息开关。

### 在线调试

无需自行构造代码，进入**应用卡片 → 发布 → API 调试**即可填写参数、运行请求并查看响应。

DashScope API 的完整字段、新版智能体的专属请求结构和典型场景示例请参考 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 与 [应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

> **注意**：新版智能体应用（Agent 2.0）与旧版智能体/工作流应用的请求字段并不完全一致，请按实际创建的应用版本对应阅读相应文档，避免参数字段错配。

## OpenAI Responses API 调用

### 端点与 SDK 配置

- HTTP：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。
- OpenAI SDK：将 `base_url` 配置为 `https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/`，`api_key` 使用 `DASHSCOPE_API_KEY`。
- 调用入口：`client.responses.create(input=..., stream=..., background=...)`。

### 关键请求字段

- `app_id`（路径参数，必选）：应用 ID，作为 URL 中的 `{APP_ID}`。
- `input`（string 或 array，必选）：可以是简单字符串（单轮）或包含 `system` / `user` / `assistant` 消息的数组（多轮）。
  - 文本：`{ "type": "input_text", "text": "..." }`。
  - 图片：`{ "type": "input_image", "image_url": "..." }`。
  - 文件：`{ "type": "input_file", "file_url": "..." }`，仅**智能体应用**支持。
- `stream`（boolean，默认 false）：是否[流式输出](../concepts/streaming.md)。工作流应用启用[流式输出](../concepts/streaming.md)还需在**结束节点**或**流程输出节点**勾选**[流式输出](../concepts/streaming-output.md)**开关并重新发布。
- `background`（boolean，默认 false）：是否以异步方式执行任务；`true` 时会立即返回任务 ID，且**[异步任务](../concepts/async-task.md)不支持[流式输出](../concepts/streaming-output.md)**。

### 多模态输入应用配置

- **图像输入**：智能体应用需将模型切换为[通义千问 VL 系列](https://help.aliyun.com/zh/model-studio/vision)，文件处理方式选**自定义处理**；工作流应用需将模型节点的入参变量填为 `imageList`。配置后重新发布应用。
- **文件输入**：仅智能体应用支持，文件处理方式需选择**全文引用**或**切片检索**。

### 响应对象

- 非流式：返回 `{ id, object: "response", created_at, status, output: [{ content: [{ type: "output_text", text }], role: "assistant", status, type: "message" }] }`。
- 流式：基于 SSE 协议返回事件流，包含整体生命周期事件（`response.created` / `in_progress` / `completed`）、输出项事件（`response.output_item.added/done`）、内容块事件（`response.content_part.added/done`）以及文本增量事件（`response.output_text.delta/done`，思考过程则为 `response.reasoning_text.delta/done`）。

完整请求字段、文本/图像/文件多种输入示例、流式响应事件协议与字段语义请参考 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

> **注意**：基于 `pre_response_id` 或 `conversation_id` 的上下文功能在 Responses API 中尚未支持，目前必须在每次请求时把完整对话历史放入 `input` 数组。

## 同步与异步选择

- **同步调用**：API 在生成完成前保持连接，适合即时交互场景（聊天、问答、短任务）。
- **异步调用**：适用于报告生成、多步工具调用等**耗时较长**的任务，避免长连接超时。流程为：
  1. **创建任务**：调用 `client.responses.create(..., background=True)`，取出返回的 `task_id`。
  2. **轮询状态**：循环调用 `client.responses.retrieve(task_id)`，建议 2 秒一次。
  3. **处理结果**：当 `status` 变为 `completed` / `failed` / `cancelled` 之一时退出循环，从 `output[0].content[0].text` 中提取最终文本。

异步调用的完整 Python/Java 示例与状态机说明参见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：[异步任务](../concepts/async-task.md)暂不支持[流式输出](../concepts/streaming-output.md)（`stream=true` 与 `background=true` 不能同时启用）。

## [流式输出](../concepts/streaming-output.md)要点

- DashScope API：通过 SDK 参数（如 Python 的 `stream=True`）或 HTTP Header（`X-DashScope-SSE: enable`）开启，事件结构以 DashScope 自定义协议返回。
- Responses API：在请求体中设置 `stream=true`，事件以 SSE 形式按 `id / event / data` 行返回；通过 `response.output_text.delta` 事件实时拼接 `delta` 即可获得渐进式文本。
- **工作流应用**：除接口层开启流式外，还必须在**结束节点**或**流程输出节点**启用**[流式输出](../concepts/streaming-output.md)**并重新发布应用，否则流式开关不生效。

## 错误码与排查

应用调用失败时，响应通常包含 `request_id`、`code`、`message` 三个字段。请保留 `request_id` 用于工单追踪，并参考 [错误码](https://help.aliyun.com/zh/model-studio/error-code) 解决常见错误。OpenAI SDK 返回的响应中可能包含百炼未实际填充的 OpenAI 协议字段（一般为 `null`），按本组文档列出的字段为准即可。

## 关键限制与注意事项

- 本组 API 仅支持**中国大陆（北京地域）**。
- 子[业务空间](../concepts/workspace.md)下的应用必须显式传入 `Workspace ID`；RAM 子账号默认只能查看其加入的[业务空间](../concepts/workspace.md)，查询全部[业务空间](../concepts/workspace.md)需主账号或拥有 `AliyunBailianFullAccess` / `AliyunBailianControlFullAccess` 权限。
- 多轮对话上下文需由客户端自行维护；服务端的会话/Response 上下文功能在 Responses API 中**尚未上线**。
- 异步调用与[流式输出](../concepts/streaming-output.md)互斥；图像/文件输入需要对应的应用类型与模型选择，否则请求会失败。
- 选择 API 时优先考虑：是否需要 OpenAI 生态兼容（→ Responses API）、是否需要平台全功能与最佳性能（→ DashScope API）。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)










