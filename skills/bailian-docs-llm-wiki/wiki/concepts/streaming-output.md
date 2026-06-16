# 流式输出

流式输出（Streaming Output）是指服务端在生成结果的过程中，将数据分片逐步推送给客户端，而非等待全部生成完毕后一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、音乐生成等多种 API，能够显著降低首次响应延迟，提升用户体验。

## 适用场景

百炼平台中以下场景支持流式输出：

| 场景 | 协议 | 典型用途 |
|------|------|----------|
| 文本生成（Qwen 系列） | HTTP SSE / WebSocket | 逐 token 返回生成文本，适合聊天对话、内容创作 |
| 实时多模态对话（Qwen-Omni-Realtime） | WebSocket 事件流 | 音频、文本实时交替输出，适合语音助手、智能客服 |
| 语音合成（CosyVoice / Qwen-TTS） | WebSocket / HTTP SSE | 边合成边播放音频片段，适合实时播报 |
| 音乐生成（Fun-Music） | HTTP SSE | 音频数据分片返回，支持边生成边试听 |
| 语音识别（Fun-ASR / Paraformer / Qwen-ASR） | WebSocket | 实时推送中间识别结果和最终结果 |

## 实现方式

百炼平台的流式输出主要通过以下两种协议实现：

### SSE（Server-Sent Events）

适用于 HTTP REST 接口。客户端在请求头中添加 `X-DashScope-SSE: enable` 即可启用。服务端通过 SSE 协议持续推送事件，每个事件包含一个数据片段。

以音乐生成为例，流式模式下：
- 中间消息：`output.audio.data` 返回 Base64 编码的音频片段，`finish_reason` 为 `"null"`
- 最终消息：`output.audio.data` 为空，`output.audio.url` 返回完整音频下载地址，`finish_reason` 为 `stop`

### WebSocket 事件流

适用于实时交互场景。服务端通过 WebSocket 连接持续下发事件，客户端按事件类型处理数据。

以 Qwen-Omni-Realtime 为例，音频通过 `response.audio.delta` 事件流式返回 PCM 数据片段，文本通过 `response.text.delta` 事件逐步返回。

## 关键参数与配置

| 参数/配置 | 接口类型 | 说明 |
|-----------|----------|------|
| `X-DashScope-SSE: enable` | DashScope HTTP API | 请求头设置，启用 SSE 流式输出 |
| `stream: true` | [OpenAI 兼容接口](openai-compatible-api.md) | 请求参数，启用流式返回 |
| `incremental_output` | DashScope 文本生成 | 设为 `true` 时每次只返回增量内容，而非累积内容 |
| `word_timestamp_enabled` | 语音合成（CosyVoice） | 设为 `true` 可在流式输出中获取字级别时间戳 |

## 流式输出与非流式输出的对比

| 维度 | 流式输出 | 非流式输出 |
|------|----------|------------|
| 首次响应延迟 | 低（生成即返回） | 高（需等待全部完成） |
| 数据完整性 | 需客户端拼接片段 | 一次获取完整结果 |
| 适用场景 | 实时交互、长内容生成 | 批量处理、短内容 |
| 实现复杂度 | 较高（需处理事件流） | 较低（标准请求-响应） |

## 开发注意事项

- **错误处理**：流式输出过程中可能发生网络中断或服务端错误，客户端应监听错误事件并实现重试逻辑。
- **数据拼接**：文本类流式输出需要在客户端侧拼接各片段；如使用 `incremental_output`，每次返回增量部分，直接追加即可。
- **资源释放**：WebSocket 场景下，流式输出结束后应及时关闭连接，避免资源泄漏。
- **字符限制差异**：部分 API（如音乐生成）在流式和非流式模式下对输入长度的限制不同，需注意查阅对应文档。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [audio api references](../api/audio-api-references.md)
- [music generation references](../api/music-generation-references.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)


