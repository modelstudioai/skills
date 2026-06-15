# 流式输出

流式输出（Streaming Output）是指服务端在生成结果的过程中，将数据分片逐步推送给客户端，而非等待全部生成完毕后一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、音乐生成和实时多模态交互等场景，显著降低用户感知的首次响应延迟。

## 流式输出的核心价值

- **降低首包延迟**：客户端无需等待完整结果即可开始渲染或播放，用户体验更流畅。
- **支持大体量内容**：长文本、长音频等场景下，流式传输可避免单次响应体过大导致的超时或内存压力。
- **实时交互基础**：在语音对话、实时 TTS 等场景中，流式输出是实现低延迟双向通信的必要机制。

## 在百炼平台不同场景中的使用方式

### 文本生成（Qwen 大模型）

通过 [OpenAI 兼容接口](openai-compatible-api.md)或 DashScope 原生接口调用 Qwen 系列模型时，设置 `stream: true` 即可启用流式输出。服务端以 SSE（Server-Sent Events）协议逐 token 推送生成内容，每个事件包含增量文本片段，最终事件通过 `finish_reason: stop` 标识生成结束。

### 语音合成（TTS）

百炼平台的语音合成支持两种流式输出方式：

- **Qwen-TTS 非实时 API**：通过 HTTP REST 接口调用时，支持流式输出模式，服务端分片返回音频数据。
- **Qwen-TTS-Realtime / CosyVoice**：基于 WebSocket 协议的实时合成，客户端流式发送文本，服务端流式返回音频 PCM/WAV/MP3 数据片段，适用于低延迟实时播报场景。

### 语音识别（ASR）

实时语音识别（Fun-ASR、Paraformer、Qwen-ASR）天然采用流式模式：客户端持续发送音频流，服务端通过 WebSocket 持续推送识别中间结果与最终结果（以 `sentence_end: true` 标识句尾）。

### 音乐生成（Fun-Music）

请求时添加 `X-DashScope-SSE: enable` 请求头即可启用 SSE 流式输出。中间消息通过 `output.audio.data` 返回 Base64 编码的音频片段（`finish_reason` 为 `"null"`），最终消息通过 `output.audio.url` 返回完整音频下载链接并附带歌词等元信息（`finish_reason` 为 `stop`）。

### 实时多模态交互（Omni-Realtime）

Qwen-Omni-Realtime API 通过 WebSocket 实现全双工流式交互。服务端以 `response.audio.delta` 事件流式返回 24 kHz PCM 音频，同时通过 `response.text.delta` 等事件流式返回文本转录和推理结果。

## 关键参数和配置

| 场景 | 协议 | 启用方式 | 数据格式 |
| --- | --- | --- | --- |
| 文本生成 | HTTP SSE | 请求体设置 `stream: true` | 增量文本 token |
| 音乐生成 | HTTP SSE | 请求头 `X-DashScope-SSE: enable` | Base64 音频片段 |
| 语音合成（非实时） | HTTP | SDK 参数或 `stream: true` | 音频数据分片 |
| 语音合成（实时） | WebSocket | 建立连接即为流式 | PCM/WAV/MP3 音频帧 |
| 语音识别 | WebSocket | 建立连接即为流式 | JSON 识别结果 |
| 多模态实时 | WebSocket | 建立连接即为流式 | 音频 PCM + 文本 JSON |

## 开发注意事项

- **SSE 流式输出**需客户端支持逐行解析 `data:` 前缀的事件流，推荐使用官方 SDK 而非手动解析。
- **WebSocket 流式输出**的音频数据通常为原始 PCM 格式，客户端需按指定采样率（如 16 kHz 输入、24 kHz 输出）正确解码和播放。
- 流式输出过程中如遇错误，服务端会通过 `error` 事件或 HTTP 错误状态码通知，客户端应做好异常处理和重连逻辑。
- 部分模型和接口对流式与非流式模式下的输入参数限制不同（如 Fun-Music 歌词长度限制），请参考各 API 文档确认。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [qwen api reference](../api/qwen-api-reference.md)


