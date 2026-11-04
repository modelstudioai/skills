# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、多轮上下文感知等场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与事件驱动控制。开发者需通过认证密钥接入，并遵循特定的消息格式与生命周期管理规范。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `model_id` 形式指定）：  
- `qwen-audio-realtime-v1`（音频流式输入/输出）  
- `qwen2.5-7b-instruct-realtime`（文本流式生成，支持工具调用与 function calling）  
- `qwen-vl-realtime-v1`（多模态流式理解，支持图像+文本混合输入）  

所有模型均支持 `input_streaming`（客户端持续推送输入）、`output_streaming`（服务端逐 token 推送响应）、`interrupt`（运行时中断）及 `stateful_session`（跨请求保持会话状态）。详细能力说明见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型标识符，必须为上述支持列表中的值 |
| `stream` | boolean | 是 | 固定为 `true`，不支持非流式模式 |
| `max_tokens` | integer | 否 | 响应最大 token 数，默认 2048，上限 4096 |
| `temperature` | number ∈ [0,2] | 否 | 默认 0.8；设为 0 时启用 determinstic 模式 |
| `enable_function_calling` | boolean | 否 | 仅对支持工具调用的模型生效；启用后需在 `tools` 字段声明函数 schema |

> **注意**：`top_p` 参数在 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中被标记为“已弃用”，但部分旧版 SDK 示例仍包含该字段；请以最新 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 文档为准，忽略 `top_p`。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起带 `Authorization: Bearer <api_key>` 的连接；  
2. **发送初始化消息（`session.update`）**：携带 `model_id`、`stream` 及其他配置；  
3. **发送用户输入（`input.audio` 或 `input.text`）**：按 chunk 分片发送，每帧需带 `sequence_id` 和时间戳；  
4. **接收服务端事件**：包括 `output.text.delta`、`output.audio.chunk`、`tool_calls`、`session.end` 等；  
5. **主动控制**：通过 `input.interrupt` 消息中止当前响应流。  

完整交互流程与消息结构详见 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md)。

## 限制和注意事项

- 单连接最长存活时间：300 秒（含握手与空闲期），超时将触发 `session.expired` 事件；  
- 音频输入采样率必须为 16kHz，PCM 编码，单通道；文本输入单次 `input.text` 消息长度 ≤ 8192 Unicode 字符；  
- 不支持跨连接共享 `session_id`；每个 WebSocket 连接对应独立会话上下文；  
- 错误码 `429 Too Many Requests` 表示 QPS 超限，需检查配额或添加退避重试逻辑；  
- AOQ 客户端 SDK 提供了自动重连、序列号校验与 buffer 管理，推荐优先使用 —— 具体集成方式参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


