# 流式输出

流式输出（Streaming Output）是百炼平台中一种实时、增量返回模型响应内容的通信模式，适用于需要低延迟交互、长文本生成或实时语音合成等场景。它通过持续发送分块数据（如 token、音频帧、文本片段），使客户端能在模型推理过程中逐步消费结果，而非等待整个响应完成。

## 在百炼平台的不同场景中，这个概念如何使用

- **Application Call（智能体/工作流调用）**：支持 DashScope 原生 API 和 OpenAI 兼容 Responses API。启用后，服务端以 Server-Sent Events（SSE）格式逐块返回 `content`、`tool_calls`、`thought`（若开启思考模式）等字段；适用于客服对话、RAG 实时检索反馈、多步骤 Agent 执行过程可视化等场景。注意：Responses API 的异步调用（`background=true`）不支持流式输出。

- **Omni Realtime API（多模态实时语音交互）**：基于 WebSocket 的原生流式协议，同时输出文本增量（`conversation.item.output.text.delta`）和音频流（`conversation.item.output.audio.delta`），支持 VAD 触发下的实时打断与重写，是构建语音助手、智能座舱等低延迟应用的核心能力。

- **Realtime API（ASR/TTS 专用）**：同样基于 WebSocket，提供 ASR 中间识别结果（`response.text.delta`）和 TTS 合成音频流（`response.audio.delta`），支持毫秒级端到端延迟，适用于实时字幕、语音会议转录等强实时性需求。

- **Sandbox（沙箱调试环境）**：支持流式推理，返回 `choices[0].delta.content` 格式的增量文本，便于开发者在本地快速验证提示词效果、token 消耗节奏及结构化输出稳定性，无需等待完整响应即可观察模型行为。

- **Toolkits & Frameworks（[OpenAI 兼容接口](openai-compatible-api.md)）**：`chat/completions` 和 `responses` 接口完全兼容 OpenAI 的 `stream=true` 参数；部分视觉模型（如 `QVQ`）**仅支持流式输出**，必须启用该模式才能正常调用。`completions` 和 `embeddings` 接口则不支持流式。

## 关键参数和配置

| 接口类型 | 启用方式 | 关键参数/头信息 | 增量控制 | 注意事项 |
|----------|-----------|------------------|------------|------------|
| **Application Call (DashScope)** | Header 控制 | `X-DashScope-SSE: enable` | `incremental_output=true`（返回 delta）<br>`false`（返回全量追加） | `stream` 字段在请求体中不生效，仅靠 Header 控制；`incremental_output` 仅在流式下有效 |
| **Application Call (Responses API)** | 请求体字段 | `"stream": true` | 默认 delta 输出（OpenAI 兼容） | 异步调用（`"background": true`）禁止设置 `stream=true`，否则报错 |
| **Omni Realtime / Realtime API** | WebSocket 协议内建 | 无显式参数，连接即启用流式 | 由事件类型天然区分（`.delta` 事件即为增量） | 必须维持 WebSocket 长连接；需按帧解析 `delta` 事件并拼接 |
| **Sandbox** | 请求体字段 | `"stream": true` | OpenAI 兼容 delta 格式（`choices[0].delta.content`） | 不支持 `stream=false` 与 `stream=true` 混合调用同一实例；超时销毁逻辑不受流式影响 |
| **[OpenAI 兼容接口](openai-compatible-api.md)（chat/responses）** | 请求体字段 | `"stream": true` | 完全遵循 OpenAI streaming JSON Lines 格式 | 使用 `base_url` 必须为业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），否则流式响应可能中断 |

> ⚠️ 通用限制：所有流式接口均不支持 HTTP 重定向；客户端需正确处理 chunked transfer encoding 或 WebSocket message 分片；建议设置合理的连接超时（推荐 ≥ 120s）以应对长生成任务。

## 面向开发者，简洁实用

- ✅ **优先启用流式**：只要前端能处理增量数据（如 React useEffect + useState 追加渲染、WebSocket onmessage 解析），就应默认开启 `stream=true` —— 它显著降低首字节延迟（TTFB），提升用户体验。
- ✅ **拼接 delta 而非依赖 finish_reason**：`delta.content` 可能为空（如工具调用前的空格），请始终检查 `delta.content` 是否存在且非空再追加；最终响应以 `event: done` 或 `finish_reason` 字段为准。
- ✅ **错误处理要流式感知**：流式响应中可能夹杂 `error` 事件（如 Omni Realtime 的 `error` 事件、Responses 的 `{"error":{...}}` chunk），需在接收循环中实时捕获并中断。
- ❌ **勿在流式中混用同步语义**：例如 Application Call 的 `stream=true` 与 `background=true` 冲突；Realtime API 不支持 HTTP GET 轮询模拟流式。
- 🛠️ **调试建议**：使用 `curl -N`（禁用缓冲）测试 SSE；用 `wscat` 连接 Realtime API 查看原始事件；Sandbox 流式响应可直接用 `openai` Python SDK 的 `stream=True` 复用现有逻辑。

## 关联主题页

- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [sandbox](../guides/sandbox.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


