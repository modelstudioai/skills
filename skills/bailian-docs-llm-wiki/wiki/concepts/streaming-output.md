# 流式输出

流式输出（Streaming Output）是百炼平台模型服务的核心响应模式之一，指模型在生成结果过程中，将输出内容按 token 或语义单元分块、实时、增量地返回给客户端，而非等待全部推理完成后再一次性返回完整响应。该机制显著降低端到端延迟，提升用户体验，是构建实时对话、语音交互、长文本生成等场景的基础设施能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼各协议与接口中统一支持，但具体实现方式和事件结构因协议而异：

- **标准模型 API（DashScope 原生 / OpenAI 兼容 Chat & Responses / Anthropic Messages）**：  
  通过请求参数 `stream=true` 启用。响应为 Server-Sent Events（SSE）格式，每条事件包含增量内容（如 `response.output_text.delta` 或 `choices[0].delta.content`），最终 chunk 包含完整 `output.text` 或 `choices[0].message.content`。适用于通用文本生成、代码补全、多轮对话等场景。

- **Realtime API（WebSocket 协议）**：  
  原生流式设计，无需显式开启 `stream` 参数。连接建立后，服务端持续推送 `response.text.delta`、`input_audio_buffer.committed`、`response.done` 等结构化事件，支持毫秒级延迟的语音转写+响应合成闭环。适用于智能硬件、实时会议助手、语音客服等低时延场景。

- **Omni Realtime API（AOQ/WebSocket/WebRTC）**：  
  同样默认流式，支持文本流（`response.text.delta`）与音频流（PCM/WAV 分片）同步输出。通过 `modalities: ["text", "audio"]` 控制多模态流组合，并可结合 `turn_detection` 实现 VAD 驱动的流式中断与续写。

- **Application Call（智能体/工作流调用）**：  
  支持 `stream=true`（DashScope 协议）或 `stream: true`（Responses 协议），返回增量执行日志、工具调用中间结果及最终答案。配合 `incremental_output=true`（仅 DashScope）可确保每个 chunk 仅含 delta 变更，避免重复传输全量上下文。

> ⚠️ 注意：异步调用（如 `background=true`）不支持流式；流式响应下，`output.text` 字段在最终 chunk 才完整可用，中间 chunk 的 `output.text` 仅为当前增量片段。

## 关键参数和配置

| 参数 | 类型 | 默认值 | 说明 | 适用协议 |
|------|------|--------|------|----------|
| `stream` | boolean | `false` | 必须显式设为 `true` 才启用流式响应。所有主流协议均支持此参数。 | 全部（DashScope / Responses / Chat / Anthropic / Application Call） |
| `incremental_output` | boolean | `false` | 仅 DashScope 协议有效。设为 `true` 时，每个流式 chunk 的 `output.text` 为 delta 增量；设为 `false`（默认）则为截至当前的全量快照。推荐生产环境启用以减少带宽与解析开销。 | DashScope（模型 API & Application Call） |
| `content-type`（响应头） | string | `text/event-stream` | 流式响应固定为 `text/event-stream; charset=utf-8`，客户端需按 SSE 规范解析。 | 全部 HTTP 流式接口 |
| WebSocket 事件类型 | string | — | Realtime/Omni Realtime 使用自定义事件名（如 `response.text.delta`, `response.done`），非标准 SSE，需按对应协议文档解析。 | Realtime API / Omni Realtime API |

## 面向开发者：简洁实用提示

- ✅ **必做**：始终检查响应状态码（200）和 `Content-Type: text/event-stream`，再开始解析 SSE；WebSocket 场景需监听 `open` 后再发送首条消息。
- ✅ **推荐**：对文本流使用 `delta` 字段拼接（而非累加 `output.text`），尤其启用 `incremental_output=true` 时更高效。
- ✅ **调试技巧**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流数据；Realtime/Omni 接口建议优先使用官方 AOQ SDK（已封装重连、VAD、音频编解码等）。
- ❌ **避免**：在流式响应未结束前关闭连接或提前释放资源；不要假设所有 chunk 都含 `output.text`（部分中间 chunk 可能只含工具调用事件）。
- 📌 **性能注意**：流式不降低单 token 计算耗时，但显著改善首字节时间（TTFB）和感知延迟；高并发流式请求需关注客户端连接池与服务端配额（动态限流策略对流式同样生效）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)


