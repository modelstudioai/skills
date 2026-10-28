# 流式输出

流式输出（Streaming Output）是指模型服务将生成结果以增量方式、按 token 或语义单元分块返回给客户端的通信模式，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户感知响应速度，是构建实时对话、语音交互、长文本生成等低延迟场景的核心能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准大模型 API（`/v1/chat/completions`）**：通过设置 `stream: true` 启用流式响应，服务端以 Server-Sent Events（SSE）格式逐 chunk 返回 `delta.content`，适用于 Web 控制台、聊天应用等需“边打字边显示”的场景。  
- **Realtime API（WebSocket）**：原生流式设计，不支持同步调用；通过 `output.text.delta` 等事件实时推送 token、音频片段或中间状态，专用于语音转写、视频帧理解等毫秒级交互场景。  
- **Application Call（智能体/工作流调用）**：`stream: true` 可启用应用级流式输出，但需满足前置条件——工作流节点必须在控制台显式开启“流式输出”开关并重新发布；新版智能体默认支持，旧版智能体与工作流需确认模型及节点配置兼容。  
- **Audio API（语音合成/识别等）**：使用 `enable_stream: true` 参数（注意参数名与模型 API 不同），配合 `Accept: text/event-stream` Header，以 SSE 方式流式返回音频二进制分片（如 TTS 的 WAV chunk）或识别文本片段（如 ASR 的实时字幕）。  
- **Test 1 服务**：同样支持 `stream: true`，但需注意：流式调用不参与部分资源包抵扣，且 `max_tokens` 实际截断行为受服务端缓冲策略影响，建议预留余量。

## 关键参数和配置

| 接口类型         | 参数名           | 类型    | 默认值 | 说明 |
|------------------|------------------|---------|--------|------|
| 模型 API / Application Call（DashScope） | `stream` | boolean | `false` | 必须显式设为 `true` 才启用流式；响应格式为 SSE（`text/event-stream`）。 |
| Application Call（OpenAI 兼容 Responses API） | `stream` | boolean | `false` | 行为与 OpenAI 一致；注意 `background=true` 时不可设为 `true`。 |
| Realtime API     | `stream`         | query string（固定 `true`） | — | URL 查询参数，不可省略；实际流式行为由 WebSocket 协议承载。 |
| Audio API        | `enable_stream`  | boolean | `false` | 注意命名差异；启用后需设置 `Accept: text/event-stream` 并按 SSE 解析。 |
| 所有流式接口     | `response_format` | string | `delta`（Realtime）、`json`（其他） | Realtime API 中 `delta` 表示 token 级增量，`json` 表示完整响应；其他接口通常忽略此参数或仅影响非流式路径。 |

> ⚠️ 重要限制：  
> - 流式响应不支持异步调用（`background=true`）；  
> - 流式连接超时后需主动重连（Realtime API 单连接 ≤300 秒，RESTful 流式无硬性超时但建议客户端设置 60s+ 超时）；  
> - 流式调用的 `max_tokens` 是软上限，服务端可能因缓冲策略提前终止，建议设置比预期多 10% 的余量。

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求 body（或 URL query）中加入 `"stream": true`，并确保请求头含 `Accept: text/event-stream`（RESTful）或建立 WebSocket 连接（Realtime）。  
- ✅ **解析建议**：使用标准 SSE 客户端库（如 `eventsource`、`fetch` + `ReadableStream`）处理 `data:` 字段；聚合 `delta.content` 即可获得完整文本，无需手动拼接 event type。  
- ✅ **错误处理**：监听 `error` 事件与 HTTP 4xx/5xx 响应；Realtime API 遇 `4290` 错误需指数退避重连（初始间隔 ≥1s）。  
- ❌ **避免陷阱**：不要在流式响应中依赖 `usage` 字段（它只在最后 `done` 事件中出现）；不要对流式响应做同步阻塞渲染（应使用增量更新 UI）。  
- 📦 **调试工具**：`curl -N` 可直接观察流式原始输出；浏览器 DevTools 的 Network → Response 面板支持 SSE 流式预览。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [test 1](../guides/test-1.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)
- [audio api references](../api/audio-api-references.md)


