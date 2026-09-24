# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的实时推理接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持模型输出逐 token 流式返回与客户端指令实时注入。该接口不兼容传统 REST 同步调用模式，需按 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 文档规范接入。

## 支持的模型与功能

- 当前支持 `qwen-audio-realtime-v1`（语音实时转写与理解）、`qwen2.5-7b-realtime`（文本流式对话）及 `qwen-vl-realtime-v1`（多模态流式推理），具体以 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“接入模型与应用”章节为准。  
- 功能包括：流式 token 输出、客户端中断（`interrupt` 指令）、上下文动态追加（`append_message`）、音频帧增量输入（仅 audio/vl 模型）、服务端状态事件（如 `input_truncated`、`output_finished`）。  
- 注意：`qwen2.5-72b-realtime` 暂未开放商用，其能力描述见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)，但实际调用将返回 `404 model_not_found`，请以控制台模型列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中列出的支持列表一致 |
| `stream` | boolean | 是 | 固定为 `true`，Realtime API 不支持非流式模式 |
| `audio_format` | string | 条件必填 | 音频模型必需，取值 `pcm16` / `opus`；详见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) |
| `max_output_tokens` | integer | 否 | 单次会话最大生成 token 数，默认 1024，上限 4096 |

> **注意**：原始文档中 `temperature` 和 `top_p` 在 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 被列为可选参数，但实测 v202407 版本服务端已忽略二者，仅响应 `system_prompt` 和 `tools` 配置 —— 请以实际调试结果为准。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/{model}`，携带 `Authorization: Bearer <api_key>` 与 `X-DashScope-Date` 时间戳头；  
2. 发送 `session.update` 初始化消息（含 `system_prompt`, `tools` 等）；  
3. 发送 `input.audio` 或 `input.text` 帧启动推理；  
4. 监听 `output.text.delta`、`output.audio.delta` 等事件，按需响应 `interrupt` 或 `cancel`；  
5. 参考完整流程与错误码定义，请查阅 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制与注意事项

- 单连接最长存活 300 秒，超时后需重连并重建 session；  
- 音频流要求采样率 16kHz、单声道、PCM 小端序（`pcm16`），否则触发 `input_invalid` 错误；  
- 每秒最多发送 20 帧音频（每帧 ≤ 20ms），超出将被限流并丢弃后续帧；  
- 所有事件结构与状态码定义以 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 为准，该文档同步更新最全 schema；  
- 不支持跨 region 调用：连接 endpoint 必须与 API Key 所属 region 一致（如 `cn-beijing` Key 需使用 `wss://dashscope.aliyuncs.com/realtime/v1/...` 的北京节点）。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


