# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种响应模式，允许模型在生成过程中持续、分块地返回结果，而非等待全部内容完成后再一次性返回。该机制显著降低端到端延迟，提升用户交互实时性，适用于对话、语音助手、长文本生成、实时音视频处理等对响应速度敏感的场景。

## 在百炼平台的不同场景中如何使用

- **标准模型 API（Chat/Completions）**：通过在请求体中设置 `stream=true`，调用 `/v1/chat/completions` 或 `/v1/completions` 接口。服务端以 Server-Sent Events（SSE）格式逐条推送 `data: {...}` 帧，每帧包含 `delta`（增量文本）、`finish_reason` 等字段。客户端需按 SSE 协议解析，不可直接 `JSON.parse` 整个响应体。

- **Realtime API（WebSocket）**：专为低延迟设计，**强制启用流式**（`stream` 固定为 `true`）。通过 WebSocket 连接持续收发二进制/JSON 帧，支持 `text_delta`、`audio_chunk`、`event`（如 `speech_start`）等细粒度响应类型，适用于语音转写、实时目标检测等流式媒体场景。

- **Omni Realtime API**：基于会话（session）的多模态流式交互，支持同时输出文本与音频流。通过 `modalities: ["text", "audio"]` 显式声明输出模态，并配合 `audio.output.voice`、采样率等参数控制合成效果；所有响应均以事件驱动方式（如 `content_part`、`audio_part`）实时推送。

- **Application Call（智能体/工作流调用）**：支持同步、异步与流式三种模式。启用 `stream=true` 后，需额外在 HTTP Header 中添加 `X-DashScope-SSE: enable`（DashScope 协议）或遵循 Responses 协议的 JSON Lines 格式。流式下可结合 `incremental_output=true` 实现纯增量文本（后续 chunk 不重复前序内容），避免客户端自行去重。

- **[OpenAI 兼容接口](openai-compatible-interface.md)**：完全兼容 OpenAI 的 `stream` 行为，包括 SSE 格式、`[DONE]` 结束标识、`delta.content` 字段语义等，便于现有 OpenAI 生态工具无缝迁移。

## 关键参数和配置

| 参数 | 类型 | 说明 | 默认值 | 注意事项 |
|------|------|------|--------|----------|
| `stream` | boolean | 全局开关，启用流式响应 | `false` | 所有协议均支持；设为 `true` 后，响应格式、解析方式、超时策略均发生变化 |
| `X-DashScope-SSE` | string header | DashScope 协议下启用 SSE 解析的显式标识 | 无 | HTTP 调用流式 Application 或原生 API 时**必须设置为 `enable`**，否则返回 400 |
| `incremental_output` | boolean | DashScope 流式专属：是否返回纯增量文本（即 `delta.content` 不含历史内容） | `false` | 仅 DashScope 协议支持；OpenAI/Anthropic/Responses 协议默认行为即为增量 |
| `modalities` | array | Omni Realtime 专用：声明输出模态组合 | `["text","audio"]` | 必须为 `["text"]` 或 `["text","audio"]`；影响服务端响应事件类型与结构 |

> ⚠️ 重要提醒：
> - 流式响应**不改变计费逻辑**：按实际生成的 token 总数计费，与是否流式无关；
> - 流式请求**仍受 `max_tokens` 硬上限约束**，超限将被截断并返回 `finish_reason="length"`；
> - 客户端必须实现健壮的流式解析器（推荐使用百炼官方 SDK），避免因网络抖动、帧乱序或连接中断导致数据丢失；
> - Realtime/Omni Realtime 场景下，流式是唯一模式，无需手动设 `stream`，但需严格遵循帧协议与心跳机制。

---  
*本文档面向开发者，聚焦「流式输出」概念本身。具体模型能力、地域接入、配额限制等，请参考对应主题文档。*

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)


