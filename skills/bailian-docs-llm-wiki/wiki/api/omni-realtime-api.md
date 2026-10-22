# omni realtime api

Qwen-Omni-Realtime 是百炼平台提供的低延迟、多模态实时交互 API，支持语音输入/输出、文本生成、工具调用（Function Calling 和 MCP）及上下文感知的流式响应。它面向语音助手、智能客服、实时会议摘要等场景，通过 AOQ、WebSocket 或 WebRTC 协议实现端到端毫秒级交互。开发者需按协议规范发送客户端事件，并处理服务端返回的结构化事件流。

## 支持的模型与功能

当前支持以下模型：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输入支持 PCM/WAV（部分模型）、单/双/四声道；输出支持 PCM/WAV（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 明确限定 `output_audio_format` 当前仅支持 `pcm`，但 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 允许配置 `wav` 输出格式）。
- **语音活动检测（VAD）**：支持 `server_vad`（声学检测）和 `semantic_vad`（语义检测），后者可过滤背景音与回应语。
- **工具调用**：支持 Function Calling（`type=function`）和 MCP（`type=mcp`）两种机制；但 `tools` 与 `enable_search` 不兼容，不可同时启用。
- **联网搜索**：`qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列模型支持，需显式设置 `enable_search: true`。
- **视频输入（仅 qwen3.8-omni-flash-realtime）**：支持 `video.input.representation_compact` 配置以降低 [Token](../concepts/token.md) 开销。

> **注意**：文档 2 中 `session.created` 示例声明 `output_audio_format` “当前仅支持设为 `pcm`”，而文档 3 的 `session.update` 明确允许 `audio.output.format.type` 设为 `wav` 且示例中已使用。实际行为以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端在 `session.updated` 中会回显 `wav` 配置，表明该能力已上线。

## 关键参数

所有配置通过 `session.update` 客户端事件传递，关键字段如下：

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色标识 | `Tina`（多数模型） |
| `audio.input.format.type` | `string` | 输入格式：`pcm`（必选）或 `wav`（部分模型） | `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率：8000/16000/24000/48000 Hz（`qwen3.8` 仅支持 16000） | `16000` |
| `audio.output.format.type` | `string` | 输出格式：`pcm` 或 `wav` | `pcm` |
| `turn_detection.type` | `string` | VAD 类型：`server_vad` 或 `semantic_vad` | `server_vad` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发阈值（ms） | `800` |
| `enable_search` | `boolean` | 启用联网搜索 | `false` |
| `tools` | `array` | 工具定义列表（Function Calling 或 MCP） | — |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 采样控制参数 | 因模型而异（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)） |
| `max_tokens` | `integer` | 单次响应最大输出 [Token](../concepts/token.md) 数 | `65536`（`qwen3.8`） |

> **注意**：`input_audio_transcription.model` 固定为 `qwen3-asr-flash-realtime`，不可修改；`session.audio.input.format.sample_rate` 在 `qwen3.8-omni-flash-realtime` 多通道输入下强制为 `16000`，且 `sample_format`、`channels`、`packing` 等字段有严格约束（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或使用官方 SDK（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）。
2. **初始化会话**：连接后立即发送 `session.update` 事件配置参数（如 `modalities`、`voice`、`tools` 等）。
3. **输入数据**：
   - 音频：通过 `input_audio_buffer.append` 追加 Base64 编码 PCM/WAV 数据；VAD 模式下由服务端自动 `commit`，Manual 模式需主动发送 `input_audio_buffer.commit`。
   - 工具结果：`conversation.item.create` 回传后，发送 `response.create` 触发续答。
4. **控制响应**：发送 `response.cancel` 中断进行中的响应。
5. **处理事件**：监听服务端事件，如 `session.created`（初始配置）、`input_audio_buffer.speech_started/stopped`（VAD 状态）、`conversation.item.created`（消息/工具调用项）、`response.done`（响应结束）等。完整事件定义见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 和 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 限制和注意事项

- **协议限制**：AOQ/WebRTC 仅适用于特定终端场景；WebSocket 是通用首选，但需维护长连接心跳。
- **音频格式**：输入音频必须为 16-bit PCM（`s16le`），16 kHz 采样率（`qwen3.8` 多通道强制）；输出音频采样率固定为 24 kHz（PCM）或按 `audio.output.format` 配置（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 注明“输出音频为24 kHz采样率的PCM音频流”，但 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 允许 `sample_rate: 24000` 输出 WAV，实际应以客户端配置为准）。
- **[Token](../concepts/token.md) 限制**：`qwen3.8-omni-flash-realtime` 输入总 Token 上限为 196608；多声道音频输入 Token 消耗为单声道的 2 倍。
- **功能互斥**：`tools` 与 `enable_search` 不可共存；`semantic_vad` 仅在 `qwen3.8` 和 `qwen3.5` 系列模型可用。
- **MCP 安全**：`server_url`、`authorization`、`headers` 等敏感字段**不会在 `session.updated` 中回显**，客户端不得依赖服务端事件重建这些配置。
- **错误处理**：所有非法参数均触发 `error` 事件（类型 `invalid_request_error`），需检查 `error.param` 字段定位问题（如 `session.modalities` 不合法时提示支持组合）。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)


