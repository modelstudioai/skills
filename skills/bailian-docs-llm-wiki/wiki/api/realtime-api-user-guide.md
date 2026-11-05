# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的实时模型调用接口，适用于语音转写、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向流式通信，支持模型侧持续输出与客户端实时交互。该接口不兼容传统 REST 同步调用模式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime` 和 `qwen-vl-realtime` 为主，后续将扩展更多多模态实时模型）：
- 实时语音识别（ASR）与语义理解一体化
- 音视频流中实时目标检测与事件标注（需配合 `qwen-vl-realtime`）
- 支持上下文感知的流式对话续写（非 session-based，依赖 `conversation_id` 维持逻辑会话）

> **注意**：文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen2.5-realtime` 模型尚未上线，实际可用模型请以控制台「API 能力列表」或 [实时模型连接指南](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中的最新标识为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-audio-realtime`；必须与 [实时模型连接指南](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 所列一致 |
| `conversation_id` | string | 否 | 用于关联同一逻辑会话的多次请求，服务端不自动维护状态，需客户端显式传递并管理 |
| `audio_encoding` / `video_encoding` | string | 条件必填 | 音频流需指定 `pcm`, `wav`, `opus`；视频流需指定 `h264` 或 `h265`；详见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 示例 |
| `sample_rate` | integer | 音频必填 | 单位 Hz，仅当 `audio_encoding=pcm` 时生效，支持 8000、16000、48000 |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Model: <model_id>` 头；
2. **发送初始化帧（Init Frame）**：JSON 格式，包含 `model`、`conversation_id` 等元信息；
3. **流式发送数据帧（Data Frame）**：二进制帧（非 Base64），按 `audio_encoding` 或 `video_encoding` 编码格式分片推送；
4. **接收响应帧（Response Frame）**：服务端以 JSON 帧返回 `event: "text_delta"`、`event: "audio_chunk"` 等类型，客户端需按序拼接。

推荐优先使用 AOQ 客户端 SDK（含重连、心跳、编码适配等封装），详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大持续时长：300 秒（含握手与空闲时间），超时后需重建连接；
- 音频流采样率与编码格式必须严格匹配，否则返回 `400 Bad Encoding` 错误；
- 不支持 `stream=false` 模式；所有响应均为流式，无终止单一 JSON 响应体；
- `conversation_id` 仅作透传字段，服务端不跨连接维护上下文，长期会话需由应用层实现 stateful 管理；
- 实时音频流要求端到端网络抖动 ≤ 80ms，丢包率 < 0.5%，否则可能触发 `event: "network_unstable"` 通知。

> **注意**：[概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提及的“自动 session 恢复”功能在 v1.2.0 版本中已被移除，当前版本无服务端会话状态持久化能力，请勿依赖该行为。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


