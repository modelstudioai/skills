# omni realtime api

Qwen-Omni-Realtime 是面向实时多模态交互（语音+文本）优化的流式大模型 API，支持低延迟音频输入/输出、端到端 VAD、工具调用（Function Calling / MCP）及联网搜索等能力。它通过 AOQ、WebSocket 和 WebRTC 三种协议提供接入，适用于智能客服、语音助手、实时会议摘要等场景。开发者需关注模态组合、音频格式约束及模型间参数兼容性差异。

## 支持的模型与功能

当前支持以下模型（均以 `-realtime` 后缀标识）：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；输入音频仅支持 `pcm`（默认）或 `wav`（部分模型），采样率需匹配（如 16 kHz 输入、24 kHz 输出）[Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。
- **语音活动检测（VAD）**：支持 `server_vad`（声学检测）和 `semantic_vad`（语义检测）两种模式；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 下生效 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。
- **工具调用**：支持 Function Calling（`type=function`）和 MCP（`type=mcp`）；MCP 配置中的 `server_url`、`authorization` 等敏感字段**不会在 `session.updated` 中回显**，客户端不可依赖该事件重建连接 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **联网搜索**：`enable_search` 仅对 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列有效，且与 `tools` **互斥**（不可同时启用）。

> **注意**：文档 2 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“不支持自定义输出采样率”，但文档 3 明确说明 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 的 `audio.output.format.sample_rate` 可设为 `8000/16000/24000/48000`。此处以文档 3 的客户端配置能力为准，服务端示例存在过时风险。

## 关键参数

所有参数通过 `session.update` 客户端事件设置，服务端校验后返回 `session.updated` 事件。关键参数如下：

| 参数 | 类型 | 说明 | 默认值 | 模型限制 |
|------|------|------|--------|----------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` | 全系列支持 |
| `voice` / `audio.output.voice` | `string` | 输出音色 | `Tina`（Qwen3.8）、`Cherry`（Qwen3.5-Flash） | [音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices) |
| `audio.input.format.type` | `string` | 输入格式：`pcm`（默认）或 `wav` | `pcm` | `qwen3.5-*` 支持两者；`qwen3.8-*` 多通道仅支持 `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率（Hz） | `16000` | `qwen3.5-*`: 8k/16k/24k/48k；`qwen3.8-*`: 仅 `16000` |
| `audio.output.format.type` | `string` | 输出格式：`pcm`（默认）或 `wav` | `pcm` | `qwen3.5-*` 支持两者 |
| `turn_detection.type` | `string` | VAD 类型：`server_vad`（默认）或 `semantic_vad` | `server_vad` | `qwen3.8-*` 和 `qwen3.5-*` 系列支持 |
| `enable_search` | `boolean` | 启用联网搜索 | `false` | `qwen3.8-*` 和 `qwen3.5-*` 系列支持；与 `tools` 不兼容 |
| `tools` | `array` | 工具定义（`function` 或 `mcp`） | `[]` | `qwen3.8-*` 支持混合配置；`qwen3.5-*` 仅支持 `function` |
| `temperature` | `float` | 采样温度 | `0.6`（Qwen3.8）、`0.7`（Qwen3.5） | `qwen-omni-turbo-*` 系列**不支持修改** |

> **注意**：`qwen-omni-turbo-*` 系列模型在 `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等参数上**完全不可配置**，文档 3 中明确标注了此限制，而文档 2 的 `session.updated` 示例中包含这些字段，易引发误用。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或使用官方 SDK（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）。
2. **初始化会话**：连接成功后，立即发送 `session.update` 事件配置参数（如 `modalities`、`voice`、`turn_detection`）。服务端返回 `session.created` 事件确认初始配置。
3. **音频流传输**：按配置的 `input_audio_format` 和采样率，持续写入 PCM/WAV 音频流至缓冲区。VAD 自动触发 `input_audio_buffer.speech_started` / `speech_stopped` 事件。
4. **交互控制**：
   - 手动提交：发送 `input_audio_buffer.commit` 触发模型响应；
   - 清空缓冲区：发送 `input_audio_buffer.clear`；
   - 动态更新：再次发送 `session.update` 修改参数（如切换音色、启用搜索）。
5. **处理响应**：监听服务端事件，如 `conversation.item.created`（含文本/音频内容）、`error`（错误处理）、`session.updated`（配置生效确认）。

## 限制和注意事项

- **音频格式硬约束**：输入必须为单声道/多声道 PCM（`s16le`）或 WAV；`qwen3.8-*` 多通道输入强制要求 `channels=2/4`、`sample_rate=16000`、`packing=interleaved`，且 `channel_layout` 必须匹配（如 `raw_mic_array`）。
- **参数互斥性**：`tools` 与 `enable_search` 不可同时为 `true`；`temperature` 和 `top_p` 建议只设置其一以避免行为不可控。
- **[Token](../concepts/token.md) 计算**：多通道音频（2/4 声道）输入 [Token](../concepts/token.md) 数为单声道的 2 倍；视频 `representation_compact=normal` 可降低 [Token](../concepts/token.md) 数至 `none` 模式的 1/4（详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)）。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址；`authorization` 和 `headers` 字段**永不回显**于服务端事件，客户端不得尝试从 `session.updated` 提取。
- **超时与配额**：MCP 调用受服务端配额及超时限制（参见 [MCP 调用限制](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-limits)）；`idle_timeout_ms` 仅在无用户语音输入时触发主动响应，计时始于上一条模型音频播放完毕。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)


