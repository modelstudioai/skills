# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与实时控制指令（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或遵循指定协议握手。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime`、`qwen-vl-realtime` 和 `qwen2.5-7b-realtime` 为代表），均针对流式输入/输出优化，具备音频流接入、多模态上下文维持、实时语音转写与合成联动能力。所有模型均要求启用 `stream=true` 并配合 `input_format` 显式声明输入类型（如 `"audio/wav"`、`"text/plain"`）。详细模型列表及能力说明见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的子页面 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md)。

> **注意**：文档中提及的 `qwen1.5-72b-realtime` 已于 v2024.09 版本下线，实际可用模型请以控制台「API 能力中心」实时列表为准；旧文档 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中的该条目尚未更新，需以平台实际返回的 `model_list` 接口响应为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime`，必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 所列支持模型一致 |
| `stream` | boolean | 是 | 必须为 `true`，Realtime API 不支持非流式调用 |
| `input_format` | string | 是（音频/视频场景） | 输入数据编码格式，如 `"audio/wav"`、`"video/mp4"`；纯文本可省略或设为 `"text/plain"` |
| `output_format` | string | 否 | 输出音频格式（仅当启用 TTS 时生效），默认 `"audio/pcm"`，支持 `"audio/mp3"` |
| `max_tokens` | integer | 否 | 单次响应最大生成 token 数，默认 1024，硬上限 4096 |

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 与 `X-DashScope-Model: <model>` 头；
2. **发送初始化帧（Init Frame）**：JSON 格式，包含 `model`、`stream`、`input_format` 等参数，详见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)；
3. **逐帧发送输入数据**（如音频 chunk）并接收增量响应帧（Delta Frame）；
4. 客户端应监听 `event: end` 或 `event: error` 帧以完成会话清理。

推荐优先使用官方 AOQ 客户端 SDK（支持 Python/JS/Android/iOS），其已封装连接管理、帧序列化与重连逻辑；SDK 使用说明见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 限制和注意事项

- 单连接最长存活时间 300 秒（含握手与空闲），超时后服务端将主动关闭连接；
- 音频输入采样率必须为 16kHz，位深 16bit，单通道（mono），否则触发 `invalid_input_format` 错误；
- 不支持 `system` 消息字段，角色设定需通过 `user` / `assistant` 显式消息流控制；
- 若在 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中提到的“自动上下文压缩”功能未生效，请确认是否启用了 `enable_context_compression=true` 参数——该参数在 v2024.08 后已废弃，实际由服务端动态决策，客户端传入将被忽略。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


