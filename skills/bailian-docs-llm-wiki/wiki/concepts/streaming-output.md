# 流式输出

流式输出（Streaming Output）是百炼平台支持的一种实时响应机制，允许模型在生成过程中将结果以增量方式分块返回（如逐 token、逐词或逐句），而非等待整个响应完成后再一次性返回。该机制显著降低用户感知延迟，提升交互自然度，是构建实时对话、语音合成、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼各核心能力模块中统一支持，但启用方式与行为细节略有差异：

- **Sandbox 实验环境**：通过 `stream: true` 参数启用，响应格式为 Server-Sent Events（SSE），每帧包含一个 `delta` 字段（新增文本片段）和 `finish_reason` 字段（如 `"stop"` 或 `"length"`）。注意：启用后 `output` 字段不返回完整结果，需客户端自行拼接。
  
- **Application Call（智能体/工作流调用）**：支持 DashScope 原生 API 与 OpenAI 兼容的 Responses API。DashScope 需同时设置 `stream: true` 并在请求 Header 中添加 `X-DashScope-SSE: enable`；Responses API 直接在请求体中传入 `stream: true` 即可。若需增量式流式（即每帧仅含新内容，不重复已发内容），须额外设置 `incremental_output: true`（仅 DashScope 支持）。

- **Qwen 系列模型 API（Chat Completions / DashScope / Anthropic Messages）**：所有协议均支持 `stream: true`。[OpenAI 兼容接口](openai-compatible-api.md)返回标准 SSE 格式；DashScope 接口默认全量追加（每帧含从开头至今的全部文本），可通过 `incremental_output: true` 切换为纯增量模式；Anthropic Messages 接口原生按 chunk 增量返回，无需额外参数。

- **Realtime API（实时音视频交互）**：流式为默认行为，无需显式配置 `stream` 参数。服务端按语音活动（VAD）、语义单元或固定时间窗口自动切分 `text` 和 `audio` 输出流，通过 WebSocket/AOQ/WebRTC 协议实时推送，适用于语音对话、实时字幕等低延迟场景。

- **Application Support（插件与 RAG 场景）**：流式输出与插件调用、RAG 检索完全兼容。当 `stream: true` 时，模型可在生成回答前先输出工具调用请求（`tool_calls`），或在检索结果注入后继续流式生成最终回复，实现“思考-检索-生成”全流程可见。

## 关键参数和配置

| 参数名 | 类型 | 作用 | 适用范围 | 注意事项 |
|--------|------|------|----------|----------|
| `stream` | `boolean` | 启用流式响应（必填） | 全部 API（Sandbox、Application Call、Qwen API、Realtime API） | 默认为 `false`；设为 `true` 后响应头 `Content-Type` 变为 `text/event-stream` |
| `incremental_output` | `boolean` | 控制流式内容是否为纯增量（仅新增部分） | Sandbox、Application Call（DashScope）、Qwen API（DashScope） | 仅在 `stream: true` 时生效；设为 `false`（默认）时，每帧返回从开头累计的完整文本（易造成前端重复渲染） |
| `X-DashScope-SSE` | HTTP Header | 显式声明启用 SSE 流式传输 | Application Call（DashScope 原生 API） | 必须设为 `enable`，否则 `stream: true` 不生效 |
| `store`（Responses API） | `boolean` | 控制流式响应是否可被后续请求引用（如 `previous_response_id`） | Application Call（Responses API） | 若 `store: false`，则流式响应不可复用，适用于临时调试场景 |

> ⚠️ 提示：所有流式响应均需客户端正确处理 SSE 协议（监听 `data:` 字段、解析 JSON、处理 `event: message` 和 `event: error`）。推荐使用百炼官方 SDK（Python/JS/Java），其内置流式解析器并自动处理重连、超时与错误恢复。

## 面向开发者：最佳实践建议

- **前端渲染**：始终使用 `incremental_output: true`（或 Anthropic/Responses 的原生增量行为），避免手动拼接导致的重复、错乱；对 Markdown 内容（如 `**bold**`）需在客户端解析，平台不提供富文本转换。
- **错误处理**：流式请求可能中途中断（如网络抖动、token 超限）。务必监听 `finish_reason` 字段（`"stop"` 正常结束，`"length"` 截断，`"error"` 异常），并实现 fallback 逻辑（如显示“生成中断，请重试”）。
- **性能权衡**：流式不降低总延迟（首 token 时间 + 总生成时间不变），但显著改善首屏响应速度（TTFT）。若关注端到端延迟，应优先优化 `temperature`、`top_p` 及 [prompt](../guides/prompt.md) 长度。
- **调试技巧**：Sandbox 控制台支持一键开启流式并实时渲染；API 调试时可用 `curl -N` 或 Postman 的 SSE 插件直接查看原始事件流。
- **合规注意**：流式响应日志同样遵循百炼数据治理规范，7 天后自动清除，不用于模型训练。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


