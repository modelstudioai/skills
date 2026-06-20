# application call

阿里云百炼平台提供两套 API 体系来调用智能体和工作流应用：DashScope API 和 OpenAI 兼容的 Responses API。开发者可根据应用类型（新版智能体、旧版智能体、工作流）和调用模式（同步、异步、流式）选择合适的接入方式。所有调用都需要先获取 APP ID 和 API Key，子业务空间下的应用还需要 Workspace ID。

## 前置准备

调用应用前需完成以下准备工作：

1. **创建应用**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中创建智能体或工作流应用
2. **获取 APP ID**：在应用列表中复制目标应用的 APP ID，详见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
3. **获取 API Key**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并配置到环境变量 `DASHSCOPE_API_KEY`
4. **获取 Workspace ID（按需）**：当应用位于子业务空间或使用德国（法兰克福）地域时，需额外提供 Workspace ID

> **注意**：目前只能通过控制台手动获取 APP ID 和 Workspace ID，不支持通过 API 或 CLI 查询。

## 两套 API 体系

百炼应用调用存在两套并行的 API 体系，适用场景不同：

| 特性 | DashScope API | Responses API（OpenAI 兼容） |
|------|--------------|---------------------------|
| 请求地址 | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| SDK | [DashScope SDK](../concepts/dashscope-sdk.md)（Python/Java） | OpenAI SDK |
| 支持的应用类型 | 新版智能体、旧版智能体、工作流 | 智能体、工作流 |
| 同步/异步 | 仅同步 | 同步和异步 |
| [流式输出](../concepts/streaming.md) | 支持 | 支持（异步模式除外） |
| 多模态输入 | 通过特定参数 | 通过 `input_image` / `input_file` 类型 |

> **注意**：两套 API 均仅适用于中国大陆版（北京地域）。如需了解 DashScope API 的完整参数，请参阅[工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)和[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。

## 调用方式

### 同步调用

同步调用适用于需要即时获取结果的实时交互场景。API 保持连接直到任务完成后返回完整结果。

**DashScope API 示例（Python）：**

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你是谁？')

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

**Responses API 示例（Python）：**

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
)

response = client.responses.create(input="你是谁？")
print(response.model_dump_json(indent=2))
```

更多语言（Java、HTTP/curl、PHP、Node.js、C#、Go）的示例详见[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。

### 异步调用

异步调用适用于耗时较长的任务（如生成报告、多步骤工具调用），通过设置 `background=true` 开启。API 立即返回任务 ID，后续通过轮询获取结果，避免请求超时。

核心流程：

1. **创建任务**：设置 `background=True`，获取任务 ID
2. **轮询状态**：定期调用 `retrieve` 方法查询任务状态
3. **处理结果**：任务状态变为 `completed`、`failed` 或 `cancelled` 时获取最终结果

```python
# 创建异步任务
response = await client.responses.create(
    input="请为我规划一个北京旅游行程。",
    background=True
)
task_id = response.id

# 轮询直到完成
while True:
    result = await client.responses.retrieve(task_id)
    if result.status in ['completed', 'failed', 'cancelled']:
        break
    await asyncio.sleep(2)
```

> **注意**：异步任务暂不支持[流式输出](../concepts/streaming.md)（`stream=true`）。详细用法参见[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

### [流式输出](../concepts/streaming.md)

在请求中设置 `stream=true` 可启用流式输出，实现边生成边返回的效果。工作流应用需在结束节点或流程输出节点中启用流式输出开关并重新发布。

## 多轮对话

两套 API 支持不同的多轮对话方式：

- **DashScope API**：通过 `session_id` 维护会话上下文。首次请求无需传入，响应会返回 `session_id`，后续请求携带即可延续对话。`session_id` 在最后一次请求后 1 小时内有效。
- **Responses API**：将包含完整历史消息的消息对象数组传递给 `input` 参数，每条消息包含 `role`（`user` / `assistant`）和 `content`。

## 多模态输入

Responses API 支持在 `content` 数组中传入多种类型的内容：

- **图像输入**：通过 `input_image` 类型传入图片 URL。智能体应用需选用通义千问 VL 系列模型，并将文件处理方式设为自定义处理。
- **文件输入**：通过 `input_file` 类型传入文件 URL。仅智能体应用支持，需将文件处理方式选择为全文引用或切片检索。

## 参数传递

通过 API 调用时可传递自定义参数：

- **自定义参数**：通过 `biz_params` 字段传递，参数名和类型需与应用内配置保持一致
- **插件参数**：需在应用中添加插件节点并配置对应的输入参数

## 关键请求参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `app_id` | string | 是 | 应用 ID，从应用管理页面获取 |
| `input` / `prompt` | string/array | 是 | 请求输入内容，字符串或消息数组 |
| `stream` | boolean | 否 | 是否流式输出，默认 `false` |
| `background` | boolean | 否 | 是否异步执行（仅 Responses API），默认 `false` |
| `session_id` | string | 否 | 多轮对话会话 ID（仅 DashScope API） |

## 在线调试

可通过**应用卡片 -> 发布 -> API 调试**路径进入调试页面，填写参数并点击运行即可快速验证。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


