# 流式输出

流式输出（Streaming Output）是百炼平台中一种实时、增量返回模型推理结果的响应机制，允许客户端在模型生成过程中逐段接收 token、文本片段、音频帧或结构化事件，而非等待整个响应完成后再一次性返回。该机制显著降低端到端延迟，是实现实时语音交互、长文本渐进渲染、低延迟多模态协同等场景的核心能力。

## 在百炼平台的不同场景中如何使用

- **Realtime API（WebSocket 实时双向接口）**：默认启用流式输出，服务端以帧（frame）为单位推送 `output.text.delta`（文本 token 增量）、`output.audio.chunk`（音频 PCM 分片）等事件；客户端需按序拼接 delta 并实时渲染，支持中断、暂停等控制指令注入。
- **Omni Realtime API（多模态实时接口）**：基于统一事件模型，流式响应通过 `output_text_delta`、`output_audio_chunk`、`output_image_preview` 等事件持续推送；`stream=false` 可显式禁用（不推荐），此时仅在会话结束时返回完整结果。
- **Audio API（RESTful 音频接口）**：TTS、ASR、Voice Conversation 等能力支持 `stream=true` 参数，响应格式为 Server-Sent Events（SSE），每行一个 `data: {...}` 事件；非流式则返回标准 JSON 包含 `output.audio_url` 或 `output.text`。
- **Application Call（智能体/工作流调用）**：通过 `stream=true`（OpenAI 兼容模式）或 `X-DashScope-SSE: enable`（DashScope 原生模式）启用；返回 SSE 流，包含 `content` 增量、`tool_calls` 触发事件及状态变更（如 `delta`, `end`, `error`）。
- **Toolkits & Frameworks（[OpenAI 兼容接口](openai-compatible-interface.md)）**：`/chat/completions`、`/vision/chat/completions` 等路径均支持 `stream=true`，行为与 OpenAI 官方一致：返回 `text/event-stream`，含 `data: {"choices":[{"delta":{"content":"..."}}]}` 格式事件；适用于 LangChain、LlamaIndex 等框架的流式回调集成。

## 关键参数和配置

| 接口类型 | 启用方式 | 关键参数/头 | 说明 |
|----------|-----------|--------------|------|
| **Realtime API** | 默认启用 | — | 无需显式配置；流式为协议级强制行为，连接即开始接收增量帧 |
| **Omni Realtime API** | URL 查询参数 | `stream=true`（默认） | 设为 `false` 将退化为单次完整响应，丧失实时性 |
| **Audio API（REST）** | 请求 Body | `"stream": true` | 必须与 `model` 匹配（如 `qwen2-audio-tts-0.5b`）；响应为 SSE，需正确解析 `data:` 行 |
| **Application Call** | DashScope 模式 | Header `X-DashScope-SSE: enable` | 无 body 参数；响应含 `event: message` / `event: tool_call` 等自定义事件类型 |
| | OpenAI 兼容模式 | Body 字段 | `"stream": true` | 标准 OpenAI 格式，支持 `stream_options.include_usage`（v2.4.0+） |
| **Toolkits & Frameworks** | Body 字段 | `"stream": true` | 所有 `/v1/chat/completions` 等兼容接口通用；注意 `qwen3.8-omni-flash` 等多模态模型同样支持 |

> ⚠️ 注意：流式响应不支持 `max_output_tokens` 超限截断后的“优雅终止”——若达到上限，服务端将发送 `finish_reason: "length"` 事件并关闭流；客户端应监听 `finish_reason` 字段判断生成是否完成。

## 面向开发者：简洁实用建议

- **始终处理增量拼接**：`output.text.delta` 或 `choices[0].delta.content` 是片段，非完整句子；需累积至 `finish_reason == "stop"` 才获得终版文本。
- **音频流需严格对齐编解码**：Realtime/Omni 的 `output.audio.chunk` 为 raw PCM（16kHz, 16-bit, mono），直接写入 AudioContext 或播放器前勿做格式转换。
- **错误恢复要重连而非重试**：WebSocket 断连后，必须新建连接 + 新 `session_id`；复用旧 ID 将触发 `session_conflict` 错误。
- **SSE 客户端请设置超时与重连**：Audio/Application 的 REST 流式响应可能因网络中断静默终止，建议设置 `fetch` 的 `signal` 或使用 `EventSource` 并监听 `error` 事件。
- **性能优化提示**：在 Omni Realtime 中，音频输入分片建议 20–200ms；过长分片会引入缓冲延迟；Realtime API 中 `temperature=0` 可减少 token 波动，提升流式稳定性。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [audio api references](../api/audio-api-references.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


