# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式集成。

## 支持的模型与功能

当前 Realtime API 支持以下模型（截至 2024 Q3）：
- `qwen-audio-realtime-v1`（音频流实时 ASR + LLM 推理）
- `qwen-video-realtime-v1`（视频帧流 + 音频流联合理解）
- `qwen-chat-realtime-v1`（纯文本流式对话，支持工具调用）

所有模型均支持 **[流式输出](../concepts/streaming-output.md)**、**客户端中断（`/interrupt` 事件）**、**会话状态保持（`session_id` 复用）** 和 **自定义 system prompt 注入**。详细能力说明见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中的“接入模型与应用”章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为上述支持列表中的值 |
| `session_id` | string | 否 | 用于跨请求维持上下文；若未提供，服务端将自动生成新会话 |
| `audio_encoding` / `video_encoding` | string | 条件必填 | 音频/视频流编码格式（如 `pcm-f32le`, `h264-annexb`），详见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) |
| `sample_rate` | integer | 条件必填 | 音频采样率（Hz），仅当传音频时必需 |
| `max_output_tokens` | integer | 否 | 输出长度上限，默认 2048，最大 4096 |

> **注意**：`temperature` 和 `top_p` 等采样参数在 Realtime API 中**不生效**——模型内部采用固定解码策略以保障实时性，此行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中描述一致，但与部分旧版 REST API 文档存在表述冲突，请以本 Realtime API 文档为准。

## 使用方式

1. 建立 WebSocket 连接：  
   `wss://dashscope.aliyuncs.com/realtime/v1/{model}`（需携带 `Authorization: Bearer <api_key>` header）

2. 发送初始化消息（JSON）：  
   ```json
   { "type": "session.update", "session": { "model": "qwen-audio-realtime-v1", "session_id": "sess_abc123" } }
   ```

3. 流式发送数据帧（二进制或 base64 编码）并监听 `response.text.delta` 或 `response.audio.delta` 事件。完整协议规范和示例见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单次会话最长持续 **300 秒**（含静默期），超时后连接自动关闭；
- 音频流要求 **单通道、16kHz 采样率、PCM 小端浮点（f32le）**，不支持 MP3/WAV 封装；
- 不支持 `stream=false` 模式；所有响应均为分块流式；
- 若需调试连接行为，建议优先使用 AOQ SDK 内置日志，而非自行封装 WebSocket——SDK 已处理重连、心跳、帧序号校验等底层细节，参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


