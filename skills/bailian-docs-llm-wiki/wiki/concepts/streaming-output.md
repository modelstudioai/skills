# 流式输出

流式输出（streaming）是指服务端将模型生成的结果分多次增量返回，而非等全部内容生成完毕后一次性下发。它能显著降低首字延迟、提升实时交互体验，适用于对话、语音等对响应速度敏感的场景。

## 在百炼平台的使用场景

百炼平台在多类接口中都提供了流式输出能力，具体开启方式因协议而异：

- **应用调用（智能体/工作流）**：无论是 OpenAI 兼容的 Responses API 还是 DashScope API，都支持流式输出。以 Responses API 为例，通过在请求中设置 `stream=true` 即可开启，服务端会以增量方式持续返回生成内容。
- **文本生成模型 API**：OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages 以及 DashScope 原生接口均支持流式返回。使用 OpenAI 客户端库时，通常只需替换 base URL 和 API Key，并按对应生态的字段约定开启流式参数。
- **实时多模态交互（Qwen-Omni-Realtime API）**：基于 WebSocket 协议实现天然的流式交互。服务端通过一系列增量事件持续推送结果，例如 `response.audio.delta`（增量音频输出）、`response.audio_transcript.delta`（增量文本转录）、`conversation.item.input_audio_transcription.delta`（实时语音识别中间结果），最终以 `response.done` 表示本轮响应完成。

## 关键参数与配置

| 场景 | 参数/事件 | 说明 |
|------|-----------|------|
| Responses API / Chat Completions | `stream` | 布尔值，是否流式输出，默认 `false`；设为 `true` 开启 |
| DashScope API | 流式开关 | 通过 SDK 的流式调用方式或对应参数开启 |
| Omni-Realtime API | `response.*.delta` 系列服务端事件 | WebSocket 连接下增量推送音频、文本转录等结果 |
| Omni-Realtime API | `response.done` | 标记单轮响应生成结束 |
| Qwen3-Omni-Flash-Realtime | `smooth_output` | 控制输出平滑度的可选参数 |

## 使用建议

- 需要即时反馈、逐字/逐段展示的实时交互（如聊天界面、语音助手）优先启用流式输出。
- 流式模式下需在客户端持续读取并拼接增量片段，直到收到结束标志（HTTP 流的结束或 `response.done` 事件）。
- 流式与异步调用（`background=true`）面向不同需求：流式关注实时增量返回，异步关注长耗时任务的非阻塞执行，二者不要混淆。
- 跨接口迁移时需核对各生态对流式参数的字段约定差异，DashScope 参数最全，OpenAI/Anthropic 兼容接口以对应生态约定为准。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)


