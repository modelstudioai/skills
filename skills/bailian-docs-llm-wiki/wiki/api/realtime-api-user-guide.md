# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时音视频辅助、多轮对话等需要毫秒级响应的场景。它基于 WebSocket 协议实现全双工通信，支持模型推理过程中的中间结果实时返回与用户动态干预。该接口不兼容传统 REST 同步调用模式，需使用专用客户端 SDK 或原生 WebSocket 实现。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime-v1` 和 `qwen-video-realtime-v1` 为主，具体以 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中“接入模型与应用”章节为准）。核心功能包括：  
- 音频/视频流实时输入与模型侧流式响应（token 级别）  
- 用户在会话中动态插入文本指令（如 `{"type": "user_input", "text": "暂停"}`）  
- 模型状态事件通知（如 `input_started`、`output_finished`）  
- 会话上下文自动维护（最长 30 分钟无活动自动过期）

> **注意**：文档 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen2.5-realtime` 模型尚未在生产环境上线，实际可用模型请以控制台模型列表或 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的 `curl -X GET https://dashscope.aliyuncs.com/api/v1/realtime/models` 返回结果为准。

## 关键参数

建立连接时必需通过 query string 传递以下参数：  
- `model`: 模型 ID（必填，如 `qwen-audio-realtime-v1`）  
- `api_key`: 有效 DashScope API Key（需具备 `realtime:inference` 权限）  
- `response_format`: 可选，`json`（默认）或 `binary`（仅音频/视频原始帧）  

消息体中关键字段（详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)）：  
- `audio_chunk`: base64 编码的 PCM 音频片段（16-bit, 16kHz, mono）  
- `video_frame`: H.264 Annex B 格式帧（仅 `qwen-video-realtime-v1`）  
- `stream_options.intermediate_results`: 布尔值，控制是否返回中间 token（默认 `true`）

## 使用方式

1. **建立 WebSocket 连接**：  
   ```bash
   wscat -c "wss://dashscope.aliyuncs.com/api/v1/realtime?model=qwen-audio-realtime-v1&api_key=sk-xxx"
   ```
2. **发送初始化消息**（JSON 格式）：  
   ```json
   {"type": "session_update", "turn_detection": {"type": "vad", "threshold": 0.5}}
   ```
3. **持续发送音频/视频帧 + 接收流式响应**：每帧需带 `type: "input_audio"` 或 `type: "input_video"`，服务端按需返回 `type: "output_text_delta"` 或 `type: "output_audio"`。完整协议细节见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大持续时间：600 秒（10 分钟），超时后需重连并新建会话  
- 音频输入采样率严格限定为 16kHz，非标准格式将被静音丢弃（参见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)）  
- 不支持跨模型热切换；若需切换模型，必须关闭当前连接并新建 WebSocket  
- 错误码 `429 Too Many Requests` 表示账户级并发连接数超限（默认 5 路），需联系技术支持调整配额  
- 所有音频/视频数据在连接关闭后立即销毁，平台不持久化存储——此行为与 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中“数据安全”章节描述一致。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


