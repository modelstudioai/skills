# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成结果过程中持续、分块地将内容（如文本 token、音频帧或结构化事件）逐段返回给客户端，而非等待全部推理完成后再一次性返回完整响应。该机制显著降低端到端延迟，提升用户交互沉浸感，是构建低延迟对话机器人、实时语音助手、长文本生成等场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用调用（`application call`）**：通过 `stream=true` 参数启用流式模式，配合 `incremental_output=true` 可获得增量式 delta 输出（即每块仅含本次新增内容），适用于智能体/工作流的对话流式渲染与前端打字机效果实现。
- **Qwen 模型 API（`qwen api reference`）**：所有协议（OpenAI 兼容、Anthropic、DashScope 原生）均支持 `stream=true`，返回 `text/event-stream` 格式 SSE 响应；流式下每个 `data:` 行包含 `delta.content` 或 `finish_reason` 字段，便于前端实时拼接与状态判断。
- **应用组件 API（`application component api reference`）**：`/v1/apps/{app_id}/chat` 等接口支持 `stream=true`，响应为标准 SSE；需按 `data:` 行解析，重点关注 `delta`（增量文本）、`finish_reason`（停止原因）及 `usage`（最终 token 统计）事件。
- **Realtime API（`realtime api user guide`）**：面向音视频实时交互，流式是默认行为（无需显式设 `stream`），通过 AOQ/WebRTC/WebSocket 协议实现毫秒级音频流与文本流同步下发，支持 `response.text.delta` 和 `response.audio.delta` 事件分离处理。
- **Omni Realtime API（`omni realtime api`）**：基于 WebSocket 的事件驱动流式接口，客户端通过 `session.update` 配置 `modalities: ["text", "audio"]` 后，服务端持续推送 `response.text.delta`、`response.audio.delta`、`response.tool_use` 等细粒度事件，支持语义级 VAD 触发与工具调用流式协同。
- **第三方客户端集成（`use chat client or development tool`）**：Cursor、Hermes Agent、Postman（需手动配置）等工具均可通过设置 `stream=true` 启用流式，响应格式遵循 OpenAI SSE 规范（`data: {"delta": {"content": "..."}}`），开发者需在 SDK 或前端代码中实现事件解析与 UI 更新逻辑。

## 关键参数和配置

| 参数 | 类型 | 说明 | 使用位置 |
|------|------|------|----------|
| `stream` | `boolean` | 是否启用流式响应。设为 `true` 时，HTTP 响应头为 `Content-Type: text/event-stream`，响应体为 SSE 格式。 | 所有 API（HTTP 请求体或 SDK 参数） |
| `incremental_output` | `boolean` | **仅应用调用支持**。控制流式输出是否为增量形式（`true`）或全量覆盖形式（`false`）。推荐始终设为 `true`，便于前端增量渲染。 | `application call` 的 `parameters.incremental_output` 字段 |
| `X-DashScope-SSE: enable` | HTTP Header | **仅 DashScope 原生协议 HTTP 调用需显式设置**。用于标识流式请求，替代 `stream=true` 在请求体中的位置。 | `application call` / `qwen api reference`（DashScope 协议） |
| `streamCall()` / `stream=True` | SDK 方法/参数 | 各语言 SDK（Python/Java/JS）提供的流式调用封装方法，自动处理连接、解析与事件分发。 | 所有 SDK 接入方式 |

> ⚠️ 注意：流式响应超时统一为 **60 秒**（应用组件 API 明确声明；其他场景未明示但遵循平台默认策略）。超时将关闭连接并返回 `504 Gateway Timeout`，建议客户端实现重连与断点续传逻辑。

## 面向开发者，简洁实用

- ✅ **必做**：启用流式时，务必使用支持 SSE 解析的 HTTP 客户端（如 `fetch` + `ReadableStream`、`axios` + `onDownloadProgress`、或百炼官方 SDK）；避免用 `JSON.parse()` 直接解析整个响应体。
- ✅ **推荐**：前端渲染时，对每个 `delta.content` 追加显示，并监听 `finish_reason` 判断生成结束（值为 `"stop"`、`"length"`、`"tool_calls"` 等）；流式下 `usage` 字段仅在最后一条事件中出现。
- ✅ **调试技巧**：用 `curl -N` 或 Postman（开启 Stream）直接测试流式接口，观察原始 `data:` 行输出，快速验证服务端行为。
- ❌ **避免**：在流式请求中混用非流式参数（如 `stream=false` 与 `X-DashScope-SSE` 共存）；不要假设流式响应顺序绝对严格（尤其[多模态](multi-modal.md)混合输出时，`text` 与 `audio` 事件可能交错）。
- 📌 **性能提示**：流式不降低模型计算开销，但可显著改善用户体验延迟（首 token 时间 TTFB 更关键）。如需优化首 token 延迟，请优先选用 `qwen-turbo`、`qwen3.6-flash` 等轻量模型，并确保 `workspace` 地域与客户端就近部署。

## 关联主题页

- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application component api reference](../api/application-component-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


