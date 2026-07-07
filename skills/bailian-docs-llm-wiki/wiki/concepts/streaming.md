# 流式输出

流式输出（Streaming）是指模型在生成过程中逐步返回部分结果，而非等待全部生成完毕后一次性返回。该机制显著降低了用户感知的首字延迟，适用于需要实时展示生成内容的交互场景。

## 工作原理

在非流式模式下，客户端发送请求后需等待模型完成全部推理，才能收到完整响应。流式模式下，服务端通过 Server-Sent Events（SSE）或 WebSocket 将生成结果拆分为多个数据块（chunk）逐个推送，客户端可边接收边渲染，实现打字机效果。

## 适用场景

百炼平台在多个层面支持流式输出：

- **模型 API 调用**：通过 OpenAI 兼容的 Chat Completions 接口或 DashScope 原生接口调用 Qwen 系列模型时，均可启用流式输出。
- **应用调用**：通过 Responses API（OpenAI 兼容模式）或 DashScope API 调用智能体应用和工作流应用时，支持流式返回生成内容。
- **实时[多模态](multimodal.md)交互**：Qwen-Omni-Realtime API 基于 WebSocket 长连接实现实时语音/视频对话，本身即为流式交互架构，响应以事件流形式持续推送。

## 关键参数与配置

### HTTP 接口（Chat Completions / DashScope / 应用调用）

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | boolean | 设为 `true` 启用流式输出，默认 `false` |
| `stream_options.include_usage` | boolean | 设为 `true` 时，流式响应的最后一个 chunk 中包含 token 用量统计 |

### 工作流应用的额外要求

调用工作流应用时，若使用 Responses API 并设置 `stream=true`，需在百炼控制台的工作流编辑器中，对结束节点或流程输出节点启用「流式输出」开关，并重新发布应用，否则流式不会生效。

### 实时[多模态](multimodal.md)接口（WebSocket）

Qwen-Omni-Realtime API 的响应天然以事件流形式返回，无需额外设置 `stream` 参数。服务端通过 `response.audio.delta`、`response.text.delta` 等事件持续推送音频和文本增量数据。

## 使用示例

### Python（OpenAI 兼容 Chat Completions）

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "介绍一下流式输出的原理"}],
    stream=True,
    stream_options={"include_usage": True}
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Python（DashScope 应用调用）

```python
from dashscope import Application
import os

responses = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你好",
    stream=True
)

for response in responses:
    if response.output and response.output.text:
        print(response.output.text, end="", flush=True)
```

## 注意事项

- [异步调用](async-invocation.md)（`background=true`）与流式输出互斥，不能同时启用。
- 流式模式下，每个 chunk 的 `finish_reason` 字段为 `null`，仅最后一个 chunk 返回 `stop` 或其他终止原因。
- 使用流式输出时，建议客户端实现超时和断线重连机制，以应对网络不稳定情况。
- 不同兼容接口（OpenAI Chat Completions、Responses、Anthropic Messages、DashScope）均支持 `stream` 参数，用法一致。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


