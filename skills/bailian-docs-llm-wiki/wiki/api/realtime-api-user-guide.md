# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需使用专用 SDK 或遵循协议规范手动实现连接。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime`、`qwen-vl-realtime` 和 `qwen2.5-7b-instruct-realtime` 为代表），均针对流式输入/输出优化。功能包括：  
- 实时音频流输入（PCM/WAV，采样率 16kHz，单通道）与文本/音频混合响应；  
- 多轮上下文维持（通过 `session_id` 绑定）；  
- 客户端主动发送 `interrupt`、`pause`、`resume` 控制指令；  
- 支持语义级中断（非仅 TCP 中断），详见 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md)。  

> **注意**：文档 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的 `qwen-audio-realtime` 模型在 v2.3.0 版本后已更名为 `qwen-audio-2-realtime`，旧名称将返回 404；请以 [快速开始](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的模型列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-2-realtime`；必须与实际部署版本匹配 |
| `session_id` | string | 否 | 用于跨请求维持会话状态；若未提供，服务端自动生成新会话 |
| `audio_format` | string | 否 | 音频编码格式，可选 `pcm`（默认）、`wav`；`wav` 需含合法 RIFF 头 |
| `max_output_tokens` | integer | 否 | 响应最大 token 数，范围 1–2048；超限将触发 `stop` 事件 |
| `temperature` | float | 否 | 采样温度，范围 0.0–2.0，默认 0.7 |

完整参数定义见 [接入模型与应用](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md)。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Model: <model>` 请求头；  
2. **发送初始化消息**：首帧为 JSON 格式的 `init` 消息，包含 `model`、`session_id` 等参数；  
3. **流式发送数据**：后续帧可为 `audio`（二进制 PCM 数据）、`text`（JSON 文本输入）或 `control`（如 `{ "type": "interrupt" }`）；  
4. **接收响应**：服务端按 `event` 类型返回 `response.start`、`token`、`response.stop` 等事件；参考 [AOQ客户端SDK](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 的事件解析逻辑。

## 限制和注意事项

- 单连接最长存活时间 300 秒，超时后需重连并重建会话；  
- 音频流要求严格：PCM 必须为小端、16-bit、单声道，无 header；WAV 必须含标准 `fmt` 和 `data` chunk；  
- 不支持 HTTP/REST 调用方式，[概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 明确指出“仅限 WebSocket”；  
- 错误码统一返回 `4xxx`（客户端错误）或 `5xxx`（服务端错误），具体含义需对照 [Realtime API (raw/model-api-reference/realtime-api-user-guide.md)](../../raw/model-api-reference/realtime-api-user-guide.md) 的错误码表；  
- 多路并发连接数受 API Key 配额限制，超出将返回 `429 Too Many Requests`。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


