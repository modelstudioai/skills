# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟大模型 API，支持语音、文本、视频等输入与文本+音频混合输出，适用于智能客服、语音助手、实时会议纪要等强交互场景。其核心能力基于 WebSocket、AOQ（AI over QUIC）和 WebRTC 三种协议实现端到端流式传输，并通过结构化事件驱动模型行为。开发者需按会话生命周期管理配置、输入、响应与工具调用。

## 支持的模型与功能

当前支持以下模型（均需通过 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 统一接入）：
- `qwen3.8-omni-flash-realtime`：支持多通道音频输入（1/2/4 声道）、语义 VAD（含 `semantic_vad_ec`）、MCP 工具集成、视频表征压缩（`representation_compact`）及 `smooth_output` 风格控制；
- `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`：支持基础 VAD（`server_vad`/`semantic_vad`）、Function Calling、联网搜索（`enable_search`），但**不支持 MCP、视频输入或 `smooth_output`**；
- `qwen3-omni-flash-realtime-2025-09-15`：为实验性版本，启用 `smooth_output`（默认 `true`）、更高 `temperature`（0.9）与 `top_k`（50），但**不兼容 `tools` 与 `enable_search` 同时开启**（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

> **注意**：文档 3 中 `session.created` 示例声明“输出音频为24 kHz采样率的PCM音频流。当前不支持自定义输出采样率”，但文档 2 明确允许 `audio.output.format.sample_rate` 在 `qwen3.5-omni-plus-realtime` 等模型中设为 8000/16000/24000/48000 Hz。此处以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的权威定义为准，服务端实际支持可配。

## 关键参数

所有配置通过 `session.update` 客户端事件传递，关键字段包括：

- **`modalities`**：必须为 `["text"]` 或 `["text","audio"]`（`["audio"]` 单独不合法），详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)；
- **`voice`**：音色标识符，默认 `Tina`；新接入应优先使用 `session.audio.output.voice`，若与 `session.voice` 冲突，以前者为准；
- **`audio.input.format` / `audio.output.format`**：推荐使用嵌套结构（含 `type` 和 `sample_rate`），历史字段 `input_audio_format`/`output_audio_format` 仅作兼容；
- **`turn_detection`**：VAD 配置，`semantic_vad_ec` 仅 `qwen3.8-omni-flash-realtime` 支持；
- **`enable_search` 与 `tools`**：互斥，不可同时为 `true`；
- **采样控制**：`temperature`、`top_p`、`top_k` 建议只设置其一；`repetition_penalty=0` 仅 `qwen3.8-omni-flash-realtime` 允许；
- **`max_tokens`**：仅截断响应，不影响生成过程；`qwen3.8-omni-flash-realtime` 最大支持 65536。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入，推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）并使用官方 SDK（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) / [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）；
2. **初始化会话**：连接后立即发送 `session.update` 事件配置模态、音色、VAD、工具等；
3. **输入数据**：
   - 音频：通过 `input_audio_buffer.append` 追加 Base64 数据，VAD 模式下由服务端自动 `commit`，Manual 模式需显式发送 `input_audio_buffer.commit`；
   - 文本/图像：通过 `conversation.item.create` 提交；
4. **触发响应**：VAD 自动触发，或手动发送 `response.create`；可随时用 `response.cancel` 中断；
5. **处理服务端事件**：监听 `session.updated`（确认配置生效）、`input_audio_buffer.speech_started/stopped`（语音活动）、`conversation.item.created`（消息/工具调用）、`response.done`（响应完成）等。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：`qwen3.8-omni-flash-realtime` 输入上限 196608 tokens；多通道音频（2/4 声道）输入 [Token](../concepts/token.md) 数为单声道的 2 倍；
- **音频约束**：`qwen3.8-omni-flash-realtime` 多通道输入强制要求 `pcm` + `16000 Hz` + `s16le` + `interleaved`，字段省略则用默认值，提供则必须严格匹配；
- **MCP 限制**：`server_url` 必须为公网 HTTPS 443 地址，`authorization`/`headers` 不在 `session.updated` 中回显，客户端不可依赖；
- **VAD 超时**：`idle_timeout_ms` 仅对 `qwen3.5-omni-plus-realtime`/`qwen3.5-omni-flash-realtime` + `server_vad` 生效，范围 [5000, 30000] ms；
- **工具冲突**：`tools` 与 `enable_search` 互斥；Function Calling 与 MCP 可共存于 `qwen3.8-omni-flash-realtime`，但需分别配置；
- **错误处理**：所有非法参数将返回 `error` 事件（如 `invalid_value`），需检查 `error.param` 字段定位问题源。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


