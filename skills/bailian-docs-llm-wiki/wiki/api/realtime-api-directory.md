# realtime api directory

实时 API 目录是百炼平台面向低延迟、流式交互场景提供的统一入口，涵盖语音识别、语音合成、音视频对话、实时翻译及多模态交互等核心能力。所有接口均基于 WebSocket 协议设计，支持端到端流式传输与双向实时交互。开发者需通过 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 文档索引获取各子模块的详细规范。

## 支持的模型与功能

当前目录下包含以下六大类实时能力：
- 实时语音识别（ASR）：支持中文、英文等多语种流式识别，含标点恢复与说话人分离选项  
- 实时语音合成（TTS）：提供多音色、可控语速/语调的流式音频生成  
- 实时语音对话（Audio Realtime）：集成 ASR+LLM+TTS 的端到端对话流水线  
- 实时音视频翻译（LiveTranslate）：支持双语字幕同步、源音保留与目标语音合成  
- 实时多模态（Omni Realtime）：融合语音、文本、图像输入的联合理解与响应（参见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)）  
- 多模态交互协议：定义客户端与服务端间事件帧格式、状态同步机制（详见 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)）

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档中声明的 `enable_interactive_mode` 参数，在最新 SDK 版本中已更名为 `interactive_mode`，旧参数名将被弃用，请以 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 文档为准。

## 关键参数

通用必填参数（所有实时 API 共享）：
- `model`: 模型标识符，如 `qwen2-audio-realtime-v1`、`qwen2-asr-v1`，具体取值见各子模块文档  
- `stream`: 布尔值，必须为 `true`  
- `audio_format`: 输入音频编码格式，支持 `pcm16`、`opus`、`mp3`（部分模型仅支持 `pcm16`）  
- `sample_rate`: 音频采样率，常见值为 `16000` 或 `48000`，需与 `audio_format` 匹配  

功能特有参数示例：
- ASR：`punctuation_prediction`, `speaker_diarization`  
- TTS：`voice`, `speed`, `pitch`  
- LiveTranslate：`source_lang`, `target_lang`, `subtitle_mode`（`single_line` / `dual_line`）

## 使用方式

1. **建立连接**：使用标准 WebSocket 客户端连接 `wss://dashscope.aliyuncs.com/realtime/v1/...`，携带 `Authorization: Bearer <api_key>` 与 `X-DashScope-Date` 时间戳头  
2. **发送初始化帧**：首帧为 JSON 格式 `{"type": "session.update", "parameters": {...}}`，声明模型、参数及会话配置  
3. **流式收发数据**：后续按协议帧类型（`input.audio`, `response.text.delta`, `event.error` 等）双向传输二进制音频或结构化事件  
4. **关闭连接**：发送 `{"type": "session.terminate"}` 或等待服务端超时断连  

推荐优先使用官方 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 或 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)，其已封装连接管理、重连逻辑与帧解析。

## 限制和注意事项

- 单次会话最大时长：30 分钟（ASR/TTS 为 60 分钟）；超时后连接强制关闭，需重建会话  
- 音频输入缓冲区上限：单次 `input.audio` 帧不超过 64KB（约 2 秒 16kHz PCM），建议分片发送  
- 并发连接数：免费版限 5 路，企业版按配额配置，超出返回 `429 Too Many Requests`  
- 所有实时 API **不支持 HTTP 轮询调用**，仅接受 WebSocket 连接；尝试 HTTP 请求将返回 `405 Method Not Allowed`  
- 服务端错误事件（`event.error`）中 `code` 字段遵循 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 定义的统一错误码体系，如 `InvalidParameter`、`AudioFormatNotSupported`

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


