# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与实时控制指令（如中断、暂停）。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或遵循指定协议握手。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime`、`qwen-vl-realtime` 和 `qwen2.5-7b-realtime` 为代表），所有模型均启用音频/视频流输入、文本流输出、上下文状态保持及实时事件反馈（如 `input_audio_buffer.committed`、`response.done`）。多模态能力（如语音转写+视觉理解联合推理）仅在 [接入模型与应用](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md) 文档中明确列出的模型上可用。

> **注意**：原始文档中 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 提到支持 `qwen1.5-14b-realtime`，但该模型已在 v2024.09 版本中下线；实际可用模型请以 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的最新支持列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为 Realtime 系列模型（如 `qwen2.5-7b-realtime`） |
| `temperature` | number | 否 | 采样温度，默认 `0.7`；设为 `0` 可启用确定性解码 |
| `max_output_tokens` | integer | 否 | 单次响应最大 token 数，上限 `4096`（超出将被截断） |
| `input_audio_format` | string | 否 | 音频编码格式，支持 `"pcm16"`（默认）、`"opus"`；详见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) |

## 使用方式

1. 建立 WebSocket 连接：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起握手，携带 `Authorization: Bearer <api_key>` 与 `X-DashScope-Model: <model_id>` 头；
2. 发送 `session.update` 消息初始化会话配置；
3. 分块发送 `input_audio_buffer.append` 或 `input_text` 消息；
4. 接收 `response.text.delta` 流式事件，并监听 `response.done` 完成信号。

完整流程示例见 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制和注意事项

- 单连接最长存活时间：300 秒（含空闲期），超时后需重连；
- 音频输入缓冲区最大长度：10 秒 PCM 数据（按 16kHz/16bit 计），超出部分将被丢弃；
- 不支持 `system` 角色消息；角色仅限 `user` 和 `assistant`；
- 所有请求必须启用 TLS 1.2+，禁用 HTTP 降级；
- 实时音频流需严格按帧时间戳对齐，时钟漂移超过 ±50ms 将触发 `input_audio_buffer.silence` 自动补偿 —— 此行为在 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 中已封装，但自建客户端需自行实现。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


