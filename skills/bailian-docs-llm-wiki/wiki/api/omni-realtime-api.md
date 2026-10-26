# omni realtime api

Qwen-Omni-Realtime API 是面向多模态实时交互场景的 WebSocket/QUIC/WebRTC 接口，支持语音、文本、视频等输入与文本+音频混合输出，提供低延迟端到端流式响应。其核心能力包括动态会话配置、VAD 驱动的语音交互、Function Calling 与 MCP 工具集成、联网搜索及细粒度生成控制。该 API 采用事件驱动模型，客户端通过发送标准事件（如 `session.update`、`response.create`）控制会话生命周期与交互节奏。

## 支持的模型与功能

当前支持以下主力模型：
- `qwen3.8-omni-flash-realtime`（推荐用于新接入，支持多通道音频、语义 VAD、MCP、视频表征压缩）
- `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`（兼容旧接入，支持基础 VAD 与 Function Calling）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text","audio"]` 输出；Qwen3.8-Omni-Flash-Realtime 还支持视频输入（`video.input.representation_compact`）。
- **语音活动检测（VAD）**：提供 `server_vad`（声学）、`semantic_vad`（语义）和 `semantic_vad_ec`（客服增强）三种模式，其中 `semantic_vad_ec` 仅限 Qwen3.8-Omni-Flash-Realtime [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **工具调用**：同时支持 Function Calling（`type=function`）与 MCP（`type=mcp`），但二者不可与 `enable_search` 共存。
- **联网搜索**：启用 `enable_search: true` 后模型可自主触发搜索，需配合 `search_options.enable_source` 控制来源返回。
- **音色与音频格式**：默认音色因模型而异（如 `Tina` 或 `Cherry`），输入/输出音频格式支持 `pcm`/`wav`，采样率可配（Qwen3.8-Omni-Flash-Realtime 输入强制 `16000 Hz`）。

> **注意**：文档 2 中称“输出音频为24 kHz采样率的PCM音频流。当前不支持自定义输出采样率”，但文档 1 明确允许在 `session.audio.output.format.sample_rate` 中设置 `8000`/`16000`/`24000`/`48000`，且示例中使用了 `24000`。以[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)为准，服务端实际支持自定义输出采样率。

## 关键参数

所有参数均通过 `session.update` 事件的 `session` 对象传递，关键字段如下：

| 参数 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 输出音色；新接入应优先使用 `audio.output.voice` | `Tina`（多数模型）或 `Cherry`（`qwen3-omni-flash-realtime-2025-09-15`） |
| `turn_detection.type` | `string` | VAD 类型：`server_vad`/`semantic_vad`/`semantic_vad_ec` | `server_vad` |
| `turn_detection.threshold` | `float` | VAD 灵敏度（-1.0 ~ 1.0） | `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 语音后静音阈值（ms） | `800` |
| `temperature` / `top_p` / `top_k` | `float`/`float`/`integer` | 生成多样性控制；建议只设其一 | 见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | `integer` | 响应最大 [Token](../concepts/token.md) 数（截断，非硬限） | `65536`（Qwen3.8）；其他模型见模型文档 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚系数 | `0` / `1.0`（Qwen3.8）；详见文档 1 |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false` |
| `tools` | `array` | Function Calling 或 MCP 工具定义列表 | `[]` |

## 使用方式

1. **建立连接**：选择 AOQ、WebSocket 或 WebRTC 协议接入，具体流程参见[Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。
2. **初始化会话**：连接后立即发送 `session.update` 事件配置 `model`、`modalities`、`audio`、`turn_detection` 等核心参数。
3. **输入处理**：
   - VAD 模式：持续发送 `input_audio_buffer.append`，服务端自动触发 `speech_started`/`speech_stopped` 并提交缓冲区；
   - Manual 模式：发送 `input_audio_buffer.append` 后，显式发送 `input_audio_buffer.commit`。
4. **触发响应**：VAD 模式下由服务端自动触发；Function Calling 场景需在 `conversation.item.created`（`function_call`）后发送 `response.create`；MCP 场景需在 `response.done` 后发送 `response.create`。
5. **取消响应**：发送 `response.cancel` 可中断正在进行的生成。
6. **监听服务端事件**：解析 `session.updated`、`conversation.item.created`、`response.content_part.added`、`response.done` 等事件流，构建 UI 或业务逻辑。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 输入总 [Token](../concepts/token.md) 上限为 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **音频约束**：Qwen3.8-Omni-Flash-Realtime 多通道输入强制要求 `pcm` + `16000 Hz` + `s16le` + `interleaved`；字段省略时使用默认值，显式提供则必须严格匹配。
- **工具与搜索互斥**：`tools` 与 `enable_search` 不可同时为 `true`，否则服务端返回错误。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址，`headers` 禁用敏感字段（如 `authorization`、`host`），凭证类字段（`authorization`, `headers`）不会在 `session.updated` 中回显。
- **VAD 超时行为**：`idle_timeout_ms` 仅对 `qwen3.5-omni-plus-realtime`/`qwen3.5-omni-flash-realtime` + `server_vad` 生效，Qwen3.8-Omni-Flash-Realtime 不支持该字段。
- **平滑输出**：`smooth_output` 仅对 `qwen3-omni-flash-realtime-2025-09-15` 生效，控制口语化/书面化风格。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)


