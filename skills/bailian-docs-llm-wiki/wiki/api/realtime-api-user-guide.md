# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时翻译、多轮对话等需要毫秒级响应的场景。它基于 WebSocket 协议，支持服务端主动推送与客户端事件驱动交互。该接口不兼容传统 REST 请求方式，需使用专用 SDK 或遵循特定握手与消息格式。

## 支持的模型与功能

当前 Realtime API 仅支持 `qwen-audio-realtime-v1` 和 `qwen-video-realtime-v1` 两类实时感知模型（详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)）。不支持文本大模型（如 qwen-max）的实时调用；若需文本流式响应，请使用 [Streaming API](../../raw/model-api-reference/streaming-api-user-guide.md)。  
> **注意**：原始文档中提及的 `qwen-realtime-v1`（见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)）已下线，实际可用模型以控制台「API 能力列表」或 [实时模型接入说明](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 为准。

## 关键参数

- `model`: 必填，取值为 `qwen-audio-realtime-v1` 或 `qwen-video-realtime-v1`  
- `temperature`: 可选，范围 `[0.0, 1.0]`，默认 `0.7`；低于 `0.3` 可能导致响应僵化（参见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)）  
- `max_input_duration`: 音频输入最大时长（秒），默认 `30`，上限 `60`  
- `enable_interim_results`: 布尔值，启用中间结果（如语音识别过程中的部分文本），默认 `false`

## 使用方式

1. 通过 `POST /v1/realtime/session` 获取 WebSocket 连接地址（含鉴权 token）  
2. 建立 WebSocket 连接，发送 `session.update` 消息初始化会话配置  
3. 按需发送 `input.audio`、`input.text` 或 `input.video` 事件；服务端通过 `output.*` 事件实时返回结果  
4. 推荐使用官方 AOQ 客户端 SDK（含重连、心跳、buffer 管理），避免手动实现连接逻辑 —— 具体用法见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)

## 限制和注意事项

- 单会话最长持续 10 分钟，超时后需新建 session  
- 音频采样率必须为 `16kHz`，单声道，PCM 编码（`int16`）；视频需为 `H.264` 编码、`30fps`、分辨率 ≤ `1280×720`  
- 不支持跨 session 的上下文继承；如需长程记忆，请在应用层维护 state 并通过 `input.text` 显式注入  
- 错误码 `429` 表示并发连接数超限（默认配额 5 个活跃 session），可通过工单申请提升 —— 配额策略详见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


