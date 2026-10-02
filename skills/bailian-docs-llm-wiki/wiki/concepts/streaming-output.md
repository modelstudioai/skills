# 流式输出

流式输出（Streaming Output）是指模型推理结果以增量、分块的方式持续返回，而非等待整个响应生成完毕后一次性返回。它通过建立持久化连接（如 WebSocket 或 HTTP/1.1 的 `text/event-stream`），将文本、音频等输出内容按 token、字节或语义单元实时推送，显著降低端到端延迟，提升用户交互沉浸感。

## 在百炼平台的不同场景中，这个概念如何使用

- **Realtime API（实时语音/视频交互）**：基于 WebSocket 双向流，服务端在收到音频/视频帧后即开始生成，并通过 `output.text.delta`、`output.audio.delta` 等事件逐帧推送文本片段或音频 PCM/WAV 数据，支持说话人分离、中断检测等低延迟交互能力。
  
- **应用组件 API（RESTful 文本生成）**：通过设置 `stream=True` 发起 HTTP 请求，服务端返回 `Content-Type: text/event-stream` 响应，客户端按 SSE（Server-Sent Events）协议解析 `data:` 行，逐个获取 `delta` 类型的 token 增量（如 `"delta": "今天"` → `"delta": "天气"` → `"delta": "很好"`）。

- **Application Support（应用层集成）**：在构建对话机器人、RAG 应用或智能体时，启用 `stream=True` 和 `incremental_output=True` 可获得真正增量式输出（即每次只返回本次新增内容，非全量重传），便于前端实现打字机效果、实时高亮、流式 TTS 合成等体验。

- **Omni Realtime API（多模态实时交互）**：支持文本 + 合成语音联合流式输出，`modalities: ["text", "audio"]` 时，服务端同步推送 `output.text.delta` 和 `output.audio.delta` 二进制音频块，开发者可并行渲染文本与播放音频，实现唇音同步级响应。

- **框架集成（LlamaIndex / Spring AI）**：`DashScopeLLM` 等封装组件原生支持 `stream=True` 参数，调用时自动处理 SSE 解析与 token 流聚合，开发者只需注册回调函数即可处理每个增量，无需手动解析 HTTP 流。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 注意事项 |
|------|----------|------|------|-----------|
| `stream` | 应用组件 API、框架集成、Application Support | `bool` | 启用流式响应模式 | 必须设为 `true` 才触发流式行为；默认为 `false`（同步模式） |
| `incremental_output` | Application Support | `bool` | 启用增量式（delta-only）输出 | 若为 `false`，部分接口可能返回全量覆盖文本（如 `output.text` 字段重复刷新），推荐始终设为 `true` |
| `max_output_tokens` / `max_tokens` | Realtime API、Omni Realtime API、应用组件 API | `integer` | 限制单次响应最大生成 token 数 | 超出后服务端主动终止流；不同 API 默认值与上限不同（如 Realtime API 为 4096，Omni Realtime 可达 65536） |
| `enable_interruption` | Realtime API | `boolean` | 是否允许用户语音打断当前输出流 | 设为 `false` 时，即使用户开口，服务端仍继续完成当前响应流，适用于播报类场景 |
| `audio.output.format` | Omni Realtime API | `object` | 指定合成语音输出格式（如 `{"type": "wav", "sample_rate": 24000}`） | 影响音频流的 chunk 大小与解码方式，需与前端播放器兼容 |

> ⚠️ 注意：`temperature`、`top_p` 等采样参数在 Realtime API 中**不可配置**（服务端固定策略），而在应用组件 API 和 Omni Realtime API 中部分模型支持（如 Qwen3.8-Omni-Flash-Realtime），但 Qwen-Omni-Turbo 系列完全忽略这些参数。

## 面向开发者，简洁实用

- ✅ **首选流式**：只要前端支持（浏览器 `EventSource`、移动端 WebSocket 客户端、CLI 工具），一律优先启用 `stream=True`，避免用户长时间白屏等待。
- ✅ **增量即 delta**：`incremental_output=True` 是实现“打字机效果”的关键——每次只取 `delta` 字段拼接，不依赖 `text` 全量字段。
- ✅ **错误容错**：流式连接可能因网络、超时（Realtime API 单连接最长 300 秒）中断，务必实现重连逻辑与会话状态恢复（如通过 `session_id` 或上下文快照续传）。
- ✅ **性能提示**：Realtime API 要求音频帧严格为 `signed-16-bit little-endian, 16kHz`；应用组件 API 流式响应的首 token 延迟（Time to First [Token](token.md), TTFT）通常 < 800ms（取决于模型与输入长度）。
- ❌ **避免混用**：不要在同一个请求中同时开启 `stream=True` 和尝试读取同步响应体（如 `response.json()`），会导致解析失败；流式必须按 SSE 或 WebSocket 协议解析。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application component api reference](../api/application-component-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)
- [frameworks](../api/frameworks.md)


