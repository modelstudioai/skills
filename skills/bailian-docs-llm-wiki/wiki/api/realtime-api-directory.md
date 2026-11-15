# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持毫秒级响应与持续上下文维护。该目录是实时类 API 的统一入口，各子模块按功能垂直划分，便于开发者按需集成。

## 支持的模型与功能

Realtime API 当前覆盖以下核心能力：
- **实时语音识别（ASR）**：支持中英文混合、多方言、带标点和语义断句的流式识别，模型包括 `qwen2-audio-realtime-asr-zh` 等；  
- **实时语音合成（TTS）**：提供多音色、可控语速/停顿/情感的流式音频生成，支持 SSML 片段注入；  
- **实时语音对话（Audio Chat）**：端到端流式语音问答，内置声学前端与语言模型协同优化；  
- **实时音视频翻译（LiveTranslate）**：支持源语语音→目标语语音/文本的跨语言实时转换；  
- **多模态实时交互（Omni）**：融合语音、文本、图像、动作信号的统一实时理解与生成，详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)；  
- **AOQ SDK 集成支持**：提供轻量客户端 SDK，封装连接管理、重连、缓冲与事件回调，降低接入复杂度，具体见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)。

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档中提及的 `audio-chat-v1` 模型已下线，当前默认使用 `qwen2-audio-realtime-chat`，请以 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 中的模型列表为准。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化时携带 query 参数或首帧 JSON message 传递配置：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-realtime-asr-zh`，完整列表见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 等子文档 |
| `language` | string | 否 | ASR/TTS 场景下指定语言代码（如 `zh`, `en`），部分模型自动检测 |
| `response_format` | string | 否 | 可选 `text` / `json` / `audio/wav`，影响返回内容类型 |
| `enable_interim_results` | boolean | 否 | ASR/TTS 默认 `true`，控制是否推送中间结果 |
| `max_input_length` | integer | 否 | 单次会话最大输入 token 或音频时长（毫秒），超限将触发截断 |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>` 发起连接，其中 `<endpoint>` 对应具体能力（如 `asr`, `tts`, `omni`）；  
2. **发送初始化消息（Init Message）**：首帧为 JSON，包含 `model`、`parameters` 等字段，格式参考 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 定义；  
3. **流式收发数据**：后续帧可为二进制音频（PCM/WAV）、文本或结构化指令（如 `{"type": "input_audio", "data": "..."}`）；  
4. **处理事件流**：服务端按 `event: audio`, `event: text`, `event: error` 等类型推送 SSE 兼容事件，客户端需按协议解析。

## 限制和注意事项

- 单连接最长存活时间 30 分钟，超时后需重建；  
- 音频输入采样率必须为 16kHz（单声道 PCM），其他格式需客户端预转码；  
- TTS 输出音频默认为 24kHz PCM，不支持 MP3 流式编码；  
- 实时音视频翻译（LiveTranslate）暂不支持自定义术语表，该能力将在下一版本通过 [实时音视频翻译](../../raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md) 更新；  
- 所有 Realtime API 均不支持 HTTP fallback，仅限 WebSocket；  
- 错误码统一遵循 RFC 6455 规范，常见 `4001`（鉴权失败）、`4003`（模型不可用）、`4007`（输入超限）。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


