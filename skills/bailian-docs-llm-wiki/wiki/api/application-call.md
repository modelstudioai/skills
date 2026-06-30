# application call

阿里云百炼应用（智能体、工作流、新版智能体 Agent 2.0）支持通过 API 调用，将你在控制台编排好的应用集成到业务系统中。调用前需先在控制台获取应用 ID 和 [API Key](../concepts/api-key.md)，再依据是否需要即时返回结果，选择 OpenAI 兼容模式的 Responses API（同步/异步）或 DashScope 原生 API（`/completion`）发起请求。

## 前置准备

调用任一百炼应用都需要以下凭证与配置：

1. **应用 ID（APP ID）**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面，从应用卡片上复制其 ID。若应用位于子[业务空间](../concepts/workspace.md)，还需同时提供 **Workspace ID**；位于默认[业务空间](../concepts/workspace.md)则仅需 APP ID。详细获取步骤见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
2. **[API Key](../concepts/api-key.md)**：通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)（推荐 `DASHSCOPE_API_KEY`）。不建议在生产环境硬编码。
3. **SDK（可选）**：OpenAI 兼容模式用 [OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)；DashScope 原生模式用对应语言的 DashScope SDK。

> **注意**：目前只能在控制台手动获取 APP ID 和 Workspace ID，不支持通过 API 或 CLI 查询。RAM 子账号默认只能查看其已加入的[业务空间](../concepts/workspace.md)的 ID；查询主账号下全部业务空间需主账号或被授予 `AliyunBailianFullAccess`/`AliyunBailianControlFullAccess` 权限。

## 两套调用 API

百炼应用提供两套 API，按是否需要复用 OpenAI 生态选择：

| API 模式 | Endpoint | 适用场景 | 文档 |
| --- | --- | --- | --- |
| **OpenAI 兼容 Responses API** | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | 复用现有 OpenAI 代码库与工具链；支持同步/异步、流式、[多模态](../concepts/multimodal.md) | [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) / [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md) |
| **DashScope 原生 API** | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | 更全面的功能与更高的性能；新版智能体（Agent 2.0）、工作流、旧版智能体均支持 | [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md) / [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md) |

> **注意**：上述 Endpoint 仅适用于华北2（北京）地域。德国（法兰克福）、新加坡、日本（东京）等地域，或调用子业务空间下的应用时，请求中必须包含 Workspace ID，该 ID 是对应地域 Base URL 的组成部分。

## OpenAI 兼容模式（Responses API）

SDK 调用需配置的 `base_url`：

```
https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1
```

HTTP 调用 Endpoint：

```
POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses
```

### 关键参数

- **app_id**（必选，string）：应用标识。HTTP 调用时放入 URL 中替换 `{APP_ID}`。
- **input**（必选，string 或 array）：核心输入。简单字符串用于单轮文本对话；消息数组用于多轮对话或[多模态](../concepts/multimodal.md)输入。
  - 消息 `role` 取值：`system`（可选，设定角色/约束）、`user`（必选）、`assistant`（可选，模型回复）。
  - [多模态](../concepts/multimodal.md) `content` 为数组，子对象 `type`：`input_text`（文本）、`input_image`（图像，需配 `image_url`）、`input_file`（文件，需配 `file_url`，仅[智能体应用](../concepts/agent-application.md)支持）。
- **stream**（可选，boolean）：是否[流式输出](../concepts/streaming-output.md)，默认 `false`。
- **background**（可选，boolean）：是否异步执行，默认 `false`。

> **注意**：基于 `pre_response_id` 或 `conversation_id` 的上下文功能将在后续支持，目前请在每次请求时传递完整对话历史（Responses API 多轮）。[异步调用](../concepts/async-invocation.md)暂不支持[流式输出](../concepts/streaming-output.md)。

### 同步调用

适用于即时获取结果的实时交互场景。单轮对话直接传字符串或 messages；多轮对话把完整历史消息数组传给 `input`：

```python
from openai import OpenAI
import os

api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'  # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

client = OpenAI(api_key=api_key, base_url=base_url)

response = client.responses.create(
    input=[
        {"role": "user", "content": "你是谁？"},
        {"role": "assistant", "content": "我是一个AI助手……"},
        {"role": "user", "content": "你能做什么？"}
    ],
)
print(response.model_dump_json(indent=2))
```

