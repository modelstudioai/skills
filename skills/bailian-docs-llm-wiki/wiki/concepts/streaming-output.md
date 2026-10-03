# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种响应模式，允许模型推理结果以增量方式（如逐 token、逐 chunk 或逐事件）实时返回给客户端，而非等待整个响应生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，是构建实时对话、语音助手、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台的多个核心接口中统一支持，但启用方式、协议承载和语义细节因场景而异：

- **Application Call（智能体/工作流调用）**：  
  支持 DashScope 原生 API 和 OpenAI 兼容的 Responses API。DashScope API 需在请求 Header 中设置 `X-DashScope-SSE: enable` 并传入 `stream=true`；Responses API 则直接在 JSON Body 中设置 `"stream": true`。响应格式为 Server-Sent Events（SSE），每条事件含 `data:` 字段，包含 `delta`（增量内容）、`finish_reason` 等字段。

- **Realtime API（低延迟音视频流）**：  
  基于 WebSocket 协议原生流式设计，不依赖 SSE。客户端通过 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 建立连接后，服务端持续推送 `output.text.delta`、`output.audio.delta` 等事件，支持毫秒级响应与实时中断（`control.interrupt`）。

- **Omni Realtime API（多模态实时交互）**：  
  同样基于 WebSocket，支持 `input_audio`/`input_text`/`input_image` 混合输入，并返回 `response.text_delta`、`response.audio.delta` 等结构化事件。特别支持 `enable_interim_results=true` 获取 ASR 中间识别结果。

- **[OpenAI 兼容接口](openai-compatible-interface.md)（Chat / Responses）**：  
  完全遵循 OpenAI 流式规范：设置 `"stream": true` 后，响应为 `text/event-stream` 类型的 SSE 流，每行以 `data:` 开头，含 `choices[0].delta.content` 字段。`finish_reason` 字段标识流结束原因（如 `"stop"`、`"length"`、`"tool_calls"`）。

- **Application Support（应用层增强）**：  
  提供 `incremental_output=true` 参数（需与 `stream=true` 同时启用），用于避免重复返回历史内容——即仅推送本次推理新增的 token，适用于前端需精确控制渲染增量的场景（如打字机效果、实时编辑预览）。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 所属接口 | 备注 |
|--------|------|------|-----------|------|
| `stream` | boolean | 启用流式响应（必选） | 全部 | 默认 `false`；设为 `true` 是启用流式的基础前提 |
| `X-DashScope-SSE` | string | Header 字段，值为 `enable` | DashScope 原生 API（Application Call） | 仅 DashScope API 需显式设置；Responses API 不需要 |
| `incremental_output` | boolean | 启用增量式流式（仅返回新增内容） | Application Call（Application Support） | 必须与 `stream=true` 同时设置，否则无效 |
| `enable_interim_results` | boolean | 启用 ASR 中间识别结果（partial transcript） | Omni Realtime API | 开启后将额外触发 `interim_transcript` 事件 |
| `max_latency_ms` | integer | Realtime API 端到端最大延迟容忍（毫秒） | Realtime API | 影响服务端调度策略，默认 `300`，取值范围 `100–2000` |

> ⚠️ 注意：所有流式接口均要求客户端正确处理分块响应（SSE 或 WebSocket 事件），并实现超时重连、心跳保活（WebSocket 场景）、错误恢复等健壮性逻辑。未按规范解析可能导致内容截断或乱序。

## 面向开发者：实用建议

- **首选 OpenAI 兼容模式**：若已使用 OpenAI SDK，优先选用 `/compatible-mode/v1/responses` 路径，`stream=true` 行为与 OpenAI 完全一致，迁移成本最低。
- **前端渲染优化**：启用 `incremental_output=true` 可避免前端重复拼接历史内容，减少 DOM 操作开销；配合 `delta.content` 累加即可获得完整响应。
- **错误处理必须覆盖**：流式请求可能中途失败（如网络中断、token 超限）。务必监听 `error` 事件（WebSocket）或 `event: error`（SSE），并实现降级逻辑（如 fallback 到非流式重试）。
- **不要忽略 `finish_reason`**：该字段明确指示流为何终止（`"stop"`=正常结束，`"length"`=达到 max_tokens，`"tool_calls"`=触发插件调用），是判断响应完整性与后续动作的关键依据。
- **调试技巧**：使用 `curl -N` 或浏览器开发者工具的 Network → EventStream 标签页可直观查看 SSE 流；WebSocket 场景推荐使用 [wscat](https://github.com/websockets/wscat) 工具快速验证连接与事件。

## 关联主题页

- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application support](../guides/application-support.md)


