# omni realtime api

Qwen-Omni-Realtime API 是面向多模态实时交互场景的 WebSocket 流式 API，支持语音、文本、图像（Qwen3.8+）、视频（Qwen3.8+）等输入与文本+音频联合输出。它采用事件驱动模型，客户端通过发送结构化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态和输入流，服务端以异步事件（如 `session.created`、`response.content_part.added`）实时反馈处理结果。该 API 适用于智能客服、实时会议助手、语音交互终端等低延迟、高交互性场景。

## 支持的模型/功能

当前支持以下核心模型系列，各模型能力存在差异：

- **Qwen3.8-Omni-Flash-Realtime**：支持多通道音频（1/2/4 声道）、空间音频、视频输入（`video.input.representation_compact`）、MCP 工具调用、`semantic_vad_ec` VAD 模式、`smooth_output` 风格控制。默认音色为 `Tina`，[Token](../concepts/token.md) 上限为 196608。
- **Qwen3.5-Omni-Plus-Realtime / Qwen3.5-Omni-Flash-Realtime**：支持基础语音+文本双模态、Function Calling、`server_vad` 和 `semantic_vad`、联网搜索（`enable_search`）。不支持视频、多通道音频或 MCP。默认音色为 `Tina`。
- **qwen3-omni-flash-realtime-2025-09-15**：为特定版本模型，启用 `smooth_output` 时默认值为 `true`，`temperature` 默认为 `0.9`，`top_p` 默认为 `1.0`，`repetition_penalty` 默认为 `1.05`，`presence_penalty` 默认为 `0.0`。

> **注意**：文档 3 中 `session.created` 示例声明“`output_audio_format` 当前仅支持设为 `pcm`”且“不支持自定义输出采样率”，但[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)明确说明 `audio.output.format.sample_rate` 在 Qwen3.5 系列中可选 8000/16000/24000/48000 Hz，默认 24000 Hz；Qwen3.8 系列亦支持配置。此处以[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)为准，服务端实际支持动态输出采样率。

## 关键参数

所有会话级配置均通过 `session.update` 事件的 `session` 对象传递，关键字段包括：

- **`modalities`**：输出模态，必须为 `["text"]` 或 `["text","audio"]`（不可仅含 `"audio"`），详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **`voice` / `audio.output.voice`**：音色选择。新接入**必须使用 `session.audio.output.voice`**；若两者同时设置，以 `audio.output.voice` 为准。
- **`audio.input.format` & `audio.output.format`**：推荐使用嵌套结构配置格式（`type` + `sample_rate`），替代已废弃的 `input_audio_format`/`output_audio_format` 字段。
- **`turn_detection`**：VAD 配置。`semantic_vad_ec` 仅 Qwen3.8 系列支持；`idle_timeout_ms` 仅在 Qwen3.5 系列 + `server_vad` 时生效。
- **`tools`**：支持 Function Calling（`type=function`）和 MCP（`type=mcp`）。**`tools` 与 `enable_search` 不可同时启用**。
- **采样控制**：`temperature`（默认 Qwen3.8=0.6, Qwen3.5=0.7）、`top_p`（默认 Qwen3.8=0.95, Qwen3.5=0.8）、`top_k`（默认均为 20，Qwen3.8 可设为 0）、`repetition_penalty`（Qwen3.8 支持 0）、`presence_penalty`（范围 [-2.0, 2.0]）。
- **`max_tokens`**：控制响应截断长度，Qwen3.8 取值范围 [1, 65536]；其他模型默认为模型最大输出长度。

## 使用方式

1. **建立连接**：通过 WebSocket（推荐）、AOQ 或 WebRTC 连接至服务端，具体协议选择见[Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)。
2. **初始化会话**：连接后服务端立即返回 `session.created` 事件，提供默认配置。
3. **配置会话**：发送 `session.update` 事件调整参数（如模态、音色、VAD、工具等）。Qwen3.8-Omni-Flash-Realtime 要求必须提供 `session` 对象。
4. **输入数据**：
   - 音频：持续发送 `input_audio_buffer.append`（Base64 PCM/WAV），VAD 模式下由服务端自动 `commit`；Manual 模式需显式发送 `input_audio_buffer.commit`。
   - 图像/视频：通过对应 buffer 事件（文档未展开，参见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)中 `video` 部分）。
5. **触发响应**：VAD 模式下语音结束自动触发；Manual 模式或工具回调后需发送 `response.create`。
6. **取消响应**：发送 `response.cancel` 终止进行中的生成。
7. **处理服务端事件**：监听 `conversation.item.created`、`response.content_part.added`、`response.done` 等事件流式消费结果。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制**：Qwen3.8-Omni-Flash-Realtime 输入 [Token](../concepts/token.md) 总数上限为 196608；多通道音频（2/4 声道）输入 Token 数为单声道的 2 倍；视频 `representation_compact=normal` 时 Token 数为 `none` 的 1/4。
- **音频格式约束**：Qwen3.8 多通道输入**强制要求** `pcm` + `16000 Hz` + `s16le` + `interleaved`；字段一旦显式提供，必须严格匹配类型与值，不可为 `null`。
- **工具与搜索互斥**：`tools` 数组非空时，`enable_search` 必须为 `false`，否则服务端返回错误。
- **MCP 安全限制**：`server_url` 必须为公网 HTTPS 443 地址，`authorization` 和 `headers` 不在 `session.updated` 中回显，客户端不得依赖其重建敏感配置。
- **兼容性字段**：`input_audio_format`/`output_audio_format` 为历史兼容字段，新接入应使用 `audio.input.format`/`audio.output.format`；`session.voice` 为兼容旧字段，新接入应使用 `session.audio.output.voice`。
- **错误处理**：服务端统一返回 `error` 事件，包含 `type`、`code`、`message` 和 `param`（如 `"session.modalities"`），需据此定位问题。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


