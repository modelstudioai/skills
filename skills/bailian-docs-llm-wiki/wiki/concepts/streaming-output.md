# 流式输出

流式输出（Streaming Output）指模型在生成过程中将结果以分块方式逐步返回给客户端，而非等待整体生成完成后一次性返回。开发者可在首 token 产出时即开始处理，从而显著降低首字延迟、改善交互体验，并支持边生成边消费的实时场景。

## 在百炼平台的使用方式

百炼的流式输出按接入协议与生成任务类型分为三种形态：

### 1. 文本生成流式（SSE）

Qwen 系列文本模型通过 OpenAI 兼容、Anthropic 兼容或 DashScope 原生接口调用时，统一以 **Server-Sent Events (SSE)** 形式增量返回。在请求体中将 `stream` 设为 `true`，响应体按 `data: {chunk}\n\n` 逐 chunk 推送 `delta` 内容，最后一个 chunk 携带 `finish_reason` 与 usage 统计。

- OpenAI 兼容接口：`POST /compatible-mode/v1/chat/completions`，字段与 OpenAI 客户端一致，可直接复用 SDK 的 stream 读取逻辑。
- Anthropic 兼容接口：`POST /compatible-mode/v1/messages`，沿用 Anthropic `message_delta` / `content_block_delta` 事件结构，支持 thinking 与工具调用增量。
- DashScope 原生接口：使用 `X-DashScope-SSE` 请求头启用，输出体为 SSE 流，参数集最完整。

### 2. 实时多模态流式（WebSocket 双向消息）

Qwen-Omni-Realtime 通过 WebSocket 长连接实现低延迟语音/视频对话，与文本 SSE 不同，它是双向事件流：

- 客户端通过 `input_audio_buffer.append` 持续推送 Base64 音频片段；
- 服务端流式返回 `response.audio.delta`、`response.audio_transcript.delta` 等增量事件，实现"边听边说"。
- 配合 VAD 模式可自动检测语音起止，配合 Manual 模式则由客户端显式 `response.create` 触发生成。

声音复刻、工具调用、联网搜索等能力均在该流式通道内完成，无需额外端点。

### 3. Managed Agents 事件流（SSE）

托管智能体在 Session 写入用户消息后，通过 SSE 端点 `GET /sessions/{session_id}/events/stream` 持续接收 Agent 的运行事件（思考、工具调用、回复文本等），直至 Session 回到 `idle`。该流式通道承载整个 Agent 执行生命周期，适合构建交互式 Agent UI。

### 4. 异步任务的非流式约定

注意：图像、视频生成类接口（万相、HappyHorse、Kling 等）**不支持流式输出**，统一采用「创建任务得 `task_id` → 轮询 `GET /tasks/{task_id}`」的异步模式。视频任务通常耗时 1–5 分钟，需按建议间隔轮询，不应将其与流式输出混淆。

## 关键参数与配置

| 参数 / 头部 | 适用接口 | 作用 |
| --- | --- | --- |
| `"stream": true` | OpenAI / Anthropic 兼容、DashScope 原生 Chat | 启用 SSE 流式返回 |
| `X-DashScope-SSE: enable` | DashScope 原生接口 | 启用流式（部分原生接口必需） |
| `stream_options.include_usage` | OpenAI 兼容 | 在末尾 chunk 携带 token usage 统计 |
| WebSocket `session.update` | Omni Realtime | 配置 VAD、音色、工具等会话级参数 |
| `idle_timeout_ms` | `qwen3.5-omni-plus-realtime` 等 | 静默超时后模型主动引导对话 |
| `Accept: text/event-stream` | Managed Agents events/stream | 声明接收 SSE 事件流 |

## 开发者注意事项

- **首字延迟 vs 总延迟**：流式不缩短总生成时间，但显著缩短首 token 等待，适合聊天、Agent 回复等交互场景。
- **断连与重试**：SSE 与 WebSocket 均为长连接，网络抖动会中断流；建议记录已消费的 chunk 序号以便续接，或降级为非流式重试。
- **工具调用**：流式下工具调用参数也是分块到达，需按 `tool_call_delta` 累积拼接后再执行。
- **地域一致性**：实时多模态与托管 Agent 必须使用与 API Key 同地域的专属域名（如 `ws_xxx.cn-beijing.maas.aliyuncs.com`），跨地域会失败。
- **[上下文窗口](context-window.md)**：流式不改变上下文限制，长对话仍需调用方截断或依赖 Responses 接口的自动历史管理。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [video generation api](../api/video-generation-api.md)
- [managed agents api](../api/managed-agents-api.md)


