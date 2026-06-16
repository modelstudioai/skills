# 流式输出

流式输出（Streaming Output）是指模型或服务在生成结果的过程中，将数据以增量片段的方式逐步返回给客户端，而非等待全部生成完毕后一次性返回。这种模式显著降低了用户感知的首字延迟，适用于对实时性要求较高的交互场景。

## 在百炼平台中的应用场景

流式输出在百炼平台的多种 API 和服务中广泛使用：

### 文本生成

通义千问（Qwen）系列模型的各类接口（OpenAI 兼容 Chat Completions、DashScope 原生接口等）均支持流式输出。开发者通过设置 `stream` 参数为 `true`，即可让模型在生成过程中逐 token 返回结果，而非等待完整响应。这在聊天对话、长文本生成等场景中尤为重要。

### 语音合成（TTS）

- **Qwen-TTS 非实时 API**：支持流式输出模式，合成过程中分片返回音频数据。
- **CosyVoice 实时语音合成**：通过 WebSocket 协议实现双向流式交互，边接收文本输入边输出合成音频。字级别时间戳功能仅在流式输出模式下可用。
- **CosyVoice 非实时语音合成**：HTTP API 同样支持流式和非流式两种输出模式。

### 实时多模态交互

Qwen-Omni-Realtime API 通过 WebSocket 实现实时语音、文本与图像的流式交互。服务端通过 `response.audio.delta` 等事件流式返回音频片段，`response.text.delta` 流式返回文本转录，实现低延迟的多模态对话体验。

### 语音识别（ASR）

实时语音识别服务（Fun-ASR、Paraformer、Qwen-ASR）通过 WebSocket 协议持续接收音频流并流式返回识别结果，包括中间结果和最终结果（`sentence_end=true`），满足实时转写场景需求。

### 应用调用

百炼平台的智能体应用和工作流应用同样支持流式输出，在调用 `Application.call()` 或 HTTP 接口时启用流式模式，可逐步接收应用的生成结果。

## 关键参数与配置

| 参数/配置 | 适用场景 | 说明 |
|-----------|---------|------|
| `stream` | 文本生成 API | 设为 `true` 开启流式输出，响应以 SSE（Server-Sent Events）格式逐块返回 |
| `incremental_output` | DashScope 文本生成 | 控制流式输出是增量模式（仅返回新增内容）还是全量模式（每次返回完整结果） |
| WebSocket 协议 | 语音合成/识别、实时多模态 | 天然支持双向流式通信，无需额外配置即可实现流式输出 |
| `response_format` | 语音合成流式输出 | 指定输出音频格式（pcm、wav、mp3、opus），影响流式分片大小 |
| SSE | HTTP 流式输出 | 通过 `text/event-stream` 内容类型实现 HTTP 长连接下的流式传输 |

## 实现方式对比

百炼平台根据不同接口协议提供两种流式输出实现：

- **HTTP SSE（Server-Sent Events）**：适用于文本生成、非实时语音合成等 HTTP 接口。客户端建立长连接后，服务端以 `data:` 前缀逐行推送结果片段。
- **WebSocket**：适用于实时语音合成、语音识别、多模态实时交互等场景。支持全双工通信，客户端和服务端可同时收发数据，延迟更低。

## 开发建议

- 对于对话类应用，建议默认启用流式输出以提升用户体验。
- 使用 HTTP SSE 时，注意处理连接中断和重连逻辑。
- 使用 WebSocket 流式输出时，需按协议规范处理各类服务端事件（如 `task-started`、`result-generated`、`task-finished`）。
- 在流式模式下，需在客户端实现结果拼接逻辑，将增量片段组装为完整响应。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [audio api references](../api/audio-api-references.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)



