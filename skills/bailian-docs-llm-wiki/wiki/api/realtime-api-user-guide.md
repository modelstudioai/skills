# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于对话交互、实时语音/文本生成等场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与事件驱动控制。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或 WebSocket 库接入。

## 支持的模型与功能

- 当前支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分 AOQ（Adaptive Output Quantization）优化模型，具体以 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中“支持的模型列表”章节为准。  
- 功能包括：流式文本生成、工具调用（function calling）、多轮上下文维护、中断/暂停/恢复控制、音频输入（ASR）与输出（TTS）集成（需启用对应能力）。  
- AOQ 模型需通过 `model` 参数显式指定（如 `qwen-plus-aoq`），其行为与标准版本存在差异，详见 [AOQ客户端SDK](https://help.aliyun.com/zh/model-studio/realtime-api-aoq-api) —— 该文档实际已整合进 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的“客户端 SDK”附录中，原独立链接内容已过时。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-turbo`；AOQ 模型需带 `-aoq` 后缀 |
| `messages` | array | 是 | 对话历史，格式同 Chat Completion，但 `role: "system"` 仅在首条消息生效 |
| `stream` | boolean | 否，但建议设为 `true` | 必须为 `true` 才启用流式响应；设为 `false` 将返回错误 |
| `tools` | array | 否 | 工具定义列表，启用 function calling 时必需 |
| `tool_choice` | string / object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定工具 |
| `max_tokens` | integer | 否 | 响应最大 token 数，硬性截断阈值 |

> **注意**：`temperature` 和 `top_p` 在 Realtime API 中**不生效**，模型输出确定性由服务端统一调控——这与 [概述](https://help.aliyun.com/zh/model-studio/realtime-api-overview) 中早期示例存在矛盾，以 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的“参数说明”节为准。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 头（通过 query 参数传递不被支持）。  
2. **发送初始化帧**：以 JSON 格式发送 `{"type": "session.update", "turn_id": "...", ...}` 或直接发送 `{"type": "conversation.item.create", ...}`。  
3. **接收事件流**：服务端按事件类型（`response.text.delta`、`response.function_call_arguments.delta`、`response.audio.delta` 等）分帧推送，客户端需按序拼接。  
4. **终止会话**：发送 `{"type": "response.cancel"}` 或关闭连接；主动关闭前建议发送 `{"type": "session.end"}` 释放资源。  
完整交互流程见 [快速开始](https://help.aliyun.com/zh/model-studio/realtime-api-quick-start-guide)，但其中 Python 示例依赖旧版 `dashscope` SDK v1.x，推荐改用 v2.0+ 并参考 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的代码片段。

## 限制和注意事项

- 单次会话最长持续 300 秒，超时自动断连；`max_tokens` 超限将触发 `response.done` 事件并终止。  
- 每个连接仅支持一个并发请求（即不支持 multiplexing），需为每轮对话新建连接。  
- 音频流（ASR/TTS）需额外申请权限，并在 `input_audio_format` / `output_audio_format` 中声明编码格式（如 `pcm16`）。  
- 错误码统一为 WebSocket 状态码 + 自定义 `error.code` 字段（如 `InvalidParameter`、`RateLimitExceeded`），需解析 payload 中的 `error` 对象而非仅依赖 HTTP 状态。  
- 日志与 trace ID 仅在 `response.done` 事件中返回，调试时请确保捕获该帧。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


