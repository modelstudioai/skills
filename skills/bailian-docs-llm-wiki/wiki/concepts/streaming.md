# 流式输出

流式输出是指服务端在生成结果的过程中，将数据分片（chunk）逐步推送给客户端，而非等待全部生成完毕后一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、语音识别、语音翻译和音乐生成等场景，用于降低首字/首帧延迟、提升用户交互体验。

## 百炼平台中的流式输出方式

百炼平台根据不同的接口协议提供三种流式输出机制：

### SSE（Server-Sent Events）

基于 HTTP 长连接的单向推送协议，适用于文本生成和音乐生成等场景。

- **文本生成**：通过 OpenAI 兼容 Chat Completions 接口设置 `stream: true`，服务端以 SSE 事件流返回文本增量。DashScope 原生接口同样支持流式模式。
- **音乐生成**：在请求头中添加 `X-DashScope-SSE: enable` 开启流式输出。中间消息通过 `output.audio.data` 返回 Base64 编码的音频片段，最终消息通过 `output.audio.url` 返回完整音频下载链接，`finish_reason` 从 `"null"` 变为 `"stop"` 标志结束。
- **语音翻译（非实时）**：`stream` 参数必须设为 `true`，模型仅支持流式输出；可通过 `stream_options.include_usage: true` 在最后一个 chunk 获取 Token 用量。

### WebSocket 双向流式

基于 WebSocket 的全双工通信，适用于实时交互场景。客户端持续推送输入数据，服务端实时返回处理结果。

- **实时多模态对话**（Qwen-Omni-Realtime）：客户端通过 `input_audio_buffer.append` 持续推送音频片段，服务端以 `response.audio.delta`、`response.text.delta`、`response.audio_transcript.delta` 等事件逐帧返回音频和文本响应。
- **实时语音合成**（Qwen-TTS-Realtime、CosyVoice、Sambert）：客户端发送文本，服务端流式返回音频数据。
- **实时语音识别**（Qwen-ASR-Realtime、Paraformer-Realtime、Fun-ASR-Realtime）：客户端流式推送 PCM/Opus 音频，服务端实时返回识别结果。
- **实时语音翻译**（Qwen-LiveTranslate-Realtime）：客户端推送音频流，服务端实时返回翻译文本或语音。

### DashScope [异步任务](async-task.md)轮询

视频生成等耗时较长的任务采用异步模式：客户端提交任务获取 `task_id`，再通过轮询或 WebSocket 查询任务状态，最终获取结果 URL。这不是严格意义上的流式输出，但也实现了非阻塞的结果获取。

## 关键参数与配置

| 参数/配置 | 适用协议 | 说明 |
| --- | --- | --- |
| `stream: true` | [OpenAI 兼容接口](openai-compatible-api.md) | 开启 SSE 流式输出 |
| `stream_options.include_usage: true` | [OpenAI 兼容接口](openai-compatible-api.md) | 在流的最后一个 chunk 中返回 Token 用量统计 |
| `X-DashScope-SSE: enable` | DashScope HTTP 接口 | 通过请求头开启 SSE 流式输出 |
| `turn_detection` | WebSocket 实时接口 | 控制 VAD/Manual 模式，决定服务端何时触发流式响应 |
| `modalities` | 多模态接口 | 控制输出模态，如 `["text"]` 或 `["text","audio"]`，影响流式返回的数据类型 |

## 开发注意事项

- SSE 流式输出的每个 chunk 通常只包含增量内容，客户端需自行拼接完整结果。
- WebSocket 流式场景中，需正确处理事件生命周期：关注 `*.delta`（增量数据）和 `*.done`（完成信号）事件的配对关系。
- 北京和新加坡地域使用不同的端点和 API Key，不可混用。新加坡地域应迁移到带 `WorkspaceId` 的新版域名。
- 流式模式下的错误处理同样重要：SSE 流可能因网络中断而截断，WebSocket 需监听 `error` 事件。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [video generation api](../api/video-generation-api.md)


