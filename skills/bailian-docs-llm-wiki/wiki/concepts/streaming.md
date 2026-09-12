# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种增量式响应机制，允许模型在生成过程中将结果以小块（chunk）形式持续、低延迟地返回给客户端，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升交互实时性，是构建对话式应用、语音助手、实时翻译等体验的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准 Chat Completion 接口（`/v1/chat/completions`）**：通过请求参数 `stream=true` 启用。服务端以 SSE（Server-Sent Events）格式逐块返回 `data: {...}` 消息，每块包含 `delta.content`（文本增量）、`delta.role` 或 `function_call.arguments.delta` 等字段。适用于 Web 前端、CLI 工具及兼容 OpenAI 协议的第三方客户端（如 Cursor、Postman）。

- **[test 1](../guides/test-1.md) 轻量推理服务**：同样支持 `stream=true` 参数，但仅限 `qwen-turbo` 和 `qwen-plus` 模型；流式响应体结构与标准接口一致，且不支持系统提示词或 LoRA 等高级功能。

- **Realtime API（WebSocket）**：流式为**强制模式**（`stream` 必须设为 `true`），基于 WebSocket 事件驱动通信。服务端按类型分帧推送 `response.text.delta`、`response.function_call_arguments.delta`、`response.audio.delta` 等事件，客户端需按序拼接并处理中断/恢复逻辑，适用于高保真实时对话与音视频协同场景。

- **Omni Realtime API（多模态）**：流式为**唯一模式**（`stream` 必须为 `true`），支持跨模态增量流：语音输入（ASR）→ 文本流 → 语音合成（TTS chunk）→ 视觉理解结果。所有输出均以事件帧（如 `output.text.delta`, `output.audio.chunk`）形式实时下发，要求客户端严格遵循时序与 ACK 协议。

- **应用观测（Monitoring）**：流式调用的 [Token](token.md) 统计依赖完整消费响应流——若客户端提前终止连接或未读取全部 chunk，`usage.output_tokens` 可能低估实际消耗，影响成本分析与配额监控，建议在生产环境确保流消费完整性。

- **开发工具集成**：多数第三方客户端（如 Cherry Studio、Kilo CLI、Dify）支持 `stream=true` 配置，但部分工具默认关闭或限制流式 UI 渲染（如仅显示最终结果）。启用前请确认工具文档是否明确声明对 SSE 或 WebSocket 流式协议的支持。

## 关键参数和配置

| 参数 | 类型 | 是否必需 | 说明 | 典型值 |
|------|------|----------|------|--------|
| `stream` | boolean | 多数场景推荐/必需 | 控制是否启用流式响应 | `true`（必须设为 `true` 才生效） |
| `max_tokens` | integer | 否 | 设置最大生成长度，流式响应将在达到该阈值时触发 `done` 事件并终止 | `1024`, `2048` |
| `temperature` / `top_p` | float | 否（部分接口不生效） | 在标准 `/v1/chat/completions` 和 [test 1](../guides/test-1.md) 中有效；**Realtime API 中被忽略**，由服务端统一调控 | `0.7`, `0.95` |

> ⚠️ 注意事项：
> - `stream=true` 时，响应体格式不再是单个 JSON 对象，而是多行 SSE 格式（`data: {...}\n\n`）或 WebSocket 事件帧；
> - Realtime API 与 Omni Realtime API **不接受 `stream=false`**，传入 `false` 将直接返回错误；
> - 流式调用仍受全局 QPS/RPM 限制，突发流量需客户端实现指数退避；
> - 所有流式接口均需正确处理连接异常、超时（如 Realtime API 单会话最长 300 秒）及 `response.done` / `session.end` 等终结事件。

面向开发者，请始终：
- 使用官方 SDK（`dashscope>=2.0`）简化流式解析与重连逻辑；
- 在前端用 `EventSource`（SSE）或 `WebSocket` 原生 API 消费流，避免阻塞主线程；
- 对 `delta.content` 做防 XSS 处理，对 `function_call.arguments.delta` 做 JSON 片段累积校验；
- 生产环境务必捕获 `error` 事件帧或 SSE 的 `event: error`，并记录 `trace_id` 用于可观测性排查。

## 关联主题页

- [test 1](../guides/test-1.md)
- [get started with models](../guides/get-started-with-models.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application monitoring](../guides/application-monitoring.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


