# application call

阿里云百炼平台提供两套 API 来调用智能体和工作流应用：DashScope API 与 OpenAI 兼容的 Responses API。开发者可根据场景选择同步调用（实时交互）或异步调用（耗时任务），并通过[流式输出](../concepts/streaming.md)降低首字延迟。调用前需获取 APP ID、API Key，如应用位于子[业务空间](../concepts/workspace.md)还需提供 Workspace ID。

## 前置准备

调用应用前需完成以下步骤：

1. **创建应用**：在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面创建智能体或工作流应用。
2. **获取 APP ID**：在应用卡片上复制 APP ID，这是调用时的必选参数。如需调用子[业务空间](../concepts/workspace.md)下的应用，还需获取 Workspace ID，具体方法参见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
3. **获取 API Key**：通过密钥管理页面获取，建议配置到环境变量 `DASHSCOPE_API_KEY` 中，避免硬编码。
4. **安装 SDK（可选）**：DashScope API 可用 Python/Java [DashScope SDK](../concepts/dashscope-sdk.md)；Responses API 可用 OpenAI Python SDK。

## 两套 API 对比

百炼应用调用支持两套接口协议，详细参数见[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)和[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

| 维度 | DashScope API | Responses API（OpenAI 兼容） |
|------|--------------|---------------------------|
| 端点 | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| SDK | DashScope Python/Java SDK | OpenAI Python SDK |
| 多轮对话 | 通过 `session_id` 自动维护云端历史（1 小时有效） | 客户端维护完整对话历史，每次传入 `input` 消息数组 |
| 异步调用 | 不支持 | 设置 `background=true`，通过轮询 `retrieve` 获取结果 |
| 适用范围 | 新版智能体、工作流、旧版智能体 | 新版智能体、工作流（仅中国大陆北京地域） |

> **注意**：两套 API 的多轮对话机制不同。DashScope API 使用服务端 `session_id` 自动管理上下文，而 Responses API 需要客户端自行拼装完整历史消息。

## 调用方式

### 单轮对话

**DashScope API（Python）**：

```python
from dashscope import Application
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你是谁？')
print(response.output.text)
```

**Responses API（Python）**：

```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/')
response = client.responses.create(input="你是谁？")
```

### 多轮对话

- **DashScope API**：首次调用无需 `session_id`，响应中会返回 `session_id`，后续请求携带即可延续对话。`session_id` 在最后一次请求后 1 小时内有效。
- **Responses API**：将包含完整历史消息的数组传入 `input` 参数，角色包括 `user`、`assistant`、`system`。

### [流式输出](../concepts/streaming.md)

两套 API 均支持[流式输出](../concepts/streaming.md)，推荐开启以降低首字延迟：

- **DashScope API**：设置 `stream=True` 和 `incremental_output=True`。HTTP 调用需添加 Header `X-DashScope-SSE: enable`。Java SDK 使用 `streamCall()` 方法。
- **Responses API**：设置 `stream=True`，工作流应用需在结束节点启用[流式输出](../concepts/streaming.md)开关。

### 异步调用

仅 Responses API 支持异步模式，适用于耗时较长的任务（如生成报告、多步骤工具调用），详见[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。核心流程：

1. 创建任务：设置 `background=True`，立即返回任务 ID。
2. 轮询状态：调用 `retrieve` 方法查询任务状态（`queued` / `running` / `completed` / `failed` / `cancelled`）。
3. 管理任务：支持 `cancel`（取消）和 `delete`（删除记录）操作。

> **注意**：异步调用暂不支持[流式输出](../concepts/streaming.md)。

## 多模态输入

### 视觉理解

通过 `image_list`（DashScope API）或 `input_image`（Responses API）传入图片 URL 或 Base64 Data URL。应用内需选择通义千问 VL 系列模型。

### 文件问答

通过 `file_list`（DashScope API）或 `input_file`（Responses API）传入文件 URL，支持文档、图片、音视频。应用内需开启预解析文件开关。

## 关键请求参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用 ID，从应用管理页面获取 |
| `prompt` / `input` | string/array | 是 | 用户输入（DashScope 用 `prompt`，Responses 用 `input`） |
| `session_id` | string | 否 | 多轮对话标识，仅 DashScope API |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming.md)，默认 `false` |
| `incremental_output` | boolean | 否 | 流式模式下是否增量输出，默认 `false` |
| `workspace` | string | 否 | 子[业务空间](../concepts/workspace.md) ID |
| `enable_thinking` | boolean | 否 | 深度思考模式开关 |
| `has_thoughts` | boolean | 否 | 是否输出思考过程 |
| `model_id` | string | 否 | 覆盖应用内配置的模型 |
| `biz_params` | object | 否 | 自定义参数 / 插件参数传递 |
| `background` | boolean | 否 | 异步模式开关，仅 Responses API |

## 响应结构

**DashScope API** 响应核心字段：

- `output.text`：模型生成的回复文本
- `output.finish_reason`：完成原因（`stop` 为正常结束）
- `output.session_id`：会话标识，用于多轮对话
- `output.thoughts`：深度思考过程（需启用 `has_thoughts`）
- `usage.models`：调用的模型及 Token 用量

**Responses API** 响应核心字段：

- `output[].content[].text`：输出文本
- `status`：任务状态（`completed` / `failed`）
- `id`：请求唯一标识

## 限制与注意事项

- 单应用默认 QPM 为 15000。
- `session_id`（DashScope API）在最后一次请求后 1 小时失效。
- 目前 APP ID 和 Workspace ID 只能通过控制台手动获取，不支持 API 查询。
- DashScope API 与 Responses API 均仅适用于中国大陆版（北京地域）。
- 调用失败时可参考错误码文档排查问题。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)



