# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中将结果以增量方式（如逐 token、逐 chunk 或逐事件）持续返回给客户端，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升交互自然度，是语音助手、实时对话、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

- **标准 Chat API（`/v1/chat/completions`）**：通过设置 `stream: true` 启用 SSE（Server-Sent Events）格式的流式响应，适用于网页前端、CLI 工具或兼容 OpenAI 协议的客户端（如 Cursor、Dify）。每条响应为独立 `data:` 行，含 `delta.content` 字段，需客户端拼接还原完整文本。
  
- **Realtime API（WebSocket）**：专为低延迟交互设计，不依赖 HTTP，服务端主动推送 `output` 事件，每个事件携带 `delta`（增量 token）、`finished_reason` 等字段。支持客户端主动发送 `interrupt` 事件中断生成，适用于语音流、视频流等强实时场景。

- **Omni Realtime API（AOQ/WebSocket/WebRTC）**：在多模态流式交互中，同时支持文本 `delta` 和音频流（PCM/WAV 分片）的实时下发。音频输出可配置采样率与格式，文本与语音严格对齐，满足 TTS+ASR 融合应用需求。

- **Application Use Cases（企业集成）**：在钉钉、企微、公众号等平台嵌入 AI 助手时，启用 `stream: true` 可实现“打字机效果”式消息回复；配合 `incremental_output: true` 可避免历史消息重复渲染，提升前端性能。

- **RAG 与插件调用场景**：流式输出与检索增强、工具调用完全兼容。例如，当模型调用搜索插件后，仍可流式返回推理过程与最终答案，无需阻塞等待插件执行完成。

- **开发工具与 SDK 集成**：官方 AOQ SDK（v2.3.0+）自动处理 WebSocket 心跳、重连、分片组装与 `delta` 拼接；OpenAI 兼容 SDK（如 `openai-python`）在 `stream=True` 下可直接复用，无需协议适配。

## 关键参数和配置

| 参数 | 类型 | 说明 | 生效范围 |
|------|------|------|----------|
| `stream` | `boolean` | 启用流式响应。设为 `true` 时，响应头含 `Content-Type: text/event-stream`，体为 SSE 格式。必须由客户端按规范解析。 | 所有基于 `/v1/chat/completions` 的调用（test-1、application [use cases](../guides/use-cases.md)、development tools） |
| `incremental_output` | `boolean` | 仅当 `stream=true` 时有效。控制是否仅返回本次增量内容（`delta`），而非完整 `message.content`。避免前端重复渲染历史部分。 | application [support](../guides/support.md)、application [use cases](../guides/use-cases.md) |
| `max_output_tokens` | `integer` | 流式生成的最大 token 数上限（非总上下文长度）。超出后触发 `stop` 事件并终止流。 | Realtime API、Omni Realtime API |
| `turn_detection.type` / `semantic_vad` | `string` | 在 Omni Realtime 中影响流式音频/文本的断句粒度与响应节奏，间接决定 `delta` 推送频率。 | Omni Realtime API |

> ⚠️ 注意：`stream=true` 要求客户端支持 chunked transfer encoding（HTTP）或正确处理 WebSocket 事件流；不兼容传统同步 JSON 解析逻辑。错误处理需监听 `error` 事件或 `data: [ERROR]` 行。

## 面向开发者：简洁实用提示

- ✅ **推荐做法**：前端优先使用 `incremental_output=true` + `stream=true` 组合，配合防抖渲染，保障流畅体验；  
- ✅ **调试技巧**：用 `curl -N` 或 Postman 的 SSE 插件直测流式接口，观察原始 `data:` 响应；  
- ✅ **错误规避**：Realtime API 单连接最长 300 秒，需在业务层实现会话续接；WebSocket 断连后勿复用旧 `session_id`；  
- ❌ **常见误区**：`stream=true` 不降低单 token 生成延迟，只优化传输与呈现；`max_tokens` 控制总长度，不影响流式行为；  
- 📦 **SDK 选型**：生产环境务必使用 AOQ SDK（Realtime）或最新版 `dashscope` Python SDK（Chat API），避免手动实现 SSE/WebSocket 协议。

## 关联主题页

- [test 1](../guides/test-1.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application use cases](../guides/application-use-cases.md)
- [application support](../guides/application-support.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


