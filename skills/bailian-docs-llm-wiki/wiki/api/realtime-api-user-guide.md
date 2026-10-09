# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式集成。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime-v1`、`qwen-video-realtime-v1` 和 `qwen2.5-7b-instruct-realtime` 为代表），具体可用模型列表请参考 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档首页的模型索引表。  
支持的核心功能包括：  
- 音频/视频流实时输入与模型侧流式响应（`audio_input` / `video_input` 字段）  
- 客户端发起的 `interrupt` 事件以终止当前推理  
- 响应中携带 `timestamp` 与 `audio_chunk_id` 用于端侧同步对齐  
- 多轮上下文保持（需显式传入 `session_id` 并复用同一连接）

> **注意**：文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中提及的 `qwen1.5-4b-realtime` 已于 v2024.09 版本下线，实际可用模型请以控制台「API 调用」页的实时模型列表为准，避免依赖过时文档中的示例模型名。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“接入模型与应用”章节所列一致 |
| `session_id` | string | 否（推荐） | 用于跨请求维持会话状态；若未提供，服务端将生成临时 session，但不保证上下文延续性 |
| `stream` | boolean | 是 | 固定为 `true`；Realtime API 不支持非流式模式 |
| `input_format` | string | 是 | 取值为 `"pcm"`、`"wav"` 或 `"mp4"`，需与实际二进制数据格式严格匹配 |

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/chat?apiKey=<YOUR_API_KEY>`  
2. 发送 `init` 事件（含 `model`、`session_id` 等初始化参数）  
3. 分帧发送 `audio_input` 或 `video_input` 事件（每帧 ≤ 200ms 音频或 1s 视频）  
4. 监听 `response.text_delta`、`response.audio_output` 等事件进行消费  
详细流程与事件定义见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 和 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 两节。

## 限制和注意事项

- 单连接最大持续时长：10 分钟（超时后连接自动关闭，需重连并传入原 `session_id` 续接）  
- 音频采样率仅支持 16kHz（PCM/WAV）或 48kHz（MP4 封装内音频轨道），不支持自动重采样  
- 每秒最多发送 10 帧输入事件；超出将触发 `rate_limit_exceeded` 错误  
- `session_id` 若在 30 分钟内无新事件，服务端将自动清理上下文 —— 此行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中描述一致，但不同于旧版文档中“长期保活”的说明，请以本条为准

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


