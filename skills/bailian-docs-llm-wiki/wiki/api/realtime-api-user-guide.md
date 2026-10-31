# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与实时中断控制。该接口不兼容传统 RESTful 同步调用模式，需按流式协议设计客户端逻辑。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime`、`qwen-vl-realtime` 和 `qwen2.5-7b-instruct-realtime` 为代表），均专为实时流式推理优化，具备音频/视频输入解析、上下文动态裁剪、[流式输出](../concepts/streaming-output.md) token 及事件驱动中断能力。所有可用模型列表及能力说明详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节。  
> **注意**：文档中提及的 `qwen1.5-7b-realtime` 已于 v2024.09 版本下线，实际可用模型请以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的 `model_id` 示例为准，避免使用已废弃标识符。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen2.5-7b-instruct-realtime`；必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中“接入模型与应用”章节所列一致 |
| `stream` | boolean | 是 | 固定为 `true`，Realtime API 不支持非流式调用 |
| `enable_interruption` | boolean | 否 | 默认 `false`；启用后允许客户端发送 `interrupt` 事件中止当前响应流 |
| `max_output_tokens` | integer | 否 | 最大生成 token 数，硬限制（含系统提示），默认 1024，不可超过 2048 |

## 使用方式

1. 建立 WebSocket 连接：请求地址为 `wss://dashscope.aliyuncs.com/realtime/v1/chat`，需携带 `Authorization: Bearer <api_key>` 头（通过 query 参数 `x-dashscope-token` 传递亦可）；  
2. 发送初始化消息（`session.update`），包含 `model_id`、`temperature` 等配置；  
3. 发送用户输入（`input.audio` 或 `input.text`），支持分片上传音频流；  
4. 接收服务端 `output.delta`、`output.end`、`event.interrupted` 等事件。完整协议格式与示例见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最大持续时长为 300 秒，超时后连接自动关闭；  
- 音频输入仅支持 PCM 编码（16-bit, 16kHz, mono），且单次 `input.audio` 分片不得超过 64KB；  
- 不支持 `system` 角色消息，系统指令需通过 `session.update` 的 `instructions` 字段传入；  
- 若在 `output.delta` 流中收到 `reason: "rate_limit_exceeded"`，表明当前账号 QPS 超限，需退避重试；该行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中描述一致，但错误码细节以实际响应为准。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


