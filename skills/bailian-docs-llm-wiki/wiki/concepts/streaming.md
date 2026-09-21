# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以连续、分块（chunk）的形式逐步返回给客户端，而非等待整个响应生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知流畅度，是构建实时对话、语音助手、长文本生成等交互式 AI 应用的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中被统一支持，但具体实现方式和适用范围因接口类型而异：

- **Qwen API（OpenAI/Anthropic/DashScope 兼容接口）**：通过 `stream=true` 参数启用。返回符合 Server-Sent Events（SSE）规范的 `text/event-stream` 响应体，每个 `data:` 行包含一个 JSON chunk（如 `{"delta": {"content": "世"}}`），客户端需按行解析并拼接。适用于所有支持文本生成的模型（如 `qwen3.8-max`、`qwen3.7-plus`），但 `Qwen-Audio` 仅在 DashScope 原生接口下支持流式 ASR/TTS。

- **Application Call（智能体/工作流调用）**：支持两种流式模式：  
  - DashScope 原生调用需设置请求头 `X-DashScope-SSE: enable`；  
  - OpenAI 兼容的 `/v1/responses` 接口直接传 `stream=true`。  
  流式响应中可包含工具调用（`tool_use`）、思考过程（`reasoning`）、最终回复（`message`）等多类型事件，便于前端实时渲染执行状态。

- **Omni Realtime API（全模态实时交互）**：基于 WebSocket 协议，天然支持双向流式。服务端主动推送多种事件类型，如 `response.text.delta`（文本增量）、`response.audio.chunk`（TTS 音频分片）、`response.vision.result`（视觉理解结果），无需 SSE 解析，适合低延迟语音+视觉协同场景。

- **Realtime API（多协议实时能力）**：AOQ/WebRTC/WebSocket 三种协议均支持流式，但能力边界不同：  
  - AOQ 支持全模态流式（文本+音频+视频帧）；  
  - WebRTC 支持文本与音频流式，但不支持纯 ASR/TTS 模型；  
  - WebSocket 主要用于 ASR/TTS 类模型的流式语音识别与合成。  
  所有协议均要求客户端按事件类型（如 `audio_chunk`、`transcript`）处理增量数据。

- **Application Component API（应用组件）**：仅 `text-generation` 类接口支持 `stream=true`，返回标准 SSE 格式；知识库检索、工具调用等非生成类组件不支持流式，需同步等待完整结果。

## 关键参数和配置

- **通用开关参数**：  
  - `stream`: `boolean`，全局启用开关，默认 `false`。所有支持流式的接口均接受此参数（Qwen API、Application Call、Application Component API）。  

- **协议级配置**：  
  - DashScope 原生接口（Application Call / Component）：需额外设置请求头 `X-DashScope-SSE: enable` 才能触发流式响应。  
  - Omni Realtime API：无需 `stream` 参数，WebSocket 连接建立后即默认流式通信，通过事件类型区分数据流。  
  - Realtime API（AOQ/WebRTC）：由 SDK 内部管理流式行为，开发者通过 `onAudioChunk`、`onTranscript` 等回调监听，不依赖 HTTP 参数。

- **注意事项**：  
  - `stream=true` 与 `background=true`（异步模式）互斥，不可同时设置；  
  - 流式响应不支持 `max_tokens` 的硬截断（部分模型可能提前终止），建议结合 `stop` 参数控制生成结束；  
  - 客户端必须正确处理 SSE 的重连逻辑（监听 `retry` 字段）、空行分隔、JSON 解析错误及连接中断；  
  - Omni Realtime 和 Realtime API 的流式数据为二进制音频或结构化事件，需按协议文档约定解析，不可直接复用 OpenAI SSE 解析器。

## 面向开发者，简洁实用

- ✅ **推荐开启**：只要前端支持（浏览器/APP/SDK），所有文本生成类请求都应设 `stream=true`，可降低首字延迟（TTFT）50%+，避免超时失败。  
- ✅ **正确解析**：使用成熟 SSE 客户端库（如 `eventsource`、`fetch-event-source`）或 WebSocket SDK，勿手动按 `\n` 切分。  
- ✅ **渐进渲染**：对 `delta.content` 增量追加 DOM 文本，对 `audio.chunk` 实时喂入 Web Audio API，对 `vision.result` 触发 UI 更新。  
- ❌ **避免踩坑**：不要在流式响应中依赖 `usage` 字段（其仅在末尾 chunk 出现）；不要对 `tool_use` 事件做阻塞等待——流式下工具调用与回复可能交错返回；`system` 消息在流式会话中仅首条生效，后续无效。  
- 🚀 **性能提示**：Qwen3.8-omni-flash 系列模型专为流式优化，TTFT < 300ms；若需极致低延迟，优先选用 AOQ 协议 + `qwen3.8-omni-flash-realtime` 模型。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application component api reference](../api/application-component-api-reference.md)


