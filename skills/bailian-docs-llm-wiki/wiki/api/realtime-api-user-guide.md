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
| `model` | string | 是 | 模型 ID，如 `qwen-audio-realtime-v1`；值必须与 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 中“接入模型与应用”章节公布的模型列表严格一致 |
| `api_key` | string | 是 | 百炼平台生成的短期有效凭证（有效期 5 分钟），不可复用 |
| `stream` | boolean | 否 | 默认 `true`；设为 `false` 将退化为单次请求模式（不推荐，已知存在兼容性问题） |

> **注意**：原始文档中 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 示例使用了 `access_token` 参数，但该字段已于 v2.3.0 起废弃，实际服务端仅校验 `api_key`；请以 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 主文档为准。

## 使用方式

1. **建立连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/audio` 发起 WebSocket 连接，附带上述查询参数；
2. **发送控制帧**：首次消息须为 `{"type": "session.update", "turn_detection": {...}}`，用于配置静音检测与会话生命周期；
3. **流式传输音频**：后续以二进制帧发送原始 PCM 数据（16-bit little-endian，单声道），每帧建议 ≤ 200ms 音频；
4. **接收响应**：服务端按事件类型返回 JSON 控制帧（如 `transcript`、`audio`）或二进制音频帧。

完整交互序列与错误码定义参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“AOQ客户端SDK”章节，其中 SDK 已封装连接管理、重连逻辑与帧编解码。

## 限制和注意事项

- 单连接最大持续时长：15 分钟（超时后需重建连接）；
- 音频输入延迟要求：端到端 P95 < 300ms，建议客户端启用硬件加速采集；
- 不支持 HTTP/2 或 gRPC 替代协议，仅接受标准 WebSocket（`ws:`/`wss:`）；
- 所有音频数据未经加密传输至服务端，敏感场景需在客户端预处理脱敏；
- 多路并发连接数受项目配额限制，具体阈值请查阅 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 文档中的“配额与计费”小节。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


