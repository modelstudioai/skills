# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式集成。

## 支持的模型与功能

当前 Realtime API 支持以下模型（截至 2024 Q3）：
- `qwen-audio-realtime-v1`（音频流实时 ASR + LLM 推理）
- `qwen-video-realtime-v1`（视频帧流 + 音频流联合理解）
- `qwen-chat-realtime-v1`（纯文本流式对话，支持工具调用）

所有模型均支持 **[流式输出](../concepts/streaming.md)**、**客户端中断（`/interrupt` 事件）**、**会话状态保持（`session_id` 复用）** 和 **自定义 system [prompt](../guides/prompt.md) 注入**。详细能力矩阵见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的子页面说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 必须为上述支持模型之一，例如 `"qwen-audio-realtime-v1"` |
| `session_id` | string | 否 | 用于恢复上下文；若为空则新建会话；[快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中有生成示例 |
| `audio_encoding` / `video_encoding` | string | 条件必填 | 音频流需指定 `"pcm"` 或 `"opus"`；视频流需指定 `"h264"`；详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) |
| `sample_rate` | integer | 条件必填 | 音频流必须提供采样率（如 `16000`），否则连接被拒绝 |

> **注意**：文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `max_tokens` 参数在 v1.2+ 版本已弃用，实际由服务端动态管理；请勿在请求中设置，否则将触发 400 错误。

## 使用方式

1. 建立 WebSocket 连接：  
   `wss://dashscope.aliyuncs.com/realtime/v1/{model}`，携带 `Authorization: Bearer <api_key>` 与 `X-DashScope-SSE: enable`（启用 Server-Sent Events 兼容模式可选）。

2. 发送初始化事件（`session.update`）配置 system [prompt](../guides/prompt.md) 与媒体参数。

3. 按需发送 `input.audio` / `input.video` / `input.text` 事件流。

4. 监听 `output.*` 事件（如 `output.text.delta`、`output.audio.chunk`）并消费流式响应。

完整握手与事件序列示例参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)，该 SDK 封装了重连、心跳、事件序列校验等底层逻辑。

## 限制与注意事项

- 单次会话最大持续时间：**300 秒**（含静默期）；超时后连接自动关闭，需重建 session。
- 音频流输入要求：单帧 ≤ 64KB，采样率必须与 `sample_rate` 严格一致，否则触发 `input.error` 事件。
- 不支持跨模型切换：一个 WebSocket 连接绑定唯一 `model`，不可在会话中变更。
- 所有 Realtime API 调用计入百炼平台的「实时推理」配额，不占用通用 `chat/completions` 配额。

> **注意**：[概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提及的“支持 HTTP/2 双向流”为历史草案描述，**当前仅支持 WebSocket**；HTTP/2 支持计划于 2025 Q1 发布，届时将同步更新此文档。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


