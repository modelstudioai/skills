# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式响应的模型调用接口，适用于语音交互、实时对话、音视频流处理等对端到端时延敏感的场景。它基于 WebSocket 协议实现双向通信，支持增量式 token 返回与实时中断控制。该接口不兼容传统 RESTful 同步调用模式，需使用专用客户端或 SDK 接入。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime-v1`、`qwen-video-realtime-v1` 和 `qwen-rtc-v2` 为主），均针对实时音频/视频流输入优化，具备语音活动检测（VAD）、流式 ASR、语义理解与 TTS 合成一体化能力。模型列表及能力详情请参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节。注意：`qwen-rtc-v1` 已于 2024-Q3 正式下线，文档中若仍提及该模型，请以 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中最新模型清单为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；必须与实际部署版本严格匹配 |
| `input_format` | string | 是 | 输入流格式，支持 `"pcm"`、`"opus"`、`"h264"`（视频）等，详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的 AOQ客户端SDK 文档 |
| `max_latency_ms` | integer | 否 | 端到端最大容忍延迟（毫秒），默认 `300`，取值范围 `100–2000` |
| `enable_vad` | boolean | 否 | 是否启用服务端 VAD，默认 `true`；设为 `false` 时需由客户端自行切分语音段 |

> **注意**：`temperature` 和 `top_p` 等采样参数在 Realtime API 中**不生效**，模型推理策略由服务端统一管控，此行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中描述一致，但与部分旧版 Quick Start 示例存在矛盾，请以本说明为准。

## 使用方式

1. 建立 WebSocket 连接：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接，携带 `Authorization: Bearer <api_key>` 头；
2. 发送 `session.update` 控制帧配置会话参数（如 `input_format`, `model`）；
3. 通过 `input.audio` 或 `input.video` 帧持续推送二进制流数据；
4. 监听 `output.text.delta`、`output.audio.delta` 等事件接收流式响应；
5. 如需中断当前响应，发送 `control.interrupt` 帧。

完整交互流程与错误码定义请参考 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md)。

## 限制和注意事项

- 单连接最长存活时间：10 分钟（超时后需重连）；
- 音频流采样率仅支持 `16000 Hz`（PCM）或 `48000 Hz`（Opus），其他采样率将被拒绝；
- 视频流分辨率建议 ≤ `640×480`，帧率 ≤ `15 fps`，超出可能触发服务端限流；
- 所有流式输入必须按时间顺序连续发送，乱序或重复帧将导致会话异常终止；
- 客户端必须实现心跳保活（每 30 秒发送 `ping` 帧），否则连接可能被中间代理关闭。

如遇连接频繁断开或延迟突增，建议优先检查网络稳定性，并确认是否符合 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 中的兼容性要求。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


