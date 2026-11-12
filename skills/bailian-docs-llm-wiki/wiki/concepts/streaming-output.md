# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种低延迟、渐进式响应机制，允许模型在推理过程中持续生成并实时返回结果片段（如 token、音频帧、文本块），而非等待整个响应完成后再一次性返回。该机制显著提升用户交互体验，适用于对话、语音合成、实时翻译等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中通过两种协议形态支持，适用于不同调用层级和业务需求：

- **HTTP/SSE 流式（Model Experience）**  
  适用于标准模型 API 调用（`/v1/models/{model_id}/invoke`）。启用后，服务端以 Server-Sent Events（SSE）格式逐条推送 `data:` 块，每块包含一个增量结果（如单个 token 的 `text` 字段或 `delta` 内容）。**仅文本生成类模型（LLM）支持该模式**；视觉、语音（ASR/TTS）、向量类模型启用 `stream: true` 将被静默忽略，返回完整同步响应。

- **WebSocket 实时流式（Realtime API）**  
  专为低延迟交互设计，用于 ASR、TTS、Audio Chat、LiveTranslate 等实时语音/多模态服务。客户端通过 WebSocket 连接建立双向数据通道，服务端按帧（frame）持续推送 `text`、`audio`、`event` 等类型消息，支持毫秒级首字/首音响应、流式打断与上下文维持。此模式不依赖 `stream` 参数，而是由协议本身强制流式。

- **应用层增量控制（Application Support）**  
  在 Assistant/Agent 应用中，除基础 `stream=True` 外，可额外启用 `incremental_output=True`（或 `stream_options.incremental=true`），确保每次 SSE 消息仅携带本次新增内容（非累计全文），避免前端重复渲染。该参数对带插件调用或 RAG 增强的复杂链路尤为重要。

> ⚠️ 注意：视觉生成（如图像）、语音识别（ASR）和向量模型（embedding/rerank）**不支持 HTTP/SSE 流式**；若需图像生成过程反馈，请使用轮询进度接口（见 [视觉生成状态查询](../../raw/model-user-guide/model-experience/image-and-video-generation.md)）。

## 关键参数和配置

| 参数名 | 类型 | 作用域 | 说明 |
|--------|------|--------|------|
| `stream` | `boolean` | Model Experience / Application API | 启用 HTTP/SSE 流式响应。默认 `false`；设为 `true` 后，响应头含 `Content-Type: text/event-stream`，响应体为 SSE 格式。仅对文本生成模型生效。 |
| `incremental_output` | `boolean` | Application API（Agent/Assistant） | 仅在 `stream=true` 时有效。控制是否返回增量 delta（`"delta": "..."`）而非累计内容（`"text": "..."`）。推荐开启以简化前端处理逻辑。 |
| `stream_options` | `object` | SDK 封装推荐用法 | 替代硬编码布尔值的结构化配置，例如：<br>`{"incremental": true, "include_usage": false}`。SDK（如 `aliyun-openapi-python-sdk` v2.3.1+）自动映射至底层参数。 |

- **Realtime API 不使用上述参数**：其流式行为由 WebSocket 协议和初始化消息（`init`）隐式决定，无需显式设置 `stream`。
- **错误处理建议**：流式请求失败时，服务端可能在任意时刻发送 `event: error` + `data: {...}`；客户端应监听所有 `event` 类型并做容错处理，不可假设仅存在 `message` 事件。

## 面向开发者：简洁实用提示

- ✅ **首选 SDK**：使用官方 `dashscope` 或 `aliyun-openapi-python-sdk`，它们已封装 SSE 解析、重连、`incremental_output` 自动适配及 Realtime WebSocket 生命周期管理。
- ✅ **前端解析 SSE**：浏览器中直接使用 `EventSource`；Node.js 中推荐 `fetch` + `ReadableStream` 或 `@microsoft/fetch-event-source` 库。
- ✅ **调试技巧**：用 `curl -N` 测试流式响应，观察 `data:` 行是否持续输出；注意末尾空行分隔。
- ❌ **避免手动拼接**：勿将 `stream=false` 的完整响应拆分为“模拟流式”——这无法降低首字延迟，且破坏 token 级精度。
- 📌 **性能提示**：流式不降低总耗时，但显著改善感知延迟（Time to First [Token](token.md)）；如需极致低延迟，请优先选用 Realtime API（如 `qwen2-audio-realtime-chat-zh`）而非通用 LLM 的 SSE 流式。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [application support](../guides/application-support.md)
- [get started with models](../guides/get-started-with-models.md)


