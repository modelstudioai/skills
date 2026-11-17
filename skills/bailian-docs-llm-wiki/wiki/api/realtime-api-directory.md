# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持毫秒级响应与持续上下文维护。该目录是实时类 API 的统一入口，各子模块按功能垂直划分，便于开发者按需集成。

## 支持的模型与功能

Realtime API 当前覆盖以下核心能力：
- **实时语音识别（ASR）**：支持中英文混合、多方言、带标点与语义断句的流式识别；  
- **实时语音合成（TTS）**：提供多音色、可控语速/语调的音频流输出；  
- **实时语音对话（Audio Chat）**：端到端流式对话，集成 ASR + LLM + TTS 闭环；  
- **实时音视频翻译（LiveTranslate）**：支持源音视频流输入、目标语言音频流输出；  
- **实时多模态交互（Omni）**：融合语音、文本、图像、动作信号的统一实时协议；  
- **AOQ SDK**：轻量客户端 SDK，封装连接管理、重连、缓冲与事件回调；  
- **多模态交互开发套件**：定义标准消息格式、状态机与错误码体系，用于自定义协议扩展。  
详细能力说明请参见 [Realtime API](../../raw/model-api-reference/realtime-api-directory.md) 主目录页。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化，必需参数包括：
- `model`: 模型标识符（如 `qwen2-audio-realtime-v1`, `qwen2-omni-realtime-v1`），必须与所选子功能匹配；  
- `api_key`: 有效平台 API Key，需具备对应模型调用权限；  
- `stream`: 布尔值，必须为 `true`；  
- `response_format`: 可选，指定返回结构（如 `json`, `pcm`, `mp3`），不同子接口支持范围不同；  
- `input_format` / `output_format`: 音频编解码参数（如 `wav`, `opus`, `pcm-16k`），需与实际流数据一致。  
具体参数约束详见 [实时语音识别](../../raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 和 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档。

## 使用方式

1. 建立 WebSocket 连接，URL 格式为 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>`，其中 `<endpoint>` 对应具体功能（如 `asr`, `tts`, `audio-chat`, `livetranslate`, `omni`）；  
2. 发送 `{"type": "session.update", ...}` 初始化会话，携带认证与配置参数；  
3. 按协议分帧发送音频/文本/图像数据（如 `{"type": "input.audio", "data": "..."}`）；  
4. 实时接收服务端流式响应（含 partial result、final result、event、error 等类型）；  
5. 主动发送 `{"type": "session.terminate"}` 或关闭连接以结束会话。  
完整交互流程与消息示例见 [实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档。

## 限制和注意事项

- 单连接最大时长为 30 分钟，超时后需重建连接；  
- 音频流采样率须严格匹配模型要求（如 ASR 默认 16kHz，TTS 输出默认 24kHz），不匹配将导致静音或解码失败；  
- `omni-realtime-api-directory.md` 中描述的“图像帧内嵌 OCR 结果”功能，当前仅对白名单客户开放，普通账号调用将返回 `403 Forbidden`；  
> **注意**：`livetranslate-realtime-api-directory.md` 中标注的“支持 5 种目标语言”，与 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 文档中“翻译能力已统一归入 Omni 协议”的说明存在路径冗余——实际生产环境推荐优先使用 Omni 接口实现音视频翻译，`livetranslate` 子目录已进入维护模式，新项目不应依赖。  
- AOQ SDK 的 `v1.2.0+` 版本强制要求 TLS 1.3，旧版客户端可能握手失败；相关兼容性细节见 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


