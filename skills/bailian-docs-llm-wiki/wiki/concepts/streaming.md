# 流式输出

流式输出（Streaming）是指模型在生成过程中将结果以增量片段（chunk / delta / 事件）形式逐步返回给客户端，而不是等全部内容生成完毕后一次性返回。它能显著降低首字延迟（TTFT），是构建实时对话、语音交互等体验的基础能力。

## 在百炼平台不同场景中的使用

### 文本生成模型 API

百炼的四类文本生成接口（OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages、DashScope 原生接口）均支持流式输出：

- **[OpenAI 兼容接口](openai-compatible-interface.md)**：在请求中设置 `stream=true`，服务端以 SSE（Server-Sent Events）分块返回增量内容，可直接复用官方 OpenAI 客户端库的流式迭代方式。
- **DashScope 原生接口**：功能与参数最完整，同样支持流式返回，适合需要平台全部能力的场景。
- 跨接口迁移时注意流式响应的字段结构以各生态的约定为准，需核对参数与返回格式的映射。

### 智能体 / 工作流应用调用

通过 Responses API（OpenAI 兼容）或 DashScope API 调用百炼应用时，均支持流式输出：

- **Responses API**：请求参数 `stream`（boolean，默认 `false`），设为 `true` 即可流式接收应用回复；耗时任务可另设 `background=true` 走异步模式。
- **DashScope API**：调用 `POST /api/v1/apps/{APP_ID}/completion` 时开启流式，结合 `session_id` 维护多轮对话上下文。

### 实时[多模态](multimodal.md)交互（Realtime API）

Qwen-Omni-Realtime 等实时接口基于 WebSocket / WebRTC / AOQ 协议，将流式思想扩展到音频与图像：

- **流式输入**：客户端通过 `input_audio_buffer.append` 持续追加音频帧、`input_image_buffer.append` 追加视频帧，VAD 模式下服务端自动检测语音起止并提交。
- **流式输出**：服务端以事件流下发增量结果，如 `response.audio.delta`（音频分片）、`response.function_call_arguments.delta`（工具调用参数增量）、`conversation.item.input_audio_transcription.delta`（实时转录预览）等，客户端边收边播实现低延迟对话与打断。
- 流式 ASR（FunASR 系列）与流式 TTS（CosyVoice 系列）也基于 WebSocket 流式协议工作。

### Managed Agents（智能体托管）

托管智能体的会话事件通过 SSE 长连接流式推送：调用 `GET /sessions/{session_id}/events/stream` 订阅，即可实时接收用户消息回执、工具调用、状态变更等事件，无需轮询。

## 关键参数与配置

| 场景 | 参数 / 机制 | 说明 |
| --- | --- | --- |
| 文本生成 / 应用调用 | `stream=true` | 开启 SSE 流式返回，默认 `false` |
| Realtime API | `*.delta` 事件 | 音频、文本、转录、工具参数均以 delta 事件增量下发 |
| Realtime API | `turn_detection` | `server_vad` 自动断句触发流式响应；置 `null` 则手动 commit |
| Managed Agents | `GET .../events/stream` | SSE 长连接订阅会话事件流 |

## 开发建议

- 交互式聊天、语音助手等对首响应时间敏感的场景优先开启流式；离线批处理或需要完整结果再处理的场景可用非流式或异步（`background=true`）。
- 客户端需按增量拼接内容，并妥善处理流中断、错误事件与重连逻辑。
- 流式与工具调用可以叠加：工具调用参数本身也会以增量事件下发（如 Realtime 的 `response.function_call_arguments.delta`），收齐后再执行工具并回传结果。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../guides/realtime-api-user-guide.md)
- [managed agents api](../api/managed-agents-api.md)


