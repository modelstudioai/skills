# application call

通过 API 调用阿里云百炼应用（智能体、工作流）时，需要提供 APP ID、API Key 等凭证，并选择合适的调用协议。百炼提供两套并行的应用调用接口：DashScope API（`/api/v1/apps/{APP_ID}/completion`）与 OpenAI 兼容模式的 Responses API（`/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`），后者又分同步与异步两种模式。所有应用调用 API 目前均仅适用于中国大陆版（北京地域），子[业务空间](../concepts/workspace.md)或海外地域则需额外提供 Workspace ID。

## 调用凭证

调用任一应用前，需准备以下凭证（详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）：

- **APP ID**：应用唯一标识。在控制台「应用管理」页面，从应用卡片上复制。HTTP 调用时拼入 URL 路径。
- **API Key**：在「密钥管理」获取，建议通过 `DASHSCOPE_API_KEY` 环境变量注入，避免硬编码到代码中。
- **Workspace ID**：[业务空间](../concepts/workspace.md)标识。仅以下场景必须在请求中携带：
  - 调用子[业务空间](../concepts/workspace.md)下的应用；
  - 调用德国（法兰克福）、华北2（北京）、新加坡、日本（东京）地域下的模型（Workspace ID 是这些地域 Base URL 的组成部分）。

> **注意**：目前只能通过控制台手动获取 APP ID 和 Workspace ID，不支持通过 API 或 CLI 查询。RAM 子账号默认仅能查看其已加入的业务空间的 ID；查询主账号下全部业务空间需超级管理员或 `AliyunBailianFullAccess`/`AliyunBailianControlFullAccess` 权限。

## 两套调用协议

百炼应用调用存在两套接口，开发者应按场景选择：

| 协议 | Endpoint | 适用场景 |
| --- | --- | --- |
| DashScope API | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | 功能最全、性能更高；通过 `input.prompt` 提交，使用 [DashScope SDK](../concepts/dashscope-sdk.md) |
| Responses API（同步） | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | OpenAI 兼容，可复用 OpenAI 代码库；实时交互 |
| Responses API（异步） | 同上，请求体 `background=true` | 耗时较长任务，先提交后轮询，避免请求超时 |

> **注意**：异步调用暂不支持[流式输出](../concepts/streaming-output.md)（`stream=true`）。`pre_response_id`/`conversation_id` 形式的上下文能力在 Responses API 中尚未支持，目前每次请求需传递完整对话历史。

## DashScope API 调用

DashScope API 同时覆盖新版智能体应用与工作流/旧版智能体应用，请求体结构一致（详见 [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) 与 [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)）：

### 请求体结构

```json
{
  "input": { "prompt": "你是谁？" },
  "parameters": {},
  "debug": {}
}
```

- `input.prompt`（必选）：用户输入文本。
- `parameters`（可选）：业务参数。
- `debug`（可选）：调试参数。

### 单轮对话示例（Python SDK）

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',       # 替换为实际的应用 ID
    prompt='你是谁？')

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}')
    print(f'code={response.status_code}')
    print(f'message={response.message}')
else:
    print(response.output.text)
```

HTTP/curl 形式：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": { "prompt": "你是谁？" },
    "parameters": {},
    "debug": {}
  }'
```

[DashScope SDK](../concepts/dashscope-sdk.md) 同时提供 Java 实现（建议 SDK 版本 ≥ 2.12.0），HTTP 方式还覆盖 PHP、Node.js、C#、Go 等语言，请求体结构一致。

### 多轮对话

DashScope API 通过 `session_id` 维护会话上下文：

1. 首次请求不传 `session_id`，响应中返回新生成的 `session_id`；
2. 后续请求携带上一轮响应的 `session_id` 即可延续对话；
3. `session_id` 在最后一次请求后 1 小时内有效。

```python
responseNext = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你有什么技能?',
    session_id=response.output.session_id)
```

> **注意**：旧版工作流应用 API 中也提到可通过 `messages` 启用多轮对话，与新版智能体应用的 `session_id` 机制不同，使用时请按所用应用类型选择对应字段。

## Responses API（OpenAI 兼容）

Responses API 让你以 OpenAI SDK 形式调用百炼应用，便于复用现有 OpenAI 生态代码（详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)）。

### base_url 与 endpoint

- SDK `base_url`：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1`
- HTTP endpoint：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`

`{APP_ID}` 需替换为实际应用 ID。

### 关键请求参数

- `app_id`（必选）：应用 ID。HTTP 调用时放入 URL；SDK 调用时通过 `base_url` 体现。
- `input`（必选）：核心输入，可为简单字符串或消息数组。
  - 简单字符串用于单轮文本对话，如 `"你好"`；
  - 消息数组用于多轮对话或多媒体输入，元素为 system / user / assistant 消息对象。
