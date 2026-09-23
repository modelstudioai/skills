# omni realtime api

Qwen-Omni-Realtime API 是百炼平台提供的低延迟、多模态实时交互接口，基于 WebSocket / AOQ / WebRTC 协议，支持语音输入/输出、文本生成、工具调用与联网搜索等能力。它面向智能客服、语音助手、实时会议摘要等场景，要求开发者按事件驱动模型管理会话生命周期。核心交互围绕 `session.update` 客户端事件与 `session.created`/`session.updated` 等服务端事件展开。

## 支持的模型/功能

当前支持以下主力模型（均需通过 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 获取连接地址）：
- `qwen3.8-omni-flash-realtime`：支持 MCP 工具、多通道音频（2/4 声道）、视频表征压缩（`representation_compact`）、语义 VAD（`semantic_vad`）及更细粒度音频控制（如 `sample_format`, `packing`, `channel_layout`）。
- `qwen3.5-omni-flash-realtime` 与 `qwen3.5-omni-plus-realtime`：支持 Function Calling、`server_vad`/`semantic_vad`、`idle_timeout_ms` 及完整音频格式配置（`audio.input.format`/`audio.output.format`）。
- `qwen3-omni-flash-realtime` 与 `qwen-omni-turbo-realtime`：基础实时能力，但部分参数（如 `temperature`, `top_p`, `max_tokens` 等）**不支持修改**，详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

> **注意**：文档 3 中 `session.created` 示例显示 `output_audio_format` 固定为 `"pcm"` 且“当前不支持自定义输出采样率”，但文档 1 明确允许在 `session.update` 中设置 `audio.output.format.sample_rate` 为 `8000`/`16000`/`24000`/`48000`，且 `session.updated` 事件会回显该值（见文档 3 示例中 `"sample_rate": 24000`）。实际以 `session.updated` 回显为准，`session.created` 中的固定描述已过时。

功能覆盖：
- 多模态输出：`["text"]` 或 `["text", "audio"]`（默认），`qwen3.8-omni-flash-realtime` 还支持视频输入。
- 音频 I/O：支持 PCM/WAV 输入；PCM/WAV 输出（采样率可配）；`qwen3.8-omni-flash-realtime` 支持多通道输入（2/4 声道）。
- 语音活动检测（VAD）：`server_vad`（声学）或 `semantic_vad`（语义），后者仅限 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列。
- 工具调用：Function Calling（`type: "function"`）与 MCP（`type: "mcp"`）并存，但 **`tools` 与 `enable_search` 不可同时启用**。
- 联网搜索：`enable_search: true` 启用，支持来源返回（`search_options.enable_source`）。

## 关键参数

所有参数均在 `session.update` 事件的 `session` 对象中配置，服务端通过 `session.updated` 事件回显生效值。关键字段如下：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `model` | `string` | 模型 ID，必须与接入协议匹配 | 如 `"qwen3.5-omni-flash-realtime"` |
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 输出音色 | `Tina`（3.5 系列）、`Cherry`（3 系列）、`longanlingxin`（3.8 新增）；若两者共存，以 `audio.output.voice` 为准 |
| `audio.input.format` | `object` | 输入音频格式：`type`（`pcm`/`wav`）、`sample_rate`（`8000`/`16000`/`24000`/`48000`）、`channels`（仅 3.8 支持 `2`/`4`）、`sample_format`（仅 3.8）、`packing`（仅 3.8） | `type: "pcm"`, `sample_rate: 16000` |
| `audio.output.format` | `object` | 输出音频格式：同上 | `type: "pcm"`, `sample_rate: 24000` |
| `turn_detection.type` | `string` | VAD 类型 | `server_vad`（默认）或 `semantic_vad`（3.5+/3.8） |
| `turn_detection.threshold` | `float` | VAD 灵敏度 | `[-1.0, 1.0]`，默认 `0.5` |
| `turn_detection.silence_duration_ms` | `integer` | 静音触发时长 | `[200, 6000]`，默认 `800` |
| `idle_timeout_ms` | `integer` | 静默超时（仅 3.5+ Flash/Plus + `server_vad`） | `[5000, 30000]` |
| `enable_search` | `boolean` | 启用联网搜索 | `false`；与 `tools` 互斥 |
| `tools` | `array` | 工具列表，支持 `function` 和 `mcp` 类型 | 空数组；MCP 需提供 `server_label` 和 `server_url` |
| `temperature` / `top_p` / `top_k` / `max_tokens` / `repetition_penalty` / `presence_penalty` / `seed` | 各类型 | 生成控制参数 | 各模型默认值不同，详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)；`qwen-omni-turbo` 系列**不支持修改** |

> **注意**：文档 1 中 `smooth_output` 字段明确标注“**仅在使用 Qwen3-Omni-Flash-Realtime 系列模型时生效**”，但文档 3 的 `session.updated` 示例未包含此字段，且其参数列表中亦未提及。该字段对 `qwen3.5-omni-flash-realtime` 及更高版本无效，接入时应忽略。

## 使用方式

1. **建立连接**：选择 AOQ、WebRTC 或 WebSocket 协议接入，获取连接地址（参见[Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。
2. **初始化会话**：连接成功后，立即发送 `session.update` 事件（含完整 `session` 配置）。服务端校验后返回 `session.created`（首次）和 `session.updated`（确认配置）。
3. **音频流式传输**：按配置的 `audio.input.format` 格式，将原始音频数据分块发送至 `input_audio_buffer.append` 事件。
4. **响应处理**：监听服务端事件：
   - `input_audio_buffer.speech_started` / `speech_stopped`：感知用户语音起止。
   - `conversation.item.created`：接收模型回复（`type: "message"`）或工具调用请求（`type: "function_call"` 或 `type: "mcp_call"`）。
   - `conversation.item.input_audio_transcription.delta`：获取 ASR 实时识别结果（拼接 `text` + `stash`）。
5. **工具调用**：收到 `function_call` 后，执行本地函数并发送 `conversation.item.input_audio_transcription.completed`（或 `conversation.item.input_text.create`）提交结果；MCP 调用流程见文档 1 中 `session.tools` 的 `mcp` 类型说明。

## 限制和注意事项

- **协议与模型兼容性**：`qwen3.8-omni-flash-realtime` 仅支持 AOQ/WebSocket；`qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 支持 AOQ/WebRTC/WebSocket；`qwen-omni-turbo-realtime` 参数不可调（见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **音频配置时机**：`audio.input.format` 和 `audio.output.format` 必须在**首次发送音频前**完成配置，之后不可修改。
- **多通道音频**：仅 `qwen3.8-omni-flash-realtime` 支持，且强制要求 `type: "pcm"`, `sample_rate: 16000`, `sample_format: "s16le"`, `packing: "interleaved"`。
- **功能互斥**：`tools`（含 Function Calling 和 MCP）与 `enable_search` **不可同时设为 `true`**，否则服务端返回 `invalid_request_error`。
- **[Token](../concepts/token.md) 限制**：`qwen3.8-omni-flash-realtime` 输入上限为 196608 tokens；`max_tokens` 仅截断输出，不影响生成过程。
- **错误处理**：所有错误均以 `error` 事件返回，含 `error.type`, `error.code`, `error.message` 和 `error.param`（如 `session.modalities`），需据此定位问题（见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


