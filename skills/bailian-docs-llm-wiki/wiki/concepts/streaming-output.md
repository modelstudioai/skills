# 流式输出

流式输出（Streaming Output）指模型在生成响应时，将文本、音频、视频或工具调用参数等内容以增量（delta）片段的形式逐步返回给客户端，而非等待整段结果一次性返回。百炼平台在文本生成、实时多模态交互、应用调用等多种场景中均支持流式输出，可显著降低首字延迟并提升交互体验。

## 适用场景

- **文本生成**：通过 OpenAI 兼容 Chat Completions、Responses、Anthropic 兼容 Messages 或 DashScope 原生接口调用 Qwen 系列模型时，可开启流式返回，逐 token 输出文本，适合聊天机器人、智能客服等需要实时反馈的交互。
- **实时多模态交互**：Qwen-Omni-Realtime API 基于 WebSocket 协议实现低延迟双向流式通信，支持增量音频、增量文本转录以及工具调用参数的流式下发。
- **应用调用**：通过 [DashScope SDK](dashscope-sdk.md) 或 HTTP API 调用智能体应用、工作流应用时，可启用流式输出逐步接收应用执行结果。

## 文本生成的流式输出

文本生成接口通过请求参数开启流式返回，响应以 chunk 序列形式下发，每个 chunk 包含一段增量内容，最后一个 chunk 标记响应完成。各兼容协议的流式字段对齐其原生规范：

- **OpenAI 兼容 Chat Completions / Responses**：使用 `stream: true` 开启，响应为 `data:` 前缀的 SSE 事件流，末尾以 `data: [DONE]` 结束。
- **Anthropic 兼容 Messages**：使用 `stream: true` 开启，响应为符合 Anthropic 规范的事件流（`message_start`、`content_block_delta`、`message_stop` 等）。
- **DashScope 原生接口**：使用 `stream: true` 或 `incremental_output: true` 开启，可获取最完整的平台流式能力。

## 实时多模态的流式事件

Qwen-Omni-Realtime API 的流式输出通过 WebSocket 服务端事件实现，主要包括以下增量事件：

| 事件 | 说明 |
| --- | --- |
| `response.audio.delta` | 增量音频数据 |
| `response.audio_transcript.delta` | 增量文本转录 |
| `response.function_call_arguments.delta` | 工具调用参数的增量输出 |
| `response.created` / `response.done` | 响应开始 / 完成标记 |

与之配合的客户端事件如 `input_audio_buffer.append`、`input_image_buffer.append` 同样以增量方式上推音频（16 kHz PCM）和图像数据，实现双向流式交互。

## 关键参数与配置

- **`stream` / `incremental_output`**：布尔值，开启流式输出。
- **音频格式**：实时多模态场景下，输入音频仅支持 PCM 16 kHz，输出音频为 PCM 24 kHz，不支持自定义。
- **VAD 模式**：在实时交互中通过 `session.turn_detection` 设为 `server_vad` 或 `semantic_vad`，服务端自动检测语音起止并触发响应；`silence_duration_ms` 控制静音多久后触发响应（默认 800ms，范围 200–6000）。
- **Manual 模式**：将 `turn_detection` 设为 `null`，客户端通过 `input_audio_buffer.commit` 和 `response.create` 手动控制发送与响应节奏。
- **响应取消**：实时交互中可通过 `response.cancel` 取消正在进行的流式响应。

## 使用建议

- 对首字延迟敏感的场景（聊天、语音对话）优先开启流式输出。
- 需要完整结果后再处理（如结构化 JSON 抽取）时，可关闭流式或在客户端拼接完整响应后再解析。
- 实时多模态场景建议根据模型支持选择合适的 VAD 模式：`server_vad` 通用兼容，`semantic_vad` 可过滤回应语和背景音（仅 Qwen3.5-Omni-Realtime 系列支持）。
- 流式输出需在客户端正确处理 chunk 拼接与末尾结束标记，避免出现截断或重复。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [model inference](../guides/model-inference.md)


