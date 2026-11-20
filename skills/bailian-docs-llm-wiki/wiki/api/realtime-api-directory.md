# realtime api directory

实时 API 目录汇总了百炼平台支持的低延迟、流式交互类音视频模型能力，覆盖语音识别（ASR）、语音合成（TTS）、语音对话、音视频翻译及多模态实时交互等场景。所有接口均基于 WebSocket 协议设计，强调端到端延迟控制与上下文连续性。开发者需结合 [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md) 的子模块文档进行具体集成。

## 支持的模型/功能

当前目录包含以下核心实时能力：
- 实时语音识别（ASR）：支持多语种、带标点与说话人分离的流式识别  
- 实时语音合成（TTS）：支持情感韵律控制与低延迟音频流输出  
- 实时语音对话（Audio Chat）：端到端流式双工对话，含语音输入→语义理解→语音响应闭环  
- 实时音视频翻译（LiveTranslate）：支持源音视频流实时转译为目标语言语音+字幕  
- 实时多模态（Omni）：融合语音、文本、视觉信号的联合理解与生成（见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)）  
- 多模态交互协议：定义客户端与服务端间事件、状态、媒体流的标准化交互格式（详见 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md)）

> **注意**：[实时语音对话](../../raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 文档中描述的 `enable_interactive_mode` 参数在 v2.3.0 SDK 中已弃用，实际应使用 `session_config.interactive` 字段；请以 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 最新版说明为准。

## 关键参数

通用关键参数（适用于多数实时接口）：
- `model`: 模型标识符，如 `qwen2-audio-realtime-v1`、`qwen2-tts-realtime-v1`  
- `audio_format`: 输入/输出音频编码格式，支持 `pcm16`、`opus`（需与 `sample_rate` 匹配）  
- `sample_rate`: 采样率，ASR/TTS 均要求 `16000`，部分多模态模型支持 `48000`  
- `enable_streaming`: 必须为 `true`，启用流式响应  
- `max_latency_ms`: 端到端延迟上限（毫秒），默认 `800`，最小可设 `300`（受模型与网络制约）  
- `session_id`: 可选，用于跨请求关联会话上下文（推荐在长会话中显式传入）

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/<endpoint>` 发起连接，其中 `<endpoint>` 对应具体能力（如 `asr`、`tts`、`audio-chat`）  
2. **发送初始化消息（Init）**：携带 `model`、`audio_format` 等参数的 JSON 对象  
3. **流式传输数据**：按协议分帧发送音频二进制数据或控制事件（如 `audio_chunk`、`user_input`）  
4. **接收流式响应**：服务端推送 `transcript`、`audio_chunk`、`response_text` 等事件（结构详见各子模块文档）  
5. **关闭连接**：发送 `close` 事件或由服务端超时断连  

SDK 封装推荐使用官方 [WebSocket SDK](../../raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk.md) 或 [AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)，避免手动处理帧协议与重连逻辑。

## 限制和注意事项

- 单连接最大持续时长：15 分钟（ASR/TTS）或 10 分钟（Audio Chat/Omni），超时后需重建连接  
- 音频输入必须为单声道、小端序 PCM（`pcm16`）或标准 Opus 封包；非标准格式将导致 `400 Bad Request`  
- 同一 `session_id` 不支持跨 endpoint 复用（例如 ASR session 不能直接用于 TTS）  
- 实时多模态（Omni）目前仅限白名单客户开通，申请入口见 [实时多模态](../../raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md)  
- 所有实时 API 均不支持 HTTP 轮询调用，仅限 WebSocket 协议；尝试 HTTP POST 将返回 `405 Method Not Allowed`

## 来源文档

- [音视频（实时）](../../raw/model-api-reference/realtime-api-directory.md)