[流式输出](../concepts/streaming-output.md)只需设置 `stream=True`。**工作流应用**需在结束节点或流程输出节点启用「[流式输出](../concepts/streaming-output.md)」开关并重新发布；**[智能体应用](../concepts/agent-application.md)**做图像输入需选用通义千问 VL 系列模型并将文件处理方式设为「自定义处理」后重新发布。

### [异步调用](../concepts/async-invocation.md)

适用于耗时较长的任务（生成报告、多步骤工具调用等）。设置 `background=True`，API 立即返回任务 ID，再通过轮询 `retrieve` 查询状态，直到进入终态（`completed`/`failed`/`cancelled`）：

```python
import asyncio, os, time
from openai import AsyncOpenAI

api_key = os.getenv("DASHSCOPE_API_KEY")
app_id = 'APP_ID'
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'
client = AsyncOpenAI(api_key=api_key, base_url=base_url)

async def main():
    create_resp = await client.responses.create(
        input="请为我规划一个为期三天的北京旅游行程。",
        background=True
    )
    task_id = create_resp.id
    while True:
        resp = await client.responses.retrieve(task_id)
        if resp.status in ['completed', 'failed', 'cancelled']:
            break
        await asyncio.sleep(2)
    print(resp.model_dump_json(indent=2))

asyncio.run(main())
```

异步任务也支持**取消**和**删除**操作，详见[异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

### 自定义参数与插件参数传递

- **自定义参数**：在应用「开始」节点创建自定义参数，大模型节点提示词中引用（如 `/city`），发布后通过 `extra_body.biz_params` 传入，参数名与类型须与应用配置一致：
  ```python
  response = await client.responses.create(
      input="你好",
      extra_body={"biz_params": {"city": "北京"}},
      background=True
  )
  ```
- **插件参数**：[智能体应用](../concepts/agent-application.md)在应用内选择插件并发布即可；工作流应用需添加插件节点，并在开始节点创建自定义参数传入插件入参，再在大模型节点提示词中引用自定义参数与插件输出参数。

## DashScope 原生模式（/completion）

请求地址：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

请求体结构：

```json
{
  "input": { "prompt": "你是谁？" },
  "parameters": {},
  "debug": {}
}
```

### 单轮对话

Python（DashScope SDK）：

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',  # 替换为实际的应用 ID
    prompt='你是谁？')

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}\ncode={response.status_code}\nmessage={response.message}')
else:
    print(response.output.text)
```

除 Python/Java SDK 外，DashScope 原生 API 还提供 PHP、Node.js、C#、Go 的 HTTP 调用示例，详见[新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)与[工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。

### 多轮对话

- **新版智能体应用**：通过 `session_id` 维护上下文。首次请求无需传入，响应中返回新生成的 `session_id`；后续请求携带上一轮的 `session_id` 即可延续对话，有效期 1 小时。
- **工作流与旧版智能体应用**：通过 `session_id` 或 `messages` 启用多轮对话。

```python
response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你是谁？')

responseNext = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='APP_ID',
    prompt='你有什么技能?',
    session_id=response.output.session_id)  # 上一轮 response 的 session_id
print(responseNext.output.text)
```

## 限制与注意事项

- **地域限制**：本文档涉及的 Responses API 与 DashScope `/completion` 接口均仅适用于华北2（北京）地域。
- **异步不支持流式**：异步任务（`background=true`）暂不支持 `stream=true`。
- **多轮上下文**：Responses API 目前不支持基于 `pre_response_id`/`conversation_id` 的上下文，每次请求需传完整历史；DashScope 原生 API 用 `session_id`（有效期 1 小时）或 `messages` 维持多轮。
- **文件输入仅智能体支持**：`input_file` 仅智能体应用可用，且应用内文件处理方式需选「全文引用」或「切片检索」。
- **应用配置须重新发布**：[流式输出](../concepts/streaming-output.md)、图像输入、插件/自定义参数等能力都需要先在应用内正确配置并**重新发布**后才能生效。
- **权限**：查询全部业务空间需主账号或被授予权限的 RAM 子账号；普通 RAM 子账号只能查看其已加入的业务空间。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)