- `stream`（可选，布尔，默认 `false`）：是否[流式输出](../concepts/streaming-output.md)。`true` 时边生成边输出 chunk。
- `background`（可选，布尔，默认 `false`）：是否异步执行。`true` 时立即返回任务 ID，后续通过 `retrieve` 查询。

#### 消息对象类型

- **System Message**（可选）：`role` 固定 `system`，`content` 为字符串，用于设定模型角色与约束。
- **User Message**（必选）：`role` 固定 `user`，`content` 可为字符串（纯文本）或数组（多模态）。
  - 文本：`type=input_text`，`text` 文本内容；
  - 图像：`type=input_image`，`image_url` 图片 URL（智能体应用需选用通义千问 VL 系列并将文件处理方式设为「自定义处理」；工作流应用需在模型节点入参变量填 `imageList`）；
  - 文件：`type=input_file`，`file_url` 文件 URL（仅智能体应用支持，应用内文件处理方式需选「全文引用」或「切片检索」）。
- **Assistant Message**（可选）：`role` 固定 `assistant`，`content` 为模型上一轮回复。

### 同步单轮与流式

单轮对话：

```python
from openai import OpenAI
import os

api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

client = OpenAI(api_key=api_key, base_url=base_url)
response = client.responses.create(input="你是谁？")
print(response.model_dump_json(indent=2))
```

[流式输出](../concepts/streaming-output.md)需设置 `stream=True`。工作流应用需在结束节点或流程输出节点启用「流式输出」开关并重新发布。

## 异步调用

对于生成报告、多步骤工具调用等耗时任务，使用异步模式可避免长时间等待或请求超时（详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)）。

### 核心流程

1. **创建任务**：`create` 时设置 `background=True`，立即获取任务 ID。
2. **轮询状态**：循环调用 `retrieve` 查询任务状态。
3. **处理结果**：状态变为 `completed`、`failed` 或 `cancelled` 时退出循环并处理最终结果。

```python
import asyncio, os, time
from openai import AsyncOpenAI

api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
    create_response = await client.responses.create(
        input="请为我规划一个为期三天的北京旅游行程，要求包含故宫、长城。",
        background=True
    )
    task_id = create_response.id

    while True:
        retrieve_response = await client.responses.retrieve(task_id)
        status = retrieve_response.status
        if status in ['completed', 'failed', 'cancelled']:
            break
        await asyncio.sleep(2)

    if retrieve_response.status == 'completed':
        result_text = retrieve_response.output[0].content[0].text
        print(result_text)

asyncio.run(main())
```

> **注意**：异步调用暂不支持流式输出。`background=true` 与 `stream=true` 不可同时使用。

### 自定义参数与插件参数传递

工作流与智能体应用支持在调用时传入自定义参数和插件参数：

- **自定义参数**：在应用「开始」节点创建自定义参数，在模型节点提示词中通过 `/参数名` 引用，发布应用。调用时通过 `biz_params` 传递，参数名与类型须与应用内配置一致。
- **插件参数传递**：智能体应用在应用内选择指定插件并发布即可；工作流应用需添加「插件节点」选择插件工具，并将开始节点的自定义参数传入插件节点输入参数，再在大模型节点提示词中引用自定义参数与插件输出参数。

```python
response = await client.responses.create(
    input="你好",
    extra_body={"biz_params": {"city": "北京"}},
    background=True
)
```

## 限制与注意事项

- **地域限制**：所有应用调用 API（DashScope 与 Responses）目前仅适用于中国大陆版（北京地域）。海外/子业务空间地域需在请求中携带 Workspace ID。
- **异步不支持流式**：`background=true` 时不可同时设置 `stream=true`。
- **会话上下文**：DashScope API 通过 `session_id`（1 小时有效）维护多轮上下文；Responses API 当前需每次请求传递完整对话历史，`pre_response_id`/`conversation_id` 形式尚未支持。
- **多模态支持范围**：文件输入仅智能体应用支持；图像输入需在应用内配置通义千问 VL 系列模型并按应用类型设置文件处理方式或模型节点入参变量。
- **SDK 版本**：Java [DashScope SDK](../concepts/dashscope-sdk.md) 建议版本 ≥ 2.12.0；Responses API 使用 OpenAI Python/Java SDK，需正确配置 `base_url`。
- **API Key 安全**：建议通过 `DASHSCOPE_API_KEY` 环境变量注入，不要在生产环境硬编码到代码中。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)


