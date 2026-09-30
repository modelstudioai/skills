# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，指模型推理结果以增量、分块的方式持续返回给客户端，而非等待整个响应生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于长文本生成、语音合成、实时对话等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用调用（Application Call）**：通过 DashScope 原生 API 或 OpenAI 兼容 Responses API 调用智能体或工作流时，设置 `stream=true` 即可启用流式输出。服务端按 SSE（Server-Sent Events）协议推送 `data:` 格式事件，每条事件包含一个响应片段（如 `text_delta`）。注意：Responses API 的异步模式（`background=true`）不支持流式输出。

- **RAG 知识问答**：在 `/api/v2/apps/knowledge/chat` 接口中，流式输出为默认行为（无需额外参数），响应以 SSE 格式逐块返回语义化答案片段，便于前端实现打字机效果或实时渲染。

- **实时多模态 API（Omni Realtime / Realtime API）**：基于 WebSocket 的实时接口天然支持流式输出。服务端持续推送结构化事件（如 `response.text.delta`、`response.audio.delta`、`conversation.item.created`），实现文本与音频的毫秒级同步输出，适用于语音助手、智能客服等低延迟交互场景。

- **应用组件 API（Application Component API）**：调用 `/v1/applications/{app_id}/chat` 时，需显式设置请求头 `Accept: text/event-stream` 并确保客户端能解析 SSE 流；响应体为标准 `data: {...}\n\n` 格式，每个 chunk 包含 `delta` 字段（文本增量）和 `finish_reason` 字段（流结束标识）。

- **开发工具集成（CLI/IDE 插件等）**：当使用 OpenAI 兼容协议接入百炼（如通过 Cursor、Cherry Studio 或自建 SDK）时，只要底层请求携带 `stream=true` 且客户端正确处理 SSE 或 chunked transfer encoding，即可获得流式响应——无需修改业务逻辑，兼容主流 AI 工具链。

## 关键参数和配置

- `stream`: 布尔类型，全局开关。所有支持流式的 API 均通过此参数启用（默认 `false`）。  
- `Accept` 请求头：对于 RESTful 流式接口（如 Application Component API），必须设置为 `text/event-stream`。  
- 响应格式：统一遵循 SSE 规范，每条消息以 `data:` 开头，JSON 内容需合法转义；末尾以双换行符 `\n\n` 分隔。典型字段包括：
  - `delta`: 当前文本增量（字符串）
  - `role`: 消息角色（通常为 `"assistant"`）
  - `finish_reason`: 结束原因（`"stop"`、`"length"`、`"tool_calls"` 等）
  - `index`: 消息序号（用于多候选响应排序）
- 注意事项：
  - 流式模式下不返回完整 `usage` 统计，需在流结束后的最终 chunk 中提取；
  - 若请求中同时指定 `stream=true` 和 `background=true`（Responses API），后者优先，流式将被禁用；
  - WebSocket 类接口（Omni/Realtime）无需 `stream` 参数，其流式行为由协议本身保证。

面向开发者，请始终校验响应 Content-Type、正确处理 SSE 解析边界，并在客户端实现超时重连与错误恢复逻辑。

## 关联主题页

- [rag api](../api/rag-api.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application component api reference](../api/application-component-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


