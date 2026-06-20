# 流式输出

流式输出（Streaming）是指服务端在生成结果的过程中，将内容以增量方式逐步推送给客户端，而非等待全部生成完毕后一次性返回。在大模型推理场景中，流式输出可以显著降低用户感知的首 Token 延迟，提升交互体验。

## 适用场景

流式输出在百炼平台的多个场景中均可使用：

- **文本生成模型调用**：通过 OpenAI 兼容 Chat Completions、Responses、Anthropic 兼容 Messages 或 DashScope 原生接口调用 Qwen 系列及第三方文本模型时，均支持流式输出。适用于聊天机器人、代码生成、文档处理等需要实时反馈的场景。
- **应用调用**：调用智能体或工作流应用时，DashScope API 和 Responses API 均支持流式输出（Responses API 的异步模式除外）。适用于同步交互场景下需要逐步展示回答的情况。
- **实时多模态交互**：Qwen-Omni-Realtime API 基于 WebSocket 协议天然支持流式通信，音频、文本转录、工具调用结果均以增量事件（delta）形式推送。

## 开启方式

### HTTP 接口（Chat Completions / DashScope）

在请求参数中设置 `stream` 为 `true`，服务端将以 Server-Sent Events（SSE）格式逐步返回生成内容。

**[OpenAI 兼容接口](openai-compatible-interface.md)示例（Python）：**

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**[DashScope SDK](dashscope-sdk.md) 示例（Python）：**

```python
from dashscope import Application

responses = Application.call(
    app_id="APP_ID",
    prompt="你好",
    stream=True
)

for response in responses:
    print(response.output.text, end="", flush=True)
```

### WebSocket 接口（Realtime API）

Qwen-Omni-Realtime API 通过 WebSocket 事件天然实现流式交互，无需额外设置。服务端通过以下事件推送增量内容：

- `response.audio.delta`：音频增量数据
- `response.audio_transcript.delta`：音频转录文本增量
- `response.text.delta`：文本增量
- `response.function_call_arguments.delta`：工具调用参数增量

## 关键参数

| 参数 | 接口 | 说明 |
|------|------|------|
| `stream` | Chat Completions / DashScope | 设为 `true` 开启流式输出 |
| `stream_options.include_usage` | Chat Completions | 设为 `true` 时在最后一个 chunk 中返回 Token 用量统计 |
| `incremental_output` | DashScope 原生接口 | 设为 `true` 时每次仅返回增量内容，否则返回累积内容 |

## 注意事项

- 流式模式下，每个返回的 chunk 包含一个 `delta` 对象（而非完整的 `message`），客户端需自行拼接完整响应。
- 应用调用中，Responses API 的异步模式（`background=true`）不支持流式输出，需通过轮询获取结果。
- 使用流式输出时，错误信息也会以流式事件形式返回，客户端应做好异常处理。
- 流式输出不影响计费方式，Token 消耗与非流式调用相同。

## 来源文档

- 文本生成模型API参考（qwen-api-reference）
- 应用调用（application-call）
- 实时多模态交互 API（omni-realtime-api）
- 模型推理（model-inference）
- 工具与框架兼容性（toolkits-and-[frameworks](../api/frameworks.md)）

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model inference](../guides/model-inference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


