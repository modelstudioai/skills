# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成结果过程中分块、渐进地返回内容，而非等待全部推理完成后再一次性返回。该机制显著降低端到端延迟，提升用户交互体验，并有效规避长响应场景下的网络超时风险。

## 在百炼平台的不同场景中如何使用

- **应用调用（`application call`）**：  
  通过 `stream=true` 参数启用流式输出，适用于智能体（Agent）或工作流（Workflow）的同步调用。服务端按 token 或语义单元（如思考步骤、工具调用片段、最终回答段落）分批推送事件。配合 `incremental_output=true` 可实现 delta 增量更新（即每帧仅含本次新增内容），便于前端逐字渲染；设为 `false` 则每帧返回当前完整累积内容。

- **Realtime API（WebSocket 实时接口）**：  
  流式输出为默认且强制行为。所有响应均以 WebSocket 事件形式实时推送，包含 `output` 类型消息，其 `delta` 字段承载增量文本、`tool_calls` 字段承载结构化工具调用信息、`finish_reason` 标识生成终止原因（如 `stop`、`length`、`tool_calls`）。该模式天然支持语音流中断恢复、多轮上下文维持与低延迟交互。

- **标准模型调用（[OpenAI 兼容接口](openai-compatible-api.md)）**：  
  在 `chat.completions.create()` 中设置 `stream=True` 即可启用。返回 `Stream[ChatCompletionChunk]` 对象，开发者需迭代处理每个 `chunk`，从中提取 `chunk.choices[0].delta.content`（文本）、`chunk.choices[0].delta.tool_calls`（工具调用）等字段。注意：`stream=True` 时 `response_format`（如 JSON Schema）仍生效，服务端保证流式输出符合指定结构。

> ⚠️ 注意：流式输出不支持异步任务（`background=true`）和部分非流式模型（如某些图像/视频生成模型），启用前请确认模型与接口类型兼容。

## 关键参数和配置

| 参数 | 所属接口 | 类型 | 说明 |
|------|----------|------|------|
| `stream` | 所有 REST 接口（Application Call / Model Call） | `boolean` | 必须显式设为 `true` 启用流式；默认 `false`（全量返回）。 |
| `incremental_output` | Application Call（DashScope API） | `boolean` | 仅当 `stream=true` 时有效：`true` → 返回 delta 增量；`false` → 返回当前完整响应（追加模式）。默认 `true`。 |
| `stream_options.include_usage` | Model Call（OpenAI 兼容） | `boolean` | 控制是否在流结束前的 `usage` 字段中包含 token 统计（实验性，部分模型暂不支持）。 |

- **HTTP Header（Application Call）**：  
  `X-DashScope-Streaming: true`（旧版兼容头，推荐优先使用 `stream` 参数）

- **WebSocket 初始化（Realtime API）**：  
  流式为协议内建能力，无需额外参数；但需正确处理 `output` 事件中的 `delta`、`index`、`finish_reason` 字段以实现可靠拼接。

## 面向开发者的实践建议

- ✅ **必做**：始终检查 `finish_reason` 字段判断流是否正常结束（避免截断）；对 `tool_calls` 等结构化字段做增量合并解析。
- ✅ **推荐**：前端使用 `TextDecoder` + `ReadableStream`（浏览器）或 `aiohttp.ClientResponse.content`（Python）高效消费流；后端避免阻塞式读取，采用异步迭代。
- ⚠️ **避坑**：  
  - `stream=true` 时 `completion.choices[0].message.content` 为空，必须从 `delta.content` 提取；  
  - Realtime API 的 `session_id` 不可复用，重复使用将创建新会话；  
  - Application Call 中 `stream=true` 与 `background=true` 互斥，不可同时设置。
- 📈 **性能提示**：流式请求仍计入 RPM/TPM 限流，但单次请求生命周期更短，有利于高并发场景下的资源利用率提升。

## 关联主题页

- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [get started with models](../guides/get-started-with-models.md)
- [more about models](../api/more-about-models.md)


