# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟大模型 API，支持语音、文本、工具调用等混合输入与音视频同步输出。它通过 AOQ、WebSocket 和 WebRTC 三种协议提供流式双向通信能力，适用于智能客服、实时会议助手、语音交互终端等对端到端延迟敏感的场景。开发者需按事件驱动模型管理会话生命周期与音频缓冲区。

## 支持的模型/功能

当前支持以下模型（均以 `qwen3.x-omni-*` 命名）：
- `qwen3.8-omni-flash-realtime`：支持多通道音频输入（1/2/4 声道）、`semantic_vad_ec` VAD 模式、MCP 工具集成、视频表征压缩（`representation_compact`）；
- `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime`：支持基础 VAD（`server_vad`/`semantic_vad`）、Function Calling、联网搜索（`enable_search`），但**不支持 MCP 或多通道音频**；
- `qwen3-omni-flash-realtime-2025-09-15`：新增 `smooth_output` 控制回复风格（口语化/书面化），默认音色为 `Cherry`。

核心功能包括：
- 实时语音识别（ASR）与合成（TTS），输入/输出音频格式支持 `pcm` 和 `wav`（[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 中明确 `input_audio_format` 和 `output_audio_format` 当前仅支持 `pcm`，但 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 明确 `audio.input.format.type` 和 `audio.output.format.type` 可设为 `wav`）；
- 多模态会话管理（`text` + `audio` 输出组合）；
- 工具调用：Function Calling（`type=function`）和 MCP（`type=mcp`），二者可共存于同一会话（仅 `qwen3.8-omni-flash-realtime` 支持）；
- 语音活动检测（VAD）：`server_vad`（所有模型）、`semantic_vad`（Qwen3.5+ 和 Qwen3.8）、`semantic_vad_ec`（仅 Qwen3.8）；
- 联网搜索（`enable_search`）：Qwen3.8 和 Qwen3.5 系列支持，但**与 `tools` 不兼容，不可同时启用**（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。

> **注意**：文档 2 中 `session.created` 示例显示 `output_audio_format` 为 `"pcm"` 且注明“当前不支持自定义输出采样率”，而文档 3 的 `session.update` 中 `audio.output.format.sample_rate` 明确支持 `24000`（默认值）及 `8000/16000/48000`。此处无矛盾——采样率可配置，但格式仍限于 `pcm` 或 `wav`；`output_audio_format` 字段是历史兼容字段，新接入应使用嵌套的 `audio.output.format.type`。

## 关键参数

| 参数 | 说明 | 默认值 | 适用模型 | 来源 |
|------|------|--------|----------|------|
| `modalities` | 输出模态数组，如 `["text"]` 或 `["text","audio"]` | `["text","audio"]` | 全系列 | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `voice` / `audio.output.voice` | 音色名称 | `Tina`（Qwen3.8/Qwen3.5），`Cherry`（2025-09-15） | 全系列 | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `turn_detection.type` | VAD 类型 | `server_vad` | 全系列 | [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) |
| `temperature` / `top_p` / `top_k` | 生成多样性控制 | 见文档 3 表格 | 全系列 | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | 单次响应最大输出 Token 数 | Qwen3.8: 65536；其他：模型上限 | 全系列 | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `enable_search` | 启用联网搜索 | `false` | Qwen3.8 & Qwen3.5 系列 | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `tools` | 工具定义列表（`function` 或 `mcp`） | — | Qwen3.8（全支持），Qwen3.5（仅 `function`） | [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |

> **注意**：`repetition_penalty` 在 Qwen3.8 中支持 `0`（禁用惩罚），而 Qwen3.5 系列要求 >0；`presence_penalty` 默认值在不同模型间差异显著（Qwen3.8 为 `1`，Qwen3.5 为 `1.5`），需按模型显式设置。

## 使用方式

1. **建立连接**：选择 AOQ（推荐低延迟）、WebSocket（通用 SDK 支持）或 WebRTC（浏览器直连），详见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)；
2. **初始化会话**：连接后服务端自动返回 `session.created` 事件，含默认配置；
3. **更新配置（可选）**：发送 `session.update` 事件调整参数（如 `modalities`、`voice`、`turn_detection`、`tools` 等）；
4. **输入音频**：
   - VAD 模式：持续发送 `input_audio_buffer.append`，服务端自动检测 `speech_started`/`speech_stopped` 并提交；
   - Manual 模式：发送 `input_audio_buffer.append` 后，必须显式发送 `input_audio_buffer.commit`；
5. **触发响应**：VAD 模式下自动触发；Manual 模式或工具调用后需发送 `response.create`；
6. **处理事件流**：监听 `conversation.item.created`（用户/模型消息）、`response.content_part.added`（流式文本/音频片段）、`response.done`（响应结束）等服务端事件。

SDK 支持：Python 和 Java 的 WebSocket 封装已提供（见 [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)）。

## 限制和注意事项

- **协议限制**：AOQ 仅支持 QUIC over UDP，需客户端网络允许；WebRTC 仅支持浏览器环境；WebSocket 为最广泛兼容方案。
- **音频约束**：
  - 输入必须为 16-bit PCM（单声道或指定多声道），采样率严格为 16 kHz（Qwen3.8 多通道）或 8/16/24/48 kHz（Qwen3.5）；
  - 输出音频采样率为 24 kHz（`pcm`）或可配（`wav`），但 `output_audio_format` 字段本身仅接受 `pcm`（历史兼容）；
  - 多通道输入（2/4 声道）**仅 Qwen3.8 支持**，且必须使用 `pcm` + `s16le` + `interleaved` + `16000 Hz` 组合。
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用；`semantic_vad_ec` 仅 Qwen3.8 支持；MCP 仅 Qwen3.8 支持。
- **Token 限制**：Qwen3.8 的 `session.update` 输入总 Token 上限为 196608；`max_tokens` 仅截断输出，不影响生成逻辑。
- **安全敏感字段**：MCP 的 `server_url`、`authorization`、`headers` **不会在 `session.updated` 事件中回显**，客户端不得依赖该事件重建配置（见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)）。
- **错误处理**：所有非法参数均返回 `error` 事件，`param` 字段指示具体出错字段（如 `session.modalities`），需据此调试（见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)）。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)


