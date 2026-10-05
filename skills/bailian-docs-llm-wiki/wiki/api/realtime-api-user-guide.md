# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持音频输入、文本输入、多模态上下文维护及结构化输出控制。该接口不兼容传统 REST 同步调用模式，需按长连接生命周期管理请求流程。

## 支持的模型与功能

当前 Realtime API 仅支持以下模型：
- `qwen-audio-realtime-v1`（音频流实时转写与理解）
- `qwen2.5-7b-instruct-realtime-v1`（文本流式推理，支持工具调用与 function calling）
- `qwen-vl-realtime-v1`（图像+文本混合输入的实时多模态理解）

> **注意**：文档 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中列出的 `qwen-14b-realtime-beta` 已于 v2024.09.15 版本下线，实际调用将返回 `model_not_found` 错误，请以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的模型列表为准。

功能包括：音频流分块上传与实时响应、文本增量输入、会话状态保持（`session_id`）、中断恢复（`interrupt` 指令）、工具调用（`tool_choice` + `tools`）、以及结构化输出约束（`response_format`）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为上述支持列表中的值 |
| `session_id` | string | 否 | 用于关联同一会话的多次请求；未提供时服务端自动生成 |
| `audio_encoding` | string | 否（音频场景必填） | `pcm16` / `opus`，需与实际音频编码一致 |
| `sample_rate` | integer | 否（音频场景必填） | 音频采样率，如 `16000` |
| `response_format` | object | 否 | 指定输出 JSON Schema，详见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) |

所有参数均通过 WebSocket 连接建立时的 `init` 消息 payload 传递，不可在会话中动态修改。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/chat?apiKey=<your_api_key>`  
2. 发送 `init` 消息（含 `model`、`session_id` 等初始化参数）  
3. 按需发送 `input` 消息（`audio_chunk` 或 `text` 类型）  
4. 接收 `output` 流式事件（含 `delta`、`finish_reason`、`tool_calls` 等字段）  
5. 主动发送 `close` 消息或等待超时自动断连  

完整交互示例见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)，该 SDK 封装了重连、心跳、chunk 分片、buffer 合并等底层逻辑，推荐生产环境直接使用。

## 限制和注意事项

- 单次会话最大时长：300 秒（含静默期），超时后连接强制关闭  
- 音频流单 chunk 大小上限：64 KB；文本单次 `input` 长度上限：8192 字符  
- 不支持跨 session 复用 `session_id`；重复使用旧 `session_id` 将触发新会话创建  
- `interrupt` 指令仅终止当前响应生成，不回滚已发送的 `input`  
- 所有音频数据必须为原始 PCM（LE）或 Opus 编码，**不支持 MP3/WAV 容器封装** —— 此限制在 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中明确说明，但 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 的示例代码未做格式校验，开发者需自行确保编码合规。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


