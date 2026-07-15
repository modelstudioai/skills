# application call

阿里云百炼平台提供两套 API 来调用智能体和工作流应用：**OpenAI 兼容的 Responses API** 和 **DashScope API**。两者均支持同步/[异步调用](../concepts/async-invocation.md)、多轮对话、[流式输出](../concepts/streaming.md)等核心能力，开发者可根据生态兼容性和功能需求选择合适的接入方式。调用前需先获取 APP ID（以及子[业务空间](../concepts/workspace.md)场景下的 Workspace ID）和 [API Key](../concepts/api-key.md)。

## 前置准备

### 获取凭证

通过 API 调用应用时，必须提供 **APP ID** 来指定目标应用。如果应用位于子[业务空间](../concepts/workspace.md)，还需提供 **Workspace ID**。详细获取方式参见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

- **APP ID**：在控制台「应用管理」页面的应用卡片上复制。
- **Workspace ID**：在调用子[业务空间](../concepts/workspace.md)下的应用或特定地域（德国、华北2、新加坡、日本）的模型时必须提供，可通过控制台右上角图标查看。

> **注意**：目前只能通过控制台手动获取 APP ID 和 Workspace ID，不支持通过 API 或 CLI 查询。

### 其他前提

- 已获取 [API Key](../concepts/api-key.md) 并配置到环境变量 `DASHSCOPE_API_KEY`。
- 已创建并发布百炼应用（智能体或工作流）。
- 如使用 SDK 调用，需安装对应的 SDK（OpenAI SDK 或 [DashScope SDK](../concepts/dashscope-sdk.md)）。

## 两套 API 对比

| 维度 | Responses API（OpenAI 兼容） | DashScope API |
|------|---------------------------|---------------|
| Endpoint | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` |
| SDK | OpenAI Python/Java SDK | DashScope Python/Java SDK |
| 多轮对话 | 通过 `input` 数组传递完整历史消息 | 通过 `session_id` 或 `messages` 维护上下文 |
| [异步调用](../concepts/async-invocation.md) | 设置 `background=true` | 暂不支持（仅 Responses API 提供） |
| 适用地域 | 仅华北2（北京） | 仅华北2（北京） |

## Responses API（OpenAI 兼容模式）

### 同步调用

适用于需要即时获取结果的实时交互场景。完整参数说明参见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

**核心请求参数：**

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `input` | string / array | 是 | 请求输入，可为简单字符串或包含多轮对话历史的消息数组 |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming.md)，默认 `false` |
| `background` | boolean | 否 | 是否异步执行，默认 `false` |

**Python 示例（单轮对话）：**

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/'
)

response = client.responses.create(input="你是谁？")
print(response.model_dump_json(indent=2))
```

**多轮对话**需在 `input` 中传递完整的消息历史数组，每条消息包含 `role`（user/assistant/system）和 `content` 字段。

### [多模态](../concepts/multimodal.md)输入

Responses API 支持在 `content` 数组中混合多种输入类型：

- **图像输入**：通过 `input_image` 类型传入图片 URL。[智能体应用](../concepts/agent-application.md)需选用通义千问 VL 系列模型并将文件处理方式设为「自定义处理」。
- **文件输入**：通过 `input_file` 类型传入文件 URL。仅[智能体应用](../concepts/agent-application.md)支持，需配置「全文引用」或「切片检索」处理方式。

### [异步调用](../concepts/async-invocation.md)

对于耗时较长的任务（如生成报告、多步骤工具调用），可设置 `background=true` 开启异步模式，避免请求超时。详细流程参见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

核心流程：

1. **创建任务**：请求中设置 `background=true`，API 立即返回任务 ID。
2. **轮询状态**：通过 `client.responses.retrieve(task_id)` 定期查询任务状态。
3. **处理结果**：当状态变为 `completed`、`failed` 或 `cancelled` 时获取最终结果。

> **注意**：异步任务暂不支持[流式输出](../concepts/streaming.md)（`stream=true`）。

### [流式输出](../concepts/streaming.md)

设置 `stream=true` 可边生成边输出，适用于需要实时展示生成内容的场景。若应用类型为工作流，需在结束节点或流程输出节点中启用「[流式输出](../concepts/streaming.md)」开关并重新发布。

## DashScope API

DashScope API 提供更全面的功能支持，适合需要深度集成百炼平台能力的场景。支持 Python、Java、PHP、Node.js、C#、Go 等多种语言的 HTTP 调用，以及 Python/Java SDK。详细参数参见 [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

**Python 示例：**

```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你是谁？'
)
print(response.output.text)
```

**多轮对话**通过 `session_id` 维护上下文：首次请求无需传入，响应中会返回 `session_id`；后续请求携带该值即可延续对话。`session_id` 在最后一次请求后 1 小时内有效。

新版[智能体应用](../concepts/agent-application.md)（Agent 2.0）的调用方式与上述基本一致，参见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

## 参数传递

### 自定义参数

工作流应用中定义的自定义参数，通过请求体中的 `biz_params` 传递，参数名和类型需与应用内配置保持一致。

```python
response = await client.responses.create(
    input="你好",
    extra_body={"biz_params": {"city": "北京"}},
    background=True
)
```

### 插件参数

智能体或工作流中配置的插件工具参数，同样通过 `biz_params` 传递。工作流需在开始节点创建自定义参数并将其传入插件节点的输入参数中。

## 限制与注意事项

- 两套 API 目前均**仅适用于华北2（北京）地域**。
- Responses API 的多轮对话暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文功能，需每次传递完整对话历史。
- [异步调用](../concepts/async-invocation.md)仅 Responses API 支持，且不能与[流式输出](../concepts/streaming.md)同时使用。
- RAM 子账号查看[业务空间](../concepts/workspace.md)管理页面需要超级管理员权限（`AliyunBailianFullAccess` 或 `AliyunBailianControlFullAccess`）。
- [API Key](../concepts/api-key.md) 不建议硬编码到代码中，应通过环境变量配置以降低泄露风险。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [应用 DashScope API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)










