# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持毫秒级响应与持续上下文维护。该目录是实时类 API 的统一入口，各子模块按功能垂直划分，便于开发者按需集成。

## 支持的模型与功能

Realtime API 当前覆盖以下核心能力：
- **实时语音识别（ASR）**：支持中英文混合、多方言、带标点和语义断句的流式识别，模型包括 `qwen2-audio-realtime-asr-zh` 等；  
- **实时语音合成（TTS）**：提供多音色、可控语速/停顿/情感的流式音频生成，支持 SSML 片段注入；  
- **实时语音对话（Audio Chat）**：端到端流式语音对话，集成 ASR + LLM + TTS 闭环，支持打断、静音检测与角色扮演；  
- **实时音视频翻译（LiveTranslate）**：双语语音流实时互译，支持源语种自动检测与目标语种指定；  
- **多模态实时交互（Omni）**：融合语音、文本、图像输入的统一实时推理协议，适用于智能硬件与会议系统；  
- **AOQ SDK 集成支持**：提供轻量客户端 SDK，封装连接管理、重连、缓冲与事件回调，详见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 文档。

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 中描述的 `enable_interactive_mode` 参数在最新 v2.3 协议中已弃用，实际应使用 `interaction_config` 对象配置，以 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 中定义为准。

## 关键参数

所有 Realtime API 共享以下基础参数（WebSocket 连接建立时通过 `init` 消息传递）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-realtime-chat-zh`，完整列表见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) |
| `audio_format` | string | 否 | 输入音频编码格式，支持 `pcm16`（默认）、`opus`；输出格式由模型决定 |
| `sample_rate` | integer | 否 | 输入采样率（Hz），仅当 `audio_format=pcm16` 时生效，支持 8000 / 16000（默认） |
| `enable_audio_output` | boolean | 否 | 是否启用音频流输出（TTS 或翻译结果），默认 `true`；设为 `false` 时仅返回文本事件 |

其他功能专属参数（如 `asr_language`, `tts_voice`, `translate_target_lang`）请参考对应子文档，例如 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md)。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/<service>` 发起连接（`<service>` 如 `asr`, `tts`, `chat`, `livetranslate`）；  
2. **发送 init 消息**：首帧必须为 JSON 格式的 `init` 控制消息，携带上述关键参数；  
3. **流式收发数据**：后续按协议分帧发送音频二进制数据或文本指令，接收 `audio`, `text`, `event` 等类型响应；  
4. **处理生命周期事件**：监听 `connected`, `error`, `session_ended`, `interrupted` 等事件，实现健壮重连逻辑；  
5. **关闭连接**：发送 `{"type": "close"}` 或直接断开，服务端将在 30 秒后自动清理会话。

推荐优先使用官方 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)，其已内置连接池、心跳保活与错误码映射。

## 限制和注意事项

- 单连接最大会话时长为 30 分钟，超时将触发 `session_ended` 事件；  
- 音频输入流需严格按 `sample_rate` 和 `audio_format` 编码，否则导致 ASR 识别失败或 TTS 输出异常；  
- 实时对话类接口（`chat`, `livetranslate`, `omni`）不支持跨会话上下文共享，每次 `init` 均为全新会话；  
- 免费调用量受项目级配额限制，超出后返回 `429 Too Many Requests`，具体配额策略参见 [概述](../../raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)；  
- 所有音频流必须连续发送，单次间隔超过 5 秒将被服务端判定为静音并可能终止识别流程。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


