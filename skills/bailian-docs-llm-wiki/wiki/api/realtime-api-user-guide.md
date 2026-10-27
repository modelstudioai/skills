# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的实时模型调用接口，适用于语音转写、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向流式通信，支持模型侧持续输出与客户端实时交互。该接口不兼容传统 REST 同步调用模式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime` 和 `qwen-vl-realtime` 为主，后续将扩展更多多模态实时模型）：
- 实时语音识别（ASR）与语义理解一体化
- 音视频流中实时目标检测与事件标注（需配合 `qwen-vl-realtime`）
- 流式 TTS 响应合成（仅限 AOQ 客户端 SDK 封装路径）

> **注意**：文档 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen2.5-realtime` 模型尚未上线，实际可用模型请以控制台「API 能力列表」或 [实时模型接入说明](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime`；必须与 [实时模型接入说明](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中公布的模型列表一致 |
| `stream` | boolean | 是 | 固定为 `true`，Realtime API 不支持非流式调用 |
| `audio_format` / `video_format` | string | 条件必填 | 根据输入流类型指定，如 `pcm-16k-1ch`、`h264-30fps`；详见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 的编解码要求 |
| `max_duration_sec` | integer | 否 | 单次会话最大时长（秒），默认 300，上限 1800 |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 头（部分 SDK 自动注入）  
2. **发送初始化帧（Init Frame）**：包含 `model`、`stream` 及媒体格式参数的 JSON 对象  
3. **持续发送媒体数据帧（Data Frame）**：二进制分块（如 PCM 音频 chunk），每帧需带 `seq` 序号与 `timestamp_ms`  
4. **接收响应帧（Response Frame）**：服务端按流式返回 `text_delta`、`event`（如 `speech_start`）、`audio_chunk` 等结构化 payload  

推荐优先使用 AOQ 客户端 SDK（封装了重连、心跳、帧序列管理等细节），其使用方法详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大并发请求数：1（Realtime API 会话为独占式长连接）  
- 音频采样率必须严格匹配所选模型要求（如 `qwen-audio-realtime` 仅支持 16kHz 单声道 PCM）；不匹配将导致 `400 Bad Request`  
- 连接空闲超时为 60 秒（无任何帧收发），超时后服务端主动关闭连接  
- 错误码统一遵循 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 定义的 `error.code` 字段，但部分旧版 SDK 可能映射不全，建议以服务端返回的原始 `error.message` 为准  
- 日志调试强烈建议启用客户端 SDK 的 `debug: true` 模式，并参考 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的典型时序图定位卡顿点

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


