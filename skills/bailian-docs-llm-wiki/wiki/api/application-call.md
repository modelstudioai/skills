# application call

阿里云百炼提供两套 API 来调用已发布的应用（智能体、工作流）：**DashScope API** 和 **OpenAI 兼容的 Responses API**。开发者需先获取 APP ID（以及子[业务空间](../concepts/workspace.md)下的 Workspace ID）和 API Key，然后根据应用类型和场景选择合适的调用方式。本文汇总了应用调用的前置准备、两套 API 的核心差异、关键参数及调用模式。

## 前置准备

调用任何百炼应用之前，需完成以下步骤：

1. **获取 API Key**：在百炼控制台的密钥管理页面创建并配置到环境变量 `DASHSCOPE_API_KEY`。
2. **获取 APP ID**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面复制目标应用的 APP ID。
3. **获取 Workspace ID**（仅子[业务空间](../concepts/workspace.md)或德国地域需要）：在控制台右上角图标处查看，或由超级管理员在[业务空间](../concepts/workspace.md)管理页面查询全部空间 ID。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
4. **安装 SDK**（可选）：根据选用的 API 安装 DashScope SDK 或 OpenAI SDK。

## 两套 API 对比

百炼应用调用目前有两套 API 体系，功能和适用场景不同：

| 维度 | DashScope API | OpenAI 兼容 Responses API |
|------|--------------|--------------------------|
| Endpoint | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| 适用应用 | 新版智能体、工作流、旧版智能体 | 智能体、工作流 |
| 多轮对话 | 通过 `session_id` 或 `messages` 维护上下文 | 需在每次请求中传递完整对话历史（`pre_response_id` / `conversation_id` 后续支持） |
| 异步调用 | 通过 `X-DashScope-Async: enable` 请求头 | 通过 `background: true` 参数 |
| [流式输出](../concepts/streaming-output.md) | `stream: true`（含 SSE） | `stream: true` |
| SDK | DashScope Python/Java SDK | OpenAI Python/Java SDK |
| 生态兼容 | 百炼原生 | 可复用 OpenAI 生态工具和代码库 |

> **注意**：两套 API 仅适用于中国大陆版（北京地域）。如需调用德国（法兰克福）地域的应用，请参考对应地域文档。

## DashScope API 调用

### 新版智能体应用

新版智能体应用（Agent 2.0）使用 DashScope SDK 中的 `Application.call()` 方法调用。核心参数包括：

- **`app_id`**（必选）：应用 ID。
- **`prompt`**（必选）：用户输入文本。
- **`session_id`**（可选）：多轮对话标识，首次请求无需传入，后续携带上一次响应返回的 `session_id` 即可延续对话。有效期为最后一次请求后 1 小时。

详细参数和多语言代码示例参见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

### 工作流与旧版智能体应用

工作流和旧版智能体使用相同的 DashScope API 端点，同样通过 `Application.call()` 调用。除基本参数外，还支持：

- **`biz_params`**：向工作流传递自定义参数（参数名和类型需与应用配置一致）。
- **`session_id` / `messages`**：两种多轮对话方式。
- 插件参数传递：智能体应用可通过 API 传入插件所需参数。

详细参数和代码示例参见 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

## OpenAI 兼容 Responses API 调用

Responses API 采用 OpenAI 兼容模式，便于开发者复用现有 OpenAI 代码库。分为同步和异步两种模式。

### 同步调用

适用于需要即时获取结果的实时交互场景。核心参数：

- **`input`**（必选）：可以是简单字符串或包含多轮对话历史的消息数组。消息数组支持 System/User/Assistant 三种角色，User 消息的 `content` 支持文本（`input_text`）、图像（`input_image`）和文件（`input_file`）。
- **`stream`**（可选）：设为 `true` 启用[流式输出](../concepts/streaming-output.md)。工作流应用需在结束节点或流程输出节点中启用[流式输出](../concepts/streaming-output.md)开关并重新发布。

详细用法参见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 异步调用

适用于耗时较长的任务（如生成报告、多步骤工具调用），可避免请求超时。核心流程：

1. **创建任务**：在请求中设置 `background: true`，API 立即返回任务 ID。
2. **轮询状态**：通过 `client.responses.retrieve(task_id)` 查询任务状态。
3. **处理结果**：状态变为 `completed`、`failed` 或 `cancelled` 时获取最终结果。

> **注意**：[异步任务](../concepts/async-task.md)暂不支持流式输出（`stream: true`）。

详细用法参见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

## 输入类型

Responses API 支持多种输入类型：

- **文本输入**：最基本的对话输入，支持单轮和多轮。
- **图像输入**：通过 `input_image` 提供图片 URL。智能体应用需选用通义千问 VL 系列模型并将文件处理方式设为自定义处理；工作流应用需将模型入参变量设为 `imageList`。
- **文件输入**：通过 `input_file` 提供文件 URL。仅智能体应用支持，需将文件处理方式选择全文引用或切片检索。

## 多语言 SDK 支持

两套 API 均提供丰富的语言支持：

- **DashScope API**：Python、Java、HTTP（curl/PHP/Node.js/C#/Go）
- **Responses API**：Python（OpenAI SDK）、Java（OpenAI SDK）、HTTP（curl）

## 限制和注意事项

- 所有应用调用 API 仅适用于**中国大陆版（北京地域）**。
- APP ID 和 Workspace ID 目前只能通过控制台手动获取，不支持通过 API 或 CLI 查询。
- 子业务空间下的应用调用必须同时提供 APP ID 和 Workspace ID。
- DashScope API 的 `session_id` 在最后一次请求后 1 小时内有效。
- Responses API 的多轮对话需在每次请求中传递完整对话历史，基于 `pre_response_id` 或 `conversation_id` 的上下文功能将在后续版本支持。
- 不建议在生产环境中将 API Key 硬编码到代码中，应通过环境变量配置。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


