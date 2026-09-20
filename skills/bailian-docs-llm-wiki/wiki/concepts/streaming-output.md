# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续、分块地返回结果（如文本 token、音频帧或事件），而非等待整个响应完成后再一次性返回。该机制显著降低端到端延迟，提升交互自然度，是构建低延迟语音助手、实时对话系统和长上下文渐进式渲染应用的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼多个 API 层级和业务场景中以不同协议与形态落地，开发者需根据任务类型选择适配方式：

- **文本生成类（[test 1](../guides/test-1.md) / Application Call）**：  
  通过 `stream=true` 参数启用 SSE（Server-Sent Events）流式响应。服务端按 token 粒度逐块返回 `data: {...}` 事件，每块包含 `delta.content`（增量文本）或 `finish_reason`（终止原因）。适用于聊天界面打字效果、实时内容审核等场景。

- **实时语音交互类（Realtime API / Omni Realtime API）**：  
  基于 WebSocket 双向流实现毫秒级响应。服务端主动推送多种事件类型（如 `response.text.delta`、`response.audio.delta`、`conversation.item.created`），支持文本+音频混合流、VAD 触发响应、工具调用中间态等复杂交互。这是唯一支持真正“边说边听、边听边答”的流式模式。

- **音频处理类（Audio API）**：  
  ASR/TTS/语音翻译等 RESTful 接口支持可选流式响应（通过 `stream=true` + `Content-Type: text/event-stream`）。适用于长音频识别进度反馈、TTS 音频流式播放等场景；但注意：音乐生成、语音对话等能力暂不支持流式输出。

- **批量与异步任务（Batch API / Background Responses）**：  
  **不支持流式输出**。此类接口设计为离线处理，结果通过回调 URL 或轮询获取完整响应。

> ✅ 提示：是否启用流式，不仅影响响应格式，也影响计费粒度（如 Realtime API 按实际传输音频帧计费，而非请求时长）和错误恢复策略（流式连接中断需重连并续传，非流式失败则重试整请求）。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 示例值 |
|------|----------|------|------|--------|
| `stream` | 全部（[test 1](../guides/test-1.md) / Application Call / Audio API） | boolean | 启用流式响应的开关。设为 `true` 后，响应头变为 `Content-Type: text/event-stream`，体内容为 SSE 格式。 | `true` |
| `X-DashScope-SSE` | [test 1](../guides/test-1.md) / Application Call（DashScope 协议） | header | 替代 `stream=true` 的 Header 方式，显式声明启用 SSE 流。更推荐用于兼容性控制。 | `enable` |
| `flow_stream_mode` | Application Call（工作流） | string | 工作流专用流式模式，控制子节点输出粒度。`message_format_plus` 支持结构化消息+元数据流，推荐新业务使用。 | `"message_format_plus"` |
| `incremental_output` | test 1 / Application Call（DashScope 流式下） | boolean | 仅当 `stream=true` 时有效。`true` 表示每块只含本次增量内容（默认）；`false` 表示每块返回截至当前的完整响应（不推荐，增加带宽与解析负担）。 | `true` |
| WebSocket 事件类型 | Realtime / Omni Realtime | — | 无参数，由客户端监听。关键事件包括：<br>• `response.text.delta`（文本流）<br>• `response.audio.delta`（PCM/WAV 音频帧）<br>• `response.function_call_arguments.*`（工具调用参数流） | — |

> ⚠️ 注意：  
> - `stream=true` 与 `max_tokens`、`temperature` 等生成参数完全正交，可同时配置；  
> - 流式响应不改变计费逻辑（仍按实际生成 token 数或音频秒数计费），但可能影响 QPS 配额消耗节奏；  
> - 所有流式接口均要求客户端实现标准 SSE 解析器或 WebSocket 事件处理器，官方 SDK（Python/Java/JS）已内置健壮支持。

## 面向开发者，简洁实用

- **快速启用**：在任意支持流式的 API 请求中添加 `"stream": true`（JSON body）或 `X-DashScope-SSE: enable`（Header），即可获得 token 级别流式响应。  
- **解析建议**：优先使用百炼官方 SDK（如 `dashscope` Python 包的 `Generation.call(..., stream=True)`），避免手动解析 SSE 边界或 WebSocket 心跳。  
- **调试技巧**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流数据；Realtime API 推荐使用 [AOQ 客户端 SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 封装的 `on('response.text.delta', ...)` 事件监听。  
- **避坑指南**：  
  • 不要在流式请求中设置过短的 `timeout`（建议 ≥60s），避免因网络抖动中断连接；  
  • Realtime API 的音频帧必须严格按时间戳对齐（如 20ms/帧），否则触发 VAD 异常；  
  • `stream=true` 与吞吐预留（TPM）完全兼容，但流式连接本身不占用 TPM 额度——TPM 保障的是单次请求的并发调度优先级，而非流持续时间。

## 关联主题页

- [test 1](../guides/test-1.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [audio api references](../api/audio-api-references.md)
- [application call](../api/application-call.md)


