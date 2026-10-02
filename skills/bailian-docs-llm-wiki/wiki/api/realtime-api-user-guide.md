# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与实时事件通知（如中断、工具调用触发等）。该接口不兼容传统 REST 同步调用模式，需使用专用客户端或遵循指定握手与消息格式。

## 支持的模型与功能

- 当前支持 `qwen-audio-realtime-v1`、`qwen-video-realtime-v1` 及部分 `qwen2.5-*` 系列模型（详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)）。
- 核心功能包括：音频/视频流实时输入与响应、多轮上下文保持、工具调用（function calling）自动触发、说话人分离（speaker diarization）及中断检测（interrupt detection）。
- 不支持图像上传类能力（如多图理解），也不支持 `qwen-vl` 等视觉语言模型的离线批处理模式。相关模型能力边界请参考 [realtime-model-connection.md](../../raw/model-api-reference/realtime-api-user-guide/realtime-model-connection.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与接入文档中声明的模型列表一致 |
| `audio_format` / `video_format` | string | 否（但至少需指定其一） | 音频：`pcm-16k`、`opus-16k`；视频：`h264-30fps`、`av1-30fps`；格式不匹配将导致连接拒绝 |
| `enable_interruption` | boolean | 否 | 默认 `true`；设为 `false` 时禁用用户语音打断，适用于播报类场景 |
| `max_output_tokens` | integer | 否 | 最大生成 token 数，范围 `1–4096`；超出将主动终止响应流 |

> **注意**：`temperature` 和 `top_p` 在 Realtime API 中**不可配置**——模型内部采用固定采样策略以保障实时性，此行为与 [realtime-api-quick-start-guide.md](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中早期示例存在不一致，以当前服务端行为为准。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起带鉴权 header 的连接（`Authorization: Bearer <api_key>`）；
2. **发送初始化消息（`session.update`）**：包含 `model`、`audio_format` 等参数，完成会话配置；
3. **流式传输媒体帧**：按约定编码格式分帧发送二进制数据（`input.audio` 或 `input.video` 事件）；
4. **接收结构化响应**：服务端通过 `output.text.delta`、`tool.use`、`session.interrupted` 等事件实时推送结果。

完整交互流程与事件定义详见 [realtime-api-overview.md](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

## 限制和注意事项

- 单连接最长存活时间：**300 秒**（含握手与空闲期），超时后需重连；
- 音频流要求：PCM 格式须为 `signed-16-bit little-endian`，采样率严格为 `16000 Hz`，单帧时长建议 `20–40 ms`；
- 视频流要求：H.264 编码需为 `baseline profile`，关键帧间隔 ≤ 2 秒；
- 不支持跨连接共享 session state，每次新连接均为独立会话；
- AOQ 客户端 SDK（v1.2+）已封装上述协议细节，推荐优先使用，详见 [realtime-api-aoq-api.md](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


