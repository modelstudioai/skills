# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式语音交互接口，适用于实时语音识别（ASR）、语音合成（TTS）与多模态对话等场景。它基于 WebSocket 协议实现双向流式通信，支持端到端毫秒级响应。该接口不经过传统 REST 请求-响应周期，需按协议规范建立并维护长连接。

## 支持的模型与功能

当前 Realtime API 支持以下核心能力：
- 实时语音识别（ASR）：支持中文普通话、英文及部分方言，采样率 16kHz，PCM/WAV 格式输入；
- 实时语音合成（TTS）：支持音色定制与语速/语调调节，输出为 PCM 流；
- 混合交互模式（ASR+LLM+TTS）：可启用 `enable_interactive_mode: true` 实现边说边思考边读的全链路流式响应。

所支持的具体模型列表详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节，其中明确列出 `qwen-audio-realtime-v1` 和 `qwen-tts-realtime-v2` 为当前 GA 版本模型。> **注意**：文档中提及的 `qwen-asr-realtime-beta` 已于 v2.3.0 版本下线，实际调用将返回 404；请以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的模型 ID 为准。

## 关键参数

建立 WebSocket 连接时，必需在 URL 查询参数中指定：
- `model`: 模型标识符（如 `qwen-audio-realtime-v1`）；
- `api_key`: 有效且具备 `realtime_api` 权限的 API Key；
- `sample_rate`: 输入音频采样率（仅 ASR/TTS 场景需匹配，推荐 `16000`）；
- `response_format`: 可选 `json`（结构化事件）或 `binary`（原始音频流），默认 `json`。

消息体中关键字段包括：
- `audio`: Base64 编码的原始 PCM 数据（小端、16bit）；
- `stream_id`: 客户端生成的 UUID，用于关联请求与响应事件；
- `enable_interactive_mode`: 布尔值，启用后服务端将按 token 粒度推送 `text_delta` 与 `audio_chunk` 事件。

完整参数定义参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档中的 `RealtimeRequest` 接口说明。

## 使用方式

1. 构造 WebSocket 连接 URL：`wss://dashscope.aliyuncs.com/realtime/v1/audio?model=qwen-audio-realtime-v1&api_key=...`  
2. 发送 `session.start` 控制事件初始化会话（含语言、角色等配置）；  
3. 持续发送 `input.audio` 事件流式上传音频帧（建议每帧 20–40ms）；  
4. 监听 `output.text_delta`、`output.audio_chunk` 等事件，按 `stream_id` 聚合响应；  
5. 主动发送 `session.end` 或等待超时自动断连。

示例代码与错误码映射见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。注意：重连机制需由客户端实现，服务端不维护连接状态。

## 限制和注意事项

- 单连接最大持续时长：180 秒（含静默期），超时后连接关闭且不触发 `session.end` 事件；  
- 音频帧间隔建议 ≤ 50ms，间隔过长（>200ms）可能导致 ASR 误切句；  
- 不支持 HTTP/2 或 gRPC，仅限标准 WebSocket（`wss://`）；  
- `audio_chunk` 输出为裸 PCM（16kHz, 16bit, mono），无 WAV 头，客户端需自行封装；  
- 同一 `api_key` 并发连接数上限为 10，超出将拒绝新连接（HTTP 429）。

> **注意**：[概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提到的“支持自定义 VAD 端点检测”尚未开放，当前 VAD 完全由服务端控制，`vad_enabled` 参数暂无效。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


