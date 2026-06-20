# 流式输出

流式输出（Streaming）是百炼平台在模型推理和应用调用中提供的一种响应交付方式，服务端在生成过程中将结果分块实时推送给客户端，而非等待全部生成完毕后一次性返回。开启流式输出可显著降低首字延迟，提升用户交互体验。

## 适用场景

流式输出在百炼平台的多个场景中均可使用：

- **应用调用**：智能体和工作流应用的 DashScope API 与 Responses API 均支持流式输出，推荐在对话类应用中默认开启。
- **模型推理**：文本生成模型通过 [OpenAI 兼容接口](openai-compatible.md)或 DashScope 原生接口调用时，均可启用流式输出。
- **实时多模态交互**：Qwen-Omni-Realtime API 基于 WebSocket 协议实现双向流式通信，音频、文本和工具调用参数均以增量方式流式下发。

## 各接口的开启方式

### DashScope API

设置以下参数启用流式输出：

- **Python SDK**：`stream=True` 配合 `incremental_output=True`，响应以迭代器形式逐块返回。
- **Java SDK**：使用 `streamCall()` 方法替代 `call()`。
- **HTTP 调用**：在请求 Header 中添加 `X-DashScope-SSE: enable`，响应以 Server-Sent Events（SSE）格式返回。

### [OpenAI 兼容接口](openai-compatible.md)（Responses API / Chat Completions）

设置 `stream=True` 即可。对于工作流应用，还需在应用的结束节点中启用流式输出开关。

### WebSocket 实时接口

Qwen-Omni-Realtime API 天然基于流式协议，音频通过 `response.audio.delta` 事件增量下发，文本通过 `response.audio_transcript.delta` 事件增量下发，工具调用参数通过 `response.function_call_arguments.delta` 事件增量下发。

## 关键参数

| 参数 | 接口 | 说明 |
|------|------|------|
| `stream` | DashScope API / Responses API | 设为 `True` 开启流式输出 |
| `incremental_output` | DashScope API | 设为 `True` 时每次返回增量内容；设为 `False` 时每次返回累积内容 |
| `X-DashScope-SSE` | DashScope HTTP | 设为 `enable` 以 SSE 格式返回流式响应 |

## 注意事项

- **增量与累积模式**：DashScope API 的 `incremental_output` 参数控制每次推送的内容是增量片段还是从头到当前的累积文本。增量模式更节省带宽，累积模式便于直接展示。
- **工作流应用**：使用 Responses API 调用工作流应用时，需确保应用的结束节点已开启流式输出开关，否则即使设置了 `stream=True` 也不会生效。
- **实时场景**：对于语音对话等低延迟要求极高的场景，建议直接使用基于 WebSocket 的 Qwen-Omni-Realtime API，而非 HTTP SSE 流式输出。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model inference](../guides/model-inference.md)


