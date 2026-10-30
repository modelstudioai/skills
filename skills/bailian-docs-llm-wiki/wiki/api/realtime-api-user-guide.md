# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时对话、音视频场景下的模型调用。它基于 WebSocket 协议实现，支持服务端主动推送事件（如 `response.audio.delta`、`input_audio_buffer.committed`），并允许客户端在会话中动态插入音频或文本输入。该接口不兼容传统 REST 调用方式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 仅支持 `qwen-audio-7b` 和 `qwen2-audio-7b` 两款音频理解与生成模型（详见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）。功能包括：  
- 实时语音识别（ASR）与合成（TTS）  
- 多轮上下文感知的语音对话（支持 `tool_choice` 和[函数调用](../concepts/function-calling.md)）  
- 音频缓冲区管理（`input_audio_buffer.*` 事件）  
- 会话级状态同步（如 `session.created`、`response.done`）  

> **注意**：文档 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中提及的 `qwen-vl-realtime` 模型已下线，实际调用将返回 `404 Model not found`，请以 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的模型列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-audio-7b` 或 `qwen2-audio-7b`（大小写敏感） |
| `modalities` | array | 否 | 默认 `["text", "audio"]`；若仅需文本输出，可设为 `["text"]` 以降低带宽消耗 |
| `temperature` | number | 否 | 范围 `[0.0, 1.0]`，默认 `0.7`；值越低输出越确定 |
| `max_output_tokens` | integer | 否 | 单次响应最大 token 数，上限 `4096`（参见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)） |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/audio` 发起连接，携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Date` 时间戳头（RFC3339 格式）  
2. **发送 `session.update` 消息** 初始化会话参数（含 `model`、`modalities` 等）  
3. **流式发送音频**：通过 `input_audio_buffer.append` 事件提交 PCM 编码音频（16-bit, 16kHz, mono），每次 ≤ 100ms  
4. **处理服务端事件**：监听 `response.text.delta`、`response.audio.delta` 等事件，按需拼接输出  

推荐使用官方 AOQ 客户端 SDK（Python/JS），其自动处理重连、心跳、事件解析等细节：[AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单会话最长持续 300 秒，超时后连接关闭且不可续期  
- 音频输入必须为未压缩的 `LINEAR16` PCM 格式，采样率严格限定为 `16000` Hz；其他格式（如 MP3、Opus）将导致 `400 Invalid audio format` 错误  
- 同一 API Key 下并发 WebSocket 连接数上限为 5，超出将拒绝新连接（错误码 `429 Too Many Connections`）  
- 服务端不会缓存历史会话数据，`session.update` 中修改 `system` 提示词仅对后续响应生效，不影响已发出的 `response.*` 流  

> **注意**：[快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中示例使用的 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 地址已废弃，正确 endpoint 为 `wss://dashscope.aliyuncs.com/realtime/v1/audio`，请以 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档中的初始化逻辑为准。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


