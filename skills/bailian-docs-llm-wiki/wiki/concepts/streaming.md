# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种响应模式，允许模型在生成过程中**逐块（chunk）返回结果**，而非等待全部内容完成后再一次性返回。它显著降低端到端延迟，提升用户感知的响应实时性，是构建交互式 AI 应用（如聊天界面、语音助手、实时翻译）的核心能力。

## 在百炼平台的不同场景中如何使用

流式输出在以下三类核心调用路径中统一支持，但协议与事件形态不同：

- **标准模型 API（`/api/v1/services/aigc/text-generation/generation`）**：通过 `stream=true` 启用，服务端以 `text/event-stream` 格式返回多个 `data: {...}` 事件，每个事件含一个 `delta` 字段（增量文本）和可选的 `finish_reason`。适用于 Qwen 系列文本模型（如 `qwen-max`）的通用文本生成。

- **应用调用 API（`/api/v1/apps/{APP_ID}/completion` 或 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）**：同样通过 `stream=true` 参数启用。智能体（Agent）或工作流（Workflow）的中间步骤（如工具调用、RAG 检索、思考过程）可被拆分为独立事件流，支持 `enable_thinking` 时返回结构化思考片段。

- **Realtime API（WebSocket 协议）**：原生流式设计，无需显式 `stream` 参数。客户端通过监听 `output.text.delta`、`output.audio.chunk`、`output.tool_call` 等细粒度事件实时消费输出，支持毫秒级响应与双向控制（如 `interrupt` 中断）。

> ✅ 统一行为：所有场景下，流式响应末尾均以 `data: [DONE]` 标识结束；若启用 `stream_options.include_usage=true`（仅限模型 API），则在 `[DONE]` 前插入含 `usage` 字段的最终事件。

## 关键参数和配置

| 参数 | 类型 | 作用域 | 说明 |
|------|------|--------|------|
| `stream` | `boolean` | 全部 RESTful API（模型、应用） | 必须设为 `true` 才启用流式；默认 `false`（同步阻塞模式） |
| `stream_options.include_usage` | `boolean` | 仅模型 API（`text-generation`） | 设为 `true` 时，在流式结束前返回 token 使用统计（`prompt_tokens`/`completion_tokens`）；会增加约 100ms 延迟 |
| `enable_thinking` / `has_thoughts` | `boolean` | 应用调用 API（智能体） | 配合 `stream=true`，使模型思考过程作为独立流式事件返回，便于前端渲染“思考中”状态 |
| `flow_stream_mode` | `string` | 工作流应用（控制台配置 + API） | 控制流式切分粒度（如 `message_format_plus`），需在控制台流程节点开启流式开关后生效 |

⚠️ 注意：
- Realtime API 不使用 `stream` 参数，其流式能力由 WebSocket 协议和事件模型天然承载；
- `stream=true` 与异步调用（`background=true`）互斥：二者不可同时启用；
- 流式响应不支持 `response_format.type="json_object"`（JSON Schema 强约束需完整上下文校验，暂不兼容流式）。

## 面向开发者：简洁实用建议

- **必做**：始终检查 HTTP 响应头 `Content-Type: text/event-stream`，并按 SSE（Server-Sent Events）协议解析 `data:` 行；
- **推荐**：前端使用 `ReadableStream` + `TextDecoderStream` 处理流数据，避免手动拼接 `delta` 导致乱码；
- **调试**：用 `curl -N` 或 Postman 的 “Stream response” 开关验证流式行为，观察是否持续收到多条 `data:` 事件；
- **容错**：监听 `error` 事件并实现重连逻辑（尤其 WebSocket 场景），Realtime API 提供 `session_id` 复用机制恢复上下文；
- **性能**：高吞吐场景慎用 `stream_options.include_usage=true`；如需计费统计，建议聚合日志中的 `x-dashscope-usage` 响应头（含 token 数）。

流式输出不是“高级选项”，而是生产环境的**默认推荐模式**——它让 AI 响应从“等待”变为“渐进呈现”，是用户体验升级的关键杠杆。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [release notes](../guides/release-notes.md)


