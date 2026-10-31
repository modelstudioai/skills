# omni realtime api

Qwen-Omni-Realtime 是百炼平台提供的低延迟、多模态实时交互 API，支持语音输入/输出、文本生成、工具调用（Function Calling / MCP）、联网搜索等能力。它面向对话式 AI 场景设计，适用于智能客服、语音助手、实时会议摘要等对端到端延迟敏感的应用。协议层支持 AOQ、WebRTC 和 WebSocket 三种传输方式，开发者可根据网络环境与终端能力灵活选型。

## 支持的模型与功能

当前支持以下模型（均以 `qwen3` 系列命名）：
- `qwen3.8-omni-flash-realtime`
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime-2025-09-15`（实验性版本）

核心功能包括：
- **多模态 I/O**：支持 `["text"]` 或 `["text", "audio"]` 输出模态；音频输入支持单/双/四声道空间音频（仅 `qwen3.8-omni-flash-realtime`）；
- **语音活动检测（VAD）**：提供 `server_vad`（基础声学检测）、`semantic_vad`（语义有效性过滤）和 `semantic_vad_ec`（客服增强版，仅 `qwen3.8-omni-flash-realtime` 支持）；
- **工具调用**：同时支持 Function Calling（`type=function`）和 MCP（`type=mcp`），但二者不可与 `enable_search` 共存；
- **联网搜索**：通过 `enable_search: true` 启用，由模型自主触发；
- **输入音频转录**：固定使用 `qwen3-asr-flash-realtime` 模型，不可更换；
- **视频输入**：仅 `qwen3.8-omni-flash-realtime` 支持，需配置 `video.input.representation_compact`。

> **注意**：文档 3 中称“`output_audio_format` 当前仅支持设为 `pcm`，输出音频为 24 kHz 采样率”，但[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)明确说明 `qwen3.5-omni-plus-realtime` 和 `qwen3.5-omni-flash-realtime` 支持 `wav` 输出及 24000 Hz 采样率，且示例中 `session.audio.output.format.type = "wav"`、`sample_rate = 24000`。此处以[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)为准，服务端文档已过时。

## 关键参数

所有会话级配置通过 `session.update` 客户端事件设置，关键字段如下：

| 字段 | 类型 | 说明 | 默认值（按模型） |
|------|------|------|------------------|
| `modalities` | `array` | 输出模态，必须为 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 音色，新接入**必须使用 `audio.output.voice`**；`session.voice` 为兼容字段 | `Tina`（除 `qwen3-omni-flash-realtime-2025-09-15` 为 `Cherry`） |
| `audio.input.format` | `object` | 输入格式：`type`（`pcm`/`wav`）、`sample_rate`（8000/16000/24000/48000 Hz）；多通道仅支持 `pcm`+`16000` | `pcm` + `16000` |
| `audio.output.format` | `object` | 输出格式同上；`qwen3.5` 系列支持 `wav` | `pcm`（`qwen3.5` 系列默认 `wav`？见上条注意） |
| `turn_detection.type` | `string` | VAD 类型：`server_vad`（全模型）、`semantic_vad`（全模型）、`semantic_vad_ec`（仅 `qwen3.8`） | `server_vad` |
| `enable_search` | `boolean` | 是否启用联网搜索 | `false` |
| `tools` | `array` | 工具定义列表；`type=function` 或 `type=mcp`；与 `enable_search` 互斥 | — |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 采样控制参数；建议**只设置其中一个多样性参数** | 见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) |
| `max_tokens` | `integer` | 单次响应最大输出 Token 数；超限将截断 | `qwen3.8`: `[1, 65536]`；其余模型见[模型列表](../../raw/model-user-guide/get-started-with-models/models.md) |
| `smooth_output` | `boolean` | **仅 `qwen3-omni-flash-realtime-2025-09-15` 生效**：`true`（口语化）、`false`（书面化） | `true` |

> **注意**：`input_audio_transcription.model` 固定为 `"qwen3-asr-flash-realtime"`，不可修改；历史字段 `input_audio_format` 和 `output_audio_format` 已废弃，新接入应使用嵌套结构 `audio.input.format` 和 `audio.output.format`，详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 使用方式

1. **建立连接**：选择 AOQ、WebRTC 或 WebSocket 协议接入。推荐 WebSocket（[WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)）或 AOQ（[AOQ 接入](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)）。
2. **初始化会话**：连接后收到 `session.created` 服务端事件，包含默认配置。
3. **更新配置（可选）**：发送 `session.update` 事件调整参数（如 `modalities`, `voice`, `turn_detection` 等）；成功后服务端返回 `session.updated`。
4. **输入数据**：
   - 音频：持续发送 `input_audio_buffer.append`（Base64 PCM/WAV），VAD 模式下由服务端自动 `commit`；Manual 模式需显式发送 `input_audio_buffer.commit`。
   - 文本/图像：通过 `conversation.item.create` 发送（本文档未覆盖，参见其他事件文档）。
5. **触发响应**：VAD 模式下语音停止后自动响应；Manual 模式或 Function Calling 后续答需发送 `response.create`。
6. **处理响应**：监听 `response.created` → `conversation.item.created` → `response.content_part.added` → `response.done` 流式事件。
7. **取消响应**：发送 `response.cancel` 终止进行中的生成。

SDK 支持：[Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 和 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：`qwen3.8-omni-flash-realtime` 输入总 Token 上限为 196608；多通道音频输入（2/4 声道）Token 消耗为单声道的 2 倍；视频输入 `representation_compact=normal` 可降低 75% Token 开销。
- **音频约束**：
  - 多通道输入（`channels > 1`）**必须**使用 `pcm` + `16000` + `s16le` + `interleaved`，不可修改；
  - `input_audio_buffer.append` 的 Base64 数据需为原始 PCM/WAV，**不含容器头以外的元数据**；
  - `input_audio_buffer.commit` 在已追加图像缓冲区时会**同时提交图像**。
- **工具与搜索互斥**：`tools` 数组非空时，`enable_search` 必须为 `false`，否则返回 `invalid_request_error`。
- **MCP 敏感字段不回显**：`server_url`、`authorization`、`headers` 仅用于服务端连接，**不会出现在 `session.updated` 事件中**，客户端不可依赖该事件重建配置。
- **VAD 超时行为**：`idle_timeout_ms` 仅在 `qwen3.5` 系列 + `server_vad` 模式下生效；`semantic_vad_ec` 不支持该字段。
- **错误处理**：所有客户端事件错误均以 `error` 事件返回，含 `error.type`、`error.code` 和 `error.param`（如 `session.modalities`），便于定位问题。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


