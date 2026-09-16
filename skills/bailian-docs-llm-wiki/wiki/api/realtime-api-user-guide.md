# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式语音交互接口，适用于实时语音识别（ASR）、语音合成（TTS）与多模态对话等场景。它基于 WebSocket 协议实现双向流式通信，支持端到端毫秒级响应。该接口不经过传统 REST 请求-响应周期，需客户端维持长连接并按帧发送/接收数据。

## 支持的模型与功能

当前 Realtime API 支持以下核心能力：
- 实时语音识别（ASR）：支持中文普通话、英文及部分方言，采样率 8kHz / 16kHz，输入格式为 PCM 或 OPUS；
- 流式语音合成（TTS）：支持音色克隆与多语种混读，输出为 OPUS 流；
- ASR+TTS 级联模式（即“语音对话”模式），支持上下文感知的实时打断与重写。

> **注意**：文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen2-audio-realtime` 模型已在 v2.3.0 版本中下线，实际可用模型请以 [实时 API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的「当前支持模型列表」为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-asr-v2`、`qwen2-audio-tts-v1`；详见 [实时 API 概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) |
| `audio_format` | string | 是 | 输入音频编码格式，取值 `pcm` 或 `opus`；必须与实际帧数据一致 |
| `sample_rate` | integer | 是 | 音频采样率，单位 Hz，仅当 `audio_format=pcm` 时生效（`8000` 或 `16000`） |
| `enable_interim_results` | boolean | 否 | 是否返回中间识别结果，默认 `true`；设为 `false` 可降低带宽消耗 |
| `max_duration_ms` | integer | 否 | 单次会话最大持续时间（毫秒），默认 `60000`（60 秒），最大支持 `300000` |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/audio` 发起连接，携带认证 Header（`Authorization: Bearer <api_key>`）；
2. **发送初始化消息（`session.update`）**：包含 `model`、`audio_format` 等参数；
3. **流式发送音频帧（`input.audio`）**：每帧为 Base64 编码的原始音频字节，建议单帧 ≤ 20ms（如 16kHz 下约 320 字节 PCM）；
4. **接收服务端事件**：包括 `response.text.delta`（识别增量文本）、`response.audio.delta`（合成音频片段）、`error` 等；
5. **结束会话**：发送 `session.terminate` 或关闭连接。

完整示例代码与错误码说明见 [实时 API 快速开始指南](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制和注意事项

- 单连接最大并发会话数：1；
- 音频帧间隔建议 ≤ 100ms，超时未收到新帧将触发自动断连（默认 5s 超时）；
- 不支持 HTTP/HTTPS 直接调用，必须使用 WebSocket；
- AOQ 客户端 SDK 提供封装好的连接管理与编解码逻辑，推荐在生产环境使用 —— 具体集成方式参见 [AOQ 客户端 SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)；
- 若使用自定义音频预处理，请确保 PCM 数据为小端序、16-bit signed integer 格式，且无额外头信息（如 WAV header）。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


