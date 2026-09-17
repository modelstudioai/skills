# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续、分块地将结果（如文本 token、音频片段或结构化事件）逐段返回给客户端，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，并支持前端实时渲染、语音流式合成、长文本渐进式处理等关键场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中统一支持但语义与实现细节因调用路径而异，开发者需按实际接口类型选择对应模式：

- **标准 Chat API（`/v1/chat/completions`）**：启用 `stream=true` 后，服务端以 SSE（Server-Sent Events）格式返回 `data: {...}` 事件流；每个事件含 `delta.content` 字段（增量文本），`delta.role`（首次出现时）、`finish_reason`（结束标识）等。适用于通用对话、RAG问答、[函数调用](function-calling.md)等场景。

- **Application Call（智能体/工作流调用）**：  
  - 新版/旧版智能体：支持 `stream=true` + `incremental_output=true` 组合，确保每次返回仅含新增 token（非全量重传），避免前端重复渲染；`delta.content` 可能为空（尤其在 function call 过渡阶段），需容错处理。  
  - 工作流：通过 `flow_stream_mode` 控制流式行为，推荐 `message_format_plus`（返回结构化消息块，含 `type`、`content`、`tool_calls` 等字段），便于前端区分文本、工具调用、状态变更等事件类型。

- **应用组件 API（`/services/aigc/text-generation/generation`）**：启用 `stream=true` 后响应体为 SSE 格式，字段命名与非流式一致（如 `output.text`），但值为增量内容；需按 `data:` 行解析并累积 `output.text` 字段。

- **Realtime API（WebSocket/AOQ/WebRTC）**：本质即流式架构，不依赖 `stream` 参数。服务端通过标准化事件（如 `response.text.delta`、`response.audio.delta`、`response.function_call`）实时推送增量内容，客户端需监听对应事件类型并按需消费。适用于语音助手、实时音视频交互等低延迟场景。

- **Omni Realtime API（WebSocket）**：基于事件驱动的原生流式协议，所有输出均为增量事件（如 `response.text.delta`、`response.audio.delta`），无需额外参数开启；`modalities` 配置决定是否同时输出文本与音频流。

## 关键参数和配置

| 参数名 | 类型 | 作用域 | 说明 |
|--------|------|--------|------|
| `stream` | boolean | 全局（Chat API、Application Call、应用组件 API） | 必须设为 `true` 以启用流式响应；默认 `false`（同步阻塞式）。 |
| `incremental_output` | boolean | 智能体类 API（新版/旧版智能体） | 仅当 `stream=true` 时生效；设为 `true` 表示返回增量 delta（推荐），`false` 表示每次返回当前完整 content（不推荐，易导致重复渲染）。 |
| `flow_stream_mode` | string | 工作流 API | 取值 `message_format_plus`（推荐，结构化消息块）、`message_format`（兼容旧版）、`full_thoughts`（含内部推理链，已不推荐）。 |
| `X-DashScope-SSE: enable` | HTTP Header | DashScope 原生 Application Call | HTTP 直接调用时必需，用于显式声明启用 SSE 协议。 |
| `x-dashscope-rtc-transport` | HTTP Header | Realtime API | 指定传输协议（`websocket`/`webrtc`/`moq`），决定底层流式通道类型。 |

> ⚠️ 注意事项：  
> - 所有流式响应均需按 **SSE 协议** 解析（以 `data:` 开头的行，忽略空行及 `event:`/`id:` 等可选字段）；  
> - `delta.content` 可能为空字符串（尤其在 function call 或 tool call 过渡阶段），请勿直接拼接，应检查 `delta.content` 是否存在且非空；  
> - 流式响应中 `finish_reason` 出现在最后一个事件，用于判断生成是否完成（如 `"stop"`、`"length"`、`"function_call"`）；  
> - SDK 用户建议直接使用 `dashscope>=1.20.0`，其内置流式迭代器（如 `for chunk in response:`）已自动处理 SSE 解析与 delta 累积。

## 面向开发者，简洁实用

- ✅ **快速启用**：在请求 body 中添加 `"stream": true`，HTTP 请求头加 `X-DashScope-SSE: enable`（Application Call），即可获得流式响应。  
- ✅ **安全消费**：用 `while` 循环读取响应流，对每个 `data:` 行 JSON 解析，提取 `delta.content` 并追加到本地 buffer；遇 `finish_reason` 则终止。  
- ✅ **前端渲染建议**：使用 `<span id="output"></span>` + `element.textContent += chunk` 实现逐字显示；语音场景建议缓冲 `response.audio.delta` 后交由 Web Audio API 播放。  
- ❌ **避免踩坑**：不要假设 `delta.content` 永不为空；不要用 `response.message.content` 替代 `delta.content`（流式下该字段不存在）；不要在未设置 `X-DashScope-SSE` 时调用 Application Call 流式接口（将返回 400 错误）。  
- 📦 **SDK 推荐**：Python 使用 `dashscope.ChatCompletion.create(..., stream=True)`；Node.js 使用 `@alicloud/dashscope-sdk-js` 的 `stream()` 方法；所有 SDK 均自动处理 SSE 解析与错误重试。

## 关联主题页

- [start using](../guides/start-using.md)
- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


