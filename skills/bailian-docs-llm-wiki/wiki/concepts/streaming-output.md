# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在推理过程中将生成结果以增量方式分块（chunk）返回，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话类、语音交互、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台的多个 API 层级和产品形态中统一支持，但协议、触发方式与消费方式略有差异：

- **Application Call（应用调用 API）**：通过 `stream=true` 参数启用，响应遵循 Server-Sent Events（SSE）协议；配合 `incremental_output=true` 可确保每个 chunk 仅包含新增 token（避免历史内容重复返回），适用于 Web 控制台、聊天前端等需逐字渲染的场景。
- **Application Component API（应用组件 API）**：在 `chat` 接口（如 `/apps/{app_id}/chat`）中设置 `stream=true`，同样采用 SSE 格式返回 `data: {...}` 消息流，便于集成至标准 HTTP 客户端（如 `fetch` + `ReadableStream`）。
- **Realtime API（实时 API）**：**强制流式**（`stream` 固定为 `true`），基于 WebSocket 协议实现双向低延迟通信；除文本外，还支持 `audio_output`、`video_output` 等多模态增量流，适用于语音助手、实时会议转录等强实时场景。
- **Omni Realtime API（多模态实时 API）**：同样基于 WebSocket，支持 `text_delta` 和 `audio_chunk` 的混合流式输出，并可通过 `turn_detection` 和 `server_vad` 实现语义级流控，满足端到端语音交互需求。
- **应用内调试与控制台预览**：在百炼控制台「应用测试」面板中，开启「流式响应」开关后，可实时观察模型 token 生成过程，辅助效果调优与问题定位。

> ⚠️ 注意：所有流式接口均**不兼容传统同步 JSON 响应解析逻辑**。客户端必须按对应协议（SSE 或 WebSocket）处理事件流，否则将导致解析失败或超时。

## 关键参数和配置

| 参数名 | 类型 | 默认值 | 说明 | 适用范围 |
|--------|------|--------|------|----------|
| `stream` | boolean | `false` | 启用流式输出。设为 `true` 后，响应头含 `Content-Type: text/event-stream`（SSE）或建立 WebSocket 连接（Realtime）。 | 全部 API（Application Call、Component、Realtime、Omni Realtime） |
| `incremental_output` | boolean | `false` | **仅 DashScope API 支持**。当 `stream=true` 时，若设为 `true`，每个 chunk 的 `output.text` 为本次新增内容（增量）；若为 `false`，则为当前完整输出（全量追加）。推荐生产环境始终启用。 | Application Call（DashScope 路径） |
| `flow_stream_mode` | string | — | 工作流流式模式，推荐使用 `message_format_plus`（带角色、状态字段）或 `message_format`；避免使用已废弃的 `full_thoughts`。 | Application Call（旧版工作流） |

- **SSE 流式响应结构示例（Application Call / Component）**：
  ```text
  data: {"output":{"text":"Hello"},"usage":{},"request_id":"xxx"}
  data: {"output":{"text":" world"},"usage":{},"request_id":"xxx"}
  data: {"output":{"text":"!"},"usage":{},"request_id":"xxx"}
  data: [DONE]
  ```
- **WebSocket 流式事件示例（Realtime / Omni Realtime）**：
  ```json
  { "event": "response.text_delta", "data": { "delta": "Hello" } }
  { "event": "response.text_delta", "data": { "delta": " world" } }
  { "event": "response.audio_output", "data": { "chunk_id": "abc123", "bytes": "..." } }
  ```

## 面向开发者：简洁实用建议

- ✅ **必做**：流式调用前务必检查客户端是否支持对应协议（浏览器 `EventSource` / `fetch().body.getReader()` 用于 SSE；`WebSocket` 或 AOQ SDK 用于 Realtime）。
- ✅ **推荐**：始终设置 `incremental_output=true`（DashScope API）或使用 `text_delta` 事件（Realtime），避免前端重复渲染或内存膨胀。
- ✅ **调试技巧**：本地测试流式响应时，可用 `curl -N` 或 `sse-cli` 工具直接查看原始 chunk 流；控制台调试建议开启「显示原始响应」开关。
- ❌ **禁止**：不要对流式响应使用 `JSON.parse(responseText)` —— 它不是单个 JSON 对象，而是多行 `data:` 消息。
- ⚡ **性能提示**：流式本身不降低模型计算耗时，但可显著改善感知延迟（TTFB 和 TTS）。若首 token 延迟高，请检查 `model_id` 是否匹配、网络链路是否跨地域、是否启用了高开销插件（如 RAG 大库检索）。

## 关联主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)


