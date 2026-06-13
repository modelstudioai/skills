# 流式输出

流式输出（Streaming）是指服务端在生成结果的过程中，将数据分块、逐步推送给客户端的传输方式，而非等待全部结果生成完毕后一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、音乐生成和实时多模态交互等场景，可以显著降低首次响应延迟，提升用户体验。

## 流式输出的两种协议

百炼平台根据不同的接口类型，主要通过以下两种协议实现流式输出：

| 协议 | 适用场景 | 工作方式 |
| --- | --- | --- |
| SSE（Server-Sent Events） | HTTP REST 接口（文本生成、语音合成非实时、音乐生成等） | 客户端发起 HTTP 请求后，服务端通过 SSE 持续推送事件流，每个事件包含一个数据片段 |
| WebSocket 事件流 | 实时交互接口（Omni-Realtime、Qwen-TTS-Realtime、ASR 实时识别等） | 全双工通信，服务端通过下行事件（如 `response.audio.delta`）逐帧推送音频或文本数据 |

## 各场景中的流式输出

### 文本生成

通义千问（Qwen）系列模型支持通过 [OpenAI 兼容接口](openai-compatible-api.md)或 DashScope 原生接口进行流式文本生成。开启流式模式后，模型生成的 token 会逐个或分批返回，客户端可以边接收边展示，实现打字机效果。

### 语音合成

- **Qwen-TTS 非实时**：通过 HTTP REST 接口 + SSE 实现流式音频输出，适合对延迟要求不高的短文本合成。
- **Qwen-TTS-Realtime**：基于 WebSocket 的 Realtime API，支持流式文本输入和实时音频输出（全双工），适合低延迟交互场景。提供 ServerCommit 和 Commit 两种模式控制合成节奏。
- **CosyVoice**：通过 WebSocket + `continue-task` 实现实时流式合成。

### 语音识别

Fun-ASR、Paraformer 和 Qwen-ASR 三大实时识别引擎均通过 WebSocket 实现流式结果推送。客户端持续发送音频流，服务端通过 `result-generated` 事件持续推送中间识别结果和最终结果（`sentence_end=true`）。

### 实时多模态交互

Qwen-Omni-Realtime API 通过 WebSocket 实现音频、文本和图像的实时流式交互。服务端通过 `response.audio.delta` 等事件逐帧推送音频数据，客户端通过 `input_audio_buffer.append` 持续发送音频流。

### 音乐生成

Fun-Music API 支持 SSE 流式输出模式。请求时设置 `X-DashScope-SSE: enable` 请求头即可启用。流式模式下，中间消息通过 `output.audio.data` 返回 Base64 编码的音频片段，最终消息通过 `output.audio.url` 返回完整音频文件的下载链接。

## 关键参数与配置

### SSE 流式输出

- 请求头中设置 `X-DashScope-SSE: enable` 启用流式模式。
- 流式响应中每个事件以 `data:` 前缀标识，包含 JSON 格式的增量数据。
- `finish_reason` 字段用于判断流是否结束：值为 `"null"` 表示中间片段，值为 `stop` 表示生成完毕。

### WebSocket 流式输出

- 通过事件驱动模型实现，客户端和服务端各有一套定义好的事件类型。
- 音频数据通常以 Base64 编码的 PCM 格式传输，输入采样率一般为 16 kHz，输出采样率一般为 24 kHz。
- VAD（语音活动检测）相关参数可控制流式交互的灵敏度和响应时机，如 `silence_duration_ms`（静音触发阈值）和 `threshold`（检测灵敏度）。

## 开发建议

- 对于文本生成和简单音频生成场景，优先使用 SSE 流式模式，实现简单且兼容性好。
- 对于实时语音交互场景（如语音助手、智能客服），使用 WebSocket 全双工流式通信可获得最低延迟。
- 流式输出下需注意处理中间结果与最终结果的区分逻辑，避免重复消费数据或遗漏最终结果。
- 在网络不稳定的环境中，建议实现断线重连和数据校验机制，确保流式数据的完整性。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [music generation references](../api/music-generation-references.md)


