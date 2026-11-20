# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种低延迟响应机制，允许模型在生成过程中**逐段、逐 token 地持续返回结果**，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、实时语音识别与合成等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非全局统一启用，而是按模型类型和调用方式差异化支持：

- **Model Experience（HTTP 同步调用）**  
  适用于 `text-generation`（如 `qwen3` 系列）和 `speech-to-text`（ASR）类模型。通过在 JSON 请求体中设置 `"stream": true`，服务端将以 `text/event-stream` MIME 类型返回 SSE（Server-Sent Events）格式数据。每条事件为 `data: {...}` 行，包含 `delta`（增量内容）、`finish_reason`（结束原因）等字段。不支持流式的模型（如 `embedding`、`rerank`、`image-generation`）会忽略该参数。

- **Realtime API（WebSocket 实时调用）**  
  所有实时音视频能力（ASR、TTS、Audio Chat、LiveTranslate 等）**强制要求流式**，通过 WebSocket 协议实现双向低延迟流传输。需显式设置 `"enable_streaming": true`，并按协议分帧发送/接收音频流或语义事件（如 `transcript`、`audio_chunk`）。此场景下“流式”是协议级基础能力，而非可选开关。

- **Application Support（AI 应用层）**  
  在 Agent 或 RAG 应用中，可通过 SDK 的 `stream=True` 参数启用流式响应；若需前端仅渲染新增内容（避免重复刷新），应额外启用 `incremental_output=True`，确保每次事件只携带本次生成的 token 差量。

> ✅ **关键区别**：HTTP 流式（SSE）适合单次请求的渐进式响应；WebSocket 流式（Realtime）面向持续会话，支持上下文保持与双向媒体流。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必需 | 备注 |
|------|------|------|------|-----------|------|
| `stream` | HTTP 请求体（`parameters` 外层） | `boolean` | 启用 HTTP 流式响应 | ❌（默认 `false`） | 仅对 `text-generation` 和 `speech-to-text` 模型生效 |
| `enable_streaming` | Realtime WebSocket 初始化消息 | `boolean` | 启用 WebSocket 流式协议 | ✅（必须为 `true`） | 所有 Realtime API 的硬性要求 |
| `incremental_output` | Application SDK / HTTP 请求体 | `boolean` | 启用增量式流式（仅返回 delta） | ❌（默认 `false`） | 配合 `stream=true` 使用，避免前端重复解析全量历史 |
| `max_latency_ms` | Realtime 初始化消息 | `integer` | 端到端最大允许延迟（毫秒） | ❌（默认 `800`） | 影响流式吞吐与实时性权衡，最小可设 `300` |

⚠️ 注意：  
- `stream=true` 对视觉生成、向量模型等不支持流式的模型**静默失效**，不会报错但返回同步响应；  
- Realtime API **不接受 HTTP 调用**，尝试 `POST /v1/models/xxx/invoke?stream=true` 将返回 `405 Method Not Allowed`；  
- 流式响应需客户端正确处理 SSE 格式（按行解析 `data:` 字段）或 WebSocket 二进制/文本帧，建议优先使用官方 SDK 封装。

## 面向开发者：快速实践提示

- ✅ **首选 SDK**：Python 使用 `dashscope.Generation.call(..., stream=True)`；JavaScript 使用 `DashScopeClient.chat(..., { stream: true })`；Realtime 场景务必使用 `@dashscope/realtime-sdk`。  
- ✅ **前端解析 SSE**：监听 `onmessage` 事件，用 `JSON.parse(event.data)` 解析每条 `data:` 内容，注意过滤空行和 `event:` 行。  
- ✅ **错误防御**：流式请求失败时，服务端可能返回非 SSE 的 `application/json` 错误体（如 `400 Bad Request`），需检查响应头 `Content-Type` 再决定解析逻辑。  
- ⚠️ **超时控制**：HTTP 流式请求默认超时 60 秒，长文本生成建议显式设置 `timeout=120`（SDK 支持）；Realtime WebSocket 连接需自行实现心跳保活与重连。  
- 🚫 **禁止行为**：不要在流式响应中修改 `input.messages` 或 `parameters` 并重发；不要对 `embedding`/`rerank` 模型设置 `stream=true` 期望获得流式结果。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [application support](../guides/application-support.md)
- [more about models](../api/more-about-models.md)


