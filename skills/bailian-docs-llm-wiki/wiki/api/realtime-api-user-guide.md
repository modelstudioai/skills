# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式交互式模型调用接口，适用于语音转写、实时对话、音视频流处理等场景。它基于 WebSocket 协议实现双向通信，支持模型响应的逐 token 流式返回与客户端指令的实时注入。该接口不兼容传统 REST 同步调用模式，需按事件驱动方式设计客户端逻辑。

## 支持的模型与功能

当前 Realtime API 支持以下模型（以 `qwen-audio-realtime` 和 `qwen-vl-realtime` 为主，后续将逐步扩展）：
- 音频流实时 ASR + LLM 推理（如语音会议实时摘要）
- 多模态流式理解（如摄像头视频帧+语音同步输入）
- 客户端可动态插入 `input_audio`、`cancel`、`pause` 等控制事件  
详细模型能力清单见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“接入模型与应用”章节。

## 关键参数

建立 WebSocket 连接时需在 URL 中携带以下必需查询参数：
- `model`: 模型标识符（如 `qwen-audio-realtime-202408`），必须与 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 兼容
- `api_key`: 项目级 API Key（非用户 [Token](../concepts/token.md)）
- `stream`: 固定为 `true`
- `response_format`: 可选 `json` 或 `delta`（默认 `delta`，用于流式 token 解析）

> **注意**：文档中提及的 `temperature` 参数在 Realtime API 中**不生效**；温度控制由服务端预设策略统一管理，客户端不可覆盖 —— 此行为与 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 中旧版示例存在矛盾，以当前运行时行为为准。

## 使用方式

1. 建立 WebSocket 连接：`wss://dashscope.aliyuncs.com/realtime/v1/chat?model=...&api_key=...`  
2. 发送 `session.update` 事件配置会话上下文（如 system [prompt](../guides/prompt.md)、input format）  
3. 通过 `input.audio` 事件持续推送音频 chunk（Base64 编码 PCM，16kHz 单声道）  
4. 监听 `output.text.delta` 事件接收流式响应，聚合后渲染  
完整事件协议与序列示例参见 [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md) 的“AOQ客户端SDK”子文档。

## 限制和注意事项

- 单连接最大时长：300 秒（含握手与空闲），超时后需重连  
- 音频输入采样率严格限定为 16kHz，其他采样率将被静音或截断  
- 不支持 `function calling` 和 `tool use`，所有交互必须通过 `input.text` / `input.audio` 显式触发  
- 错误码 `4290` 表示流控拒绝，此时应退避重试（指数退避，初始间隔 ≥ 1s）  
- 客户端必须实现 `ping/pong` 心跳（建议 20s 间隔），否则服务端可能主动断连  

请务必参考 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 中的生命周期图谱，避免在 `session.ended` 后继续发送事件。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


