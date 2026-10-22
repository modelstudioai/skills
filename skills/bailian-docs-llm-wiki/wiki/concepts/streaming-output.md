# 流式输出

流式输出（Streaming Output）是指模型服务将生成结果以增量方式、分块推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户体验，尤其适用于长文本生成、实时语音交互、对话界面渲染等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台覆盖文本、音频及实时交互三大类服务，具体应用如下：

- **文本生成类 API（如 Qwen Chat / Responses / Anthropic Messages）**：通过 `stream=true` 启用 SSE（Server-Sent Events）流式响应，服务端按 token 或语义 chunk 逐段返回 `content`，支持前端实现“打字机效果”或渐进式思考展示（如 `thinking` 事件）。

- **音频类 API（ASR/TTS/Voice Conversation）**：在 RESTful 接口上启用 `stream=true`，配合 `Accept: text/event-stream` 请求头，可获得分段识别结果（ASR 的 partial transcript）或分段合成音频（TTS 的 `audio_chunk`）。注意：并非所有音频模型均支持流式，需查阅对应子文档的能力说明表。

- **Realtime API（WebSocket 协议）**：原生流式设计，不依赖 HTTP 流。客户端通过 WebSocket 持续发送音频帧，服务端实时返回 `output.text_delta`（文本增量）、`output.audio_chunk`（PCM 音频块）等事件，实现毫秒级双向流式交互。

- **应用层（Agent / Assistant）**：除基础 `stream=true` 外，支持 `incremental_output=true` 参数，确保每个 event 仅包含本次新增 token（而非从开头累计的全量文本），便于前端精准增量渲染与状态同步。

## 关键参数和配置

| 参数 | 类型 | 说明 | 适用接口 |
|------|------|------|----------|
| `stream` | `boolean` | 必须设为 `true` 以启用流式响应；默认为 `false`（非流式） | 全部支持流式的 API（Qwen Chat/Responses/Anthropic、Audio API、Application API） |
| `incremental_output` | `boolean` | 仅当 `stream=true` 时生效；`true` 表示每个 event 返回增量 token（推荐用于前端拼接）；`false` 表示返回累计全文（兼容旧逻辑） | Application API、Qwen Responses API（部分版本） |
| `Accept` 请求头 | `string` | 必须设置为 `text/event-stream`，否则流式请求将被拒绝或降级为非流式响应 | 所有基于 HTTP 的流式 API（RESTful 类） |
| WebSocket 连接参数 | — | Realtime API 无需 `stream` 参数，但需在 URL 中指定 `model` 和 `api_key`，并通过 `enable_interactive_mode` 控制是否启用细粒度 token 级响应 | Realtime API（WebSocket） |

> ⚠️ 注意：流式能力因模型而异。例如 `Qwen-Audio` 不支持 OpenAI 兼容协议下的流式；`QwQ` 模型不建议设置 `system` 消息，可能影响流式稳定性。务必以各模型文档中的“流式支持说明”为准。

## 面向开发者，简洁实用

- ✅ **必做**：启用流式时，HTTP 请求头必须包含 `Accept: text/event-stream`；WebSocket 场景需严格遵循 `session.start` → `input.audio` → 监听 `output.*` 事件的生命周期。
- ✅ **推荐**：前端消费流式响应时，使用标准 SSE 解析器（如 `EventSource` 或 `fetch + ReadableStream`），并开启 `incremental_output=true` 以避免重复解析全量文本。
- ✅ **调试技巧**：流式响应中每个 `data:` 行是一个 JSON 对象（如 `{"delta": "你好", "finish_reason": null}`），可通过 `curl -N` 或 Postman 的 “Stream response” 开关直观查看原始流。
- ❌ **避坑**：不要在流式请求中省略 `model` 或认证头；不要对非流式支持的模型强行传 `stream=true`（将返回 400 错误）；Realtime API 不接受 `stream` 参数，勿混淆协议类型。
- 📈 **性能提示**：流式不改变计费逻辑——仍按实际生成的 token 数或音频时长计费；但可显著降低首字节时间（TTFB），建议高交互性应用默认启用。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [audio api references](../api/audio-api-references.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


