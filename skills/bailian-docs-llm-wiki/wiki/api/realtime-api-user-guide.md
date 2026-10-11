# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持请求中动态注入上下文、中断控制和增量式输出。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或遵循指定协议握手。

## 支持的模型与功能

当前 Realtime API 仅支持 `qwen-audio-realtime-v1` 和 `qwen-video-realtime-v1` 两类专用实时模型（详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)）。不支持通用文本模型（如 `qwen-max`）直接接入。功能包括：音频/视频流实时输入与模型响应流式返回、会话级状态保持（如 speaker diarization 上下文）、以及通过 `interrupt` 消息主动终止当前响应。多模态融合能力依赖 AOQ 客户端 SDK 的预处理模块，原始文档中提及的“纯文本实时对话”为过时描述，实际已下线。

> **注意**：[Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“支持任意 Qwen 系列模型”的表述与当前生产环境不符，应以控制台模型列表及 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 文档为准。

## 关键参数

- `model`: 必填，仅接受 `qwen-audio-realtime-v1` 或 `qwen-video-realtime-v1`；
- `input_format`: 指定输入流编码格式（`pcm`, `wav`, `mp4`），需与 `model` 匹配；
- `output_format`: 响应流格式，目前仅支持 `jsonl`（每行一个结构化事件）；
- `max_latency_ms`: 软性延迟上限（单位毫秒），默认 `300`，取值范围 `100–2000`；
- `session_id`: 可选，用于跨请求关联会话状态，若未提供则服务端自动生成。

## 使用方式

1. 通过 WebSocket 连接 `wss://dashscope.aliyuncs.com/realtime/v1/chat`（鉴权使用 `Authorization: Bearer <api_key>`）；  
2. 发送 `init` 握手消息（含 `model`, `input_format` 等参数）；  
3. 持续发送 `audio_chunk` 或 `video_chunk` 二进制帧（按 `input_format` 编码）；  
4. 接收 `response_chunk`、`event`（如 `speech_started`）、`error` 等 JSONL 格式事件。  
完整协议细节与示例见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制和注意事项

- 单次会话最长持续 300 秒，超时后连接自动关闭；  
- 音频流采样率必须为 16kHz，位深 16bit，单通道；视频流分辨率建议 ≤ 720p；  
- 不支持 HTTP/REST 封装调用，所有请求必须走 WebSocket；  
- 错误重试需重建连接，服务端不保留断连前的会话上下文；  
- 流量计费按实际传输字节数（含音频/视频原始帧）计算，非按 token —— 此规则在 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中有明确说明。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


