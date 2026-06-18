# 流式输出

流式输出（Streaming）是指模型在生成过程中将结果逐步返回给客户端的技术，而非等待全部生成完毕后一次性返回。通过流式输出，开发者可以显著降低首字延迟（Time to First Token），提升用户的交互体验。

## 工作原理

流式输出基于 Server-Sent Events（SSE）协议实现。服务端在生成每个 Token 后立即将其推送到客户端，客户端可以实时渲染已接收的内容，而无需等待完整响应。这对于长文本生成、对话式交互等场景尤为重要。

## 在百炼平台中的使用场景

### 文本生成模型调用

百炼平台的文本生成模型（如 Qwen 系列）通过 [OpenAI 兼容接口](openai-compatible.md)或 DashScope 原生接口均支持流式输出。开发者在调用时设置 `stream=True` 即可启用。

### 应用调用（DashScope API）

通过 DashScope API 调用智能体或工作流应用时，流式输出通过以下参数控制：

- **Python SDK**：设置 `stream=True` 和 `incremental_output=True`，其中 `incremental_output=True` 表示每次仅返回增量内容而非累积内容。
- **Java SDK**：使用 `streamCall()` 方法替代 `call()` 方法。
- **HTTP 调用**：在请求 Header 中添加 `X-DashScope-SSE: enable`。

```python
from dashscope import Application
import os

responses = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你的问题',
    stream=True,
    incremental_output=True)

for response in responses:
    print(response.output.text, end='')
```

### 应用调用（Responses API）

通过 OpenAI 兼容的 Responses API 调用应用时，设置 `stream=True` 即可启用流式输出。需要注意，工作流应用需在结束节点启用流式输出开关才能生效。

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/api/v2/apps/agent/YOUR_APP_ID/compatible-mode/v1/")

stream = client.responses.create(
    input="你的问题",
    stream=True)

for event in stream:
    print(event)
```

### 实时多模态交互（Omni Realtime API）

Qwen-Omni-Realtime API 基于 WebSocket 协议实现双向流式通信，天然支持流式输出。服务端通过以下事件增量推送生成内容：

- `response.audio.delta`：增量音频数据
- `response.audio_transcript.delta`：增量文本转录
- `response.function_call_arguments.delta`：工具调用参数的增量输出

这种模式适用于实时语音对话、音视频交互等低延迟场景。

## 关键参数

| 参数 | 适用接口 | 说明 |
|------|---------|------|
| `stream` | DashScope API / Responses API / [OpenAI 兼容接口](openai-compatible.md) | 设为 `True` 启用流式输出 |
| `incremental_output` | DashScope API | 设为 `True` 时每次仅返回增量内容；设为 `False` 时返回累积内容 |
| `X-DashScope-SSE: enable` | DashScope HTTP API | HTTP 调用时通过 Header 启用流式输出 |

## 注意事项

- **异步调用不支持流式输出**：Responses API 的异步模式（`background=True`）暂不支持流式输出，需通过轮询获取结果。
- **工作流应用需额外配置**：通过 Responses API 调用工作流应用时，需在工作流的结束节点启用流式输出开关。
- **增量与累积模式**：DashScope API 的 `incremental_output` 参数控制返回内容是增量还是累积。增量模式适合逐字渲染，累积模式适合需要完整上下文的场景。
- **首字延迟优化**：流式输出的核心价值在于降低首字延迟，建议在面向用户的交互场景中默认开启。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model inference](../guides/model-inference.md)
- [bailian application calling](../guides/bailian-application-calling.md)


