# omni realtime api

omni realtime api 是百炼平台提供的低延迟、流式多模态实时交互接口，支持语音输入/输出、文本流式响应与视觉理解能力的协同。该 API 采用 WebSocket 协议实现双向实时通信，适用于智能客服、实时翻译、语音助手等对端到端延迟敏感的场景。详细协议规范与事件定义见 [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)。

## 支持的模型/功能

- 当前仅支持 `qwen-omni-realtime` 模型（v1.0+），具备语音识别（ASR）、大语言模型推理（LLM）、语音合成（TTS）及可选视觉理解（VLM）的端到端联合建模能力。
- 支持声音复刻（Voice Cloning），需提前上传参考音频并生成 voice_id；具体流程参见 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。
- 支持多轮上下文维持、中断恢复、语义级流式响应（非 chunk 级），以及服务端主动触发的音效与状态事件。完整事件类型清单请查阅 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 和 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-omni-realtime`；其他模型名将被拒绝 |
| `voice_id` | string | 否 | 声音复刻 ID；若未提供，则使用默认 TTS 声音。详见 [声音复刻](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md) |
| `input_format` | string | 否 | `"pcm"`（默认）或 `"wav"`；采样率必须为 16kHz，单声道 |
| `output_format` | string | 否 | `"pcm"`（默认）或 `"mp3"`；影响 TTS 输出编码格式 |
| `enable_vision` | boolean | 否 | `false`（默认）；设为 `true` 时需在 `input` 中携带 base64 编码图像帧 |

> **注意**：原始文档中 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 描述的 `max_turns` 参数已在 v1.2 版本中移除，当前会话轮次由服务端自动管理，客户端无需传入。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/api/v1/omni-realtime`（鉴权通过 `Authorization: Bearer <api_key>` 头或 query 参数 `api_key`）  
2. 发送 `session.create` 控制消息初始化会话（含 `model`、`voice_id` 等参数）  
3. 流式发送音频数据帧（二进制）或文本/图像（JSON 格式 `input` 消息）  
4. 接收服务端推送的 `response.text.delta`、`response.audio.chunk`、`response.vision.result` 等事件  
5. 参考 SDK 快速接入：[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 与 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 提供了连接管理、事件解析与重连逻辑封装。

## 限制和注意事项

- 单次会话最大时长：10 分钟；超时后连接自动关闭，需重新创建 session  
- 音频输入帧间隔建议 ≤ 200ms；过长间隔可能导致 ASR 上下文断开  
- 视觉输入仅支持单帧 JPEG/PNG，尺寸不超过 1920×1080，base64 编码后长度 ≤ 4MB  
- 不支持跨 session 的上下文继承；如需[长期记忆](../concepts/memory.md)，须由应用层维护并显式注入 `system` 消息  
- 所有事件结构与错误码定义以 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 和 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 文档为准。

## 来源文档

- [实时多模态](../../raw/model-api-reference/omni-realtime-api.md)


