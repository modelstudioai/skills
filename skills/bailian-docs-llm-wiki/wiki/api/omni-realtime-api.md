# omni realtime api

Qwen-Omni-Realtime 是面向多模态实时交互场景的低延迟大模型 API，支持文本、音频（含空间音频）、视频输入与文本+音频联合输出。它提供 WebSocket、WebRTC 和 AOQ 三种传输协议接入方式，适用于智能客服、实时语音助手、会议纪要等对端到端延迟敏感的场景。所有模型均基于统一的 Realtime API 协议设计，事件驱动、双向流式交互。

## 支持的模型/功能

当前支持以下模型（按发布顺序）：
- `qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`
- `qwen3.8-omni-flash-realtime`（新增空间音频、视频输入、MCP 工具集成）
- `qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`（部分参数不可调）

核心功能包括：
- 多模态输入：单/双/四通道 PCM 音频（16 kHz）、WAV 封装音频、视频帧（Qwen3.8-Omni-Flash-Realtime）
- 多模态输出：文本 + 可配置采样率/格式的合成语音（`pcm` 或 `wav`）
- 实时语音活动检测（VAD）：支持 `server_vad`（声学）和 `semantic_vad`（语义）两种模式
- 工具调用：Function Calling（`type=function`）与 MCP（`type=mcp`）双轨支持，但二者不可与 `enable_search` 同时启用
- 联网搜索：仅 `qwen3.8-omni-flash-realtime` 和 `qwen3.5-omni-realtime` 系列支持，需显式设置 `enable_search: true`

> **注意**：文档 3 中 `session.created` 示例显示 `"output_audio_format": "pcm"` 且注明“当前不支持自定义输出采样率”，但文档 2 明确说明 `session.audio.output.format.sample_rate` 在 `qwen3.5-omni-plus-realtime` 等模型上可设为 8000/16000/24000/48000 Hz，默认 24000 Hz。该矛盾以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 为准，服务端事件中的限制性描述已过时。

## 关键参数

所有会话通过 `session.update` 事件初始化或更新，关键参数如下：

| 参数 | 类型 | 说明 | 默认值/约束 |
|------|------|------|-------------|
| `modalities` | `array` | 输出模态，仅支持 `["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` / `audio.output.voice` | `string` | 合成音色 | `Tina`（Qwen3.5/Qwen3.8 系列），`Cherry`（Qwen3-Omni-Flash）；新接入**必须使用 `audio.output.voice`** |
| `audio.input.format` | `object` | 输入音频格式：`type`（`pcm`/`wav`）、`sample_rate`（8k/16k/24k/48k Hz）；Qwen3.8 多通道强制 `pcm`+`16000` | `{"type":"pcm","sample_rate":16000}` |
| `audio.output.format` | `object` | 输出音频格式：同上，`sample_rate` 可设为 24000 Hz（推荐） | `{"type":"wav","sample_rate":24000}` |
| `turn_detection` | `object` | VAD 配置：`type`（`server_vad`/`semantic_vad`）、`threshold`（-1.0~1.0）、`silence_duration_ms`（200~6000 ms） | `{"type":"server_vad","threshold":0.5,"silence_duration_ms":800}` |
| `enable_search` | `boolean` | 启用联网搜索 | `false`；与 `tools` 互斥 |
| `tools` | `array` | Function Calling 或 MCP 工具定义 | 空数组；[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 提供完整 schema |
| `temperature` / `top_p` / `top_k` | `float`/`integer` | 生成控制参数 | 各模型默认值不同，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 表格；**建议只设置其中一个多样性参数** |
| `max_tokens` | `integer` | 响应最大 Token 数 | Qwen3.8：1~65536；其他模型见 [模型列表](raw/model-user-guide/get-started-with-models/models.md) |

> **注意**：`qwen-omni-turbo` 系列模型**不支持修改** `temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等全部生成参数，文档 2 和文档 3 中相关默认值说明对其不适用。

## 使用方式

1. **建立连接**：选择 WebSocket（推荐）、WebRTC 或 AOQ 协议接入。WebSocket 连接地址与握手流程详见 [WebSocket 接入指南](../../raw/_short/omni-realtime-interaction-process-c1786114b7f9b9c5.md)。
2. **初始化会话**：连接成功后，立即发送 `session.update` 事件（含完整 `session` 对象）。服务端校验通过后返回 `session.created`（首次）或 `session.updated`（后续更新）。
3. **音频输入**：
   - VAD 模式：持续发送 `input_audio_buffer.append` 二进制数据，服务端自动触发 `speech_started`/`speech_stopped`/`committed` 事件；
   - Manual 模式：发送 `input_audio_buffer.commit` 显式提交。
4. **接收响应**：服务端推送 `conversation.item.created`（含文本/音频/工具调用）、`response.audio.delta`（音频流片段）、`response.text.delta`（文本流片段）等事件。
5. **SDK 快速启动**：官方提供 Python 和 Java SDK，封装连接管理、事件解析与重试逻辑，详见 [Python SDK](../../raw/_short/omni-realtime-python-sdk-c6ee137356d19420.md) 和 [Java SDK](../../raw/_short/omni-realtime-java-sdk-80f4b2a483df02c3.md)。

## 限制和注意事项

- **Token 限制**：Qwen3.8-Omni-Flash-Realtime 单次 `session.update` 的 `session` 对象总 Token 上限为 196608；输入音频 Token 计算与声道数强相关（2/4 声道为单声道 2 倍），详见 [Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。
- **音频配置时机**：`audio.input.format` 和 `audio.output.format` **必须在首段音频发送前完成配置**，音频流开始后不可修改。
- **多通道约束**：Qwen3.8-Omni-Flash-Realtime 的多通道输入（2/4 声道）强制要求 `type=pcm`、`sample_rate=16000`、`sample_format=s16le`、`packing=interleaved`，`channel_layout` 需与 `channels` 匹配（1→`mono`，2→`raw_mic_array`，4→`foa_ambix`）。
- **工具与搜索互斥**：`tools` 数组非空时，`enable_search` 必须为 `false`，反之亦然。
- **错误处理**：服务端返回 `error` 事件时（如 `invalid_request_error`），需检查 `error.param` 字段定位问题参数，例如 `session.modalities` 不合法会明确提示支持的组合。
- **音色兼容性**：`session.voice` 是历史字段，新接入必须使用 `session.audio.output.voice`；若两者同时存在，以 `audio.output.voice` 为准。

## 来源文档

- [Qwen-Omni-Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md)
- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)


