# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中将结果以增量方式分块（chunk）持续返回，而非等待全部内容生成完毕后一次性返回。该机制显著降低首字延迟（Time to First [Token](token.md), TTFT），提升用户交互体验，尤其适用于对话类、语音合成、长文本生成等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

- **基础模型调用（Text Generation）**：通过 DashScope 原生 API 或 [OpenAI 兼容接口](openai-compatible-api.md)（`/chat/completions`、`/responses`）调用 Qwen 系列文本模型时，设置 `stream=true` 即可启用流式响应，服务端按 SSE（Server-Sent Events）协议逐 token 推送 `data: {...}` 格式消息。
  
- **智能体与工作流应用调用**：在 `application call` 场景中（如调用已发布的 Agent 或 Workflow），同样通过 `stream=true` 启用流式输出；若需进一步优化带宽与解析效率，可叠加 `incremental_output=true`，确保每个 chunk 仅包含新增 token，避免历史内容重复回传。

- **多模态实时交互（Realtime API）**：在 `Qwen-Omni-Realtime` 和 `Qwen-Audio-Realtime` 等低延迟场景中，流式是默认且强制的工作模式。模型同时输出文本与音频流（如 PCM/WAV 片段），客户端需基于 WebSocket 事件（如 `output.text.delta`、`output.audio.delta`）实时消费和渲染。

- **知识库问答与 RAG 应用**：控制台零代码构建的知识库问答应用默认支持流式响应；若通过 API 调用，需在请求参数中显式开启 `stream`，RAG 检索与大模型生成阶段的中间结果亦可随流式通道逐步透出（取决于应用配置）。

> ⚠️ 注意：`stream=true` 与异步模式互斥——例如 Responses API 中 `background=true` 时不可启用流式；Realtime API 不兼容 REST 流式，必须使用 WebSocket 或 AOQ 协议。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 默认值 | 生效范围 |
|--------|------|------|--------|----------|
| `stream` | `boolean` | 启用流式响应开关 | `false` | 所有支持流式的 API（DashScope、OpenAI Chat/Responses、Anthropic Messages、Application Call、Realtime API） |
| `incremental_output` | `boolean` | 在 `stream=true` 下启用增量式输出（每个 chunk 仅含新 token，非全量重传） | `false` | Application Call（DashScope & Responses）、部分智能体 API |
| `enable_interim_results` | `boolean` | （Realtime 专用）启用语音识别中间结果（ASR partial text） | `false` | Realtime API（`qwen-audio-realtime-v1`） |

- **响应格式**：流式响应统一采用 SSE 协议（除 Realtime API 使用 WebSocket 事件）。典型 chunk 示例：
  ```text
  data: {"id":"cmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"content":"你好"},"index":0}]}
  ```
- **错误处理**：流式过程中若发生错误，服务端可能发送 `event: error` 消息，但其 `code` 字段不保证完整；**务必同步检查 HTTP 状态码（如 4xx/5xx）及响应体中的 `code` 和 `message` 字段**。
- **SDK 支持**：Python SDK（`dashscope>=1.20.0`）和 Node.js SDK（`@alibabacloud/dashscope>=1.15.0`）均提供 `.stream()` 方法或 `stream: true` 选项，自动处理 SSE 解析与 chunk 合并，推荐直接使用。

面向开发者，请始终：
- 显式设置 `stream=true` 并正确处理 SSE 流（或 WebSocket 事件）；
- 对于长响应，启用 `incremental_output=true` 避免前端重复渲染；
- 在 Realtime 场景中，优先使用 AOQ 客户端 SDK 管理连接、心跳与 buffer，勿手动实现底层协议；
- 生产环境注意流式连接超时（如 Realtime 单会话上限 10 分钟）、并发配额（如 Realtime 默认 5 个活跃 session）等限制。

## 关联主题页

- [start using](../guides/start-using.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


