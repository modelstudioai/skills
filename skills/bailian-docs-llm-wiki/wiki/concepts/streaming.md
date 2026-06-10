# 流式输出

流式输出（Streaming）是指模型在生成过程中将结果分片逐步返回给客户端的通信模式，而非等待全部生成完毕后一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、语音识别、音乐生成和应用调用等场景，可显著降低用户感知的首次响应延迟。

## 流式协议类型

百炼平台根据不同场景提供两种流式协议：

| 协议 | 传输层 | 适用场景 | 典型接口 |
| --- | --- | --- | --- |
| SSE（Server-Sent Events） | HTTP | 文本生成、音乐生成、应用调用 | Chat Completions、Fun-Music API、Application API |
| WebSocket | WebSocket | 实时语音合成、实时语音识别、多模态实时对话 | CosyVoice、Qwen-TTS Realtime、Qwen-ASR、Qwen-Omni-Realtime |

SSE 基于标准 HTTP 长连接，客户端发送一次请求后持续接收服务端推送的事件流，适合单向输出场景。WebSocket 提供全双工通信，客户端和服务端可同时收发数据，适合需要持续输入（如音频流）与持续输出的实时交互场景。

## 各场景的流式使用方式

### 文本生成

通过 [OpenAI 兼容接口](openai-compatible-api.md)调用时，设置 `stream: true` 即可启用 SSE 流式输出，模型会逐 token 返回生成内容。DashScope 原生接口同样支持流式模式。

### 语音合成

- **Qwen-TTS 非实时**：通过 HTTP 接口的流式模式，分片返回音频数据。
- **Qwen-TTS Realtime / CosyVoice / Sambert**：基于 WebSocket 协议，客户端通过 `input_text_buffer.append` 追加文本，服务端通过 `response.audio.delta` 事件流式返回 Base64 编码的音频片段，直到 `response.audio.done` 标志合成完成。
- **MiniMax Speech**：支持 HTTP 流式输出，兼容 OpenAI 风格接口。

### 语音识别

实时语音识别天然是流式场景。客户端通过 WebSocket 持续发送音频流，服务端持续推送中间识别结果（`sentence_end=false`）和最终识别结果（`sentence_end=true`）。Fun-ASR、Paraformer 和 Qwen-ASR 三大系列均支持此模式。

### 音乐生成

Fun-Music API 通过在请求头中设置 `X-DashScope-SSE: enable` 启用 SSE 流式输出。启用后，中间消息的 `output.audio.data` 返回 Base64 音频数据片段（`finish_reason` 为 `"null"`），最终消息的 `output.audio.url` 返回完整音频下载链接（`finish_reason` 为 `stop`）。

### 应用调用

DashScope 应用调用 API 通过 `parameters.incremental_output` 参数控制流式行为。启用增量模式后，每次返回的内容仅包含新增部分，而非累积的完整内容，便于客户端实时拼接展示。

## 关键参数与配置

| 参数 / 配置 | 作用 | 适用范围 |
| --- | --- | --- |
| `stream: true` | 启用 SSE 流式输出 | [OpenAI 兼容接口](openai-compatible-api.md)（文本生成） |
| `X-DashScope-SSE: enable` | 通过请求头启用 SSE | DashScope HTTP 接口（音乐生成等） |
| `incremental_output` | 增量输出模式，每次仅返回新增内容 | 应用调用 API |
| WebSocket 事件协议 | 通过事件驱动实现双向流式通信 | 语音合成、语音识别、多模态实时对话 |

## 开发注意事项

- **协议选择**：单向输出（文本、音乐）优先使用 SSE，需要双向实时交互（语音对话、实时转写）使用 WebSocket。
- **增量与全量**：部分接口默认返回累积全量内容，需显式开启增量模式以减少传输冗余。
- **连接管理**：WebSocket 场景需关注连接的生命周期管理，包括心跳保活、异常重连和资源释放。
- **音频编码**：语音类流式输出通常使用 Base64 编码传输 PCM 或 MP3 数据片段，客户端需按顺序拼接解码后播放。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [application call](../api/application-call.md)


