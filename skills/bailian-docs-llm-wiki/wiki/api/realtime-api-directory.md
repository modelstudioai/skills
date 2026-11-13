# realtime api directory

Realtime API 是百炼平台提供的低延迟、流式交互式模型服务接口集合，面向语音识别、语音合成、多模态对话、实时翻译等场景。所有接口均基于 WebSocket 协议实现双向流式通信，支持端到端毫秒级响应。该目录统一管理各实时能力的接入路径、协议规范与能力边界，是开发者集成实时 AI 能力的核心入口。

## 支持的模型/功能

Realtime API 目录涵盖以下核心实时能力模块：
- 实时多模态交互（含视觉理解与语音融合）：详见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- 实时语音识别（ASR）：支持多语种、带标点、说话人分离等高级选项  
- 实时语音合成（TTS）：提供音色可控、情感调节、低延迟[流式输出](../concepts/streaming-output.md)  
- 实时语音对话（Audio-based LLM Interaction）：端到端语音输入→语义理解→语音回复闭环  
- 实时音视频翻译（Live Translate）：支持双语字幕同步、源音保留、声道分离  
- AOQ SDK：轻量级客户端 SDK，封装连接管理、重连、buffer 控制等，降低接入复杂度  
- 多模态交互开发套件：定义标准协议帧结构与事件生命周期，便于自定义前端适配  

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 当前仅支持 `qwen-audio` 系列模型，而 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 已扩展支持 `qwen-vl-plus` 和 `qwen2-audio`，二者模型兼容范围存在差异，请按实际需求选型。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化时携带 query 参数或首帧 JSON 消息传递配置：
- `model`: 必填，指定模型 ID（如 `qwen2-audio`, `qwen-asr-zh`, `qwen-tts-en`），需与具体子目录文档一致  
- `stream`: 布尔值，控制是否启用流式响应（默认 `true`）  
- `language`: ASR/TTS 场景下必填（如 `zh`, `en`, `ja`）；多模态场景可选  
- `audio_format`: 输入音频编码格式（`pcm`, `wav`, `opus`），必须与实际发送数据匹配  
- `enable_interim_results`: ASR 专用，启用中间结果（默认 `false`）  
- `voice`: TTS 专用，指定音色 ID（见 [实时语音合成](../../raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档列表）  

## 使用方式

1. 建立 WebSocket 连接：使用 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>`，其中 `<endpoint>` 对应具体能力（如 `asr`, `tts`, `omni`, `livetranslate`）  
2. 发送初始化消息（JSON 格式），包含上述关键参数及认证信息（`api_key` 或 `Authorization` header）  
3. 按协议分帧发送音频/图像/文本数据（参考 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 定义的帧格式）  
4. 接收服务端推送的 `response`, `event`, `error` 等类型消息，处理流式结果  

## 限制和注意事项

- 单连接最大持续时长为 30 分钟，超时后需重建连接  
- 音频流要求采样率 16kHz、单声道、PCM 编码（除非 endpoint 明确支持其他格式）  
- ASR 输入音频长度无硬性上限，但建议单次会话不超过 2 小时以保障稳定性  
- TTS 输出音频默认为 24kHz PCM，不支持直接返回 MP3；如需压缩，须客户端自行转码  
- 所有 Realtime API **不支持 HTTP fallback**，必须使用 WebSocket；HTTP 接口仅用于鉴权或元数据查询  
- [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) 提供了自动重连与网络抖动缓冲机制，强烈推荐在移动端或弱网环境下使用

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


