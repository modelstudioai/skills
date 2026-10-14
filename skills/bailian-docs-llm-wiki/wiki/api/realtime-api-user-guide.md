# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式集成。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime-v1`、`qwen-video-realtime-v1` 和 `qwen2.5-7b-instruct-realtime` 为代表），具体可用模型列表请参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档首页的模型索引表。  
支持的核心功能包括：  
- 音频/视频流实时输入与模型侧流式响应（text/audio）  
- 客户端发起的 `interrupt`、`pause`、`resume` 控制指令  
- 多模态上下文保持（如语音+文本混合输入）  
- 基于 AOQ 协议的端到端 QoS 保障（详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)）

> **注意**：文档中提及的 `qwen1.5-72b-realtime` 已于 v2024.09 版本下线，实际可用模型请以控制台「API 调用」页的实时下拉列表为准，避免依赖过时文档中的示例模型名。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为 Realtime 系列模型（如 `qwen-audio-realtime-v1`）；非 Realtime 模型将返回 400 错误 |
| `input` | object | 是 | 包含 `audio` 或 `video` 字段的流式输入对象，格式详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中的输入规范 |
| `stream` | boolean | 否（默认 `true`） | 强制设为 `true`；`false` 将被忽略并静默转为流式 |
| `max_tokens` | integer | 否 | 单次会话最大生成 token 数，上限 8192；超出后连接自动关闭 |

## 使用方式

1. **建立 WebSocket 连接**：使用 `wss://dashscope.aliyuncs.com/realtime/v1/chat`（生产环境）或沙箱地址，携带 `Authorization: Bearer <api_key>` 头；
2. **发送初始化消息**：包含 `model`、`input` 及可选配置，参考 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的握手示例；
3. **处理双向事件**：监听 `response.text.delta`（流式文本）、`response.audio.chunk`（PCM 音频帧）、`error` 等事件类型；
4. **主动控制会话**：通过发送 `{"type": "interrupt"}` 等控制消息实现交互干预。

## 限制和注意事项

- 单连接最长存活时间：60 秒（含握手与空闲期），超时后服务端强制关闭；
- 音频输入采样率必须为 16kHz，单通道，PCM 编码（未压缩）；视频输入仅支持 H.264 Annex B 格式裸流；
- 不支持 HTTP/REST fallback，所有请求必须走 WebSocket；
- 流式响应中 `response.text.final` 事件仅在会话结束时触发一次，不可用于中间状态判断；
- 若发现 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 中描述的“多轮 session_id 复用”与当前 SDK 行为不一致（如 SDK 强制每次新建 session），请以 SDK 实现为准——该文档尚未同步更新。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


