# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟大模型 API，支持语音、文本、视频等输入与文本+音频混合输出，适用于智能客服、语音助手、实时会议纪要等强交互场景。其核心能力基于 AOQ、WebSocket 和 WebRTC 三种协议实现端到端毫秒级响应，并提供细粒度的会话控制、VAD 配置、工具调用与联网搜索能力。开发者需通过 `session.update` 初始化配置，并按事件驱动模型收发客户端/服务端事件。

## 支持的模型与功能

当前支持以下模型（均需通过 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 接入）：
- `qwen3.8-omni-flash-realtime`（推荐新项目使用）
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本，部分参数行为不同）

**核心功能包括**：
- 多模态 I/O：支持 `["text"]` 或 `["text","audio"]` 输出；Qwen3.8-Omni-Flash-Realtime 还支持视频输入（`video.input.representation_compact`）。
- 实时语音活动检测（VAD）：支持 `server_vad`（通用）、`semantic_vad`（语义过滤）、`semantic_vad_ec`（客服增强），详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- 工具调用：支持 Function Calling（`type=function`）和 MCP（`type=mcp`），但二者不可与 `enable_search` 同时启用。
- 联网搜索：仅 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列支持 `enable_search: true`。
- 输入音频转录：固定使用 `qwen3-asr-flash-realtime` 模型，通过 `input_audio_transcription` 控制开关。

> **注意**：文档 3 中 `session.created` 示例声明“`output_audio_format` 当前仅支持 `pcm`”且“不支持自定义输出采样率”，但文档 2 明确允许 `wav` 格式及 `8000/16000/24000/48000 Hz` 输出采样率（对 Qwen3.5 系列），且 `session.updated` 事件会回显 `audio.output.format` 结构。实际以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的字段定义为准，服务端兼容性优先于文档 3 的静态描述。

## 关键参数

所有配置通过 `session.update` 事件提交，关键参数如下（完整字段见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | `string` | 音色（如 `Tina`, `Cherry`） | `Tina`（除 `qwen3-omni-flash-realtime-2025-09-15` 为 `Cherry`） |
| `audio.input.format.type` | `string` | 输入格式：`pcm`（默认）或 `wav`（Qwen3.5 系列）；Qwen3.8 多通道仅支持 `pcm` | `pcm` |
| `audio.input.format.sample_rate` | `integer` | 输入采样率：Qwen3.5 系列支持 `8000/16000/24000/48000`；Qwen3.8 多通道强制 `16000` | `16000` |
| `audio.output.format.type` | `string` | 输出格式：`pcm` 或 `wav` | `pcm` |
| `audio.output.format.sample_rate` | `integer` | 输出采样率：Qwen3.5 系列支持 `8000/16000/24000/48000`（默认 `24000`） | `24000`（Qwen3.5）；`24000`（Qwen3.8） |
| `turn_detection.type` | `string` | VAD 类型：`server_vad` / `semantic_vad` / `semantic_vad_ec` | `server_vad` |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false` |
| `tools` | `array` | 工具列表（Function Calling 或 MCP） | — |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 采样参数，三者建议只设其一 | 见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格 |
| `max_tokens` | `integer` | 单次响应最大输出 [Token](../concepts/token.md) 数 | `65536`（Qwen3.8）；各模型上限见 [模型列表](raw/model-user-guide/get-started-with-models/models.md) |

> **注意**：`smooth_output` 仅对 `qwen3-omni-flash-realtime-2025-09-15` 生效，其他模型忽略该字段；`idle_timeout_ms` 仅在 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` + `server_vad` 时有效，Qwen3.8 不支持。

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入，推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或使用官方 SDK（[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md)、[Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)）。
2. **初始化会话**：连接后立即发送 `session.update` 事件配置参数（如 `modalities`, `voice`, `turn_detection`）。
3. **发送用户输入**：
   - 音频：分块发送 `input_audio_buffer.append` → 手动模式下发送 `input_audio_buffer.commit`；VAD 模式下由服务端自动提交。
   - 文本/图像：通过 `conversation.item.create` 提交。
4. **触发响应**：发送 `response.create` 启动模型生成；收到 `response.done` 后可发下一轮。
5. **处理服务端事件**：监听 `conversation.item.created`（新消息）、`response.content_part.added`（流式音频/文本）、`input_audio_buffer.speech_started/stopped`（VAD 状态）等，详见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 输入总 [Token](../concepts/token.md) 上限为 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍，详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。
- **协议约束**：
  - WebRTC：仅支持音频，不支持文本/视频输入。
  - AOQ：需 QUIC 支持，适合高丢包网络。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时为 `true`。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址；`authorization` 和 `headers` 不在 `session.updated` 中回显，客户端不可依赖。
- **音频格式兼容性**：Qwen3.8-Omni-Flash-Realtime 多通道输入强制要求 `pcm` + `16000 Hz` + `s16le` + `interleaved`；省略字段时使用默认值，但显式设置必须严格匹配。
- **错误处理**：所有非法参数均返回 `error` 事件（如 `invalid_value`），需检查 `error.param` 定位问题字段，详见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

> **注意**：文档 2 中 `input_audio_buffer.commit` 描述“若已发送 `input_image_buffer.append`，则 `input_audio_buffer.commit` 将同时提交图像缓冲区”，但文档 3 未提及此联动行为，且无对应服务端事件说明。实际集成时应以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 的明确约定为准，避免依赖未定义的隐式行为。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


