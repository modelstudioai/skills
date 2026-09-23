# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式双向通信接口，适用于语音交互、实时对话、音视频辅助理解等场景。它基于 WebSocket 协议，支持模型推理过程中的增量响应与用户中断重置。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或标准 WebSocket 库接入。

## 支持的模型与功能

当前 Realtime API 仅支持以下模型：
- `qwen-audio-realtime-v1`（音频流式输入/输出）
- `qwen-vl-realtime-v1`（多模态流式理解，支持图像帧+文本混合输入）

不支持 `qwen-max`、`qwen-plus` 等通用大模型的实时流式调用。所有模型均要求启用 `enable_input_streaming: true` 且必须通过 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 或原生 WebSocket 实现连接。功能上支持：语音转文本（ASR）、文本转语音（TTS）、上下文感知的流式 LLM 推理、用户语音打断（`interrupt` event）及会话状态同步。

> **注意**：[快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中示例使用的 `qwen-realtime-v1` 模型别名已废弃，实际应使用 `qwen-audio-realtime-v1`；请以 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 文档中最新模型列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-audio-realtime-v1` |
| `audio_format` | string | 否 | 音频编码格式，支持 `pcm16`（默认）、`opus`；需与客户端采样率一致 |
| `sample_rate` | integer | 否 | 音频采样率，`qwen-audio-realtime-v1` 仅支持 `16000` |
| `max_output_tokens` | integer | 否 | 单次响应最大 token 数，范围 1–2048，默认 1024 |
| `temperature` | float | 否 | 0.0–1.0，默认 0.7；注意该参数在流式 TTS 阶段被忽略 |

所有参数需在 WebSocket 连接建立时通过 `init` message 发送。详见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的协议帧结构定义。

## 使用方式

1. 建立 WebSocket 连接：  
   `wss://dashscope.aliyuncs.com/realtime/v1/<model>`（需携带 `Authorization: Bearer <api_key>` header）

2. 发送 `init` 消息初始化会话（含上述关键参数及 `session_id`）

3. 持续发送 `input` 消息（音频 chunk 或文本），接收 `output` 流式事件（含 `text_delta`, `audio_delta`, `final_text` 等字段）

4. 主动发送 `end_session` 或服务端超时（默认 300 秒无活动）将终止连接

推荐优先使用 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)，其已封装重连、心跳、音频 buffer 管理与事件分发逻辑。

## 限制和注意事项

- 单连接最大持续时间：300 秒（可配置，但不超过 600 秒）
- 音频流输入速率需稳定，瞬时丢包率 >5% 可能导致 ASR 质量显著下降
- 不支持跨连接复用 `session_id`；每个新会话必须新建 WebSocket 连接
- `system` 消息仅在 `init` 时允许设置一次，后续无法动态更新
- 错误码 `429 Too Many Requests` 表示并发连接数超限（默认配额为 10 个并发连接/项目）

> **注意**：[快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中提到的“自动 session 复用”功能尚未上线，当前所有会话均为独立生命周期，请勿依赖历史 `session_id`。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


