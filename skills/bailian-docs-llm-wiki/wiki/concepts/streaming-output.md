# 流式输出

流式输出是指服务端在生成结果的同时，将数据分片逐步推送给客户端的交互模式。相比等待完整响应一次性返回，流式输出可显著降低首字节延迟，提升用户体验，适用于文本生成、语音合成、语音识别、音乐生成等多种实时场景。

## 百炼平台中的流式输出方式

百炼平台根据业务场景提供两种主要的流式传输协议：

### SSE（Server-Sent Events）

基于 HTTP 长连接的单向流式推送，适用于文本生成和音乐生成等场景：

- **文本生成**：通过 [OpenAI 兼容接口](openai-compatible-api.md)设置 `stream: true`，或通过 [DashScope 接口](dashscope-api.md)启用增量输出，模型逐 token 返回生成内容。
- **音乐生成**：请求头添加 `X-DashScope-SSE: enable`，服务端以 SSE 事件流推送 Base64 音频片段，最终消息包含完整音频 URL。

### WebSocket 双向流式

基于 WebSocket 的全双工通信，适用于需要实时双向交互的音频场景：

- **实时多模态对话（Omni-Realtime）**：客户端持续推送音频/图像帧，服务端实时返回 `response.audio.delta`、`response.text.delta` 等增量事件。
- **实时语音合成（TTS-Realtime / CosyVoice）**：客户端发送文本片段，服务端流式返回合成音频数据。
- **实时语音识别（ASR-Realtime）**：客户端流式上传 PCM/Opus 音频，服务端实时返回识别文本。

## 关键参数与配置

| 协议 | 启用方式 | 适用场景 |
| --- | --- | --- |
| SSE | 请求头 `X-DashScope-SSE: enable` 或请求体 `stream: true` | 文本生成、音乐生成 |
| WebSocket | 连接 `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | 语音合成、语音识别、多模态实时对话 |

### SSE 流式输出要点

- 每个 SSE 事件以 `data:` 前缀发送 JSON 负载
- 中间消息的 `finish_reason` 为 `null`，最终消息为 `stop`
- 客户端需逐行解析事件流并拼接增量内容

### WebSocket 流式输出要点

- 连接建立后通过 `session.update` 配置会话参数
- 音频数据以 Base64 编码的 PCM 片段传输（`input_audio_buffer.append`）
- 服务端通过 `*.delta` 事件推送增量数据，通过 `*.done` 事件标记完成
- 支持 VAD（语音活动检测）自动切分和手动提交两种模式

## 开发建议

- 对延迟敏感的交互场景（对话、语音通话）优先使用 WebSocket 流式接口
- 对实现简单性要求高的场景（文本生成、离线音频）可使用 SSE 模式
- 流式输出中需关注错误事件处理，及时释放连接资源
- 不同地域（北京 / 新加坡）的端点和 API Key 不通用，需分别配置

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [music generation references](../api/music-generation-references.md)


