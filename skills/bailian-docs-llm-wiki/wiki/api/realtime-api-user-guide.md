# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式语音交互接口，适用于实时语音识别（ASR）、语音合成（TTS）、语音转文字+意图理解等端到端场景。它基于 WebSocket 协议实现双向流式通信，支持音频流边传边处理，响应延迟通常低于 300ms（端到端）。该接口需配合 AOQ 客户端 SDK 或原生 WebSocket 实现接入，详细行为请参考 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 支持的模型与功能

- **语音识别（ASR）**：支持 `qwen-audio-realtime-asr-v1`（中文为主，含基础英文热词识别）  
- **语音合成（TTS）**：支持 `qwen-audio-realtime-tts-v1`（中文语音，多音色可选）  
- **语音交互（ASR+LLM+TTS）**：支持 `qwen-audio-realtime-conversation-v1`，内置对话状态管理与流式响应  
- 所有模型均仅支持采样率 16kHz、单声道、PCM 编码的原始音频帧（无 WAV 头），具体格式要求见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中的“接入模型与应用”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-conversation-v1`；必须与 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 兼容的模型列表一致 |
| `audio_format` | string | 是 | 固定为 `"pcm"`；不支持 `wav`、`mp3` 等封装格式 |
| `sample_rate` | integer | 是 | 固定为 `16000`；其他值将被拒绝 |
| `enable_interim_results` | boolean | 否 | 默认 `false`；设为 `true` 时返回中间识别结果（ASR 场景适用） |
| `voice` | string | 否 | TTS 或 conversation 场景下指定音色，如 `"zhiyuan"`；取值范围见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的快速开始指南 |

> **注意**：文档中 `max_duration_ms` 参数在 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中标注为“推荐 ≤ 60000”，但 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中明确说明服务端硬限制为 120000ms（2 分钟），实际以服务端限制为准。

## 使用方式

1. **认证**：使用 `X-DashScope-Access-Token` 请求头传递临时 [Token](../concepts/token.md)（通过 `/api/v1/tokens` 获取）  
2. **建连**：向 `wss://dashscope.aliyuncs.com/api/v1/realtime` 发起 WebSocket 连接，携带上述参数作为 query string（如 `?model=qwen-audio-realtime-conversation-v1&audio_format=pcm`）  
3. **发送音频**：按 20–200ms 帧长分片发送原始 PCM 数据（每次 `binary` message ≤ 64KB）  
4. **接收响应**：服务端以 JSON 消息流返回事件（`event: "audio"` / `"text"` / `"error"`），结构详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档  

建议优先使用官方 AOQ SDK（支持 Web/iOS/Android），其已封装重连、心跳、帧缓冲等逻辑，避免手动实现导致连接中断或音频失步。

## 限制和注意事项

- 单连接最长持续 120 秒（含静音等待），超时后服务端主动关闭连接  
- 音频流中断超过 5 秒（无新帧到达）将触发会话终止  
- 不支持跨 session 的上下文继承；如需多轮对话，请在 `conversation-v1` 模型中复用同一连接，并依赖服务端维护的会话状态  
- 所有音频数据在传输中未加密（TLS 已保障链路安全），但**禁止上传含 PCI-DSS 或 HIPAA 敏感字段的语音**（如银行卡号、病历详情）——该限制在 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中有明确合规声明。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


