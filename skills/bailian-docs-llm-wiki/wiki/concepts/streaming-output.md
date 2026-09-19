# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中将结果以增量方式分块（chunk）返回，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，是构建实时对话、语音交互、长文本生成等场景的核心能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼多个 API 层级和产品形态中统一支持，但具体行为与配置方式因协议和场景而异：

- **Application Call（智能体/工作流调用）**：通过 `stream=true` 启用流式响应。DashScope 原生 API 默认不启用，推荐显式设置；OpenAI 兼容的 Responses API 同样需手动开启。工作流应用额外支持 `flow_stream_mode` 参数，用于控制流式粒度（如 `message_format_plus` 按语义消息块返回，适合前端渲染）。

- **Qwen 系列模型直调（Chat / Responses / DashScope API）**：所有协议均支持 `stream=true`。Responses API 返回结构化事件流（含 `content_delta`、`tool_calls` 等字段）；DashScope API 支持 `incremental_output=true` 实现真正增量（后续 chunk 仅含新增 token，非全量重传），避免前端重复拼接。

- **Realtime API（Omni & Realtime）**：底层强制流式，基于 WebSocket 或 AOQ 双向流传输。服务端持续推送 `output.text.delta`、`output.audio.delta` 等事件，无需显式传 `stream` 参数。客户端需按事件类型解析并实时渲染/播放。

- **插件与 RAG 增强场景**：流式输出与插件调用、知识检索天然兼容——模型可在生成过程中穿插工具调用或知识引用，流式响应会同步透出 `tool_use` 或 `retrieval` 事件（需 `has_thoughts=true` 配合），便于前端展示思考过程。

> ⚠️ 注意：流式模式下，`messages` 响应体结构与非流式不同（如为 `delta` 字段而非 `content`），请务必按对应协议文档解析事件格式，不可直接复用非流式 JSON Schema。

## 关键参数和配置

| 参数 | 类型 | 作用域 | 说明 |
|------|------|--------|------|
| `stream` | `boolean` | 全部 API（Application Call / Qwen API / Realtime API 初始化） | **必需开关**：设为 `true` 启用流式传输。默认 `false`。 |
| `incremental_output` | `boolean` | 仅 DashScope 原生 API（Application Call / Qwen 文本生成） | **优化选项**：启用后，每个 `content` chunk 仅包含本次新增 token（如 `"世"` → `"界"` → `"好"`），而非累计内容（`"世"` → `"世界"` → `"世界好"`）。推荐开启以简化前端处理。 |
| `flow_stream_mode` | `string` | 仅 Application Call 中的工作流应用（DashScope 协议） | **工作流专属**：控制流式粒度，取值：<br>• `message_format_plus`（推荐）：按语义完整消息块返回（含 role/content/tool_calls）<br>• `message_format`：兼容旧版消息格式<br>• `full_thoughts`（不推荐）：返回原始思考链，调试用 |
| `enable_interim_results` | `boolean` | Omni Realtime API（ASR 场景） | **语音识别专用**：设为 `true` 时，ASR 引擎推送中间识别结果（如 `"今天天"`），适用于实时字幕等低延迟需求。 |

> ✅ 最佳实践：  
> - 前端务必监听 `data: ` 事件（HTTP SSE）或 `message` 事件（WebSocket），按行解析流式数据；  
> - 对 `incremental_output=false` 的流式响应，需自行累积 `content` 字段；  
> - 使用官方 SDK（如 `dashscope-python-sdk>=1.20.14`）可自动处理流式解析与重试，强烈推荐。

## 面向开发者提示

- 流式输出不改变计费逻辑：按实际生成 token 数计费，与是否流式无关。  
- 错误处理需适配流式：流式请求失败可能发生在任意 chunk，需监听 `error` 事件或检查末尾 `{"error":{...}}` 事件。  
- 超时设置建议：HTTP 流式请求需延长客户端超时（建议 ≥120s）；WebSocket 连接需实现心跳保活与断线重连。  
- 调试技巧：使用 `curl -N` 或 Postman 的 Stream 模式可直观观察流式响应；SDK 日志开启 `DEBUG` 级别可打印原始 chunk。

## 关联主题页

- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)


