# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时对话、多轮上下文协同等场景。它基于 WebSocket 协议，支持模型推理过程中的 token 级别流式返回与客户端指令实时注入（如中断、暂停、工具调用）。该 API 不同于标准 REST 推理接口，需维持长连接并遵循特定帧协议。

## 支持的模型与功能

当前 Realtime API 仅支持以下模型：`qwen-audio-realtime-v1`（语音输入/输出）、`qwen2.5-7b-instruct-realtime-v1`（文本交互），后续将逐步扩展至更多实时优化模型。核心功能包括：
- 实时音频流输入（PCM/WAV）与合成语音流输出（ulaw/alaw）
- 多轮会话状态自动维护（含 `session_id` 生命周期管理）
- 客户端主动发送 `input_interrupt`、`tool_use_request` 等控制帧
- 模型侧触发 `tool_call` 后支持同步/异步工具执行反馈

> **注意**：文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen-vl-realtime-beta` 已于 v2.3.0 版本下线，实际可用模型请以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的 `model_list` 响应为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中注册的模型一致 |
| `temperature` | float | 否 | 采样温度，默认 `0.7`，取值范围 `[0.0, 2.0]` |
| `max_output_tokens` | int | 否 | 单次响应最大 token 数，硬上限 `4096` |
| `enable_audio` | boolean | 否 | 是否启用音频编解码（仅对音频模型有效），默认 `false` |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Model: <model>` 头；
2. **发送初始化帧**：首帧为 JSON 格式 `{"type": "session.update", "session": {...}}`，其中 `session` 字段需包含 `turn_id`、`user_id` 等元信息；
3. **交互循环**：后续按帧发送 `input.audio`、`input.text` 或 `input.tool_result`；接收 `output.text.delta`、`output.audio.chunk` 等流式响应；
4. **终止会话**：发送 `{"type": "session.end"}` 帧，服务端将关闭连接并释放资源。

推荐使用官方 AOQ 客户端 SDK（Python/JS）封装连接管理与帧序列化逻辑，详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最长存活时间 30 分钟，超时后需重连并新建 `session_id`；
- 音频流输入需严格满足采样率 16kHz、单声道、16-bit PCM 格式，否则将触发 `input_format_error` 错误；
- 同一 `session_id` 不支持跨连接复用，重复使用将导致 `session_conflict`；
- 工具调用（`tool_use`）仅支持预注册函数，未在 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中配置的工具将被静默忽略。

> **注意**：[概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提及的“自动重连机制”尚未在 v2.4.0 生产环境启用，当前需由客户端自行实现断线重连与会话恢复逻辑。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


