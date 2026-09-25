# omni realtime api

Qwen-Omni-Realtime 是面向实时语音交互场景的多模态大模型 API，支持文本、音频（含 TTS/ASR）及视频输入，提供低延迟流式响应。它通过 AOQ、WebSocket 和 WebRTC 三种协议接入，适用于智能客服、语音助手、会议纪要等强实时性需求场景。开发者需基于会话（session）模型发送结构化客户端事件，并处理服务端返回的异步事件流。

## 支持的模型与功能

当前支持以下模型（均以 `-realtime` 后缀标识）：
- `qwen3.8-omni-flash-realtime`（推荐用于高精度+低延迟场景，支持 MCP 工具、语义 VAD、多通道音频、视频 compact 表征）
- `qwen3.5-omni-plus-realtime` 与 `qwen3.5-omni-flash-realtime`（通用主力模型，支持工具调用、联网搜索、server_vad）
- `qwen3-omni-flash-realtime`（基础版，部分高级参数不可调）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出；音频输入支持 PCM/WAV、8k/16k/24k/48k 采样率；输出音频支持自定义格式与采样率（如 `wav` + `24000`）。
- **语音活动检测（VAD）**：`server_vad`（声学特征）与 `semantic_vad`（语义有效性），后者仅限 Qwen3.8/Qwen3.5 系列模型 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **工具调用**：Function Calling（`type: "function"`）与 MCP（`type: "mcp"`）双模式，但 `tools` 与 `enable_search` **互斥**，不可同时启用。
- **联网搜索**：`enable_search: true` 可触发自主搜索，支持 `search_options.enable_source` 返回来源。
- **视频输入**：仅 Qwen3.8-Omni-Flash-Realtime 支持 `video.input.representation_compact`（`none` / `normal`），影响 [Token](../concepts/token.md) 消耗 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 3 中 `session.created` 事件说明“`output_audio_format` 当前仅支持 `pcm`”且“不支持自定义输出采样率”，但文档 2 的 `session.update` 示例明确配置了 `"output": {"format": {"type": "wav", "sample_rate": 24000}}`，且文档 3 的 `session.updated` 示例也回显了 `wav` + `24000`。因此，**文档 3 关于输出格式限制的描述已过时**，应以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准。

## 关键参数

所有参数均在 `session.update` 事件的 `session` 对象中配置，服务端通过 `session.updated` 回显确认值：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色，Qwen3.8 推荐使用 `audio.output.voice` 字段 | Qwen3.5: `Tina`；Qwen3.8: `Tina`（新增 `longanlingxin`） |
| `audio.input.format` | `object` | 输入格式：`type`（`pcm`/`wav`）、`sample_rate`（8000/16000/24000/48000） | `{"type": "pcm", "sample_rate": 16000}` |
| `audio.output.format` | `object` | 输出格式：同上，支持 `wav` + `24000` | `{"type": "pcm", "sample_rate": 24000}` |
| `turn_detection.type` | `string` | `server_vad`（默认）或 `semantic_vad`（Qwen3.8/Qwen3.5 支持） | `server_vad` |
| `turn_detection.silence_duration_ms` | `integer` | 静音阈值（200–6000 ms） | `800` |
| `idle_timeout_ms` | `integer` | 静默超时（5000–30000 ms），**仅对 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 生效** | — |
| `enable_search` | `boolean` | 启用联网搜索（与 `tools` 不兼容） | `false` |
| `tools` | `array` | Function Calling 或 MCP 工具列表 | `[]` |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 生成控制参数，**`qwen-omni-turbo` 系列不支持修改** | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `integer` | 响应最大 [Token](../concepts/token.md) 数（截断，不影响生成过程） | Qwen3.8: `65536`；其他模型见 [模型列表](raw/model-user-guide/get-started-with-models/models.md) |

## 使用方式

1. **建立连接**：选择 AOQ（推荐低延迟）、WebSocket（通用）或 WebRTC（浏览器直连），详见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。
2. **初始化会话**：连接后立即发送 `session.update` 事件配置参数（如 `modalities`, `model`, `voice`, `audio` 等）。服务端校验后返回 `session.created`（首次）或 `session.updated`（成功更新）。
3. **发送音频**：按配置的 `audio.input.format` 发送原始音频数据帧；VAD 自动触发 `speech_started`/`speech_stopped` 事件。
4. **处理响应**：监听 `conversation.item.created`（含 `message` 或 `function_call`）、`input_audio_buffer.committed`、`conversation.item.input_audio_transcription.delta`（实时 ASR）等事件。
5. **调用工具**：收到 `function_call` 后，执行本地函数并发送 `conversation.item.input_audio_transcription.completed` 或 `conversation.item.function_call_output`；MCP 工具调用流程参见 [MCP 调用限制](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

SDK 支持：[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 与 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **协议限制**：AOQ/WebRTC 仅支持 Qwen3.8/Qwen3.5 系列；`qwen-omni-turbo-realtime` 仅支持 WebSocket。
- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 单次 `session.update` 输入总 Token 上限为 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **音频配置时机**：`audio.input.format` / `audio.output.format` 必须在**首段音频发送前**完成配置，之后不可修改。
- **参数互斥**：`tools` 与 `enable_search` 不可同时为 `true`；`temperature` 与 `top_p` 建议只设置其一。
- **模型特异性**：`qwen-omni-turbo-realtime` 系列**不支持修改** `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed`；`qwen3.8-omni-flash-realtime` 的 `repetition_penalty` 可设为 `0`，其他模型需 `> 0`。
- **错误处理**：服务端返回 `error` 事件（含 `code` 与 `param`），例如 `invalid_value` 错误会明确指出问题字段（如 `"param": "session.modalities"`）。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


