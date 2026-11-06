# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在推理过程中边生成、边返回结果片段（如 token、音频帧或结构化事件），而非等待整个响应完成后再一次性返回。该机制显著降低端到端延迟，提升用户体验，尤其适用于对话交互、语音合成、长文本生成等对实时性敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准模型调用（`model experience`）**：通过 `stream: true` 参数启用 SSE（Server-Sent Events）流式响应，适用于 Qwen 系列文本模型、Qwen-VL/Qwen-Omni 等支持流式输出的多模态模型；返回格式为逐行 `data: {...}` 的 JSON 对象，每条包含一个增量 token 或中间状态（如 `finish_reason`）。  
- **Realtime API（WebSocket 场景）**：流式为强制模式（`stream` 必须为 `true`），所有实时能力（ASR、TTS、Audio Chat、Omni 多模态交互）均基于双向 WebSocket 流实现，支持毫秒级音频 chunk 输入与结构化事件（如 `response.output`, `response.audio`, `event.partial`）实时输出。  
- **Qwen 兼容 API（OpenAI/Anthropic/DashScope 协议）**：统一支持 `stream: true` 参数，行为一致：OpenAI Chat 和 Responses、Anthropic Messages、DashScope 原生接口均可触发 token 级流式响应；注意 Qwen-Audio 模型仅 DashScope 协议支持流式，OpenAI 兼容协议不适用。  
- **应用层集成（`application support`）**：在智能体（Agent）或 Assistant API 调用中，除 `stream=True` 外，可叠加 `incremental_output=True` 实现真正增量式输出——即每次只返回新增 token，避免重复回传历史内容，减少带宽消耗与客户端解析开销。  
- **SDK 封装层**：Python SDK（`dashscope>=2.0.0`）提供 `Generation.call(..., stream=True)` 和 `RealtimeClient` 两类流式调用入口；前者自动处理 SSE 解析并 yield `GenerationResponse` 对象，后者封装 WebSocket 生命周期管理与事件分发，开发者只需注册回调函数即可处理 `on_token`, `on_audio`, `on_error` 等事件。

## 关键参数和配置

| 参数 | 类型 | 说明 | 默认值 | 生效范围 |
|------|------|------|--------|----------|
| `stream` | `boolean` | 启用流式响应机制 | `false` | 所有 HTTP 模型 API（`model experience`, Qwen API）、Realtime API（强制 `true`） |
| `incremental_output` | `boolean` | 在 `stream=True` 下启用增量式输出（仅返回新增 token，非全量重传） | `false` | `application support` 场景（Agent/Assistant API）、部分 DashScope 高级调用 |
| `response_format` | `string` | Realtime API 中指定流式响应结构，`"json"`（完整对象）或 `"delta"`（纯 token 字符串） | `"json"` | Realtime API（WebSocket） |
| `enable_intermediate_results` | `boolean` | ASR/TTS 类 Realtime 接口专用，控制是否返回中间识别/合成结果 | `false` | Realtime API（ASR/TTS 子模块） |

> ⚠️ 注意事项：  
> - 视觉生成（如 Wanx）、[向量嵌入](vector-embedding.md)（embedding）、重排序（rerank）等非生成类模型**不支持流式输出**；  
> - TTS 在 HTTP 接口（非 Realtime）中默认不启用流式，需显式设置 `stream=true` 并确认模型支持（如 `qwen2-tts-flash`）；  
> - 流式响应需客户端按协议正确解析：HTTP 流用 SSE 标准（检查 `Content-Type: text/event-stream`），WebSocket 流需遵循 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 定义的事件格式。

## 面向开发者，简洁实用

- ✅ **快速启用**：在请求体中添加 `"stream": true`，配合 SDK 的 `stream=True` 参数即可开启基础流式；  
- ✅ **优化体验**：对长文本生成或对话应用，务必启用 `incremental_output=True`，避免前端重复渲染；  
- ✅ **实时交互首选**：语音/视频类低延迟场景，**必须使用 Realtime API（WebSocket）**，HTTP 流式无法满足毫秒级要求；  
- ✅ **错误处理**：流式请求失败时，服务端可能在任意时刻发送 `error` 事件或终止连接，客户端应监听 `on_error` 回调并实现重连逻辑（Realtime API 连接超时为 30 分钟）；  
- ✅ **调试建议**：使用 `curl -N` 或 Postman 的 SSE 插件直接测试 HTTP 流式响应；Realtime API 推荐使用官方 `dashscope-realtime` SDK 或参考 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 示例代码。

## 关联主题页

- [preparations](../api/preparations.md)
- [model experience](../guides/model-experience.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [application support](../guides/application-support.md)


