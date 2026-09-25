# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的实时模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端延迟敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 流式返回与客户端主动控制（如中断、暂停）。该接口不兼容传统 RESTful 同步调用模式，需使用专用 SDK 或原生 WebSocket 客户端接入。

## 支持的模型与功能

当前 Realtime API 支持以下模型（截至 2024 Q3）：
- `qwen-audio-realtime-v1`（音频流实时 ASR + LLM 推理）
- `qwen-video-realtime-v1`（视频帧流+音频流联合理解与生成）
- `qwen-text-realtime-v1`（纯文本流式对话，支持 system/user/assistant 角色切换）

所有模型均支持 **[流式输出](../concepts/streaming-output.md)（delta tokens）**、**客户端中断（`interrupt` event）**、**会话状态保持（`session_id` 复用）** 和 **自定义工具调用（function calling）**。详细能力说明见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档中的 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 章节。

> **注意**：文档中提及的 `qwen-realtime-v0` 模型已下线，实际可用模型列表以 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中的 `model` 参数示例为准，旧版 SDK 示例代码若引用该模型名将返回 `400 Bad Request`。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 所列一致 |
| `session_id` | string | 否 | 用于恢复上下文的会话 ID；首次调用可不传，服务端将生成并返回 |
| `temperature` | float | 否 | 采样温度（0.0–2.0），默认 `0.7`；仅对 `qwen-text-realtime-v1` 生效 |
| `max_output_tokens` | integer | 否 | 最大生成 token 数，范围 `1–8192`；超出将触发 `stop` 事件 |

所有参数需在 WebSocket 连接建立后的 `init` 消息中以 JSON 格式发送。参数校验失败时服务端立即关闭连接，不返回 HTTP 状态码。

## 使用方式

1. **建立 WebSocket 连接**：  
   URL 格式为 `wss://dashscope.aliyuncs.com/realtime/v1/chat?apiKey=<your_api_key>`（注意：`apiKey` 为查询参数，非 header）  
2. **发送 `init` 消息**：包含 `model`、`session_id` 等初始化参数（参考 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 的 `initRequest` 结构）  
3. **发送 `input` 消息**：按类型提交数据（如音频 base64 分片、文本 message 对象）  
4. **接收 `output` 流**：服务端逐帧推送 `delta` 字段，客户端需自行拼接完整响应  

推荐直接使用官方 AOQ SDK（v2.3.0+），其自动处理重连、分片、心跳与错误恢复。原始 WebSocket 协议细节详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 部分。

## 限制和注意事项

- 单连接最大持续时间：**300 秒**（含握手与空闲期），超时后服务端强制关闭  
- 音频流输入要求：采样率 16kHz、单声道、PCM 编码（`int16`），每帧 ≤ 200ms 数据  
- 并发连接数限制：免费版 ≤ 5 路，企业版按配额配置（见控制台「API 配额」页）  
- 不支持跨区域调用：WebSocket endpoint 必须与 API Key 所属地域一致（如华东 1 的 Key 只能访问 `wss://dashscope.aliyuncs.com/...`，不可用 `dashscope-intl.aliyuncs.com`）  

> **注意**：[快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中给出的 Python 示例使用了已废弃的 `websocket-client` 库手动管理连接，存在心跳丢失风险；请优先采用 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 提供的 `RealtimeClient` 类。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


