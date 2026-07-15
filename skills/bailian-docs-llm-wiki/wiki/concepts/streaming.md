# 流式输出

流式输出（Streaming）是指服务端在生成内容的过程中，以增量分片（delta）的方式持续返回结果，而非等待全部内容生成完毕后一次性返回。它能显著降低首字延迟、改善实时交互体验，广泛用于对话、语音助手等场景。

## 在百炼平台的使用场景

百炼平台在多类接口中都支持流式输出，核心场景包括：

- **应用调用（Application Call）**：无论是 OpenAI 兼容的 Responses API 还是 DashScope 原生 API，调用智能体或工作流应用时均支持流式输出，可用于需要边生成边展示的实时交互场景。
- **文本生成模型 API**：OpenAI 兼容 Chat Completions / Responses、Anthropic 兼容 Messages 以及 DashScope 原生接口均可开启流式返回，适合聊天补全类应用逐字/逐段渲染输出。
- **实时多模态交互（Omni-Realtime API）**：基于 WebSocket 协议，流式是其原生工作方式。服务端通过一系列增量事件持续推送音频与文本，天然适配低延迟的语音对话场景。

## 关键参数与配置

### HTTP / SDK 接口

- **`stream`**：布尔值，控制是否开启流式输出，默认 `false`。设为 `true` 后，服务端以 SSE（Server-Sent Events）方式逐片返回结果。
  - 适用于 OpenAI 兼容 Responses API、DashScope API 等应用调用与模型调用接口。
- 使用 SDK 时，开启 `stream=true` 后通过迭代响应对象逐步获取增量内容；部分接口可配合 `stream_options` 等参数控制是否返回用量统计等附加信息（以对应接口文档为准）。

### Omni-Realtime（WebSocket）

实时接口不使用 `stream` 参数，而是以事件流的形式天然流式返回。关键的增量事件包括：

| 事件 | 含义 |
| --- | --- |
| `response.audio.delta` | 增量音频输出 |
| `response.audio_transcript.delta` | 增量文本转录 |
| `conversation.item.input_audio_transcription.delta` | 实时语音识别中间结果 |
| `response.done` | 本轮响应流结束 |

此外，可通过 `session.update` 事件中的 `smooth_output`（部分模型支持）等参数调节流式输出的平滑度。

## 开发建议

- **注意结束标志**：SSE 流需处理到结束标记（如 `[DONE]`）或 `response.done` 事件后再收尾，避免内容截断。
- **增量拼接**：客户端需将各 delta 分片按序拼接，才能得到完整结果。
- **错误处理**：流式过程中仍可能收到错误事件，需在读取流的循环中做好异常捕获与连接重试。
- **跨接口差异**：不同接口的分片结构与字段命名不同（OpenAI/Anthropic 兼容接口以对应生态约定为准，DashScope 参数最全），跨接口迁移时需核对字段映射。

## 关联主题页

- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)


