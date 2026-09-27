# omni realtime api

Qwen-Omni-Realtime 是面向语音交互场景的低延迟、多模态实时大模型 API，支持文本与音频同步生成，并提供 VAD 驱动的流式语音交互、工具调用（Function Calling / MCP）、联网搜索等能力。它通过 AOQ、WebSocket 和 WebRTC 三种协议接入，适用于智能客服、语音助手、会议纪要等对实时性要求高的场景。开发者需基于会话（session）生命周期管理配置与事件流。

## 支持的模型/功能

当前支持以下模型（均以 `-realtime` 后缀标识）：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime`
- `qwen-omni-turbo-realtime`

核心功能包括：
- **多模态输出**：支持 `["text"]` 或 `["text", "audio"]` 组合，音频可配置格式（`pcm`/`wav`）与采样率（`8000`–`48000` Hz）；
- **语音活动检测（VAD）**：支持 `server_vad`（声学）和 `semantic_vad`（语义），后者可过滤背景音与回应语，仅 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列支持；
- **工具调用**：支持 Function Calling（`tools` 字段）和 MCP（`type: "mcp"`）两种方式，但二者与 `enable_search` **互斥**，不可同时启用；
- **联网搜索**：由 `enable_search: true` 启用，支持返回来源（`search_options.enable_source`），仅适用于 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列；
- **多通道音频输入**：仅 `qwen3.8-omni-flash-realtime` 支持 2/4 声道 PCM 输入（`channels: 2` 或 `4`），需在首段音频发送前完成配置；
- **视频输入表征压缩**：仅 `qwen3.8-omni-flash-realtime` 支持 `video.input.representation_compact: "normal"` 以降低 [Token](../concepts/token.md) 开销。

> **注意**：文档 3 中称 `output_audio_format` “当前仅支持设为 `pcm`” 且“不支持自定义输出采样率”，但[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)明确允许 `audio.output.format.type: "wav"` 和 `sample_rate: 24000`（示例中已使用）。该矛盾以[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)为准，服务端实际支持 `wav` 输出及 `24000` 采样率。

## 关键参数

所有配置通过 `session.update` 客户端事件提交，关键字段如下：

| 字段 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|----------------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色名；新接入推荐用 `audio.output.voice` | `Tina`（Qwen3.5）、`Cherry`（Qwen3-Flash）、`Chelsie`（Turbo） |
| `audio.input.format` | `object` | 输入格式：`type`（`pcm`/`wav`）、`sample_rate`（`8000`–`48000`） | `{"type": "pcm", "sample_rate": 16000}` |
| `audio.output.format` | `object` | 输出格式：同上，`sample_rate` 支持 `24000`（见上文注意） | `{"type": "wav", "sample_rate": 24000}` |
| `turn_detection` | `object` | VAD 配置：`type`、`threshold`（`-1.0`–`1.0`）、`silence_duration_ms`（`200`–`6000`） | `{"type": "server_vad", "threshold": 0.5, "silence_duration_ms": 800}` |
| `idle_timeout_ms` | `integer` | 静默超时（仅 `qwen3.5-omni-plus/flash-realtime` + `server_vad` 生效） | `5000`–`30000` |
| `enable_search` | `boolean` | 启用联网搜索（与 `tools` 互斥） | `false` |
| `tools` | `array` | Function Calling 工具列表；MCP 工具需 `type: "mcp"` 并配置 `server_url` 等 | `[]` |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 生成控制参数；建议只设其一；`qwen-omni-turbo` 系列**不支持修改** | 见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | `integer` | 最大输出 [Token](../concepts/token.md) 数；`qwen3.8-omni-flash-realtime` 范围 `[1, 65536]` | 模型最大输出长度 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数；`qwen3.8-omni-flash-realtime` 支持 `repetition_penalty: 0` | 见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |

> **注意**：`qwen-omni-turbo-realtime` 系列模型对 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` **全部不支持修改**，传入将被忽略。详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或 AOQ（[AOQ 接入](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)）；
2. **初始化会话**：连接后立即发送 `session.update` 事件配置 `modalities`、`model`、`voice`、`audio` 等核心参数；
3. **处理服务端事件**：监听 `session.created`（确认初始配置）、`session.updated`（确认更新）、`input_audio_buffer.speech_started/stopped`（VAD 状态）、`conversation.item.created`（消息/工具调用）等事件；
4. **发送音频**：按配置的 `audio.input.format` 发送原始音频数据流（PCM/WAV）；
5. **处理响应**：接收 `conversation.item.created`（含 `text` 和 `input_audio` 内容）及 `conversation.item.input_audio_transcription.delta`（实时 ASR 结果）；
6. **调用工具**：收到 `type: "function_call"` 的 `conversation.item.created` 后，执行对应函数并用 `conversation.item.input_audio_transcription.delta` 回传结果。

SDK 支持 Python 和 Java：[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：`qwen3.8-omni-flash-realtime` 单次 `session.update` 的全部输入 Token 上限为 **196608**；多通道音频输入（2/4 声道）的 Token 消耗为单声道的 2 倍；
- **音频配置时机**：`audio.input.format` 和 `audio.output.format` 必须在**首段音频发送前**完成配置，之后不可修改；
- **互斥约束**：`tools`（含 Function Calling 和 MCP）与 `enable_search` **不可同时为 `true`**；
- **VAD 模式差异**：`semantic_vad` 仅 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列支持；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus/flash-realtime` + `server_vad` 下生效；
- **错误处理**：服务端返回 `error` 事件（如 `invalid_request_error`），需检查 `error.param` 字段定位问题，例如 `session.modalities` 值非法；
- **兼容字段**：`input_audio_format` / `output_audio_format` 为历史字段，新接入应使用嵌套的 `audio.input.format` / `audio.output.format`；
- **MCP 限制**：MCP 工具调用受服务配额、超时及响应大小限制，详情见 [MCP 调用限制](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


