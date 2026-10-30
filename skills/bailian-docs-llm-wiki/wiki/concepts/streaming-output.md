# 流式输出

流式输出（Streaming Output）是指模型 API 在生成响应过程中，将结果以连续、分块的方式实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种机制显著降低端到端延迟，提升用户体验，尤其适用于对话交互、语音合成、长文本生成等对实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非单一功能，而是贯穿多个协议与服务层的通用能力，具体使用方式依调用路径而异：

- **标准 REST API（Application Support / Qwen API / Audio API）**：通过请求参数 `stream=true` 启用，响应格式为 Server-Sent Events（SSE），每条事件包含一个 `data:` 行（如 `data: {"delta": "你好", "finish_reason": null}`）。适用于 HTTP 客户端（如 `fetch`、`curl` 或 `dashscope` SDK 的 `stream=True` 模式）。

- **Realtime API（WebSocket / AOQ / WebRTC）**：原生支持双向流式通信，无需显式设置 `stream` 参数。服务端主动推送结构化事件（如 `response.text.delta`、`response.audio.delta`、`input_audio_buffer.speech_started`），客户端按事件类型实时处理。这是语音助手、实时会议纪要等低延迟场景的首选方式。

- **Omni Realtime API**：基于 WebSocket 协议，以事件驱动模型实现细粒度流控。例如，`response.audio.delta` 事件逐帧推送 PCM 音频数据，`response.text.delta` 推送文字片段，配合 `smooth_output` 等参数可实现自然停顿与语义连贯输出。

- **多模态与音频专用接口**：所有音频类 API（ASR/TTS/Audio Generation）均明确支持流式响应；Qwen 多模态模型（如 `qwen3.8-omni-flash`）在 DashScope 原生协议下也支持流式文本输出，但 OpenAI 兼容协议中部分多模态字段（如 `image_url`）不参与流式解析。

> ⚠️ 注意：流式模式下，`usage`（token 统计）仅在最终 `done` 事件或流结束 chunk 中完整返回；中间 chunk 的 `usage` 字段为 `null` 或缺失。

## 关键参数和配置

| 参数 | 类型 | 作用域 | 说明 |
|------|------|--------|------|
| `stream` | boolean | REST API（Application Support / Qwen / Audio） | 必填开关，默认 `false`；设为 `true` 后启用 SSE 流式响应。SDK 中通常对应 `stream=True` 或 `stream: true`。 |
| `modalities` | string[] | Realtime / Omni Realtime API | 控制输出模态组合，如 `["text"]`（仅文本流）、`["text","audio"]`（文本+音频双流）。影响服务端推送的事件类型。 |
| `smooth_output` | boolean | Omni Realtime（仅 `qwen3.8-omni-flash-realtime`） | 启用语义级平滑输出，自动插入合理停顿与语气词，使流式 TTS 更自然；默认 `true`。 |
| `max_tokens` | integer | 所有流式接口 | **硬性截断阈值**：达到该值时服务端强制终止流并发送 `finish_reason="length"`。非建议值，不可省略用于流控。 |
| `temperature` / `top_p` | float | 全部 | 影响流式输出的多样性与稳定性；建议避免同时设为 `0`（确定性冲突），详见 [Application Support](../../raw/application-user-guide/application-support.md) 参数约束说明。 |

- **HTTP Header 要求（REST 流式）**：必须设置 `Accept: text/event-stream`，否则返回 `406 Not Acceptable`。
- **连接超时**：流式请求需延长客户端超时时间（推荐 ≥ 120 秒），避免因网络空闲中断连接；`preparations` 文档建议显式配置 `timeout=60` 以上。
- **错误处理**：流式响应中若发生错误，服务端会推送 `event: error` + `data: {"code": "...", "message": "..."}`，客户端应监听并终止解析。

## 面向开发者：简洁实用提示

- ✅ **优先使用 SDK**：`dashscope` Python SDK（v1.18.0+）和官方 AOQ/Realtime SDK 已封装流式解析逻辑，避免手动处理 SSE 格式或 WebSocket 事件循环。
- ✅ **流式必校验 `finish_reason`**：`stop`（正常结束）、`length`（被 `max_tokens` 截断）、`tool_calls`（触发[函数调用](function-calling.md)）—— 不同原因决定后续逻辑（如是否追加 `tool_result`）。
- ❌ **勿在前端硬编码 API Key**：流式请求仍需 `Authorization` 头，密钥泄露风险更高；务必通过后端代理转发。
- ⚡ **Realtime 场景禁用 REST 流式**：语音对话等强实时需求必须使用 WebSocket/AOQ 协议，HTTP SSE 无法满足 <500ms 端到端延迟要求。
- 📉 **监控流中断**：生产环境应记录 `stream interrupted` 日志，并捕获 `onclose` / `onerror` 事件，实现自动重连（Realtime SDK 已内置）。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)


