# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种增量式响应机制，服务端在模型推理过程中持续生成并分块返回结果（如 token、音频帧或结构化事件），而非等待全部内容生成完毕后一次性返回。该机制显著降低首字延迟（Time to First [Token](token.md), TTFT），提升用户体验，并支持实时渲染、语音合成、VAD 驱动交互等低延迟场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一能力，而是贯穿多个 API 层级的通用交互范式，具体应用方式因协议与场景而异：

- **RESTful 文本/音频 API**：通过 `stream=true` 参数启用 Server-Sent Events（SSE）流式响应。服务端按 `data: {...}\n\n` 格式逐条推送 `chunk` 事件（含 `delta.content` 或 `delta.text`），客户端需按 SSE 协议解析事件流。适用于标准文本生成、ASR、TTS 等调用，兼容任意 HTTP 客户端。

- **Realtime API（WebSocket）**：基于 WebSocket 的双向事件流，不依赖 `stream` 参数。服务端主动推送 `assistant.message.chunk`（文本 token）、`assistant.audio.chunk`（PCM 音频帧）等细粒度事件，客户端可实时消费、中断（`interrupt`）或暂停（`pause`）。适用于语音对话、实时多轮交互等强实时性场景。

- **Omni Realtime API（WebSocket/QUIC/WebRTC）**：在 Realtime 基础上扩展多模态流式能力。支持 `text` 与 `audio` 混合输出，音频流可配置采样率（8k/16k/24k/48k Hz）与音色；VAD 触发后自动流式提交语音输入，并同步流式返回文本+音频。适用于端到端语音助手、智能座舱、客服系统等复杂交互场景。

- **Prime 模式（高吞吐优化）**：虽为 RESTful 接口，但底层采用加速推理引擎，天然支持更密集的 token 流（更高 tokens/sec）。流式响应中可区分 `delta.reasoning_content`（思考过程）与 `delta.content`（最终回答），便于前端分层渲染。

> ⚠️ 注意：流式输出需客户端主动适配——RESTful 接口必须处理 SSE；WebSocket 接口必须监听指定事件类型；非流式请求（`stream=false` 或未设）将返回完整 JSON 响应体，不支持增量消费。

## 关键参数和配置

| 参数 | 所属接口 | 类型 | 说明 | 是否必需 |
|------|----------|------|------|-----------|
| `stream` | RESTful（文本生成、音频 API） | boolean | 启用 SSE 流式响应。设为 `true` 时，响应头为 `Content-Type: text/event-stream`，Body 为事件流。 | 是（流式场景） |
| `modalities` | Omni Realtime API | array | 指定输出模态，如 `["text"]` 或 `["text","audio"]`。决定是否生成音频流及对应事件类型。 | 是（Omni 场景） |
| `turn_detection.type` | Omni Realtime API | string | VAD 类型（`server_vad`/`semantic_vad`/`semantic_vad_ec`），直接影响音频输入触发时机与流式响应节奏。 | 否（默认 `server_vad`） |
| `audio.output.format.sample_rate` | Omni Realtime API | integer | 输出音频采样率（Hz），支持 `8000`/`16000`/`24000`/`48000`。影响音频流带宽与质量。 | 否（默认由模型决定） |
| `max_tokens` | 所有流式接口 | integer | 控制单次响应最大 token 数（非硬限，超限触发截断事件）。对流式体验至关重要——过小导致频繁截断，过大增加尾部延迟。建议根据业务需求设置（如对话场景常用 `2048`–`4096`）。 | 否（有默认值） |

> ✅ 最佳实践：  
> - RESTful 流式调用务必设置 `Accept: text/event-stream` 请求头；  
> - WebSocket 流式调用需监听 `assistant.message.chunk`（文本）、`assistant.audio.chunk`（音频）、`assistant.message.done`（完成）等核心事件；  
> - 处理流式音频时，建议缓冲 ≥200ms 数据再送入播放器，避免卡顿；  
> - 流式响应中若含错误（如 `error` 事件），应立即终止消费并重试。

## 面向开发者，简洁实用

- 流式不是“开关”，而是**协议+参数+客户端协同**的结果：REST 用 `stream=true` + SSE 解析；WebSocket 用事件监听 + 状态管理。
- 不同接口的流式语义不同：REST 流是“内容分块”，Realtime/Omni 流是“事件驱动”，Prime 流是“高密 token 流”——请严格按对应文档实现。
- 调试流式请求时，优先使用 `curl -N`（禁用缓存）或专用 SSE 客户端（如 `sse-cli`），避免浏览器或 SDK 自动聚合事件。
- 生产环境务必实现流式超时、断连重连、事件丢失检测（如检查 `event_id` 连续性）等健壮性逻辑。
- 计费按实际生成 token 数或音频时长计算，与是否流式无关；但流式可降低客户端内存占用与用户等待感，间接优化成本体验比。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [audio api references](../api/audio-api-references.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


