# 流式输出

流式输出（Streaming Output）是百炼平台中一种将模型响应分块、实时、渐进式返回给客户端的通信机制，而非等待整个响应生成完毕后一次性返回。它显著降低端到端延迟，提升交互自然度，是构建低延迟语音助手、实时翻译、长文本生成等体验的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一接口特性，而是贯穿多类 API 的通用交互范式，具体应用方式依协议与场景而异：

- **Realtime API（omni-realtime / realtime）**：基于 WebSocket 或 AOQ 协议，采用**事件驱动流式**。服务端按语义单元（如 ASR 词片段、LLM token、TTS 音频帧）持续推送结构化事件（如 `output.text.delta`、`output.audio.delta`），客户端需逐帧解析、拼接并渲染。适用于语音输入→文本+语音同步输出的全链路实时交互。

- **Qwen API（OpenAI/Anthropic/DashScope 兼容）**：通过标准 `stream: true` 参数启用**SSE（Server-Sent Events）流式**。服务端以 `data: {...}` 行格式持续返回 `chunk` 对象（含 `delta.content`、`delta.tool_calls` 等），客户端按行解析并累积内容。适用于 Web 应用、CLI 工具等需要文本渐进渲染的场景。

- **应用组件 API（Application Component）**：同样支持 `stream: true`，但**强制使用 SSE 协议**（不支持 WebSocket）。返回格式与 Qwen API 兼容，适合企业级 RAG 应用集成，需配合前端 SSE EventSource 或后端流式 HTTP 客户端处理。

- **开发工具链（CLI/IDE 插件/Web 平台）**：所有基于 OpenAI 或 Anthropic 兼容协议的工具（如 Hermes Agent、Cursor、Dify）均自动识别 `stream: true` 并实现本地流式渲染（如打字机效果），开发者无需额外编码即可获得流式体验。

> ⚠️ 注意：流式能力与模型和协议强绑定。例如，ASR/TTS 模型仅在 Realtime API 中支持流式；`Qwen-Audio` 不支持 OpenAI 协议，故无法通过 [OpenAI 兼容接口](openai-compatible-api.md)启用流式；WebRTC 协议虽属 Realtime API，但其媒体流本身即为天然流式，不依赖 `stream` 参数控制。

## 关键参数和配置

| 参数 | 所属 API | 类型 | 说明 | 默认值 |
|------|----------|------|------|--------|
| `stream` | Qwen API、应用组件 API | boolean | 启用流式响应（SSE） | `false` |
| `enable_interim_results` | Omni Realtime API | boolean | 启用 ASR 中间结果（非最终识别词）流式推送 | `false`（生产环境建议保持） |
| `modalities` | Realtime API | string[] | 指定流式输出模态，如 `["text"]`、`["text","audio"]`，决定接收哪些 `.delta` 事件 | `["text"]` |

- **协议约束**：
  - Realtime API（WebSocket/AOQ）：流式由协议原生承载，无需 `stream` 参数；`enable_interim_results` 是其专属开关。
  - Qwen API / 应用组件 API：必须显式设置 `stream: true`，且仅支持 SSE；WebSocket 不被支持。
- **鉴权与端点**：流式请求仍需标准 `Authorization: Bearer <API_KEY>`，且 Base URL 必须与所选方案（Token Plan / Coding Plan / 按量计费）及地域严格匹配。

## 面向开发者，简洁实用

- ✅ **快速启用**：在 Qwen API 或应用组件 API 的请求体中添加 `"stream": true`，即可获得文本流式响应；在 Realtime API 中，建立 WebSocket 连接后默认即为流式，关注 `output.*.delta` 事件即可。
- ✅ **处理建议**：
  - 使用官方 SDK（如 Python/Java Realtime SDK、OpenAI Python SDK）——它们已封装流式解析逻辑，避免手动处理 SSE 分隔符或 WebSocket 二进制帧。
  - 前端使用 `EventSource` 处理 SSE；服务端推荐使用支持流式 HTTP 的客户端（如 `aiohttp`、`fetch` + `ReadableStream`）。
  - 对于 Realtime API，务必监听 `response.done` 事件作为流结束信号，而非依赖超时。
- ❌ **避坑提示**：
  - 不要对 `enable_interim_results: true` 的中间结果做最终状态判断（如存库、触发动作），因其可能被后续 `is_final: true` 事件覆盖。
  - 流式响应中 `usage` 字段仅在最后 `done` 事件中完整返回，切勿在中间 chunk 中解析。
  - Token Plan/Coding Plan 的凭证**不支持**在 Postman/cURL 中调试流式请求（因缺少 SSE 自动重连与解析），请改用 SDK 或支持 SSE 的专用工具（如 `sse-cli`）。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application component api reference](../api/application-component-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


