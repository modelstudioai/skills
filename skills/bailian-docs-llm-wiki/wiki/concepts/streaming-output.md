# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型服务将生成结果以增量方式分块、低延迟地持续返回，而非等待全部内容完成后再一次性返回。该机制显著降低端到端延迟，提升用户体验，尤其适用于对话交互、实时语音处理、长文本生成等对响应速度和渐进式反馈敏感的场景。

## 在百炼平台的不同场景中如何使用

- **标准大模型 API（如 `text-generation`）**：通过在请求参数中设置 `stream: true`，启用基于 Server-Sent Events（SSE）协议的流式响应。服务端按 token 或语义 chunk 分批返回 `output.choices[0].delta.content`，客户端需逐行解析 `data:` 字段并拼接渲染。
  
- **Realtime API 与 Omni Realtime API（WebSocket 场景）**：流式为默认行为（`stream` 参数默认 `true`），采用事件驱动模型。服务端通过结构化事件（如 `output.text.delta`、`transcript`、`audio.chunk`）实时推送中间结果，支持 ASR 实时转写、TTS 音频流、多模态帧级理解等毫秒级交互。

- **音频类 REST API（ASR/TTS/Conversation）**：在 `audio/asr`、`audio/tts` 等接口中，设置 `stream: true` 后，响应头为 `Content-Type: text/event-stream`，返回符合 SSE 格式的分块数据；ASR 场景下需关注 `is_final` 字段判断结果是否稳定。

- **应用层（Application / Agent）**：除 `stream: true` 外，可额外启用 `incremental_output: true`，确保每个流式 chunk 仅包含本次新增 token（非全量重传），便于前端实现“打字机效果”等精准 UI 渲染。

> ⚠️ 注意：流式响应不可直接 `JSON.parse()` 整个响应体；必须按行解析 SSE 格式（每行以 `data:` 开头，空行分隔），并忽略 `event:`、`id:`、`retry:` 等控制字段。

## 关键参数和配置

| 参数名 | 类型 | 默认值 | 说明 | 支持场景 |
|--------|------|--------|------|----------|
| `stream` | boolean | `false` | 启用流式响应模式 | 所有 REST API（text-generation、audio/*）、Application API |
| `incremental_output` | boolean | `false` | 在 `stream=true` 下启用增量式输出（每个 chunk 仅含新内容，无重复） | Application / Agent API（如 `/v1/agents/run`, `/v1/chat/completions`） |
| `enable_interim_results` | boolean | `true` | 控制是否返回中间识别/生成结果（如 ASR 的 partial transcript） | Omni Realtime API、Realtime API |
| `max_latency_ms` | integer | `300–500`（依文档略有差异） | 服务端调度延迟上限（毫秒），影响流式 chunk 的触发节奏 | Omni Realtime API（关键 QoS 控制参数） |

- **REST 场景**：`stream=true` 时，HTTP 响应状态码仍为 `200 OK`，但响应体为 SSE 流；超时需由客户端主动控制（建议设置 `timeout: 120000`）。
- **WebSocket 场景**：无需显式传 `stream`，连接即默认流式；通过 `session.update` 事件配置 `enable_interim_results` 和 `max_latency_ms`。
- **错误处理**：流式过程中若发生错误（如模型中断、鉴权失败），服务端会发送 `event: error` 或 `error.code` 事件，客户端应监听并终止流。

## 面向开发者：简洁实用提示

- ✅ **必做**：前端使用 `EventSource`（浏览器）或 `SSE client` 库（Node.js/Python）解析流；WebSocket 客户端需注册 `message` 事件处理器。
- ✅ **推荐**：启用 `incremental_output=true` 避免前端重复渲染；对 ASR/TTS 流，务必校验 `is_final` 或 `event` 类型再提交业务逻辑。
- ❌ **禁止**：对流式响应调用 `response.json()`；在未关闭连接前重复发送同一会话的 `input.audio` 帧（Realtime API 要求严格顺序）。
- 🛠️ **调试技巧**：用 `curl -N` 查看原始 SSE 流；检查响应头 `Content-Type: text/event-stream` 是否存在；确认 `Access-Control-Allow-Headers` 包含 `Authorization`（跨域场景）。
- ⏱️ **性能提示**：流式不降低总生成耗时，但显著改善首 token 延迟（Time to First [Token](token.md), TTFT）；实际 P95 TTFT 通常 < 800ms（依赖模型与网络）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)
- [audio api references](../api/audio-api-references.md)


