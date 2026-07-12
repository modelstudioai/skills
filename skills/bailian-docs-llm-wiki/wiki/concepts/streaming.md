# 流式输出

流式输出（Streaming）是指服务端在生成内容的过程中，将结果以增量（delta）方式分片实时返回给客户端，而非等待全部内容生成完毕后一次性返回。它能显著降低首字延迟、提升长文本和实时交互场景的体验。

## 在百炼平台的使用场景

百炼平台的多类接口都支持流式输出，但触发方式和传输协议因场景而异：

### 应用调用（智能体 / 工作流）

无论是 OpenAI 兼容的 Responses API 还是 DashScope API，调用智能体和工作流应用时都支持流式输出。在 Responses API 中，通过在请求体中设置 `stream=true` 开启，服务端会以 SSE（Server-Sent Events）形式持续推送增量结果，适用于对话类实时交互场景。

### 文本生成模型（Qwen 系列）

Qwen 系列文本生成模型的各类接口（OpenAI 兼容 Chat Completions / Responses、Anthropic 兼容 Messages、DashScope 原生）普遍支持 `stream` 参数。从 OpenAI / Anthropic 迁移时，应先确认目标模型在对应兼容接口下是否支持 `stream` 等参数，再决定接口选型。兼容接口的流式字段与官方客户端保持一致，可直接复用现有 SDK 与示例代码。

### 实时[多模态](multimodal.md)交互（Omni-Realtime API）

Qwen-Omni-Realtime API 基于 WebSocket 协议，本身就是全程流式的低延迟音视频对话接口。它不通过一次性的 `stream` 开关，而是通过一系列增量事件持续收发数据：

- 客户端事件：`input_audio_buffer.append`（追加音频）、`response.create`（触发生成）等。
- 服务端事件：`response.audio.delta`（增量音频输出）、`response.audio_transcript.delta`（增量文本转录）、`conversation.item.input_audio_transcription.delta`（实时语音识别中间结果），最终以 `response.done` 标记响应完成。

## 关键参数与配置

| 场景 | 开启 / 控制方式 | 传输协议 |
|------|----------------|----------|
| Responses API（应用/模型） | 请求体 `stream=true`（默认 `false`） | SSE |
| DashScope API | 设置流式参数 / 使用 SDK 的流式调用方法 | SSE |
| OpenAI / Anthropic 兼容接口 | 请求体 `stream=true` | SSE |
| Omni-Realtime API | 无开关，通过 `response.*.delta` 事件流持续推送 | WebSocket |

补充说明：

- **默认关闭**：文本类接口的 `stream` 默认为 `false`，需显式开启才会分片返回。
- **增量拼接**：流式响应返回的是增量片段，客户端需按到达顺序拼接为完整内容。
- **结束标志**：SSE 场景通常以结束标记（如 `[DONE]`）收尾；Realtime 场景以 `response.done` 事件表示单轮响应结束。
- **与异步调用的区别**：流式输出是"边生成边返回"的实时推送；异步调用（`background=true`）是先返回任务 ID 再轮询结果，二者面向不同的时延与任务类型，不要混淆。

## 面向开发者的实用建议

- 实时对话、长文本生成优先使用流式输出以降低首字延迟。
- 使用 SDK 时优先调用其封装好的流式迭代接口，避免手动解析 SSE 分片。
- 音视频等实时交互场景直接采用 Omni-Realtime 的 WebSocket 事件流，并处理好语音打断（VAD）与增量音频的实时播放。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)



