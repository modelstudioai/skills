# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式语音交互接口，适用于实时语音识别（ASR）、语音合成（TTS）与多模态对话等场景。它基于 WebSocket 协议实现双向流式通信，支持端到端毫秒级响应。该接口不经过传统 REST 请求-响应周期，需按协议规范建立并维护长连接。

## 支持的模型与功能

当前 Realtime API 支持以下核心能力：
- 实时语音识别（ASR）：支持中文普通话、英文及部分方言，采样率 16kHz，PCM/WAV 格式输入；
- 实时语音合成（TTS）：支持情感化、多音色合成，输出为 PCM 流；
- 混合模式（ASR+TTS+LLM）：在单次会话中串联识别、大模型推理与合成，适用于智能座舱、客服机器人等闭环场景。

所支持的具体模型列表详见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节，其中明确列出 `qwen-audio-realtime-v1` 和 `qwen-tts-realtime-v2` 为当前 GA 版本模型。

## 关键参数

建立 WebSocket 连接时，必须携带以下查询参数（区分大小写）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-audio-realtime-v1`；值必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“接入模型与应用”章节所列一致 |
| `api_key` | string | 是 | 百炼平台颁发的短期有效凭证（JWT），有效期 5 分钟，需通过 `/v1/auth/token` 接口获取 |
| `sample_rate` | integer | 否 | 输入音频采样率，默认 `16000`；若非标准值，必须显式声明，否则连接将被拒绝 |

> **注意**：原始文档中 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 示例代码误将 `api_key` 写作 `access_token`，实际参数名应为 `api_key` —— 请以 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 主文档为准。

## 使用方式

1. **建立连接**：向 `wss://dashscope.aliyuncs.com/api/v1/realtime` 发起 WebSocket 连接，附带上述查询参数；
2. **发送控制帧**：首次消息须为 `{"type": "session.update", ...}`，用于配置 `input_audio_format`、`output_audio_format` 等会话级参数；
3. **流式收发**：后续按帧发送音频数据（Base64 编码的 PCM chunk）或接收结构化响应（含 `type: "response.audio.delta"` 或 `"response.text"`）；
4. **结束会话**：发送 `{"type": "session.end"}` 或关闭连接，服务端将在 3 秒内释放资源。

完整交互序列与事件类型定义参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“AOQ客户端SDK”子文档，该文档同时提供 Python/JS SDK 的初始化与错误重连示例。

## 限制和注意事项

- 单连接最大持续时长：15 分钟（超时后需重连）；
- 音频输入帧大小建议 ≤ 20ms（即 320 字节 @16kHz/16bit），过大帧将导致 ASR 延迟上升；
- 不支持跨区域 token 复用：华东1（`cn-shanghai`）签发的 `api_key` 无法用于华北2（`cn-beijing`）节点；
- 所有音频数据在传输中默认加密（TLS 1.3），但服务端**不持久化存储**原始音频流 —— 此行为与 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中“数据合规性”条款一致。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


